import csv
import json
import pandas as pd
from typing import List, Dict, Optional
import os
import sys

# Import modul preprocessing
from text_cleaner import TextCleaner
from preprocessing.stopwords_removal import get_stopwords, remove_stopwords_from_text


class DatasetPreprocessor:
    """
    Pipeline lengkap untuk preprocessing dataset berita sepak bola
    """
    
    def __init__(self, 
                 cleaning_level: str = 'standard',
                 remove_stopwords: bool = True,
                 keep_numbers: bool = True):
        """
        Args:
            cleaning_level: 'basic', 'standard', atau 'aggressive'
            remove_stopwords: apakah hapus stopwords
            keep_numbers: apakah pertahankan angka
        """
        self.cleaner = TextCleaner()
        self.cleaning_level = cleaning_level
        self.remove_stopwords_flag = remove_stopwords
        self.keep_numbers = keep_numbers
        self.stopwords = get_stopwords() if remove_stopwords else set()
        
        self.stats = {
            'total_processed': 0,
            'avg_length_before': 0,
            'avg_length_after': 0,
            'total_words_removed': 0
        }
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess single text
        
        Pipeline:
        1. Text cleaning (hapus \n, whitespace, dll)
        2. Remove stopwords
        3. Final normalization
        """
        if not text or not isinstance(text, str):
            return ""
        
        original_length = len(text)
        
        # Step 1: Text Cleaning
        if self.cleaning_level == 'basic':
            text = self.cleaner.clean_basic(text)
        elif self.cleaning_level == 'aggressive':
            text = self.cleaner.clean_aggressive(text)
        else:  # standard
            text = self.cleaner.clean_standard(text)
        
        # Step 2: Remove Stopwords (jika diaktifkan)
        if self.remove_stopwords_flag:
            text = remove_stopwords_from_text(text)
        
        # Step 3: Final cleanup
        text = self.cleaner.remove_extra_whitespace(text)
        
        # Update stats
        cleaned_length = len(text)
        self.stats['total_words_removed'] += (original_length - cleaned_length)
        
        return text
    
    def preprocess_article(self, article: Dict) -> Dict:
        """
        Preprocess single article (dict)
        
        Args:
            article: dict dengan keys: title, content, dll
        
        Returns:
            dict dengan text yang sudah dipreprocess
        """
        processed = article.copy()
        
        # Preprocess title
        if 'title' in article and article['title']:
            processed['title_clean'] = self.preprocess_text(article['title'])
        
        # Preprocess content
        if 'content' in article and article['content']:
            processed['content_clean'] = self.preprocess_text(article['content'])
        
        # Gabungkan title + content untuk indexing (opsional)
        title_clean = processed.get('title_clean', '')
        content_clean = processed.get('content_clean', '')
        processed['text_combined'] = f"{title_clean} {content_clean}".strip()
        
        return processed
    
    def preprocess_csv(self, 
                       input_file: str, 
                       output_file: str,
                       text_columns: List[str] = ['title', 'content']) -> None:
        """
        Preprocess CSV file
        
        Args:
            input_file: path input CSV
            output_file: path output CSV
            text_columns: kolom yang akan dipreprocess
        """
        print("\n" + "="*60)
        print("📊 PREPROCESSING DATASET")
        print("="*60)
        print(f"📂 Input:  {input_file}")
        print(f"📁 Output: {output_file}")
        print(f"🔧 Level:  {self.cleaning_level}")
        print(f"🚫 Remove stopwords: {'Yes' if self.remove_stopwords_flag else 'No'}")
        print("="*60 + "\n")
        
        # Baca CSV dengan pandas
        try:
            df = pd.read_csv(input_file, encoding='utf-8')
            total_rows = len(df)
            print(f"✅ Loaded {total_rows} rows from CSV")
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return
        
        # Preprocess setiap text column
        for col in text_columns:
            if col not in df.columns:
                print(f"⚠️ Column '{col}' not found, skipping...")
                continue
            
            print(f"\n🔄 Processing column: {col}")
            
            # Hitung statistik before
            before_lengths = df[col].fillna('').apply(len)
            avg_before = before_lengths.mean()
            
            # Preprocess
            df[f'{col}_clean'] = df[col].fillna('').apply(self.preprocess_text)
            
            # Hitung statistik after
            after_lengths = df[f'{col}_clean'].apply(len)
            avg_after = after_lengths.mean()
            
            reduction = ((avg_before - avg_after) / avg_before * 100) if avg_before > 0 else 0
            
            print(f"  • Avg length before: {avg_before:.0f} chars")
            print(f"  • Avg length after:  {avg_after:.0f} chars")
            print(f"  • Reduction: {reduction:.1f}%")
        
        # Buat kolom text_combined (title + content)
        if 'title_clean' in df.columns and 'content_clean' in df.columns:
            print(f"\n🔗 Creating combined text column...")
            df['text_combined'] = df['title_clean'] + ' ' + df['content_clean']
            df['text_combined'] = df['text_combined'].str.strip()
        
        # Simpan hasil
        try:
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            
            print(f"\n{'='*60}")
            print("✅ PREPROCESSING SELESAI!")
            print("="*60)
            print(f"📁 Output file: {output_file}")
            print(f"📦 File size: {file_size:.2f} MB")
            print(f"📋 Total rows: {len(df)}")
            print(f"📑 Total columns: {len(df.columns)}")
            print("="*60 + "\n")
            
            # Tampilkan sample
            print("📝 Sample hasil (5 baris pertama):\n")
            print(df[['id', 'source', 'title_clean', 'content_clean']].head())
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
    
    def preprocess_json(self,
                        input_file: str,
                        output_file: str) -> None:
        """
        Preprocess JSON file
        
        Args:
            input_file: path input JSON
            output_file: path output JSON
        """
        print(f"\n🔄 Processing JSON: {input_file}")
        
        # Load JSON
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Loaded {len(data)} articles")
        except Exception as e:
            print(f"❌ Error reading JSON: {e}")
            return
        
        # Preprocess setiap article
        processed_data = []
        for i, article in enumerate(data, 1):
            processed = self.preprocess_article(article)
            processed_data.append(processed)
            
            if i % 50 == 0:
                print(f"  Processed {i}/{len(data)} articles...")
        
        # Simpan
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Saved to {output_file}")
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")


def main():
    """
    Main function untuk menjalankan preprocessing
    """
    
    # Konfigurasi
    INPUT_CSV = "../data/merge-all.csv"
    OUTPUT_CSV = "../data/merge-all-clean.csv"
    
    # Pilihan preprocessing level:
    # - 'basic': cleaning minimal (hapus \n, whitespace, lowercase)
    # - 'standard': cleaning standar (+ hapus punctuation, URL, email)
    # - 'aggressive': cleaning maksimal (+ hapus angka, repeated chars)
    
    CLEANING_LEVEL = 'standard'  # Ubah sesuai kebutuhan
    REMOVE_STOPWORDS = True       # True = hapus stopwords Indonesia
    
    print("\n" + "="*60)
    print("🚀 MULAI PREPROCESSING DATASET BERITA SEPAK BOLA")
    print("="*60)
    print(f"\n⚙️ Konfigurasi:")
    print(f"  • Cleaning Level: {CLEANING_LEVEL}")
    print(f"  • Remove Stopwords: {REMOVE_STOPWORDS}")
    print(f"  • Input: {INPUT_CSV}")
    print(f"  • Output: {OUTPUT_CSV}")
    
    # Inisialisasi preprocessor
    preprocessor = DatasetPreprocessor(
        cleaning_level=CLEANING_LEVEL,
        remove_stopwords=REMOVE_STOPWORDS
    )
    
    # Jalankan preprocessing
    preprocessor.preprocess_csv(
        input_file=INPUT_CSV,
        output_file=OUTPUT_CSV,
        text_columns=['title', 'content']
    )
    
    print("\n🎉 Preprocessing selesai!")
    print("💡 File sudah siap untuk indexing!\n")


if __name__ == "__main__":
    main()
