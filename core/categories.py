CATEGORIES = {
    "frontend": ["HTML", "CSS", "JS", "Images", "Frontend"],
    "backend": ["Backend", "SQL", "JSON", "Database"],
    "security": ["Secrets", "Gitignore", "Backend"],
    "performance": ["Images", "Frontend", "CSS", "JS"],
    "architecture": ["Architecture", "Frontend", "Backend"],
    "python": ["Python"],
    "php": ["PHP"],
    "quality": ["Python", "PHP", "Markdown", "JSON", "Gitignore"],
    "all": ["SQL", "Secrets", "Gitignore", "HTML", "Python", "PHP", "CSS", "JSON", "Markdown", "JS", "Images", "Backend", "Frontend", "Architecture", "Database"],
}

def get_categories_for_only(only):
    if not only:
        return None
    if isinstance(only, str):
        only = [x.strip().lower() for x in only.split(",") if x.strip()]
    allowed = []
    for name in only:
        if name in CATEGORIES:
            for cat in CATEGORIES[name]:
                if cat not in allowed:
                    allowed.append(cat)
        elif name:
            allowed.append(name.capitalize())
    return allowed

def filter_results(results, only):
    allowed = get_categories_for_only(only)
    if not allowed:
        return results
    return {k: v for k, v in results.items() if k in allowed}

def is_category_applicable(category, project_type, file_counts):
    type_text = " ".join([str(t) for t in project_type]).lower()
    has_py = file_counts.get(".py", 0) > 0
    has_php = file_counts.get(".php", 0) > 0
    has_sql = file_counts.get(".sql", 0) > 0
    has_js = file_counts.get(".js", 0) + file_counts.get(".jsx", 0) + file_counts.get(".ts", 0) + file_counts.get(".tsx", 0) > 0
    has_html = file_counts.get(".html", 0) > 0
    has_css = file_counts.get(".css", 0) > 0
    has_images = file_counts.get(".png", 0) + file_counts.get(".jpg", 0) + file_counts.get(".jpeg", 0) + file_counts.get(".webp", 0) + file_counts.get(".svg", 0) + file_counts.get(".ico", 0) > 0
    has_frontend_stack = "next.js" in type_text or "react" in type_text or "vue" in type_text or "angular" in type_text or "vite" in type_text or has_js or has_html
    has_backend_stack = "express" in type_text or "next.js" in type_text or has_py or has_php or has_sql
    if category == "Python":
        if has_py:
            return True, ""
        return False, "No Python files found in tech stack"
    if category == "PHP":
        if has_php:
            return True, ""
        return False, "No PHP files found in tech stack"
    if category == "SQL":
        if has_sql:
            return True, ""
        return False, "No SQL files found in tech stack"
    if category in ["HTML", "CSS", "JS", "Frontend"]:
        if has_frontend_stack:
            return True, ""
        return False, "No frontend detected in tech stack"
    if category == "Images":
        if has_images or has_frontend_stack:
            return True, ""
        return False, "No images or frontend found in tech stack"
    if category == "Backend":
        if has_backend_stack:
            return True, ""
        return False, "No backend detected in tech stack"
    if category == "Database":
        if has_backend_stack or has_sql:
            return True, ""
        return False, "No database usage detected in tech stack"
    return True, ""

def filter_by_stack(categories_list, project_type, file_counts):
    applicable = []
    skipped = []
    for cat in categories_list:
        ok, reason = is_category_applicable(cat, project_type, file_counts)
        if ok:
            applicable.append(cat)
        else:
            skipped.append((cat, reason))
    return applicable, skipped