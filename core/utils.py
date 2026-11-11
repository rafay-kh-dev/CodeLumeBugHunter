from pathlib import Path

IGNORE = {"node_modules", ".next", ".git", "__pycache__", ".venv", "venv", "dist", "build"}

def format_size(n):
    """Bytes ko KB / MB me badlo, taake parhne me asan ho."""
    if n > 1024 * 1024:
        return f"{n/(1024*1024):.2f} MB"
    return f"{n/1024:.1f} KB"

def is_ignored(p: Path):
    """Check karo ke ye file ignore wale folder me to nahi hai."""
    for part in p.parts:
        if part in IGNORE:
            return True
    return False

def is_test_file(p: Path):
    """Test wali file hai ya nahi? Test ko bug nahi samajhna."""
    name = p.name.lower()
    return ".test." in name or ".spec." in name or "test_" in name

def safe_read(file: Path):
    """File ko safe tareeqe se parho, agar error aaye to khali string do."""
    try:
        return file.read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

def get_files_by_ext(project: Path, ext: str):
    """Kisi ek type ki sab files dhoondo, misal: .sql, .py, .php"""
    out = []
    for f in project.rglob(f"*{ext}"):
        if not is_ignored(f):
            out.append(f)
    return out

def get_all_code_files(project: Path):
    """Sab code files ek sath - .js .jsx .py .php .html .sql"""
    files = []
    for ext in [".js", ".jsx", ".ts", ".tsx", ".py", ".php", ".html", ".sql"]:
        for f in get_files_by_ext(project, ext):
            if not is_test_file(f):
                files.append(f)
    return files