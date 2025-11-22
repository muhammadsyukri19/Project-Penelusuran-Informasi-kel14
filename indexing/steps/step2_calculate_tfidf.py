"""
STEP 2: Calculate TF-IDF Weights
Menghitung TF-IDF score untuk setiap term dalam setiap dokumen
"""
import pandas as pd
import json
import pickle
import sys
import os
from collections import defaultdict
import math

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    INPUT_FILE, INVERTED_INDEX_FILE, TFIDF_MATRIX_FILE,
    TEXT_COLUMN, VERBOSE, SUBLINEAR_TF, SMOOTH_IDF
)
from utils.text_processor import tokenize

def calculate_tfidf(df, inverted_index):
    """
    Calculate TF-IDF matrix
    
    TF-IDF = TF * IDF
    - TF: Term Frequency (normalized by document length)
    - IDF: Inverse Document Frequency
    """
    total_docs = len(df)
    tfidf_matrix = {}
    
    print(f"\n📊 Calculating TF-IDF weights...")
    print(f"   Total documents: {total_docs}")
    print(f"   Sublinear TF: {SUBLINEAR_TF}")
    print(f"   Smooth IDF: {SMOOTH_IDF}\n")
    
    # Step 1: Calculate IDF for each term
    print("   🔢 Calculating IDF...")
    idf = {}
    for term, data in inverted_index.items():
        doc_count = data["doc_count"]
        if SMOOTH_IDF:
            idf[term] = math.log((1 + total_docs) / (1 + doc_count)) + 1
        else:
            idf[term] = math.log(total_docs / doc_count)
    
    print(f"   ✓ IDF calculated for {len(idf)} terms")
    
    # Step 2: Calculate TF-IDF for each document
    print(f"   🔢 Calculating TF-IDF for each document...\n")
    
    for idx, row in df.iterrows():
        doc_id = row['id']
        text = row[TEXT_COLUMN]
        
        # Tokenize
        terms = tokenize(text)
        doc_length = len(terms)
        
        if doc_length == 0:
            tfidf_matrix[doc_id] = {}
            continue
        
        # Count term frequencies
        term_counts = {}
        for term in terms:
            term_counts[term] = term_counts.get(term, 0) + 1
        
        # Calculate TF-IDF
        tfidf_scores = {}
        for term, count in term_counts.items():
            # Calculate TF
            if SUBLINEAR_TF:
                tf = 1 + math.log(count) if count > 0 else 0
            else:
                tf = count / doc_length
            
            # Calculate TF-IDF
            tfidf = tf * idf.get(term, 0)
            tfidf_scores[term] = round(tfidf, 6)
        
        tfidf_matrix[doc_id] = tfidf_scores
        
        if VERBOSE and (idx + 1) % 50 == 0:
            print(f"   ✓ Processed {idx + 1}/{len(df)} documents")
    
    print(f"\n✅ TF-IDF matrix calculated!")
    print(f"   📊 Documents: {len(tfidf_matrix)}")
    
    # Calculate statistics
    total_tfidf_entries = sum(len(scores) for scores in tfidf_matrix.values())
    avg_terms_per_doc = total_tfidf_entries / len(tfidf_matrix) if tfidf_matrix else 0
    print(f"   📊 Avg unique terms per document: {avg_terms_per_doc:.1f}")
    
    return tfidf_matrix, idf

def main():
    print("\n" + "="*60)
    print("📈 STEP 2: CALCULATE TF-IDF WEIGHTS")
    print("="*60)
    print("Operations:")
    print("  ✓ Load inverted index")
    print("  ✓ Calculate IDF (Inverse Document Frequency)")
    print("  ✓ Calculate TF (Term Frequency)")
    print("  ✓ Calculate TF-IDF scores")
    print("="*60)
    
    # Load data
    print(f"\n📂 Loading: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, encoding='utf-8')
    print(f"✅ Loaded {len(df)} documents")
    
    # Load inverted index
    print(f"\n📂 Loading inverted index: {INVERTED_INDEX_FILE}")
    with open(INVERTED_INDEX_FILE, 'r', encoding='utf-8') as f:
        inverted_index = json.load(f)
    print(f"✅ Loaded inverted index with {len(inverted_index)} terms")
    
    # Calculate TF-IDF
    tfidf_matrix, idf = calculate_tfidf(df, inverted_index)
    
    # Save TF-IDF matrix (using pickle for efficiency)
    print(f"\n💾 Saving TF-IDF matrix to: {TFIDF_MATRIX_FILE}")
    with open(TFIDF_MATRIX_FILE, 'wb') as f:
        pickle.dump({
            'tfidf_matrix': tfidf_matrix,
            'idf': idf,
            'metadata': {
                'total_documents': len(df),
                'vocab_size': len(idf),
                'sublinear_tf': SUBLINEAR_TF,
                'smooth_idf': SMOOTH_IDF
            }
        }, f)
    
    print(f"\n✅ Step 2 completed!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
