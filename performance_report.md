# CodeLume Bug Hunter - V5
Project: C:\Jasa Backlinks

## Project Type
- Vite + React Project - normal <img> + loading=lazy use hoga

## SQL
  Koi .sql file nahi mili, skip. Agar MongoDB hai to ye normal hai.

## Secrets
  [PASS] Koi hardcoded secret nahi mila. Acha hai.

## Gitignore
  .gitignore mili: .gitignore
  [PASS] .env .gitignore me hai
  [PASS] node_modules .gitignore me hai
  [FAIL] __pycache__ .gitignore me nahi hai - Is ko add karo warna leak ho jayega

## HTML
HTML Files: 1, JSX/TSX Files: 19
  [PASS] Sab <img> me alt hai, accessibility theek hai.
  Project Vite / HTML hai, is liye <img loading='lazy'> use karo, next/image nahi.

## Python
  Koi .py nahi, skip.

## PHP
  Koi .php nahi, skip.

## CSS
Total CSS Files: 2
Unique Colors: 1, !important: 0

## JSON
Total JSON Files: 11
  Tech Stack (backend\package.json): axios, cors, dotenv, express, express-rate-limit, helmet ... Total 12
  Tech Stack (frontend\package.json): @paypal/react-paypal-js, @stripe/react-stripe-js, @stripe/stripe-js, @tailwindcss/vite, axios, react ... Total 20

## JS
Total JS Files (test chor ke): 50
  [INFO] <img> mila: frontend\src\components\FloatingContactWidget.jsx - 1 baar - loading='lazy' + width/height lagao
  [INFO] <img> mila: frontend\src\components\Footer.jsx - 1 baar - loading='lazy' + width/height lagao
  [INFO] <img> mila: frontend\src\components\Header.jsx - 4 baar - loading='lazy' + width/height lagao
  [INFO] <img> mila: frontend\src\components\PageLoader.jsx - 1 baar - loading='lazy' + width/height lagao
  [INFO] <img> mila: frontend\src\pages\AdminBlog.jsx - 6 baar - loading='lazy' + width/height lagao
  [INFO] <img> mila: frontend\src\pages\Blog.jsx - 4 baar - loading='lazy' + width/height lagao
  [INFO] <img> mila: frontend\src\pages\BlogPost.jsx - 3 baar - loading='lazy' + width/height lagao
  [INFO] <img> mila: frontend\src\pages\Home.jsx - 8 baar - loading='lazy' + width/height lagao
  [INFO] <img> mila: frontend\src\pages\Services.jsx - 1 baar - loading='lazy' + width/height lagao
Summary: <img>: 29, console.log: 12 [WARN] Zyada hai

## Images
Total Images: 3, Total: 453.6 KB
  [WARN] screenshot.png - 399.1 KB - frontend\public\screenshot.png
  [OK] SeoHubLogo.png - 41.8 KB - frontend\public\SeoHubLogo.png
  [OK] hero.png - 12.8 KB - frontend\src\assets\hero.png

## Backend
  CORS: [PASS]
  MongoDB: [PASS]
  SQL: [INFO] .sql nahi, MongoDB ho sakta hai
  JWT: [WARN] Nahi mila
  [PASS] .env: backend\.env, frontend\.env