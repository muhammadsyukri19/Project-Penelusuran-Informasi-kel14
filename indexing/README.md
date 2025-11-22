# 📇 Indexing Pipeline

Pipeline untuk membuat index dari hasil preprocessing untuk sistem pencarian.

## 📁 Struktur Folder

```
indexing/
├── config.py                      # Konfigurasi terpusat
├── run_all_steps.py               # Master script untuk menjalankan semua step
├── README.md                      # Dokumentasi ini
├── steps/
│   ├── step1_build_inverted_index.py    # Build inverted index
│   ├── step2_calculate_tfidf.py         # Hitung TF-IDF weights
│   ├── step3_build_document_index.py    # Build document metadata index
│   └── step4_generate_statistics.py     # Generate statistik
└── utils/
    └── text_processor.py          # Utility functions untuk text processing
```

## 🔄 Alur Indexing

### Step 1: Build Inverted Index

- Input: `merge-all-clean.csv` (hasil preprocessing)
- Output: `inverted_index.json`, `vocabulary.json`
- Proses:
  - Tokenize text dari setiap dokumen
  - Build mapping: **term → document IDs**
  - Hitung frekuensi kemunculan term per dokumen
  - Simpan vocabulary lengkap

**Struktur Inverted Index:**

```json
{
  "persib": {
    "doc_ids": ["bolanet_3", "bolanet_5", ...],
    "doc_count": 15,
    "term_freq": {
      "bolanet_3": 5,
      "bolanet_5": 3
    }
  }
}
```

### Step 2: Calculate TF-IDF

- Input: `merge-all-clean.csv`, `inverted_index.json`
- Output: `tfidf_matrix.pkl`
- Proses:
  - Hitung **IDF (Inverse Document Frequency)** untuk setiap term
  - Hitung **TF (Term Frequency)** untuk setiap dokumen
  - Hitung **TF-IDF = TF × IDF**
  - Simpan dalam format pickle (lebih efisien)

**Formula:**

- TF = 1 + log(freq) jika SUBLINEAR_TF=True
- IDF = log((1 + N) / (1 + df)) + 1 jika SMOOTH_IDF=True
- N = total dokumen, df = document frequency

### Step 3: Build Document Index

- Input: `merge-all-clean.csv`
- Output: `document_index.json`
- Proses:
  - Extract metadata: id, source, title, url, image, word_count, dll
  - Simpan text preview (200 karakter pertama)
  - Create lookup table untuk retrieval

**Struktur Document Index:**

```json
{
  "bolanet_0": {
    "id": "bolanet_0",
    "source": "bolanet",
    "title": "...",
    "url": "...",
    "main_image": "...",
    "word_count": 341,
    "char_count": 2192,
    "text_preview": "..."
  }
}
```

### Step 4: Generate Statistics

- Input: Semua file index
- Output: `index_stats.json`
- Proses:
  - Hitung statistik vocabulary
  - Hitung statistik dokumen
  - Identifikasi term paling umum
  - Identifikasi term paling diskriminatif (IDF tinggi)
  - Analisis distribusi sumber berita

## 🚀 Cara Menjalankan

### Jalankan Semua Step

```bash
cd indexing
python run_all_steps.py
```

### Jalankan Step Individual

```bash
# Step 1: Build inverted index
python steps/step1_build_inverted_index.py

# Step 2: Calculate TF-IDF
python steps/step2_calculate_tfidf.py

# Step 3: Build document index
python steps/step3_build_document_index.py

# Step 4: Generate statistics
python steps/step4_generate_statistics.py
```

## ⚙️ Konfigurasi

Edit `config.py` untuk mengubah parameter:

```python
# Input/Output paths
INPUT_FILE = "data/merge-all-clean.csv"
INDEX_DIR = "data/index/"

# TF-IDF Parameters
MIN_DF = 1              # Minimum document frequency
MAX_DF = 0.95           # Maximum document frequency (ignore kata terlalu umum)
SUBLINEAR_TF = True     # Use 1 + log(tf) instead of raw tf
SMOOTH_IDF = True       # Add smoothing to IDF

# Processing
VERBOSE = True          # Show progress
BATCH_SIZE = 100        # Batch size untuk processing
```

## 📊 Output Files

Semua file index disimpan di `data/index/`:

1. **`inverted_index.json`** (1-5 MB)

   - Inverted index lengkap: term → documents
   - Untuk query lookup cepat

2. **`tfidf_matrix.pkl`** (5-20 MB)

   - TF-IDF weights untuk semua term-document pairs
   - Binary format (pickle) untuk efisiensi

3. **`document_index.json`** (500 KB - 2 MB)

   - Metadata lengkap semua dokumen
   - Untuk display hasil pencarian

4. **`vocabulary.json`** (200-500 KB)

   - Daftar lengkap semua term unik
   - Vocab size dan statistik

5. **`index_stats.json`** (50-100 KB)
   - Statistik komprehensif
   - Analisis term dan dokumen

## 📝 Catatan

- **Waktu eksekusi**: ~5-15 detik untuk 376 dokumen
- **Total size index**: ~10-30 MB
- **Memory usage**: ~200-500 MB saat processing
- **Format**: JSON untuk readability, Pickle untuk efficiency

## 🔍 Penggunaan Index

Index yang dibuat akan digunakan untuk:

1. **Query Processing**: Search dan ranking
2. **Document Retrieval**: Ambil dokumen relevan
3. **Relevance Scoring**: Hitung similarity score
4. **Search UI**: Display hasil pencarian

## ⚡ Tips

- Run step-by-step saat development/debugging
- Check `index_stats.json` untuk memahami karakteristik data
- Gunakan VERBOSE=True untuk melihat progress detail
- Backup index files sebelum re-indexing
