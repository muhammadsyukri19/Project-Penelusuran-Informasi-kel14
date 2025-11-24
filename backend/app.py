"""
Flask Backend API for Indonesian News Search Engine
Supports TF-IDF and BM25 algorithms
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import time
import logging

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "implementation", "search_engine"))

# Import config
from config import (
    API_HOST, API_PORT, DEBUG, CORS_ORIGINS,
    DEFAULT_LIMIT, MAX_LIMIT, LOG_LEVEL, LOG_FORMAT
)

# Import search engines
try:
    from search_tfidf import search_tfidf
    from search_bm25 import search_bm25
    SEARCH_AVAILABLE = True
except ImportError as e:
    print(f"[ERROR] Failed to import search engines: {e}")
    SEARCH_AVAILABLE = False

# Setup logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)

# ===================== INITIALIZATION =====================

def init_search_engines():
    """Verify search engine modules are available"""
    logger.info("Search engines ready (indices will be loaded on first use)")
    return SEARCH_AVAILABLE

# ===================== HELPER FUNCTIONS =====================

def format_search_result(result, algorithm):
    """Format a single search result from search engine output"""
    return {
        "doc_id": result.get("doc_id"),
        "title": result.get("title", ""),
        "snippet": result.get("snippet", ""),
        "url": result.get("url", ""),
        "published_at": result.get("published_at"),
        "score": round(float(result.get("score", 0)), 4),
        "rank": result.get("rank"),
        "algorithm": algorithm
    }

def validate_limit(limit):
    """Validate and normalize limit parameter"""
    try:
        limit = int(limit)
        if limit < 1:
            limit = DEFAULT_LIMIT
        elif limit > MAX_LIMIT:
            limit = MAX_LIMIT
        return limit
    except (ValueError, TypeError):
        return DEFAULT_LIMIT

# ===================== API ROUTES =====================

@app.route("/", methods=["GET"])
def home():
    """API info endpoint"""
    return jsonify({
        "name": "Indonesian News Search API",
        "version": "1.0.0",
        "status": "running",
        "algorithms": ["tfidf", "bm25"],
        "endpoints": {
            "health": "/api/health",
            "search": "/api/search",
            "compare": "/api/search/compare",
            "document": "/api/document/<doc_id>",
            "stats": "/api/stats"
        }
    })

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": time.time(),
        "search_engines": {
            "tfidf": SEARCH_AVAILABLE,
            "bm25": SEARCH_AVAILABLE
        }
    })

@app.route("/api/search", methods=["POST"])
def search():
    """
    Single algorithm search endpoint
    
    Body:
    {
        "query": "timnas indonesia",
        "algorithm": "tfidf",  // or "bm25"
        "limit": 10
    }
    """
    try:
        data = request.get_json()
        
        if not data or "query" not in data:
            return jsonify({"error": "Missing 'query' in request body"}), 400
        
        query = data["query"].strip()
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        algorithm = data.get("algorithm", "tfidf").lower()
        if algorithm not in ["tfidf", "bm25"]:
            return jsonify({"error": "Algorithm must be 'tfidf' or 'bm25'"}), 400
        
        limit = validate_limit(data.get("limit", DEFAULT_LIMIT))
        
        # Execute search
        start_time = time.time()
        
        if algorithm == "tfidf":
            results = search_tfidf(query=query, top_k=limit)
        else:  # bm25
            results = search_bm25(query=query, top_k=limit)
        
        execution_time = time.time() - start_time
        
        # Format results
        formatted_results = [
            format_search_result(result, algorithm)
            for result in results
        ]
        
        return jsonify({
            "query": query,
            "algorithm": algorithm,
            "execution_time": round(execution_time, 4),
            "total_results": len(formatted_results),
            "results": formatted_results
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/search/compare", methods=["POST"])
def search_compare():
    """
    Compare TF-IDF and BM25 algorithms
    
    Body:
    {
        "query": "timnas indonesia",
        "limit": 10
    }
    """
    try:
        data = request.get_json()
        
        if not data or "query" not in data:
            return jsonify({"error": "Missing 'query' in request body"}), 400
        
        query = data["query"].strip()
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        limit = validate_limit(data.get("limit", DEFAULT_LIMIT))
        
        # TF-IDF search
        start_tfidf = time.time()
        tfidf_results = search_tfidf(query=query, top_k=limit)
        time_tfidf = time.time() - start_tfidf
        
        # BM25 search
        start_bm25 = time.time()
        bm25_results = search_bm25(query=query, top_k=limit)
        time_bm25 = time.time() - start_bm25
        
        # Format results
        tfidf_formatted = [
            format_search_result(result, "tfidf")
            for result in tfidf_results
        ]
        
        bm25_formatted = [
            format_search_result(result, "bm25")
            for result in bm25_results
        ]
        
        # Calculate overlap
        tfidf_ids = set(r["doc_id"] for r in tfidf_formatted)
        bm25_ids = set(r["doc_id"] for r in bm25_formatted)
        overlap_ids = tfidf_ids & bm25_ids
        overlap_count = len(overlap_ids)
        overlap_percentage = (overlap_count / limit * 100) if limit > 0 else 0
        
        return jsonify({
            "query": query,
            "tfidf": {
                "execution_time": round(time_tfidf, 4),
                "total_results": len(tfidf_formatted),
                "results": tfidf_formatted
            },
            "bm25": {
                "execution_time": round(time_bm25, 4),
                "total_results": len(bm25_formatted),
                "results": bm25_formatted
            },
            "comparison": {
                "overlap_count": overlap_count,
                "overlap_percentage": round(overlap_percentage, 2),
                "tfidf_only": list(tfidf_ids - bm25_ids),
                "bm25_only": list(bm25_ids - tfidf_ids),
                "faster_algorithm": "tfidf" if time_tfidf < time_bm25 else "bm25",
                "speed_difference": abs(round(time_tfidf - time_bm25, 4))
            }
        })
        
    except Exception as e:
        logger.error(f"Compare search error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/document/<int:doc_id>", methods=["GET"])
def get_document(doc_id):
    """Get full document by ID"""
    try:
        # Load CSV to get document
        import pandas as pd
        from config import DATA_PATH
        
        df = pd.read_csv(DATA_PATH)
        
        if doc_id < 0 or doc_id >= len(df):
            return jsonify({"error": f"Document {doc_id} not found"}), 404
        
        row = df.iloc[doc_id]
        
        return jsonify({
            "doc_id": doc_id,
            "title": str(row.get("title", "")) if not pd.isna(row.get("title", "")) else "",
            "content": str(row.get("content", "")) if not pd.isna(row.get("content", "")) else "",
            "url": str(row.get("url", "")) if not pd.isna(row.get("url", "")) else "",
            "source": str(row.get("source", "")) if not pd.isna(row.get("source", "")) else "",
            "main_image": str(row.get("main_image", "")) if "main_image" in df.columns and not pd.isna(row.get("main_image", "")) else "",
            "published_at": str(row.get("published_at", "")) if "published_at" in df.columns and not pd.isna(row.get("published_at", "")) else None
        })
        
    except Exception as e:
        logger.error(f"Get document error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get corpus statistics"""
    try:
        import pandas as pd
        from config import DATA_PATH
        
        df = pd.read_csv(DATA_PATH)
        total_docs = len(df)
        
        # Count by source
        sources = {}
        if "source" in df.columns:
            sources = df["source"].value_counts().to_dict()
        
        return jsonify({
            "total_documents": total_docs,
            "sources": sources,
            "algorithms_available": {
                "tfidf": SEARCH_AVAILABLE,
                "bm25": SEARCH_AVAILABLE
            }
        })
        
    except Exception as e:
        logger.error(f"Get stats error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/documents", methods=["GET"])
