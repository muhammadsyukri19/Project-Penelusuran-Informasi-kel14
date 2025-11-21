# PREPROCESSING DATASET - DOKUMENTASI

## 📁 Struktur Folder

```
preprocessing/
├── stopwords_id.py          # Daftar stopwords bahasa Indonesia
├── text_cleaner.py          # Modul untuk text cleaning
├── preprocess_pipeline.py   # Pipeline utama preprocessing
└── README.md               # Dokumentasi ini
```

## 🔄 Alur Preprocessing

```
Input: merge-all.csv (data mentah)
    ↓
Step 1: Text Cleaning
    - Hapus newline (\n, \r, \t)
    - Hapus extra whitespace
    - Hapus URL & email
    - Hapus punctuation
    - Normalize case (lowercase)
    - Hapus repeated characters
    ↓
Step 2: Remove Stopwords
    - Hapus kata-kata umum Indonesia
    - Hapus kata filler berita
    ↓
Step 3: Finalisasi
    - Cleanup final
    - Gabung title + content
    ↓
Output: merge-all-clean.csv (data bersih, siap indexing)
```

## 🚀 Cara Menggunakan

### Opsi 1: Jalankan Pipeline Utama (Recommended)

```bash
cd preprocessing
python preprocess_pipeline.py
```

### Opsi 2: Custom Configuration

Edit file `preprocess_pipeline.py`:

```python
# Ubah konfigurasi di bagian main()
CLEANING_LEVEL = 'standard'  # 'basic', 'standard', atau 'aggressive'
REMOVE_STOPWORDS = True       # True atau False
```

### Opsi 3: Gunakan sebagai Module

```python
from preprocessing.text_cleaner import TextCleaner
from preprocessing.stopwords_id import remove_stopwords_from_text

# Cleaning
cleaner = TextCleaner()
clean_text = cleaner.clean_standard("Text dengan \n newline")

# Remove stopwords
filtered = remove_stopwords_from_text("Persib akan bermain di Jakarta")
```

## ⚙️ Level Cleaning

### 1. Basic

- Hapus newline & extra whitespace
- Lowercase
- **Use case**: Masih ingin pertahankan struktur dasar

### 2. Standard (Recommended)

- Basic cleaning
- Hapus URL, email
- Hapus punctuation
- **Use case**: Untuk indexing & search

### 3. Aggressive

- Standard cleaning
- Hapus angka
- Hapus repeated characters
- **Use case**: NLP & machine learning

## 📊 Output

File output `merge-all-clean.csv` berisi kolom:

**Kolom Original:**

- id, source, url, title, content, main_image, images_count, content_length

**Kolom Baru (Hasil Preprocessing):**

- `title_clean` - Judul yang sudah dibersihkan
- `content_clean` - Konten yang sudah dibersihkan
- `text_combined` - Gabungan title + content (untuk indexing)

## 🔧 Customisasi

### Tambah Stopwords

Edit `stopwords_id.py`:

```python
CUSTOM_STOPWORDS = {
    'kata1', 'kata2', 'kata3'
}
```

### Ubah Cleaning Rules

Edit `text_cleaner.py` - sesuaikan method `clean_custom()` dengan kebutuhan.

## 📈 Statistik yang Ditampilkan

- Jumlah baris diproses
- Rata-rata panjang text sebelum & sesudah
- Persentase reduksi
- Sample hasil preprocessing

## 💡 Tips

1. **Untuk Indexing**: Gunakan level `standard` + remove stopwords
2. **Untuk Machine Learning**: Gunakan level `aggressive`
3. **Untuk Preview/Display**: Gunakan level `basic`
4. **Backup Data**: Script otomatis tidak menimpa file original

## ⚠️ Troubleshooting

**Error: Module not found**

```bash
# Pastikan di folder preprocessing
cd preprocessing
python preprocess_pipeline.py
```

**Error: File not found**

```bash
# Cek path input CSV di preprocess_pipeline.py
INPUT_CSV = "../data/merge-all.csv"  # Sesuaikan dengan lokasi file Anda
```

## 📝 Contoh Hasil

**Before:**

```
Title: Persib Bandung\nMengalahkan Persija Jakarta!!!
Content: Jakarta - Persib Bandung berhasil mengalahkan...
```

**After (Standard + Remove Stopwords):**

```
title_clean: persib bandung mengalahkan persija jakarta
content_clean: persib bandung berhasil mengalahkan persija...
text_combined: persib bandung mengalahkan persija jakarta persib bandung berhasil...
```

## 🎯 Next Steps

Setelah preprocessing selesai:

1. ✅ Data sudah bersih dan terstruktur
2. ➡️ Lanjut ke tahap **Indexing** (Whoosh/Elasticsearch)
3. ➡️ Build **Search Engine**
4. ➡️ Develop **Frontend UI**
