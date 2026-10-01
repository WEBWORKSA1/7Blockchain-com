# 7Blockchain.com — Concept Decision + Phase-wise Build Prompt

Prepared 2026-10-01 for Web (Webworks). Based on a teardown of 37 niche sites (Binance Academy, Coinbase Learn, Kraken Learn, Investopedia, Bybit Learn, Ledger Academy, ethereum.org, Blockchain Council, 101 Blockchains, Gemini Cryptopedia, Moralis/Bullmania, Cointelegraph, CoinDesk, Decrypt, The Block, CoinMarketCap, CoinGecko, CryptoSlate, BeInCrypto, Cryptonews, Bitcoin Magazine, DL News, Messari, NerdWallet, Forbes Advisor, Bankrate, CryptoPotato, Coin Bureau, Milk Road, BitDegree, CryptoJobsList, Web3.career, Gitcoin, DropsTab/CoinCarp, Alchemy Dapps, Bankless).

---

## 1. The idea (position taken)

**7Blockchain.com = "Everything in blockchain, ranked and explained in sevens."**
An independent blockchain intelligence hub where every content unit is a 7:

| Format | What it is | Why it monetizes |
|---|---|---|
| **Top 7 rankings** | Exchanges, wallets, Layer-1s, Layer-2s, DeFi platforms, crypto cards, tax tools — sortable scorecards with a 7-metric methodology | Affiliate CPA ($20–$150 per exchange/wallet signup), "Promoted" paid placements, sponsor-of-the-list |
| **7-Step learning path** | Beginner → confident in 7 chapters with progress, quizzes, downloadable Starter Kit | Lead magnet (email), AdSense on high-dwell pages, course/affiliate upsell |
| **7-in-7 digest** | 7 stories in 7 minutes, weekly | Newsletter = owned audience, sponsor slot per issue |
| **Tools** | DCA, staking yield, fee comparison, profit/loss, glossary, 7-question quiz | SEO magnets, calculators have highest RPM dwell time |
| **Videos** | YouTube hub + embedded playlists | YouTube revenue + watch-time, cross-channel subscribers |

**Why this beats the alternatives considered**
- Exchange academies can't recommend rivals → independent comparisons are a gap.
- Cert sites hard-sell; news sites burn cash on staff. A ranking+tools hub is a 1-person-operable asset.
- None of the 37 sites own a memorable format. "7" is a brandable content constraint (like "Milk Road" owns the newsletter voice).
- Crypto/finance is a top-3 AdSense RPM vertical; affiliate CPA is the highest in consumer web.

**Revenue stack (ordered by expected contribution at 100k monthly visits)**
1. Affiliate (exchanges, hardware wallets, tax software, cards) — 50–65%
2. Sponsored "Promoted" placements + list sponsorship + digest sponsor — 15–25%
3. Google AdSense (leaderboard, in-content, sticky sidebar, anchor) — 10–20%
4. YouTube (embedded channel + ad share) — 3–8%
5. Donations/supporter tiers, contest sponsors, job-post fees — 2–5%

---

## 2. Trademark / copyright position

- Use the domain-form brand **"7Blockchain.com"** everywhere, never "Seven Blockchain Inc." or a stylised lock-up that mimics any registered mark. "Blockchain" is a generic, descriptive term; "7" is a numeral. The combination is used descriptively (seven-item format).
- Every page carries a **Trademark & Copyright Disclosure** (dedicated page + footer line): independent publication, not affiliated with, endorsed by, or sponsored by any entity using "7", "Seven", "Blockchain" or "7 Blockchain" in its name; all third-party names/logos belong to their owners and are used nominatively for identification/comparison; original content © 7Blockchain.com; DMCA contact via the contact form.
- No third-party logos are hosted; brands are referenced by text only.

---

## 3. Phase-wise build prompt (copy/paste per phase into any builder)

### Phase 0 — Constraints (prepend to every phase)
```
Build a static website for the domain 7Blockchain.com that runs on GitHub Pages free plan
(no server, no build step at deploy time, no database). Pure HTML5 + CSS3 + vanilla JS.
Mobile-first, responsive, dark/light theme, WCAG AA. Every page must:
1. Show a top bar: "Contact, if you are interested in this website / domain name / Sponsorship /
   Advertisement / Partnership" linking to https://web.works/contact.
2. Route ALL contact/inquiry/form submissions to one email, webworksa1@gmail.com, which must NEVER
   appear in visible text or plain HTML source. Assemble it at runtime from obfuscated parts and
   attach it to links/forms via JS (mailto: with pre-filled subject/body), with an optional form
   endpoint upgrade (FormSubmit/Formspree) set in a single config file.
3. Include Google AdSense slot placeholders (leaderboard, in-content, sidebar sticky, anchor) gated by
   a config value so nothing errors until the publisher ID is set; ship ads.txt placeholder.
4. Include YouTube embed facades (click-to-load for speed).
5. Carry the trademark/copyright disclosure line in the footer linking to /trademark/.
6. Be generated from a single Python generator (_build/build.py) with shared layout so adding a page
   or a Top-7 list is a data change, not a markup change.
```

