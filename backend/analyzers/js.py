import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext, is_test_file, safe_read

def check_js_smart(project):
    results = []
    all_files = get_files_by_ext(project, [".js", ".jsx", ".ts", ".tsx"])
    js_files = [f for f in all_files if not is_test_file(f)]
    if not js_files:
        results.append("  No JS / JSX files found, skipped.")
        return results
    results.append(f"Total JS Files (excluding tests): {len(js_files)}")
    total_img = 0
    total_console = 0
    for f in js_files:
        try:
            text = safe_read(f)
            rel = f.relative_to(project)
            imgs = re.findall(r"<img[^>]*>", text, re.IGNORECASE)
            if imgs:
                total_img += len(imgs)
                results.append(f"  [FAIL] <img> found: {rel} - {len(imgs)} times - Use next/image <Image> for optimization")
            total_console += text.count("console.log")
        except:
            pass
    results.append(f"Summary: <img>: {total_img}, console.log: {total_console}")
    if total_console > 0:
        results.append(f"  [WARN] console.log found: {total_console} times - Remove before production")
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_js_smart(Path(path)):
        print(line)