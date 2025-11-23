import os
import json
import re
import pickle
from typing import List, Dict, Any, Tuple

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None
    print("[WARN] rank_bm25 belum terinstall. Jalankan: pip install rank-bm25")


# ===================== KONFIGURASI =====================

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
INDEX_DIR = os.path.join(ROOT_DIR, "indexing")

CORPUS_PATTERN_SUFFIX = "_bola_indonesia.json"
BM25_INDEX_PATH = os.path.join(INDEX_DIR, "bm25_index.pkl")


def simple_tokenize(text: str) -> List[str]:
    """Tokenisasi sederhana untuk BM25."""
    if not text:
        return []
    text = text.lower()
    # pisah kata berdasarkan non-alphanumeric
    tokens = re.split(r"[^0-9a-zA-Zà-ž_]+", text)
    return [t for t in tokens if t]


def load_corpus() -> List[Dict[str, Any]]:
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
            if "title" not in item or "content" not in item:
                continue
            docs.append(item)

    for i, d in enumerate(docs):
        d["doc_id"] = i

    print(f"[BM25] Loaded {len(docs)} documents from data/")
    return docs


def build_or_load_bm25_index() -> Tuple[BM25Okapi, List[List[str]], List[Dict[str, Any]]]:
    if BM25Okapi is None:
        raise ImportError("rank_bm25 belum diinstall. Jalankan: pip install rank-bm25")

    os.makedirs(INDEX_DIR, exist_ok=True)

    if os.path.exists(BM25_INDEX_PATH):
        with open(BM25_INDEX_PATH, "rb") as f:
            data = pickle.load(f)
        print("[BM25] Index loaded from", BM25_INDEX_PATH)
        return data["bm25"], data["corpus_tokens"], data["docs"]

    docs = load_corpus()
    corpus_tokens = []

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
    if not content:
        return ""
    content = content.replace("\n", " ")
    if len(content) <= max_len:
        return content
    return content[:max_len].rsplit(" ", 1)[0] + "..."


def search_bm25(query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    bm25, corpus_tokens, docs = build_or_load_bm25_index()

    q_tokens = simple_tokenize(query)
    scores = bm25.get_scores(q_tokens)

    # ambil index dokumen dengan skor tertinggi
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    results = []
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
                "published_at": doc.get("published_at"),
                "doc_id": doc.get("doc_id", idx),
            }
        )

    return results


if __name__ == "__main__":
    print("=== Demo BM25 Search ===")
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