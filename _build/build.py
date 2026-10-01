#!/usr/bin/env python3
"""Static site generator for 7Blockchain.com. Run: python3 _build/build.py  (writes into repo root)."""
import os, json, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from layout import *
from data_top7 import LISTS, M7
from data_content import CHAPTERS, GLOSSARY, QUIZ, VIDEOS, DIGEST

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TODAY = datetime.date.today().isoformat()
PAGES = []   # (path, title, desc, keywords) for sitemap + search index

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(content)

def emit(path, title, desc, body, ld=None, kind="website", keywords="", sticky=True):
    depth = path.count("/")
    R = "../" * depth if depth else "./"
    write(path + ("index.html" if path.endswith("/") or path == "" else ""), page(R, path, title, desc, body, ld, kind, sticky_cta=sticky))
    PAGES.append((path, title, desc, keywords))
    return R

def crumbs(R, items):
    return '<div class="wrap breadcrumb"><a href="' + R + '">Home</a>' + "".join(f' › <a href="{R}{u}">{esc(t)}</a>' if u else f' › {esc(t)}' for t, u in items) + '</div>'

def simple(path, title, desc, inner, keywords="", faqs=None, aside=True, R=None):
    depth = path.count("/"); R = "../" * depth if depth else "./"
    side = f'<aside class="side">{ad("rect","rect")}{newsletter_box(R,"sidebar")}<div class="card flat"><h3>Top 7 rankings</h3>' + "".join(f'<a href="{R}top7/{k}/" style="display:block;padding:4px 0">{esc(v["title"])}</a>' for k, v in LISTS.items()) + '</div></aside>' if aside else ""
    body = crumbs(R, [(title, None)]) + f'<div class="wrap article-wrap"><article class="article"><h1>{esc(title)}</h1><p class="lede muted">{esc(desc)}</p>{inner}{faq_block(faqs or [])}</article>{side}</div>'
    emit(path, title + " | 7Blockchain.com", desc, body, faq_ld(faqs) if faqs else None, keywords=keywords)

# ---------------------------------------------------------------- HOME
def home():
    R = "./"
    top7cards = "".join(f'<div class="card"><span class="badge gold">Top 7</span><h3><a href="{R}top7/{k}/">{esc(v["title"])}</a></h3><p class="muted small">{esc(v["desc"])}</p><a class="btn sm ghost" href="{R}top7/{k}/">See the ranking →</a></div>' for k, v in LISTS.items())
    steps = "".join(f'<a class="card flat" href="{R}learn/{c["slug"]}/" style="color:inherit"><div class="num">{c["n"]}</div><h3>{esc(c["title"])}</h3><p class="muted small">{esc(c["desc"])}</p><span class="small">{c["read"]} · {c["level"]}</span></a>' for c in CHAPTERS)
    tools = [("DCA calculator","tools/dca-calculator/","What a fixed weekly buy becomes over time."),("Staking calculator","tools/staking-calculator/","Compound APY on any coin."),("Fee comparison","tools/fee-comparison/","Real cost of trading on each exchange."),("Profit / loss","tools/profit-calculator/","Returns and break-even after fees."),("Live converter","tools/converter/","Crypto → USD at live prices."),("7-question quiz","tools/quiz/","Score 7/7 to enter the contest.")]
    toolcards = "".join(f'<div class="card flat"><h3><a href="{R}{u}">{esc(t)}</a></h3><p class="muted small">{esc(d)}</p></div>' for t, u, d in tools)
    vids = "".join(yt(v) for v in VIDEOS[:3])
    body = f'''
<section class="hero"><div class="wrap">
<span class="badge violet">Independent · Updated {TODAY}</span>
<h1>Everything in blockchain,<br><span>ranked and explained in sevens.</span></h1>
<p class="lede">Top-7 rankings with a published 7-metric score, a 7-step learning path, 7-minute weekly digest, and calculators that show you the numbers — no hype, no paid rankings disguised as advice.</p>
<div class="cta-row"><a class="btn primary" href="{R}start/">Get the free 7-Step Starter Kit</a><a class="btn ghost" href="{R}top7/exchanges/">Top 7 Exchanges</a><a class="btn ghost" href="{R}learn/">Start learning</a></div>
<div class="stats"><div><b>7×7</b><span>rankings × metrics, published</span></div><div><b>7 steps</b><span>beginner → confident</span></div><div><b>90+</b><span>glossary terms</span></div><div><b>$0</b><span>paid for placement in rankings</span></div></div>
<div class="fg" id="feargreed" style="margin-top:22px"></div>
</div></section>
<div class="wrap">{ad("leader","leader")}</div>
<section class="sec"><div class="wrap"><div class="sec-head"><div><h2>Top 7 rankings</h2><p class="sub">Seven picks per category. Seven metrics each. Scores you can argue with.</p></div><a class="btn sm ghost" href="{R}how-we-rank/">How we rank</a></div><div class="grid g3">{top7cards}</div></div></section>
<section class="sec" style="background:var(--bg2)"><div class="wrap"><div class="sec-head"><div><h2>The 7-step path</h2><p class="sub">About an hour of reading, in order. Finish and you'll understand more than most people in the industry.</p></div><a class="btn sm primary" href="{R}learn/">Open the path</a></div><div class="grid g4">{steps}</div></div></section>
<section class="sec"><div class="wrap"><div class="grid g2"><div>{newsletter_box(R,"home","Join the 7-in-7 Digest","Seven stories, seven minutes, every week — plus the Starter Kit PDF the moment you subscribe.")}</div><div class="card"><h3>Find your starter kit in 3 clicks</h3><p class="muted">Tell us your country, experience and goal; get a recommended exchange, wallet and first chapter.</p><a class="btn violet" href="{R}start/">Start the wizard</a></div></div></div></section>
<section class="sec" style="background:var(--bg2)"><div class="wrap"><div class="sec-head"><div><h2>Tools</h2><p class="sub">Numbers beat opinions.</p></div><a class="btn sm ghost" href="{R}tools/">All tools</a></div><div class="grid g3">{toolcards}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><h2>Watch</h2><p class="sub">The best explainers on the internet, curated by chapter.</p></div><a class="btn sm ghost" href="{R}videos/">Video hub</a> <a class="btn sm primary" data-yt-sub href="#" target="_blank" rel="noopener">Subscribe on YouTube</a></div><div class="grid g3">{vids}</div></div></section>
<div class="wrap">{ad("leader","leader")}</div>
<section class="sec" style="background:var(--bg2)"><div class="wrap"><h2>Keep this site independent</h2><p class="sub">No exchange owns us. Readers, sponsors and partners fund the work.</p><div class="grid g4">
<div class="card flat"><h3>Support</h3><p class="muted small">Donate in crypto or fiat; funds operations, promotion and contest prizes.</p><a class="btn sm primary" href="{R}support/">Support us</a></div>
<div class="card flat"><h3>Advertise</h3><p class="muted small">Sponsor a ranking, the digest, a tool or a video.</p><a class="btn sm ghost" href="{R}advertise/">Packages</a></div>
<div class="card flat"><h3>Contests</h3><p class="muted small">Score 7/7 on the quiz; win a share of the prize pool.</p><a class="btn sm ghost" href="{R}contests/">Enter</a></div>
<div class="card flat"><h3>Write for us</h3><p class="muted small">Paid bounties for rankings, explainers and tools.</p><a class="btn sm ghost" href="{R}careers/">Bounties</a></div></div></div></section>'''
    emit("", "7Blockchain.com — Top 7 crypto rankings, 7-step blockchain course, tools & digest", "Independent blockchain education and rankings: Top 7 exchanges, wallets, Layer-1s, Layer-2s, DeFi, cards and tax tools, plus a 7-step learning path, calculators and a weekly 7-in-7 digest.", body, keywords="home crypto blockchain rankings learn")

