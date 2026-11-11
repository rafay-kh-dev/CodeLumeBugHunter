from pathlib import Path
from core.utils import safe_read, is_ignored

def check_gitignore_smart(project, counts):
    """Root wali .gitignore ko pehle dekho, phir conditional check karo."""
    out = []

    gitignore = project / ".gitignore"
    if not gitignore.exists():
        all_git = [g for g in project.rglob(".gitignore") if not is_ignored(g)]
        if all_git:
            gitignore = all_git[0]
            out.append(f"  [WARN] Root me .gitignore nahi, subfolder wali mili: {gitignore.relative_to(project)}")
        else:
            out.append("  [FAIL] .gitignore nahi hai - .env 【entity-GitHub¦canonical_name=GitHub】 pe chala jayega!")
            return out
    else:
        out.append(f"  .gitignore mili: {gitignore.relative_to(project)} (Root wali - sahi)")

    text = safe_read(gitignore)

    if ".env" in text:
        out.append("  [PASS] .env .gitignore me hai")
    else:
        out.append("  [FAIL] .env .gitignore me nahi hai - 【entity-GitHub¦canonical_name=GitHub】 pe leak ho jayega")

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