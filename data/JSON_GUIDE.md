# 📦 CSV to JSON Conversion - Complete Guide

## ✅ Yang Sudah Dibuat:

### 1. **Script Converter**

**Lokasi:** `data/csv_to_json.py`

**Fungsi:**

- Convert `merge-all-clean.csv` → `documents.json`
- Format JSON dengan metadata lengkap
- Include pagination support

**Cara Pakai:**

```bash
cd data
python csv_to_json.py
```

**Output:**

```
📂 Location: data/index/documents.json
📊 Size: ~0.93 MB
📄 Total: 376 documents
```

---

### 2. **JSON File Structure**

**Lokasi:** `data/index/documents.json`

```json
{
  "total_documents": 376,
  "sources": {
    "bolanet": 150,
    "kompas": 124,
    "sindonews": 102
  },
  "documents": [
    {
      "doc_id": 0,
      "title": "RESMI: Rizky Ridho Perpanjang Kontrak...",
      "content": "resmi rizky ridho panjang kontrak...",
      "url": "https://bolanet.com/...",
      "source": "bolanet",
      "main_image": "https://...",
      "published_at": "2025-11-15"
    }
    // ... 375 more documents
  ]
}
```

---

### 3. **Backend API Endpoint**

**Endpoint Baru:** `GET /api/documents`

**Features:**

- ✅ Pagination support
- ✅ Configurable page size
- ✅ Source statistics
- ✅ Easy to test in Postman

**Examples:**

```bash
# Get first 10 documents
GET http://localhost:5000/api/documents

# Get page 2, 20 documents per page
GET http://localhost:5000/api/documents?page=2&per_page=20

# Get specific page
GET http://localhost:5000/api/documents?page=5&per_page=50
```

**Response:**

```json
{
  "total_documents": 376,
  "page": 1,
  "per_page": 10,
  "total_pages": 38,
  "sources": {
    "bolanet": 150,
    "kompas": 124,
    "sindonews": 102
  },
  "documents": [
    {
      "doc_id": 0,
      "title": "...",
      "content": "...",
      "url": "...",
      "source": "...",
      "main_image": "...",
      "published_at": "..."
    }
    // ... 9 more
  ]
}
```

---

## 🧪 Testing di Postman

### **Step 1: Import Collection**

Postman collection sudah diupdate dengan endpoint baru:

- Endpoint #7: "Get All Documents (JSON)"

### **Step 2: Test Endpoints**

#### **Test 1: Get Default (10 documents)**

```
Method: GET
URL: http://localhost:5000/api/documents
```

#### **Test 2: Get with Pagination**

```
Method: GET
URL: http://localhost:5000/api/documents?page=2&per_page=20

Query Params:
- page: 2
- per_page: 20
```

#### **Test 3: Get Large Page**

```
Method: GET
URL: http://localhost:5000/api/documents?page=1&per_page=100

Query Params:
- page: 1
- per_page: 100 (max limit)
```

---

## 📂 File Locations & Structure

```
UAS/
├── data/
│   ├── merge-all-clean.csv       # ← Original CSV
│   ├── csv_to_json.py            # ← Converter script ✨ NEW
│   └── index/
│       ├── documents.json        # ← JSON output ✨ NEW
│       ├── tfidf_index.pkl
│       └── bm25_index.pkl
│
├── backend/
│   ├── app.py                    # ← Updated with new endpoint
│   ├── config.py                 # ← Updated with JSON path
│   ├── test_json_endpoint.py    # ← Test script ✨ NEW
│   └── Search_Engine_API.postman_collection.json  # ← Updated
```

---

## 💡 Benefits of JSON Format

### **1. Easy Testing in Postman**

- ✅ Direct preview in Postman
- ✅ No need to parse CSV
- ✅ Beautiful JSON formatting

### **2. Frontend Integration**

```javascript
// Easy to consume in frontend
const response = await fetch("/api/documents?page=1&per_page=10");
const data = await response.json();

data.documents.forEach((doc) => {
  console.log(doc.title);
});
```

### **3. Pagination Support**

- ✅ Load data in chunks
- ✅ Better performance
- ✅ User-friendly

### **4. Structured Data**

- ✅ Typed fields
- ✅ Nested objects
- ✅ Easy to query

---

## 🔧 Configuration

### **Path Configuration (config.py)**

```python
# CSV path (original)
DATA_PATH = os.path.join(DATA_DIR, "merge-all-clean.csv")

# JSON path (new)
JSON_DATA_PATH = os.path.join(DATA_DIR, "index", "documents.json")
```

### **Pagination Limits**

```python
# In app.py endpoint
DEFAULT_PER_PAGE = 10
MAX_PER_PAGE = 100  # Prevent too large requests
```

---

## 📊 API Endpoints Summary

| #   | Method | Endpoint              | Function                           |
| --- | ------ | --------------------- | ---------------------------------- |
| 1   | GET    | `/api/health`         | Check server status                |
| 2   | POST   | `/api/search`         | Search (TF-IDF/BM25)               |
| 3   | POST   | `/api/search/compare` | Compare algorithms                 |
| 4   | GET    | `/api/document/<id>`  | Get single document (CSV)          |
| 5   | GET    | `/api/stats`          | Corpus statistics                  |
| 6   | GET    | `/api/documents`      | **Get all docs (JSON)** ✨ **NEW** |

---

## 🚀 Quick Start

### **1. Generate JSON (First Time Only)**

```bash
cd data
python csv_to_json.py
```

**Output:**

```
✅ Saved 376 documents
📦 File size: 0.93 MB
📂 Location: data/index/documents.json
```

### **2. Start Server**

```bash
cd backend
python app.py
```

### **3. Test in Postman**

```
1. Import updated collection: Search_Engine_API.postman_collection.json
2. Click endpoint #7: "Get All Documents (JSON)"
3. Click Send
4. View beautiful JSON response!
```

### **4. Test with Browser**

```
Open: http://localhost:5000/api/documents
```

---

## 💡 Use Cases

### **For Testing:**

- ✅ Verify all documents loaded correctly
- ✅ Check data structure
- ✅ Browse documents easily in Postman

### **For Frontend:**

- ✅ Display document list/table
- ✅ Build pagination UI
- ✅ Show document cards
- ✅ Create browse/explore page

### **For Development:**

- ✅ Quick data inspection
- ✅ Debugging
- ✅ API testing

---

## 📝 Notes

1. **File Size:** JSON file ~0.93 MB (safe untuk load di memory)
2. **Pagination:** Max 100 documents per request (prevent overload)
3. **Auto-generated:** Run `csv_to_json.py` after CSV updates
4. **Location:** Stored in `data/index/` bersama dengan index files
5. **Format:** UTF-8 encoding, pretty printed (indent=2)

---

## ✅ Summary

**What's Added:**

1. ✅ `data/csv_to_json.py` - Converter script
2. ✅ `data/index/documents.json` - JSON output (376 docs)
3. ✅ `backend/config.py` - JSON_DATA_PATH variable
4. ✅ `backend/app.py` - New endpoint `/api/documents`
5. ✅ Postman collection - Updated with endpoint #7
6. ✅ `backend/test_json_endpoint.py` - Test script

**Ready to Use:**

- ✅ JSON file generated (0.93 MB)
- ✅ API endpoint working
- ✅ Postman collection updated
- ✅ Pagination implemented
- ✅ Server running on port 5000

**Test Now:**

```bash
# In Postman
GET http://localhost:5000/api/documents

# Or browser
http://localhost:5000/api/documents
```

🎉 **JSON endpoint ready untuk testing di Postman!**