# ---------------------------------------------------------------- LEARN
def learn():
    R = "../"
    steps = "".join(f'<a class="card" href="{R}learn/{c["slug"]}/" style="color:inherit"><div class="num">{c["n"]}</div><h3>{esc(c["title"])}</h3><p class="muted small">{esc(c["desc"])}</p><span class="badge">{c["level"]}</span> <span class="small muted">{c["read"]}</span></a>' for c in CHAPTERS)
    body = crumbs(R, [("Learn", None)]) + f'''<section class="hero"><div class="wrap"><h1>The 7-Step Blockchain Path</h1><p class="lede">Seven chapters, about an hour total, written for someone who has never bought a coin. Every chapter ends with seven takeaways and a next step.</p><div class="cta-row"><a class="btn primary" href="{R}learn/step-1/">Start with Step 1</a><a class="btn ghost" href="{R}tools/quiz/">Skip to the quiz</a></div></div></section>
<div class="wrap">{ad("leader","leader")}<div class="grid g3" style="margin:30px 0">{steps}</div>{newsletter_box(R,"learn-hub","Get the 7-Step Starter Kit PDF","All seven chapters, checklists and the 7 security rules in one printable PDF.")}</div>'''
    ld = {"@context": "https://schema.org", "@type": "Course", "name": "The 7-Step Blockchain Path", "description": "Free seven-chapter blockchain and crypto course for beginners.", "provider": {"@type": "Organization", "name": SITE_NAME, "sameAs": SITE_URL}}
    emit("learn/", "Learn Blockchain in 7 Steps — Free Course | 7Blockchain.com", "Free 7-step blockchain and crypto course: blockchain basics, Bitcoin, Ethereum, wallets, exchanges, DeFi and security.", body, ld, keywords="learn course beginner blockchain crypto")
    for i, c in enumerate(CHAPTERS):
        R = "../../"
        prev = CHAPTERS[i-1] if i > 0 else None; nxt = CHAPTERS[i+1] if i < 6 else None
        toc = "".join(f'<a href="#s{j+1}">{esc(h)}</a>' for j, (h, _) in enumerate(c["sections"]))
        secs = ""
        for j, (h, txt) in enumerate(c["sections"]):
            secs += f'<h2 id="s{j+1}">{esc(h)}</h2><p>{txt}</p>'
            if j == 1: secs += ad("leader", "leader")
            if j == 2: secs += newsletter_box(R, f"chapter-{c['n']}")
        vids = "".join(yt(v) for v in VIDEOS if v["step"] == c["n"])
        vids_html = f'<h2>Watch</h2><div class="grid g2">{vids}</div>' if vids else ""
        nav = f'<div class="stepnav">' + (f'<a class="btn ghost" href="{R}learn/{prev["slug"]}/">← Step {prev["n"]}</a>' if prev else f'<a class="btn ghost" href="{R}learn/">← Path overview</a>') + (f'<a class="btn primary" href="{R}learn/{nxt["slug"]}/">Step {nxt["n"]}: {esc(nxt["title"])} →</a>' if nxt else f'<a class="btn primary" href="{R}tools/quiz/">Take the 7-question quiz →</a>') + '</div>'
        body = f'<div class="progress" style="position:sticky;top:64px;z-index:49;margin:0;border-radius:0;height:4px"><i id="readprog" style="width:0"></i></div>' + crumbs(R, [("Learn", "learn/"), (f"Step {c['n']}", None)]) + f'''<div class="wrap article-wrap"><article class="article">
<span class="badge violet">Step {c["n"]} of 7</span> <span class="badge">{c["level"]}</span>
<h1>{esc(c["title"])}</h1><div class="meta"><span>{c["read"]} read</span><span>Updated {TODAY}</span><span>By the 7Blockchain editorial team</span></div>
<div class="progress"><i style="width:{round(c['n']/7*100)}%"></i></div>
<div class="takeaways"><h3>7 key takeaways</h3><ol>{"".join(f"<li>{esc(t)}</li>" for t in c["takeaways"])}</ol></div>
{secs}{vids_html}{faq_block(c["faq"])}{nav}
<div class="disclosure">Educational content, not financial advice. Some links to exchanges and wallets are affiliate links; rankings are never sold. <a href="{R}affiliate-disclosure/">Disclosure</a>.</div>
</article><aside class="side"><div class="card flat toc"><h3>In this chapter</h3>{toc}<a href="#faq">FAQ</a></div>{ad("rect","rect")}<div class="card flat"><h3>All 7 steps</h3>{"".join(f'<a href="{R}learn/{x["slug"]}/" style="display:block;padding:4px 0;{"font-weight:800;color:var(--gold2)" if x["n"]==c["n"] else ""}">{x["n"]}. {esc(x["title"])}</a>' for x in CHAPTERS)}</div></aside></div>'''
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": c["title"], "description": c["desc"], "datePublished": TODAY, "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE_NAME}, "publisher": {"@type": "Organization", "name": SITE_NAME}}, faq_ld(c["faq"])]
        emit(f"learn/{c['slug']}/", f"Step {c['n']}: {c['title']} | 7Blockchain.com", c["desc"], body, ld, kind="article", keywords="learn chapter " + c["title"].lower())

# ---------------------------------------------------------------- TOP 7
def top7():
    R = "../"
    def chips(v): return "".join(f"<span class=chip>{i+1}. {esc(it['name'])}</span>" for i, it in enumerate(v["items"][:3]))
    cards = "".join(f'<div class="card"><span class="badge gold">Top 7</span><h3><a href="{R}top7/{k}/">{esc(v["title"])}</a></h3><p class="muted small">{esc(v["desc"])}</p><div class="pill-row">{chips(v)}</div><a class="btn sm ghost" href="{R}top7/{k}/">Full ranking →</a></div>' for k, v in LISTS.items())
    body = crumbs(R, [("Top 7", None)]) + f'''<section class="hero"><div class="wrap"><h1>Top 7 Rankings</h1><p class="lede">Seven picks per category, scored 0–10 on seven published metrics. We never sell a position; "Promoted" labels mark paid placements outside the ranking.</p><div class="cta-row"><a class="btn ghost" href="{R}how-we-rank/">How we rank</a><a class="btn ghost" href="{R}advertise/">Sponsor a list</a></div></div></section><div class="wrap">{ad("leader","leader")}<div class="grid g3" style="margin:30px 0">{cards}</div></div>'''
    emit("top7/", "Top 7 Crypto Rankings: Exchanges, Wallets, Chains, DeFi, Cards, Tax | 7Blockchain.com", "All Top 7 rankings in one place, each scored on seven metrics: security, fees, ease of use, assets, features, support and reputation.", body, keywords="top 7 best rankings")
    os.makedirs(os.path.join(OUT, "data/top7"), exist_ok=True)
    for k, v in LISTS.items():
        R = "../../"
        write(f"data/top7/{k}.json", json.dumps({"title": v["title"], "metrics": M7, "items": v["items"]}, indent=1))
        rows = ""
        for i, it in enumerate(v["items"]):
            rows += f'<tr><td data-v="{i+1}">#{i+1}</td><td><b>{esc(it["name"])}</b><br><span class="small muted">{esc(it["badge"])}</span></td><td data-v="{it["score"]}"><b>{it["score"]}</b>/10</td><td>{esc(it["fee"])}</td><td>{esc(it["coins"])}</td><td>{esc(it["us"])}</td><td>{esc(it["bestfor"])}</td><td><a class="btn sm primary" data-go="{it["key"]}" href="#">Visit</a></td></tr>'
        table = f'<div class="table-wrap"><table class="cmp"><thead><tr><th>#</th><th>Name</th><th>{v["cols"][0]} ↕</th><th>{v["cols"][1]}</th><th>{v["cols"][2]}</th><th>{v["cols"][3]}</th><th>{v["cols"][4]}</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>'
        entries = ""
        for i, it in enumerate(v["items"]):
            metrics = "".join(f'<div>{m}<b>{s}</b></div>' for m, s in zip(M7, it["m"]))
            entries += f'''<div class="card" id="{it["key"]}"><div class="rank"><div class="pos">{i+1}<small>of 7</small></div><div>
<span class="badge gold">{esc(it["badge"])}</span><h2 style="margin:8px 0 4px">{esc(it["name"])}</h2>
<div class="score">{it["score"]}<small>/ 10</small></div><div class="scorebar"><i style="width:{it["score"]*10}%"></i></div>
<div class="metrics">{metrics}</div>
<div class="proscons"><div><b>Pros</b><ul class="pros">{"".join(f"<li>{esc(p)}</li>" for p in it["pros"])}</ul></div><div><b>Cons</b><ul class="cons">{"".join(f"<li>{esc(p)}</li>" for p in it["cons"])}</ul></div></div>
<p class="small"><b>Choose it if</b> {esc(it["choose"])} <b>Skip it if</b> {esc(it["skip"])}</p>
<div class="cta-row" style="margin:10px 0 0"><a class="btn primary" data-go="{it["key"]}" href="#">Visit {esc(it["name"])}</a><a class="btn ghost sm" href="#top">Back to table</a></div></div></div></div>'''
            if i == 2: entries += ad("leader", "leader")
        disc = f'<div class="disclosure"><b>Advertiser disclosure.</b> We may earn a commission when you open an account through "Visit" links. Commissions never influence scores or order — see <a href="{R}how-we-rank/">how we rank</a> and our <a href="{R}affiliate-disclosure/">affiliate disclosure</a>. Figures are indicative as of {TODAY}; verify on the provider site.</div>'
        others = "".join(f'<a href="{R}top7/{k2}/" style="display:block;padding:4px 0">{esc(v2["title"])}</a>' for k2, v2 in LISTS.items() if k2 != k)
        body = crumbs(R, [("Top 7", "top7/"), (v["title"], None)]) + f'''<div class="wrap article-wrap" id="top"><article class="article" style="max-width:none">
<span class="badge gold">Top 7</span><h1>{esc(v["h1"])}</h1><div class="meta"><span>Updated {TODAY}</span><span>7-metric methodology</span><span>Independent — positions are not for sale</span></div>
<p class="lede">{esc(v["intro"])}</p>{disc}{table}
<h2>The seven, in detail</h2>{entries}{faq_block(v["faq"])}{newsletter_box(R,"top7-"+k)}{disc}
</article><aside class="side">{ad("sky","sky")}<div class="card flat"><h3>Other rankings</h3>{others}</div><div class="card flat"><h3>Sponsor this ranking</h3><p class="small muted">Your brand above the table, labelled "Presented by". Scores unaffected.</p><a class="btn sm ghost" href="{R}advertise/">See packages</a></div></aside></div>'''
        ld = [{"@context": "https://schema.org", "@type": "ItemList", "name": v["h1"], "itemListOrder": "https://schema.org/ItemListOrderDescending", "numberOfItems": 7, "itemListElement": [{"@type": "ListItem", "position": i+1, "name": it["name"]} for i, it in enumerate(v["items"])]}, faq_ld(v["faq"])]
        emit(f"top7/{k}/", v["h1"] + " | 7Blockchain.com", v["desc"], body, ld, kind="article", keywords="top 7 best " + k + " " + " ".join(it["name"].lower() for it in v["items"]))

