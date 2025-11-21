"""
Konfigurasi terpusat untuk preprocessing pipeline
"""
import os

# ===================== PATH CONFIGURATION =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

INPUT_FILE = os.path.join(DATA_DIR, "merge-all.csv")
STEP1_OUTPUT = os.path.join(DATA_DIR, "step1_basic_cleaned.csv")
STEP2_OUTPUT = os.path.join(DATA_DIR, "step2_normalized.csv")
STEP3_OUTPUT = os.path.join(DATA_DIR, "step3_no_stopwords.csv")
FINAL_OUTPUT = os.path.join(DATA_DIR, "merge-all-clean.csv")
STATS_OUTPUT = os.path.join(DATA_DIR, "preprocessing_stats.json")

# ===================== PREPROCESSING PARAMETERS =====================
TEXT_COLUMNS = ["title", "content"]
REMOVE_NEWLINES = True  # PENTING: Hapus \n, \r, \t
LOWERCASE = True
REMOVE_PUNCTUATION = True
KEEP_NUMBERS = True
REMOVE_STOPWORDS = True
USE_SASTRAWI = True
MIN_WORD_LENGTH = 2
VERBOSE = True