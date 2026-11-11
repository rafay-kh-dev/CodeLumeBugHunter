import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext, safe_read, format_size

def check_css_smart(project):
    results = []
    css_files = get_files_by_ext(project, [".css"])
    css_files = [f for f in css_files if f.suffix == ".css"]
    if not css_files:
        results.append("  No .css files found, skipped. Tailwind may be in use.")
        return results
    results.append(f"Total CSS Files: {len(css_files)}")
    all_colors = set()
    total_important = 0
    total_size = 0
    for f in css_files:
        try:
            text = safe_read(f)
            total_size += f.stat().st_size
            colors = re.findall(r"#[0-9a-fA-F]{3,8}\b", text)
            all_colors.update([c.lower() for c in colors])
            total_important += text.count("!important")
        except:
            pass
    results.append(f"Unique Colors in CSS: {len(all_colors)}")
    if len(all_colors) <= 10:
        results.append(f"  [PASS] Color palette is consistent, only {len(all_colors)} unique colors")
    else:
        results.append(f"  [WARN] Too many colors: {len(all_colors)} unique colors - Use design tokens for consistency")
    results.append(f"!important count: {total_important}")
    if total_important <= 5:
        results.append("  [PASS] !important usage is acceptable")
    else:
        results.append(f"  [WARN] Too many !important: {total_important} - Avoid !important, use specificity instead")
    results.append(f"Total CSS Size: {format_size(total_size)}")
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_css_smart(Path(path)):
        print(line)