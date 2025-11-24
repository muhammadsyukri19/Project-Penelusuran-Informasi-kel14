"""
STEP 2: Normalization
- Remove punctuation
- Remove/keep numbers
- Remove repeated characters
"""
import pandas as pd
import re
import string
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STEP1_OUTPUT, STEP2_OUTPUT, TEXT_COLUMNS, KEEP_NUMBERS, VERBOSE


def remove_punctuation(text):
    """Hapus semua tanda baca"""
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def remove_numbers(text):
    """Hapus semua angka"""
    return re.sub(r'\d+', '', text)


def remove_repeated_chars(text, max_repeat=2):
    """Hapus karakter berulang: gooolll -> gol"""
    pattern = r'(.)\1{' + str(max_repeat) + ',}'
    return re.sub(pattern, r'\1' * max_repeat, text)


def normalize_text(text, keep_nums=True):
    """Pipeline normalization"""
    if not isinstance(text, str):
        return ""
    
    # 1. Remove punctuation
    text = remove_punctuation(text)
    
    # 2. Remove numbers (optional)
    if not keep_nums:
        text = remove_numbers(text)
    
    # 3. Remove repeated chars
    text = remove_repeated_chars(text)
    
    # 4. Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def main():
    print("\n" + "="*60)
    print("🔧 STEP 2: NORMALIZATION")
    print("="*60)
    print("Operations:")
    print("  ✓ Remove punctuation")
    print(f"  {'✓' if KEEP_NUMBERS else '✗'} Keep numbers: {KEEP_NUMBERS}")
    print("  ✓ Remove repeated characters")
    print("="*60 + "\n")
    
    print(f"📂 Loading: {STEP1_OUTPUT}")
    df = pd.read_csv(STEP1_OUTPUT, encoding='utf-8')
    print(f"✅ Loaded {len(df)} articles\n")
    
    # CONTENT: Full normalization - REPLACE column
    print(f"🔄 Processing: content (full normalization)")
    
    if VERBOSE:
        sample_idx = 0
        before_content = df['content'].iloc[sample_idx]
    
    df['content'] = df['content'].apply(lambda x: normalize_text(x, KEEP_NUMBERS))
    
    if VERBOSE:
        print(f"\n📝 Sample CONTENT:")
        print(f"  BEFORE: {before_content[:100]}...")
        print(f"  AFTER:  {df['content'].iloc[sample_idx][:100]}...")
        print()
    
    # TITLE: SKIP normalization (keep as is)
    print(f"⏭️  Skipping: title (NO preprocessing - keep original)")
    
    if VERBOSE:
        print(f"\n📝 TITLE unchanged (only lowercase from step 1):")
        print(f"  Title:  {df['title'].iloc[0][:80]}...")
        print()
    
    print(f"💾 Saving to: {STEP2_OUTPUT}")
    df.to_csv(STEP2_OUTPUT, index=False, encoding='utf-8')
    
    print(f"\n✅ Step 2 completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()