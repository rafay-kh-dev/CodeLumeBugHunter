// @ts-nocheck
/* eslint-disable */
import Header from "./components/Header";
import Hero from "./components/Hero";
import ProjectPicker from "./components/ProjectPicker";
import CategoryGrid from "./components/CategoryGrid";
import ScanControls from "./components/ScanControls";
import ScoreCard from "./components/ScoreCard";
import LiveStatusCard from "./components/LiveStatusCard";
import MethodCard from "./components/MethodCard";
import ResultSection from "./components/ResultSection";
import { useScan } from "./hooks/useScan";

export default function App() {
  const s = useScan();
  return (
    <div className="min-h-screen">
      <Header />
      <Hero />
      <div className="layout">
        <aside className="sidebar h-fit">
          <ProjectPicker
            project={s.project}
            onChange={s.setProject}
            recent={s.recent}
          />
          <CategoryGrid selected={s.cats} onToggle={s.toggleCat} />
          <ScanControls scanning={s.scanning} step={s.step} onStart={s.start} />
        </aside>
        <main className="flex-1">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <ScoreCard score={s.score} />
            <LiveStatusCard scanning={s.scanning} />
            <MethodCard />
          </div>
          <ResultSection tab={s.tab} onTab={s.setTab} report={s.report} />
        </main>
      </div>
    </div>
  );
}
