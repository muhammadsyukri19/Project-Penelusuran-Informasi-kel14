"""
STEP 4: Stemming
- Mengubah kata ke bentuk dasar menggunakan Sastrawi
- Contoh: bermain → main, memperpanjang → panjang
- Jalankan sebelum finalize untuk hasil optimal
"""
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STEP3_OUTPUT, STEP4_OUTPUT, VERBOSE

# Import Sastrawi Stemmer
try:
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    print(f"✅ Sastrawi Stemmer loaded successfully")
    SASTRAWI_AVAILABLE = True
except ImportError:
    print("❌ Sastrawi not installed!")
    print("💡 Install with: pip install Sastrawi")
    SASTRAWI_AVAILABLE = False


def stem_text(text):
    """
    Stem text menggunakan Sastrawi
    
    Args:
        text: string text yang akan di-stem
    
    Returns:
        string text dengan kata-kata dalam bentuk dasar
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    if not SASTRAWI_AVAILABLE:
        return text
    
    # Stem menggunakan Sastrawi
    stemmed = stemmer.stem(text)
    
    return stemmed


def stem_word_by_word(text):
    """
    Alternative: Stem word by word (lebih detail untuk melihat proses)
    
    Args:
        text: string text
    
    Returns:
        string text yang sudah di-stem per kata
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    if not SASTRAWI_AVAILABLE:
        return text
    
    words = text.split()
    stemmed_words = [stemmer.stem(word) for word in words]
    
    return ' '.join(stemmed_words)


def main():
    if not SASTRAWI_AVAILABLE:
        print("\n❌ Cannot proceed without Sastrawi")
        print("💡 Install with: pip install Sastrawi")
        return
    
    print("\n" + "="*60)
    print("🌿 STEP 4: STEMMING")
    print("="*60)
    print("Operations:")
    print("  ✓ Convert words to base form (kata dasar)")
    print("  ✓ Using Sastrawi Indonesian Stemmer")
    print("  ✓ Example: bermain → main, memperpanjang → panjang")
    print("="*60 + "\n")
    
    # Load data dari step 3 (setelah stopwords removal)
    print(f"📂 Loading: {STEP3_OUTPUT}")
    df = pd.read_csv(STEP3_OUTPUT, encoding='utf-8')
    print(f"✅ Loaded {len(df)} articles\n")
    
    # CONTENT: Stemming - REPLACE column
    print(f"🔄 Processing: content (stemming)")
    
    if VERBOSE:
        sample_idx = 0
        before_content = df['content'].iloc[sample_idx]
    
    # Apply stemming
    print("⏳ Stemming content... (this may take a while)")
    df['content'] = df['content'].apply(stem_text)
    
    if VERBOSE:
        print(f"\n📝 Sample CONTENT transformation:")
        print(f"  BEFORE: {before_content[:150]}...")
        print(f"  AFTER:  {df['content'].iloc[sample_idx][:150]}...")
        print()
        
        # Show specific word transformations
        before_words = before_content.split()[:10]
        after_words = df['content'].iloc[sample_idx].split()[:10]
        print(f"  Word-by-word comparison (first 10 words):")
        for i, (b, a) in enumerate(zip(before_words, after_words), 1):
            if b != a:
                print(f"    {i}. {b} → {a}")
        print()
    
    # TITLE: Stemming - REPLACE column
    print(f"🔄 Processing: title (stemming)")
    
    if VERBOSE:
        before_title = df['title'].iloc[0]
    
    df['title'] = df['title'].apply(stem_text)
    
    if VERBOSE:
        print(f"\n📝 Sample TITLE:")
        print(f"  Before: {before_title}")
        print(f"  After:  {df['title'].iloc[0]}")
        print()
    
    # Save to step4 output (akan diproses step5 finalize)
    print(f"\n💾 Saving to: {STEP4_OUTPUT}")
    df.to_csv(STEP4_OUTPUT, index=False, encoding='utf-8')
    
    print(f"\n✅ Step 4 (Stemming) completed!")
    print(f"📊 Output: {len(df)} rows, {len(df.columns)} columns")
    print("="*60 + "\n")
    
    print("💡 TIP: Stemming sangat berguna untuk:")
    print("  • Information Retrieval (search engine)")
    print("  • Text similarity comparison")
    print("  • Reducing vocabulary size")
    print("  • Improving search recall")


if __name__ == "__main__":
    main()
