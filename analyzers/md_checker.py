from core.utils import get_files_by_ext

def check_md_smart(project):
    """Sirf .md files ka check."""
    out = []
    files = get_files_by_ext(project, ".md")

    out.append(f"Total MD Files: {len(files)}")

    if (project / "README.md").exists():
        out.append("  [PASS] README.md hai, acha hai.")
    else:
        out.append("  [WARN] README.md nahi hai - Project ka README banao, taake naye bande ko samajh aaye")

    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            if len(text) < 200 and f.name.lower() == "readme.md":
                out.append(f"  [WARN] README bohot choti hai: {f.relative_to(project)} - Poora guide likho")
        except:
            pass

    return out