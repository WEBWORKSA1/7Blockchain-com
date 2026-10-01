import json, html

SITE_URL = "https://7blockchain.com"
SITE_NAME = "7Blockchain.com"
TAGLINE = "Everything in blockchain, ranked and explained in sevens."

NAV = [("Learn", "learn/"), ("Top 7", "top7/"), ("Tools", "tools/"), ("Digest", "digest/"), ("Videos", "videos/"), ("Support us", "support/"), ("Advertise", "advertise/")]

FOOTER = {
 "Learn": [("7-Step Path", "learn/"), ("Step 1: What is a blockchain?", "learn/step-1/"), ("Step 4: Wallets & self-custody", "learn/step-4/"), ("Glossary", "glossary/"), ("Videos", "videos/"), ("7-in-7 Digest", "digest/")],
 "Top 7 Rankings": [("Exchanges", "top7/exchanges/"), ("Wallets", "top7/wallets/"), ("Layer-1 blockchains", "top7/layer-1/"), ("Layer-2 networks", "top7/layer-2/"), ("DeFi platforms", "top7/defi/"), ("Crypto cards", "top7/cards/"), ("Tax tools", "top7/tax-tools/")],
 "Tools": [("DCA calculator", "tools/dca-calculator/"), ("Staking calculator", "tools/staking-calculator/"), ("Fee comparison", "tools/fee-comparison/"), ("Profit / loss", "tools/profit-calculator/"), ("Converter", "tools/converter/"), ("7-question quiz", "tools/quiz/"), ("Starter Kit wizard", "start/")],
 "Company": [("About", "about/"), ("Contact", "contact/"), ("Careers & bounties", "careers/"), ("Contests", "contests/"), ("Newsletter", "newsletter/"), ("Support us", "support/")],
 "Partner": [("Advertise & sponsor", "advertise/"), ("Partnerships", "advertise/#partnership"), ("How we rank", "how-we-rank/"), ("Editorial policy", "editorial-policy/"), ("Affiliate disclosure", "affiliate-disclosure/")],
 "Legal": [("Privacy", "privacy/"), ("Terms", "terms/"), ("Risk disclaimer", "disclaimer/"), ("Trademark & copyright", "trademark/")],
}

def esc(s): return html.escape(str(s), quote=True)

def ad(kind="leader", slot="leader"):
    label = {"leader": "Advertisement · 970×90 / responsive", "rect": "Advertisement · 300×250", "sky": "Advertisement · 300×600"}[kind]
    return f'<div class="ad {kind}" data-slot="{slot}" aria-label="advertisement">{label}</div>'

def newsletter_box(R, variant="inline", title="Get the 7-in-7 Digest", text="Seven stories, seven minutes, every week. Plus the free 7-Step Starter Kit PDF."):
    return f'''<div class="lead"><h3>{esc(title)}</h3><p class="muted">{esc(text)}</p>
<form class="form" data-form="Newsletter signup ({variant})"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
<div class="inline-sub"><input type="email" name="email" placeholder="you@example.com" required aria-label="Email address"><button class="btn primary" type="submit">Subscribe free</button></div>
<div class="note">No spam. Unsubscribe any time. By subscribing you agree to the <a href="{R}privacy/">privacy policy</a>.</div><div class="ok">Thanks — check your inbox to confirm.</div></form></div>'''

def yt(v):
    return f'<div class="vcard"><div class="yt" data-id="{v["id"]}" role="button" tabindex="0" aria-label="Play {esc(v["title"])}"><div class="play"><i>▶</i></div></div><h3>{esc(v["title"])}</h3><div class="small muted">{esc(v["by"])}</div></div>'

