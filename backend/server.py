import os
import sys
import json
import threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import main as run_scan

scan_status = {"running": False, "log": [], "report": None}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return
    def send_json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/status":
            return self.send_json(scan_status)
        if path == "/api/report":
            return self.send_json({"report": scan_status.get("report") or "No report yet"})
        if path == "/" or path == "/index.html":
            f = Path("frontend/dist/index.html")
            if f.exists():
                data = f.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            return self.send_json({"ok": True, "msg": "Backend running. Run frontend dev server."})
        return self.send_json({"error": "Not found"}, 404)
    def do_POST(self):
        if urlparse(self.path).path != "/api/scan":
            return self.send_json({"error": "Not found"}, 404)
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length).decode() or "{}")
        project = data.get("project", "")
        categories = data.get("categories", [])
        if not project or not Path(project).exists():
            return self.send_json({"error": "Select a valid project folder"}, 400)
        if scan_status["running"]:
            return self.send_json({"error": "Scan already running"}, 400)
        scan_status["running"] = True
        scan_status["report"] = None
        only = ",".join(categories) if categories else None
        def do_scan():
            try:
                run_scan(project, only=only)
                reports = sorted(Path(".").glob("codelume-report-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
                if reports:
                    scan_status["report"] = reports[0].read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                scan_status["log"].append(str(e))
            finally:
                scan_status["running"] = False
        threading.Thread(target=do_scan, daemon=True).start()
        return self.send_json({"ok": True})

if __name__ == "__main__":
    print("CodeLume Backend running on http://127.0.0.1:5000")
    HTTPServer(("127.0.0.1", 5000), Handler).serve_forever()