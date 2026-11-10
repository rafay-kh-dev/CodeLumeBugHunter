# sql_checker.py - CodeLume Bug Hunter - Sirf .sql ka check
# Kaam: SQL Database ka kacha chitta nikalna
# Ise performance.py bulayega, khud nahi chalega

from core.utils import safe_read, get_files_by_ext, format_size

def check_sql_smart(project):
    """Sirf .sql files ka check, baaki kuch nahi."""
    out = []
    files = get_files_by_ext(project, ".sql")

    # Agar .sql hai hi nahi, to 【entity-MongoDB¦canonical_name=MongoDB】 ho sakta hai, is liye skip
    if not files:
        return ["  Koi .sql file nahi mili, skip. Agar 【entity-MongoDB¦canonical_name=MongoDB】 hai to ye normal hai."]

    out.append(f"Total SQL Files: {len(files)}")
    total_tables = 0
    total_star = 0

    for f in files:
        text = safe_read(f)
        upper = text.upper()

        tables = upper.count("CREATE TABLE")
        total_tables += tables

        star = text.count("SELECT *") + text.count("select *")
        total_star += star

        out.append(f"  File: {f.relative_to(project)} - Tables: {tables}, Size: {format_size(f.stat().st_size)}")

        if star > 0:
            out.append(f"    [FAIL] SELECT * {star} baar mila - Sirf zaroori columns likho, * slow karta hai")

        # DELETE bina WHERE ke - Sab se khatarnak
        for line in text.split("\n"):
            l = line.strip().upper()
            if l.startswith("DELETE FROM") and "WHERE" not in l:
                out.append(f"    [FAIL] Khatarnak DELETE bina WHERE ke: {line.strip()[:70]} - Poora table delete ho jayega!")
            if l.startswith("DROP TABLE"):
                out.append(f"    [WARN] DROP TABLE mila: {line.strip()[:70]} - Backup le ke hi chalao")

        if "PRIMARY KEY" not in upper and tables > 0:
            out.append(f"    [FAIL] PRIMARY KEY nahi hai - Har table me PRIMARY KEY hona chahiye")

        if "INDEX" not in upper and tables > 0:
            out.append(f"    [WARN] INDEX nahi mila - Bina index ke search slow hoga")

        if "FOREIGN KEY" not in upper and tables > 1:
            out.append(f"    [WARN] FOREIGN KEY nahi mila - Tables ka relation kaise pata chalega?")

    out.append(f"Summary: Total Tables: {total_tables}, Total SELECT *: {total_star}")
    if total_star == 0:
        out.append("  [PASS] SELECT * nahi hai, acha hai.")

    return out