# ---------------------------------------------------------------- TOOLS
def tools():
    R = "../"
    tl = [("DCA calculator","tools/dca-calculator/","Project a fixed recurring buy at any growth rate, using the live BTC price."),("Staking calculator","tools/staking-calculator/","Compound any APY daily, weekly or monthly over years."),("Exchange fee comparison","tools/fee-comparison/","What your monthly trading actually costs on each Top-7 exchange."),("Profit / loss calculator","tools/profit-calculator/","Returns, fees and break-even price for any trade."),("Live converter","tools/converter/","Crypto to USD at live market prices."),("7-question quiz","tools/quiz/","Test the whole 7-step path; a perfect score enters the contest."),("Glossary","glossary/","90+ terms, searchable.")]
    body = crumbs(R, [("Tools", None)]) + f'<section class="hero"><div class="wrap"><h1>Crypto Tools &amp; Calculators</h1><p class="lede">Free, no sign-up, run in your browser. Nothing you type leaves your device.</p></div></section><div class="wrap">{ad("leader","leader")}<div class="grid g3" style="margin:30px 0">' + "".join(f'<div class="card"><h3><a href="{R}{u}">{esc(t)}</a></h3><p class="muted small">{esc(d)}</p><a class="btn sm ghost" href="{R}{u}">Open →</a></div>' for t, u, d in tl) + '</div></div>'
    emit("tools/", "Free Crypto Tools & Calculators | 7Blockchain.com", "DCA calculator, staking yield calculator, exchange fee comparison, profit/loss calculator, live converter and quiz.", body, keywords="tools calculators")

    def toolpage(path, title, desc, tool_html, expl, faqs, kw):
        R = "../../"
        inner = f'<div class="tool">{tool_html}</div>{ad("leader","leader")}{expl}'
        simple(path, title, desc, inner, keywords=kw, faqs=faqs)

    toolpage("tools/dca-calculator/", "Crypto DCA Calculator", "See what a fixed weekly or monthly buy becomes over time at any growth rate — starts from the live Bitcoin price.",
      '<form id="dca-form" class="form"><div class="row"><div><label>Amount per month ($)</label><input id="dca-amt" type="number" value="200" min="1"></div><div><label>Months</label><input id="dca-months" type="number" value="36" min="1" max="360"></div><div><label>Assumed annual growth (%)</label><input id="dca-growth" type="number" value="20" step="1"></div><div><label>Starting price ($, live BTC auto-fills)</label><input id="dca-price" type="number" placeholder="live"></div></div></form><div class="out" id="dca-out"></div>',
      '<h2>How to read this</h2><p>Dollar-cost averaging buys a fixed amount on a schedule regardless of price. The model compounds your assumed annual growth monthly and buys at each month\'s modelled price. Try 0% growth and –30% to see how DCA behaves in flat and falling markets — the average buy price is what matters.</p><p>Automate it on an exchange from our <a href="../../top7/exchanges/">Top 7 Exchanges</a> and read <a href="../../learn/step-5/">Step 5</a> for the fee traps.</p>',
      [["Is DCA better than lump-sum?","Lump-sum wins on average in rising markets; DCA wins on behaviour because it removes timing decisions. Most people stick with DCA longer."],["Which coin should I DCA?","The calculator is coin-agnostic. The majority of long-term DCA plans use BTC and ETH — see Step 2 and Step 3."]], "dca calculator dollar cost averaging")
    toolpage("tools/staking-calculator/", "Crypto Staking Calculator", "Compound any staking APY over time — daily, weekly or monthly — and compare with simple interest.",
      '<form id="stake-form" class="form"><div class="row"><div><label>Amount staked (coins or $)</label><input id="st-amt" type="number" value="10" step="any"></div><div><label>APY (%)</label><input id="st-apy" type="number" value="4" step="0.1"></div><div><label>Years</label><input id="st-years" type="number" value="5" step="1"></div><div><label>Compounds per year</label><select id="st-comp"><option value="365">Daily</option><option value="52">Weekly</option><option value="12">Monthly</option><option value="1">Yearly</option></select></div></div></form><div class="out" id="st-out"></div>',
      '<h2>Where staking yield comes from</h2><p>Proof-of-Stake networks pay validators new coins plus fees for securing the chain. Ethereum pays roughly 3–4%, Solana 6–8%, Cardano 2–3%; liquid staking tokens (stETH, jitoSOL) pass most of that through. Yield in coins is not yield in dollars — price moves dominate. Read <a href="../../learn/step-3/">Step 3</a> and the <a href="../../top7/defi/">Top 7 DeFi</a> list.</p>',
      [["Is staking risky?","Slashing on major networks is rare; the real risks are smart-contract bugs in liquid staking and exchange insolvency in custodial staking."],["Are rewards taxable?","Usually as income at the time received, then capital gains when sold. See Step 7."]], "staking calculator apy compound")
    rows = "".join(f'<tr data-maker="{m}" data-taker="{t}"><td><b>{n}</b></td><td>{m}%</td><td>{t}%</td><td class="costm">—</td><td class="cost" data-v="0">—</td></tr>' for n, m, t in [("Coinbase (Advanced)",0.40,0.60),("Kraken (Pro)",0.25,0.40),("Binance",0.10,0.10),("Bybit",0.10,0.10),("OKX",0.08,0.10),("Crypto.com",0.075,0.075),("Bitget",0.10,0.10)])
    toolpage("tools/fee-comparison/", "Crypto Exchange Fee Comparison", "Enter your average trade size and monthly trade count to see what each Top-7 exchange costs you per month.",
      f'<form id="fee-form" class="form"><div class="row"><div><label>Average trade size ($)</label><input id="fee-trade" type="number" value="500"></div><div><label>Trades per month</label><input id="fee-n" type="number" value="12"></div></div></form><div class="table-wrap"><table class="cmp" id="fee-table"><thead><tr><th>Exchange</th><th>Maker</th><th>Taker</th><th>Monthly (maker)</th><th>Monthly (taker)</th></tr></thead><tbody>{rows}</tbody></table></div><p class="small muted">Base-tier spot fees, indicative; most exchanges discount with volume or native tokens. Simple-buy buttons add a 1–2% spread on top — use the trading screen.</p>',
      '<h2>Why fees matter more than you think</h2><p>At 12 trades a month of $500, the gap between a 0.60% and a 0.10% taker fee is $30 a month — $360 a year, before spreads and withdrawal fees. Limit (maker) orders are cheaper almost everywhere. Full scores: <a href="../../top7/exchanges/">Top 7 Exchanges</a>.</p>',
      [["What is a maker vs taker?","A maker order sits on the order book (limit order); a taker fills an existing order (market order). Makers pay less because they add liquidity."]], "exchange fees comparison maker taker")
    toolpage("tools/profit-calculator/", "Crypto Profit / Loss Calculator", "Compute profit, return and break-even price for any trade after fees.",
      '<form id="pl-form" class="form"><div class="row"><div><label>Quantity</label><input id="pl-qty" type="number" value="0.5" step="any"></div><div><label>Buy price ($)</label><input id="pl-buy" type="number" value="60000"></div><div><label>Sell price ($)</label><input id="pl-sell" type="number" value="75000"></div><div><label>Fee per side (%)</label><input id="pl-fee" type="number" value="0.4" step="0.01"></div></div></form><div class="out" id="pl-out"></div>',
      '<h2>Notes</h2><p>Fees are applied on both the buy and the sell. Break-even is the sell price at which net proceeds equal total cost. Taxes are not included — use a tool from <a href="../../top7/tax-tools/">Top 7 Tax Tools</a>.</p>', [], "profit loss calculator")
    toolpage("tools/converter/", "Live Crypto Converter", "Convert BTC, ETH, SOL and more to USD at live market prices.",
      '<form id="conv-form" class="form"><div class="row"><div><label>Amount</label><input id="cv-amt" type="number" value="1" step="any"></div><div><label>Coin</label><select id="cv-coin"><option value="bitcoin">Bitcoin (BTC)</option><option value="ethereum">Ethereum (ETH)</option><option value="solana">Solana (SOL)</option><option value="binancecoin">BNB</option><option value="ripple">XRP</option><option value="cardano">Cardano (ADA)</option><option value="avalanche-2">Avalanche (AVAX)</option><option value="chainlink">Chainlink (LINK)</option><option value="polkadot">Polkadot (DOT)</option><option value="the-open-network">Toncoin (TON)</option></select></div></div></form><div class="out" id="cv-out"></div><p class="small muted">Prices via CoinGecko public API; refreshed on page load.</p>',
      '<h2>Buying at this price</h2><p>Compare venues on the <a href="../../top7/exchanges/">Top 7 Exchanges</a> list and check the real cost with the <a href="../fee-comparison/">fee tool</a>.</p>', [], "converter price usd")
    qs = ""
    for i, q in enumerate(QUIZ):
        opts = "".join(f'<button type="button" data-ok="{1 if j==q["ok"] else 0}">{esc(o)}</button>' for j, o in enumerate(q["opts"]))
        qs += f'<div class="q {"active" if i==0 else ""}"><span class="badge violet">Question {i+1} of 7</span><h3>{esc(q["q"])}</h3><div class="opts">{opts}</div><p class="why small muted" style="display:none">{esc(q["why"])}</p></div>'
    quiz_html = f'<div class="quiz" id="quiz">{qs}</div><div id="quiz-result" class="result-box"><h3>Your score: <span id="qscore" class="hl"></span></h3><p id="qmsg"></p><div class="cta-row"><a class="btn primary" href="../../contests/">Enter the contest</a><a class="btn ghost" href="../../learn/">Review the path</a></div><form class="form" data-form="Quiz result + newsletter" style="margin-top:14px"><input type="hidden" name="score" id="quiz-score-field"><input type="text" name="_honey" style="display:none" tabindex="-1"><label>Save my score and send the Starter Kit</label><div class="inline-sub"><input type="email" name="email" placeholder="you@example.com" required><button class="btn primary" type="submit">Send</button></div><div class="ok">Sent.</div></form></div>'
    toolpage("tools/quiz/", "Crypto Basics Quiz (7 Questions)", "Seven questions covering the 7-step path. Score 7/7 to qualify for the current contest.", quiz_html,
      '<h2>About the quiz</h2><p>Each question maps to one chapter of the <a href="../../learn/">7-step path</a>. Missed one? The explanation names the chapter to re-read. Perfect scores qualify for the <a href="../../contests/">contest</a>.</p>', [], "quiz test knowledge contest")