def faq_block(faqs):
    if not faqs: return ""
    items = "".join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in faqs)
    return f'<section class="faq" id="faq"><h2>Frequently asked questions</h2>{items}</section>'

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def page(R, path, title, desc, body, ld=None, kind="website", extra_head="", sticky_cta=True):
    url = SITE_URL + "/" + path
    ldj = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": SITE_URL, "potentialAction": {"@type": "SearchAction", "target": SITE_URL + "/?q={search_term_string}", "query-input": "required name=search_term_string"}},
           {"@context": "https://schema.org", "@type": "Organization", "name": SITE_NAME, "url": SITE_URL, "logo": SITE_URL + "/favicon.svg"}]
    if ld: ldj += ld if isinstance(ld, list) else [ld]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ldj)
    nav_links = "".join(f'<a href="{R}{h}">{esc(t)}</a>' for t, h in NAV)
    foot_cols = "".join(f'<div><h4>{esc(h)}</h4>' + "".join(f'<a href="{R}{u}">{esc(t)}</a>' for t, u in links) + "</div>" for h, links in FOOTER.items())
    sticky = f'<div class="stickybar"><span class="small"><b>Free:</b> 7-Step Starter Kit</span><a class="btn sm primary" href="{R}start/">Get it</a></div>' if sticky_cta else ""
    return f'''<!doctype html>
<html lang="en" data-root="{R}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="{SITE_NAME}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}/og.svg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{SITE_URL}/og.svg">
<meta name="theme-color" content="#0b0f1a">
<link rel="icon" href="{R}favicon.svg" type="image/svg+xml"><link rel="manifest" href="{R}manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link rel="preconnect" href="https://api.coingecko.com">
<link rel="stylesheet" href="{R}assets/css/style.css">
{ld_html}{extra_head}
</head>
<body>
<div class="topbar">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership — <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a></div>
<header class="header"><div class="wrap nav">
<a class="logo" href="{R}"><span class="mark">7</span><span>7Blockchain<span class="muted">.com</span></span></a>
<nav class="menu" aria-label="Main">{nav_links}</nav>
<span class="spacer"></span>
<div class="search"><input id="site-search" type="search" placeholder="Search (press /)" aria-label="Search site"><div class="results" id="search-results"></div></div>
<button class="iconbtn" data-theme-toggle title="Toggle theme" aria-label="Toggle light/dark theme">◐</button>
<button class="iconbtn" id="burger" aria-label="Open menu">☰</button>
</div>
<nav class="mobilemenu" id="mobilemenu" aria-label="Mobile">{nav_links}<a href="{R}start/">Free Starter Kit</a><a href="{R}contact/">Contact</a></nav>
</header>
<div class="ticker" aria-label="Live crypto prices"><div class="track" id="ticker-track"><span class="coin muted">Loading live prices…</span></div></div>
<main>
{body}
</main>
<footer class="footer"><div class="wrap">
<div class="cols">{foot_cols}<div><h4>Follow</h4><div class="socials" id="socials"></div><p class="small muted" style="margin-top:12px">Press <b>/</b> to search.</p></div></div>
<div class="legal">
<p><b>Trademark &amp; copyright disclosure.</b> 7Blockchain.com is an independent publication. It is not affiliated with, endorsed by, or sponsored by any company, product, or organisation using "7", "Seven", "Blockchain" or "7 Blockchain" in its name or marks. "Blockchain" is used in its generic, descriptive sense. All third-party names, brands and trademarks belong to their respective owners and are referenced for identification and comparison only. <a href="{R}trademark/">Full disclosure</a>.</p>
<p><b>Not financial advice.</b> Content is educational. Crypto assets are volatile and you can lose your entire investment. Some links are affiliate links — see our <a href="{R}affiliate-disclosure/">affiliate disclosure</a> and <a href="{R}disclaimer/">risk disclaimer</a>.</p>
<p>© <span data-year>2026</span> 7Blockchain.com. All rights reserved. · <a href="{R}privacy/">Privacy</a> · <a href="{R}terms/">Terms</a> · <a href="{R}contact/">Contact</a> · <a href="{R}sitemap.xml">Sitemap</a></p>
</div></div></footer>
<div class="slidein" id="slidein"><button class="x" aria-label="Close">×</button><h3 style="margin-top:0">Before you go…</h3><p class="small muted">Grab the free 7-Step Starter Kit and the weekly 7-in-7 Digest.</p>
<form class="form" data-form="Newsletter signup (slide-in)"><input type="text" name="_honey" style="display:none" tabindex="-1"><div class="inline-sub"><input type="email" name="email" placeholder="you@example.com" required aria-label="Email"><button class="btn sm primary" type="submit">Send it</button></div><div class="ok">Thanks!</div></form></div>
<div class="consent" id="consent">We use cookies for analytics and advertising (Google AdSense). By continuing you accept our <a href="{R}privacy/">privacy policy</a>. <button class="btn sm primary" style="margin-left:8px">OK</button></div>
{sticky}
<script src="{R}assets/js/config.js"></script><script src="{R}assets/js/app.js" defer></script>
</body></html>'''
