# CodeLume Bug Hunter - Professional Modular Report
Project: C:\CodeLume

## Project Type
- Next.js Project - next/image use hoga
- Python Project - 6 files - automation ya backend

## File Counts
- .py: 6
- .jsx: 68
- .js: 8
- .css: 1
- .json: 5
- .md: 2

## SQL
  Koi .sql file nahi mili, skip. Agar 【entity-MongoDB¦canonical_name=MongoDB】 hai to ye normal hai.

## Secrets
  [PASS] Koi hardcoded secret nahi mila. Acha hai.

## Gitignore
  [WARN] Root me .gitignore nahi, subfolder wali mili: codelume-automation\.gitignore
  [PASS] .env .gitignore me hai
  [FAIL] node_modules .gitignore me nahi hai
  [PASS] __pycache__ .gitignore me hai

## HTML
HTML Files: 0, JSX/TSX Files: 68
  [PASS] Sab <img> me alt hai, accessibility theek hai.
  Project Next.js hai, is liye <img> ki jagah <Image> use karo.

## Python
Total Python Files: 6
  [WARN] print() zyada hai: codelume-automation\auto_index_gsc.py - logging use karo, print production me nahi
  [WARN] Khali except hai: codelume-automation\filter_hot.py - except Exception as e likho, warna error chup jayega
  [WARN] print() zyada hai: codelume-automation\indexing_automation.py - logging use karo, print production me nahi
  [WARN] Khali except hai: codelume-automation\uk_email_finder.py - except Exception as e likho, warna error chup jayega
  [WARN] print() zyada hai: codelume-automation\uk_maps_scraper.py - logging use karo, print production me nahi
  [WARN] Khali except hai: codelume-automation\uk_maps_scraper.py - except Exception as e likho, warna error chup jayega
  [WARN] print() zyada hai: codelume-automation\uk_sender.py - logging use karo, print production me nahi
  [WARN] Khali except hai: codelume-automation\uk_sender.py - except Exception as e likho, warna error chup jayega

## PHP
  Koi .php file nahi mili, skip.

## CSS
Total CSS Files: 1
Unique Colors in CSS: 3
  [PASS] Colors theek hain, sirf 3 unique colors hain
!important count: 3
  [PASS] !important theek hai

## JSON
Total JSON Files: 5
  Tech Stack (codelume-backend\package.json): cloudinary, cors, dotenv, express, jsonwebtoken, mongoose ... Total 9 deps
  Tech Stack (codelume-frontend\package.json): @emailjs/browser, @thesvg/react, dompurify, framer-motion, lucide-react, motion-dom ... Total 19 deps

## Markdown
Total MD Files: 2
  [PASS] README.md hai, acha hai.

## JS
Total JS Files (test chor ke): 76
  [FAIL] <img> mila: codelume-frontend\src\components\MeetRafay.jsx - 1 baar - next/image use karo
  [FAIL] <img> mila: codelume-frontend\src\app\about\page.jsx - 1 baar - next/image use karo
  [FAIL] <img> mila: codelume-frontend\src\app\blogs\page.jsx - 3 baar - next/image use karo
  [FAIL] <img> mila: codelume-frontend\src\app\tools\meta-extractor\page.jsx - 1 baar - next/image use karo
  [FAIL] <img> mila: codelume-frontend\src\app\blogs\[slug]\ClientArticle.jsx - 2 baar - next/image use karo
  [FAIL] <img> mila: codelume-frontend\src\app\admin\create-post\page.jsx - 2 baar - next/image use karo
  [FAIL] <img> mila: codelume-frontend\src\app\admin\dashboard\page.jsx - 2 baar - next/image use karo
  [FAIL] <img> mila: codelume-frontend\src\app\admin\edit-post\[id]\page.jsx - 1 baar - next/image use karo
Summary: <img>: 13, console.log: 4

## Images
Total Images: 3, Total Size: 1.18 MB
  [FAIL] screenshot.png - 772.3 KB - codelume-frontend\public\screenshot.png
       Fix: 200KB se kam karo, WebP me badlo.
  [WARN] rafay-profile.webp - 257.8 KB - codelume-frontend\public\rafay-profile.webp
  [OK] preview.png - 176.6 KB - codelume-frontend\public\preview.png

## Backend
  [WARN] JWT: Install to hai (package.json me hai), lekin code me use nahi ho raha - Ya to use karo, ya uninstall karo
  CORS: [PASS] Mila
  MongoDB: [PASS] Mila
  SQL: [INFO] .sql nahi, MongoDB ho sakta hai
  [PASS] PORT: .env se aa raha hai
  [PASS] .env files: codelume-backend\.env, codelume-frontend\.env