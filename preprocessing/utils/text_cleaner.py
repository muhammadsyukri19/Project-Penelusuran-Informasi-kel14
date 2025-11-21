import re
import string
from typing import List, Dict


class TextCleaner:
    """
    Kelas untuk membersihkan teks dari berbagai noise
    """
    
    def __init__(self):
        # Pattern untuk cleaning
        self.url_pattern = re.compile(r'https?://\S+|www\.\S+')
        self.email_pattern = re.compile(r'\S+@\S+')
        self.mention_pattern = re.compile(r'@\w+')
        self.hashtag_pattern = re.compile(r'#\w+')
        self.number_pattern = re.compile(r'\d+')
        
    def remove_newlines(self, text: str) -> str:
        """Hapus newline dan ganti dengan spasi"""
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')
        return text
    
    def remove_extra_whitespace(self, text: str) -> str:
        """Hapus whitespace berlebih"""
        # Ganti multiple spaces dengan single space
        text = re.sub(r'\s+', ' ', text)
        # Trim
        text = text.strip()
        return text
    
    def remove_urls(self, text: str) -> str:
        """Hapus URL dari teks"""
        return self.url_pattern.sub('', text)
    
    def remove_emails(self, text: str) -> str:
        """Hapus email dari teks"""
        return self.email_pattern.sub('', text)
    
    def remove_mentions(self, text: str) -> str:
        """Hapus mention (@username)"""
        return self.mention_pattern.sub('', text)
    
    def remove_hashtags(self, text: str) -> str:
        """Hapus hashtag (#tag)"""
        return self.hashtag_pattern.sub('', text)
    
    def remove_numbers(self, text: str, keep_numbers: bool = True) -> str:
        """
        Hapus atau pertahankan angka
        
        Args:
            text: teks input
            keep_numbers: True = pertahankan angka, False = hapus
        """
        if not keep_numbers:
            return self.number_pattern.sub('', text)
        return text
    
    def remove_punctuation(self, text: str, keep_punctuation: List[str] = None) -> str:
        """
        Hapus tanda baca
        
        Args:
            text: teks input
            keep_punctuation: list tanda baca yang ingin dipertahankan
        """
        if keep_punctuation:
            # Buat translator hanya untuk punctuation yang tidak di-keep
            translator = str.maketrans('', '', ''.join([p for p in string.punctuation if p not in keep_punctuation]))
        else:
            # Hapus semua punctuation
            translator = str.maketrans('', '', string.punctuation)
        
        return text.translate(translator)
    
    def normalize_case(self, text: str, method: str = 'lower') -> str:
        """
        Normalisasi case
        
        Args:
            method: 'lower', 'upper', atau 'title'
        """
        if method == 'lower':
            return text.lower()
        elif method == 'upper':
            return text.upper()
        elif method == 'title':
            return text.title()
        return text
    
    def remove_repeated_chars(self, text: str, max_repeat: int = 2) -> str:
        """
        Hapus karakter berulang berlebih
        Contoh: 'gooolll' -> 'gol', 'mantaaap' -> 'mantap'
        
        Args:
            max_repeat: jumlah maksimal pengulangan yang diperbolehkan
        """
        pattern = r'(.)\1{' + str(max_repeat) + ',}'
        return re.sub(pattern, r'\1' * max_repeat, text)
    
    def clean_basic(self, text: str) -> str:
        """
        Cleaning dasar:
        1. Hapus newline
        2. Hapus extra whitespace
        3. Lowercase
        """
        text = self.remove_newlines(text)
        text = self.remove_extra_whitespace(text)
        text = self.normalize_case(text, 'lower')
        return text
    
    def clean_standard(self, text: str) -> str:
        """
        Cleaning standar untuk berita:
        1. Hapus URL, email
        2. Hapus newline
        3. Hapus extra whitespace
        4. Hapus punctuation
        5. Lowercase
        """
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.remove_newlines(text)
        text = self.remove_extra_whitespace(text)
        text = self.remove_punctuation(text)
        text = self.normalize_case(text, 'lower')
        return text
    
    def clean_aggressive(self, text: str) -> str:
        """
        Cleaning agresif (untuk indexing):
        1. Hapus URL, email, mention, hashtag
        2. Hapus newline
        3. Hapus punctuation
        4. Hapus angka
        5. Hapus repeated chars
        6. Hapus extra whitespace
        7. Lowercase
        """
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.remove_mentions(text)
        text = self.remove_hashtags(text)
        text = self.remove_newlines(text)
        text = self.remove_punctuation(text)
        text = self.remove_numbers(text, keep_numbers=False)
        text = self.remove_repeated_chars(text)
        text = self.remove_extra_whitespace(text)
        text = self.normalize_case(text, 'lower')
        return text
    
    def clean_custom(self, text: str, config: Dict) -> str:
        """
        Cleaning custom berdasarkan konfigurasi
        
        Args:
            config: dict dengan key:
                - remove_urls: bool
                - remove_emails: bool
                - remove_newlines: bool
                - remove_punctuation: bool
                - remove_numbers: bool
                - lowercase: bool
        """
        if config.get('remove_urls', True):
            text = self.remove_urls(text)
        
        if config.get('remove_emails', True):
            text = self.remove_emails(text)
        
        if config.get('remove_newlines', True):
            text = self.remove_newlines(text)
        
        if config.get('remove_punctuation', True):
            text = self.remove_punctuation(text)
        
        if config.get('remove_numbers', False):
            text = self.remove_numbers(text, keep_numbers=False)
        
        text = self.remove_extra_whitespace(text)
        
        if config.get('lowercase', True):
            text = self.normalize_case(text, 'lower')
        
        return text


# Helper function untuk kemudahan penggunaan
def clean_text(text: str, level: str = 'standard') -> str:
    """
    Quick function untuk clean text
    
    Args:
        text: teks yang akan dibersihkan
        level: 'basic', 'standard', atau 'aggressive'
    
    Returns:
        teks yang sudah dibersihkan
    """
    cleaner = TextCleaner()
    
    if level == 'basic':
        return cleaner.clean_basic(text)
    elif level == 'aggressive':
        return cleaner.clean_aggressive(text)
    else:  # standard
        return cleaner.clean_standard(text)


if __name__ == "__main__":
    # Test
    cleaner = TextCleaner()
    
    sample = """Persib Bandung\nberhasil mengalahkan\tPersija Jakarta
    dengan skor 3-1 di Stadion Gelora Bandung Lautan Api.
    
    Goooolll!!! Mantaaap!!!
    
    Kunjungi https://www.example.com untuk info lebih lanjut.
    Contact: info@persib.com"""
    
    print("Original:")
    print(sample)
    print("\n" + "="*60)
    
    print("\nBasic Cleaning:")
    print(cleaner.clean_basic(sample))
    
    print("\n" + "="*60)
    print("\nStandard Cleaning:")
    print(cleaner.clean_standard(sample))
    
    print("\n" + "="*60)
    print("\nAggressive Cleaning:")
    print(cleaner.clean_aggressive(sample))
