# performance.py - CodeLume Bug Hunter - UNIVERSAL SMART VERSION 6
# Fix: Next.js pehchanna, .gitignore root wali, JWT Installed vs Used
# Run: py performance.py "C:\CodeLume"

import argparse
import json
import re
from pathlib import Path

IGNORE = {"node_modules", ".next", ".git", "__pycache__", ".venv", "venv", "dist", "build"}

ALL_EXTS = [".html", ".py", ".jsx", ".tsx", ".js", ".ts", ".php", ".css", ".json", ".md", ".sql"]

def format_size(n):
    if n > 1024*1024:
        return f"{n/(1024*1024):.2f} MB"
    return f"{n/1024:.1f} KB"

def is_ignored(p: Path):
    for part in p.parts:
        if part in IGNORE:
            return True
    return False

def is_test_file(p: Path):
    name = p.name.lower()
    return ".test." in name or ".spec." in name or "test_" in name

def safe_read(file: Path):
    try:
        return file.read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

def get_files_by_ext(project: Path, ext: str):
    out = []
    for f in project.rglob(f"*{ext}"):
        if not is_ignored(f):
            out.append(f)
    return out

def get_all_code_files(project: Path):
    files = []
    for ext in [".js", ".jsx", ".ts", ".tsx", ".py", ".php", ".html", ".sql"]:
        for f in get_files_by_ext(project, ext):
            if not is_test_file(f):
                files.append(f)
    return files

# ---------- 1. PROJECT TYPE - FIXED ----------

def detect_project_type(project: Path):
    types = []
    counts = {}
    for ext in ALL_EXTS:
        c = len(get_files_by_ext(project, ext))
        if c > 0:
            counts[ext] = c

    has_next = False
    has_vite = False
    has_react = False
    # package.json se sahi check - bina space ke
    for pf in get_files_by_ext(project, ".json"):
        if pf.name == "package.json":
            try:
                data = json.loads(safe_read(pf))
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "next" in deps:
                    has_next = True
                if "vite" in deps or "@vitejs/plugin-react" in deps or "@tailwindcss/vite" in deps:
                    has_vite = True
                if "react" in deps:
                    has_react = True
            except:
                pass
    # File se bhi pehchano - agar app/page.jsx hai aur next.config hai to Next.js hai
    if (project / "next.config.js").exists() or (project / "next.config.mjs").exists():
        has_next = True
    if list(project.rglob("next.config.*")):
        has_next = True
    # Agar .jsx hai aur next hai to Next.js, agar .jsx hai aur vite hai to Vite
    if has_next:
        types.append("Next.js Project - next/image use hoga")
    elif has_vite and has_react:
        types.append("Vite + React Project - normal <img> + loading=lazy use hoga")
    elif has_react:
        types.append("React Project - Vite ya Next.js check karo")
    if counts.get(".php", 0) > 0:
        types.append(f"PHP Project - {counts['.php']} files")
    if counts.get(".py", 0) > 0:
        types.append(f"Python Project - {counts['.py']} files - automation ya backend")
    if counts.get(".sql", 0) > 0:
        types.append(f"SQL Database Project - {counts['.sql']} .sql files")
    if counts.get(".html", 0) > 0 and not has_next and not has_vite and not has_react:
        types.append(f"Static HTML Website - {counts['.html']} files")
    if not types:
        types.append("Unknown / Mixed Project")
    return types, counts, has_next, has_vite

# ---------- 2. SQL CHECK ----------

def check_sql_smart(project: Path):
    out = []
    files = get_files_by_ext(project, ".sql")
    if not files:
        return ["  Koi .sql file nahi mili, skip. Agar 【entity-MongoDB¦canonical_name=MongoDB】 hai to ye normal hai."]
    out.append(f"Total SQL Files: {len(files)}")
    total_tables = 0
    total_star = 0
    for f in files:
        text = safe_read(f)
        upper = text.upper()
        tables = upper.count("CREATE TABLE")
        total_tables += tables
        star = text.count("SELECT *") + text.count("select *")
        total_star += star
        out.append(f"  File: {f.relative_to(project)} - Tables: {tables}")
        if star > 0:
            out.append(f"    [FAIL] SELECT * {star} baar - Sirf zaroori columns likho")
        for line in text.split("\n"):
            l = line.strip().upper()
            if l.startswith("DELETE FROM") and "WHERE" not in l:
                out.append(f"    [FAIL] Khatarnak DELETE bina WHERE ke: {line.strip()[:70]}")
        if "PRIMARY KEY" not in upper and tables > 0:
            out.append(f"    [FAIL] PRIMARY KEY nahi hai")
        if "INDEX" not in upper and tables > 0:
            out.append(f"    [WARN] INDEX nahi mila - Search slow hoga")
    out.append(f"Summary: Tables: {total_tables}, SELECT *: {total_star}")
    return out

