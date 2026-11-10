# php_checker.py - CodeLume Bug Hunter - Sirf PHP ka check
# Kaam: PHP me SQL Injection, XSS, kamzor password hashing pakarna
# Ise performance.py bulayega, khud nahi chalega

from utils import safe_read, get_files_by_ext

def check_php_smart(project):
    """Sirf .php files ka check, baaki kuch nahi."""
    out = []
    files = get_files_by_ext(project, ".php")

    if not files:
        return ["  Koi .php file nahi mili, skip."]

    out.append(f"Total PHP Files: {len(files)}")

    for f in files:
        text = safe_read(f)

        # SQL Injection - sab se khatarnak
        if "mysqli_query" in text and "prepare" not in text:
            out.append(f"  [FAIL] SQL Injection ka khatra: {f.relative_to(project)} - mysqli_prepare() use karo, direct query mat likho")

        # XSS - user ka data bina saf kiye dikhana
        if "echo $_GET" in text or "echo $_POST" in text:
            out.append(f"  [FAIL] XSS ka khatra: {f.relative_to(project)} - htmlspecialchars() lagao")

        # Kamzor password hashing
        if "md5(" in text or "sha1(" in text:
            out.append(f"  [FAIL] Kamzor password hashing: {f.relative_to(project)} - password_hash() use karo, md5 ab toot jata hai")

        # Hardcoded password ka shak
        if "password" in text.lower() and "=" in text and "$_ENV" not in text:
            out.append(f"  [WARN] Hardcoded password ho sakta hai: {f.relative_to(project)} - .env me rakho")

    if len(out) == 1:
        out.append("  [PASS] PHP me bara masla nahi mila.")

    return out