# ---------------------------------------------------------------- GLOSSARY, VIDEOS, DIGEST
def glossary():
    terms = sorted(GLOSSARY, key=lambda t: t[0].lower())
    letters = sorted(set(t[0][0].upper() for t in terms))
    az = '<div class="azbar">' + "".join(f'<a href="#g-{l}">{l}</a>' for l in letters) + '</div>'
    html_terms = ""; cur = ""
    for t, d in terms:
        l = t[0].upper()
        if l != cur: cur = l; html_terms += f'<h2 id="g-{l}">{l}</h2>'
        html_terms += f'<div class="term" id="{t.lower().replace(" ","-").replace("(","").replace(")","")}"><b>{esc(t)}</b>{esc(d)}</div>'
    inner = f'<input id="gloss-filter" type="search" placeholder="Filter terms…" class="form" style="width:100%;padding:12px;border-radius:10px;border:1px solid var(--line);background:var(--bg3);color:var(--text)">{az}{ad("leader","leader")}<div class="gloss">{html_terms}</div>'
    ld = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "7Blockchain Crypto Glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in terms]}
    simple("glossary/", "Blockchain & Crypto Glossary", f"{len(terms)} blockchain and crypto terms defined in one line each, A–Z and searchable.", inner, keywords="glossary terms definitions " + " ".join(t.lower() for t, _ in terms))

def videos():
    R = "../"
    grid = "".join(yt(v) + f'<div class="small"><a href="{R}learn/step-{v["step"]}/">Goes with Step {v["step"]}</a></div>' for v in VIDEOS)
    body = crumbs(R, [("Videos", None)]) + f'''<section class="hero"><div class="wrap"><h1>Video Hub</h1><p class="lede">The clearest explainers on the internet, mapped to the 7-step path. Videos load only when you press play.</p><div class="cta-row"><a class="btn primary" data-yt-sub href="#" target="_blank" rel="noopener">Subscribe to our YouTube channel</a><a class="btn ghost" href="{R}advertise/">Sponsor a video</a></div></div></section><div class="wrap">{ad("leader","leader")}<div class="grid g3" style="margin:30px 0">{grid}</div>{newsletter_box(R,"videos")}<p class="small muted" style="margin-top:20px">Videos are embedded from YouTube under their standard embed terms and belong to their creators. Want yours featured or removed? <a href="{R}contact/">Contact us</a>.</p></div>'''
    emit("videos/", "Blockchain & Crypto Video Hub | 7Blockchain.com", "Curated blockchain and crypto explainer videos mapped to the 7-step learning path.", body, keywords="videos youtube watch")

