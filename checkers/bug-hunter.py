# bug_hunter.py - CodeLume Bug Hunter Version 1
# Kaam: MERN project ke common bugs pakarna, bina API ke
# Run: py bug_hunter.py "C:\CodeLume"

import argparse
import json
from pathlib import Path

def print_result(naam, passed, detail):
    nishan = "[PASS]" if passed else "[FAIL]"
    print(f"{nishan} {naam} - {detail}")

def check_package_json(project: Path):
    file = project / "package.json"
    if not file.exists():
        return False, "package.json nahi mili. Kya ye Node.js project hai?"
    try:
        data = json.loads(file.read_text(encoding="utf-8", errors="ignore"))
        deps = list(data.get("dependencies", {}).keys())
        return True, f"package.json mil gayi. Dependencies: {', '.join(deps[:5])}"
    except:
        return False, "package.json kharab hai, JSON parha nahi gaya"

def check_env(project: Path):
    file = project / ".env"
    if not file.exists():
        return False, ".env nahi mili. MONGO_URI aur PORT is me hone chahiye"
    text = file.read_text(encoding="utf-8", errors="ignore")
    if "MONGO_URI" not in text and "【entity-MONGODB¦canonical_name=MongoDB】" not in text:
        return False, ".env mil gayi lekin us me MONGO_URI nahi hai"
    return True, ".env mil gayi aur MONGO_URI bhi hai"

def search_in_js_files(project: Path, lafz: str):
    for file in project.rglob("*.js"):
        if "node_modules" in str(file):
            continue
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
            if lafz in text:
                return True, str(file)
        except:
            continue
    return False, ""

def check_cors(project: Path):
    mila, kahan = search_in_js_files(project, "cors")
    if mila:
        return True, f"CORS mil gaya, file: {kahan}"
    return False, "CORS nahi mila. Backend me 'npm i cors' aur 'app.use(cors())' lagana parega"

def check_mongodb(project: Path):
    mila, kahan = search_in_js_files(project, "mongoose")
    if not mila:
        mila, kahan = search_in_js_files(project, "MONGO_URI")
    if mila:
        return True, f"【entity-MongoDB¦canonical_name=MongoDB】 connection mil gaya, file: {kahan}"
    return False, "【entity-MongoDB¦canonical_name=MongoDB】 connection nahi mila. mongoose.connect() ya MONGO_URI check karo"

def check_port(project: Path):
    mila, kahan = search_in_js_files(project, "process.env.PORT")
    if mila:
        return True, f"PORT process.env se aa raha hai, file: {kahan}"
    return False, "PORT hardcoded hai ya missing hai. process.env.PORT use karo"

def main():
    parser = argparse.ArgumentParser(description="CodeLume Bug Hunter - Offline")
    parser.add_argument("rasta", help="Apne project ka folder ka rasta likho, misal: C:\\CodeLume")
    args = parser.parse_args()

    project = Path(args.rasta)
    if not project.exists():
        print(f"ERROR: Ye folder nahi mila: {args.rasta}")
        return

    print(f"Checking project: {project}")
    print("=" * 50)

    checks = [
        ("package.json", check_package_json(project)),
        (".env File", check_env(project)),
        ("CORS Check", check_cors(project)),
        ("MongoDB Check", check_mongodb(project)),
        ("PORT Check", check_port(project)),
    ]

    for naam, (passed, detail) in checks:
        print_result(naam, passed, detail)

    print("=" * 50)
    total_pass = sum(1 for _, (p, _) in checks if p)
    print(f"Result: {total_pass} / {len(checks)} PASS")

    lines = [f"# Bug Hunter Report - {project}", ""]
    for naam, (passed, detail) in checks:
        lines.append(f"- [{'PASS' if passed else 'FAIL'}] {naam} - {detail}")
    Path("bug_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Report ban gayi: bug_report.md")

if __name__ == "__main__":
    main()