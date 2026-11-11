import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext

def check_md_smart(project):
    results = []
    md_files = get_files_by_ext(project, [".md"])
    md_files = [f for f in md_files if f.suffix == ".md"]

    if not md_files:
        results.append("  [WARN] No Markdown files found.")
        return results

    results.append(f"Total MD Files: {len(md_files)}")
    readme = Path(project) / "README.md"
    if readme.exists():
        results.append("  [PASS] README.md found.")
        try:
            text = readme.read_text(encoding="utf-8", errors="ignore")
            checks = {
                "Installation": "Installation" in text or "Install" in text,
                "Usage": "Usage" in text or "Usage" in text,
                "Features": "Features" in text or "Feature" in text,
                "License": "License" in text,
            }
            for section, found in checks.items():
                if found:
                    results.append(f"  [PASS] README contains {section} section.")
                else:
                    results.append(f"  [WARN] README missing {section} section.")
            if len(text.strip()) < 200:
                results.append("  [WARN] README.md is too short, add project description.")
            broken = re.findall(r"\[.*?\]\(\)", text)
            if broken:
                results.append(f"  [FAIL] Empty links found in README.md: {len(broken)}")
            images = re.findall(r"!\[.*?\]\(.*?\)", text)
            if images:
                results.append(f"  [INFO] Images in README.md: {len(images)}")
        except:
            pass
    else:
        results.append("  [FAIL] README.md not found in project root.")
    for f in md_files:
        if f.name == "README.md":
            continue
        try:
            if f.stat().st_size == 0:
                results.append(f"  [WARN] Empty file: {f.relative_to(project)}")
        except:
            pass
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_md_smart(Path(path)):
        print(line)