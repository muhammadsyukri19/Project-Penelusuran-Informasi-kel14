"""
Master script to run all preprocessing steps
"""
import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from steps import step1_basic_cleaning
from steps import step2_normalize
from steps import step3_remove_stopwords
from steps import step4_finalize


def run_all():
    print("\n" + "="*60)
    print("🚀 PREPROCESSING PIPELINE - MODULAR EXECUTION")
    print("="*60)
    print("This will run all preprocessing steps sequentially")
    print("="*60 + "\n")
    
    steps = [
        ("Step 1: Basic Cleaning", step1_basic_cleaning.main),
        ("Step 2: Normalization", step2_normalize.main),
        ("Step 3: Remove Stopwords", step3_remove_stopwords.main),
        ("Step 4: Finalize & Combine", step4_finalize.main),
    ]
    
    total_start = time.time()
    
    for i, (name, func) in enumerate(steps, 1):
        print(f"\n{'='*60}")
        print(f"▶️  [{i}/{len(steps)}] {name}")
        print("="*60)
        
        start = time.time()
        try:
            func()
            elapsed = time.time() - start
            print(f"✅ {name} completed in {elapsed:.2f}s")
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    total_elapsed = time.time() - total_start
    
    print("\n" + "="*60)
    print("🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"⏱️  Total time: {total_elapsed:.2f}s")
    print(f"📁 Final output: merge-all-clean.csv")
    print("="*60 + "\n")
    
    return True


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)