def digest():
    R = "../"
    issues = "".join(f'<div class="card"><span class="badge violet">{d["date"]}</span><h3><a href="{R}digest/{d["slug"]}/">{esc(d["title"])}</a></h3><p class="muted small">{esc(d["items"][0][1][:140])}…</p><a class="btn sm ghost" href="{R}digest/{d["slug"]}/">Read →</a></div>' for d in DIGEST[::-1])
    body = crumbs(R, [("Digest", None)]) + f'''<section class="hero"><div class="wrap"><h1>7-in-7 Digest</h1><p class="lede">Seven stories, seven minutes, every week. Each story ends with one action. Sponsored by nobody until a sponsor earns the slot.</p></div></section><div class="wrap"><div class="grid g2"><div>{newsletter_box(R,"digest-hub","Subscribe to 7-in-7","Delivered weekly. Free forever.")}</div><div class="card"><h3>Sponsor the digest</h3><p class="muted small">One labelled slot per issue, above the fold, in every inbox and on this page.</p><a class="btn sm ghost" href="{R}advertise/">Rates</a></div></div>{ad("leader","leader")}<h2 style="margin-top:30px">Issues</h2><div class="grid g2">{issues}</div></div>'''
    emit("digest/", "7-in-7 Digest — Weekly Crypto Briefing | 7Blockchain.com", "Weekly crypto and blockchain digest: seven stories, seven minutes, one action each.", body, keywords="digest newsletter weekly news")
    for d in DIGEST:
        R = "../../"
        items = "".join(f'<h2>{i+1}. {esc(h)}</h2><p>{t}</p>' + (ad("leader","leader") if i == 2 else "") for i, (h, t) in enumerate(d["items"]))
        inner = f'<div class="disclosure"><b>Sponsor:</b> {d["sponsor"].replace("/advertise/", R + "advertise/")}</div>{items}{newsletter_box(R, "digest-"+d["slug"])}'
        simple(f"digest/{d['slug']}/", d["title"], f"7-in-7 Digest issue dated {d['date']}: " + "; ".join(h for h, _ in d["items"][:4]) + ".", inner, keywords="digest issue")

# ---------------------------------------------------------------- LEAD GEN / NEWSLETTER / START
def start():
    R = "../"
    body = crumbs(R, [("Starter Kit", None)]) + f'''<section class="hero"><div class="wrap"><h1>Find your 7-Step Starter Kit</h1><p class="lede">Three questions. You get a recommended exchange, wallet and the chapter to start on — plus the Starter Kit PDF by email.</p></div></section>
<div class="wrap"><div class="grid g2"><div class="card wizard" id="wizard">
<div class="step active" data-key="country"><h3>1. Where are you based?</h3><div class="choices"><button data-v="us">United States</button><button data-v="eu">Europe / UK</button><button data-v="asia">Asia / India</button><button data-v="other">Elsewhere</button></div></div>
<div class="step" data-key="level"><h3>2. Your experience?</h3><div class="choices"><button data-v="beginner">Never bought crypto</button><button data-v="some">Bought on an exchange</button><button data-v="advanced">Use a self-custody wallet</button></div></div>
<div class="step" data-key="goal"><h3>3. Main goal?</h3><div class="choices"><button data-v="hold">Hold long term</button><button data-v="trade">Trade actively</button><button data-v="defi">Earn in DeFi</button><button data-v="spend">Spend with a card</button></div></div>
<div class="step"><h3>Your picks</h3><div id="wz-out"></div>
<form class="form" data-form="Starter Kit request" style="margin-top:18px"><input type="hidden" name="profile" id="wz-profile"><input type="text" name="_honey" style="display:none" tabindex="-1"><label>Email me the Starter Kit PDF and these picks</label><div class="inline-sub"><input type="email" name="email" placeholder="you@example.com" required><button class="btn primary" type="submit">Send my kit</button></div><div class="note">You'll also get the weekly 7-in-7 Digest. Unsubscribe any time.</div><div class="ok">On its way.</div></form></div>
</div><div><div class="card"><h3>What's in the kit</h3><ul><li>All 7 chapters as a printable PDF</li><li>Exchange setup checklist (KYC, 2FA, whitelist)</li><li>Hardware-wallet setup card</li><li>The 7 security rules, wallet-sized</li><li>Tax log template</li><li>The 7-question quiz with answers</li><li>Links to every Top-7 ranking</li></ul></div>{ad("rect","rect")}</div></div></div>'''
    emit("start/", "Free 7-Step Crypto Starter Kit — personalised in 3 clicks | 7Blockchain.com", "Answer three questions and get a recommended exchange, wallet and first chapter, plus the free 7-Step Starter Kit PDF.", body, keywords="start starter kit beginner wizard free pdf", sticky=False)

def newsletter():
    R = "../"
    body = crumbs(R, [("Newsletter", None)]) + f'''<section class="hero"><div class="wrap"><h1>The 7-in-7 Digest</h1><p class="lede">Seven stories. Seven minutes. One action each. Every week, free.</p></div></section><div class="wrap"><div class="grid g2"><div>{newsletter_box(R,"newsletter-page","Subscribe","Join readers who'd rather read seven things that matter than seventy that don't.")}</div><div class="card"><h3>What you get</h3><ul><li>The 7-in-7 Digest every week</li><li>The 7-Step Starter Kit PDF instantly</li><li>Contest announcements and winners</li><li>Ranking updates when scores change</li></ul><p class="small muted">Sample: <a href="{R}digest/issue-1/">Issue #1</a>.</p></div></div>{ad("leader","leader")}</div>'''
    emit("newsletter/", "Subscribe to the 7-in-7 Digest | 7Blockchain.com", "Weekly crypto digest: seven stories, seven minutes, one action each. Free.", body, keywords="newsletter subscribe", sticky=False)

# ---------------------------------------------------------------- SUPPORT / CONTESTS / CAREERS / ADVERTISE
def support():
    R = "../"
    coins = [("Bitcoin (BTC)","btc"),("Ethereum (ETH)","eth"),("Solana (SOL)","sol"),("USDC (ERC-20)","usdc")]
    addr = "".join(f'<div class="card flat"><h3>{n}</h3><div class="addr"><code data-addr="{k}"></code><button class="btn sm ghost" data-copy="">Copy</button></div><div class="qr" style="margin-top:10px">QR appears once address is set</div></div>' for n, k in coins)
    body = crumbs(R, [("Support", None)]) + f'''<section class="hero"><div class="wrap"><h1>Support 7Blockchain.com</h1><p class="lede">No exchange owns this site. Donations fund operations, promotion, contest prizes and paid writers — and keep rankings unbought.</p><div class="goal" id="goal"></div></div></section>
<div class="wrap"><div class="grid g2"><div class="card"><h3>Donate with fiat</h3><p class="muted small">One-off or monthly.</p><div class="cta-row"><a class="btn primary" data-link="buymeacoffee" href="#">Buy us a coffee</a><a class="btn ghost" data-link="paypal" href="#">PayPal</a><a class="btn ghost" data-link="githubSponsors" href="#">GitHub Sponsors</a></div></div>
<div class="card"><h3>What your support funds</h3><ul><li><b>Operations</b> — hosting, data APIs, tooling</li><li><b>Promotion &amp; marketing</b> — getting rankings in front of new readers</li><li><b>Hiring talent</b> — paid bounties for writers and developers (<a href="{R}careers/">bounties</a>)</li><li><b>Contests &amp; prizes</b> — funded prize pools (<a href="{R}contests/">current contest</a>)</li></ul></div></div>
<h2 style="margin-top:30px">Donate in crypto</h2><div class="grid g2">{addr}</div>
<h2 style="margin-top:30px">Supporter tiers</h2><div class="grid g3 tiers">
<div class="card"><div class="price">$7<small>/one-off</small></div><h3>Reader</h3><p class="small muted">Name on the supporters list (optional) and our thanks.</p></div>
<div class="card best"><div class="price">$27<small>/month</small></div><h3>Member</h3><p class="small muted">Early access to new rankings, vote on the next Top-7 category, member badge.</p></div>
<div class="card"><div class="price">$177<small>/month</small></div><h3>Patron</h3><p class="small muted">Everything above plus a monthly call with the editors and your name in the footer.</p></div></div>
<div class="card" style="margin-top:30px"><h3>Tell us about your donation</h3><p class="small muted">Optional — so we can thank you and list you if you wish.</p><form class="form" data-form="Donation notice"><input type="text" name="_honey" style="display:none" tabindex="-1"><div class="row"><div><label>Name (or alias)</label><input name="name"></div><div><label>Email</label><input type="email" name="email" required></div><div><label>Amount &amp; method</label><input name="amount_and_method" placeholder="e.g. $27 via PayPal"></div><div><label>List me publicly?</label><select name="list_publicly"><option>Yes</option><option>No</option></select></div></div><label>Message</label><textarea name="message" rows="3"></textarea><button class="btn primary" type="submit">Send</button><div class="ok">Thank you!</div></form></div>{ad("leader","leader")}</div>'''
    emit("support/", "Support 7Blockchain.com — Donate | 7Blockchain.com", "Donate in crypto or fiat to fund independent rankings, promotion, hiring and contest prizes.", body, keywords="support donate donation crypto address", sticky=False)

