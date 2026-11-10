# project_detector.py - CodeLume Bug Hunter - Project ki pehchan
# Kaam: Batana ke ye project Next.js hai, Vite hai, Python hai, PHP hai, SQL hai
# Ise performance.py sab se pehle bulayega

import json
from core.utils import safe_read, get_files_by_ext

ALL_EXTS = [".html", ".py", ".jsx", ".tsx", ".js", ".ts", ".php", ".css", ".json", ".md", ".sql"]

def detect_project_type(project):
    """Project ka type pehchano, file counts bhi do, aur has_next / has_vite bhi do."""
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

    # File se bhi pehchano - next.config hai to Next.js hai
    if list(project.rglob("next.config.*")):
        has_next = True

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