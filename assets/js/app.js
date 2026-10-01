/* 7Blockchain.com — site runtime (vanilla JS, no dependencies) */
(function () {
  const S = window.SITE || {};
  const $ = (q, c) => (c || document).querySelector(q);
  const $$ = (q, c) => Array.from((c || document).querySelectorAll(q));
  const ROOT = document.documentElement.getAttribute("data-root") || "/";
  const store = {
    get: (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- Theme ---------- */
  const saved = store.get("theme");
  if (saved) document.documentElement.setAttribute("data-theme", saved);
  $$("[data-theme-toggle]").forEach(b => b.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", cur); store.set("theme", cur);
  }));

  /* ---------- Mobile menu ---------- */
  const burger = $("#burger"), mm = $("#mobilemenu");
  if (burger && mm) burger.addEventListener("click", () => mm.classList.toggle("open"));

  /* ---------- Active nav ---------- */
  const path = location.pathname.replace(/index\.html$/, "");
  $$(".menu a").forEach(a => { const h = a.getAttribute("href"); if (h && h !== ROOT && path.startsWith(h)) a.classList.add("active"); });

  /* ---------- Contact pipeline (address assembled at runtime, never printed) ---------- */
  function addr() { try { return atob(S.contactKey || "").split("").reverse().join(""); } catch (e) { return ""; } }
  function mailto(subject, body) {
    return "mailto:" + addr() + "?subject=" + encodeURIComponent(subject || "Inquiry via 7Blockchain.com") + (body ? "&body=" + encodeURIComponent(body) : "");
  }
  $$("[data-contact]").forEach(a => {
    const subj = a.getAttribute("data-subject") || "Inquiry via 7Blockchain.com";
    a.setAttribute("href", "#"); a.setAttribute("rel", "nofollow");
    a.addEventListener("click", (e) => { e.preventDefault(); location.href = mailto(subj, a.getAttribute("data-body") || ""); });
  });
  $$("form[data-form]").forEach(f => {
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      const kind = f.getAttribute("data-form") || "Form";
      const data = new FormData(f); const lines = [];
      data.forEach((v, k) => { if (k !== "_honey" && String(v).trim()) lines.push(k.replace(/_/g, " ") + ": " + v); });
      if (data.get("_honey")) return; // bot
      lines.push("", "Page: " + location.href, "Sent: " + new Date().toISOString());
      const subject = "[7Blockchain.com] " + kind + (data.get("subject") ? " — " + data.get("subject") : "");
      const ok = $(".ok", f);
      if (S.formEndpoint) {
        try {
          const r = await fetch(S.formEndpoint, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(Object.assign({ _subject: subject, _page: location.href }, Object.fromEntries(data))) });
          if (r.ok) { if (ok) ok.style.display = "block"; f.reset(); toast("Sent. Thank you!"); if (kind.toLowerCase().includes("newsletter")) store.set("subscribed", "1"); return; }
        } catch (err) { /* fall through to mailto */ }
      }
      location.href = mailto(subject, lines.join("\n"));
      if (ok) ok.style.display = "block";
      if (kind.toLowerCase().includes("newsletter")) store.set("subscribed", "1");
      toast("Opening your mail app…");
    });
  });

  /* ---------- Toast ---------- */
  let tt; function toast(m) { let t = $(".toast"); if (!t) { t = document.createElement("div"); t.className = "toast"; document.body.appendChild(t); } t.textContent = m; t.style.display = "block"; clearTimeout(tt); tt = setTimeout(() => t.style.display = "none", 3200); }
  window.toast = toast;

  /* ---------- Copy buttons ---------- */
  $$("[data-copy]").forEach(b => b.addEventListener("click", () => { const v = b.getAttribute("data-copy"); navigator.clipboard && navigator.clipboard.writeText(v).then(() => toast("Copied")); }));

  /* ---------- Ads (gated by config) ---------- */
  if (S.adsenseClient) {
    const s = document.createElement("script"); s.async = true; s.crossOrigin = "anonymous";
    s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + S.adsenseClient; document.head.appendChild(s);
    $$(".ad[data-slot]").forEach(a => {
      const slot = S.adSlots[a.getAttribute("data-slot")]; if (!slot) return;
      a.setAttribute("data-live", "1"); a.innerHTML = '<ins class="adsbygoogle" style="display:block;width:100%" data-ad-client="' + S.adsenseClient + '" data-ad-slot="' + slot + '" data-ad-format="auto" data-full-width-responsive="true"></ins>';
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
  }
  if (S.ga4) { const g = document.createElement("script"); g.async = true; g.src = "https://www.googletagmanager.com/gtag/js?id=" + S.ga4; document.head.appendChild(g); window.dataLayer = window.dataLayer || []; function gtag() { dataLayer.push(arguments); } gtag("js", new Date()); gtag("config", S.ga4); }

  /* ---------- Live ticker (CoinGecko public API) ---------- */
  const ticker = $("#ticker-track");
  if (ticker) {
    const ids = "bitcoin,ethereum,solana,binancecoin,ripple,cardano,avalanche-2,chainlink,polkadot,the-open-network";
    fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=" + ids + "&price_change_percentage=24h")
      .then(r => r.json()).then(list => {
        const html = list.map(c => { const ch = c.price_change_percentage_24h || 0; return '<span class="coin"><b>' + c.symbol.toUpperCase() + '</b> $' + fmt(c.current_price) + ' <span class="' + (ch >= 0 ? "up" : "down") + '">' + (ch >= 0 ? "▲" : "▼") + Math.abs(ch).toFixed(2) + '%</span></span>'; }).join("");
        ticker.innerHTML = html + html; window.PRICES = Object.fromEntries(list.map(c => [c.id, c.current_price]));
        document.dispatchEvent(new Event("prices"));
      }).catch(() => { ticker.innerHTML = '<span class="coin muted">Live prices unavailable right now.</span>'; });
  }
  function fmt(n) { return n >= 1000 ? n.toLocaleString(undefined, { maximumFractionDigits: 0 }) : n >= 1 ? n.toFixed(2) : n.toPrecision(3); }
  window.fmtNum = fmt;

  /* ---------- Fear & Greed ---------- */
  const fg = $("#feargreed");
  if (fg) fetch("https://api.alternative.me/fng/?limit=1").then(r => r.json()).then(d => { const v = d.data[0]; fg.innerHTML = '<div class="dial">' + v.value + '</div><div><b>' + v.value_classification + '</b><br><span class="small muted">Crypto Fear &amp; Greed Index</span></div>'; }).catch(() => fg.innerHTML = '<span class="muted small">Index unavailable</span>');

  /* ---------- Search (site index) ---------- */
  const si = $("#site-search"); const sr = $("#search-results");
  if (si && sr) {
    let idx = null;
    const load = () => { if (!idx) fetch(ROOT + "data/site-index.json").then(r => r.json()).then(j => { idx = j; if (si.value) si.dispatchEvent(new Event("input")); }); };
    si.addEventListener("focus", load); setTimeout(load, 1500);
    si.addEventListener("input", () => {
      const q = si.value.trim().toLowerCase(); const box = si.closest(".search");
      if (!q || !idx) { box.classList.remove("open"); return; }
      const hits = idx.filter(p => (p.t + " " + p.d + " " + (p.k || "")).toLowerCase().includes(q)).slice(0, 8);
      sr.innerHTML = hits.map(h => '<a href="' + ROOT + h.u + '">' + h.t + '<small>' + h.d + '</small></a>').join("") || '<a>No results</a>';
      box.classList.add("open");
    });
    document.addEventListener("click", (e) => { if (!e.target.closest(".search")) si.closest(".search").classList.remove("open"); });
    document.addEventListener("keydown", (e) => { if (e.key === "/" && document.activeElement.tagName !== "INPUT") { e.preventDefault(); si.focus(); } });
  }

  /* ---------- YouTube facade ---------- */
  $$(".yt").forEach(y => {
    const id = y.getAttribute("data-id");
    y.style.backgroundImage = "url(https://i.ytimg.com/vi/" + id + "/hqdefault.jpg)";
    y.addEventListener("click", () => { y.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0" title="YouTube video" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'; });
  });
  $$("[data-yt-sub]").forEach(a => a.href = (S.youtubeChannel || "#") + "?sub_confirmation=1");

  /* ---------- Sortable tables ---------- */
  $$("table.cmp").forEach(t => $$("th", t).forEach((th, i) => th.addEventListener("click", () => {
    const rows = $$("tbody tr", t); const asc = th.getAttribute("data-asc") !== "1"; th.setAttribute("data-asc", asc ? "1" : "0");
    rows.sort((a, b) => { const x = a.children[i].getAttribute("data-v") || a.children[i].textContent, y = b.children[i].getAttribute("data-v") || b.children[i].textContent; const nx = parseFloat(x), ny = parseFloat(y); return (!isNaN(nx) && !isNaN(ny)) ? (asc ? nx - ny : ny - nx) : (asc ? x.localeCompare(y) : y.localeCompare(x)); });
    rows.forEach(r => t.tBodies[0].appendChild(r));
  })));

  /* ---------- Outbound /go/ links ---------- */
  $$("a[data-go]").forEach(a => { const k = a.getAttribute("data-go"); a.href = (S.go && S.go[k]) || a.href; a.target = "_blank"; a.rel = "nofollow sponsored noopener"; });

  /* ---------- Countdown ---------- */
  $$("[data-countdown]").forEach(el => {
    const end = new Date(el.getAttribute("data-countdown")).getTime();
    function tick() { let d = Math.max(0, end - Date.now()); const D = Math.floor(d / 864e5), H = Math.floor(d % 864e5 / 36e5), M = Math.floor(d % 36e5 / 6e4), Ss = Math.floor(d % 6e4 / 1e3); el.innerHTML = [[D, "days"], [H, "hours"], [M, "min"], [Ss, "sec"]].map(x => "<div><b>" + x[0] + "</b><span>" + x[1] + "</span></div>").join(""); }
    tick(); setInterval(tick, 1000);
  });

  /* ---------- Donation config ---------- */
  const dn = S.donate || {};
  $$("[data-addr]").forEach(el => { const v = dn[el.getAttribute("data-addr")] || ""; el.textContent = v; const b = el.parentElement.querySelector("[data-copy]"); if (b) b.setAttribute("data-copy", v); const q = el.closest(".card") && el.closest(".card").querySelector(".qr"); if (q && v && !/REPLACE/.test(v)) q.innerHTML = '<img alt="QR code" src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=' + encodeURIComponent(v) + '">'; });
  $$("[data-link]").forEach(a => { const v = dn[a.getAttribute("data-link")]; if (v) { a.href = v; a.target = "_blank"; a.rel = "noopener"; } else a.style.display = "none"; });
  const goal = $("#goal"); if (goal) { const pct = Math.min(100, Math.round((dn.goalRaised || 0) / (dn.goalTarget || 1) * 100)); goal.innerHTML = '<div class="small muted">' + (dn.goalLabel || "") + '</div><div class="bar"><i style="width:' + pct + '%"></i></div><div class="small">$' + (dn.goalRaised || 0).toLocaleString() + ' raised of $' + (dn.goalTarget || 0).toLocaleString() + ' (' + pct + '%)</div>'; }

  /* ---------- Contest config ---------- */
  const ct = S.contest; const cbox = $("#contest-box");
  if (cbox && ct) { if (!ct.active) cbox.innerHTML = '<p class="muted">No contest is running right now. Subscribe to the digest to hear about the next one.</p>'; else { $("#c-title") && ($("#c-title").textContent = ct.title); $("#c-prize") && ($("#c-prize").textContent = ct.prize); $("#c-rules") && ($("#c-rules").textContent = ct.rules); $("#c-sponsor") && ($("#c-sponsor").textContent = ct.sponsor); const cd = $("#c-countdown"); if (cd) { cd.setAttribute("data-countdown", ct.deadline); const end = new Date(ct.deadline).getTime(); const tick = () => { let d = Math.max(0, end - Date.now()); cd.innerHTML = [[Math.floor(d / 864e5), "days"], [Math.floor(d % 864e5 / 36e5), "hours"], [Math.floor(d % 36e5 / 6e4), "min"], [Math.floor(d % 6e4 / 1e3), "sec"]].map(x => "<div><b>" + x[0] + "</b><span>" + x[1] + "</span></div>").join(""); }; tick(); setInterval(tick, 1000); } } }

  /* ---------- Social links ---------- */
  const soc = $("#socials"); if (soc && S.social) { const L = { x: "X", youtube: "YT", telegram: "TG", linkedin: "in", reddit: "r/", github: "GH" }; soc.innerHTML = Object.entries(S.social).filter(([k, v]) => v).map(([k, v]) => '<a href="' + v + '" target="_blank" rel="noopener" title="' + k + '">' + L[k] + '</a>').join(""); }

  /* ---------- Exit-intent / timed slide-in (once per session) ---------- */
  const sl = $("#slidein");
  if (sl && !store.get("subscribed") && !sessionStorage.getItem("slidein")) {
    const show = () => { if (sessionStorage.getItem("slidein")) return; sl.classList.add("show"); sessionStorage.setItem("slidein", "1"); };
    setTimeout(show, 45000); document.addEventListener("mouseleave", (e) => { if (e.clientY < 0) show(); });
    $(".x", sl).addEventListener("click", () => sl.classList.remove("show"));
  }

  /* ---------- Consent notice ---------- */
  const cn = $("#consent"); if (cn && !store.get("consent")) { cn.classList.add("show"); $("button", cn).addEventListener("click", () => { store.set("consent", "1"); cn.classList.remove("show"); }); }

  /* ---------- Reading progress for chapters ---------- */
  const rp = $("#readprog"); if (rp) window.addEventListener("scroll", () => { const h = document.body.scrollHeight - innerHeight; rp.style.width = Math.min(100, scrollY / h * 100) + "%"; });

  /* ---------- Glossary filter ---------- */
  const gf = $("#gloss-filter"); if (gf) gf.addEventListener("input", () => { const q = gf.value.toLowerCase(); $$(".gloss .term").forEach(t => t.style.display = t.textContent.toLowerCase().includes(q) ? "" : "none"); });

  /* ---------- Starter-kit wizard ---------- */
  const wz = $("#wizard");
  if (wz) {
    const ans = {}; const steps = $$(".step", wz); let i = 0;
    $$(".choices button", wz).forEach(b => b.addEventListener("click", () => {
      const k = b.closest(".step").getAttribute("data-key"); ans[k] = b.getAttribute("data-v"); $$("button", b.parentElement).forEach(x => x.classList.remove("sel")); b.classList.add("sel");
      steps[i].classList.remove("active"); i++; if (steps[i]) steps[i].classList.add("active"); if (i === steps.length - 1) render();
    }));
    function render() {
      const us = ans.country === "us", beg = ans.level === "beginner";
      const ex = us ? (beg ? "Coinbase" : "Kraken") : (beg ? "Binance" : "Bybit"); const exk = ex.toLowerCase();
      const wl = ans.goal === "hold" ? "Ledger (hardware)" : ans.goal === "defi" ? "Rabby + Ledger" : "Trust Wallet"; const wk = ans.goal === "hold" ? "ledger" : ans.goal === "defi" ? "rabby" : "trustwallet";
      const ch = beg ? 1 : ans.goal === "defi" ? 6 : ans.goal === "trade" ? 5 : 4;
      $("#wz-out").innerHTML = '<div class="grid g3"><div class="card flat"><span class="badge gold">Exchange</span><h3>' + ex + '</h3><a class="btn sm primary" data-go="' + exk + '" href="#">Visit ' + ex + '</a> <a class="btn sm ghost" href="' + ROOT + 'top7/exchanges/">See Top 7</a></div><div class="card flat"><span class="badge violet">Wallet</span><h3>' + wl + '</h3><a class="btn sm primary" data-go="' + wk + '" href="#">Get it</a> <a class="btn sm ghost" href="' + ROOT + 'top7/wallets/">See Top 7</a></div><div class="card flat"><span class="badge green">Start at</span><h3>Step ' + ch + '</h3><a class="btn sm primary" href="' + ROOT + 'learn/step-' + ch + '/">Open chapter</a></div></div>';
      $$("#wz-out a[data-go]").forEach(a => { a.href = S.go[a.getAttribute("data-go")] || "#"; a.target = "_blank"; a.rel = "nofollow sponsored noopener"; });
      const hid = $("#wz-profile"); if (hid) hid.value = "Country: " + ans.country + " | Level: " + ans.level + " | Goal: " + ans.goal + " | Picks: " + ex + ", " + wl + ", Step " + ch;
    }
  }

  /* ---------- Quiz ---------- */
  const qz = $("#quiz");
  if (qz) {
    const qs = $$(".q", qz); let n = 0, score = 0;
    qs.forEach((q, qi) => $$(".opts button", q).forEach(b => b.addEventListener("click", () => {
      if (q.getAttribute("data-done")) return; q.setAttribute("data-done", "1");
      const ok = b.getAttribute("data-ok") === "1"; if (ok) score++; b.classList.add(ok ? "correct" : "wrong");
      $$(".opts button", q).forEach(x => { if (x.getAttribute("data-ok") === "1") x.classList.add("correct"); });
      $(".why", q).style.display = "block";
      setTimeout(() => { q.classList.remove("active"); n++; if (qs[n]) qs[n].classList.add("active"); else { const r = $("#quiz-result"); r.style.display = "block"; $("#qscore").textContent = score + " / " + qs.length; $("#qmsg").textContent = score === qs.length ? "Perfect score — you qualify for the contest entry!" : score >= 5 ? "Strong. Review the chapters you missed and retake for a perfect 7." : "Start with Step 1 of the 7-step path and come back."; const sc = $("#quiz-score-field"); if (sc) sc.value = score + "/" + qs.length; } }, 1400);
    })));
  }

  /* ---------- Tools ---------- */
  function num(id) { const e = $(id); return e ? parseFloat(e.value) || 0 : 0; }
  const dca = $("#dca-form");
  if (dca) { const run = () => { const amt = num("#dca-amt"), m = num("#dca-months"), r = num("#dca-growth") / 100; let units = 0, price = num("#dca-price") || 1, invested = 0; const g = Math.pow(1 + r, 1 / 12) - 1; for (let k = 0; k < m; k++) { units += amt / price; invested += amt; price *= 1 + g; } const val = units * price; $("#dca-out").innerHTML = '<div class="kpi"><div><span>Total invested</span><b>$' + invested.toLocaleString(undefined, { maximumFractionDigits: 0 }) + '</b></div><div><span>Portfolio value</span><b>$' + val.toLocaleString(undefined, { maximumFractionDigits: 0 }) + '</b></div><div><span>Gain / loss</span><b class="' + (val >= invested ? "hl" : "") + '">' + ((val - invested) / invested * 100).toFixed(1) + '%</b></div><div><span>Avg. buy price</span><b>$' + (invested / units).toLocaleString(undefined, { maximumFractionDigits: 2 }) + '</b></div></div>'; }; dca.addEventListener("input", run); dca.addEventListener("submit", e => { e.preventDefault(); run(); }); document.addEventListener("prices", () => { if (window.PRICES && !$("#dca-price").value) { $("#dca-price").value = window.PRICES.bitcoin; run(); } }); run(); }
  const stk = $("#stake-form");
  if (stk) { const run = () => { const p = num("#st-amt"), apy = num("#st-apy") / 100, y = num("#st-years"), n = num("#st-comp") || 365; const fv = p * Math.pow(1 + apy / n, n * y); const simple = p * (1 + apy * y); $("#st-out").innerHTML = '<div class="kpi"><div><span>Final balance (compounded)</span><b>' + fv.toLocaleString(undefined, { maximumFractionDigits: 2 }) + '</b></div><div><span>Rewards earned</span><b class="hl">' + (fv - p).toLocaleString(undefined, { maximumFractionDigits: 2 }) + '</b></div><div><span>Without compounding</span><b>' + simple.toLocaleString(undefined, { maximumFractionDigits: 2 }) + '</b></div><div><span>Effective APY</span><b>' + ((Math.pow(1 + apy / n, n) - 1) * 100).toFixed(2) + '%</b></div></div>'; }; stk.addEventListener("input", run); stk.addEventListener("submit", e => { e.preventDefault(); run(); }); run(); }
  const pl = $("#pl-form");
  if (pl) { const run = () => { const q = num("#pl-qty"), b = num("#pl-buy"), s = num("#pl-sell"), f = num("#pl-fee") / 100; const cost = q * b * (1 + f), proceeds = q * s * (1 - f), gain = proceeds - cost; $("#pl-out").innerHTML = '<div class="kpi"><div><span>Total cost</span><b>$' + cost.toLocaleString(undefined, { maximumFractionDigits: 2 }) + '</b></div><div><span>Net proceeds</span><b>$' + proceeds.toLocaleString(undefined, { maximumFractionDigits: 2 }) + '</b></div><div><span>Profit / loss</span><b class="' + (gain >= 0 ? "hl" : "") + '">$' + gain.toLocaleString(undefined, { maximumFractionDigits: 2 }) + '</b></div><div><span>Return</span><b>' + (cost ? (gain / cost * 100).toFixed(2) : 0) + '%</b></div><div><span>Break-even sell price</span><b>$' + (q ? (cost / (q * (1 - f))).toLocaleString(undefined, { maximumFractionDigits: 2 }) : 0) + '</b></div></div>'; }; pl.addEventListener("input", run); pl.addEventListener("submit", e => { e.preventDefault(); run(); }); run(); }
  const fee = $("#fee-form");
  if (fee) { const run = () => { const t = num("#fee-trade"), n = num("#fee-n"); const rows = $$("#fee-table tbody tr"); rows.forEach(r => { const mk = parseFloat(r.getAttribute("data-maker")), tk = parseFloat(r.getAttribute("data-taker")); const c = t * n * (tk / 100); r.querySelector(".cost").innerHTML = "<b>$" + c.toLocaleString(undefined, { maximumFractionDigits: 2 }) + "</b>"; r.querySelector(".cost").setAttribute("data-v", c); r.querySelector(".costm").textContent = "$" + (t * n * mk / 100).toLocaleString(undefined, { maximumFractionDigits: 2 }); }); rows.sort((a, b) => parseFloat(a.querySelector(".cost").getAttribute("data-v")) - parseFloat(b.querySelector(".cost").getAttribute("data-v"))).forEach(r => $("#fee-table tbody").appendChild(r)); }; fee.addEventListener("input", run); fee.addEventListener("submit", e => { e.preventDefault(); run(); }); run(); }
  const cv = $("#conv-form");
  if (cv) { const run = () => { const a = num("#cv-amt"), c = $("#cv-coin").value; const p = window.PRICES && window.PRICES[c]; $("#cv-out").innerHTML = p ? '<b>$' + (a * p).toLocaleString(undefined, { maximumFractionDigits: 2 }) + '</b> <span class="muted small">at $' + fmt(p) + ' per coin (live)</span>' : '<span class="muted">Loading live price…</span>'; }; cv.addEventListener("input", run); document.addEventListener("prices", run); run(); }

  /* ---------- Sticky mobile bar ---------- */
  if ($(".stickybar")) document.body.classList.add("has-stickybar");

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(e => e.textContent = new Date().getFullYear());
})();
