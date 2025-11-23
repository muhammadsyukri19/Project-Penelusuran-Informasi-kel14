import os
import json
import re
import pickle
from typing import List, Dict, Any, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ===================== KONFIGURASI =====================

# path relatif dari file ini ke root repo
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
INDEX_DIR = os.path.join(ROOT_DIR, "indexing")

CORPUS_PATTERN_SUFFIX = "_bola_indonesia.json"
TFIDF_INDEX_PATH = os.path.join(INDEX_DIR, "tfidf_index.pkl")


# ===================== UTILITAS =====================

def simple_preprocess(text: str) -> str:
    """Preprocessing ringan untuk TF-IDF (lowercase + buang karakter aneh)."""
    if not text:
        return ""
    text = text.lower()
    # bisa ditambah stopword removal / stemming nanti
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_corpus() -> List[Dict[str, Any]]:
    """
    Load semua file JSON di folder data/ yang namanya diakhiri dengan `_bola_indonesia.json`.
    Masing-masing file berisi list artikel: {url, title, content, ...}.
    """
    docs = []
    if not os.path.isdir(DATA_DIR):
        raise FileNotFoundError(f"Folder data tidak ditemukan: {DATA_DIR}")

    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(CORPUS_PATTERN_SUFFIX):
            continue
        fpath = os.path.join(DATA_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            try:
                items = json.load(f)
            except json.JSONDecodeError:
                print(f"[WARN] Gagal parse JSON: {fpath}")
                continue

        for item in items:
            # pastikan ada field minimal
            if "title" not in item or "content" not in item:
                continue
            docs.append(item)

    # beri id numerik
    for i, d in enumerate(docs):
        d["doc_id"] = i

    print(f"[TF-IDF] Loaded {len(docs)} documents from data/")
    return docs


def build_or_load_tfidf_index() -> Tuple[TfidfVectorizer, Any, List[Dict[str, Any]]]:
    """
    Kalau index sudah ada di indexing/tfidf_index.pkl → load.
    Kalau belum → build dari awal lalu simpan.
    """
    os.makedirs(INDEX_DIR, exist_ok=True)

    if os.path.exists(TFIDF_INDEX_PATH):
        with open(TFIDF_INDEX_PATH, "rb") as f:
            data = pickle.load(f)
        print("[TF-IDF] Index loaded from", TFIDF_INDEX_PATH)
        return data["vectorizer"], data["doc_matrix"], data["docs"]

    # build baru
    docs = load_corpus()
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
    # ambil index dokumen dengan skor tertinggi
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
    print("=== Demo TF-IDF Search ===")
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