import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext

def is_build_file(path):
    parts = set(path.parts)
    return bool(parts & {"node_modules", ".next", ".git", "__pycache__", "dist", "build", ".vercel", "coverage"})

def check_frontend_smart(project, has_next=False):
    results = []
    all_js = get_files_by_ext(project, [".jsx", ".tsx", ".js"])
    all_css = get_files_by_ext(project, [".css"])
    jsx_files = [f for f in all_js if not is_build_file(f.relative_to(project)) and "codelume-backend" not in str(f.relative_to(project))]
    css_files = [f for f in all_css if not is_build_file(f.relative_to(project))]
    jsx_only = [f for f in jsx_files if f.suffix in [".jsx", ".tsx"]]
    total_js_size = 0
    total_css_size = 0
    for f in jsx_files:
        try:
            total_js_size += f.stat().st_size
        except:
            pass
    for f in css_files:
        try:
            total_css_size += f.stat().st_size
        except:
            pass
    total_kb = (total_js_size + total_css_size) / 1024
    results.append(f"Frontend Files: {len(jsx_files)} JS/JSX, {len(css_files)} CSS")
    results.append(f"Total Frontend Bundle: {total_kb:.1f} KB")
    if total_kb > 1000:
        results.append(f"  [FAIL] Frontend bundle too large: {total_kb:.1f} KB - Split code, remove unused dependencies")
    elif total_kb > 500:
        results.append(f"  [WARN] Frontend bundle large: {total_kb:.1f} KB - Consider code splitting")
    else:
        results.append(f"  [PASS] Frontend bundle size OK: {total_kb:.1f} KB")
    img_total = 0
    img_lazy = 0
    img_files = []
    for f in jsx_only:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            imgs = re.findall(r"<img[^>]*>", text, re.IGNORECASE)
            for img in imgs:
                img_total += 1
                if 'loading="lazy"' in img or "loading='lazy'" in img:
                    img_lazy += 1
            if imgs and has_next:
                img_files.append(f)
        except:
            pass
    for f in jsx_only:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            if ".map(" in text and "key=" not in text:
                results.append(f"  [WARN] Missing key prop in list: {f.relative_to(project)} - Add key to .map() items")
        except:
            pass
    if img_total > 0:
        results.append(f"Images in JSX: {img_total}, Lazy Loaded: {img_lazy}")
        if img_lazy < img_total:
            results.append(f"  [WARN] {img_total - img_lazy} images missing loading=\"lazy\" - Add lazy loading for faster page load")
        else:
            results.append("  [PASS] All images use lazy loading.")
        if has_next and img_files:
            results.append(f"  [FAIL] <img> found in {len(img_files)} files - Use next/image <Image> for optimization")
    console_count = 0
    debugger_count = 0
    for f in jsx_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            console_count += text.count("console.log")
            debugger_count += text.count("debugger")
        except:
            pass
    if console_count > 0:
        results.append(f"  [WARN] console.log found: {console_count} times - Remove before production")
    if debugger_count > 0:
        results.append(f"  [FAIL] debugger found: {debugger_count} times - Remove before production")
    large_files = []
    for f in jsx_files:
        try:
            size_kb = f.stat().st_size / 1024
            if size_kb > 200:
                large_files.append(f"{f.relative_to(project)} - {size_kb:.1f} KB")
        except:
            pass
    for lf in large_files:
        results.append(f"  [WARN] Large file: {lf} - Split into smaller components")
    if not large_files:
        results.append("  [PASS] No large frontend files found.")
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_frontend_smart(Path(path), True):
        print(line)