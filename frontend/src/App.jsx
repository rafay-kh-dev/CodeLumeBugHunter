import { useState } from "react";

export default function App() {
  const [project, setProject] = useState("");
  const [cats, setCats] = useState([]);
  const [score, setScore] = useState("--");
  const [report, setReport] = useState("");
  const [status, setStatus] = useState(
    "Ready - Select a folder and press Start Scan",
  );
  const [tab, setTab] = useState("overview");

  const categories = [
    "Frontend",
    "Backend",
    "Security",
    "Performance",
    "Architecture",
    "Python",
    "PHP",
    "Quality",
  ];

  const toggleCat = (c) => {
    setCats((prev) =>
      prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c],
    );
  };

  const startScan = async () => {
    if (!project) {
      alert("Please select project folder path first");
      return;
    }
    setStatus("Scanning... Please wait, everything is happening here.");
    await fetch("/api/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project, categories: cats }),
    });
    const check = setInterval(async () => {
      const r = await fetch("/api/status").then((res) => res.json());
      if (!r.running) {
        clearInterval(check);
        setStatus("Done! Check Issues and Report tabs.");
        const rep = await fetch("/api/report").then((res) => res.json());
        setReport(rep.report);
        const m = rep.report.match(/\*\*Score:\*\* (\d+)/);
        if (m) setScore(m[1]);
        setTab("issues");
      }
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-indigo-600 text-white font-bold text-xl flex items-center justify-center rounded-lg">
            C
          </div>
          <div className="text-2xl font-bold">
            CodeLume{" "}
            <span className="text-indigo-600 font-normal">Bug Hunter</span>
          </div>
        </div>
        <span className="bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-xs font-bold">
          PREMIUM • v1.0
        </span>
      </header>
      <div className="flex max-w-7xl mx-auto p-5 gap-5">
        <aside className="w- bg-white rounded-2xl p-5 h-fit shadow-sm">
          <h2 className="font-bold text-lg">Your Project</h2>
          <p className="text-sm text-slate-500">
            Which folder do you want to check?
          </p>
          <input
            value={project}
            onChange={(e) => setProject(e.target.value)}
            placeholder="C:\MyProject"
            className="w-full mt-3 bg-slate-100 rounded-lg px-3 py-2.5 outline-none"
          />
          <p className="text-xs text-slate-400 mt-2">
            Paste your project folder path here
          </p>
          <h2 className="font-bold mt-6">What to check?</h2>
          <p className="text-sm text-slate-500">
            Leave empty = Check Everything
          </p>
          <div className="mt-3 space-y-2">
            {categories.map((c) => (
              <label key={c} className="flex gap-2 items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={cats.includes(c)}
                  onChange={() => toggleCat(c)}
                  className="w-4 h-4 accent-indigo-600"
                />
                <span>{c}</span>
              </label>
            ))}
          </div>
          <button
            onClick={startScan}
            className="w-full mt-6 bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-3.5 rounded-xl"
          >
            Start Scan
          </button>
        </aside>
        <main className="flex-1">
          <div className="grid grid-cols-4 gap-3">
            <div className="bg-white rounded-2xl p-4 text-center shadow-sm">
              <div className="text-xs font-bold text-slate-400">SCORE</div>
              <div className="text-3xl font-bold text-indigo-600">{score}</div>
            </div>
            <div className="bg-white rounded-2xl p-4 text-center shadow-sm">
              <div className="text-xs font-bold text-slate-400">STATUS</div>
              <div className="text-sm mt-2">{status}</div>
            </div>
            <div className="bg-white rounded-2xl p-4 text-center shadow-sm col-span-2">
              <div className="text-xs font-bold text-slate-400">RESULT</div>
              <div className="text-sm mt-2">
                {score === "--"
                  ? "Run a scan to see your project health"
                  : `Your Score: ${score} / 100`}
              </div>
            </div>
          </div>
          <div className="flex gap-2 mt-5">
            {["overview", "issues", "report"].map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-4 py-2 rounded-full font-bold capitalize ${tab === t ? "bg-indigo-600 text-white" : "bg-white"}`}
              >
                {t === "issues"
                  ? "Issues Found"
                  : t === "report"
                    ? "Full Report"
                    : "Overview"}
              </button>
            ))}
          </div>
          <div className="bg-white rounded-2xl p-5 mt-3 shadow-sm min-h-">
            {tab === "overview" && (
              <div>
                <h3 className="font-bold text-lg">Result Summary</h3>
                <p className="text-slate-500 mt-2">
                  Your score and what needs fixing - all in one place.
                </p>
                <div className="text-4xl font-bold mt-4">{score} / 100</div>
              </div>
            )}
            {tab === "issues" && (
              <pre className="whitespace-pre-wrap text-sm">
                {report
                  ? report.slice(0, 8000)
                  : "No report yet. Run a scan first."}
              </pre>
            )}
            {tab === "report" && (
              <pre className="whitespace-pre-wrap text-xs">
                {report || "No report yet."}
              </pre>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
