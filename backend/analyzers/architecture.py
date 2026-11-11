import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.utils import get_files_by_ext, is_ignored, is_test_file

def check_architecture(project_path):
    print("\n[ARCHITECTURE CHECK]:")
    project = Path(project_path)

    print("  Folder Structure (Top Level):")
    top_folders = []
    for item in project.iterdir():
        if item.is_dir() and not is_ignored(item) and item.name not in [".git", "__pycache__"]:
            top_folders.append(item.name)
    if top_folders:
        for f in sorted(top_folders):
            print(f"    - {f}/")
    else:
        print("    [WARN] Koi folder nahi mila, sab files root me pari hain - structure kharab hai")

    jsx_files = get_files_by_ext(project, [".jsx", ".tsx"])
    pages = [f for f in jsx_files if f.name in ["page.jsx", "page.tsx", "page.js"]]
    vite_pages = [f for f in jsx_files if "pages" in str(f).lower() and not is_test_file(f)]
    
    print(f"\n  Pages: {len(pages) + len(vite_pages)}")
    if pages:
        for p in pages[:10]:
            try:
                rel = p.relative_to(project)
                print(f"    - {rel}")
            except:
                print(f"    - {p.name}")
        if len(pages) > 10:
            print(f"    ... aur {len(pages) - 10} pages hain")
    if vite_pages:
        print(f"    Vite Pages: {len(vite_pages)}")

    components = [f for f in jsx_files if "component" in str(f).lower() and not is_test_file(f)]
    print(f"\n  Components: {len(components)}")
    if len(components) == 0:
        print("    [WARN] Koi components folder nahi mila - Sab code pages me likha hua lagta hai, reuse nahi hoga")
    elif len(components) < 5:
        print("    [WARN] Components bahut kam hain - Code reuse nahi ho raha")
    else:
        print("    [PASS] Components ka structure theek lag raha hai")

    js_files = get_files_by_ext(project, [".js", ".jsx", ".ts", ".tsx"])
    py_files = get_files_by_ext(project, [".py"])
    
    api_files = [f for f in jsx_files + js_files if "/api/" in str(f).replace("\\", "/")]
    express_routes = 0
    for f in js_files:
        if is_test_file(f):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            express_routes += text.count("app.get(") + text.count("app.post(") + text.count("app.put(") + text.count("app.delete(") + text.count("router.get(") + text.count("router.post(")
        except:
            pass
    py_routes = 0
    for f in py_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            py_routes += text.count("@app.route") + text.count("@router")
        except:
            pass

    api_routes = len(api_files) + express_routes + py_routes
    print(f"\n  API / Routes: {api_routes}")
    print(f"    - Next.js API Files: {len(api_files)}")
    print(f"    - Express Routes (app.get/post): {express_routes}")
    print(f"    - Python Routes (@app.route): {py_routes}")
    if api_routes == 0:
        print("    [INFO] Koi API route nahi mili - Agar ye sirf frontend hai to normal hai")

    # 5. Database Models - Mongoose / SQL models
    model_files = [f for f in js_files + py_files if "model" in str(f).lower() or "schema" in str(f).lower()]
    print(f"\n  DB Models / Schemas: {len(model_files)}")
    if model_files:
        for m in model_files[:5]:
            try:
                print(f"    - {m.relative_to(project)}")
            except:
                print(f"    - {m.name}")
    else:
        print("    [INFO] Koi model file nahi mili - Agar MongoDB hai to models folder check karo")

    print("\n  Architecture Summary:")
    if len(pages) + len(vite_pages) > 0 and len(components) >= 5 and len(top_folders) >= 2:
        print("    [PASS] Architecture theek hai - Pages, Components, Folders alag alag hain")
    elif len(top_folders) <= 1:
        print("    [FAIL] Architecture kharab hai - Sab kuch ek hi folder me hai, alag karo")
    else:
        print("    [WARN] Architecture adhi sahi hai - Kuch folders missing hain")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    check_architecture(path)