# ---------- 3. SECRETS ----------

def check_secrets_smart(project: Path):
    out = []
    found = 0
    for f in get_all_code_files(project):
        if ".env.example" in str(f):
            continue
        text = safe_read(f)
        patterns = [
            (r'API_KEY\s*=\s*["\'][^"\']{8,}["\']', "API_KEY hardcoded"),
            (r'password\s*=\s*["\'][^"\']{4,}["\']', "password hardcoded"),
            (r'sk-[a-zA-Z0-9]{10,}', "Stripe/OpenAI Secret Key lag rahi hai"),
            (r'ghp_[a-zA-Z0-9]{10,}', "GitHub Token leak"),
        ]
        for pat, msg in patterns:
            if re.search(pat, text):
                out.append(f"  [FAIL] {msg}: {f.relative_to(project)} - .env me rakho")
                found += 1
                break
    if found == 0:
        out.append("  [PASS] Koi hardcoded secret nahi mila.")
    return out

# ---------- 4. GITIGNORE - FIXED: Root pehle, Conditional ----------

def check_gitignore_smart(project: Path, counts):
    out = []
    # Pehle root wali .gitignore dhoondo - FIX
    gitignore = project / ".gitignore"
    if not gitignore.exists():
        all_git = [g for g in project.rglob(".gitignore") if not is_ignored(g)]
        if all_git:
            gitignore = all_git[0]
            out.append(f"  [WARN] Root me .gitignore nahi, subfolder wali mili: {gitignore.relative_to(project)}")
        else:
            out.append("  [FAIL] .gitignore nahi hai - .env GitHub pe chala jayega!")
            return out
    else:
        out.append(f"  .gitignore mili: {gitignore.relative_to(project)} (Root wali - sahi)")
    text = safe_read(gitignore)
    # Sab ko .env chahiye
    if ".env" in text:
        out.append("  [PASS] .env .gitignore me hai")
    else:
        out.append("  [FAIL] .env .gitignore me nahi hai")
    # JS wale ko node_modules chahiye
    is_js = counts.get(".js", 0) > 0 or counts.get(".jsx", 0) > 0 or counts.get(".json", 0) > 0
    is_py = counts.get(".py", 0) > 0
    if is_js:
        if "node_modules" in text:
            out.append("  [PASS] node_modules .gitignore me hai")
        else:
            out.append("  [FAIL] node_modules .gitignore me nahi hai")
    if is_py:
        if "__pycache__" in text:
            out.append("  [PASS] __pycache__ .gitignore me hai")
        else:
            out.append("  [FAIL] __pycache__ .gitignore me nahi hai - Python wale ke liye zaroori hai")
    if not is_js and not is_py:
        out.append("  [INFO] JS/Python nahi, is liye node_modules/__pycache__ ki zaroorat nahi")
    return out

# ---------- 5. HTML + ACCESSIBILITY ----------

def check_html_smart(project: Path, has_next):
    out = []
    files = get_files_by_ext(project, ".html")
    jsx_files = get_files_by_ext(project, ".jsx") + get_files_by_ext(project, ".tsx")
    out.append(f"HTML: {len(files)}, JSX/TSX: {len(jsx_files)}")
    no_alt = 0
    for f in files + jsx_files:
        if is_test_file(f):
            continue
        text = safe_read(f)
        for img in re.findall(r"<img[^>]*>", text):
            if "alt" not in img:
                no_alt += 1
                out.append(f"  [FAIL] <img> me alt nahi: {f.relative_to(project)}")
                break
    if no_alt == 0:
        out.append("  [PASS] Sab <img> me alt hai.")
    if has_next:
        out.append("  Project Next.js hai, <img> ki jagah <Image> use karo.")
    else:
        out.append("  Project Vite/HTML hai, <img loading='lazy'> use karo.")
    return out

