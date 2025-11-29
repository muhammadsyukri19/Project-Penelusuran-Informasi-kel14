import { useState, useEffect } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";

function ComparePage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const query = searchParams.get("q") || "";

  const [searchQuery, setSearchQuery] = useState(query);
  const [loading, setLoading] = useState(true);
  const [comparisonData, setComparisonData] = useState(null);
  const [error, setError] = useState(null);
  const [selectedDoc, setSelectedDoc] = useState(null);

  useEffect(() => {
    if (query) {
      fetchDetailedComparison(query);
    }
  }, [query]);

  const fetchDetailedComparison = async (searchQuery) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:5000/api/search/compare", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: searchQuery }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch results");
      }

      const data = await response.json();
      setComparisonData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/compare?q=${encodeURIComponent(searchQuery)}`);
      fetchDetailedComparison(searchQuery);
    }
  };

  const handleDocumentClick = (doc, algorithm) => {
    setSelectedDoc({ ...doc, algorithm });
  };

  return (
    <div className="relative min-h-screen bg-slate-100">
      {/* Background with light overlay */}
      <div
        className="fixed inset-0 bg-cover bg-center z-0"
        style={{
          backgroundImage: "url(/image/frontend-bg.jpg)",
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-b from-white/40 via-white/45 to-white/40" />
      </div>

      {/* Header */}
      <header className="sticky top-0 z-30 bg-grey/10 backdrop-blur-lg border-b border-slate-300 shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center gap-6">
            <Link to="/" className="flex-shrink-0">
              <img
                src="/image/nubofind.png"
                alt="Find Logo"
                className="h-10 w-auto"
              />
            </Link>

            <form onSubmit={handleSearch} className="flex-1 max-w-3xl">
              <div className="relative">
                <svg
                  className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 pointer-events-none"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <circle cx="11" cy="11" r="8" />
                  <path d="M21 21l-4.35-4.35" />
                </svg>
                <input
                  type="text"
                  className="w-full pl-12 pr-20 py-3 bg-white border border-slate-300 rounded-xl text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary/50 transition-all duration-300"
                  placeholder="Cari pemain, tim, atau berita sepak bola..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button
                  type="submit"
                  className="absolute right-2 top-1/2 -translate-y-1/2 bg-gradient-to-r from-primary to-accent text-white px-4 py-2 rounded-lg hover:shadow-lg hover:shadow-primary/50 transition-all duration-300"
                >
                  Cari
                </button>
              </div>
            </form>

            <Link
              to={`/search?q=${encodeURIComponent(query)}`}
              className="px-4 py-2 text-slate-700 hover:text-primary transition-colors duration-300 font-medium"
            >
              ← Kembali
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 container mx-auto px-6 py-8">
        {/* Page Title */}
        <div className="mb-8 animate-fadeIn">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">
            Perbandingan Detail Algoritma
          </h1>
          <p className="text-slate-600">
            Query: <span className="font-semibold text-primary">"{query}"</span>
          </p>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-red-700 animate-fadeIn">
            <p className="font-semibold">Error:</p>
            <p>{error}</p>
          </div>
        )}

        {/* Detailed Comparison */}
        {!loading && !error && comparisonData && (
          <div className="space-y-8 animate-fadeInUp">
            {/* Algorithm Configuration Cards */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* TF-IDF Config */}
              <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-slate-300 p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                    TF
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-slate-800">TF-IDF</h3>
                    <p className="text-sm text-slate-600">
                      Term Frequency - Inverse Document Frequency
                    </p>
                  </div>
                </div>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between py-2 border-b border-slate-200">
                    <span className="text-slate-600">Total Hasil:</span>
                    <span className="font-semibold text-slate-800">
                      {comparisonData.tfidf?.results?.length || 0}
                    </span>
                  </div>
                  <div className="flex justify-between py-2 border-b border-slate-200">
                    <span className="text-slate-600">Waktu Eksekusi:</span>
                    <span className="font-semibold text-slate-800">
                      {comparisonData.tfidf?.execution_time?.toFixed(4) ||
                        "N/A"}{" "}
                      detik
                    </span>
                  </div>
                  <div className="flex justify-between py-2 border-b border-slate-200">
                    <span className="text-slate-600">Top Score:</span>
                    <span className="font-semibold text-blue-600">
                      {comparisonData.tfidf?.results?.[0]?.score?.toFixed(4) ||
                        "N/A"}
                    </span>
                  </div>
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                    <p className="text-xs text-slate-700 leading-relaxed">
                      <strong>Formula:</strong> TF-IDF = TF × IDF
                      <br />
                      Menghitung frekuensi term dalam dokumen dan
                      mempertimbangkan seberapa umum term tersebut di seluruh
                      dokumen.
                    </p>
                  </div>
                </div>
              </div>

              {/* BM25 Config */}
              <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-slate-300 p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center text-white font-bold text-lg">
                    BM
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-slate-800">BM25</h3>
                    <p className="text-sm text-slate-600">Best Matching 25</p>
                  </div>
                </div>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between py-2 border-b border-slate-200">
                    <span className="text-slate-600">Total Hasil:</span>
                    <span className="font-semibold text-slate-800">
                      {comparisonData.bm25?.results?.length || 0}
                    </span>
                  </div>
                  <div className="flex justify-between py-2 border-b border-slate-200">
                    <span className="text-slate-600">Waktu Eksekusi:</span>
                    <span className="font-semibold text-slate-800">
                      {comparisonData.bm25?.execution_time?.toFixed(4) || "N/A"}{" "}
                      detik
                    </span>
                  </div>
                  <div className="flex justify-between py-2 border-b border-slate-200">
                    <span className="text-slate-600">Top Score:</span>
                    <span className="font-semibold text-primary">
                      {comparisonData.bm25?.results?.[0]?.score?.toFixed(4) ||
                        "N/A"}
                    </span>
                  </div>
                  <div className="mt-4 p-3 bg-green-50 rounded-lg">
                    <p className="text-xs text-slate-700 leading-relaxed">
                      <strong>Formula:</strong> BM25 dengan k1=1.5, b=0.75
                      <br />
                      Algoritma probabilistik yang mengatasi saturasi term
                      frequency dan normalisasi panjang dokumen.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Full Results Comparison Table */}
            <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-slate-300 overflow-hidden">
              <div className="bg-gradient-to-r from-slate-700 to-slate-800 text-white px-6 py-4">
                <h3 className="text-xl font-bold">Semua Hasil Pencarian</h3>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-100 border-b border-slate-300">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase">
                        Rank
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase">
                        TF-IDF Results
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase">
                        Score
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase">
                        BM25 Results
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase">
                        Score
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200">
                    {Array.from({
                      length: Math.max(
                        comparisonData.tfidf?.results?.length || 0,
                        comparisonData.bm25?.results?.length || 0
                      ),
                    }).map((_, index) => {
                      const tfidfDoc = comparisonData.tfidf?.results?.[index];
                      const bm25Doc = comparisonData.bm25?.results?.[index];

                      return (
                        <tr
                          key={index}
                          className="hover:bg-slate-50 transition-colors"
                        >
                          <td className="px-6 py-4 text-sm font-semibold text-slate-700">
                            #{index + 1}
                          </td>
                          <td className="px-6 py-4">
                            {tfidfDoc ? (
                              <button
                                onClick={() =>
                                  handleDocumentClick(tfidfDoc, "TF-IDF")
                                }
                                className="text-left hover:text-blue-600 transition-colors"
                              >
                                <p className="text-sm font-medium text-slate-800 line-clamp-2">
                                  {tfidfDoc.title}
                                </p>
                                <p className="text-xs text-slate-500 mt-1">
                                  {tfidfDoc.source}
                                </p>
                              </button>
                            ) : (
                              <span className="text-sm text-slate-400">-</span>
                            )}
                          </td>
                          <td className="px-6 py-4">
                            {tfidfDoc ? (
                              <span className="text-sm font-semibold text-blue-600">
                                {tfidfDoc.score?.toFixed(4)}
                              </span>
                            ) : (
                              <span className="text-sm text-slate-400">-</span>
                            )}
                          </td>
                          <td className="px-6 py-4">
                            {bm25Doc ? (
                              <button
                                onClick={() =>
                                  handleDocumentClick(bm25Doc, "BM25")
                                }
                                className="text-left hover:text-primary transition-colors"
                              >
                                <p className="text-sm font-medium text-slate-800 line-clamp-2">
                                  {bm25Doc.title}
                                </p>
                                <p className="text-xs text-slate-500 mt-1">
                                  {bm25Doc.source}
                                </p>
                              </button>
                            ) : (
                              <span className="text-sm text-slate-400">-</span>
                            )}
                          </td>
                          <td className="px-6 py-4">
                            {bm25Doc ? (
                              <span className="text-sm font-semibold text-primary">
                                {bm25Doc.score?.toFixed(4)}
                              </span>
                            ) : (
                              <span className="text-sm text-slate-400">-</span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Document Detail Modal */}
      {selectedDoc && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fadeIn"
          onClick={() => setSelectedDoc(null)}
        >
          <div
            className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[80vh] overflow-hidden animate-fadeInUp"
            onClick={(e) => e.stopPropagation()}
          >
            <div
              className={`px-6 py-4 ${
                selectedDoc.algorithm === "TF-IDF"
                  ? "bg-gradient-to-r from-blue-500 to-blue-600"
                  : "bg-gradient-to-r from-primary to-accent"
              } text-white`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm opacity-90">{selectedDoc.algorithm}</p>
                  <h3 className="text-xl font-bold">Detail Dokumen</h3>
                </div>
                <button
                  onClick={() => setSelectedDoc(null)}
                  className="w-8 h-8 flex items-center justify-center hover:bg-white/20 rounded-lg transition-colors"
                >
                  <svg
                    className="w-5 h-5"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <div className="p-6 overflow-y-auto max-h-[calc(80vh-100px)]">
              <h4 className="text-2xl font-bold text-slate-800 mb-4">
                {selectedDoc.title}
              </h4>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-xs text-slate-600 mb-1">Sumber</p>
                  <p className="text-sm font-semibold text-slate-800">
                    {selectedDoc.source}
                  </p>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-xs text-slate-600 mb-1">Skor Relevansi</p>
                  <p
                    className={`text-sm font-semibold ${
                      selectedDoc.algorithm === "TF-IDF"
                        ? "text-blue-600"
                        : "text-primary"
                    }`}
                  >
                    {selectedDoc.score?.toFixed(4)}
                  </p>
                </div>
              </div>

              <div className="mb-6">
                <p className="text-sm font-semibold text-slate-700 mb-2">
                  Konten:
                </p>
                <p className="text-sm text-slate-600 leading-relaxed">
                  {selectedDoc.content}
                </p>
              </div>

              {selectedDoc.url && (
                <a
                  href={selectedDoc.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`inline-flex items-center gap-2 px-4 py-2 ${
                    selectedDoc.algorithm === "TF-IDF"
                      ? "bg-blue-600 hover:bg-blue-700"
                      : "bg-primary hover:bg-primary/90"
                  } text-white rounded-lg transition-colors`}
                >
                  Baca Artikel Lengkap
                  <svg
                    className="w-4 h-4"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3" />
                  </svg>
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ComparePage;
