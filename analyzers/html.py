import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext, safe_read

def check_html_smart(project):
    results = []
    html_files = get_files_by_ext(project, [".html"])
    jsx_files = get_files_by_ext(project, [".jsx", ".tsx"])
    results.append(f"HTML Files: {len(html_files)}, JSX/TSX Files: {len(jsx_files)}")
    total_img = 0
    missing_alt = 0
    for f in html_files + jsx_files:
        try:
            text = safe_read(f)
            imgs = re.findall(r"<img[^>]*>", text, re.IGNORECASE)
            for img in imgs:
                total_img += 1
                if "alt=" not in img.lower():
                    missing_alt += 1
        except:
            pass
    if total_img == 0:
        results.append("  [INFO] No <img> tags found.")
    elif missing_alt == 0:
        results.append("  [PASS] All <img> tags have alt attributes, accessibility is good.")
    else:
        results.append(f"  [WARN] {missing_alt} of {total_img} <img> tags missing alt attribute - Add alt for accessibility")
    # Next.js detection
    is_next = False
    for f in get_files_by_ext(project, [".json"]):
        try:
            if f.name == "package.json" and '"next"' in safe_read(f):
                is_next = True
                break
        except:
            pass
    if is_next:
        results.append("  Project is Next.js, use <Image> instead of <img> for optimization.")
    return results

check_html_universal = check_html_smart
check_html = check_html_smart

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_html_smart(Path(path)):
        print(line)