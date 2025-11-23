import json
import os
from typing import List, Dict, Any

from implementation.search_engine.search_tfidf import search_tfidf
from implementation.search_engine.search_bm25 import search_bm25

# ===================== KONFIGURASI =====================

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COMPARISON_DIR = os.path.dirname(__file__)

QUERIES_PATH = os.path.join(COMPARISON_DIR, "queries_example.json")
RESULTS_PATH = os.path.join(COMPARISON_DIR, "results_tfidf_bm25.json")

TOP_K = 10


# ===================== GROUND TRUTH =====================

"""
GROUND_TRUTH berisi daftar dokumen relevan untuk setiap query.

Kamu bisa isi pakai URL artikel (paling gampang), contohnya:
GROUND_TRUTH = {
    "persib dewa united": [
        "https://bola.kompas.com/read/...persib-usai-acl-2...",
        "https://www.bola.net/indonesia/6-kemenangan-beruntun-jadi-modal-penting-persib-bandung-siap-hadapi-dewa-united..."
    ],
    ...
}
"""

GROUND_TRUTH: Dict[str, List[str]] = {
    # TODO: isi manual berdasarkan penilaianmu
    # "persib dewa united": [
    #     "https://bola.kompas.com/read/2025/11/10/15332998/jadwal-persib-usai-acl-2-lawan-dewa-united-dan-lion-city-sailors",
    #     "https://www.bola.net/indonesia/6-kemenangan-beruntun-jadi-modal-penting-persib-bandung-siap-hadapi-dewa-united-di-bri-super--1b3200.html"
    # ],
}


# ===================== METRIK =====================

def precision_at_k(retrieved_urls: List[str], relevant_urls: List[str], k: int) -> float:
    if k == 0:
        return 0.0
    retrieved_k = retrieved_urls[:k]
    if not retrieved_k:
        return 0.0
    rel_set = set(relevant_urls)
    hit = sum(1 for url in retrieved_k if url in rel_set)
    return hit / len(retrieved_k)


def average_precision(retrieved_urls: List[str], relevant_urls: List[str], k: int) -> float:
    rel_set = set(relevant_urls)
    if not rel_set:
        return 0.0

    precisions = []
    hits = 0
    for i, url in enumerate(retrieved_urls[:k], start=1):
        if url in rel_set:
            hits += 1
            precisions.append(hits / i)

    if not precisions:
        return 0.0

    return sum(precisions) / len(rel_set)


def mean_average_precision(all_ap: List[float]) -> float:
    if not all_ap:
        return 0.0
    return sum(all_ap) / len(all_ap)


# ===================== EVALUASI =====================

def evaluate_method(method_name: str, search_func, queries: List[str]) -> Dict[str, Any]:
    per_query = []
    aps = []

    for q in queries:
        rel = GROUND_TRUTH.get(q, [])
        res = search_func(q, top_k=TOP_K)
        urls = [r["url"] for r in res]

        p5 = precision_at_k(urls, rel, 5)
        p10 = precision_at_k(urls, rel, 10)
        ap = average_precision(urls, rel, TOP_K)

        aps.append(ap)
        per_query.append(
            {
                "query": q,
                "relevant_count": len(rel),
                "precision@5": p5,
                "precision@10": p10,
                "AP": ap,
                "top_urls": urls,
            }
        )

    map_score = mean_average_precision(aps)

    return {
        "method": method_name,
        "MAP": map_score,
        "detail": per_query,
    }


def main():
    # load queries
    with open(QUERIES_PATH, "r", encoding="utf-8") as f:
        queries = json.load(f)

    print("Queries to evaluate:", len(queries))

    tfidf_result = evaluate_method("TF-IDF", search_tfidf, queries)
    bm25_result = evaluate_method("BM25", search_bm25, queries)

    results = {
        "TF-IDF": tfidf_result,
        "BM25": bm25_result,
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n=== Ringkasan ===")
    print(f"MAP TF-IDF: {tfidf_result['MAP']:.4f}")
    print(f"MAP BM25 : {bm25_result['MAP']:.4f}")
    print("\nDetail disimpan di:", RESULTS_PATH)


if __name__ == "__main__":
    main()