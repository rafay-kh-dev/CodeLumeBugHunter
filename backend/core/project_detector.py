import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext, safe_read

def detect_project_type(project):
    types = []
    package_files = [f for f in get_files_by_ext(project, [".json"]) if f.name == "package.json"]
    combined_pkg = ""
    for f in package_files:
        try:
            combined_pkg += safe_read(f) + "\n"
        except:
            pass
    if '"next"' in combined_pkg:
        types.append("Next.js Project - Use next/image for optimized images")
    elif '"react"' in combined_pkg:
        if '"vite"' in combined_pkg:
            types.append("React + Vite Project - Use optimized images and code splitting")
        else:
            types.append("React Project - Use optimized images and code splitting")
    if '"【entity-express¦canonical_name=Express】"' in combined_pkg:
        types.append("【entity-Express¦canonical_name=Express】 Backend - Check routes, auth, and environment variables")
    if '"vue"' in combined_pkg:
        types.append("Vue Project - Use optimized images and lazy loading")
    if '"@angular/core"' in combined_pkg:
        types.append("Angular Project - Use optimized images and lazy loading")
    py_files = get_files_by_ext(project, [".py"])
    py_files = [f for f in py_files if f.suffix == ".py"]
    if py_files:
        types.append(f"Python Project - {len(py_files)} files - Automation or backend scripts")
    php_files = get_files_by_ext(project, [".php"])
    php_files = [f for f in php_files if f.suffix == ".php"]
    if php_files:
        types.append(f"PHP Project - {len(php_files)} files - Check sanitization and SQL injection")
    if not types:
        types.append("General Project - Mixed file types detected")
    return types

detect_project = detect_project_type
get_project_type = detect_project_type
detect_project_types = detect_project_type

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    for line in detect_project_type(Path(path)):
        print(line)