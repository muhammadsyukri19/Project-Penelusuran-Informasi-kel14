"""
Convert merge-all-clean.csv to JSON format
untuk memudahkan akses di Postman dan API
"""

import pandas as pd
import json
import os

# Paths
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(DATA_DIR, 'merge-all-clean.csv')
OUTPUT_JSON = os.path.join(DATA_DIR, 'index', 'documents.json')

print("=" * 60)
print("  Converting CSV to JSON")
print("=" * 60)

# Read CSV
print(f"\n📖 Reading: {INPUT_CSV}")
df = pd.read_csv(INPUT_CSV)
print(f"   Total documents: {len(df)}")

# Convert to JSON structure
print("\n🔄 Converting to JSON...")
documents = []

for idx, row in df.iterrows():
    doc = {
        "doc_id": int(idx),
        "title": str(row.get('title', '')) if pd.notna(row.get('title')) else "",
        "content": str(row.get('content', '')) if pd.notna(row.get('content')) else "",
        "url": str(row.get('url', '')) if pd.notna(row.get('url')) else "",
        "source": str(row.get('source', '')) if pd.notna(row.get('source')) else "",
        "main_image": str(row.get('main_image', '')) if pd.notna(row.get('main_image', '')) else "",
        "published_at": str(row.get('published_at', '')) if pd.notna(row.get('published_at', '')) else None
    }
    documents.append(doc)

# Save JSON
print(f"\n💾 Saving to: {OUTPUT_JSON}")

# Create index folder if not exists
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

# Save with pretty print
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump({
        "total_documents": len(documents),
        "sources": df['source'].value_counts().to_dict(),
        "documents": documents
    }, f, ensure_ascii=False, indent=2)

print(f"   ✅ Saved {len(documents)} documents")

# Get file size
file_size = os.path.getsize(OUTPUT_JSON) / (1024 * 1024)  # MB
print(f"   📦 File size: {file_size:.2f} MB")

# Sample output
print("\n📝 Sample document (first):")
print(json.dumps(documents[0], ensure_ascii=False, indent=2)[:500])
print("...")

print("\n" + "=" * 60)
print("  ✅ Conversion Complete!")
print("=" * 60)
print(f"\n📂 JSON file location: {OUTPUT_JSON}")
print(f"📊 Total documents: {len(documents)}")
print(f"\n💡 Usage in Postman:")
print(f"   GET http://localhost:5000/api/documents")
print(f"   GET http://localhost:5000/api/document/0")
