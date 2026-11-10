# performance.py - CodeLume Bug Hunter - FOLDERS WALA BOSS
# Kaam: Sirf checkers ko bulana, khud kuch check nahi karna
# Ab checkers checkers/ folder me hain, core core/ folder me hai
# Run: py performance.py "C:\CodeLume"

import argparse
from pathlib import Path

# Core se - bunyad wali cheez
from core.project_detector import detect_project_type
# Checkers se - sab checkers apne folder se
from checkers.sql_checker import check_sql_smart
from checkers.secrets_checker import check_secrets_smart
from checkers.gitignore_checker import check_gitignore_smart
from checkers.html_checker import check_html_smart
from checkers.python_checker import check_python_smart
from checkers.php_checker import check_php_smart
from checkers.css_checker import check_css_smart
from checkers.json_checker import check_json_smart
from checkers.js_checker import check_js_smart
from checkers.images_checker import check_images
from checkers.backend_checker import check_backend_universal
from checkers.md_checker import check_md_smart

def main():
    parser = argparse.ArgumentParser(description="CodeLume Bug Hunter - Professional Folders")
    parser.add_argument("rasta", help="Project ka rasta, misal: C:\\CodeLume")
    args = parser.parse_args()
    project = Path(args.rasta)

    if not project.exists():
        print(f"ERROR: Folder nahi mila: {args.rasta}")
        return

    print("CODELUME BUG HUNTER - PROFESSIONAL FOLDERS VERSION")
    print(f"Project: {project}")
    print("=" * 70)

    # Step 1 - Pehle project ki pehchan
    types, counts, has_next, has_vite = detect_project_type(project)
    print("\n[1] PROJECT TYPE:")
    for t in types:
        print(f"  - {t}")
    print("  File Counts:")
    for k, v in counts.items():
        print(f"    {k}: {v}")

    # Step 2 - Sab checkers ko bulayo
    all_results = {}
    all_results["SQL"] = check_sql_smart(project)
    all_results["Secrets"] = check_secrets_smart(project)
    all_results["Gitignore"] = check_gitignore_smart(project, counts)
    all_results["HTML"] = check_html_smart(project, has_next)
    all_results["Python"] = check_python_smart(project)
    all_results["PHP"] = check_php_smart(project)
    all_results["CSS"] = check_css_smart(project)
    all_results["JSON"] = check_json_smart(project)
    all_results["Markdown"] = check_md_smart(project)
    all_results["JS"] = check_js_smart(project, has_next)
    all_results["Images"] = check_images(project)
    all_results["Backend"] = check_backend_universal(project)

    titles = {
        "SQL": "[2] SQL CHECK:",
        "Secrets": "[3] SECRETS CHECK:",
        "Gitignore": "[4] GITIGNORE CHECK:",
        "HTML": "[5] HTML + ACCESSIBILITY:",
        "Python": "[6] PYTHON CHECK:",
        "PHP": "[7] PHP CHECK:",
        "CSS": "[8] CSS CHECK:",
        "JSON": "[9] JSON + TECH STACK:",
        "Markdown": "[10] MARKDOWN / README:",
        "JS": "[11] JS / JSX:",
        "Images": "[12] IMAGES:",
        "Backend": "[13] BACKEND:",
    }

    for key in ["SQL", "Secrets", "Gitignore", "HTML", "Python", "PHP", "CSS", "JSON", "Markdown", "JS", "Images", "Backend"]:
        print(f"\n{titles[key]}")
        for line in all_results[key]:
            print(line)

    print("\n" + "=" * 70)
    print("Report ban rahi hai: performance_report.md")
    report = [f"# CodeLume Bug Hunter - Folders Report", f"Project: {project}", "", "## Project Type"] + [f"- {t}" for t in types]
    report += ["", "## File Counts"] + [f"- {k}: {v}" for k, v in counts.items()]
    for key in ["SQL", "Secrets", "Gitignore", "HTML", "Python", "PHP", "CSS", "JSON", "Markdown", "JS", "Images", "Backend"]:
        report += ["", f"## {key}"] + all_results[key]

    Path("performance_report.md").write_text("\n".join(report), encoding="utf-8")
    print("Ho gaya! Folders wala architecture chal gaya.")

if __name__ == "__main__":
    main()