def contests():
    R = "../"
    body = crumbs(R, [("Contests", None)]) + f'''<section class="hero"><div class="wrap"><h1>Contests &amp; Prizes</h1><p class="lede">Learn, score, win. Prize pools are funded by sponsors and reader support; winners are announced in the digest.</p></div></section>
<div class="wrap" id="contest-box"><div class="card"><span class="badge gold">Live</span><h2 id="c-title"></h2><p><b>Prize:</b> <span id="c-prize"></span></p><div class="countdown" id="c-countdown"></div><p class="small muted" style="margin-top:10px"><b>Rules:</b> <span id="c-rules"></span></p><p class="small"><span id="c-sponsor"></span></p><div class="cta-row"><a class="btn primary" href="{R}tools/quiz/">Take the quiz</a><a class="btn ghost" href="#enter">Submit entry</a></div></div>
<div class="grid g2" style="margin-top:24px"><div class="card" id="enter"><h3>Entry form</h3><form class="form" data-form="Contest entry"><input type="text" name="_honey" style="display:none" tabindex="-1"><div class="row"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div><div><label>Quiz score</label><input name="score" placeholder="7/7" required></div><div><label>Country</label><input name="country"></div></div><label>Link to your score screenshot (Drive/Imgur) or paste a note</label><input name="proof_link"><label><input type="checkbox" required style="width:auto"> I accept the rules and the <a href="{R}terms/">terms</a></label><button class="btn primary" type="submit">Submit entry</button><div class="ok">Entry received.</div></form></div>
<div><div class="card"><h3>Sponsor a prize</h3><p class="muted small">Fund a prize pool and your brand appears on every contest page, the quiz result screen and the winners' announcement.</p><a class="btn sm ghost" href="{R}advertise/">Sponsorship packages</a></div><div class="card" style="margin-top:18px"><h3>Past winners</h3><p class="muted small">First contest in progress — winners will be listed here.</p></div>{ad("rect","rect")}</div></div>
<h2 style="margin-top:30px">Official rules (summary)</h2><p class="small muted">Open worldwide where legal; void where prohibited. No purchase necessary. One entry per person. Winners drawn at random among eligible entries after the deadline and notified by email; prizes paid in USDC or gift cards within 14 days. Sponsors' employees ineligible. We may publish winners' first name and country. Full terms on request via the <a href="{R}contact/">contact form</a>.</p></div>'''
    emit("contests/", "Contests & Prizes | 7Blockchain.com", "Score 7/7 on the crypto basics quiz and enter to win a share of the prize pool. Sponsor a contest to reach engaged learners.", body, keywords="contest giveaway prize win", sticky=False)

def careers():
    R = "../"
    roles = [("Ranking analyst (freelance)","$150–$400 per Top-7 ranking","Research 20+ providers, score on seven metrics with sources, write pros/cons and FAQ."),("Explainer writer (freelance)","$100–$250 per chapter","Plain-English explainers at Step-1 to Step-7 level, with takeaways and FAQ."),("Tool developer (freelance)","$300–$900 per calculator","Vanilla-JS tools with tests; see /tools/ for the standard."),("Video editor (freelance)","$80–$200 per video","Cut 7-minute explainers and Shorts from scripts."),("Ambassador","Revenue share + perks","Share rankings in your community; earn on referred sponsors and subscribers.")]
    cards = "".join(f'<div class="card"><h3>{esc(t)}</h3><span class="badge green">{esc(p)}</span><p class="muted small" style="margin-top:8px">{esc(d)}</p></div>' for t, p, d in roles)
    body = crumbs(R, [("Careers", None)]) + f'''<section class="hero"><div class="wrap"><h1>Careers, Bounties &amp; Ambassadors</h1><p class="lede">Remote, paid per deliverable in USDC or fiat. Show us one great piece of work and you're in.</p></div></section>
<div class="wrap"><div class="grid g3">{cards}</div><div class="grid g2" style="margin-top:26px"><div class="card"><h3>Apply or pitch a bounty</h3><form class="form" data-form="Job / bounty application"><input type="text" name="_honey" style="display:none" tabindex="-1"><div class="row"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div><div><label>Role</label><select name="role"><option>Ranking analyst</option><option>Explainer writer</option><option>Tool developer</option><option>Video editor</option><option>Ambassador</option><option>Other</option></select></div><div><label>Portfolio / LinkedIn / GitHub</label><input name="portfolio" required></div></div><label>Pitch (what would you build or write first?)</label><textarea name="pitch" rows="4" required></textarea><label>Preferred payment</label><select name="payment"><option>USDC</option><option>Bank transfer</option><option>PayPal</option></select><button class="btn primary" type="submit">Send application</button><div class="ok">Received — we reply within 7 days.</div></form></div>
<div><div class="card"><h3>How bounties work</h3><ol><li>Pitch a piece or claim an open one.</li><li>Get a brief and a fixed fee in writing.</li><li>Deliver; one revision round.</li><li>Paid within 7 days of publishing, byline included.</li></ol></div>{ad("rect","rect")}</div></div></div>'''
    emit("careers/", "Careers, Writer Bounties & Ambassadors | 7Blockchain.com", "Paid freelance bounties for crypto writers, analysts, developers and video editors; ambassador programme with revenue share.", body, keywords="careers jobs hiring bounty write for us", sticky=False)

