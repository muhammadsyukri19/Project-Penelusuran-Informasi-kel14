import json
import csv
import os

# ===================== KONFIGURASI =====================

INPUT_JSON = "merge-all.json"
OUTPUT_CSV = "merge-all.csv"

# ===================== FUNGSI KONVERSI =====================

def json_to_csv(json_file, csv_file):
    """
    Konversi file JSON ke CSV
    
    Args:
        json_file: Path file JSON input
        csv_file: Path file CSV output
    """
    
    print("\n" + "="*60)
    print("📄 KONVERSI JSON KE CSV")
    print("="*60)
    print(f"📂 Input:  {json_file}")
    print(f"📁 Output: {csv_file}")
    print("="*60 + "\n")
    
    # Cek apakah file JSON ada
    if not os.path.exists(json_file):
        print(f"❌ Error: File {json_file} tidak ditemukan!")
        return False
    
    # Load JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Berhasil load JSON: {len(data)} artikel")
    except Exception as e:
        print(f"❌ Error membaca JSON: {e}")
        return False
    
    if not data:
        print("⚠️ Data JSON kosong!")
        return False
    
    # Definisi kolom CSV
    fieldnames = [
        'id',
        'source',
        'url',
        'title',
        'content',
        'main_image',
        'images_count',
        'content_length'
    ]
    
    # Tulis ke CSV
    try:
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Tulis header
            writer.writeheader()
            
            # Tulis setiap baris
            for article in data:
                # Hitung jumlah gambar
                images = article.get('images', [])
                images_count = len(images) if images else 0
                
                # Hitung panjang konten
                content = article.get('content', '')
                content_length = len(content)
                
                # Siapkan row untuk CSV
                row = {
                    'id': article.get('id', ''),
                    'source': article.get('source', ''),
                    'url': article.get('url', ''),
                    'title': article.get('title', ''),
                    'content': content,
                    'main_image': article.get('main_image', ''),
                    'images_count': images_count,
                    'content_length': content_length
                }
                
                writer.writerow(row)
        
        print(f"\n✅ Berhasil konversi {len(data)} artikel ke CSV")
        
        # Tampilkan statistik
        print(f"\n{'='*60}")
        print("📊 STATISTIK FILE CSV")
        print("="*60)
        
        file_size = os.path.getsize(csv_file) / (1024 * 1024)  # MB
        print(f"📦 Ukuran file: {file_size:.2f} MB")
        print(f"📋 Jumlah baris: {len(data) + 1} (termasuk header)")
        print(f"📑 Jumlah kolom: {len(fieldnames)}")
        
        # Statistik per sumber
        sources = {}
        for article in data:
            source = article.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print(f"\n📰 Per Sumber:")
        for source, count in sorted(sources.items()):
            percentage = (count / len(data) * 100) if len(data) > 0 else 0
            print(f"  • {source}: {count} artikel ({percentage:.1f}%)")
        
        print(f"\n{'='*60}")
        print(f"✨ File CSV berhasil dibuat: {csv_file}")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error menulis CSV: {e}")
        return False


def main():
    """Fungsi utama"""
    success = json_to_csv(INPUT_JSON, OUTPUT_CSV)
    
    if success:
        print("🎉 Konversi selesai!")
        print("\n💡 Tips:")
        print("  - File CSV bisa dibuka di Excel/Google Sheets")
        print("  - Gunakan untuk indexing dengan Whoosh")
        print("  - Encoding UTF-8 untuk karakter Indonesia")
    else:
        print("❌ Konversi gagal!")


if __name__ == "__main__":
    main()
