# js_checker.py - CodeLume Bug Hunter - Sirf JS / JSX / TSX ka check
# Kaam: <img> aur console.log pakarna, Vite vs Next ka farq samajh ke
# Ise performance.py bulayega, khud nahi chalega

from core.utils import safe_read, get_files_by_ext, is_test_file

def check_js_smart(project, has_next):
    """Sirf JS / JSX / TS / TSX ka check, test files ko chor ke."""
    out = []
    files = []

    for ext in [".js", ".jsx", ".ts", ".tsx"]:
        for f in get_files_by_ext(project, ext):
            if not is_test_file(f):
                files.append(f)

    if not files:
        return ["  Koi JS / JSX file nahi mili, skip."]

    out.append(f"Total JS Files (test chor ke): {len(files)}")

    img_c = 0
    console_c = 0

    for f in files:
        text = safe_read(f)

        if "<img" in text:
            c = text.count("<img")
            img_c += c
            if has_next:
                out.append(f"  [FAIL] <img> mila: {f.relative_to(project)} - {c} baar - next/image use karo")
            else:
                out.append(f"  [INFO] <img> mila: {f.relative_to(project)} - {c} baar - loading='lazy' + width/height lagao")

        if "console.log" in text:
            console_c += text.count("console.log")

    out.append(f"Summary: <img>: {img_c}, console.log: {console_c}")

    if console_c > 5:
        out.append(f"  [WARN] console.log {console_c} baar hai, zyada hai - Production me hatayo")
    elif console_c == 0:
        out.append(f"  [PASS] Koi console.log nahi, clean code hai")

    return out