def advertise():
    R = "../"
    pk = [("List sponsor","$700 / month","\"Presented by\" banner above one Top-7 table and its sidebar. Scores unaffected.", False),("Promoted placement","$350 / month","A labelled card beneath a ranking table with your CTA — outside the ranked seven.", False),("Digest sponsor","$270 / issue","One labelled slot above the fold in the 7-in-7 email and web issue.", True),("Tool sponsor","$450 / month","Your brand on a calculator page with a CTA in the results box.", False),("Video integration","$500 / video","30-second integration in a 7Blockchain explainer plus pinned link.", False),("Homepage takeover","$1,700 / week","Hero banner and leaderboard across the site for seven days.", False),("Custom / partnership","Let's talk","Content partnerships, data licensing, co-branded rankings, white-label tools, domain inquiries.", False)]
    cards = "".join(f'<div class="card {"best" if b else ""}"><h3>{esc(t)}</h3><div class="price">{esc(p)}</div><p class="muted small">{esc(d)}</p></div>' for t, p, d, b in pk)
    body = crumbs(R, [("Advertise", None)]) + f'''<section class="hero"><div class="wrap"><h1>Advertise, Sponsor, Partner</h1><p class="lede">Reach people at the exact moment they choose an exchange, wallet, chain or tax tool. Every placement is labelled; rankings are never for sale — which is why readers trust the pages your brand sits on.</p><div class="cta-row"><a class="btn primary" href="#book">Book a slot</a><a class="btn ghost" href="{R}how-we-rank/">Our independence policy</a></div></div></section>
<div class="wrap"><div class="grid g4"><div class="card flat"><b class="hl">Audience</b><p class="small muted">Beginners-to-intermediate crypto buyers researching a decision.</p></div><div class="card flat"><b class="hl">Intent pages</b><p class="small muted">7 Top-7 rankings, 6 tools, 7-step course.</p></div><div class="card flat"><b class="hl">Formats</b><p class="small muted">Sponsor banners, promoted cards, digest, video, takeover.</p></div><div class="card flat"><b class="hl">Reporting</b><p class="small muted">Monthly impressions and clicks per placement.</p></div></div>
<h2 style="margin-top:30px">Packages</h2><div class="grid g3 tiers">{cards}</div>
<div class="grid g2" style="margin-top:30px"><div class="card" id="book"><h3>Booking &amp; inquiries</h3><p class="small muted" id="partnership">Advertising, sponsorship, partnership, or interest in this website or domain name.</p><form class="form" data-form="Advertising / partnership inquiry"><input type="text" name="_honey" style="display:none" tabindex="-1"><div class="row"><div><label>Name</label><input name="name" required></div><div><label>Company</label><input name="company"></div><div><label>Email</label><input type="email" name="email" required></div><div><label>Interest</label><select name="subject"><option>List sponsor</option><option>Promoted placement</option><option>Digest sponsor</option><option>Tool sponsor</option><option>Video integration</option><option>Homepage takeover</option><option>Partnership</option><option>This website / domain name</option></select></div></div><label>Budget &amp; timing</label><input name="budget_and_timing"><label>Details</label><textarea name="details" rows="4"></textarea><button class="btn primary" type="submit">Send inquiry</button><div class="ok">Thanks — we reply within 2 business days.</div></form></div>
<div><div class="card"><h3>Prefer email?</h3><p class="small muted">Use the button; it opens a pre-addressed message.</p><a class="btn ghost" data-contact data-subject="Advertising / partnership inquiry via 7Blockchain.com" href="#">Email the team</a></div><div class="card" style="margin-top:18px"><h3>Media kit</h3><p class="small muted">Request current traffic, audience and placement specs through the form.</p></div>{ad("rect","rect")}</div></div></div>'''
    emit("advertise/", "Advertise, Sponsor & Partner | 7Blockchain.com", "Sponsorship packages for Top-7 rankings, the 7-in-7 digest, tools and videos; partnership and domain inquiries.", body, keywords="advertise sponsor partnership media kit", sticky=False)

# ---------------------------------------------------------------- ABOUT / CONTACT / LEGAL
def about_contact_legal():
    simple("about/", "About 7Blockchain.com", "An independent blockchain publication built on one constraint: everything in sevens.",
      '''<h2>Why sevens</h2><p>Infinite lists are how the industry hides mediocrity. Forcing every ranking to seven picks and every pick to seven scored metrics forces us to make calls — and to show our work so you can disagree with the weights.</p>
<h2>How we make money</h2><p>Affiliate commissions when you open an account through our links, labelled sponsorships, display advertising, reader support and paid contests. Rankings and scores are never sold. Read the <a href="../how-we-rank/">methodology</a> and <a href="../affiliate-disclosure/">disclosure</a>.</p>
<h2>Who we are</h2><p>7Blockchain.com is operated by an independent publisher, with freelance analysts, writers and developers paid per piece (<a href="../careers/">join them</a>). We are not affiliated with any exchange, wallet, blockchain foundation or any company using "7" or "Blockchain" in its name — see the <a href="../trademark/">trademark disclosure</a>.</p>
<h2>Interested in this website or domain?</h2><p>Inquiries about sponsorship, advertising, partnership or the website/domain name go through <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a> or our <a href="../contact/">contact form</a>.</p>''', keywords="about us")
    simple("contact/", "Contact", "Questions, corrections, partnerships, sponsorship or interest in the website/domain — one form, answered within two business days.",
      '''<div class="card"><form class="form" data-form="Contact"><input type="text" name="_honey" style="display:none" tabindex="-1"><div class="row"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div><label>Topic</label><select name="subject"><option>General question</option><option>Correction / update to a ranking</option><option>Sponsorship / advertising</option><option>Partnership</option><option>This website / domain name</option><option>Press</option><option>Content removal / DMCA</option><option>Other</option></select><label>Message</label><textarea name="message" rows="5" required></textarea><button class="btn primary" type="submit">Send message</button><div class="ok">Sent.</div></form><p class="small muted" style="margin-top:12px">Or <a data-contact data-subject="Message via 7Blockchain.com contact page" href="#">open a pre-addressed email</a>. For website, domain, sponsorship, advertising or partnership interest you can also use <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a>.</p></div>''', keywords="contact email inquiry", aside=False)
    simple("how-we-rank/", "How We Rank: the 7-Metric Method", "Every Top-7 pick is scored 0–10 on seven metrics with equal weight. Here is exactly how.",
      '''<h2>The seven metrics</h2><table><tr><th>Metric</th><th>What we look at</th></tr><tr><td>Security</td><td>Breach history, proof-of-reserves/audits, custody model, regulatory standing</td></tr><tr><td>Fees</td><td>Published base-tier fees, spreads, withdrawal and hidden costs</td></tr><tr><td>Ease of use</td><td>Onboarding, app quality, clarity of the primary task</td></tr><tr><td>Assets</td><td>Breadth and relevance of supported coins/chains/integrations</td></tr><tr><td>Features</td><td>Depth beyond the basic task (staking, derivatives, DeFi, reporting)</td></tr><tr><td>Support</td><td>Channels, responsiveness, documentation</td></tr><tr><td>Reputation</td><td>Longevity, transparency, community and press track record</td></tr></table>
<h2>Scoring</h2><p>Each metric scores 0–10; the overall score is the mean, shown to one decimal. Ties are broken by Security. We re-score each list at least quarterly and whenever a material event (breach, fee change, regulatory action) occurs. Figures are indicative on the date shown; verify on the provider site.</p>
<h2>Independence</h2><p>Affiliate relationships and sponsorships never change a score or a position. Paid placements are labelled "Promoted" or "Presented by" and sit outside the ranked seven. Analysts disclose holdings in the products they score.</p>
<h2>Disagree?</h2><p>Good. Every metric is shown on the page so you can reweight it yourself. Send corrections through the <a href="../contact/">contact form</a>.</p>''', keywords="methodology how we rank scores")
    simple("editorial-policy/", "Editorial Policy", "Accuracy, independence, corrections and the line between editorial and paid content.",
      '''<p><b>Accuracy.</b> We cite primary sources (official docs, fee schedules, audits, on-chain data) and date every page. <b>Independence.</b> Editorial decisions are made without advertiser input; see <a href="../how-we-rank/">how we rank</a>. <b>Paid content.</b> Sponsored, promoted and affiliate content is labelled. <b>Corrections.</b> Material errors are fixed and noted on the page within 48 hours of verification. <b>Not advice.</b> Nothing here is financial, legal or tax advice. <b>Contact.</b> Use the <a href="../contact/">contact form</a>.</p>''', keywords="editorial policy")
    simple("affiliate-disclosure/", "Affiliate & Advertising Disclosure", "How we earn commissions and why it never changes a ranking.",
      '''<p>7Blockchain.com participates in affiliate programmes operated by exchanges, wallet makers, tax-software vendors and other services. When you open an account or buy through a "Visit" or similar link, we may receive a commission at no extra cost to you. Links that may be compensated are marked with <code>rel="sponsored"</code>. We also display advertising served by Google AdSense and sell labelled sponsorships. None of these relationships affect scores, positions or editorial opinions — see <a href="../how-we-rank/">how we rank</a>. Not all providers we rank have an affiliate programme with us; some of our top picks pay us nothing.</p>''', keywords="affiliate disclosure")
    simple("privacy/", "Privacy Policy", "What we collect, what third parties collect, and your choices.",
      f'''<p><b>Data we collect.</b> When you submit a form (newsletter, contact, contest, application, donation notice) we receive what you type, plus the page URL and time. Forms open your email client or post to a form service you can see in the request; we never sell your data. <b>Cookies and advertising.</b> We use Google AdSense, which uses cookies to serve ads based on prior visits; you can opt out at <a href="https://www.google.com/settings/ads" rel="noopener" target="_blank">Google Ads Settings</a> and <a href="https://www.aboutads.info" rel="noopener" target="_blank">aboutads.info</a>. Optional analytics (Google Analytics 4) may be enabled. <b>Local storage.</b> Your theme choice, consent acknowledgement and newsletter-subscribed flag are stored in your browser only. <b>Third-party embeds.</b> YouTube (privacy-enhanced mode), CoinGecko and alternative.me APIs receive your IP address when pages load their data. <b>Your rights.</b> Request access or deletion through the <a href="../contact/">contact form</a>. <b>Children.</b> This site is not directed at children under 16. Updated {TODAY}.</p>''', keywords="privacy policy cookies")
    simple("terms/", "Terms of Use", "The rules for using 7Blockchain.com.",
      '''<p>By using this site you agree to these terms. Content is provided "as is" for educational purposes without warranties. We are not liable for losses arising from reliance on any content, link, tool output or third-party service. Tools are calculators, not advice; verify results independently. You may not scrape, republish or frame content without permission; short quotations with attribution and a link are welcome. Contests are governed by the rules on the contest page. Links to third-party sites are provided for convenience; we do not control them. These terms are governed by the laws applicable to the operator's jurisdiction. Questions: <a href="../contact/">contact form</a>.</p>''', keywords="terms of use")
    simple("disclaimer/", "Risk Disclaimer", "Crypto assets are volatile and unregulated in many places. Read this before acting on anything here.",
      '''<p>Nothing on 7Blockchain.com is financial, investment, legal or tax advice, and no content constitutes a recommendation to buy, sell or hold any asset. Crypto-asset prices can fall to zero; past performance is not indicative of future results. Rankings, scores and figures are editorial opinions based on information believed accurate on the date shown and may be outdated. Yields, fees, rewards and availability change without notice. Do your own research and consider consulting a licensed professional. You are solely responsible for your decisions.</p>''', keywords="risk disclaimer not financial advice")
    simple("trademark/", "Trademark & Copyright Disclosure", "Our independence, how third-party marks are used, and how to request content changes.",
      '''<h2>Independence</h2><p>7Blockchain.com is an independent online publication. It is not affiliated with, endorsed by, sponsored by, or connected to any company, product, protocol, foundation or organisation that uses "7", "Seven", "Blockchain" or "7 Blockchain" in its name, branding or trademarks. The name of this website is a domain name used descriptively: "blockchain" is a generic term for the technology we cover, and "7" describes our seven-item editorial format.</p>
<h2>Third-party trademarks</h2><p>Names such as Bitcoin, Ethereum, Coinbase, Binance, Kraken, Ledger, Trezor, MetaMask and all other product, company and protocol names referenced on this site are trademarks or registered trademarks of their respective owners. They are used nominatively, solely to identify, describe, compare and review the products and services concerned. No logos are hosted by us. Use of a name does not imply any endorsement of this site by the owner, or of the owner by this site.</p>
<h2>Our content</h2><p>Original text, scores, methodology, tools and design are © 7Blockchain.com. Short quotations with attribution and a link are permitted; wholesale reproduction is not. Embedded videos belong to their creators and are shown under YouTube's embed terms; price data is provided by third-party APIs under their terms.</p>
<h2>Requests</h2><p>Trademark owners who believe a reference is inaccurate, and copyright owners who believe content infringes their rights, may submit a notice (identifying the work, the URL, and your contact details) through the <a href="../contact/">contact form</a> selecting "Content removal / DMCA". We act on valid notices promptly.</p>''', keywords="trademark copyright disclosure dmca")

