from pathlib import Path

def is_ignored(path):
    parts = set(Path(path).parts)
    ignored = {"node_modules", ".next", ".git", "__pycache__", "dist", "build", ".vercel", "coverage", ".idea", ".vscode"}
    if parts & ignored:
        return True
    name = Path(path).name
    if name.startswith(".next"):
        return True
    return False

def get_files_by_ext(project, exts):
    project = Path(project)
    if isinstance(exts, str):
        exts = [exts]
    exts = [e.lower() if e.startswith(".") else f".{e.lower()}" for e in exts]
    result = []
    for f in project.rglob("*"):
        if not f.is_file():
            continue
        try:
            rel = f.relative_to(project)
        except:
            rel = f
        if is_ignored(rel):
            continue
        if f.suffix.lower() in exts:
            result.append(f)
    return result

def get_all_code_files(project):
    exts = [".py", ".js", ".jsx", ".ts", ".tsx", ".php", ".css", ".html", ".json", ".md", ".sql"]
    return get_files_by_ext(project, exts)

def safe_read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

def is_test_file(path):
    p = Path(path)
    name = p.name.lower()
    parts = set(part.lower() for part in p.parts)
    if "test" in parts or "tests" in parts or "__tests__" in parts:
        return True
    if "test" in name or "spec" in name:
        return True
    return False

def is_binary_file(path):
    try:
        return Path(path).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".pdf", ".woff", ".woff2", ".ttf"}
    except:
        return False

def format_size(size_bytes):
    try:
        size = float(size_bytes)
    except:
        return "0 B"
    if size < 1024:
        return f"{size:.0f} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.2f} MB"

def get_file_size_kb(path):
    try:
        return Path(path).stat().st_size / 1024
    except:
        return 0

def get_file_size(path):
    try:
        return Path(path).stat().st_size
    except:
        return 0