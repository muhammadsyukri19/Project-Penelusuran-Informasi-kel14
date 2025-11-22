"""
STEP 4: Generate Index Statistics
Membuat statistik lengkap dari index yang sudah dibuat
"""
import json
import pickle
import sys
import os
from collections import Counter

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    INVERTED_INDEX_FILE, TFIDF_MATRIX_FILE, DOCUMENT_INDEX_FILE,
    VOCABULARY_FILE, INDEX_STATS_FILE, VERBOSE
)

def calculate_statistics(inverted_index, tfidf_data, document_index, vocabulary_data):
    """
    Calculate comprehensive statistics
    """
    print(f"\n📊 Calculating index statistics...\n")
    
    # Basic counts
    total_docs = len(document_index)
    vocab_size = len(inverted_index)
    
    # Term statistics
    term_doc_counts = [data["doc_count"] for data in inverted_index.values()]
    avg_doc_per_term = sum(term_doc_counts) / len(term_doc_counts) if term_doc_counts else 0
    max_doc_per_term = max(term_doc_counts) if term_doc_counts else 0
    min_doc_per_term = min(term_doc_counts) if term_doc_counts else 0
    
    # Find most common terms
    most_common_terms = sorted(
        inverted_index.items(), 
        key=lambda x: x[1]["doc_count"], 
        reverse=True
    )[:20]
    
    # Document length statistics
    doc_lengths = [doc["word_count"] for doc in document_index.values() if "word_count" in doc]
    avg_doc_length = sum(doc_lengths) / len(doc_lengths) if doc_lengths else 0
    max_doc_length = max(doc_lengths) if doc_lengths else 0
    min_doc_length = min(doc_lengths) if doc_lengths else 0
    
    # TF-IDF statistics
    tfidf_matrix = tfidf_data.get('tfidf_matrix', {})
    idf_scores = tfidf_data.get('idf', {})
    
    # Calculate average TF-IDF scores
    all_tfidf_scores = []
    for doc_scores in tfidf_matrix.values():
        all_tfidf_scores.extend(doc_scores.values())
    
    avg_tfidf = sum(all_tfidf_scores) / len(all_tfidf_scores) if all_tfidf_scores else 0
    max_tfidf = max(all_tfidf_scores) if all_tfidf_scores else 0
    
    # Terms with highest IDF (most discriminative)
    top_idf_terms = sorted(idf_scores.items(), key=lambda x: x[1], reverse=True)[:20]
    
    # Source distribution
    source_counts = Counter(doc["source"] for doc in document_index.values() if "source" in doc)
    
    statistics = {
        "overview": {
            "total_documents": total_docs,
            "vocabulary_size": vocab_size,
            "avg_terms_per_document": round(avg_doc_length, 2),
            "total_index_entries": sum(len(scores) for scores in tfidf_matrix.values())
        },
        "term_statistics": {
            "avg_documents_per_term": round(avg_doc_per_term, 2),
            "max_documents_per_term": max_doc_per_term,
            "min_documents_per_term": min_doc_per_term,
            "most_common_terms": [
                {"term": term, "doc_count": data["doc_count"]} 
                for term, data in most_common_terms
            ]
        },
        "document_statistics": {
            "avg_document_length": round(avg_doc_length, 2),
            "max_document_length": max_doc_length,
            "min_document_length": min_doc_length,
            "source_distribution": dict(source_counts)
        },
        "tfidf_statistics": {
            "avg_tfidf_score": round(avg_tfidf, 6),
            "max_tfidf_score": round(max_tfidf, 6),
            "top_discriminative_terms": [
                {"term": term, "idf_score": round(score, 4)} 
                for term, score in top_idf_terms
            ]
        },
        "metadata": tfidf_data.get('metadata', {})
    }
    
    return statistics

