import json
import csv
from datetime import datetime
import os

# ===================== KONFIGURASI =====================

INPUT_FILES = [
    "kompas_bola_indonesia.json",
    "bolanet_bola_indonesia.json",
    "sindonews_bola_indonesia.json"
]

OUTPUT_JSON = "hasil_crawling_gabungan.json"
OUTPUT_CSV = "hasil_crawling_gabungan.csv"

# ===================== FUNGSI UTAMA =====================

def load_json_file(filename):
    """Membaca file JSON dan mengembalikan datanya."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✓ Berhasil membaca {filename}: {len(data)} artikel")
            return data
    except FileNotFoundError:
        print(f"✗ File {filename} tidak ditemukan")
        return []
    except json.JSONDecodeError as e:
        print(f"✗ Error membaca {filename}: {e}")
        return []
    except Exception as e:
        print(f"✗ Error tidak terduga pada {filename}: {e}")
        return []


def extract_source_from_url(url):
    """Mengekstrak sumber berita dari URL."""
    if "kompas.com" in url:
        return "Kompas"
    elif "bola.net" in url:
        return "Bola.net"
    elif "sindonews.com" in url:
        return "SINDOnews"
    else:
        return "Unknown"


def merge_articles():
    """Menggabungkan semua artikel dari berbagai sumber."""
    all_articles = []
    article_id = 1
    
    print("\n" + "="*60)
    print("MEMULAI PENGGABUNGAN DATA CRAWLING")
    print("="*60 + "\n")
    
    for filename in INPUT_FILES:
        articles = load_json_file(filename)
        
        # Tambahkan metadata ke setiap artikel
        for article in articles:
            article['id'] = article_id
            article['source'] = extract_source_from_url(article.get('url', ''))
            
            # Pastikan semua field ada (untuk konsistensi)
            article.setdefault('title', 'N/A')
            article.setdefault('url', 'N/A')
            article.setdefault('published_at', None)
            article.setdefault('content', '')
            article.setdefault('content_length', 0)
            article.setdefault('images', [])
            
            all_articles.append(article)
            article_id += 1
    
    return all_articles


def save_to_json(articles, filename):
    """Menyimpan artikel ke file JSON."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Berhasil menyimpan {len(articles)} artikel ke {filename}")
        return True
    except Exception as e:
        print(f"\n✗ Error menyimpan JSON: {e}")
        return False


def save_to_csv(articles, filename):
    """Menyimpan artikel ke file CSV."""
    try:
        if not articles:
            print("\n✗ Tidak ada artikel untuk disimpan ke CSV")
            return False
        
        # Definisikan kolom CSV
        fieldnames = [
            'id',
            'source',
            'title',
            'url',
            'published_at',
            'content_length',
            'images_count',
            'content'
        ]
        
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for article in articles:
                # Siapkan data untuk CSV
                csv_row = {
                    'id': article.get('id', ''),
                    'source': article.get('source', ''),
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'published_at': article.get('published_at', ''),
                    'content_length': article.get('content_length', 0),
                    'images_count': len(article.get('images', [])),
                    'content': article.get('content', '')[:500] + '...' if len(article.get('content', '')) > 500 else article.get('content', '')
                }
                writer.writerow(csv_row)
        
        print(f"✓ Berhasil menyimpan {len(articles)} artikel ke {filename}")
        return True
    except Exception as e:
        print(f"\n✗ Error menyimpan CSV: {e}")
        return False


def print_statistics(articles):
    """Menampilkan statistik hasil penggabungan."""
    print("\n" + "="*60)
    print("STATISTIK HASIL CRAWLING")
    print("="*60)
    
    total = len(articles)
    print(f"\nTotal artikel: {total}")
    
    # Hitung per sumber
    sources = {}
    for article in articles:
        source = article.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print("\nPer Sumber:")
    for source, count in sorted(sources.items()):
        percentage = (count / total * 100) if total > 0 else 0
        print(f"  - {source}: {count} artikel ({percentage:.1f}%)")
    
    # Statistik konten
    content_lengths = [article.get('content_length', 0) for article in articles]
    if content_lengths:
        avg_length = sum(content_lengths) / len(content_lengths)
        min_length = min(content_lengths)
        max_length = max(content_lengths)
        
        print(f"\nStatistik Panjang Konten:")
        print(f"  - Rata-rata: {avg_length:.0f} karakter")
        print(f"  - Minimum: {min_length} karakter")
        print(f"  - Maximum: {max_length} karakter")
    
    # Artikel dengan gambar
    with_images = sum(1 for article in articles if article.get('images'))
    print(f"\nArtikel dengan gambar: {with_images} ({with_images/total*100:.1f}%)")
    
    # Artikel dengan tanggal publikasi
    with_date = sum(1 for article in articles if article.get('published_at'))
    print(f"Artikel dengan tanggal publikasi: {with_date} ({with_date/total*100:.1f}%)")
    
    print("\n" + "="*60)


def main():
    """Fungsi utama untuk menjalankan proses penggabungan."""
    
    # Gabungkan semua artikel
    merged_articles = merge_articles()
    
    if not merged_articles:
        print("\n✗ Tidak ada artikel yang berhasil digabungkan!")
        return
    
    # Tampilkan statistik
    print_statistics(merged_articles)
    
    # Simpan ke JSON
    print("\n" + "-"*60)
    print("MENYIMPAN HASIL")
    print("-"*60)
    save_to_json(merged_articles, OUTPUT_JSON)
    
    # Simpan ke CSV
    save_to_csv(merged_articles, OUTPUT_CSV)
    
    print("\n" + "="*60)
    print("PROSES SELESAI")
    print("="*60)
    print(f"\nFile output:")
    print(f"  - JSON: {OUTPUT_JSON}")
    print(f"  - CSV: {OUTPUT_CSV}")
    print()


if __name__ == "__main__":
    main()
