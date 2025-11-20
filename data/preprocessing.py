import json
import re
import sys

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ---------------------------------------------------------
# NOTE:
# Sebelum menjalankan file ini, pastikan:
# 1) pip install Sastrawi nltk
# 2) Di Python shell:
#       import nltk
#       nltk.download('punkt')
#       nltk.download('stopwords')
# ---------------------------------------------------------

INPUT_FILE = "merge-all.json"      # nama file gabungan kamu
OUTPUT_FILE = "preprocessed.json"  # output hasil preprocessing


def load_articles(path: str):
    """Load artikel dari file JSON gabungan."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[INFO] Berhasil load {len(data)} artikel dari {path}")
        return data
    except FileNotFoundError:
        print(f"[ERROR] File {path} tidak ditemukan. Pastikan namanya benar dan ada di folder yang sama.")
        sys.exit(1)


def setup_text_tools():
    """Siapkan stemmer dan stopwords bahasa Indonesia."""
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    stop_words = set(stopwords.words("indonesian"))

    # kata penting sepak bola yang TIDAK BOLEH dihapus
    domain_keep = {
        "gol", "goal", "assist", "penalti", "penalty",
        "liga", "liga1", "liga", "super", "league",
        "timnas", "u-23", "u23",
        "persib", "persija", "arema", "persebaya",
        "madura", "bali", "united", "psm", "psis"
    }
    # hapus kata-kata penting itu dari stopwords
    stop_words = {w for w in stop_words if w not in domain_keep}

    return stemmer, stop_words


def clean_text(text: str) -> str:
    """Bersihkan teks mentah menjadi lowercase + tanpa simbol aneh."""
    if not text:
        return ""
    text = text.lower()
    # hapus tag HTML (jika ada)
    text = re.sub(r"<.*?>", " ", text)
    # sisakan huruf, angka, spasi, dan tanda -
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    # rapikan spasi berulang
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_documents(articles, stemmer, stop_words):
    """Lakukan cleaning, tokenisasi, stopword removal, dan stemming."""
    processed_docs = []

    for art in articles:
        # gabungkan judul + isi artikel
        raw_text = (art.get("title", "") or "") + " " + (art.get("content", "") or "")
        cleaned = clean_text(raw_text)

        # tokenisasi
        tokens = word_tokenize(cleaned)

        # buang stopword & token super pendek
        tokens = [t for t in tokens if t not in stop_words and len(t) > 1]

        # stemming
        stemmed = [stemmer.stem(t) for t in tokens]

        processed_docs.append({
            "id": art.get("id", ""),
            "source": art.get("source", ""),
            "url": art.get("url", ""),
            "title": art.get("title", ""),
            "tokens": stemmed
        })

    return processed_docs


def main():
    # 1. Load data gabungan
    articles = load_articles(INPUT_FILE)

    # 2. Siapkan stemmer & stopwords
    stemmer, stop_words = setup_text_tools()

    # 3. Preprocess semua dokumen
    processed_docs = preprocess_documents(articles, stemmer, stop_words)

    print(f"[INFO] Total dokumen setelah preprocessing: {len(processed_docs)}")

    # 4. Simpan ke JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_docs, f, ensure_ascii=False, indent=2)

    print(f"[DONE] Hasil preprocessing disimpan ke: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
