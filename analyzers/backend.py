import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext, safe_read

def check_backend_smart(project):
    results = []
    backend_files = get_files_by_ext(project, [".js", ".py", ".php", ".json"])
    all_text = ""
    for f in backend_files:
        try:
            all_text += safe_read(f) + "\n"
        except:
            pass
    lower_text = all_text.lower()
    if "jsonwebtoken" in lower_text or "jwt" in lower_text or "jwt_secret" in lower_text:
        results.append("  [PASS] JWT: In use")
    else:
        results.append("  [INFO] JWT: Not found")
    if "cors" in lower_text:
        results.append("  CORS: [PASS] Found")
    else:
        results.append("  CORS: [WARN] Not found - Add CORS if frontend is separate")
    if "mongoose" in lower_text or "mongodb" in lower_text or "mongoclient" in lower_text:
        results.append("  MongoDB: [PASS] Found")
    else:
        results.append("  MongoDB: [INFO] Not found")
    sql_files = get_files_by_ext(project, [".sql"])
    if sql_files:
        results.append(f"  SQL: [INFO] {len(sql_files)} .sql files found")
    else:
        results.append("  SQL: [INFO] No .sql files, MongoDB may be in use")
    if "process.env.port" in lower_text or "os.getenv" in lower_text or "process.env['port']" in lower_text:
        results.append("  [PASS] PORT: Loaded from environment variables")
    else:
        results.append("  [WARN] PORT: Hardcoded - Use environment variables")
    env_files = list(project.rglob(".env")) + list(project.rglob(".env.example"))
    env_files = [f for f in env_files if ".git" not in str(f) and "node_modules" not in str(f)]
    if env_files:
        results.append(f"  [PASS] .env found: {len(env_files)} file(s)")
    else:
        results.append("  [FAIL] No .env file found in any folder - MONGO_URI, JWT_SECRET, PORT required")
    return results

check_backend_universal = check_backend_smart

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_backend_smart(Path(path)):
        print(line)