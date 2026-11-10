# secrets_checker.py - CodeLume Bug Hunter - Sirf Secrets ka check
# Kaam: Password / API Key code me to nahi likha hua, ye pakarna
# Ise performance.py bulayega, khud nahi chalega

import re
from utils import safe_read, get_all_code_files

def check_secrets_smart(project):
    """Har code file me hardcoded secret dhoondo."""
    out = []
    found = 0

    for f in get_all_code_files(project):
        # .env.example ko chor do, wo sample hai
        if ".env.example" in str(f):
            continue

        text = safe_read(f)

        # Ye patterns hain jo secret ko pakarte hain
        patterns = [
            (r'API_KEY\s*=\s*["\'][^"\']{8,}["\']', "API_KEY hardcoded hai"),
            (r'api_key\s*=\s*["\'][^"\']{8,}["\']', "api_key hardcoded hai"),
            (r'password\s*=\s*["\'][^"\']{4,}["\']', "password hardcoded hai"),
            (r'SECRET\s*=\s*["\'][^"\']{8,}["\']', "SECRET hardcoded hai"),
            (r'sk-[a-zA-Z0-9]{10,}', "Stripe / OpenAI Secret Key lag rahi hai"),
            (r'ghp_[a-zA-Z0-9]{10,}', "GitHub Token leak ho raha hai"),
        ]

        for pat, msg in patterns:
            if re.search(pat, text):
                out.append(f"  [FAIL] {msg}: {f.relative_to(project)} - Ise .env me rakho, code me nahi")
                found += 1
                break

    if found == 0:
        out.append("  [PASS] Koi hardcoded secret nahi mila. Acha hai.")

    return out