# ---------- 6. PYTHON ----------

def check_python_smart(project: Path):
    out = []
    files = get_files_by_ext(project, ".py")
    if not files:
        return ["  Koi .py nahi, skip."]
    out.append(f"Total Python Files: {len(files)}")
    for f in files:
        text = safe_read(f)
        if text.count("print(") > 5:
            out.append(f"  [WARN] print() zyada: {f.relative_to(project)} - logging use karo")
        if "except:" in text:
            out.append(f"  [WARN] Khali except: {f.relative_to(project)} - except Exception as e likho")
    if len(out) == 1:
        out.append("  [PASS] Python theek hai.")
    return out

# ---------- 7. PHP ----------

def check_php_smart(project: Path):
    out = []
    files = get_files_by_ext(project, ".php")
    if not files:
        return ["  Koi .php nahi, skip."]
    out.append(f"Total PHP: {len(files)}")
    for f in files:
        text = safe_read(f)
        if "mysqli_query" in text and "prepare" not in text:
            out.append(f"  [FAIL] SQL Injection: {f.relative_to(project)}")
    if len(out) == 1:
        out.append("  [PASS] PHP theek hai.")
    return out

# ---------- 8. CSS ----------

def check_css_smart(project: Path):
    out = []
    files = get_files_by_ext(project, ".css")
    if not files:
        return ["  Koi .css nahi, skip."]
    out.append(f"Total CSS: {len(files)}")
    uniq = set()
    for f in files:
        t = safe_read(f)
        for col in re.findall(r"#[0-9a-fA-F]{6}", t):
            if col.lower() not in ["#ffffff", "#000000"]:
                uniq.add(col.lower())
    out.append(f"Unique Colors: {len(uniq)}")
    return out

# ---------- 9. JSON ----------

def check_json_smart(project: Path):
    out = []
    files = get_files_by_ext(project, ".json")
    out.append(f"Total JSON: {len(files)}")
    for f in files:
        if "package-lock" in f.name:
            continue
        try:
            data = json.loads(safe_read(f))
            if f.name == "package.json":
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                out.append(f"  Tech Stack ({f.relative_to(project)}): {', '.join(list(deps.keys())[:6])} ... Total {len(deps)}")
        except:
            out.append(f"  [FAIL] Toota JSON: {f.relative_to(project)}")
    return out

# ---------- 10. JS / JSX ----------

def check_js_smart(project: Path, has_next):
    out = []
    files = []
    for ext in [".js", ".jsx", ".ts", ".tsx"]:
        for f in get_files_by_ext(project, ext):
            if not is_test_file(f):
                files.append(f)
    out.append(f"Total JS Files (test chor ke): {len(files)}")
    img_c = 0
    console_c = 0
    for f in files:
        text = safe_read(f)
        if "<img" in text:
            c = text.count("<img")
            img_c += c
            if has_next:
                out.append(f"  [FAIL] <img>: {f.relative_to(project)} - {c} baar - next/image use karo")
            else:
                out.append(f"  [INFO] <img>: {f.relative_to(project)} - {c} baar - loading='lazy' lagao")
        if "console.log" in text:
            console_c += text.count("console.log")
    out.append(f"Summary: <img>: {img_c}, console.log: {console_c}")
    return out

# ---------- 11. IMAGES + BACKEND ----------

def check_images(project: Path):
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
    images.sort(key=lambda x: x[1], reverse=True)
    out.append(f"Total Images: {len(images)}, Total: {format_size(total)}")
    for f, sz in images[:8]:
        st = "FAIL" if sz > 500*1024 else "WARN" if sz > 200*1024 else "OK"
        out.append(f"  [{st}] {f.name} - {format_size(sz)} - {f.relative_to(project)}")
    return out

