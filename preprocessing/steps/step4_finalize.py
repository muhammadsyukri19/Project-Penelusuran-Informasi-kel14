"""
STEP 4: Finalize & Combine
- Combine title + content
- Final cleanup
- Calculate statistics
"""
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STEP3_OUTPUT, FINAL_OUTPUT, TEXT_COLUMNS


def main():
    print("\n" + "="*60)
    print("🎯 STEP 4: FINALIZE & COMBINE")
    print("="*60 + "\n")
    
    print(f"📂 Loading: {STEP3_OUTPUT}")
    df = pd.read_csv(STEP3_OUTPUT, encoding='utf-8')
    print(f"✅ Loaded {len(df)} articles\n")
    
    # Rename step3 columns to _clean
    df['title_clean'] = df['title_step3']
    df['content_clean'] = df['content_step3']
    
    # Combine title + content
    print("🔗 Creating text_combined...")
    df['text_combined'] = df['title_clean'] + ' ' + df['content_clean']
    df['text_combined'] = df['text_combined'].str.strip()
    
    # Calculate statistics
    print("📊 Calculating statistics...")
    df['word_count'] = df['text_combined'].str.split().str.len()
    df['char_count'] = df['text_combined'].str.len()
    
    # Show statistics
    print(f"\n📈 Statistics:")
    print(f"  Total articles: {len(df)}")
    print(f"  Avg words per article: {df['word_count'].mean():.1f}")
    print(f"  Avg chars per article: {df['char_count'].mean():.1f}")
    print(f"  Min words: {df['word_count'].min()}")
    print(f"  Max words: {df['word_count'].max()}")
    
    # Save final
    print(f"\n💾 Saving to: {FINAL_OUTPUT}")
    df.to_csv(FINAL_OUTPUT, index=False, encoding='utf-8')
    
    print(f"\n✅ Step 4 completed!")
    print(f"📊 Final output: {len(df)} rows, {len(df.columns)} columns")
    print("\n🎉 ALL PREPROCESSING DONE!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()