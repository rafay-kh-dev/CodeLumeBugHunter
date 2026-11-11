import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext, safe_read

def check_secrets_smart(project):
    results = []
    code_files = get_files_by_ext(project, [".js", ".jsx", ".ts", ".tsx", ".py", ".php", ".json"])
    sensitive_names = ["gsc-key", "service-account", "credentials", "private-key", ".pem", "id_rsa"]
    for f in code_files:
        try:
            name_lower = f.name.lower()
            if any(s in name_lower for s in sensitive_names):
                if "package" not in name_lower and "tsconfig" not in name_lower:
                    rel = f.relative_to(project)
                    results.append(f"  [WARN] Sensitive key file found: {rel} - Ensure it is in .gitignore")
        except:
            pass
    secret_pattern = re.compile(r"(api[_-]?key|secret|password|passwd|pwd|token)\s*[:=]\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
    skip_words = ["token expired", "invalid token", "no token", "token required", "token missing", "token invalid", "unauthorized", "login successful"]
    for f in code_files:
        try:
            if f.suffix == ".json" and f.name in ["package.json", "package-lock.json", "tsconfig.json"]:
                continue
            text = safe_read(f)
            lines = text.splitlines()
            for idx, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("/*") or stripped.startswith("*"):
                    continue
                lower_line = line.lower()
                if "process.env" in lower_line or "os.getenv" in lower_line or "os.environ" in lower_line or "getenv" in lower_line:
                    continue
                if "req.headers" in lower_line or "authorization" in lower_line and "token:" not in lower_line:
                    continue
                if "jwt.sign" in lower_line or "jwt.verify" in lower_line or "jsonwebtoken" in lower_line:
                    continue
                match = secret_pattern.search(line)
                if match:
                    value = match.group(2)
                    value_lower = value.lower()
                    if " " in value:
                        continue
                    if any(w in value_lower for w in skip_words):
                        continue
                    if value_lower in ["your-token", "your_api_key", "example", "test", "dummy", "xxx", "todo", "changeme", "placeholder", "token", "secret", "password"]:
                        continue
                    if value.startswith("your-") or value.startswith("example") or value.startswith("test-"):
                        continue
                    if len(value) < 16:
                        continue
                    if value_lower in ["undefined", "null", "true", "false"]:
                        continue
                    rel = f.relative_to(project)
                    results.append(f"  [FAIL] Hardcoded token found: {rel}:{idx} - Move to JWT, do not hardcode admin token")
        except:
            pass
    if not any("[FAIL]" in r or "[WARN]" in r for r in results):
        results.append("  [PASS] No hardcoded secrets found.")
    return results

check_secrets_universal = check_secrets_smart

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_secrets_smart(Path(path)):
        print(line)