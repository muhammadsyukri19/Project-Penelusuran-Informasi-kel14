"""
STEP 1: Basic Text Cleaning
- Hapus SEMUA newline (\n, \r, \t) -> SEBARIS PENUH
- Hapus extra whitespace
- Hapus URL & email
- Lowercase conversion
"""
import pandas as pd
import re
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import INPUT_FILE, STEP1_OUTPUT, TEXT_COLUMNS, VERBOSE


def clean_newlines_aggressive(text):
    """Hapus SEMUA newline dan jadikan 1 baris panjang"""
    if not isinstance(text, str):
        return ""
    
    # Hapus \n, \r, \t, dan semua whitespace character
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    
    # Hapus multiple spaces jadi single space
    text = re.sub(r'\s+', ' ', text)
    
    # Trim
    text = text.strip()
    
    return text


def remove_urls(text):
    """Hapus URL"""
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)


def remove_emails(text):
    """Hapus email"""
    email_pattern = r'\S+@\S+'
    return re.sub(email_pattern, '', text)


def basic_clean(text):
    """Pipeline cleaning dasar"""
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs
    text = remove_urls(text)
    
    # 3. Remove emails
    text = remove_emails(text)
    
    # 4. Remove newlines AGRESIF
    text = clean_newlines_aggressive(text)
    
    return text


def main():
    print("\n" + "="*60)
    print("🧹 STEP 1: BASIC TEXT CLEANING")
    print("="*60)
    print("Operations:")
    print("  ✓ Remove ALL newlines (\\n, \\r, \\t)")
    print("  ✓ Convert to single long line")
    print("  ✓ Remove URLs & emails")
    print("  ✓ Lowercase conversion")
    print("  ✓ Remove extra whitespace")
    print("="*60 + "\n")
    
    # Load data
    print(f"📂 Loading: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, encoding='utf-8')
    print(f"✅ Loaded {len(df)} articles\n")
    
    # Process each text column
    for col in TEXT_COLUMNS:
        if col not in df.columns:
            print(f"⚠️  Column '{col}' not found, skipping...")
            continue
        
        print(f"🔄 Processing column: {col}")
        
        # Apply cleaning
        df[f'{col}_step1'] = df[col].fillna('').apply(basic_clean)
        
        # Show sample
        if VERBOSE:
            sample_idx = 0
            original = df[col].iloc[sample_idx]
            cleaned = df[f'{col}_step1'].iloc[sample_idx]
            
            print(f"\n📝 Sample transformation:")
            print(f"  BEFORE (first 150 chars):")
            print(f"  {repr(original[:150])}...")
            print(f"\n  AFTER (first 150 chars):")
            print(f"  {cleaned[:150]}...")
            print()
    
    # Save
    print(f"💾 Saving to: {STEP1_OUTPUT}")
    df.to_csv(STEP1_OUTPUT, index=False, encoding='utf-8')
    
    print(f"\n✅ Step 1 completed!")
    print(f"📊 Output: {len(df)} rows, {len(df.columns)} columns")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()