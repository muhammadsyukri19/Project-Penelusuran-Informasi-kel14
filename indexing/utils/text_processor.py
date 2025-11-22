"""
Utility functions untuk text processing saat indexing
"""
from collections import Counter
import math

def tokenize(text):
    """
    Simple tokenization - split by whitespace
    Karena text sudah di-preprocess, cukup split by space
    """
    if not isinstance(text, str):
        return []
    return text.split()

def calculate_tf(term_counts):
    """
    Calculate Term Frequency (TF)
    TF = (jumlah kemunculan term) / (total term dalam dokumen)
    """
    total_terms = sum(term_counts.values())
    if total_terms == 0:
        return {}
    
    tf = {}
    for term, count in term_counts.items():
        tf[term] = count / total_terms
    
    return tf

def calculate_idf(term_doc_count, total_docs):
    """
    Calculate Inverse Document Frequency (IDF)
    IDF = log(total dokumen / jumlah dokumen yang mengandung term)
    """
    idf = {}
    for term, doc_count in term_doc_count.items():
        idf[term] = math.log(total_docs / (1 + doc_count))
    
    return idf

def calculate_tfidf_score(tf, idf):
    """
    Calculate TF-IDF score
    TF-IDF = TF * IDF
    """
    tfidf = {}
    for term, tf_value in tf.items():
        tfidf[term] = tf_value * idf.get(term, 0)
    
    return tfidf

def get_term_statistics(term_counts):
    """
    Get statistics dari term counts
    """
    if not term_counts:
        return {
            'total_terms': 0,
            'unique_terms': 0,
            'avg_term_frequency': 0,
            'max_term_frequency': 0
        }
    
    total = sum(term_counts.values())
    unique = len(term_counts)
    avg_freq = total / unique if unique > 0 else 0
    max_freq = max(term_counts.values()) if term_counts else 0
    
    return {
        'total_terms': total,
        'unique_terms': unique,
        'avg_term_frequency': round(avg_freq, 2),
        'max_term_frequency': max_freq
    }
