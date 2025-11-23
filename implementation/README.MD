# Implementation: Search Engine & Algorithm Comparison

Folder ini berisi:

- Implementasi search engine menggunakan:
  - TF-IDF (Cosine Similarity)
  - BM25
- Script untuk:
  - Mencari berita bola Indonesia via CLI
  - Membandingkan performa TF-IDF vs BM25

Struktur:

- `search_engine/`
  - `search_tfidf.py`  → fungsi search berbasis TF-IDF
  - `search_bm25.py`   → fungsi search berbasis BM25
  - `demo_cli.py`      → demo sederhana di terminal

- `comparison/`
  - `queries_example.json` → contoh query untuk evaluasi
  - `evaluate.py`          → hitung Precision@k, MAP, dll
  - `compare_tfidf_bm25.ipynb` → notebook analisis (isi contoh ada di bawah, bisa dibuat manual di Jupyter)

> Catatan:
> - Script mencari data JSON hasil crawling di folder `data/` (relatif dari root repo).
> - Semua file `*_bola_indonesia.json` akan digabung sebagai satu korpus.