def get_all_documents():
    """Get all documents in JSON format (for Postman testing)"""
    try:
        import json
        from config import JSON_DATA_PATH
        
        # Check if JSON file exists
        if not os.path.exists(JSON_DATA_PATH):
            return jsonify({
                "error": "JSON file not found. Run csv_to_json.py first.",
                "path": JSON_DATA_PATH
            }), 404
        
        # Load JSON
        with open(JSON_DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Optional: Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)  # Max 100 per page
        
        documents = data.get('documents', [])
        total = len(documents)
        start = (page - 1) * per_page
        end = start + per_page
        
        return jsonify({
            "total_documents": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "sources": data.get('sources', {}),
            "documents": documents[start:end]
        })
        
    except Exception as e:
        logger.error(f"Get documents error: {e}")
        return jsonify({"error": str(e)}), 500

# ===================== ERROR HANDLERS =====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ===================== MAIN =====================

if __name__ == "__main__":
    if not SEARCH_AVAILABLE:
        logger.error("Search engines not available. Exiting.")
        sys.exit(1)
    
    # Initialize search engines
    if not init_search_engines():
        logger.error("Failed to initialize search engines. Exiting.")
        sys.exit(1)
    
    logger.info(f"Starting Flask API on {API_HOST}:{API_PORT}")
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)
