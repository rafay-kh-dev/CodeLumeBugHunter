import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext

def check_php_smart(project):
    results = []
    php_files = get_files_by_ext(project, [".php"])
    php_files = [f for f in php_files if f.suffix == ".php"]
    if not php_files:
        results.append("  No .php files found, skipped.")
        return results
    results.append(f"Total PHP Files: {len(php_files)}")
    for f in php_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            rel = f.relative_to(project)
            if "echo $_GET" in text or "echo $_POST" in text:
                results.append(f"  [FAIL] Unsanitized output found: {rel} - Use htmlspecialchars() to prevent XSS")
            if "mysql_query" in text:
                results.append(f"  [FAIL] Deprecated mysql_query() found: {rel} - Use PDO or MySQLi")
            if "$_GET" in text and "isset" not in text:
                results.append(f"  [WARN] Direct $_GET access: {rel} - Validate input before use")
            if "var_dump" in text or "print_r" in text:
                results.append(f"  [WARN] Debug function found: {rel} - Remove before production")
        except:
            pass
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_php_smart(Path(path)):
        print(line)