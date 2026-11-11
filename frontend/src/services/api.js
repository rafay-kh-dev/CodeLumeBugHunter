// @ts-nocheck
export async function startScan(payload) {
  return fetch("/api/scan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
}
export async function getStatus() {
  const r = await fetch("/api/status")
  return r.json()
}
export async function getReport() {
  const r = await fetch("/api/report")
  return r.json()
}