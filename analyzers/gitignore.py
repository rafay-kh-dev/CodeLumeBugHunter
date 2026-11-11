import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def check_gitignore_smart(project, counts=None):
    results = []
    root_gitignore = Path(project) / ".gitignore"
    gitignore_path = None
    gitignore_text = ""
    if root_gitignore.exists():
        gitignore_path = root_gitignore
        gitignore_text = root_gitignore.read_text(encoding="utf-8", errors="ignore")
    else:
        for p in Path(project).rglob(".gitignore"):
            if ".git" not in p.parts and "node_modules" not in p.parts:
                gitignore_path = p
                gitignore_text = p.read_text(encoding="utf-8", errors="ignore")
                results.append(f"  [WARN] No .gitignore in root, found in subfolder: {p.relative_to(project)}")
                break
        if gitignore_path is None:
            results.append("  [FAIL] No .gitignore found in project.")
            return results
    checks = [".env", "node_modules", "__pycache__", ".git", "dist", "build"]
    for item in checks:
        if item in gitignore_text:
            results.append(f"  [PASS] {item} is in .gitignore")
        else:
            if item == ".env":
                results.append(f"  [FAIL] {item} not in .gitignore")
            elif item == "node_modules":
                results.append(f"  [FAIL] {item} not in .gitignore")
            else:
                results.append(f"  [INFO] {item} not in .gitignore")
    return results

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in check_gitignore_smart(Path(path), {}):
        print(line)