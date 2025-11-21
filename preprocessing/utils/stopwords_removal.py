# Indonesian Stopwords untuk Berita Olahraga
# Sumber: Sastrawi + domain-specific olahraga

try:
    # Import dari Sastrawi (lebih lengkap dan ter-maintain)
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
    
    factory = StopWordRemoverFactory()
    sastrawi_stopwords = factory.get_stop_words()
    INDONESIAN_STOPWORDS = set(sastrawi_stopwords)
    print(f"✅ Loaded {len(INDONESIAN_STOPWORDS)} stopwords from Sastrawi")
    
except ImportError:
    # Fallback: jika Sastrawi belum terinstall, gunakan manual list
    print("⚠️ Sastrawi not installed. Using manual stopwords list.")
    print("💡 Install with: pip install Sastrawi")
    
    INDONESIAN_STOPWORDS = {
        # Kata umum
        'yang', 'untuk', 'pada', 'ke', 'para', 'namun', 'menurut', 'antara', 'dia', 'dua',
        'ia', 'seperti', 'jika', 'sehingga', 'kembali', 'dan', 'ini', 'itu', 
        'adalah', 'ada', 'dari', 'di', 'dengan', 'atau', 'akan', 'telah', 'dalam', 'tidak',
        'juga', 'oleh', 'saat', 'serta', 'karena', 'sebagai', 'bisa', 'dapat', 'sudah',
        'masih', 'hanya', 'lebih', 'sangat', 'paling', 'sekali', 'selalu', 'pernah',
        
        # Kata ganti
        'saya', 'anda', 'dia', 'kami', 'kita', 'mereka', 'nya', 'mu', 'ku',
        
        # Kata tanya
        'apa', 'siapa', 'bagaimana', 'kapan', 'dimana', 'mengapa', 'kenapa',
        
        # Kata penghubung
        'tetapi', 'namun', 'sedangkan', 'meskipun', 'walaupun', 'setelah', 'sebelum',
        'ketika', 'sementara', 'hingga', 'sampai', 'sejak',
        
        # Kata keterangan waktu umum
        'kemarin', 'besok', 'lusa', 'nanti', 'sekarang', 'kini',
        
        # Preposisi
        'atas', 'bawah', 'luar', 'dalam', 'depan', 'belakang', 'antara', 'tanpa',
        
        # Kata bantu
        'harus', 'perlu', 'ingin', 'mau', 'hendak', 'bisa', 'boleh', 'dapat',
    }

# Domain-specific stopwords untuk berita olahraga
SPORTS_STOPWORDS = {
    # Kata umum olahraga (kurang informatif untuk search)
    'laga', 'pertandingan', 'tim', 'pemain', 'pelatih', 'skuad', 'klub', 
    'stadion', 'menit', 'babak', 'gol', 'wasit',
    
    # Kata filler berita
    'jakarta', 'tempo', 'co', 'com', 'id', 'bola', 'kompas', 'sindonews',
    'foto', 'video', 'berita', 'artikel', 'halaman', 'selengkapnya',
}

# Stopwords tambahan yang bisa di-customize
CUSTOM_STOPWORDS = set()  # Empty set, bisa ditambahkan nanti

# Gabungkan semua stopwords
ALL_STOPWORDS = INDONESIAN_STOPWORDS | SPORTS_STOPWORDS | CUSTOM_STOPWORDS


def get_stopwords():
    """Return set stopwords Indonesia"""
    return ALL_STOPWORDS


def add_stopwords(words):
    """
    Tambah stopwords baru
    
    Args:
        words: list atau set kata yang akan ditambahkan
    """
    global ALL_STOPWORDS
    if isinstance(words, list):
        ALL_STOPWORDS.update(set(words))
    else:
        ALL_STOPWORDS.update(words)


def remove_stopwords_from_list(words):
    """
    Hapus stopwords dari list kata
    
    Args:
        words: list kata
    
    Returns:
        list kata tanpa stopwords
    """
    return [word for word in words if word.lower() not in ALL_STOPWORDS]


def remove_stopwords_from_text(text):
    """
    Hapus stopwords dari teks
    
    Args:
        text: string teks
    
    Returns:
        string teks tanpa stopwords
    """
    words = text.split()
    filtered = remove_stopwords_from_list(words)
    return ' '.join(filtered)


if __name__ == "__main__":
    # Test
    print(f"Total stopwords: {len(ALL_STOPWORDS)}")
    print(f"\nContoh stopwords: {list(ALL_STOPWORDS)[:20]}")
    
    # Test remove stopwords
    sample = "Timnas Indonesia akan bertanding di Jakarta pada hari Minggu"
    print(f"\nOriginal: {sample}")
    print(f"Filtered: {remove_stopwords_from_text(sample)}")
