# backend_checker.py - CodeLume Bug Hunter - Sirf Backend ka check
# Kaam: CORS, MongoDB, SQL, JWT Installed vs Used, .env - ye sab pakarna
# Ise performance.py bulayega, khud nahi chalega

import json
from utils import safe_read, get_files_by_ext, get_all_code_files, is_ignored

def check_backend_universal(project):
    """Backend ka pura check - ek jagah."""
    out = []
    all_text = ""
    for f in get_all_code_files(project):
        all_text += safe_read(f) + "\n"

    # JWT - Installed hai ya Used bhi ho raha hai? - SMART
    jwt_installed = False
    for pf in get_files_by_ext(project, ".json"):
        if pf.name == "package.json":
            try:
                data = json.loads(safe_read(pf))
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "jsonwebtoken" in deps:
                    jwt_installed = True
            except:
                pass

    jwt_used = "jsonwebtoken" in all_text or "jwt.verify" in all_text or "JWT_SECRET" in all_text

    if jwt_used:
        out.append("  [PASS] JWT: Use ho raha hai")
    elif jwt_installed and not jwt_used:
        out.append("  [WARN] JWT: Install to hai (package.json me hai), lekin code me use nahi ho raha - Ya to use karo, ya uninstall karo")
    else:
        out.append("  [INFO] JWT: Install bhi nahi, use bhi nahi - Agar login nahi hai to theek hai")

    out.append(f"  CORS: {'[PASS] Mila' if 'cors' in all_text.lower() else '[INFO] Nahi mila / Zaroorat nahi'}")
    out.append(f"  MongoDB: {'[PASS] Mila' if 'mongoose' in all_text or 'MONGO_URI' in all_text else '[INFO] Nahi mila'}")
    out.append(f"  SQL: {'[PASS] .sql files mili' if get_files_by_ext(project, '.sql') else '[INFO] .sql nahi, MongoDB ho sakta hai'}")

    # PORT env check
    if "process.env.PORT" in all_text or "os.environ" in all_text:
        out.append("  [PASS] PORT: .env se aa raha hai")
    else:
        out.append("  [INFO] PORT: .env se nahi mila")

    # .env check - subfolder me bhi dhoondo
    env_files = [str(f.relative_to(project)) for f in project.rglob(".env*") if not is_ignored(f)]
    if env_files:
        out.append(f"  [PASS] .env files: {', '.join(env_files)}")
    else:
        out.append("  [FAIL] .env nahi mili, kisi folder me bhi nahi - MONGO_URI, JWT_SECRET, PORT chahiye")

    return out