"""
STEP 3: Build Document Index
Membuat index untuk metadata dokumen (untuk retrieval dan display)
"""
import pandas as pd
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    INPUT_FILE, DOCUMENT_INDEX_FILE, METADATA_COLUMNS, 
    TEXT_COLUMN, VERBOSE
)

def build_document_index(df):
    """
    Build document index dengan metadata lengkap
    
    Document Index structure:
    {
        "doc_id": {
            "id": "bolanet_0",
            "source": "bolanet",
            "title": "...",
            "url": "...",
            "main_image": "...",
            "word_count": 341,
            "char_count": 2192,
            "text_preview": "first 200 chars..."
        }
    }
    """
    document_index = {}
    
    print(f"\n📑 Building Document Index...")
    print(f"   Metadata columns: {', '.join(METADATA_COLUMNS)}\n")
    
    for idx, row in df.iterrows():
        doc_id = row['id']
        
        # Extract metadata
        doc_data = {}
        for col in METADATA_COLUMNS:
            if col in df.columns:
                value = row[col]
                # Convert numpy types to python types
                if pd.isna(value):
                    doc_data[col] = None
                elif isinstance(value, (int, float)):
                    doc_data[col] = int(value) if col in ['word_count', 'char_count', 'images_count'] else float(value)
                else:
                    doc_data[col] = str(value)
        
        # Add text preview (first 200 chars)
        text = row[TEXT_COLUMN] if TEXT_COLUMN in df.columns else ""
        doc_data['text_preview'] = text[:200] + "..." if len(text) > 200 else text
        
        document_index[doc_id] = doc_data
        
        if VERBOSE and (idx + 1) % 50 == 0:
            print(f"   ✓ Indexed {idx + 1}/{len(df)} documents")
    
    print(f"\n✅ Document index built!")
    print(f"   📊 Total documents indexed: {len(document_index)}")
    
    return document_index

def main():
    print("\n" + "="*60)
    print("📑 STEP 3: BUILD DOCUMENT INDEX")
    print("="*60)
    print("Operations:")
    print("  ✓ Extract document metadata")
    print("  ✓ Create document lookup table")
    print("  ✓ Add text previews")
    print("="*60)
    
    # Load data
    print(f"\n📂 Loading: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, encoding='utf-8')
    print(f"✅ Loaded {len(df)} documents")
    
    # Build document index
    document_index = build_document_index(df)
    
    # Count documents by source
    sources = {}
    for doc_data in document_index.values():
        source = doc_data.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print(f"\n📊 Documents by source:")
    for source, count in sorted(sources.items()):
        print(f"   • {source}: {count} documents")
    
    # Save document index
    print(f"\n💾 Saving document index to: {DOCUMENT_INDEX_FILE}")
    with open(DOCUMENT_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(document_index, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Step 3 completed!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
