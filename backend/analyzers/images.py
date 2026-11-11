import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext, format_size

def check_images(project):
    results = []
    image_exts = [".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".ico"]
    image_files = get_files_by_ext(project, image_exts)
    if not image_files:
        results.append("  No images found.")
        return results
    total_size = 0
    for f in image_files:
        try:
            total_size += f.stat().st_size
        except:
            pass
    results.append(f"Total Images: {len(image_files)}, Total Size: {format_size(total_size)}")
    for f in image_files:
        try:
            size_kb = f.stat().st_size / 1024
            rel = f.relative_to(project)
            if size_kb > 200:
                results.append(f"  [FAIL] {f.name} - {size_kb:.1f} KB - {rel}")
                results.append(f"       Fix: Reduce to under 200KB, convert to WebP.")
            elif size_kb > 100:
                results.append(f"  [WARN] {f.name} - {size_kb:.1f} KB - {rel}")
            else:
                results.append(f"  [OK] {f.name} - {size_kb:.1f} KB - {rel}")
        except:
            pass
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_images(Path(path)):
        print(line)