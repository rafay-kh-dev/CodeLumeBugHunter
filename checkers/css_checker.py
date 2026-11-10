# css_checker.py - CodeLume Bug Hunter - Sirf CSS ka check
# Kaam: Colors zyada hain, !important zyada hai, CSS bari hai, ye pakarna
# Ise performance.py bulayega, khud nahi chalega

import re
from utils import safe_read, get_files_by_ext, format_size

def check_css_smart(project):
    """Sirf .css files ka check, baaki kuch nahi."""
    out = []
    files = get_files_by_ext(project, ".css")

    if not files:
        return ["  Koi .css file nahi mili, skip. Tailwind ho sakta hai."]

    out.append(f"Total CSS Files: {len(files)}")

    unique_colors = set()
    total_important = 0

    for f in files:
        text = safe_read(f)

        # Saare hex colors dhoondo, white/black ko chor do
        for col in re.findall(r"#[0-9a-fA-F]{6}", text):
            if col.lower() not in ["#ffffff", "#000000"]:
                unique_colors.add(col.lower())

        total_important += text.count("!important")

        sz = f.stat().st_size
        if sz > 100 * 1024:
            out.append(f"  [WARN] Bari CSS file: {f.name} - {format_size(sz)} - Unused CSS hatayo, choti karo")

    out.append(f"Unique Colors in CSS: {len(unique_colors)}")
    if len(unique_colors) > 20:
        out.append(f"  [WARN] {len(unique_colors)} alag alag colors hain - Design System banao, ek file me colors rakho")
    else:
        out.append(f"  [PASS] Colors theek hain, sirf {len(unique_colors)} unique colors hain")

    out.append(f"!important count: {total_important}")
    if total_important > 5:
        out.append(f"  [WARN] !important {total_important} baar hai - Specificity theek karo, !important se bacho")
    else:
        out.append(f"  [PASS] !important theek hai")

    return out