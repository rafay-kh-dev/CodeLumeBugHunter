// @ts-nocheck
import { useState } from "react"
import { startScan, getStatus, getReport } from "../services/api"
export function useScan() {
  const [project, setProject] = useState("")
  const [cats, setCats] = useState([])
  const [score, setScore] = useState(null)
  const [report, setReport] = useState("")
  const [scanning, setScanning] = useState(false)
  const [step, setStep] = useState(0)
  const [tab, setTab] = useState("overview")
  const [recent, setRecent] = useState(function() {
    try { return JSON.parse(localStorage.getItem("codelume-recent") || "[]") } catch { return [] }
  })
  function toggleCat(c) {
    if (cats.includes(c)) setCats(cats.filter(function(x) { return x !== c }))
    else setCats(cats.concat(c))
  }
  async function start() {
    if (!project) { alert("Pehle project folder path likho"); return }
    const next = [project].concat(recent.filter(function(x) { return x !== project })).slice(0, 4)
    setRecent(next)
    localStorage.setItem("codelume-recent", JSON.stringify(next))
    setScanning(true)
    setStep(0)
    setTab("overview")
    setTimeout(function() { setStep(1) }, 900)
    setTimeout(function() { setStep(2) }, 1800)
    setTimeout(function() { setStep(3) }, 2700)
    await startScan({ project: project, categories: cats })
    const check = setInterval(async function() {
      const r = await getStatus()
      if (!r.running) {
        clearInterval(check)
        setScanning(false)
        const rep = await getReport()
        setReport(rep.report)
        const m = rep.report.match(/\*\*Score:\*\* (\d+)/)
        if (m) setScore(parseInt(m[1]))
        setTab("issues")
      }
    }, 1200)
  }
  return { project, setProject, cats, toggleCat, score, report, scanning, step, tab, setTab, recent, start }
}