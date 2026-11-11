// @ts-nocheck
import { categories } from "../data/categories";
export default function CategoryGrid(props) {
  return (
    <div>
      <div className="label-spaced mt-6">02 - Scope</div>
      <h2 className="font-extrabold text-lg mt-2 font-display">
        What to check?
      </h2>
      <p className="text-sm text-slate-500">
        Capsule pe click karo, khali chhoro to sab check kar dunga
      </p>
      <div className="cat-grid">
        {categories.map(function (c) {
          const Icon = c.icon;
          const on = props.selected.includes(c.name);
          const btnClass = on ? "bg-black text-white border-black" : "bg-white";
          const descClass = on ? "text-white/70" : "text-slate-400";
          const iconClass = on ? "text-white" : "text-black";
          return (
            <button
              key={c.name}
              onClick={function () {
                props.onToggle(c.name);
              }}
              className={"cat-btn " + btnClass}
            >
              <Icon size={22} className={iconClass} />
              <div className="font-bold text-sm mt-2.5">{c.name}</div>
              <div className={"text-xs " + descClass}>{c.desc}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
