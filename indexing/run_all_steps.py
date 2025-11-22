"""
Master script to run all indexing steps
"""
import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from steps import step1_build_inverted_index
from steps import step2_calculate_tfidf
from steps import step3_build_document_index
from steps import step4_generate_statistics

def run_all():
    print("\n" + "="*60)
    print("🚀 INDEXING PIPELINE - MODULAR EXECUTION")
    print("="*60)
    print("This will build the search index from preprocessed data")
    print("="*60 + "\n")
    
    steps = [
        ("Step 1: Build Inverted Index", step1_build_inverted_index.main),
        ("Step 2: Calculate TF-IDF", step2_calculate_tfidf.main),
        ("Step 3: Build Document Index", step3_build_document_index.main),
        ("Step 4: Generate Statistics", step4_generate_statistics.main),
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
    print("🎉 ALL INDEXING STEPS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"⏱️  Total time: {total_elapsed:.2f}s")
    print(f"📁 Index files saved in: data/index/")
    print("\n📊 Index files created:")
    print("   • inverted_index.json - Term to document mapping")
    print("   • tfidf_matrix.pkl - TF-IDF weights")
    print("   • document_index.json - Document metadata")
    print("   • vocabulary.json - Complete vocabulary")
    print("   • index_stats.json - Index statistics")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
