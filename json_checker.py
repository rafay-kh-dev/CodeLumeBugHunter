# json_checker.py - CodeLume Bug Hunter - Sirf JSON + Tech Stack ka check
# Kaam: Toota JSON pakarna, aur package.json se Tech Stack nikalna
# Ise performance.py bulayega, khud nahi chalega

import json
from utils import safe_read, get_files_by_ext

def check_json_smart(project):
    """Sirf .json files ka check, baaki kuch nahi."""
    out = []
    files = get_files_by_ext(project, ".json")

    if not files:
        return ["  Koi .json file nahi mili, skip."]

    out.append(f"Total JSON Files: {len(files)}")

    for f in files:
        # package-lock ko chor do, wo bohot lambi hoti hai
        if "package-lock" in f.name:
            continue

        text = safe_read(f)

        try:
            data = json.loads(text)
        except:
            out.append(f"  [FAIL] Toota hua JSON: {f.relative_to(project)} - JSON syntax check karo, kahin comma ya bracket missing hai")
            continue

        # Agar ye package.json hai to Tech Stack nikalo
        if f.name == "package.json":
            deps = {}
            deps.update(data.get("dependencies", {}))
            deps.update(data.get("devDependencies", {}))
            if deps:
                out.append(f"  Tech Stack ({f.relative_to(project)}): {', '.join(list(deps.keys())[:6])} ... Total {len(deps)} deps")
            else:
                out.append(f"  [WARN] package.json khali hai: {f.relative_to(project)}")

        # JSON me secret to nahi
        if "password" in text.lower() or "secret" in text.lower():
            if "example" not in f.name.lower():
                out.append(f"  [WARN] JSON me secret lag raha hai: {f.relative_to(project)} - Secret .env me rakho")

    return out