# python_checker.py - CodeLume Bug Hunter - Sirf Python ka check
# Kaam: Python me print() zyada hai, khali except hai, ye pakarna
# Ise performance.py bulayega, khud nahi chalega

from core.utils import safe_read, get_files_by_ext

def check_python_smart(project):
    """Sirf .py files ka check, baaki kuch nahi."""
    out = []
    files = get_files_by_ext(project, ".py")

    if not files:
        return ["  Koi .py file nahi mili, skip."]

    out.append(f"Total Python Files: {len(files)}")

    for f in files:
        text = safe_read(f)

        if text.count("print(") > 5:
            out.append(f"  [WARN] print() zyada hai: {f.relative_to(project)} - logging use karo, print production me nahi")

        if "except:" in text:
            out.append(f"  [WARN] Khali except hai: {f.relative_to(project)} - except Exception as e likho, warna error chup jayega")

        if "TODO" in text or "FIXME" in text:
            out.append(f"  [WARN] TODO / FIXME mila: {f.relative_to(project)} - Kaam adhoora hai")

        # Bari file ka check
        sz = f.stat().st_size
        if sz > 80 * 1024:
            out.append(f"  [WARN] Bari file hai: {f.name} - {sz // 1024} KB - Tor ke choti files banao")

    if len(out) == 1:
        out.append("  [PASS] Python me bara masla nahi mila.")

    return out