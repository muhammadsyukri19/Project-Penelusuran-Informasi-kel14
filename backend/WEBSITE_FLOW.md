# Flow Website & API Integration

## 🎯 Alur Website

```
┌─────────────────────────────────────────────────────────────┐
│                     HALAMAN 1: HOME                         │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │   🔍  Cari Berita Sepak Bola Indonesia             │    │
│  │                                                      │    │
│  │   [____________________________________]  [Search]   │    │
│  │        (Input query dari user)                       │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  User ketik query → Tekan "Search" → Pindah ke Compare     │
└─────────────────────────────────────────────────────────────┘

                            ↓ (Setelah klik Search)

┌─────────────────────────────────────────────────────────────┐
│              HALAMAN 2: COMPARE RESULTS                      │
│                                                              │
│  Query: "timnas indonesia"                    [Compare ℹ️]  │
│                                                              │
│  ┌─────────────────────┬─────────────────────┐            │
│  │   TF-IDF Results    │    BM25 Results      │            │
│  │   ⏱️ 0.05s          │    ⏱️ 0.02s          │            │
│  ├─────────────────────┼─────────────────────┤            │
│  │ 1. [Title 1]        │ 1. [Title 1]         │            │
│  │    Score: 0.89      │    Score: 8.5        │            │
│  │    [Snippet...]     │    [Snippet...]      │            │
│  │                     │                      │            │
│  │ 2. [Title 2]        │ 2. [Title 3]         │            │
│  │    Score: 0.75      │    Score: 7.2        │            │
│  │    [Snippet...]     │    [Snippet...]      │            │
│  │                     │                      │            │
│  │ 3. [Title 3]        │ 3. [Title 2]         │            │
│  │    ...              │    ...               │            │
│  └─────────────────────┴─────────────────────┘            │
│                                                              │
│  * Klik Compare button → Muncul CARD MODAL/SIDEBAR         │
└─────────────────────────────────────────────────────────────┘

                            ↓ (Klik Compare ℹ️)

┌─────────────────────────────────────────────────────────────┐
│                  CARD: COMPARISON DETAIL                     │
│                                                              │
│  📊 Perbandingan Algoritma                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│  ⚡ Kecepatan:                                              │
│     • TF-IDF: 0.0512s                                       │
│     • BM25: 0.0234s                                         │
│     • Winner: BM25 (2.2x lebih cepat)                       │
│                                                              │
│  🎯 Hasil:                                                  │
│     • TF-IDF: 10 dokumen                                    │
│     • BM25: 10 dokumen                                      │
│     • Overlap: 6 dokumen sama (60%)                         │
│                                                              │
│  📈 Dokumen Unik:                                           │
│     • Hanya di TF-IDF: 4 dokumen                            │
│       → Doc #5, #12, #45, #67                               │
│     • Hanya di BM25: 4 dokumen                              │
│       → Doc #8, #23, #56, #89                               │
│                                                              │
│  💡 Kesimpulan:                                             │
│     BM25 lebih cepat dan memberikan hasil                   │
│     yang berbeda 40% dari TF-IDF                            │
│                                                              │
│  [Tutup]                                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 API Integration untuk Frontend

### **HALAMAN 1: Home (Search Page)**

#### Saat User Submit Query:

```javascript
// Frontend code (contoh)
async function handleSearch(event) {
  event.preventDefault();
  const query = document.getElementById("searchInput").value;

  // Redirect ke halaman compare dengan query parameter
  window.location.href = `/compare?q=${encodeURIComponent(query)}`;
}
```

---

### **HALAMAN 2: Compare Page**

#### Load Data Saat Halaman Dibuka:

```javascript
// Frontend code
async function loadCompareResults() {
  const params = new URLSearchParams(window.location.search);
  const query = params.get("q");

  // ✅ Panggil API Compare
  const response = await fetch("http://localhost:5000/api/search/compare", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: query,
      limit: 10, // Tampilkan 10 hasil per algoritma
    }),
  });

  const data = await response.json();

  // Render hasil
  renderTfidfResults(data.tfidf.results);
  renderBm25Results(data.bm25.results);

  // Simpan comparison data untuk modal
  window.comparisonData = data.comparison;
}
```

#### Response dari API:

```json
{
  "query": "timnas indonesia",
  "tfidf": {
    "execution_time": 0.0512,
    "total_results": 10,
    "results": [
      {
        "doc_id": 123,
        "title": "Timnas Indonesia Menang 2-1 Melawan Thailand",
        "score": 0.8945,
        "snippet": "Timnas Indonesia berhasil mengalahkan Thailand...",
        "url": "https://kompas.com/...",
        "source": "kompas"
      }
      // ... 9 results lainnya
    ]
  },
  "bm25": {
    "execution_time": 0.0234,
    "total_results": 10,
    "results": [
      {
        "doc_id": 123,
        "title": "Timnas Indonesia Menang 2-1 Melawan Thailand",
        "score": 8.523,
        "snippet": "Timnas Indonesia berhasil mengalahkan Thailand...",
        "url": "https://kompas.com/...",
        "source": "kompas"
      }
      // ... 9 results lainnya
    ]
  },
  "comparison": {
    "overlap_count": 6,
    "overlap_percentage": 60.0,
    "overlap_docs": [123, 45, 67, 89, 12, 34],
    "tfidf_only": [5, 12, 45, 67],
    "bm25_only": [8, 23, 56, 89],
    "faster_algorithm": "bm25",
    "speed_difference": 0.0278
  }
}
```

---

### **CARD MODAL: Comparison Detail**

#### Saat User Klik Button "Compare ℹ️":

```javascript
// Frontend code
function showComparisonModal() {
  const data = window.comparisonData;

  // Render modal dengan data comparison
  const modalHTML = `
    <div class="modal">
      <h3>📊 Perbandingan Algoritma</h3>
      
      <div class="speed-section">
        <h4>⚡ Kecepatan:</h4>
        <p>• TF-IDF: ${data.tfidf_time}s</p>
        <p>• BM25: ${data.bm25_time}s</p>
        <p>• Winner: ${data.faster_algorithm.toUpperCase()} 
           (${(data.speed_difference * 1000).toFixed(0)}ms lebih cepat)</p>
      </div>
      
      <div class="overlap-section">
        <h4>🎯 Hasil:</h4>
        <p>• Overlap: ${data.overlap_count} dokumen 
           (${data.overlap_percentage}%)</p>
        <p>• Hanya di TF-IDF: ${data.tfidf_only.length} dokumen</p>
        <p>• Hanya di BM25: ${data.bm25_only.length} dokumen</p>
      </div>
      
      <button onclick="closeModal()">Tutup</button>
    </div>
  `;

  document.body.insertAdjacentHTML("beforeend", modalHTML);
}
```

---

## 🎨 Rekomendasi UI/UX

### Halaman Home:

- **Hero Section**: Input search besar di tengah
- **Placeholder**: "Cari berita: timnas indonesia, persib bandung, ..."
- **Button**: Warna mencolok (primary color)

### Halaman Compare:

- **Layout**: Split screen 50-50 (TF-IDF kiri, BM25 kanan)
- **Header**: Tampilkan query + execution time
- **Result Card**:
  - Title (link ke artikel)
  - Score badge
  - Snippet (150 chars)
  - Source badge (Kompas/Bolanet/SINDOnews)
- **Button Compare**: Fixed position di kanan atas

### Modal Compare:

- **Style**: Card/Modal dengan backdrop gelap
- **Animasi**: Slide dari kanan
- **Konten**:
  - Speed comparison (bar chart?)
  - Overlap percentage (pie chart?)
  - Unique documents list
  - Kesimpulan singkat

---

## 📦 API Endpoints yang Dibutuhkan

| Halaman | API Endpoint          | Method | Fungsi                        |
| ------- | --------------------- | ------ | ----------------------------- |
| Home    | `/api/health`         | GET    | Cek server ready              |
| Compare | `/api/search/compare` | POST   | Get both results + comparison |
| Detail  | `/api/document/<id>`  | GET    | View full article (optional)  |

**NOTE**: Cukup 1 API call untuk load halaman compare!
API `/api/search/compare` sudah return semua data yang dibutuhkan:

- ✅ TF-IDF results
- ✅ BM25 results
- ✅ Comparison statistics
- ✅ Execution time
- ✅ Overlap data

---

## 🚀 Next Steps

### Frontend Development:

1. **Setup Project**: React/Vue/HTML+Vanilla JS
2. **Create Pages**:
   - `index.html` (Home/Search)
   - `compare.html` (Results + Comparison)
3. **Components**:
   - SearchBar component
   - ResultCard component
   - ComparisonModal component
4. **Styling**: CSS/TailwindCSS
5. **Integration**: Connect to API

### Testing Flow:

1. User buka `http://localhost:3000/` (home)
2. Ketik "timnas indonesia"
3. Klik Search → Redirect ke `/compare?q=timnas+indonesia`
4. Load results from API
5. Tampilkan split view
6. Klik Compare button → Show modal

---

## 💡 Tips:

1. **Loading State**: Tampilkan skeleton loader saat fetch API
2. **Error Handling**: Handle query kosong, API error, no results
3. **Responsive**: Desktop (split), Mobile (tabs/accordion)
4. **Highlight**: Highlight query terms di snippet
5. **Bookmark**: Allow share URL with query parameter

---

**Ready untuk mulai frontend development!** 🎯
