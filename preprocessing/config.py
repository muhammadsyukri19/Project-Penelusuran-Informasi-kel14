"""
Konfigurasi terpusat untuk preprocessing pipeline
"""
import os

# ===================== PATH CONFIGURATION =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

INPUT_FILE = os.path.join(DATA_DIR, "merge-all.csv")

# Step outputs - each step feeds into next step
STEP1_OUTPUT = os.path.join(DATA_DIR, "preprocessing_step2.csv")  # Output step1 → Input step2
STEP2_OUTPUT = os.path.join(DATA_DIR, "preprocessing_step3.csv")  # Output step2 → Input step3
STEP3_OUTPUT = os.path.join(DATA_DIR, "preprocessing_step4.csv")  # Output step3 → Input step4 (stemming)
STEP4_OUTPUT = os.path.join(DATA_DIR, "preprocessing_step5.csv")  # Output step4 (stemming) → Input step5 (finalize)

# Final output
FINAL_OUTPUT = os.path.join(DATA_DIR, "merge-all-clean.csv")
STATS_OUTPUT = os.path.join(DATA_DIR, "preprocessing_stats.json")

# ===================== PREPROCESSING PARAMETERS =====================
TEXT_COLUMNS = ["content"]
REMOVE_NEWLINES = True  # PENTING: Hapus \n, \r, \t
LOWERCASE = True
REMOVE_PUNCTUATION = True
KEEP_NUMBERS = True
REMOVE_STOPWORDS = True
USE_SASTRAWI = True
MIN_WORD_LENGTH = 2
VERBOSE = True