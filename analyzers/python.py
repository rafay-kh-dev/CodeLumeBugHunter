import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext

def check_python_smart(project):
    results = []
    py_files = get_files_by_ext(project, [".py"])
    py_files = [f for f in py_files if f.suffix == ".py"]
    if not py_files:
        results.append("  No .py files found, skipped.")
        return results
    results.append(f"Total Python Files: {len(py_files)}")
    for f in py_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            rel = f.relative_to(project)
            print_count = text.count("print(")
            if print_count > 3:
                results.append(f"  [WARN] Too many print() calls: {rel} - Use logging instead, print is not for production")
            if re.search(r"except\s*:", text):
                results.append(f"  [WARN] Bare except found: {rel} - Use except Exception as e, otherwise errors will be hidden")
            if "import os" in text and "os.system" in text:
                results.append(f"  [WARN] os.system() found: {rel} - Use subprocess instead")
            if "eval(" in text or "exec(" in text:
                results.append(f"  [FAIL] eval() / exec() found: {rel} - Dangerous, avoid dynamic code execution")
        except:
            pass
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_python_smart(Path(path)):
        print(line)