function LoadingScreen({
  message = "Memuat Data",
  subtitle = "Mohon tunggu sebentar...",
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-primary/10 via-slate-100 to-accent/10 animate-fadeIn">
      <div className="text-center space-y-8">
        {/* Logo / Icon Area */}
        <div className="relative flex justify-center">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-32 h-32 bg-gradient-to-br from-primary/20 to-accent/20 rounded-full animate-pulse"></div>
          </div>
          <div className="relative">
            <img
              src="/image/nubofind.png"
              alt="Loading"
              className="w-68 h-40 object-contain drop-shadow-xl animate-float"
            />
          </div>
        </div>

        {/* Spinner */}
        <div className="flex justify-center">
          <div className="relative">
            <div className="w-20 h-20 border-4 border-slate-200 rounded-full"></div>
            <div className="absolute inset-0 w-20 h-20 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
          </div>
        </div>

        {/* Text */}
        <div className="space-y-3">
          <h3 className="text-3xl font-bold text-slate-900 animate-pulse">
            {message}
          </h3>
          <p className="text-lg text-slate-600 font-medium">{subtitle}</p>
        </div>

        {/* Progress Dots */}
        <div className="flex justify-center gap-2">
          <div
            className="w-3 h-3 bg-primary rounded-full animate-bounce"
            style={{ animationDelay: "0ms" }}
          ></div>
          <div
            className="w-3 h-3 bg-primary rounded-full animate-bounce"
            style={{ animationDelay: "150ms" }}
          ></div>
          <div
            className="w-3 h-3 bg-primary rounded-full animate-bounce"
            style={{ animationDelay: "300ms" }}
          ></div>
        </div>
      </div>
    </div>
  );
}

export default LoadingScreen;