def print_statistics(stats):
    """
    Print statistics in readable format
    """
    print("\n" + "="*60)
    print("📊 INDEX STATISTICS SUMMARY")
    print("="*60)
    
    # Overview
    print("\n📋 Overview:")
    overview = stats["overview"]
    print(f"   • Total documents: {overview['total_documents']}")
    print(f"   • Vocabulary size: {overview['vocabulary_size']}")
    print(f"   • Avg terms per document: {overview['avg_terms_per_document']}")
    print(f"   • Total index entries: {overview['total_index_entries']}")
    
    # Term statistics
    print("\n📝 Term Statistics:")
    term_stats = stats["term_statistics"]
    print(f"   • Avg documents per term: {term_stats['avg_documents_per_term']}")
    print(f"   • Max documents per term: {term_stats['max_documents_per_term']}")
    print(f"   • Min documents per term: {term_stats['min_documents_per_term']}")
    
    print("\n   Top 10 most common terms:")
    for i, item in enumerate(term_stats["most_common_terms"][:10], 1):
        print(f"      {i}. '{item['term']}' - appears in {item['doc_count']} documents")
    
    # Document statistics
    print("\n📄 Document Statistics:")
    doc_stats = stats["document_statistics"]
    print(f"   • Avg document length: {doc_stats['avg_document_length']} words")
    print(f"   • Max document length: {doc_stats['max_document_length']} words")
    print(f"   • Min document length: {doc_stats['min_document_length']} words")
    
    print("\n   Documents by source:")
    for source, count in sorted(doc_stats["source_distribution"].items()):
        print(f"      • {source}: {count} documents")
    
    # TF-IDF statistics
    print("\n📈 TF-IDF Statistics:")
    tfidf_stats = stats["tfidf_statistics"]
    print(f"   • Avg TF-IDF score: {tfidf_stats['avg_tfidf_score']}")
    print(f"   • Max TF-IDF score: {tfidf_stats['max_tfidf_score']}")
    
    print("\n   Top 10 discriminative terms (highest IDF):")
    for i, item in enumerate(tfidf_stats["top_discriminative_terms"][:10], 1):
        print(f"      {i}. '{item['term']}' - IDF: {item['idf_score']}")
    
    print("\n" + "="*60)

def main():
    print("\n" + "="*60)
    print("📊 STEP 4: GENERATE INDEX STATISTICS")
    print("="*60)
    print("Operations:")
    print("  ✓ Load all index files")
    print("  ✓ Calculate comprehensive statistics")
    print("  ✓ Identify key patterns")
    print("="*60)
    
    # Load inverted index
    print(f"\n📂 Loading inverted index: {INVERTED_INDEX_FILE}")
    with open(INVERTED_INDEX_FILE, 'r', encoding='utf-8') as f:
        inverted_index = json.load(f)
    print(f"✅ Loaded inverted index")
    
    # Load TF-IDF matrix
    print(f"\n📂 Loading TF-IDF matrix: {TFIDF_MATRIX_FILE}")
    with open(TFIDF_MATRIX_FILE, 'rb') as f:
        tfidf_data = pickle.load(f)
    print(f"✅ Loaded TF-IDF matrix")
    
    # Load document index
    print(f"\n📂 Loading document index: {DOCUMENT_INDEX_FILE}")
    with open(DOCUMENT_INDEX_FILE, 'r', encoding='utf-8') as f:
        document_index = json.load(f)
    print(f"✅ Loaded document index")
    
    # Load vocabulary
    print(f"\n📂 Loading vocabulary: {VOCABULARY_FILE}")
    with open(VOCABULARY_FILE, 'r', encoding='utf-8') as f:
        vocabulary_data = json.load(f)
    print(f"✅ Loaded vocabulary")
    
    # Calculate statistics
    statistics = calculate_statistics(inverted_index, tfidf_data, document_index, vocabulary_data)
    
    # Print statistics
    print_statistics(statistics)
    
    # Save statistics
    print(f"\n💾 Saving statistics to: {INDEX_STATS_FILE}")
    with open(INDEX_STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(statistics, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Step 4 completed!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
