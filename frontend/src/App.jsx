import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [algo, setAlgo] = useState("tfidf");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setError("");
    setHasSearched(true);

    if (!query.trim()) {
      setResults([]);
      setError("Silakan ketik kata kunci pencarian terlebih dahulu.");
      return;
    }

    try {
      setLoading(true);
      setResults([]);
      const API_BASE = "";
      const url = `${API_BASE}/api/search?q=${encodeURIComponent(
        query
      )}&algo=${algo}`;
      const res = await fetch(url);

      if (!res.ok) {
        throw new Error(
          `Gagal memuat data (status ${res.status}). Pastikan backend /api/search mengembalikan JSON.`
        );
      }

      const data = await res.json();
      if (!Array.isArray(data)) {
        throw new Error("Format respons backend tidak sesuai (bukan array JSON).");
      }
      setResults(data);
    } catch (err) {
      console.error(err);
      setError(
        err.message ||
          "Terjadi kesalahan saat mengambil data. Cek kembali backend /api/search."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return "-";
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    return d.toLocaleDateString("id-ID", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const formatScore = (score) => {
    if (score === null || score === undefined) return "-";
    return Number(score).toFixed(4);
  };

  return (
    <div className="app-root">
      {/* Stadium Background */}
      <div className="stadium-background"></div>
      
      <div className="app-container">
        {/* Header with Football Icon */}
        <header className="app-header">
          <div className="header-icon">⚽</div>
          <h1>Pencarian Berita Sepak Bola</h1>
          <p className="app-subtitle">
            Portal berita sepak bola terlengkap dengan pencarian cerdas
          </p>
        </header>

        {/* Search Section */}
        <section className="search-section">
          <form className="search-form" onSubmit={handleSearch}>
            <div className="input-group">
              <label htmlFor="searchInput" className="input-label">
                🔍 Cari Berita Sepak Bola
              </label>
              <input
                id="searchInput"
                type="text"
                className="search-input"
                placeholder="Ketik kata kunci: Persija, Liga Champions, Timnas..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>

            <div className="algo-selector">
              <span className="algo-label">Algoritma Pencarian:</span>
              <div className="algo-options">
                <label className="algo-option">
                  <input
                    type="radio"
                    name="algo"
                    value="tfidf"
                    checked={algo === "tfidf"}
                    onChange={(e) => setAlgo(e.target.value)}
                  />
                  <span className="algo-badge">TF-IDF</span>
                </label>
                <label className="algo-option">
                  <input
                    type="radio"
                    name="algo"
                    value="bm25"
                    checked={algo === "bm25"}
                    onChange={(e) => setAlgo(e.target.value)}
                  />
                  <span className="algo-badge">BM25</span>
                </label>
              </div>
            </div>

            <button
              type="submit"
              className="search-button"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Mencari Berita...
                </>
              ) : (
                <>
                  <span className="btn-icon">🔎</span>
                  Cari Sekarang
                </>
              )}
            </button>
          </form>

          <p className="help-text">
            💡 <strong>Tips Pencarian:</strong> Gunakan kata kunci spesifik untuk hasil lebih akurat
          </p>

          {error && (
            <div className="error-box">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}
        </section>

        {/* Results Section */}
        <section className="results-section">
          {hasSearched && !loading && results.length === 0 && !error && (
            <div className="empty-state">
              <div className="empty-icon">📰</div>
              <p className="empty-title">Tidak ada hasil ditemukan</p>
              <p className="empty-subtitle">
                Coba kata kunci lain atau ubah algoritma pencarian
              </p>
            </div>
          )}

          {results.length > 0 && (
            <>
              <div className="results-summary">
                <span className="results-count">{results.length}</span>
                <span className="results-text">
                  berita ditemukan untuk <strong>"{query}"</strong>
                </span>
              </div>
              <ul className="results-list">
                {results.map((item, idx) => (
                  <li key={idx} className="result-card">
                    <div className="result-number">{idx + 1}</div>
                    <div className="result-content">
                      <a
                        href={item.url || "#"}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="result-title"
                      >
                        {item.title || "Tanpa Judul"}
                      </a>
                      <div className="result-meta">
                        <span className="meta-item">
                          📅 {formatDate(item.date)}
                        </span>
                        <span className="meta-divider">•</span>
                        <span className="meta-item">
                          Skor: <strong>{formatScore(item.score)}</strong>
                        </span>
                      </div>
                      <p className="result-snippet">
                        {item.snippet || "Tidak ada ringkasan tersedia."}
                      </p>
                    </div>
                  </li>
                ))}
              </ul>
            </>
          )}
        </section>

        {/* Footer */}
        <footer className="app-footer">
          <p>
            ⚽ <strong>Football News Search Engine</strong> • Powered by Kelompok 14 UAS PI
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
