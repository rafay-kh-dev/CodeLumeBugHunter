import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext, safe_read

def check_database_smart(project):
    results = []
    db_files = get_files_by_ext(project, [".js", ".jsx", ".ts", ".tsx", ".py", ".php"])
    all_text = ""
    file_texts = {}
    for f in db_files:
        try:
            text = safe_read(f)
            file_texts[f] = text
            all_text += text + "\n"
        except:
            pass
    if "mongoose" not in all_text.lower() and "【entity-mongodb¦canonical_name=MongoDB】" not in all_text.lower() and "SELECT" not in all_text and "prisma" not in all_text.lower():
        results.append("  No database usage found, skipped.")
        return results
    results.append("Database usage detected.")
    lower_text = all_text.lower()
    if "mongoose" in lower_text or "【entity-mongodb¦canonical_name=MongoDB】" in lower_text:
        if ".index(" in all_text or "index: true" in all_text or "index:true" in all_text:
            results.append("  [PASS] 【entity-MongoDB¦canonical_name=MongoDB】 indexes found - Queries will be fast")
        else:
            results.append("  [WARN] No 【entity-MongoDB¦canonical_name=MongoDB】 indexes found - Add index() on frequently queried fields")
        if ".limit(" in all_text or ".skip(" in all_text or "paginate" in lower_text or "page" in lower_text and "limit" in lower_text:
            results.append("  [PASS] Pagination or limit found - Large lists are handled")
        else:
            results.append("  [WARN] No pagination or limit found - Add .limit() to avoid loading all documents")
        n_plus_one = 0
        for f, text in file_texts.items():
            if re.search(r"for\s*\(.*\)\s*\{[^}]*\.(find|findOne)", text, re.DOTALL) or re.search(r"\.map\s*\(.*=>.*\.(find|findOne)", text, re.DOTALL):
                n_plus_one += 1
        if n_plus_one > 0:
            results.append(f"  [WARN] Possible N+1 query in {n_plus_one} file(s) - Avoid find() inside loops, use $in or populate")
        else:
            results.append("  [PASS] No N+1 pattern found")
        if ".lean()" in all_text:
            results.append("  [PASS] lean() used - Read queries are optimized")
        else:
            results.append("  [INFO] lean() not used - Use .lean() for read-only queries")
    if "SELECT" in all_text:
        if re.search(r"SELECT\s+\*\s+FROM", all_text, re.IGNORECASE):
            results.append("  [WARN] SELECT * found - Select only required columns")
        if "LIMIT" not in all_text.upper():
            results.append("  [WARN] SQL query without LIMIT - Add LIMIT to large queries")
    return results

check_database_universal = check_database_smart

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_database_smart(Path(path)):
        print(line)