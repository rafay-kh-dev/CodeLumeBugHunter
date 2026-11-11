// @ts-nocheck
import { Globe, Server, ShieldCheck, Zap, Layout, Code2, FileCode, Sparkles } from "lucide-react"
export const categories = [
  { name: "Frontend", icon: Globe, desc: "Design, Images, Speed" },
  { name: "Backend", icon: Server, desc: "Server, Database" },
  { name: "Security", icon: ShieldCheck, desc: "Secrets, Safety" },
  { name: "Performance", icon: Zap, desc: "Fast Loading" },
  { name: "Architecture", icon: Layout, desc: "Project Structure" },
  { name: "Python", icon: Code2, desc: "Python Checks" },
  { name: "PHP", icon: FileCode, desc: "PHP Checks" },
  { name: "Quality", icon: Sparkles, desc: "Clean Code" }
]
export function getScoreMessage(score) {
  if (score === null) return "Abhi tak scan nahi hua. Chalo shuru karte hain."
  if (score >= 80) return "Bespoke quality. Tumhara project to ekdum fit hai."
  if (score >= 50) return "Good start. Thodi si engineering baaki hai."
  return "Thoda kaam karna parega, par fikar nahi, sab bata dunga."
}