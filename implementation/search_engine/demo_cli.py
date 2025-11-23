from search_tfidf import search_tfidf
from search_bm25 import search_bm25, BM25Okapi


def print_results(label, results, max_len_title=80):
    print(f"\n=== {label} ===")
    if not results:
        print("  (tidak ada hasil)")
        return

    for r in results:
        title = r["title"]
        if len(title) > max_len_title:
            title = title[:max_len_title].rstrip() + "..."
        print(f"[{r['rank']}] ({r['score']:.4f}) {title}")
        print(f"     {r['url']}")


if __name__ == "__main__":
    print("=== Demo CLI: Perbandingan TF-IDF vs BM25 ===")
    print("Ketik 'exit' untuk keluar.\n")

    # cek BM25 terinstall
    if BM25Okapi is None:
        print("Peringatan: BM25 (rank_bm25) belum terinstall. Jalankan: pip install rank-bm25")
        use_bm25 = False
    else:
        use_bm25 = True

    while True:
        q = input("\nQuery: ").strip()
        if q.lower() == "exit":
            break

        tfidf_res = search_tfidf(q, top_k=5)
        print_results("TF-IDF", tfidf_res)

        if use_bm25:
            bm25_res = search_bm25(q, top_k=5)
            print_results("BM25", bm25_res) 