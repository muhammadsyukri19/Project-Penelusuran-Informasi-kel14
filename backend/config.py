# Backend API Configuration

import os

# ===================== PATH CONFIGURATION =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
INDEX_DIR = os.path.join(ROOT_DIR, "indexing")
SEARCH_ENGINE_DIR = os.path.join(ROOT_DIR, "implementation", "search_engine")

# Dataset
DATA_PATH = os.path.join(DATA_DIR, "merge-all-dual-storage.csv")
JSON_DATA_PATH = os.path.join(DATA_DIR, "index", "documents.json")

# Index files
TFIDF_INDEX_PATH = os.path.join(INDEX_DIR, "tfidf_index.pkl")
BM25_INDEX_PATH = os.path.join(INDEX_DIR, "bm25_index.pkl")

# ===================== API CONFIGURATION =====================
API_HOST = "0.0.0.0"
API_PORT = 5000
DEBUG = True

# CORS settings
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173", "*"]

# ===================== SEARCH CONFIGURATION =====================
DEFAULT_LIMIT = 10
MAX_LIMIT = 50
MIN_SCORE_THRESHOLD = 0.0  # Minimum relevance score

# Snippet length for results
SNIPPET_LENGTH = 200  # characters

# ===================== CACHE CONFIGURATION =====================
ENABLE_CACHE = True
CACHE_TTL = 3600  # seconds (1 hour)

# ===================== LOGGING =====================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
