// @ts-nocheck
import { useState } from "react";
import { Copy, Download, Search } from "lucide-react";
export default function ResultSection(props) {
  const [q, setQ] = useState("");
  const [filter, setFilter] = useState("all");
  const tabs = ["overview", "issues", "report"];
  function filteredReport() {
    let r = props.report || "";
    if (filter !== "all")
      r = r
        .split("\n")
        .filter(function (l) {
          return (
            l.toLowerCase().includes(filter) ||
            l.startsWith("#") ||
            l.startsWith("|")
          );
        })
        .join("\n");
    if (q)
      r = r
        .split("\n")
        .filter(function (l) {
          return l.toLowerCase().includes(q.toLowerCase());
        })
        .join("\n");
    return r || "Kuch nahi mila. Filter change karo.";
  }
  function download() {
    const blob = new Blob([props.report], { type: "text/markdown" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "codelume-report.md";
    a.click();
  }
  function copyReport() {
    navigator.clipboard.writeText(props.report);
  }
  return (
    <div>
      <div className="flex flex-wrap gap-2 mt-5">
        {tabs.map(function (t) {
          const active = props.tab === t;
          const tabClass = active ? "capsule-active" : "capsule";
          const label =
            t === "issues"
              ? "Issues Found"
              : t === "report"
                ? "Full Report"
                : "Overview";
          return (
            <button
              key={t}
              onClick={function () {
                props.onTab(t);
              }}
              className={
                "px-5 py-2.5 rounded-full font-bold capitalize text-sm " +
                tabClass
              }
            >
              {label}
            </button>
          );
        })}
      </div>
      <div className="card mt-3 min-h-96">
        {props.tab === "overview" && (
          <div>
            <div className="label-spaced">Result Summary</div>
            <h3 className="font-extrabold text-2xl font-display mt-2">
              Bespoke digital solutions to scale your business.
            </h3>
            <p className="text-slate-500 mt-2">
              Tumhara score aur kya fix karna hai, sab ek jagah.
            </p>
            <div className="grid grid-cols-3 gap-3 mt-6">
              <div className="bg-[#F5F5F0] rounded-2xl p-4 text-center">
                <div className="font-black text-lg font-display">Pass</div>
                <div className="text-xs font-bold text-slate-500 mt-1">
                  PASSED
                </div>
              </div>
              <div className="bg-[#F5F5F0] rounded-2xl p-4 text-center">
                <div className="font-black text-lg font-display">Warn</div>
                <div className="text-xs font-bold text-slate-500 mt-1">
                  WARNING
                </div>
              </div>
              <div className="bg-[#F5F5F0] rounded-2xl p-4 text-center">
                <div className="font-black text-lg font-display">Fail</div>
                <div className="text-xs font-bold text-slate-500 mt-1">
                  FAILED
                </div>
              </div>
            </div>
            <p className="text-sm text-slate-400 mt-6">
              Scan ke baad yahan pura summary aayega. Abhi Start Scan dabao.
            </p>
          </div>
        )}
        {props.tab !== "overview" && (
          <div>
            <div className="flex flex-wrap gap-2 mb-4">
              <div className="flex items-center gap-2 bg-[#F5F5F0] rounded-full px-3 py-2 flex-1 min-w-48">
                <Search size={16} />
                <input
                  value={q}
                  onChange={function (e) {
                    setQ(e.target.value);
                  }}
                  placeholder="Report me search karo..."
                  className="bg-transparent outline-none text-sm w-full"
                />
              </div>
              <button
                onClick={function () {
                  setFilter("all");
                }}
                className="tool-btn"
              >
                All
              </button>
              <button
                onClick={function () {
                  setFilter("fail");
                }}
                className="tool-btn"
              >
                Fail
              </button>
              <button
                onClick={function () {
                  setFilter("warn");
                }}
                className="tool-btn"
              >
                Warn
              </button>
              <button
                onClick={copyReport}
                className="tool-btn flex items-center gap-1"
              >
                <Copy size={14} /> Copy
              </button>
              <button
                onClick={download}
                className="tool-btn flex items-center gap-1 bg-black text-white border-black"
              >
                <Download size={14} /> Export .md
              </button>
            </div>
            <pre className="whitespace-pre-wrap text-sm leading-relaxed">
              {props.report
                ? filteredReport().slice(0, 9000)
                : "Abhi koi report nahi hai. Pehle scan karo."}
            </pre>
          </div>
        )}
      </div>
      <p className="text-center text-xs text-slate-400 mt-6">
        4.9 Rating • 40+ Projects • 24h Reply • Engineered by Rafay
      </p>
    </div>
  );
}
