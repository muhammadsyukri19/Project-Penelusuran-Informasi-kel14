"""
STEP 1: Build Inverted Index
Membuat inverted index: term -> [doc_ids yang mengandung term]
"""
import pandas as pd
import json
import sys
import os
from collections import defaultdict, Counter

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    INPUT_FILE, INVERTED_INDEX_FILE, VOCABULARY_FILE, 
    TEXT_COLUMN, VERBOSE
)
from utils.text_processor import tokenize, get_term_statistics

def build_inverted_index(df):
    """
    Build inverted index dari dataframe
    
    Inverted Index structure:
    {
        "term1": {
            "doc_ids": [1, 5, 10, ...],
            "doc_count": 3,
            "term_freq": {
                "doc1": 5,  # term muncul 5x di doc1
                "doc5": 2,
                "doc10": 1
            }
        },
        "term2": {...}
    }
    """
    inverted_index = defaultdict(lambda: {
        "doc_ids": [],
        "doc_count": 0,
        "term_freq": {}
    })
    
    vocabulary = set()
    total_terms_processed = 0
    
    print(f"\n🔨 Building Inverted Index...")
    print(f"   Processing {len(df)} documents\n")
    
    for idx, row in df.iterrows():
        doc_id = row['id']
        text = row[TEXT_COLUMN]
        
        # Tokenize
        terms = tokenize(text)
        term_counts = Counter(terms)
        
        # Update vocabulary
        vocabulary.update(terms)
        total_terms_processed += len(terms)
        
        # Build inverted index
        for term, count in term_counts.items():
            inverted_index[term]["doc_ids"].append(doc_id)
            inverted_index[term]["doc_count"] += 1
            inverted_index[term]["term_freq"][doc_id] = count
        
        if VERBOSE and (idx + 1) % 50 == 0:
            print(f"   ✓ Processed {idx + 1}/{len(df)} documents")
    
    print(f"\n✅ Inverted Index built!")
    print(f"   📊 Total unique terms: {len(vocabulary)}")
    print(f"   📊 Total terms processed: {total_terms_processed}")
    print(f"   📊 Avg terms per document: {total_terms_processed / len(df):.1f}")
    
    return dict(inverted_index), sorted(list(vocabulary))

def main():
    print("\n" + "="*60)
    print("📇 STEP 1: BUILD INVERTED INDEX")
    print("="*60)
    print("Operations:")
    print("  ✓ Tokenize text")
    print("  ✓ Build term -> document mapping")
    print("  ✓ Count term frequencies")
    print("  ✓ Create vocabulary")
    print("="*60)
    
    # Load data
    print(f"\n📂 Loading: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, encoding='utf-8')
    print(f"✅ Loaded {len(df)} documents")
    
    # Build inverted index
    inverted_index, vocabulary = build_inverted_index(df)
    
    # Save inverted index
    print(f"\n💾 Saving inverted index to: {INVERTED_INDEX_FILE}")
    with open(INVERTED_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(inverted_index, f, ensure_ascii=False, indent=2)
    
    # Save vocabulary
    print(f"💾 Saving vocabulary to: {VOCABULARY_FILE}")
    vocab_data = {
        "vocabulary": vocabulary,
        "vocab_size": len(vocabulary),
        "total_documents": len(df)
    }
    with open(VOCABULARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Step 1 completed!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
