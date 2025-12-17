import { useState } from "react";
import { useNavigate } from "react-router-dom";
import TextType from "../components/TextType";

function LandingPage() {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

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
      navigate(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  const handlePopularSearch = (term) => {
    setQuery(term);
    navigate(`/search?q=${encodeURIComponent(term)}`);
  };

  return (
    <>
      <style>
        {`
          @keyframes bounce3D {
            0%, 100% {
              transform: translateY(0) translateZ(0) rotateX(0deg) rotateY(0deg) scale(1);
            }
            40% {
              transform: translateY(-30px) translateZ(40px) rotateX(-8deg) rotateY(5deg) scale(0.85);
            }
            50% {
              transform: translateY(-35px) translateZ(45px) rotateX(-10deg) rotateY(6deg) scale(0.8);
            }
            60% {
              transform: translateY(-30px) translateZ(40px) rotateX(-8deg) rotateY(5deg) scale(0.85);
            }
          }
        `}
      </style>
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
          <img
            src="image/nubofind.png"
            alt="Find Logo"
            className="h-12 w-auto"
          />
        </div>

        <div className="relative z-10 w-full max-w-4xl px-6 py-12 min-h-screen flex flex-col">
          {/* Content Area - Centered */}
          <div className="flex-1 flex flex-col justify-center">
            {/* Header */}
            <header className="text-center mb-12 animate-fadeIn">
              <h1
                className="text-7xl md:text-6xl font-serif font-bold text-slate-900 mb-4"
                style={{ fontFamily: "'Playfair Display', Georgia, serif" }}
              >
                <TextType
                  text={["Indonesian Football", "Search", "With NuboFind"]}
                  typingSpeed={75}
                  pauseDuration={1500}
                  showCursor={true}
                  cursorCharacter="|"
                />
              </h1>
              <p
                className="text-lg md:text-xl text-slate-800 max-w-2xl mx-auto leading-relaxed font-medium"
                style={{ fontFamily: "'Inter', 'Segoe UI', sans-serif" }}
              >
                Temukan semua informasi sepak bola yang Anda butuhkan. Jelajahi
                artikel mendalam, wawasan pertandingan, pembaruan pemain, dan
                sorotan tim semuanya di ujung jari Anda.
              </p>
            </header>

            {/* Search Section */}
            <section className="mb-8 animate-fadeInUp">
              <form onSubmit={handleSearch} className="mb-6">
                <div className="relative group">
                  <svg
                    className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-600 group-hover:text-primary pointer-events-none z-10 transition-colors duration-300"
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
                    className="w-full pl-12 pr-20 py-3.5 text-base bg-white/75 backdrop-blur-md border-2 border-slate-300 rounded-full text-slate-900 placeholder-slate-600 focus:outline-none focus:border-primary focus:shadow-lg focus:shadow-primary/20 hover:border-slate-400 transition-all duration-300"
                    placeholder="Cari pemain, tim, atau berita sepak bola..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                  />
                  <button
                    type="submit"
                    className="absolute right-3 top-1/2 -translate-y-1/2 bg-gradient-to-r from-primary to-primary/90 text-white px-5 py-2.5 rounded-full hover:from-primary hover:to-accent hover:shadow-md hover:shadow-primary/30 transition-all duration-300 flex items-center gap-1.5 font-medium text-sm"
                  >
                    <svg
                      className="w-4 h-4"
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
              <div className="flex items-center justify-center gap-2">
                <span className="text-slate-700 text-xs font-semibold whitespace-nowrap">
                  Pencarian populer:
                </span>
                {popularSearches.map((term) => (
                  <button
                    key={term}
                    type="button"
                    onClick={() => handlePopularSearch(term)}
                    className="px-3 py-1.5 bg-white/80 backdrop-blur-md border border-slate-300 text-slate-900 text-xs font-medium rounded-xl hover:bg-white hover:border-primary hover:shadow-lg hover:shadow-primary/30 transition-all duration-300 transform hover:-translate-y-0.5 whitespace-nowrap"
                  >
                    {term}
                  </button>
                ))}
              </div>
            </section>
          </div>

          {/* Footer - Pushed to Bottom */}
          <footer className="text-center text-slate-700 text-sm pb-8 animate-fadeIn">
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="h-px w-16 bg-gradient-to-r from-transparent to-slate-400"></div>
              <span className="text-xs font-semibold text-slate-700">
                NuboFind
              </span>
              <div className="h-px w-16 bg-gradient-to-l from-transparent to-slate-400"></div>
            </div>

            <p className="text-slate-700 font-medium mb-3">
              Copyright © 2025 | Indonesian Football Search Engine
            </p>

            {/* Team Names with Hover Cards */}
            <div className="flex items-center justify-center gap-2 mb-3">
              <span className="text-xs text-slate-600 font-semibold">
                Kelompok 14:
              </span>
              <div className="flex items-center gap-3">
                {[
                  {
                    name: "Muhammad Caesar Aidarus",
                    nim: "2308107010072",
                    img: "/image/caesar.jpg",
                  },
                  {
                    name: "Muhammad Syukri",
                    nim: "2308107010060",
                    img: "/image/syukri.jpg",
                  },
                ].map((member, index) => (
                  <div key={index} className="relative group inline-block">
                    {/* Name Link */}
                    <span className="relative text-xs text-slate-800 cursor-pointer font-semibold transition-all duration-300 inline-block group-hover:scale-105">
                      <span className="relative z-10 bg-gradient-to-r from-slate-800 to-slate-800 group-hover:from-primary group-hover:to-accent bg-clip-text group-hover:text-transparent transition-all duration-500">
                        {member.name}
                      </span>
                      <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-primary to-accent group-hover:w-full transition-all duration-500 ease-out"></span>
                    </span>

                    {/* Hover Card - Ball Shaped */}
                    <div
                      className="absolute bottom-full left-1/2 -translate-x-1/2 mb-6 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-500 ease-out pointer-events-none z-50"
                      style={{ perspective: "1000px" }}
                    >
                      {/* Outer ball border with real football texture */}
                      <div
                        className="relative w-[240px] h-[240px] rounded-full p-[6px] transition-all duration-700 ease-out"
                        style={{
                          backgroundImage: "url('/image/bola.jpg')",
                          backgroundSize: "cover",
                          backgroundPosition: "center",
                          boxShadow:
                            "0 20px 60px rgba(0, 0, 0, 0.3), 0 0 40px rgba(16, 185, 129, 0.2)",
                          transform:
                            "translateY(0) translateZ(0) rotateX(0deg) rotateY(0deg) scale(1)",
                          animation: "bounce3D 2.5s ease-in-out infinite",
                        }}
                      >
                        {/* Inner card content */}
                        <div className="relative w-full h-full backdrop-blur rounded-full shadow-2xl transform group-hover:translate-y-0 translate-y-3 group-hover:scale-100 scale-95 transition-all duration-500 ease-out overflow-hidden flex flex-col items-center justify-center p-6">
                          {/* Animated gradient background */}
                          <div className="absolute inset-0 rounded-full bg-gradient-to-br from-primary/5 via-accent/5 to-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>

                          {/* Glow effect */}
                          <div
                            className="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                            style={{
                              boxShadow:
                                "inset 0 0 40px rgba(16, 185, 129, 0.1)",
                            }}
                          ></div>

                          {/* Photo - Circular */}
                          <div className="relative w-28 h-28 mx-auto mb-4 overflow-hidden rounded-full bg-gradient-to-br from-primary/20 to-accent/20 ring-4 ring-white/50 group-hover:ring-primary/30 transition-all duration-500">
                            <img
                              src={member.img}
                              alt={member.name}
                              className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700 ease-out"
                              onError={(e) => {
                                e.target.src =
                                  'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="112" height="112"><rect width="112" height="112" fill="%23f1f5f9"/><text x="56" y="56" text-anchor="middle" dy=".3em" fill="%2310b981" font-family="system-ui" font-size="40" font-weight="bold">' +
                                  member.name.charAt(0) +
                                  "</text></svg>";
                              }}
                            />
                            {/* Shimmer overlay on hover */}
                            <div
                              className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent opacity-0 group-hover:opacity-100 group-hover:animate-shimmer rounded-full"
                              style={{ backgroundSize: "200% 100%" }}
                            ></div>
                          </div>

                          {/* Info - Centered in circle */}
                          <div className="text-center relative z-10 max-w-[180px]">
                            <h4 className="font-bold text-slate-900 text-sm mb-2 leading-tight transform group-hover:translate-y-0 translate-y-1 opacity-0 group-hover:opacity-100 transition-all duration-500 delay-100">
                              {member.name}
                            </h4>
                            <p className="text-xs text-slate-700 font-medium mb-3 transform group-hover:translate-y-0 translate-y-1 opacity-0 group-hover:opacity-100 transition-all duration-500 delay-150">
                              NIM: {member.nim}
                            </p>
                            <span className="inline-block px-3 py-1.5 bg-gradient-to-r from-primary/20 to-accent/20 text-primary text-xs rounded-full font-semibold transform group-hover:translate-y-0 translate-y-1 opacity-0 group-hover:opacity-100 transition-all duration-500 delay-200 group-hover:shadow-md border border-primary/30">
                              Kelompok 14
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </footer>
        </div>
      </div>
    </>
  );
}

export default LandingPage;
