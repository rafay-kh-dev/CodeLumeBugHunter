# html_checker.py - CodeLume Bug Hunter - Sirf HTML + Accessibility ka check
# Kaam: <img> me alt hai ya nahi, aur Vite hai ya Next.js, us hisab se salah dena
# Ise performance.py bulayega, khud nahi chalega

import re
from core.utils import safe_read, get_files_by_ext, is_test_file

def check_html_smart(project, has_next):
    """HTML + JSX me alt check karo, aur Vite vs Next ka farq batao."""
    out = []
    files = get_files_by_ext(project, ".html")
    jsx_files = get_files_by_ext(project, ".jsx") + get_files_by_ext(project, ".tsx")

    out.append(f"HTML Files: {len(files)}, JSX/TSX Files: {len(jsx_files)}")

    no_alt = 0
    for f in files + jsx_files:
        if is_test_file(f):
            continue
        text = safe_read(f)
        # Saare <img> dhoondo
        for img in re.findall(r"<img[^>]*>", text):
            if "alt" not in img:
                no_alt += 1
                out.append(f"  [FAIL] <img> me alt nahi hai: {f.relative_to(project)} - alt='...' likho, blind users ke liye zaroori hai")
                break

    if no_alt == 0:
        out.append("  [PASS] Sab <img> me alt hai, accessibility theek hai.")

    # Vite hai ya Next.js, us hisab se salah - SMART
    if has_next:
        out.append("  Project Next.js hai, is liye <img> ki jagah <Image> use karo.")
    else:
        out.append("  Project Vite / HTML hai, is liye <img loading='lazy'> use karo, next/image nahi.")

    return out