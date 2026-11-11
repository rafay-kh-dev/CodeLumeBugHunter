import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext

def check_sql_smart(project):
    results = []
    sql_files = get_files_by_ext(project, [".sql"])
    sql_files = [f for f in sql_files if f.suffix == ".sql"]

    if not sql_files:
        results.append("  No .sql files found, skipped. Normal if using MongoDB.")
        return results

    results.append(f"Total SQL Files: {len(sql_files)}")
    for f in sql_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            rel = f.relative_to(project)
            if "SELECT *" in text:
                results.append(f"  [WARN] SELECT * found: {rel} - Specify columns instead of *")
            if "DELETE" in text and "WHERE" not in text:
                results.append(f"  [FAIL] DELETE without WHERE: {rel} - Dangerous, will delete all rows")
            if "DROP TABLE" in text:
                results.append(f"  [WARN] DROP TABLE found: {rel}")
            if "PRIMARY KEY" in text:
                results.append(f"  [PASS] PRIMARY KEY found: {rel}")
            if "INDEX" in text:
                results.append(f"  [PASS] INDEX found: {rel}")
            if "FOREIGN KEY" in text:
                results.append(f"  [PASS] FOREIGN KEY found: {rel}")
        except:
            pass
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_sql_smart(Path(path)):
        print(line)