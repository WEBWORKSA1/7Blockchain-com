# 7Blockchain.com

Static, dependency-free website for **7blockchain.com** — "Everything in blockchain, ranked and explained in sevens."
Hosted free on GitHub Pages. Built 2026-10-01.

## Hosting (GitHub Pages, free plan)
1. Settings → Pages → **Source: Deploy from a branch** → Branch **main**, folder **/ (root)** → Save. The site goes live at `https://webworksa1.github.io/7Blockchain-com/` within a minute or two.
2. Custom domain: point DNS first — A records for `7blockchain.com` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `www` CNAME → `webworksa1.github.io`. Then in Settings → Pages enter `7blockchain.com` as the custom domain (GitHub creates the `CNAME` file) and tick **Enforce HTTPS**.
3. Optional CI build: add `.github/workflows/pages.yml` (kept out of this repo because the publishing connector lacks the `workflow` scope; the file is in the project deliverables) and set Settings → Actions → Workflow permissions to "Read and write". It regenerates the site from `_build/` on every push.

## Structure
- `index.html`, `learn/`, `top7/`, `tools/`, `glossary/`, `digest/`, `videos/`, `start/`, `newsletter/`, `support/`, `contests/`, `careers/`, `advertise/`, legal pages — generated HTML (committed, so no build step is needed to host).
- `assets/css/style.css`, `assets/js/app.js` — design system and runtime.
- `assets/js/config.js` — **the only file you need to edit** for AdSense ID, form endpoint, donation addresses, affiliate links, socials, contest.
- `_build/` — Python generator (`python3 _build/build.py`) and content data. Edit data, rebuild, commit.

## Contact pipeline
All forms and contact links route to one address assembled at runtime from `SITE.contactKey`; it never appears in page text or markup. Default transport is the visitor's mail client (`mailto:`); set `SITE.formEndpoint` for server-side delivery.

## Trademark / copyright
See `/trademark/` — independent publication; third-party names used nominatively; no logos hosted.
