import { useState } from "react";
import "./App.css";
import TextType from "./components/TextType";

function App() {
  const [query, setQuery] = useState("");

  const popularSearches = [
    "Timnas Indonesia",
    "Persib Bandung",
    "Liga Champions",
    "Piala Dunia",
    "Transfer Pemain",
  ];

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      console.log("Searching for:", query);
      // TODO: Navigate to search results page
    }
  };

  const handlePopularSearch = (term) => {
    setQuery(term);
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-100">
      {/* Background with light overlay */}
      <div
        className="absolute inset-0 bg-cover bg-center z-0"
        style={{
          backgroundImage: "url(/image/frontend-bg.jpg)",
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-b from-white/40 via-white/45 to-white/40" />
      </div>

      {/* Logo */}
      <div className="absolute top-8 left-8 z-20">
        <img src="image/nubofind.png" alt="Find Logo" className="h-12 w-auto" />
      </div>

      <div className="relative z-10 w-full max-w-4xl px-6 py-12">
        {/* Header */}
        <header className="text-center mb-12 animate-fadeIn">
          <h1 className="text-7xl md:text-6xl font-bold text-slate-800 mb-4">
            <TextType
              text={["Indonesian Football", "Search", "With NuboFind"]}
              typingSpeed={75}
              pauseDuration={1500}
              showCursor={true}
              cursorCharacter="|"
            />
          </h1>
          <p className="text-lg md:text-xl text-slate-700 max-w-2xl mx-auto leading-relaxed">
            Temukan semua informasi sepak bola yang Anda butuhkan. Jelajahi
            artikel mendalam, wawasan pertandingan, pembaruan pemain, dan
            sorotan tim — semuanya di ujung jari Anda.
          </p>
        </header>

        {/* Search Section */}
        <section className="mb-8 animate-fadeInUp">
          <form onSubmit={handleSearch} className="mb-6">
            <div className="relative group">
              <svg
                className="absolute left-5 top-1/2 -translate-y-1/2 w-6 h-6 text-slate-500 pointer-events-none z-10"
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
                className="w-full pl-16 pr-24 py-5 text-lg bg-white/80 backdrop-blur-lg border border-slate-300 rounded-2xl text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary/50 transition-all duration-300 shadow-xl"
                placeholder="Cari pemain, tim, atau berita sepak bola..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <button
                type="submit"
                className="absolute right-3 top-1/2 -translate-y-1/2 bg-gradient-to-r from-primary to-accent text-white px-6 py-3 rounded-xl hover:shadow-lg hover:shadow-primary/50 transition-all duration-300 flex items-center gap-2"
              >
                <svg
                  className="w-5 h-5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <circle cx="11" cy="11" r="8" />
                  <path d="M21 21l-4.35-4.35" />
                </svg>
              </button>
            </div>
          </form>

          {/* Popular Searches */}
          <div className="flex flex-wrap items-center justify-center gap-3">
            <span className="text-slate-600 text-sm font-medium">
              Pencarian populer:
            </span>
            {popularSearches.map((term) => (
              <button
                key={term}
                type="button"
                onClick={() => handlePopularSearch(term)}
                className="px-4 py-2 bg-white/70 backdrop-blur-md border border-slate-300 text-slate-800 text-sm rounded-lg hover:bg-white hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20 transition-all duration-300 transform hover:-translate-y-0.5"
              >
                {term}
              </button>
            ))}
          </div>
        </section>

        {/* Footer */}
        <footer className="text-center text-slate-600 text-sm mt-16 animate-fadeIn">
          <p>Copyright © 2024 | Football Search Engine</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