def check_backend_universal(project: Path):
    out = []
    all_text = ""
    for f in get_all_code_files(project):
        all_text += safe_read(f) + "\n"
    # JWT - Installed vs Used - SMART
    jwt_installed = False
    for pf in get_files_by_ext(project, ".json"):
        if pf.name == "package.json":
            try:
                data = json.loads(safe_read(pf))
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "jsonwebtoken" in deps:
                    jwt_installed = True
            except:
                pass
    jwt_used = "jsonwebtoken" in all_text or "jwt.verify" in all_text or "JWT_SECRET" in all_text
    if jwt_used:
        out.append("  [PASS] JWT: Use ho raha hai")
    elif jwt_installed and not jwt_used:
        out.append("  [WARN] JWT: Install to hai (package.json me hai), lekin code me use nahi ho raha - Ya to use karo, ya uninstall karo")
    else:
        out.append("  [INFO] JWT: Install bhi nahi, use bhi nahi - Agar login nahi hai to theek hai")
    out.append(f"  CORS: {'[PASS]' if 'cors' in all_text.lower() else '[INFO] Nahi mila'}")
    out.append(f"  MongoDB: {'[PASS]' if 'mongoose' in all_text else '[INFO] Nahi mila'}")
    env_files = [str(f.relative_to(project)) for f in project.rglob(".env*") if not is_ignored(f)]
    if env_files:
        out.append(f"  [PASS] .env: {', '.join(env_files)}")
    else:
        out.append("  [FAIL] .env nahi mili")
    return out

def check_md_smart(project: Path):
    out = []
    files = get_files_by_ext(project, ".md")
    out.append(f"Total MD: {len(files)}")
    if (project / "README.md").exists():
        out.append("  [PASS] README.md hai")
    else:
        out.append("  [WARN] README.md nahi hai")
    return out

def main():
    parser = argparse.ArgumentParser(description="CodeLume Bug Hunter - V6")
    parser.add_argument("rasta", help="Project ka rasta")
    args = parser.parse_args()
    project = Path(args.rasta)
    if not project.exists():
        print(f"ERROR: Folder nahi mila: {args.rasta}")
        return
    print("CODELUME BUG HUNTER - UNIVERSAL SMART VERSION 6")
    print(f"Project: {project}")
    print("=" * 70)
    types, counts, has_next, has_vite = detect_project_type(project)
    print("\n[1] PROJECT TYPE - FIXED:")
    for t in types:
        print(f"  - {t}")
    print("  File Counts:")
    for k, v in counts.items():
        print(f"    {k}: {v}")
    print("\n[2] SQL CHECK:")
    for l in check_sql_smart(project):
        print(l)
    print("\n[3] SECRETS CHECK:")
    for l in check_secrets_smart(project):
        print(l)
    print("\n[4] GITIGNORE CHECK - FIXED:")
    for l in check_gitignore_smart(project, counts):
        print(l)
    print("\n[5] HTML + ACCESSIBILITY:")
    for l in check_html_smart(project, has_next):
        print(l)
    print("\n[6] PYTHON CHECK:")
    for l in check_python_smart(project):
        print(l)
    print("\n[7] PHP CHECK:")
    for l in check_php_smart(project):
        print(l)
    print("\n[8] CSS CHECK:")
    for l in check_css_smart(project):
        print(l)
    print("\n[9] JSON + TECH STACK:")
    for l in check_json_smart(project):
        print(l)
    print("\n[10] MARKDOWN:")
    for l in check_md_smart(project):
        print(l)
    print("\n[11] JS / JSX - Vite vs Next:")
    for l in check_js_smart(project, has_next):
        print(l)
    print("\n[12] IMAGES:")
    for l in check_images(project):
        print(l)
    print("\n[13] BACKEND - JWT Installed vs Used:")
    for l in check_backend_universal(project):
        print(l)
    print("\n" + "=" * 70)
    print("Report ban rahi hai: performance_report.md")
    report = [f"# CodeLume Bug Hunter - V6", f"Project: {project}", "", "## Project Type"] + [f"- {t}" for t in types]
    report += ["", "## SQL"] + check_sql_smart(project)
    report += ["", "## Secrets"] + check_secrets_smart(project)
    report += ["", "## Gitignore"] + check_gitignore_smart(project, counts)
    report += ["", "## HTML"] + check_html_smart(project, has_next)
    report += ["", "## Python"] + check_python_smart(project)
    report += ["", "## PHP"] + check_php_smart(project)
    report += ["", "## CSS"] + check_css_smart(project)
    report += ["", "## JSON"] + check_json_smart(project)
    report += ["", "## JS"] + check_js_smart(project, has_next)
    report += ["", "## Images"] + check_images(project)
    report += ["", "## Backend"] + check_backend_universal(project)
    Path("performance_report.md").write_text("\n".join(report), encoding="utf-8")
    print("Ho gaya! Ab tool aur bhi smart hai.")

if __name__ == "__main__":
    main()