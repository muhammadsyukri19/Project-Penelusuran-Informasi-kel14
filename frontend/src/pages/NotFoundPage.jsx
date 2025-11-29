import { Link } from "react-router-dom";

function NotFoundPage() {
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-100">
      {/* Background with light overlay */}
      <div
        className="fixed inset-0 bg-cover bg-center z-0"
        style={{
          backgroundImage: "url(/image/frontend-bg.jpg)",
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-b from-white/40 via-white/45 to-white/40" />
      </div>

      {/* Logo */}
      <div className="absolute top-8 left-8 z-20">
        <Link to="/">
          <img
            src="/image/nubofind.png"
            alt="Find Logo"
            className="h-12 w-auto"
          />
        </Link>
      </div>

      {/* 404 Content */}
      <div className="relative z-10 text-center px-6 animate-fadeInUp">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-slate-800 mb-4">404</h1>
          <div className="w-32 h-1 bg-gradient-to-r from-primary to-accent mx-auto mb-6"></div>
        </div>

        <h2 className="text-3xl md:text-4xl font-bold text-slate-800 mb-4">
          Halaman Tidak Ditemukan
        </h2>

        <p className="text-lg text-slate-600 mb-8 max-w-md mx-auto">
          Maaf, halaman yang Anda cari tidak ditemukan atau telah dipindahkan.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
          <Link
            to="/"
            className="px-8 py-3 bg-gradient-to-r from-primary to-accent text-white font-semibold rounded-xl hover:shadow-xl hover:shadow-primary/50 transition-all duration-300 transform hover:-translate-y-1 flex items-center gap-2"
          >
            <svg
              className="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Kembali ke Beranda
          </Link>

          <button
            onClick={() => window.history.back()}
            className="px-8 py-3 bg-white/70 backdrop-blur-md border border-slate-300 text-slate-800 font-semibold rounded-xl hover:bg-white hover:shadow-lg transition-all duration-300 flex items-center gap-2"
          >
            <svg
              className="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Halaman Sebelumnya
          </button>
        </div>

        {/* Additional Help */}
        <div className="mt-12 p-6 bg-white/70 backdrop-blur-md rounded-2xl border border-slate-300 max-w-lg mx-auto">
          <h3 className="text-lg font-semibold text-slate-800 mb-3">
            Butuh Bantuan?
          </h3>
          <p className="text-sm text-slate-600 mb-4">
            Coba gunakan pencarian untuk menemukan informasi sepak bola yang
            Anda butuhkan:
          </p>
          <div className="flex gap-2">
            <Link
              to="/?q=Timnas%20Indonesia"
              className="px-4 py-2 bg-white border border-slate-300 text-slate-700 text-sm rounded-lg hover:bg-slate-50 transition-colors"
            >
              Timnas Indonesia
            </Link>
            <Link
              to="/?q=Liga%20Champions"
              className="px-4 py-2 bg-white border border-slate-300 text-slate-700 text-sm rounded-lg hover:bg-slate-50 transition-colors"
            >
              Liga Champions
            </Link>
            <Link
              to="/?q=Piala%20Dunia"
              className="px-4 py-2 bg-white border border-slate-300 text-slate-700 text-sm rounded-lg hover:bg-slate-50 transition-colors"
            >
              Piala Dunia
            </Link>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="absolute bottom-8 left-0 right-0 text-center text-slate-600 text-sm z-10">
        <p>Copyright © 2024 | Football Search Engine</p>
      </footer>
    </div>
  );
}

export default NotFoundPage;
