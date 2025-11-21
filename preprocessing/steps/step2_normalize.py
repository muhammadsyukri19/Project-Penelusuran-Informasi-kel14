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
    
    for col in TEXT_COLUMNS:
        step1_col = f'{col}_step1'
        if step1_col not in df.columns:
            print(f"⚠️  Column '{step1_col}' not found, skipping...")
            continue
        
        print(f"🔄 Processing: {step1_col}")
        df[f'{col}_step2'] = df[step1_col].apply(lambda x: normalize_text(x, KEEP_NUMBERS))
        
        if VERBOSE:
            sample_idx = 0
            before = df[step1_col].iloc[sample_idx]
            after = df[f'{col}_step2'].iloc[sample_idx]
            
            print(f"\n📝 Sample:")
            print(f"  BEFORE: {before[:100]}...")
            print(f"  AFTER:  {after[:100]}...")
            print()
    
    print(f"💾 Saving to: {STEP2_OUTPUT}")
    df.to_csv(STEP2_OUTPUT, index=False, encoding='utf-8')
    
    print(f"\n✅ Step 2 completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()