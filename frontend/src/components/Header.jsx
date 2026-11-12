// @ts-nocheck
import { Search, Bell } from "lucide-react"
export default function Header(props) {
  return (
    <header className="sticky top-0 z-50 bg-white/85 backdrop-blur px-6 py-3 border-b border-neutral-100">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-1.5">
            <span className="text-2xl font-bold"><span className="text-green-500">&lt;</span><span className="text-amber-500">/</span><span className="text-blue-500">&gt;</span></span>
            <span className="text- font-bold tracking-tight">CodeLume <span className="font-medium text-neutral-500">Bug Hunter</span></span>
          </div>
          <nav className="hidden lg:flex gap-6 text- text-neutral-500 font-medium">
            <span className="text-black font-semibold cursor-pointer">Scanner</span>
            <span className="cursor-pointer hover:text-black">Reports</span>
            <span className="cursor-pointer hover:text-black">History</span>
            <span className="cursor-pointer hover:text-black">Docs</span>
          </nav>
        </div>
        <div className="flex items-center gap-2">
          <span className="hidden md:flex w-9 h-9 border rounded-full items-center justify-center"><Search size={16} /></span>
          <span className="hidden md:flex w-9 h-9 border rounded-full items-center justify-center"><Bell size={16} /></span>
          <span className="w-9 h-9 bg-black text-white rounded-full flex items-center justify-center text-sm font-bold">R</span>
          <button onClick={props.onStart} className="hidden sm:block bg-black text-white px-5 py-2.5 rounded-full text- font-medium">Start Scan</button>
        </div>
      </div>
    </header>
  )
}