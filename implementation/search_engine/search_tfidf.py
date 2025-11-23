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
DATA_PATH = os.path.join(DATA_DIR, "merge-all-clean.csv")

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
    Load korpus dari file CSV hasil preprocessing:
    data/merge-all-clean.csv

    Diasumsikan kolom minimal:
      - 'title'
      - 'content'
      - 'url'           (optional, kalau tidak ada akan dikosongkan)
      - 'published_at'  (optional)
    """
    if not os.path.isfile(DATA_PATH):
        raise FileNotFoundError(f"Dataset CSV tidak ditemukan: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # cek kolom wajib
    if "title" not in df.columns or "content" not in df.columns:
        raise ValueError(
            "CSV harus punya kolom 'title' dan 'content'. "
            f"Kolom yang ada sekarang: {list(df.columns)}"
        )

    docs: List[Dict[str, Any]] = []
    for i, row in df.iterrows():
        doc = {
            "doc_id": int(i),
            "title": str(row.get("title", "")) if not pd.isna(row.get("title", "")) else "",
            "content": str(row.get("content", "")) if not pd.isna(row.get("content", "")) else "",
            "url": str(row.get("url", "")) if "url" in df.columns and not pd.isna(row.get("url", "")) else "",
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
        title = d.get("title", "")
        content = d.get("content", "")
        full_text = f"{title}\n{content}"
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
                "title": doc.get("title", ""),
                "url": doc.get("url", ""),
                "snippet": make_snippet(doc.get("content", "")),
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