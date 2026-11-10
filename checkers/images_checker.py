# images_checker.py - CodeLume Bug Hunter - Sirf Images ka check
# Kaam: Bari images pakarna jo website ko slow karti hain
# Ise performance.py bulayega, khud nahi chalega

from utils import is_ignored, format_size

def check_images(project):
    """Sirf images ka check - .jpg .png .webp sab."""
    out = []
    images = []
    total = 0

    for f in project.rglob("*"):
        if is_ignored(f):
            continue
        if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"]:
            sz = f.stat().st_size
            total += sz
            images.append((f, sz))

    # Sab se bari image pehle
    images.sort(key=lambda x: x[1], reverse=True)

    out.append(f"Total Images: {len(images)}, Total Size: {format_size(total)}")

    for f, sz in images[:10]:
        if sz > 500 * 1024:
            st = "FAIL"
        elif sz > 200 * 1024:
            st = "WARN"
        else:
            st = "OK"
        out.append(f"  [{st}] {f.name} - {format_size(sz)} - {f.relative_to(project)}")
        if sz > 500 * 1024:
            out.append(f"       Fix: 200KB se kam karo, WebP me badlo.")

    if not images:
        out.append("  [INFO] Koi image nahi mili.")

    return out