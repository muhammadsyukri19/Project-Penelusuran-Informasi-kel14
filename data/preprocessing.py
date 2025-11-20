import json
import re
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# ==============================
# CONFIG
# ==============================
INPUT_FILE = "merge-all.json"
OUTPUT_FILE = "preprocessed.json"

# Ubah ini ke 10 untuk testing
LIMIT = 300       # ← ambil 10 dokumen saja
# LIMIT = None   # ← kalau nanti mau full dataset

# Pastikan paket NLTK sudah ada
nltk.download('punkt')
nltk.download('stopwords')


# ==============================
# LOAD DATA
# ==============================
def load_articles(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if LIMIT:
            data = data[:LIMIT]

        print(f"[INFO] Loaded {len(data)} articles from {path}")
        return data

    except FileNotFoundError:
        print(f"[ERROR] File {path} not found!")
        sys.exit(1)


# ==============================
# TEXT CLEANING
# ==============================
def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()

    # hapus HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # hilangkan simbol kecuali huruf, angka, spasi, dan strip
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)

    # rapikan spasi
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ==============================
# SETUP STOPWORDS & STEMMER
# ==============================
factory = StemmerFactory()
stemmer = factory.create_stemmer()

stop_words = set(stopwords.words("indonesian"))

# Kata penting sepak bola agar tidak terhapus
DOMAIN_KEEP = {
    "gol", "goal", "assist", "penalti", "penalty",
    "liga", "liga1", "league",
    "timnas", "u23", "u-23",
    "persib", "persija", "arema", "persebaya",
    "madura", "bali", "united", "psis", "psm"
}

stop_words = {w for w in stop_words if w not in DOMAIN_KEEP}


# ==============================
# PREPROCESSING FUNCTION
# ==============================
def preprocess_documents(articles):
    processed_docs = []

    for art in articles:
        raw_text = (art.get("title", "") or "") + " " + (art.get("content", "") or "")
        cleaned = clean_text(raw_text)

        # tokenisasi dengan NLTK
        tokens = word_tokenize(cleaned)

        # buang stopword & token pendek
        tokens = [t for t in tokens if t not in stop_words and len(t) > 1]

        # stemming (Sastrawi)
        stemmed = [stemmer.stem(t) for t in tokens]

        # ambil gambar (kalau ada)
        images = art.get("images", [])
        main_image = images[0] if images else ""

        processed_docs.append({
            "id": art.get("id", ""),
            "source": art.get("source", ""),
            "url": art.get("url", ""),
            "title": art.get("title", ""),
            "main_image": main_image,
            "tokens": stemmed
        })

    return processed_docs


# ==============================
# MAIN PROCESS
# ==============================
def main():
    articles = load_articles(INPUT_FILE)
    processed = preprocess_documents(articles)

    print(f"[INFO] Total processed documents: {len(processed)}")

    # Simpan sekali saja di luar loop
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

    print(f"[DONE] Saved preprocessed data to {OUTPUT_FILE}")
    print(f"[SAMPLE] Example document:")
    print(processed[0])


if __name__ == "__main__":
    main()
