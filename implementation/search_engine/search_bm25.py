import os
import re
import pickle
from typing import List, Dict, Any, Tuple

import pandas as pd

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None
    print("[WARN] rank_bm25 belum terinstall. Jalankan: pip install rank-bm25")


# ===================== KONFIGURASI =====================

# path relatif dari file ini ke root repo
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
INDEX_DIR = os.path.join(ROOT_DIR, "indexing")

# pakai dataset hasil preprocessing (sama seperti TF-IDF CSV)
DATA_PATH = os.path.join(DATA_DIR, "merge-all-clean.csv")
BM25_INDEX_PATH = os.path.join(INDEX_DIR, "bm25_index.pkl")


# ===================== UTILITAS =====================

def simple_tokenize(text: str) -> List[str]:
    """Tokenisasi sederhana untuk BM25."""
    if not text:
        return []
    text = text.lower()
    # pisah kata berdasarkan non-alphanumeric
    tokens = re.split(r"[^0-9a-zA-Zà-ž_]+", text)
    return [t for t in tokens if t]


def load_corpus_from_csv() -> List[Dict[str, Any]]:
    """
    Load korpus dari file CSV hasil preprocessing:
    data/merge-all-clean.csv

    Diasumsikan kolom minimal:
      - 'title'
      - 'content'
      - 'url' (optional)
      - 'published_at' (optional)
    """
    if not os.path.isfile(DATA_PATH):
        raise FileNotFoundError(f"Dataset CSV tidak ditemukan: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    if "title" not in df.columns or "content" not in df.columns:
        raise ValueError(
            "CSV harus punya kolom 'title' dan 'content'. "
            f"Kolom yang ada sekarang: {list(df.columns)}"
        )

    docs: List[Dict[str, Any]] = []
    for i, row in df.iterrows():
        doc = {
            "doc_id": int(i),
            "title": (
                str(row.get("Title", ""))
                if "Title" in df.columns and not pd.isna(row.get("Title", ""))
                else str(row.get("title", "")) if not pd.isna(row.get("title", "")) else ""
            ),
            "content": (
                str(row.get("content", ""))
                if not pd.isna(row.get("content", ""))
                else ""
            ),
            "url": (
                str(row.get("url", ""))
                if "url" in df.columns and not pd.isna(row.get("url", ""))
                else ""
            ),
            "main_image": (
                str(row.get("main_image", ""))
                if "main_image" in df.columns and not pd.isna(row.get("main_image", ""))
                else ""
            ),
            "source": (
                str(row.get("source", ""))
                if "source" in df.columns and not pd.isna(row.get("source", ""))
                else ""
            ),
            "published_at": (
                str(row.get("published_at", ""))
                if "published_at" in df.columns
                and not pd.isna(row.get("published_at", ""))
                else None
            ),
        }

        # skip kalau title + content kosong
        if not doc["title"] and not doc["content"]:
            continue

        docs.append(doc)

    print(f"[BM25] Loaded {len(docs)} documents from CSV: {DATA_PATH}")
    return docs


def build_or_load_bm25_index() -> Tuple[BM25Okapi, List[List[str]], List[Dict[str, Any]]]:
    """
    Kalau index sudah ada di indexing/bm25_index.pkl → load.
    Kalau belum → build dari merge-all-clean.csv lalu simpan.
    """
    if BM25Okapi is None:
        raise ImportError("rank_bm25 belum diinstall. Jalankan: pip install rank-bm25")

    os.makedirs(INDEX_DIR, exist_ok=True)

    if os.path.exists(BM25_INDEX_PATH):
        with open(BM25_INDEX_PATH, "rb") as f:
            data = pickle.load(f)
        print("[BM25] Index loaded from", BM25_INDEX_PATH)
        return data["bm25"], data["corpus_tokens"], data["docs"]

    # build baru dari CSV
    docs = load_corpus_from_csv()
    corpus_tokens: List[List[str]] = []

    for d in docs:
        title = d.get("title", "")
        content = d.get("content", "")
        full_text = f"{title}\n{content}"
        tokens = simple_tokenize(full_text)
        corpus_tokens.append(tokens)

    bm25 = BM25Okapi(corpus_tokens)

    with open(BM25_INDEX_PATH, "wb") as f:
        pickle.dump(
            {
                "bm25": bm25,
                "corpus_tokens": corpus_tokens,
                "docs": docs,
            },
            f,
        )
    print("[BM25] Index built and saved to", BM25_INDEX_PATH)
    return bm25, corpus_tokens, docs


def make_snippet(content: str, max_len: int = 250) -> str:
    """Ambil potongan awal konten sebagai snippet."""
    if not content:
        return ""
    content = content.replace("\n", " ")
    if len(content) <= max_len:
        return content
    return content[:max_len].rsplit(" ", 1)[0] + "..."


# ===================== SEARCH FUNCTION =====================

def search_bm25(query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Jalankan pencarian menggunakan BM25.
    Return: list dict {rank, score, title, url, snippet, published_at}
    """
    bm25, corpus_tokens, docs = build_or_load_bm25_index()

    q_tokens = simple_tokenize(query)
    scores = bm25.get_scores(q_tokens)

    # ambil index dokumen dengan skor tertinggi
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    results: List[Dict[str, Any]] = []
    for rank, idx in enumerate(top_idx, start=1):
        doc = docs[idx]
        score = float(scores[idx])

        results.append(
            {
                "rank": rank,
                "score": score,
                "title": doc.get("title", ""),
                "url": doc.get("url", ""),
                "snippet": make_snippet(doc.get("content", "")),
                "main_image": doc.get("main_image", ""),
                "source": doc.get("source", ""),
                "published_at": doc.get("published_at"),
                "doc_id": doc.get("doc_id", idx),
            }
        )

    return results


# ===================== DEMO =====================

if __name__ == "__main__":
    print("=== Demo BM25 Search (CSV: merge-all-clean.csv) ===")
    if BM25Okapi is None:
        print("Install dulu: pip install rank-bm25")
        raise SystemExit

    bm25, corpus_tokens, docs = build_or_load_bm25_index()

    while True:
        q = input("\nMasukkan query (atau 'exit'): ").strip()
        if q.lower() == "exit":
            break

        res = search_bm25(q, top_k=5)
        if not res:
            print("Tidak ada hasil.")
            continue

        for r in res:
            print(f"[{r['rank']}] ({r['score']:.4f}) {r['title']}")
            print(f"     {r['url']}")
            print(f"     {r['snippet']}\n")