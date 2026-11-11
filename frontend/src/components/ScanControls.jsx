// @ts-nocheck
import { ArrowRight, CheckCircle2 } from "lucide-react";
export default function ScanControls(props) {
  const steps = [
    "Files parh raha hun...",
    "Stack pehchan raha hun...",
    "Bugs dhoond raha hun...",
    "Report bana raha hun...",
  ];
  return (
    <div>
      <button
        onClick={props.onStart}
        disabled={props.scanning}
        className="btn-black"
      >
        {props.scanning ? (
          "Checking... Ruko zara"
        ) : (
          <span className="flex items-center gap-2">
            Start Scan <ArrowRight size={18} />
          </span>
        )}
      </button>
      {props.scanning && (
        <div className="mt-4 space-y-2">
          {steps.map(function (t, i) {
            const done = i <= props.step;
            const rowClass = done ? "text-black font-medium" : "text-slate-300";
            return (
              <div
                key={t}
                className={"flex items-center gap-2 text-sm " + rowClass}
              >
                {done ? (
                  <CheckCircle2 size={16} />
                ) : (
                  <div className="w-4 h-4 rounded-full border-2 border-slate-200" />
                )}
                {t}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
