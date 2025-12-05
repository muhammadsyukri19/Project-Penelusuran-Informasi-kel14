import { useState, useEffect } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";

function SearchPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const query = searchParams.get("q") || "";

  const [searchQuery, setSearchQuery] = useState(query);
  const [loading, setLoading] = useState(true);
  const [tfidfResults, setTfidfResults] = useState([]);
  const [bm25Results, setBm25Results] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (query) {
      fetchComparisonResults(query);
    }
  }, [query]);

  const fetchComparisonResults = async (searchQuery) => {
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
      setTfidfResults(data.tfidf.results || []);
      setBm25Results(data.bm25.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
      fetchComparisonResults(searchQuery);
    }
  };

  const handleViewDetails = () => {
    navigate(`/compare?q=${encodeURIComponent(query)}`);
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

      {/* Header with Logo and Search Bar */}
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
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 container mx-auto px-6 py-8">
        {/* Search Info */}
        <div className="mb-6 animate-fadeIn">
          <h2 className="text-2xl font-bold text-slate-800 mb-2">
            Hasil pencarian: <span className="text-primary">"{query}"</span>
          </h2>
          <p className="text-slate-600">
            Membandingkan hasil dari 2 algoritma: TF-IDF dan BM25
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

        {/* Results Comparison */}
        {!loading && !error && (
          <div className="space-y-6 animate-fadeInUp">
            {/* Comparison Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* TF-IDF Results */}
              <div className="bg-white/20 backdrop-blur-lg rounded-2xl shadow-xl border border-slate-300 overflow-hidden">
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-4">
                  <h3 className="text-xl font-bold">TF-IDF Algorithm</h3>
                  <p className="text-sm text-blue-100 mt-1">
                    {tfidfResults.length} hasil ditemukan
                  </p>
                </div>

                <div className="p-6 space-y-4 max-h-[600px] overflow-y-auto">
                  {tfidfResults.length === 0 ? (
                    <p className="text-slate-500 text-center py-8">
                      Tidak ada hasil ditemukan
                    </p>
                  ) : (
                    tfidfResults.slice(0, 5).map((result, index) => (
                      <div
                        key={index}
                        className="flex gap-3 p-4 bg-white border border-slate-200 rounded-lg hover:shadow-lg hover:border-blue-300 transition-all duration-300"
                      >
                        {result.main_image && (
                          <img
                            src={`http://localhost:5000/api/image-proxy?url=${encodeURIComponent(
                              result.main_image
                            )}`}
                            alt={result.title}
                            className="w-24 h-24 object-cover rounded-lg flex-shrink-0 bg-slate-200"
                            onError={(e) => {
                              console.log(
                                "TF-IDF Image failed:",
                                result.source,
                                result.main_image
                              );
                              e.target.src =
                                'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="%23e2e8f0"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="%2394a3b8" font-family="sans-serif" font-size="12">No Image</text></svg>';
                            }}
                          />
                        )}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-3 mb-2">
                            <h4 className="font-semibold text-slate-800 line-clamp-2">
                              {result.title}
                            </h4>
                            <span className="flex-shrink-0 px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded">
                              #{index + 1}
                            </span>
                          </div>
                          <p className="text-sm text-slate-600 line-clamp-2 mb-2">
                            {result.content}
                          </p>
                          <div className="flex items-center justify-between text-xs">
                            <span className="text-slate-500">
                              {result.source}
                            </span>
                            <span className="text-blue-600 font-semibold">
                              Score: {result.score?.toFixed(4) || "N/A"}
                            </span>
                          </div>
                          {result.url && (
                            <a
                              href={result.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs text-blue-600 hover:underline mt-2 inline-block"
                            >
                              Baca selengkapnya →
                            </a>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* BM25 Results */}
              <div className="bg-white/20 backdrop-blur-lg rounded-2xl shadow-xl border border-slate-300 overflow-hidden">
                <div className="bg-gradient-to-r from-primary to-accent text-white px-6 py-4">
                  <h3 className="text-xl font-bold">BM25 Algorithm</h3>
                  <p className="text-sm text-green-100 mt-1">
                    {bm25Results.length} hasil ditemukan
                  </p>
                </div>

                <div className="p-6 space-y-4 max-h-[600px] overflow-y-auto">
                  {bm25Results.length === 0 ? (
                    <p className="text-slate-500 text-center py-8">
                      Tidak ada hasil ditemukan
                    </p>
                  ) : (
                    bm25Results.slice(0, 5).map((result, index) => (
                      <div
                        key={index}
                        className="flex gap-3 p-4 bg-white border border-slate-200 rounded-lg hover:shadow-lg hover:border-primary transition-all duration-300"
                      >
                        {result.main_image && (
                          <img
                            src={`http://localhost:5000/api/image-proxy?url=${encodeURIComponent(
                              result.main_image
                            )}`}
                            alt={result.title}
                            className="w-24 h-24 object-cover rounded-lg flex-shrink-0 bg-slate-200"
                            onError={(e) => {
                              console.log(
                                "BM25 Image failed:",
                                result.source,
                                result.main_image
                              );
                              e.target.src =
                                'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="%23e2e8f0"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="%2394a3b8" font-family="sans-serif" font-size="12">No Image</text></svg>';
                            }}
                          />
                        )}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-3 mb-2">
                            <h4 className="font-semibold text-slate-800 line-clamp-2">
                              {result.title}
                            </h4>
                            <span className="flex-shrink-0 px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">
                              #{index + 1}
                            </span>
                          </div>
                          <p className="text-sm text-slate-600 line-clamp-2 mb-2">
                            {result.content}
                          </p>
                          <div className="flex items-center justify-between text-xs">
                            <span className="text-slate-500">
                              {result.source}
                            </span>
                            <span className="text-primary font-semibold">
                              Score: {result.score?.toFixed(4) || "N/A"}
                            </span>
                          </div>
                          {result.url && (
                            <a
                              href={result.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs text-primary hover:underline mt-2 inline-block"
                            >
                              Baca selengkapnya →
                            </a>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>

            {/* View Detailed Comparison Button */}
            <div className="flex justify-center mt-8">
              <button
                onClick={handleViewDetails}
                className="px-8 py-3 bg-gradient-to-r from-primary to-accent text-white font-semibold rounded-xl hover:shadow-xl hover:shadow-primary/50 transition-all duration-300 transform hover:-translate-y-1 flex items-center gap-2"
              >
                <svg
                  className="w-5 h-5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  <path d="M9 12h6m-6 4h6" />
                </svg>
                Lihat Konfigurasi Lengkap & Detail Perbandingan
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default SearchPage;
