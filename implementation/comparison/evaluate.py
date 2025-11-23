import os
import sys
import json
from typing import List, Dict, Callable, Any

# ===================== PERBAIKAN PENTING =====================
# Tambahkan root project ke sys.path supaya "implementation" bisa di-import
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ROOT_DIR)

# Setelah sys.path ditambah, baru import modul search_engine
from implementation.search_engine.search_tfidf import search_tfidf
from implementation.search_engine.search_bm25 import search_bm25


# ===================== KONFIGURASI =====================

RESULT_PATH = os.path.join(os.path.dirname(__file__), "results_tfidf_bm25.json")
QUERIES_FILE = os.path.join(os.path.dirname(__file__), "queries_example.json")


# ===================== METRIK IR =====================

def precision_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    if k <= 0:
        return 0.0
    top_k = retrieved[:k]
    if not top_k:
        return 0.0

    rel_set = set(relevant)
    hit = sum(1 for url in top_k if url in rel_set)
    return hit / len(top_k)


def average_precision(retrieved: List[str], relevant: List[str]) -> float:
    rel_set = set(relevant)
    if not rel_set:
        return 0.0

    score = 0.0
    hit = 0

    for i, url in enumerate(retrieved, start=1):
        if url in rel_set:
            hit += 1
            score += hit / i

    return score / len(rel_set)


# ===================== LOAD QUERIES & GROUND TRUTH =====================

def load_queries_and_ground_truth():
    """
    Format queries_example.json:
    [
      {
        "query": "persib bandung",
        "relevant_urls": ["url1", "url2", ...]
      }
    ]
    """
    with open(QUERIES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    queries: List[str] = []
    ground_truth: Dict[str, List[str]] = {}

    for item in data:
        q = item.get("query", "").strip()
        rel = item.get("relevant_urls", [])
        if not q:
            continue
        queries.append(q)
        ground_truth[q] = rel

    return queries, ground_truth


# ===================== EVALUASI METODE =====================

def evaluate_method(
    name: str,
    search_fn: Callable[[str, int], List[Dict[str, Any]]],
    queries: List[str],
    ground_truth: Dict[str, List[str]],
    top_k: int = 10,
) -> Dict[str, Any]:

    print(f"\n=== Evaluasi {name} ===")
    ap_scores = []
    details = []

    for q in queries:
        rel = ground_truth.get(q, [])
        results = search_fn(q, top_k=top_k)

        retrieved_urls = [r.get("url", "") for r in results]

        ap = average_precision(retrieved_urls, rel)
        p5 = precision_at_k(retrieved_urls, rel, 5)
        p10 = precision_at_k(retrieved_urls, rel, 10)

        ap_scores.append(ap)

        details.append(
            {
                "query": q,
                "relevant_urls": rel,
                "retrieved_urls": retrieved_urls,
                "AP": ap,
                "P@5": p5,
                "P@10": p10,
            }
        )

        print(f"- Query: {q}")
        print(f"  AP={ap:.4f}, P@5={p5:.4f}, P@10={p10:.4f}")

    map_score = sum(ap_scores) / len(ap_scores) if ap_scores else 0.0

    print(f"\nMAP {name}: {map_score:.4f}")

    return {
        "method": name,
        "MAP": map_score,
        "per_query": details,
    }


# ===================== MAIN =====================

def main():
    queries, ground_truth = load_queries_and_ground_truth()

    print(f"Queries to evaluate: {len(queries)}")

    tfidf_result = evaluate_method("TF-IDF", search_tfidf, queries, ground_truth)
    bm25_result = evaluate_method("BM25", search_bm25, queries, ground_truth)

    all_results = {
        "TF-IDF": tfidf_result,
        "BM25": bm25_result,
    }

    with open(RESULT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\nDetail disimpan di: {RESULT_PATH}")


if __name__ == "__main__":
    main()