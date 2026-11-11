// @ts-nocheck
import { Search, CheckCircle2, AlertTriangle, XCircle } from "lucide-react";
export default function LiveStatusCard(props) {
  return (
    <div className="card bg-black text-white border-black">
      <div className="label-spaced text-white/60">Live Status</div>
      <div className="flex items-center gap-2 font-bold font-display mt-3">
        <Search size={18} /> {props.scanning ? "Scanning..." : "Ready"}
      </div>
      <p className="text-white/70 text-sm mt-2 leading-relaxed">
        {props.scanning
          ? "Scan chal raha hai, sab yahin dikhega..."
          : "Ready ho? Project select karo aur Start Scan dabao."}
      </p>
      <div className="mt-4 flex gap-2">
        <span className="bg-white/10 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
          <CheckCircle2 size={13} /> Pass
        </span>
        <span className="bg-white/10 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
          <AlertTriangle size={13} /> Warn
        </span>
        <span className="bg-white/10 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
          <XCircle size={13} /> Fail
        </span>
      </div>
    </div>
  );
}
