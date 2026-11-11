// @ts-nocheck
import { FolderOpen } from "lucide-react";
export default function ProjectPicker(props) {
  return (
    <div>
      <div className="label-spaced">01 - Project</div>
      <h2 className="font-extrabold text-lg flex items-center gap-2 font-display mt-2">
        <FolderOpen size={20} /> Select Project
      </h2>
      <p className="text-sm text-slate-500 mt-1">
        Konsa folder check karna hai?
      </p>
      <input
        value={props.project}
        onChange={function (e) {
          props.onChange(e.target.value);
        }}
        placeholder="C:\MyProject"
        className="input-box"
      />
      {props.recent.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-3">
          {props.recent.map(function (r) {
            return (
              <button
                key={r}
                onClick={function () {
                  props.onChange(r);
                }}
                className="chip"
              >
                {r}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