### Phase 1 — Brand, design system, layout shell
```
Create the design system: Inter font, dark-first palette (ink #0b0f1a, gold accent #f5b400, violet
#7c5cff), 8px spacing scale, 16px mobile gutters, cards with 14px radius, sticky header with
mega-nav (Learn, Top 7, Tools, Digest, Videos, Support, Advertise), theme toggle, search box that
filters the site index JSON, live crypto ticker (CoinGecko public API, 8 coins, 24h %), Fear & Greed
widget (alternative.me API). Footer: 6 columns (Learn, Compare, Tools, Company, Monetize/Partner,
Legal), socials, newsletter box, disclosure line. Build /404.html, robots.txt, sitemap.xml, CNAME
(7blockchain.com), manifest.json, favicon as inline SVG "7".
```

### Phase 2 — Core content engine
```
Implement data-driven pages:
- /learn/ hub + /learn/step-1..7/ (7-chapter path: What is a blockchain; Bitcoin; Ethereum & smart
  contracts; Wallets & self-custody; Exchanges & buying safely; DeFi, NFTs & L2s; Security, taxes &
  7 rules). Each chapter: key takeaways (7 bullets), 6–9 min read, sticky TOC, FAQ, "next step"
  progress bar, mid-article newsletter box, end-of-article CTA.
- /top7/ hub + 7 ranking pages from data/top7/*.json: rank, name, 7-metric score (/10), badge
  (Best overall / Best for beginners / Lowest fees / Best for US / Most regulated / Editor's choice /
  Promoted), pros/cons, "Choose if / Skip if", dual CTA (Visit = affiliate link via /go/ redirect
  map; Read details), sortable table, advertiser disclosure box top and bottom, FAQ schema.
- /glossary/ with 100+ terms, A–Z jump, live filter.
- /digest/ hub + issue template "7 in 7" with sponsor slot.
- /videos/ hub from data/videos.json.
```

### Phase 3 — Tools (SEO + dwell time)
```
Build client-side tools under /tools/: DCA calculator (live price via API, optional), staking yield
calculator (APY compounding), exchange fee comparison (uses top7 data), profit/loss calculator,
7-question crypto quiz with score + share + email capture of result. Each tool page: H1, tool,
explanation, FAQ, related Top-7 links, ad slot below the fold.
```

### Phase 4 — Lead generation (dedicated, high-conversion)
```
Build /start/ "Find your 7-step starter kit": 3-question wizard (country, experience, goal) →
personalised recommendations (exchange, wallet, first chapter) + email capture to receive the
Starter Kit PDF. Also: newsletter boxes in 4 placements (hero, mid-article, end-of-article,
footer), exit-intent slide-in (once per session, dismissible), sticky mobile bar CTA. All forms
submit via the single contact pipeline; store nothing client-side except a "subscribed" flag.
Build /newsletter/ landing page with sample issue, subscriber-count placeholder, 3 benefits.
```

### Phase 5 — Monetization & operations pages
```
- /advertise/: 7 sponsorship packages (list sponsor, Promoted placement, digest sponsor, video
  integration, homepage takeover, tool sponsor, custom), media kit stats placeholders, booking form.
- /support/ (donations): crypto address grid with QR (BTC, ETH, SOL, USDC) as config placeholders,
  Buy Me a Coffee / PayPal / GitHub Sponsors links, funding goal progress bar, "what this funds" (ops,
  promotion, hiring, prizes), supporter tiers ($5 badge, $20 name in footer, $100 early access).
- /contests/: live contest card (prize, deadline countdown, rules), entry form, past winners list,
  sponsor-a-prize CTA.
- /careers/: open roles, writer bounty program (paid per published piece), ambassador program,
  application form with portfolio link.
- /partners/ merged into /advertise/ with partnership inquiry type.
- /about/, /contact/ (inquiry-type selector), /editorial-policy/, /how-we-rank/,
  /affiliate-disclosure/, /privacy/, /terms/, /disclaimer/, /trademark/.
```

### Phase 6 — Performance, SEO, compliance
```
Inline critical CSS; lazy-load images/embeds; preconnect to APIs; Open Graph + Twitter cards;
JSON-LD (WebSite, Organization, Article, FAQPage, ItemList for Top-7); canonical URLs on
https://7blockchain.com; sitemap.xml; cookie/consent notice (AdSense EU requirement); "Not
financial advice" risk disclaimer; "Updated <date>" stamps; Lighthouse ≥ 90 on all four scores.
```

### Phase 7 — Deploy & grow
```
Push to github.com/webworksa1/7Blockchain-com (main). Add .github/workflows/pages.yml using
actions/configure-pages (enablement: true), actions/upload-pages-artifact, actions/deploy-pages so
Pages is enabled and deployed automatically on every push. Add CNAME. After first deploy: point
7blockchain.com A records to GitHub Pages IPs (185.199.108–111.153) and www CNAME to
webworksa1.github.io, enforce HTTPS. Growth loop: publish 1 Top-7 refresh/week, 1 digest/week,
1 tool/month; every ranking links to deals, every chapter links to a ranking and a tool.
```

---

## 4. Post-launch checklist for Web (things only you can set)
1. `assets/js/config.js`: AdSense publisher ID, YouTube channel ID, form endpoint (optional), donation addresses/links, affiliate URLs in `go` map, social handles.
2. Replace `ads.txt` placeholder line with your AdSense line.
3. DNS as in Phase 7; then tick "Enforce HTTPS" in repo Settings → Pages.
4. Apply for AdSense only after ~20 indexed pages (already shipped: 45+).
5. Register exchange/wallet affiliate programs (Binance, Coinbase, Kraken, Ledger, Trezor, Koinly, CoinLedger) and paste links into the `go` map.
