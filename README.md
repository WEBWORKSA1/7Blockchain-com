# 7Blockchain.com

Static, dependency-free website for **7blockchain.com** — "Everything in blockchain, ranked and explained in sevens."
Hosted free on GitHub Pages. Built 2026-10-01.

## Structure
- `index.html`, `learn/`, `top7/`, `tools/`, `glossary/`, `digest/`, `videos/`, `start/`, `newsletter/`, `support/`, `contests/`, `careers/`, `advertise/`, legal pages — generated HTML.
- `assets/css/style.css`, `assets/js/app.js` — design system and runtime.
- `assets/js/config.js` — **the only file you need to edit** for AdSense ID, form endpoint, donation addresses, affiliate links, socials, contest.
- `_build/` — Python generator (`python3 _build/build.py`) and content data. Edit data, rebuild, commit.
- `.github/workflows/pages.yml` — deploys to GitHub Pages on every push (enables Pages automatically).

## Contact pipeline
All forms and contact links route to one address assembled at runtime from `SITE.contactKey`; it never appears in page text or markup. Default transport is the visitor's mail client (`mailto:`); set `SITE.formEndpoint` for server-side delivery.

## Custom domain
`CNAME` is set to `7blockchain.com`. Point DNS: A records → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `www` CNAME → `webworksa1.github.io`. Then enable "Enforce HTTPS" in Settings → Pages.

## Trademark / copyright
See `/trademark/` — independent publication; third-party names used nominatively; no logos hosted.
