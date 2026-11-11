# CodeLume Bug Hunter

A smart, universal, and stack-aware bug hunter for any project. It detects your tech stack first, then runs only the checks that actually apply to your project.

No more noise. No false positives for stacks you don't use.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Why CodeLume?

Most scanners run every check on every project. CodeLume does not.

- **Stack-Aware:** Detects Next.js, React, Vite, Vue, Angular, 【entity-Express¦canonical_name=Express】, Python, PHP, 【entity-MongoDB¦canonical_name=MongoDB】, SQL, and more, then skips checks that are not in your stack.
- **Category-Based:** Scan only what you need - frontend, backend, security, performance, or architecture.
- **Universal:** Works on any project type, from a Next.js website to a Python automation script.
- **Zero Dependencies:** Uses only Python standard library. No install headaches.
- **Professional Reports:** Clean Markdown reports with score, summary table, and skipped reasons.

## Features

- **15 Analyzers:** SQL, Secrets, Gitignore, HTML, Python, PHP, CSS, JSON, Markdown, JS, Images, Backend, Frontend, Architecture, Database
- **Database Checks:** 【entity-MongoDB¦canonical_name=MongoDB】 index check, pagination / limit check, N+1 query detection, `lean()` check
- **Secrets Detection:** Hardcoded tokens, API keys, passwords - with false-positive filtering for `process.env`, JWT, and `req.headers`
- **Frontend Checks:** `<img>` vs `next/image`, missing `alt`, missing `key` prop, lazy loading, bundle size
- **Backend Checks:** JWT, CORS, 【entity-MongoDB¦canonical_name=MongoDB】, PORT from environment variables, `.env` presence
- **Images:** Size check, WebP recommendation, SVG / ICO support
- **Score:** 0-100 score based on PASS / WARN / FAIL

## Installation

```bash
git clone https://github.com/rafay-kh-dev/codelume-bug-hunter.git
cd codelume-bug-hunter
```
