// @ts-nocheck
import { getScoreMessage } from "../data/categories";
export default function ScoreCard(props) {
  const barWidth = props.score === null ? "0%" : props.score + "%";
  const barStyle = { width: barWidth };
  return (
    <div className="card">
      <div className="label-spaced">Your Score</div>
      <div className="text-5xl font-black font-display mt-3">
        {props.score === null ? "--" : props.score}
        <span className="text-lg text-slate-400 font-bold"> / 100</span>
      </div>
      <div className="progress-track">
        <div className="progress-fill" style={barStyle}></div>
      </div>
      <div className="text-sm text-slate-500 leading-snug mt-3">
        {getScoreMessage(props.score)}
      </div>
    </div>
  );
}
