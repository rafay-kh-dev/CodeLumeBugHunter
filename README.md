# CodeLume Bug Hunter

A smart, universal, and stack-aware bug hunter for any project. It detects your tech stack first, then runs only the checks that actually apply to your project.

No more noise. No false positives for stacks you don't use.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Download Software - No Terminal Needed

**Easiest way. For everyone. No Python, no VS Code, no commands.**

### Option 1 - Download EXE (Recommended)

1. Go to [Releases](https://github.com/rafay-kh-dev/codelume-bug-hunter/releases)
2. Download `CodeLume-Bug-Hunter.exe`
3. Double-click to open
4. Click **Browse Folder** > Select your project > Click **Start Scan**
5. See Score, Issues and Full Report inside the software

### Option 2 - Download ZIP

1. Download this repo as ZIP and unzip it
2. Double-click `run.bat`
3. Software will open automatically - no black terminal window

> Everything happens inside the software. You never need to open terminal or VS Code. Scan, processing, issues and report - all in one place.

## How The Software Works

**Step 1 - Choose Your Project**
Click Browse Folder and select your project folder.

**Step 2 - What To Check?**
Tick any category, or leave empty to check everything. CodeLume will auto-skip categories not in your stack.

**Step 3 - Start Scan**
Click Start Scan. Live processing will show inside the software.

**Result - Inside The Software:**

- **Overview Tab** - Score out of 100, Passed / Warning / Failed counts, live processing log
- **Issues Found Tab** - Every issue pointed out with Status, Category, File, Line and Issue. Click any row to see full detail and how to fix it.
- **Full Report Tab** - Complete report inside the software. Open or Copy in one click.

## Why CodeLume?

Most scanners run every check on every project. CodeLume does not.

- **Stack-Aware:** Detects Next.js, React, Vite, Vue, Angular, 【entity-Express¦canonical_name=Express】, Python, PHP, 【entity-MongoDB¦canonical_name=MongoDB】, SQL, and more, then skips checks that are not in your stack.
- **Category-Based:** Scan only what you need - frontend, backend, security, performance, or architecture.
- **Universal:** Works on any project type, from a Next.js website to a Python automation script.
- **Zero Dependencies:** Uses only Python standard library. No install headaches.
- **Professional Reports:** Clean Markdown reports with score, summary table, and skipped reasons.
- **User-Friendly GUI:** Built for beginners. Big buttons, simple steps, no commands to remember.

## Features

- **15 Analyzers:** SQL, Secrets, Gitignore, HTML, Python, PHP, CSS, JSON, Markdown, JS, Images, Backend, Frontend, Architecture, Database
- **Database Checks:** 【entity-MongoDB¦canonical_name=MongoDB】 index check, pagination / limit check, N+1 query detection, lean() check
- **Secrets Detection:** Hardcoded tokens, API keys, passwords - with false-positive filtering for process.env, JWT, and req.headers
- **Frontend Checks:** img vs next/image, missing alt, missing key prop, lazy loading, bundle size
- **Backend Checks:** JWT, CORS, 【entity-MongoDB¦canonical_name=MongoDB】, PORT from environment variables, .env presence
- **Images:** Size check, WebP recommendation, SVG / ICO support
- **Score:** 0-100 score based on PASS / WARN / FAIL
- **GUI:** Overview, Issues Found with file + line pointing, and Full Report viewer - all inside the app

## Installation

### For Software Users

No installation needed. Just download EXE from Releases, or download ZIP and double-click `run.bat`.

### For Developers (CLI)

```bash
git clone https://github.com/rafay-kh-dev/codelume-bug-hunter.git
cd codelume-bug-hunter
```
