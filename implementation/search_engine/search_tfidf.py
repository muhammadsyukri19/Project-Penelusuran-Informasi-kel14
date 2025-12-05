import os
import re
import pickle
from typing import List, Dict, Any, Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ===================== KONFIGURASI =====================

# path relatif dari file ini ke root repo
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
INDEX_DIR = os.path.join(ROOT_DIR, "indexing")

# pakai dataset hasil preprocessing
DATA_PATH = os.path.join(DATA_DIR, "merge-all-dual-storage.csv")

TFIDF_INDEX_PATH = os.path.join(INDEX_DIR, "tfidf_index.pkl")


# ===================== UTILITAS =====================

def simple_preprocess(text: str) -> str:
    """Preprocessing ringan untuk TF-IDF (lowercase + buang whitespace aneh)."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_corpus_from_csv() -> List[Dict[str, Any]]:
    """
    Load korpus dari file CSV dengan DUAL STORAGE:
    data/merge-all-dual-storage.csv

    Kolom:
      - 'title' (ORIGINAL untuk display)
      - 'title_clean' (CLEAN untuk indexing)
      - 'content' (ORIGINAL untuk display)
      - 'content_clean' (CLEAN untuk indexing)
      - 'url', 'main_image', 'source' (metadata)
    """
    if not os.path.isfile(DATA_PATH):
        raise FileNotFoundError(f"Dataset CSV tidak ditemukan: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # cek kolom wajib
    required_cols = ['title', 'content', 'title_clean', 'content_clean']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(
            f"CSV harus punya kolom: {required_cols}. "
            f"Kolom yang hilang: {missing}"
        )

    docs: List[Dict[str, Any]] = []
    for i, row in df.iterrows():
        doc = {
            "doc_id": str(row.get("doc_id", i)) if "doc_id" in df.columns else int(i),
            # ORIGINAL data (untuk display)
            "title": str(row.get("title", "")) if not pd.isna(row.get("title", "")) else "",
            "content": str(row.get("content", "")) if not pd.isna(row.get("content", "")) else "",
            # CLEAN data (untuk indexing)
            "title_clean": str(row.get("title_clean", "")) if not pd.isna(row.get("title_clean", "")) else "",
            "content_clean": str(row.get("content_clean", "")) if not pd.isna(row.get("content_clean", "")) else "",
            # Metadata
            "url": str(row.get("url", "")) if "url" in df.columns and not pd.isna(row.get("url", "")) else "",
            "main_image": str(row.get("main_image", "")) if "main_image" in df.columns and not pd.isna(row.get("main_image", "")) else "",
            "source": str(row.get("source", "")) if "source" in df.columns and not pd.isna(row.get("source", "")) else "",
            "published_at": (
                str(row.get("published_at", ""))
                if "published_at" in df.columns and not pd.isna(row.get("published_at", ""))
                else None
            ),
        }

        # skip kalau title + content kosong
        if not doc["title"] and not doc["content"]:
            continue

        docs.append(doc)

    print(f"[TF-IDF] Loaded {len(docs)} documents from CSV: {DATA_PATH}")
    return docs


def build_or_load_tfidf_index() -> Tuple[TfidfVectorizer, Any, List[Dict[str, Any]]]:
    """
    Kalau index sudah ada di indexing/tfidf_index.pkl → load.
    Kalau belum → build dari merge-all-clean.csv lalu simpan.
    """
    os.makedirs(INDEX_DIR, exist_ok=True)

    if os.path.exists(TFIDF_INDEX_PATH):
        with open(TFIDF_INDEX_PATH, "rb") as f:
            data = pickle.load(f)
        print("[TF-IDF] Index loaded from", TFIDF_INDEX_PATH)
        return data["vectorizer"], data["doc_matrix"], data["docs"]

    # build baru dari CSV
    docs = load_corpus_from_csv()
    texts = []
    for d in docs:
        # Gunakan CLEAN data untuk indexing
        title_clean = d.get("title_clean", "")
        content_clean = d.get("content_clean", "")
        full_text = f"{title_clean}\n{content_clean}"
        texts.append(simple_preprocess(full_text))

    vectorizer = TfidfVectorizer(
        max_features=50000,
        ngram_range=(1, 2),
    )
    doc_matrix = vectorizer.fit_transform(texts)

    with open(TFIDF_INDEX_PATH, "wb") as f:
        pickle.dump(
            {
                "vectorizer": vectorizer,
                "doc_matrix": doc_matrix,
                "docs": docs,
            },
            f,
        )
    print("[TF-IDF] Index built and saved to", TFIDF_INDEX_PATH)
    return vectorizer, doc_matrix, docs


def make_snippet(content: str, max_len: int = 250) -> str:
    """Ambil potongan awal konten sebagai snippet."""
    if not content:
        return ""
    content = content.replace("\n", " ")
    if len(content) <= max_len:
        return content
    return content[:max_len].rsplit(" ", 1)[0] + "..."


# ===================== SEARCH FUNCTION =====================

def search_tfidf(query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Jalankan pencarian menggunakan TF-IDF + Cosine Similarity.
    Return: list dict {rank, score, title, url, snippet, published_at}
    """
    vectorizer, doc_matrix, docs = build_or_load_tfidf_index()

    q = simple_preprocess(query)
    q_vec = vectorizer.transform([q])

    sims = cosine_similarity(q_vec, doc_matrix)[0]  # shape: (n_docs,)
    top_idx = sims.argsort()[::-1][:top_k]

    results = []
    for rank, idx in enumerate(top_idx, start=1):
        doc = docs[idx]
        score = float(sims[idx])

        results.append(
            {
                "rank": rank,
                "score": score,
                # Return ORIGINAL data untuk display
                "title": doc.get("title", ""),
                "url": doc.get("url", ""),
                "snippet": make_snippet(doc.get("content", "")),  # ORIGINAL content
                "main_image": doc.get("main_image", ""),
                "source": doc.get("source", ""),
                "published_at": doc.get("published_at"),
                "doc_id": doc.get("doc_id", idx),
            }
        )

    return results


# ===================== DEMO =====================

if __name__ == "__main__":
    print("=== Demo TF-IDF Search (CSV: merge-all-clean.csv) ===")
    vectorizer, doc_matrix, docs = build_or_load_tfidf_index()

    while True:
        q = input("\nMasukkan query (atau 'exit'): ").strip()
        if q.lower() == "exit":
            break

        res = search_tfidf(q, top_k=5)
        if not res:
            print("Tidak ada hasil.")
            continue

        for r in res:
            print(f"[{r['rank']}] ({r['score']:.4f}) {r['title']}")
            print(f"     {r['url']}")
            print(f"     {r['snippet']}\n")