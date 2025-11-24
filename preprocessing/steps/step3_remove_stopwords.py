"""
STEP 3: Remove Stopwords
- Using Sastrawi stopwords
- Add custom sports stopwords
- Remove short words
"""
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STEP2_OUTPUT, STEP3_OUTPUT, TEXT_COLUMNS, MIN_WORD_LENGTH, VERBOSE

# Import stopwords
try:
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
    factory = StopWordRemoverFactory()
    STOPWORDS = set(factory.get_stop_words())
    print(f"✅ Loaded {len(STOPWORDS)} stopwords from Sastrawi")
except ImportError:
    print("⚠️  Sastrawi not installed, using minimal stopwords")
    STOPWORDS = {'yang', 'untuk', 'pada', 'ke', 'di', 'dari', 'dan', 'atau', 'akan', 'adalah'}

# Add sports-specific stopwords
SPORTS_STOPWORDS = {
    'jakarta', 'tempo', 'com', 'id', 'foto', 'video', 'berita', 'artikel'
}

ALL_STOPWORDS = STOPWORDS | SPORTS_STOPWORDS


def remove_stopwords(text, min_length=2):
    """Remove stopwords and short words"""
    if not isinstance(text, str):
        return ""
    
    words = text.split()
    filtered = [
        word for word in words 
        if word.lower() not in ALL_STOPWORDS and len(word) >= min_length
    ]
    
    return ' '.join(filtered)


def main():
    print("\n" + "="*60)
    print("🚫 STEP 3: REMOVE STOPWORDS")
    print("="*60)
    print(f"Total stopwords: {len(ALL_STOPWORDS)}")
    print(f"Min word length: {MIN_WORD_LENGTH}")
    print("="*60 + "\n")
    
    print(f"📂 Loading: {STEP2_OUTPUT}")
    df = pd.read_csv(STEP2_OUTPUT, encoding='utf-8')
    print(f"✅ Loaded {len(df)} articles\n")
    
    # CONTENT: Remove stopwords - REPLACE column
    print(f"🔄 Processing: content")
    
    # Calculate stats before
    before_words = df['content'].str.split().str.len().mean()
    
    if VERBOSE:
        sample_idx = 0
        before_content = df['content'].iloc[sample_idx]
    
    # REPLACE content with stopwords removed
    df['content'] = df['content'].apply(lambda x: remove_stopwords(x, MIN_WORD_LENGTH))
    
    # Calculate stats after
    after_words = df['content'].str.split().str.len().mean()
    reduction = ((before_words - after_words) / before_words * 100) if before_words > 0 else 0
    
    print(f"  Avg words before: {before_words:.1f}")
    print(f"  Avg words after: {after_words:.1f}")
    print(f"  Reduction: {reduction:.1f}%")
    
    if VERBOSE:
        print(f"\n📝 Sample CONTENT:")
        print(f"  BEFORE: {before_content[:100]}...")
        print(f"  AFTER:  {df['content'].iloc[sample_idx][:100]}...")
        print()
    
    # TITLE: SKIP stopword removal (keep as is)
    print(f"\n⏭️  Skipping: title (NO preprocessing - keep original)")
    
    if VERBOSE:
        print(f"\n📝 TITLE unchanged:")
        print(f"  Title: {df['title'].iloc[0][:80]}...")
        print()
    
    print(f"💾 Saving to: {STEP3_OUTPUT}")
    df.to_csv(STEP3_OUTPUT, index=False, encoding='utf-8')
    
    print(f"\n✅ Step 3 completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()