# ---------------------------------------------------------------- MISC FILES
def misc():
    write("go/index.html", '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting… | 7Blockchain.com</title><meta name="robots" content="noindex"><script src="../assets/js/config.js"></script><script>
var k=new URLSearchParams(location.search).get("to");var u=(window.SITE&&window.SITE.go&&window.SITE.go[k])||"../";document.write('<p style="font-family:sans-serif;padding:40px">Redirecting to <a href="'+u+'">'+u+'</a>…</p>');location.replace(u);</script></head><body></body></html>''')
    write("404.html", page("/", "404", "Page not found | 7Blockchain.com", "That page doesn't exist.", '<section class="hero"><div class="wrap"><h1>404 — not one of our sevens</h1><p class="lede">The page moved or never existed. Try the search, or start here:</p><div class="cta-row"><a class="btn primary" href="/">Home</a><a class="btn ghost" href="/top7/">Top 7 rankings</a><a class="btn ghost" href="/learn/">Learn</a></div></div></section>', sticky_cta=False).replace('href="/assets','href="/assets'))
    write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f5b400"/><stop offset="1" stop-color="#7c5cff"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="url(#g)"/><text x="32" y="46" font-family="Inter,Arial,sans-serif" font-size="40" font-weight="900" fill="#fff" text-anchor="middle">7</text></svg>')
    write("og.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0f1a"/><stop offset="1" stop-color="#1b1230"/></linearGradient><linearGradient id="a" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f5b400"/><stop offset="1" stop-color="#a48cff"/></linearGradient></defs><rect width="1200" height="630" fill="url(#g)"/><rect x="80" y="150" width="140" height="140" rx="30" fill="url(#a)"/><text x="150" y="252" font-family="Inter,Arial,sans-serif" font-size="100" font-weight="900" fill="#fff" text-anchor="middle">7</text><text x="250" y="230" font-family="Inter,Arial,sans-serif" font-size="72" font-weight="900" fill="#fff">7Blockchain.com</text><text x="250" y="300" font-family="Inter,Arial,sans-serif" font-size="36" fill="#9aa5bf">Everything in blockchain, ranked and explained in sevens.</text><text x="80" y="520" font-family="Inter,Arial,sans-serif" font-size="30" fill="url(#a)" font-weight="700">Top 7 rankings · 7-step course · tools · 7-in-7 digest</text></svg>')
    write("manifest.json", json.dumps({"name": "7Blockchain.com", "short_name": "7Blockchain", "start_url": "/", "display": "standalone", "background_color": "#0b0f1a", "theme_color": "#0b0f1a", "icons": [{"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=1))
    write("robots.txt", "User-agent: *\nAllow: /\nDisallow: /go/\nSitemap: https://7blockchain.com/sitemap.xml\n")
    write("CNAME", "7blockchain.com\n")
    write("ads.txt", "# Replace with your Google AdSense line, e.g.:\n# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n")
    write(".nojekyll", "")
    urls = "".join(f"<url><loc>{SITE_URL}/{p}</loc><lastmod>{TODAY}</lastmod><changefreq>{'daily' if p=='' else 'weekly'}</changefreq><priority>{'1.0' if p=='' else '0.8' if p.count('/')==1 else '0.6'}</priority></url>" for p, *_ in PAGES)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    write("data/site-index.json", json.dumps([{"u": p, "t": t.replace(" | 7Blockchain.com", ""), "d": d, "k": k} for p, t, d, k in PAGES]))
    write(".github/workflows/pages.yml", '''name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configure Pages (enables Pages on first run)
        uses: actions/configure-pages@v5
        with:
          enablement: true
      - uses: actions/upload-pages-artifact@v3
        with:
          path: .
      - id: deployment
        uses: actions/deploy-pages@v4
''')
    write("README.md", f'''# 7Blockchain.com

Static, dependency-free website for **7blockchain.com** — "Everything in blockchain, ranked and explained in sevens."
Hosted free on GitHub Pages. Built {TODAY}.

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
''')

if __name__ == "__main__":
    home(); learn(); top7(); tools(); glossary(); videos(); digest(); start(); newsletter(); support(); contests(); careers(); advertise(); about_contact_legal(); misc()
    print(f"Built {len(PAGES)} pages into {OUT}")
