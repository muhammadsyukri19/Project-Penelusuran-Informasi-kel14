import { useState, useEffect } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";
import LoadingScreen from "../components/LoadingScreen";

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
      // Minimum loading time 2 detik untuk menampilkan loading animation
      const [response] = await Promise.all([
        fetch("http://localhost:5000/api/search/compare", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: searchQuery }),
        }),
        new Promise((resolve) => setTimeout(resolve, 2000)),
      ]);

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
                  className="absolute right-2 top-1/2 -translate-y-1/2 bg-gradient-to-r from-primary to-accent text-white px-4 py-2 rounded-2xl hover:shadow-lg hover:shadow-primary/50 transition-all duration-300"
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
          <LoadingScreen
            message="Mencari Hasil"
            subtitle="Membandingkan TF-IDF dan BM25 untuk query Anda..."
          />
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
            <div className="grid md:grid-cols-2 gap-8">
              {/* TF-IDF Results */}
              <div className="bg-white/60 backdrop-blur-2xl rounded-3xl shadow-xl border border-slate-200/30 overflow-hidden transition-all duration-500 hover:shadow-2xl hover:border-primary/20">
                <div className="bg-slate-800/90 backdrop-blur-md px-8 py-6 border-b border-slate-700/50">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-2 h-2 bg-primary rounded-full"></div>
                    <h3 className="text-2xl font-bold text-white tracking-tight">
                      TF-IDF Algorithm
                    </h3>
                  </div>
                  <p className="text-sm text-slate-300 font-medium">
                    {tfidfResults.length} hasil ditemukan
                  </p>
                </div>

                <div className="p-6 space-y-3 max-h-[600px] overflow-y-auto custom-scrollbar">
                  {tfidfResults.length === 0 ? (
                    <p className="text-slate-500 text-center py-12 font-medium">
                      Tidak ada hasil ditemukan
                    </p>
                  ) : (
                    tfidfResults.slice(0, 5).map((result, index) => (
                      <div
                        key={index}
                        className="group relative bg-white/70 backdrop-blur-xl rounded-2xl p-5 border border-slate-200/50 hover:border-primary/30 hover:bg-white/90 hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 hover:-translate-y-1"
                      >
                        <div className="flex gap-4">
                          {result.main_image && (
                            <div className="relative flex-shrink-0 overflow-hidden rounded-xl">
                              <img
                                src={`http://localhost:5000/api/image-proxy?url=${encodeURIComponent(
                                  result.main_image
                                )}`}
                                alt={result.title}
                                className="w-28 h-28 object-cover bg-slate-100 transition-transform duration-500 group-hover:scale-105"
                                onError={(e) => {
                                  e.target.src =
                                    'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="112" height="112"><rect width="112" height="112" fill="%23f1f5f9"/><text x="56" y="56" text-anchor="middle" dy=".3em" fill="%2394a3b8" font-family="system-ui" font-size="11">No Image</text></svg>';
                                }}
                              />
                              <div className="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                            </div>
                          )}
                          <div className="flex-1 min-w-0">
                            <div className="flex items-start justify-between gap-3 mb-3">
                              <h4 className="font-semibold text-slate-900 line-clamp-2 text-base leading-snug group-hover:text-primary transition-colors duration-300">
                                {result.title}
                              </h4>
                              <span className="flex-shrink-0 px-2.5 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-lg border border-slate-200">
                                #{index + 1}
                              </span>
                            </div>
                            <p className="text-sm text-slate-600 line-clamp-2 mb-3 leading-relaxed">
                              {result.content}
                            </p>
                            <div className="flex items-center justify-between text-xs mb-2">
                              <span className="text-slate-600 font-medium bg-slate-100 px-2 py-1 rounded">
                                {result.source}
                              </span>
                              <span className="text-primary font-bold bg-primary/10 px-2 py-1 rounded">
                                {result.score?.toFixed(4) || "N/A"}
                              </span>
                            </div>
                            {result.url && (
                              <a
                                href={result.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1 text-xs text-primary hover:text-accent font-semibold mt-1 group/link"
                              >
                                <span>Baca selengkapnya</span>
                                <svg
                                  className="w-3 h-3 transition-transform duration-300 group-hover/link:translate-x-1"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M9 5l7 7-7 7"
                                  />
                                </svg>
                              </a>
                            )}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* BM25 Results */}
              <div className="bg-white/60 backdrop-blur-2xl rounded-3xl shadow-xl border border-slate-200/30 overflow-hidden transition-all duration-500 hover:shadow-2xl hover:border-accent/20">
                <div className="bg-slate-800/90 backdrop-blur-md px-8 py-6 border-b border-slate-700/50">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-2 h-2 bg-accent rounded-full"></div>
                    <h3 className="text-2xl font-bold text-white tracking-tight">
                      BM25 Algorithm
                    </h3>
                  </div>
                  <p className="text-sm text-slate-300 font-medium">
                    {bm25Results.length} hasil ditemukan
                  </p>
                </div>

                <div className="p-6 space-y-3 max-h-[600px] overflow-y-auto custom-scrollbar">
                  {bm25Results.length === 0 ? (
                    <p className="text-slate-500 text-center py-12 font-medium">
                      Tidak ada hasil ditemukan
                    </p>
                  ) : (
                    bm25Results.slice(0, 5).map((result, index) => (
                      <div
                        key={index}
                        className="group relative bg-white/70 backdrop-blur-xl rounded-2xl p-5 border border-slate-200/50 hover:border-accent/30 hover:bg-white/90 hover:shadow-xl hover:shadow-accent/10 transition-all duration-300 hover:-translate-y-1"
                      >
                        <div className="flex gap-4">
                          {result.main_image && (
                            <div className="relative flex-shrink-0 overflow-hidden rounded-xl">
                              <img
                                src={`http://localhost:5000/api/image-proxy?url=${encodeURIComponent(
                                  result.main_image
                                )}`}
                                alt={result.title}
                                className="w-28 h-28 object-cover bg-slate-100 transition-transform duration-500 group-hover:scale-105"
                                onError={(e) => {
                                  e.target.src =
                                    'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="112" height="112"><rect width="112" height="112" fill="%23f1f5f9"/><text x="56" y="56" text-anchor="middle" dy=".3em" fill="%2394a3b8" font-family="system-ui" font-size="11">No Image</text></svg>';
                                }}
                              />
                              <div className="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                            </div>
                          )}
                          <div className="flex-1 min-w-0">
                            <div className="flex items-start justify-between gap-3 mb-3">
                              <h4 className="font-semibold text-slate-900 line-clamp-2 text-base leading-snug group-hover:text-accent transition-colors duration-300">
                                {result.title}
                              </h4>
                              <span className="flex-shrink-0 px-2.5 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-lg border border-slate-200">
                                #{index + 1}
                              </span>
                            </div>
                            <p className="text-sm text-slate-600 line-clamp-2 mb-3 leading-relaxed">
                              {result.content}
                            </p>
                            <div className="flex items-center justify-between text-xs mb-2">
                              <span className="text-slate-600 font-medium bg-slate-100 px-2 py-1 rounded">
                                {result.source}
                              </span>
                              <span className="text-accent font-bold bg-accent/10 px-2 py-1 rounded">
                                {result.score?.toFixed(4) || "N/A"}
                              </span>
                            </div>
                            {result.url && (
                              <a
                                href={result.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1 text-xs text-accent hover:text-primary font-semibold mt-1 group/link"
                              >
                                <span>Baca selengkapnya</span>
                                <svg
                                  className="w-3 h-3 transition-transform duration-300 group-hover/link:translate-x-1"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M9 5l7 7-7 7"
                                  />
                                </svg>
                              </a>
                            )}
                          </div>
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
                className="group px-8 py-3 bg-gradient-to-r from-primary to-accent text-white font-semibold rounded-xl hover:shadow-2xl hover:shadow-primary/40 transition-all duration-300 transform hover:scale-105 flex items-center gap-2"
              >
                <svg
                  className="w-5 h-5 group-hover:rotate-12 transition-transform duration-300"
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
