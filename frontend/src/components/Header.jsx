// @ts-nocheck
export default function Header() {
  return (
    <header className="site-header px-6 py-5">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-black text-white font-black text-xl flex items-center justify-center rounded-full">
            C
          </div>
          <div>
            <div className="text-xl font-extrabold leading-none font-display">
              CodeLume
            </div>
            <div className="label-spaced mt-1">Bug Hunter</div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="hidden md:block text-xs font-semibold text-slate-500">
            4.9 Rating • 40+ Projects
          </span>
          <span className="bg-black text-white px-4 py-1.5 rounded-full text-xs font-bold">
            PREMIUM v1.0
          </span>
        </div>
      </div>
    </header>
  );
}
