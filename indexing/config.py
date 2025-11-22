"""
Konfigurasi untuk Indexing Pipeline
"""
import os

# ===================== PATH CONFIGURATION =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_DIR = os.path.join(DATA_DIR, "index")  # Folder khusus untuk index results

# Input file (hasil preprocessing)
INPUT_FILE = os.path.join(DATA_DIR, "merge-all-clean.csv")

# Output files untuk setiap step
INVERTED_INDEX_FILE = os.path.join(INDEX_DIR, "inverted_index.json")
DOCUMENT_INDEX_FILE = os.path.join(INDEX_DIR, "document_index.json")
TFIDF_MATRIX_FILE = os.path.join(INDEX_DIR, "tfidf_matrix.pkl")
VOCABULARY_FILE = os.path.join(INDEX_DIR, "vocabulary.json")
INDEX_STATS_FILE = os.path.join(INDEX_DIR, "index_stats.json")

# ===================== INDEXING PARAMETERS =====================
# Kolom yang akan diindex
TEXT_COLUMN = "text_combined"  # Kolom hasil preprocessing yang sudah digabung

# Metadata columns
METADATA_COLUMNS = ["id", "source", "url", "title", "main_image", "word_count", "char_count"]

# TF-IDF Parameters
MIN_DF = 1  # Minimum document frequency (kata muncul minimal di berapa dokumen)
MAX_DF = 0.95  # Maximum document frequency (ignore kata yang terlalu umum)
USE_IDF = True  # Gunakan IDF weighting
SMOOTH_IDF = True  # Smooth IDF weights
SUBLINEAR_TF = True  # Use sublinear TF scaling (1 + log(tf))

# Index options
SAVE_RAW_COUNTS = True  # Simpan raw term frequency
CALCULATE_TFIDF = True  # Hitung TF-IDF weights
BUILD_INVERTED_INDEX = True  # Build inverted index

# Performance
VERBOSE = True  # Show progress
BATCH_SIZE = 100  # Untuk processing dalam batch

# ===================== CREATE INDEX DIRECTORY =====================
os.makedirs(INDEX_DIR, exist_ok=True)
