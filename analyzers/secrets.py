import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext

def check_secrets_smart(project):
    results = []
    patterns = {
        "API Key": re.compile(r"(api[_-]?key|apikey)\s*[:=]\s*['\"][^'\"]{10,}['\"]", re.IGNORECASE),
        "Secret": re.compile(r"secret\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.IGNORECASE),
        "Password": re.compile(r"password\s*[:=]\s*['\"][^'\"]{4,}['\"]", re.IGNORECASE),
        "Token": re.compile(r"token\s*[:=]\s*['\"][^'\"]{20,}['\"]", re.IGNORECASE),
    }
    files = get_files_by_ext(project, [".py", ".js", ".jsx", ".ts", ".tsx", ".php"])
    found = False
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            rel = f.relative_to(project)
            for num, line in enumerate(text.splitlines(), 1):
                low = line.lower()
                if "process.env" in line or "os.environ" in line or "os.getenv" in line or "getenv" in line:
                    continue
                if "example" in low or "placeholder" in low or "dummy" in low:
                    continue
                if "req." in low or "jwt." in low or "header" in low or "authorization" in low or "bearer" in low or "split(" in low:
                    continue
                if "token" in low and ("sign" in low or "verify" in low or "decode" in low):
                    continue
                for label, pattern in patterns.items():
                    if pattern.search(line):
                        results.append(f"  [FAIL] {label} found: {rel}:{num} - Move to environment variables")
                        found = True
                        break
        except:
            pass
    key_files = list(Path(project).rglob("gsc-key.json")) + list(Path(project).rglob("*.pem")) + list(Path(project).rglob("*_key.json"))
    for kf in key_files:
        results.append(f"  [WARN] Sensitive key file found: {kf.relative_to(project)} - Ensure it is in .gitignore")
    if not found and not key_files:
        results.append("  [PASS] No hardcoded secrets found.")
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_secrets_smart(Path(path)):
        print(line)