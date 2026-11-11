# CodeLume Bug Hunter

A smart, universal, and stack-aware bug hunter for any project. It detects your tech stack first, then runs only the checks that actually apply to your project.

No more noise. No false positives for stacks you don't use.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Why CodeLume?

Most scanners run every check on every project. CodeLume does not.

- **Stack-Aware:** Detects Next.js, React, Vite, Vue, Angular, Express, Python, PHP, MongoDB, SQL, and more, then skips checks that are not in your stack.
- **Category-Based:** Scan only what you need - frontend, backend, security, performance, or architecture.
- **Universal:** Works on any project type, from a Next.js website to a Python automation script.
- **Zero Dependencies:** Uses only Python standard library. No install headaches.
- **Professional Reports:** Clean Markdown reports with score, summary table, and skipped reasons.

## Features

- **15 Analyzers:** SQL, Secrets, Gitignore, HTML, Python, PHP, CSS, JSON, Markdown, JS, Images, Backend, Frontend, Architecture, Database
- **Database Checks:** MongoDB index check, pagination / limit check, N+1 query detection, lean() check
- **Secrets Detection:** Hardcoded tokens, API keys, passwords - with false-positive filtering for process.env, JWT, and req.headers
- **Frontend Checks:** img vs next/image, missing alt, missing key prop, lazy loading, bundle size
- **Backend Checks:** JWT, CORS, MongoDB, PORT from environment variables, .env presence
- **Images:** Size check, WebP recommendation, SVG / ICO support
- **Score:** 0-100 score based on PASS / WARN / FAIL

## Installation

```bash
git clone https://github.com/rafay-kh-dev/codelume-bug-hunter.git
cd codelume-bug-hunter
```

Requires Python 3.9 or higher. No external packages required.

## Usage

### Full Scan

```bash
py codelume.py "C:\\MyProject"
```

### Scan Only One Category

```bash
py codelume.py "C:\\MyProject" --only frontend
py codelume.py "C:\\MyProject" --only backend
py codelume.py "C:\\MyProject" --only security
py codelume.py "C:\\MyProject" --only performance
py codelume.py "C:\\MyProject" --only frontend,backend
```

### Interactive Menu

```bash
py codelume.py "C:\\MyProject" --menu
```

### List All Categories

```bash
py codelume.py "C:\\MyProject" --list
```

### Custom Report Name

```bash
py codelume.py "C:\\MyProject" --only frontend --output my-frontend-report.md
```

Default report name is:

```
codelume-report-<project>-<date>.md
```

Example:

```
codelume-report-codelume-2026-11-11.md
```

## Categories

| Category     | What It Checks                         |
| ------------ | -------------------------------------- |
| frontend     | HTML, CSS, JS, Images, Frontend        |
| backend      | Backend, SQL, JSON, Database           |
| security     | Secrets, Gitignore, Backend            |
| performance  | Images, Frontend, CSS, JS              |
| architecture | Architecture, Frontend, Backend        |
| python       | Python                                 |
| php          | PHP                                    |
| quality      | Python, PHP, Markdown, JSON, Gitignore |
| all          | All analyzers                          |

## Stack-Aware Filtering

CodeLume checks your tech stack before running a category.

Example - Backend scan on a Next.js + MongoDB project:

```
Categories: backend
Skipped - Not in Tech Stack:
  - SQL: No SQL files found in tech stack
```

If you run --only php on a project with no PHP files:

```
No applicable categories found for this tech stack.
```

You will never see PHP results on a Python project, or SQL results on a MongoDB project.

## Example Report

```markdown
# CodeLume - Project Report

**Project:** C:\\CodeLume
**Score:** 81 / 100 - Good
**Categories:** backend

## Summary

| Category | PASS | WARN | FAIL |
| -------- | ---- | ---- | ---- |
| JSON     | 0    | 0    | 0    |
| Backend  | 4    | 0    | 1    |
| Database | 2    | 1    | 0    |

## Skipped - Not in Tech Stack

- SQL: No SQL files found in tech stack
```

## Project Structure

```
codelume-bug-hunter/
├── codelume.py              # Entry point
├── engine.py                # Report builder + category system
├── core/
│   ├── categories.py        # Category definitions + stack filter
│   ├── project_detector.py  # Tech stack detection
│   └── utils.py             # Shared helpers
├── analyzers/
│   ├── sql.py
│   ├── secrets.py
│   ├── gitignore.py
│   ├── html.py
│   ├── python.py
│   ├── php.py
│   ├── css.py
│   ├── json.py
│   ├── markdown.py
│   ├── js.py
│   ├── images.py
│   ├── backend.py
│   ├── frontend.py
│   ├── architecture.py
│   └── database.py
└── README.md
```

## Roadmap

- [x] Stack-aware category system
- [x] Database analyzer (MongoDB + SQL)
- [x] Smart secrets detection
- [x] Professional Markdown reports
- [ ] VS Code extension with right-click categories
- [ ] Auto-fix mode
- [ ] HTML report export

## Contributing

Pull requests are welcome. Keep the code clean, professional, and dependency-free.

## License

MIT License. See LICENSE for details.

---

Built with CodeLume Bug Hunter.
