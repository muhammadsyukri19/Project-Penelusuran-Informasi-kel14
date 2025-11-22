"""
STEP 5: Finalize & Combine
- Combine title + content (sudah di-stem)
- Calculate final statistics
- Generate final output
"""
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STEP4_OUTPUT, FINAL_OUTPUT


def main():
    print("\n" + "="*60)
    print("🎯 STEP 5: FINALIZE & COMBINE")
    print("="*60 + "\n")
    
    print(f"📂 Loading: {STEP4_OUTPUT}")
    df = pd.read_csv(STEP4_OUTPUT, encoding='utf-8')
    print(f"✅ Loaded {len(df)} articles\n")
    
    # title dan content sudah bersih dari step sebelumnya
    # Tambahkan column text_combined saja
    print("🔗 Creating text_combined...")
    df['text_combined'] = df['title'] + ' ' + df['content']
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
    
    print(f"\n✅ Step 5 (Finalize) completed!")
    print(f"📊 Final output: {len(df)} rows, {len(df.columns)} columns")
    print("\n🎉 ALL PREPROCESSING DONE!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()