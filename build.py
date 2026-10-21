#!/usr/bin/env python3
"""Builds agriculture.gujaratbio.com (later www.gujaratbio.com): plain HTML, no dependencies.
Edit the content_*.py files, then run: python3 build.py
Photos/videos: put files with the exact names listed in MEDIA_LIST.csv into assets/media/ and rebuild."""
import os, json, html as H, re, csv
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://agriculture.gujaratbio.com"   # change to https://www.gujaratbio.com at launch
TRIAL = True                                   # True: every page is noindex and a trial notice shows
OLD_SITE = "https://en.gujaratbio.com"
B2B = "https://b2b.gujaratbio.com"
GTM_ID = "GTM-5JDXGL2S"
WA = "919978791167"; PHONE = "+91 99787 91167"; TEL = "+919978791167"; MAIL = "sales@gujaratbio.com"
NAME = "Gujarat Bio Organics Pvt. Ltd."; SHORT = "Gujarat Bio Organics"
CIN = "U24123GJ2009PTC058701"
FACTORY = "Plot No. 321, GIDC 2, Ghanghali Road, Shihor, Bhavnagar, Gujarat 364240"
REGOFF = "First Floor, 110 Shoppers Plaza, Parimal Chowk, Waghawadi Road, Bhavnagar, Gujarat 364002"
SOCIAL = ["https://www.facebook.com/gujaratbio", "https://www.youtube.com/@Gujaratbio"]
RESULTS = "Results differ from farm to farm with soil, weather, crop and management. Farmer experiences on this site are their own reports, not a promise of results."

for _f in ("content_products.py", "content_crops.py", "content_crops2.py", "content_knowledge.py", "content_pages.py"):
    exec(open(os.path.join(ROOT, _f), encoding="utf-8").read())

def esc(s): return H.escape(str(s), quote=True)
def wa(msg): return f"https://wa.me/{WA}?text={quote(msg)}"
def cap(s): return s[0].upper() + s[1:]
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1-.7-.3-1.5-.7-2.2-1.5-.6-.5-1-1.2-1.2-1.4-.1-.2 0-.4.1-.5l.4-.4.3-.5v-.5l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
TEL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'
def btn_wa(msg, label="WhatsApp us"): return f'<a class="btn btn-wa" href="{wa(msg)}" data-ev="click_whatsapp">{WA_SVG}{esc(label)}</a>'
def btn_call(label="Call us"): return f'<a class="btn btn-line" href="tel:{TEL}" data-ev="click_phone">{TEL_SVG}{esc(label)}</a>'
def btn_enq(label="Send enquiry", q=""): return f'<a class="btn btn-leaf" href="/enquiry{q}" data-ev="begin_enquiry">{esc(label)}</a>'

# ---------------------------------------------------------------- media slots
MEDIA = []  # (file, kind, description, page)
_CUR = {"page": "/"}
def media(fname, desc, kind="img", cls=""):
    """A named photo/video slot. If assets/media/<fname> exists it is shown; otherwise a labelled placeholder."""
    MEDIA.append((fname, kind, desc, _CUR["page"]))
    path = os.path.join(ROOT, "assets", "media", fname)
    if os.path.exists(path):
        if kind == "video":
            return f'<div class="media {cls}"><video controls preload="none" playsinline src="/assets/media/{fname}" aria-label="{esc(desc)}"></video></div>'
        return f'<div class="media {cls}"><img src="/assets/media/{fname}" alt="{esc(desc)}" loading="lazy"></div>'
    label = "Video coming soon" if kind == "video" else "Photo coming soon"
    return f'<div class="slot {"video " if kind == "video" else ""}{cls}" role="img" aria-label="{esc(label + ": " + desc)}"><span>{label}</span><span class="fn">{esc(fname)}</span><span class="ds">{esc(desc)}</span></div>'

def pimg(p, w=None):
    f = os.path.join(ROOT, "assets", "img", "products", p["slug"] + ".webp")
    if os.path.exists(f):
        return f'<img src="/assets/img/products/{p["slug"]}.webp" alt="{esc(p["name"])} bottle" loading="lazy">'
    MEDIA.append((p["slug"] + ".webp", "img", f"Product photo of {p['name']} pack on white background (save in assets/img/products/)", _CUR["page"]))
    return f'<span class="noimg">{esc(p["slug"])}.webp</span>'

# ---------------------------------------------------------------- navigation
CRP = sorted(CROPS, key=lambda c: c["name"])
NAV = [("/", "Home", None),
       ("/crops", "Crops", [(f"/crops/{c['slug']}", c["name"]) for c in CRP]),
       ("/products", "Products", [(f"/products#{g}", t) for g, t, _ in GROUPS]),
       ("/farmer-stories", "Farmer Stories", None),
       ("/knowledge", "Knowledge", [("/crop-problems", "Crop problems"), ("/knowledge/soil-health", "Soil health"), ("/knowledge/soil-fertility", "Soil fertility"),
                                    ("/knowledge/sustainability", "Sustainability and the 5 Rs"), ("/guides", "Farming guides"), ("/articles", "Articles")]),
       ("/about", "About", [("/about", "About us"), ("/our-story", "Our story: since 2006"), ("/our-impact", "Our impact"), ("/quality", "Quality and approvals"), ("/factory-and-rd", "Factory and R&D")]),
       ("/dealers", "Dealers & Bulk", [("/dealers", "Become a dealer"), ("/bulk-buyers", "Bulk buyers"), ("/oem-private-label", "Need OEM or private label?"), ("/where-to-buy", "Where to buy")])]

def header(path):
    items = []
    for h, t, sub in NAV:
        cur = ' aria-current="page"' if (path == h or (h != "/" and path.startswith(h))) else ""
        s = ""
        if sub:
            s = f'<div class="sub{" wide" if len(sub) > 8 else ""}">' + "".join(f'<a href="{u}">{esc(n)}</a>' for u, n in sub) + "</div>"
        items.append(f'<div class="ni"><a href="{h}"{cur}>{t}</a>{s}</div>')
    trial = '<span class="t">Trial version of the new website.</span>' if TRIAL else "<span></span>"
    return f'''<a class="skip" href="#main">Skip to content</a><div class="strip"><div class="wrap">{trial}<span><a href="tel:{TEL}">{PHONE}</a> &middot; <a href="{OLD_SITE}" rel="nofollow">Want to see our old website? Click here</a></span></div></div>
<header class="top"><div class="wrap"><a class="brand" href="/"><img src="/assets/img/brand/gbo-logo.webp" alt="Gujarat Bio Organics logo" width="46" height="46"><span class="bt"><b>Gujarat Bio Organics</b><span>Working with farmers since 2006</span></span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button><nav class="nav" id="nav" aria-label="Main">{"".join(items)}<a class="enq" href="/enquiry" data-ev="begin_enquiry">Send enquiry</a></nav></div></header>'''

def footer():
    crops = "".join(f'<li><a href="/crops/{c["slug"]}">{c["name"]}</a></li>' for c in CRP[:10])
    return f'''<div class="biz"><div class="wrap"><h2>Bulk buyer, manufacturer or brand?</h2><p>Need bulk supply, OEM or private label? Our business site has grades, specifications and export terms.</p>
<div class="btns"><a class="btn" href="/bulk-buyers">Bulk buyers</a><a class="btn" href="/dealers">Become a dealer</a><a class="btn" href="{B2B}/private-label-oem?utm_source=agriculture.gujaratbio.com&amp;utm_medium=referral&amp;utm_campaign=farmer_site">OEM and private label</a></div></div></div>
<footer class="foot"><div class="wrap"><div class="cols">
<div><img src="/assets/img/brand/gbo-logo.webp" alt="" width="70" height="70" style="background:#fff;border-radius:12px;padding:4px"><h2>{NAME}</h2><p>Biostimulants, biofertilizers and organic fertilizers, made in Bhavnagar, Gujarat. Working with farmers since 2006.</p>
<p>Factory: {FACTORY}<br>Office: {REGOFF}<br>CIN {CIN}</p><p><a href="tel:{TEL}">{PHONE}</a> &middot; <a href="mailto:{MAIL}">{MAIL}</a></p>
<p><a href="{SOCIAL[0]}" rel="noopener">Facebook</a> &middot; <a href="{SOCIAL[1]}" rel="noopener">YouTube</a></p></div>
<div><h2>Crops</h2><ul>{crops}<li><a href="/crops">All crops</a></li></ul></div>
<div><h2>Immunity</h2><ul>{"".join(f'<li><a href="/products#{g}">{t}</a></li>' for g, t, _ in GROUPS)}<li><a href="/where-to-buy">Where to buy</a></li><li><a href="/enquiry">Send enquiry</a></li></ul></div>
<div><h2>Company</h2><ul><li><a href="/about">About us</a></li><li><a href="/our-story">Our story</a></li><li><a href="/our-impact">Our impact</a></li><li><a href="/quality">Quality and approvals</a></li><li><a href="/farmer-stories">Farmer stories</a></li><li><a href="/knowledge">Knowledge</a></li><li><a href="/dealers">Dealers</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy-policy">Privacy</a></li><li><a href="/terms">Terms</a></li><li><a href="/shipping-and-returns">Shipping and returns</a></li><li><a href="{OLD_SITE}" rel="nofollow">Old website</a></li></ul></div>
</div><p class="note" style="color:#bfb3a5;margin-top:20px">{RESULTS}</p><p class="note" style="color:#bfb3a5">&copy; 2026 {NAME}. Immunity is a brand of {SHORT}.</p></div></footer>
<nav class="bar" aria-label="Quick contact"><a class="c" href="tel:{TEL}" data-ev="click_phone">Call</a><a class="w" href="{wa("Hello Gujarat Bio Organics, I need help with my crop.")}" data-ev="click_whatsapp">WhatsApp</a></nav>'''

def tracking():
    js = ("window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}"
          "(function(){var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}"
          "var eu=/^(Europe\\/|Atlantic\\/(Canary|Madeira|Azores|Faroe|Reykjavik))/.test(tz);var v=eu?'denied':'granted';"
          "gtag('consent','default',{ad_storage:v,ad_user_data:v,ad_personalization:v,analytics_storage:v});"
          "dataLayer.push({site_section:'farmer_site'});"
          "(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
          "var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f)})"
          f"(window,document,'script','dataLayer','{GTM_ID}')}})();")
    return "<script>" + js + "</script>"

FONT = "https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Mukta:wght@400;600;700&display=swap"
CSS = re.sub(r"\s*([{};:,>])\s*", r"\1", re.sub(r"/\*.*?\*/", "", open(os.path.join(ROOT, "assets", "site.css"), encoding="utf-8").read(), flags=re.S)).replace(";}", "}")
JS = ("document.querySelector('.menu-btn')?.addEventListener('click',function(){var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)});"
      "document.addEventListener('click',function(e){var a=e.target.closest('[data-ev]');if(a){window.dataLayer=window.dataLayer||[];dataLayer.push({event:a.dataset.ev,link_url:a.href||'',page_path:location.pathname})}});"
      "var F=document.getElementById('enqform');if(F){var q=new URLSearchParams(location.search);['crop','product','type'].forEach(function(k){var v=q.get(k);if(v&&F[k])F[k].value=v});"
      "F.addEventListener('submit',function(e){e.preventDefault();var d=new FormData(F),m='Hello Gujarat Bio Organics, I am sending an enquiry from your website.';"
      "d.forEach(function(v,k){if(v)m+='\\n'+k.charAt(0).toUpperCase()+k.slice(1)+': '+v});window.dataLayer=window.dataLayer||[];dataLayer.push({event:'generate_lead',enquiry_type:d.get('type')||''});"
      f"location.href='https://wa.me/{WA}?text='+encodeURIComponent(m)}})}}")

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": SITE + "/#org", "name": NAME, "alternateName": ["Gujarat Bio Organics", "GBO"],
       "url": SITE + "/", "logo": SITE + "/assets/img/brand/gbo-logo.png", "foundingDate": "2006", "email": MAIL, "telephone": TEL, "sameAs": SOCIAL + [B2B + "/"],
       "address": {"@type": "PostalAddress", "streetAddress": "Plot No. 321, GIDC 2, Ghanghali Road, Shihor", "addressLocality": "Bhavnagar", "addressRegion": "Gujarat", "postalCode": "364240", "addressCountry": "IN"},
       "brand": {"@type": "Brand", "name": "Immunity", "logo": SITE + "/assets/img/brand/immunity-logo.webp"}}

PAGES = []
def render(path, title, desc, body, schemas=None, crumbs=None, prio="0.6", lang="en"):
    url = SITE + path
    ld = [ORG] if path == "/" else []
    if crumbs:
        items = [("Home", "/")] + crumbs
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or path)} for i, (n, u) in enumerate(items)]})
    ld += schemas or []
    ldh = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = "noindex,follow" if TRIAL else "index,follow,max-image-preview:large"
    assert len(title) <= 66, (path, len(title), title)
    out = f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8">{tracking()}<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="{robots}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{SHORT}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/brand/gbo-logo.png">
<meta name="theme-color" content="#1c4720"><link rel="icon" href="/assets/img/brand/gbo-logo.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="{FONT}">
<style>{CSS}</style>{ldh}</head><body><noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
{header(path)}<main id="main">{body}</main>{footer()}<script>{JS}</script></body></html>'''
    d = ROOT if path == "/" else os.path.join(ROOT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
    if path != "/404": PAGES.append((path, prio))

def start(path): _CUR["page"] = path

# ---------------------------------------------------------------- building blocks
def hero(title, lead, crumbs=None, light=False, side=""):
    cr = ""
    if crumbs:
        cr = '<div class="crumbs"><a href="/">Home</a>' + "".join(f' / <a href="{u}">{esc(n)}</a>' if u else f' / {esc(n)}' for n, u in crumbs) + "</div>"
    inner = f'{cr}<h1>{esc(title)}</h1><p class="lead">{esc(lead)}</p>'
    if side: inner = f'<div class="hero-grid"><div>{inner}</div><div>{side}</div></div>'
    return f'<section class="hero{" light" if light else ""}"><div class="wrap">{inner}</div></section>'
def sec(inner, title=None, sub=None, tint=False, id=None):
    t = f"<h2>{esc(title)}</h2>" if title else ""
    s = f'<p class="sub">{esc(sub)}</p>' if sub else ""
    i = f' id="{id}"' if id else ""
    return f'<section class="sec{" tint" if tint else ""}"{i}><div class="wrap">{t}{s}{inner}</div></section>'
def ul(items, cls="ticks"): return f'<ul class="{cls}">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"
def body_of(x): return ul(x, "") if isinstance(x, list) else f"<p>{esc(x)}</p>"
def answer(t): return f'<p class="answer">{esc(t)}</p>'
def faq_html(qs): return '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in qs) + "</div>"
def faq_ld(qs): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}
def card(href, title, text, meta="", more="Read more"):
    m = f'<div class="meta">{esc(meta)}</div>' if meta else ""
    return f'<article class="card">{m}<h3><a href="{href}">{esc(title)}</a></h3><p>{esc(text)}</p><a class="more" href="{href}">{esc(more)}</a></article>'
def pcard(p): return f'<a class="pcard" href="/products/{p["slug"]}">{pimg(p)}<span><h3>{esc(p["name"])}</h3><p>{esc(p["line"])}</p><p class="note" style="margin-top:6px">Price on enquiry &middot; Where to buy</p></span></a>'
def enquiry_box(crop="", product="", title="Send us your enquiry"):
    q = "?" + "&".join(f"{k}={quote(v)}" for k, v in (("crop", crop), ("product", product)) if v) if (crop or product) else ""
    what = product or (f"my {crop.lower()} crop" if crop else "my crop")
    return sec(f'<p class="prose">Tell us your crop, the problem and your location, and send a photo if you can. Our team replies on WhatsApp or calls you with what to check, which product suits and where to buy it near you.</p>'
               f'<div class="btns">{btn_enq("Send enquiry", q)}{btn_wa(f"Hello Gujarat Bio Organics, I want to know about {what}.", "WhatsApp a photo")}{btn_call()}</div>', title, tint=True)
def article_ld(path, headline, desc):
    return {"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": desc, "mainEntityOfPage": SITE + path,
            "author": {"@type": "Person", "name": "Gafar Laiya", "jobTitle": "Founder, Gujarat Bio Organics", "url": SITE + "/about"},
            "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-IN"}
def picker():
    tiles = []
    for c in CRP:
        p = PBY[c["product"]]
        tiles.append(f'<a href="/crops/{c["slug"]}"><span class="tx"><b>{c["name"]}</b><span>{esc(c["hook"])}</span></span>{pimg(p)}</a>')
    return '<div class="picker">' + "".join(tiles) + "</div>"

# ---------------------------------------------------------------- home
start("/")
home_faq = [("Who is Gujarat Bio Organics?", f"{NAME} makes biostimulants, biofertilizers and organic fertilizers at its own factory in Shihor, Bhavnagar, Gujarat. We have worked with farmers since 2006 and sell crop formulas under the Immunity brand."),
            ("Which crops does Immunity cover?", "Immunity has Specials for 20 crops, including sugarcane, potato, mango, apple, banana, citrus, cotton, onion and paddy, plus formulas for all crops, 11 biofertilizers and soil granules."),
            ("How do I buy Immunity?", "Send an enquiry on this site, WhatsApp or call us. We tell you which product suits your crop and where to buy it near you."),
            ("Can you tell me what to use on my crop?", "Yes. Send a photo, your location and the problem. Our team replies with what to check and a programme for your field.")]
specials = [p for p in PRODUCTS if p["group"] == "specials"]
home = hero("What do you grow?", f"Pick your crop. See its stages, the problems farmers face, what has worked for them and the Immunity formula made for it. From {SHORT}, working with farmers since 2006.")
home = home.replace("</p></div></section>", f"</p>{picker()}</div></section>", 1)
home += sec(f'<div class="hero-grid"><div class="prose"><p>{SHORT} started in 2006 in Bhavnagar, Gujarat. For nearly 20 years we have worked on real farms: sugarcane in South Gujarat, potato in Punjab and Haryana, apple in Himachal Pradesh and Jammu and Kashmir, banana in Central Gujarat and mango across India.</p>'
            f'<p>Every Immunity formula came from a problem farmers brought to us. We make them at our own factory in Shihor, with biostimulants as our main line.</p><div class="btns"><a class="btn btn-leaf" href="/our-story">Read our story</a>{btn_enq()}</div></div>'
            f'<div>{media("home-founder-in-field.webp", "Gafar Laiya with a farmer in a crop field, both looking at the crop, natural daylight")}</div></div>', "Nearly 20 years on Indian farms")
home += sec('<div class="stats">' + "".join(f'<div class="stat"><b>{a}</b>{esc(b)}</div>' for a, b in [("2006", "Working with farmers since"), ("20", "Crops with their own Immunity Special"), ("36", "Biostimulant grades with Gujarat NOCs"), ("11", "Biofertilizer types")]) + "</div>", tint=True)
home += sec('<div class="pgrid">' + "".join(pcard(p) for p in specials[:9]) + f'</div><div class="btns"><a class="btn btn-leaf" href="/products">See all 36 Immunity products</a></div>',
            "Immunity crop formulas", "One formula made for each crop, plus formulas for all crops, biofertilizers and soil granules.")
home += sec('<div class="grid">' + media("home-video-sugarcane-farmer.mp4", "Sugarcane farmer in South Gujarat talking about his crop, filmed in his field", "video")
            + media("home-video-apple-grower.mp4", "Apple grower in Himachal Pradesh walking through his orchard and talking about tree health", "video")
            + media("home-video-mango-grower.mp4", "Mango grower showing his trees and fruit, talking about flowering and fruit set", "video")
            + '</div><div class="btns"><a class="btn btn-line" href="/farmer-stories">All farmer stories</a></div>', "Farmers in their own words", "Growers tell what they faced and what changed on their farm.", tint=True)
home += sec('<div class="grid">' + "".join(card(f"/crop-problems/{p['slug']}", cap(p["h1"]), p["answer"][:140].rsplit(" ", 1)[0] + "...", CBY[p["crop"]]["name"]) for p in PROBLEMS[:6]) + "</div>",
            "Common crop problems", "What you see in the field, why it happens and what growers can do.")
home += sec('<div class="grid">' + "".join(card(f"/knowledge/{k['slug']}", k["h1"].split(":")[0], k["desc"], "Knowledge") for k in KNOW) + "</div>", "Soil, fertility and sustainable farming", tint=True)
home += sec(f'<div class="grid two"><div class="prose"><p>Shop owners and distributors: Immunity covers 20 crops with farmer-tested formulas, approvals and support. Dealer prices and margins on enquiry.</p><div class="btns"><a class="btn btn-leaf" href="/dealers">Become a dealer</a><a class="btn btn-line" href="/where-to-buy">Where to buy</a></div></div>'
            f'<div>{media("home-dealer-shop-display.webp", "Agri input shop counter with Immunity bottles on display and the shop owner")}</div></div>', "Dealers wanted")
home += sec(faq_html(home_faq), "Questions farmers ask", tint=True)
render("/", "Gujarat Bio Organics: Immunity Crop Formulas Since 2006",
       "Immunity crop formulas for sugarcane, potato, mango, apple and 16 more crops, biofertilizers and crop guides from Gujarat Bio Organics, Bhavnagar. Working with farmers since 2006.",
       home, [faq_ld(home_faq), {"@context": "https://schema.org", "@type": "WebSite", "url": SITE + "/", "name": SHORT, "publisher": {"@id": SITE + "/#org"}}], None, "1.0")

# ---------------------------------------------------------------- crops
start("/crops")
render("/crops", "Crop Guides for 20 Crops | Gujarat Bio Organics",
       "Stage-by-stage guides for 20 crops, from sugarcane, potato, mango and apple to paddy, cotton, onion and pulses, with common problems and the Immunity formula for each.",
       hero("Crop guides", "Each guide follows the crop stage by stage, lists the problems farmers bring to us, and shows the Immunity formula made for it.", [("Crops", None)])
       + sec(picker().replace('class="picker"', 'class="picker" style="margin-top:0"')) + enquiry_box(), None, [("Crops", None)], "0.9")

for c in CROPS:
    path = f"/crops/{c['slug']}"; start(path)
    p = PBY[c["product"]]
    probs = [x for x in PROBLEMS if x["crop"] == c["slug"]]
    stages = '<ol class="stages">' + "".join(f'<li><h3>{esc(n)}</h3><div class="when">{esc(w)}</div><p>{esc(t)}</p></li>' for n, w, t in c["stages"]) + "</ol>"
    body = hero(f"{c['name']} guide", c["hook"], [("Crops", "/crops"), (c["name"], None)],
                side=media(f"crop-{c['slug']}-hero.webp", f"Wide photo of a healthy {c['name'].lower()} crop in the field, ideally with the farmer, in {c['where'].split(',')[0]}"))
    body += sec(answer(c["intro"]) + f'<p class="prose">Main growing areas: {esc(c["where"])}.</p>' + stages, f"{c['name']} stage by stage")
    body += sec(f'<div class="grid two"><div><h3>Problems farmers bring to us</h3>{ul(c["problems"])}</div><div><h3>What to check first</h3>{ul(c["checks"])}</div></div>'
                + ("<h3>Read more</h3><ul>" + "".join(f'<li><a href="/crop-problems/{x["slug"]}">{esc(cap(x["h1"]))}</a></li>' for x in probs) + "</ul>" if probs else "")
                + f'<div class="grid" style="margin-top:18px">{media(f"crop-{c["slug"]}-problem-1.webp", f"Close-up photo of a common {c["name"].lower()} problem in the field (for example: {c["problems"][0].lower()})")}'
                f'{media(f"crop-{c["slug"]}-problem-2.webp", f"Close-up photo of another {c["name"].lower()} problem: {c["problems"][1].lower()}")}'
                f'{media(f"crop-{c["slug"]}-healthy.webp", f"Close-up photo of a healthy {c["name"].lower()} plant, roots or produce for comparison")}</div>',
                f"Common {c['name'].lower()} problems", tint=True)
    body += sec(f'<div class="pbox"><div class="pshot">{pimg(p)}</div><div class="prose"><h3>{esc(p["name"])}</h3><p>{esc(p["line"])}</p>'
                + (f'<p>{esc(p["story"])}</p>' if p["story"] else "") + f'<p><b>Packs:</b> {esc(", ".join(p["packs"]))}</p>'
                f'<div class="btns"><a class="btn btn-leaf" href="/products/{p["slug"]}">See {esc(p["name"])}</a>{btn_enq("Send enquiry", "?crop=" + quote(c["name"]) + "&product=" + quote(p["name"]))}</div><p class="note">{RESULTS}</p></div></div>',
                f"The Immunity formula for {c['name'].lower()}")
    body += sec('<div class="grid">' + media(f"crop-{c['slug']}-farmer-video-1.mp4", f"{c['name']} farmer talking in his field about his crop and what changed", "video")
                + media(f"crop-{c['slug']}-farmer-video-2.mp4", f"Second {c['name'].lower()} farmer story, filmed in the field", "video")
                + media(f"crop-{c['slug']}-field-visit.mp4", f"Our team on a field visit to a {c['name'].lower()} farm, checking roots and crop", "video") + "</div>", f"{c['name']} farmers in their own words", tint=True)
    body += sec(faq_html(c["faq"]), f"{c['name']} questions") + enquiry_box(c["name"], p["name"])
    title = f"{c['name']} Farming Guide: Stages, Problems & Care | GBO"
    if len(title) > 66: title = f"{c['name']} Guide: Stages, Problems & Care | GBO"
    render(path, title, f"{c['name']} guide for growers: stage-by-stage care, common problems, what to check, and {p['name']}.",
           body, [faq_ld(c["faq"]), article_ld(path, f"{c['name']} farming guide", c["intro"])], [("Crops", "/crops"), (c["name"], None)], "0.8")

# ---------------------------------------------------------------- products
start("/products")
pb = hero("Immunity products", "36 products: Specials for 20 crops, formulas for all crops, a finisher, 11 biofertilizers and soil granules. Made by Gujarat Bio Organics in Bhavnagar, Gujarat.", [("Products", None)],
          side=f'<img src="/assets/img/brand/immunity-logo.webp" alt="Immunity brand logo" style="max-width:320px;background:#fff;border-radius:16px;padding:12px">')
pb += sec('<div class="chips">' + "".join(f'<a href="#{g}">{esc(t)}</a>' for g, t, _ in GROUPS) + "</div>")
for i, (g, t, d) in enumerate(GROUPS):
    pb += sec('<div class="pgrid">' + "".join(pcard(p) for p in PRODUCTS if p["group"] == g) + "</div>", t, d, tint=bool(i % 2 == 0), id=g)
pb += enquiry_box()
render("/products", "Immunity Products: 36 Crop Formulas & Biofertilizers | GBO",
       "All Immunity products: Specials for 20 crops, Immunity Gold for all crops, Finisher, 11 biofertilizers and Immunity Granules. Pack sizes and enquiry.",
       pb, [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/products/{p['slug']}", "name": p["name"]} for i, p in enumerate(PRODUCTS)]}],
       [("Products", None)], "0.9")

GNAME = {g: t for g, t, _ in GROUPS}
for p in PRODUCTS:
    path = f"/products/{p['slug']}"; start(path)
    c = CBY.get(p["crop"]) if p["crop"] else None
    packs = ", ".join(p["packs"]) if p["packs"] else "Pack sizes on enquiry"
    q = "?product=" + quote(p["name"]) + ("&crop=" + quote(c["name"]) if c else "")
    crop_line = f'<p><b>Made for:</b> <a href="/crops/{c["slug"]}">{c["name"]}</a></p>' if c else f'<p><b>Range:</b> {esc(GNAME[p["group"]])}</p>'
    if p.get("also"): crop_line += f'<p><b>Also used on:</b> {esc(p["also"])}</p>'
    body = hero(p["name"], p["line"], [("Products", "/products"), (p["name"].replace("Immunity ", ""), None)])
    body += sec(f'''<div class="pbox"><div class="pshot">{pimg(p)}</div><div><p><b>Form:</b> {esc(p["form"])}</p>{crop_line}<p><b>Pack sizes:</b> {esc(packs)}</p>
<p><b>Price:</b> send an enquiry or call us for the price.</p>
<div class="btns">{btn_enq("Send enquiry for price", q)}{btn_call("Call for price")}{btn_wa(f"Hello Gujarat Bio Organics, please send the price of {p['name']}. Pack size: / Location:", "Ask price on WhatsApp")}<a class="btn btn-line" href="/where-to-buy">Where to buy</a></div></div></div>''')
    left = f'<div><h3>{"Made for" if p["group"] != "bio" else "Suits"}</h3>{ul(p["made_for"])}</div>' if p["made_for"] else ""
    story = f'<div class="prose"><h3>How it was developed</h3><p>{esc(p["story"])}</p></div>' if p["story"] else f'<div class="prose"><h3>Ask us</h3><p>Send your crop, its stage and your location, and our team will tell you how {esc(p["name"])} fits your programme.</p></div>'
    body += sec(f'<div class="grid two">{left}{story}</div>', "Who it is for", tint=True)
    body += sec(f'<div class="prose"><p>The right amount and timing depend on your crop, its stage and your soil. Every pack carries the label dose. Send us your crop, stage and location and our team will send a schedule for your field.</p></div><div class="btns">{btn_wa(f"Hello Gujarat Bio Organics, please send the schedule for {p['name']}. Crop: / Stage: / Location:", "Get a schedule on WhatsApp")}</div>', "How to use it")
    body += sec('<div class="grid">' + media(f"{p['slug']}-farmer-story.mp4", f"Farmer who used {p['name']} talking in his field about his crop", "video")
                + media(f"{p['slug']}-how-to-apply.mp4", f"Short video showing how {p['name']} is mixed and applied in the field", "video")
                + media(f"{p['slug']}-label.webp", f"Clear photo of the back label of {p['name']} showing composition and directions") + f'</div><p class="note" style="margin-top:14px">{RESULTS}</p>', "Farmer videos and label", tint=True)
    pfaq = [(f"What is {p['name']}?", f"{p['line']} It is made by {NAME} in Bhavnagar, Gujarat."),
            (f"What pack sizes does {p['name']} come in?", packs + "."),
            (f"What is the price of {p['name']}?", "Prices are shared on enquiry, together with the nearest place to buy. Send an enquiry or WhatsApp us."),
            ("How much should I use?", "The dose depends on crop, stage and soil. Follow the label, or ask us for a schedule for your field.")]
    body += sec(faq_html(pfaq), "Questions") + enquiry_box(c["name"] if c else "", p["name"])
    prod_ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["line"], "brand": {"@type": "Brand", "name": "Immunity"},
               "manufacturer": {"@id": SITE + "/#org"}, "category": GNAME[p["group"]]}
    if os.path.exists(os.path.join(ROOT, "assets", "img", "products", p["slug"] + ".webp")): prod_ld["image"] = f"{SITE}/assets/img/products/{p['slug']}.webp"
    t = f"{p['name']}: Uses, Packs & Enquiry | Gujarat Bio Organics"
    if len(t) > 66: t = f"{p['name']}: Uses, Packs & Enquiry | GBO"
    if len(t) > 66: t = f"{p['name']} | Gujarat Bio Organics"
    if len(t) > 66: t = f"{p['name']} | GBO"
    render(path, t, f"{p['line']} Pack sizes, who it is for and how to send an enquiry.", body, [prod_ld, faq_ld(pfaq)], [("Products", "/products"), (p["name"], None)], "0.8")

# ---------------------------------------------------------------- farmer stories
start("/farmer-stories")
stories = [("Last year I did 3 times re-transplanting of my sugarcane crop.", "Jagdish Bhai", "Sugarcane grower, on the problem he faced before working with us"),
           ("Reported a single sugarcane of 4.5 kg from his field, shown in his Facebook video.", "Dharmesh Patel", "Sugarcane grower, South Gujarat. Farmer reported")]
sq = '<div class="grid two">' + "".join(f'<blockquote class="quote"><p>{esc(t)}</p><cite>{esc(n)}</cite><span class="tag">{esc(r)}</span></blockquote>' for t, n, r in stories) + "</div>"
fs = hero("Farmer stories", "Growers tell, in their own words, what they faced and what changed on their farm.", [("Farmer stories", None)])
fs += sec('<div class="chips">' + "".join(f'<a href="#{c["slug"]}">{c["name"]}</a>' for c in CROPS[:10]) + "</div>" + sq + f'<p class="note" style="margin-top:16px">{RESULTS}</p>', "What farmers told us")
for i, c in enumerate(CROPS[:10]):
    fs += sec('<div class="grid">' + media(f"story-{c['slug']}-1.mp4", f"{c['name']} farmer story 1: farmer in his field, name and village on screen", "video")
              + media(f"story-{c['slug']}-2.mp4", f"{c['name']} farmer story 2", "video") + media(f"story-{c['slug']}-photo.webp", f"Photo of a {c['name'].lower()} farmer with his crop or harvest") + "</div>",
              f"{c['name']} growers", tint=(i % 2 == 0), id=c["slug"])
fs += sec(f'<p class="prose">Have you used Immunity on your farm? Send us your story and photos on WhatsApp. With your permission, we will share it to help other farmers.</p><div class="btns">{btn_wa("Hello Gujarat Bio Organics, I want to share my farm story.", "Share your story")}</div>', "Share your story")
render("/farmer-stories", "Farmer Stories and Videos | Gujarat Bio Organics", "Sugarcane, potato, mango, apple, banana and other growers tell what they faced on their farms and what changed. Videos and farmer reports.",
       fs, None, [("Farmer stories", None)], "0.8")

# ---------------------------------------------------------------- knowledge
start("/knowledge")
kn = hero("Agriculture knowledge", "Plain answers on soil, crops and sustainable farming, from nearly 20 years in the field.", [("Knowledge", None)])
kn += sec('<div class="grid">' + "".join(card(f"/knowledge/{k['slug']}", k["h1"].split(":")[0], k["desc"], "Pillar guide") for k in KNOW) + "</div>", "Soil and sustainability")
kn += sec('<div class="grid">' + "".join(card(f"/crop-problems/{x['slug']}", cap(x["h1"]), x["desc"], CBY[x["crop"]]["name"]) for x in PROBLEMS) + "</div>", "Crop problems", tint=True)
kn += sec('<div class="grid">' + "".join(card(f"/guides/{g['slug']}", g["h1"], g["desc"], "Guide") for g in GUIDES) + '</div><div class="btns"><a class="btn btn-leaf" href="/articles">All articles</a></div>', "Farming guides")
render("/knowledge", "Agriculture Knowledge: Soil, Crops, Sustainability | GBO", "Guides on soil health, soil fertility, sustainable farming and the 5 Rs, crop problems and practical farming topics from Gujarat Bio Organics.",
       kn, None, [("Knowledge", None)], "0.8")

def article_page(path, basename, baseurl, x, crop=None, hero_media=None):
    start(path)
    body = hero(cap(x["h1"]), x["desc"], [(basename, baseurl), (x["h1"].split(":")[0][:40], None)], light=True)
    inner = answer(x["answer"])
    for fn, ds in (hero_media or []): inner += media(fn, ds)
    inner += "".join(f"<h2>{esc(h)}</h2>" + body_of(items) for h, items in x["sections"])
    if crop:
        c = CBY[crop]; p = PBY[c["product"]]
        inner += f'<p>See the full <a href="/crops/{crop}">{c["name"].lower()} guide</a> and <a href="/products/{p["slug"]}">{p["name"]}</a>.</p>'
    inner += f'<p class="note">Written by Gafar Laiya, founder of {SHORT}, working with farmers since 2006. {RESULTS}</p>'
    body += sec(f'<div class="prose">{inner}</div>') + sec(faq_html(x["faq"]), "Questions", tint=True) + enquiry_box(CBY[crop]["name"] if crop else "")
    render(path, x["title"] if len(x["title"]) <= 66 else x["title"][:66], x["desc"], body, [faq_ld(x["faq"]), article_ld(path, x["h1"], x["desc"])],
           [(basename, baseurl), (x["h1"].split(":")[0][:40], None)], "0.7")

for k in KNOW: article_page(f"/knowledge/{k['slug']}", "Knowledge", "/knowledge", k, hero_media=k["media"])
start("/crop-problems")
render("/crop-problems", "Crop Problems: Causes, Signs and What to Do | GBO",
       "Plain guides to common crop problems: apple root rot, mango fruit drop and alternate bearing, sugarcane poor germination, small potatoes and citrus dieback.",
       hero("Crop problems", "What you see in the field, why it happens, and what growers can do.", [("Knowledge", "/knowledge"), ("Crop problems", None)])
       + sec('<div class="grid">' + "".join(card(f"/crop-problems/{x['slug']}", cap(x["h1"]), x["answer"][:150].rsplit(" ", 1)[0] + "...", CBY[x["crop"]]["name"]) for x in PROBLEMS) + "</div>")
       + enquiry_box(), None, [("Knowledge", "/knowledge"), ("Crop problems", None)], "0.8")
for x in PROBLEMS: article_page(f"/crop-problems/{x['slug']}", "Crop problems", "/crop-problems", x, x["crop"], [(f"problem-{x['slug']}.webp", f"Clear field photo showing {x['h1'].split(':')[0].lower()}")])
start("/guides")
render("/guides", "Farming Guides: Biostimulants, Compost, Soil Tests | GBO",
       "Plain farming guides from Gujarat Bio Organics: biostimulants, tired soil, compost and humic acid, and how to take a soil sample.",
       hero("Farming guides", "Plain answers to the questions farmers ask us most.", [("Knowledge", "/knowledge"), ("Guides", None)])
       + sec('<div class="grid">' + "".join(card(f"/guides/{g['slug']}", g["h1"], g["desc"], "Guide") for g in GUIDES) + "</div>") + enquiry_box(), None, [("Knowledge", "/knowledge"), ("Guides", None)], "0.7")
for g in GUIDES: article_page(f"/guides/{g['slug']}", "Guides", "/guides", g)

# ---------------------------------------------------------------- articles (moved from the old website)
ARTICLES = json.load(open(os.path.join(ROOT, "content_articles.json"), encoding="utf-8"))
ACAT = [("soil", "Soil health"), ("compost", "Compost"), ("crops", "Crop guides"), ("organic", "Organic and sustainable farming")]
def md_html(t):
    out, ul_open = [], False
    for b in t.split("\n\n"):
        b = b.strip()
        if b.startswith("- "):
            if not ul_open: out.append("<ul>"); ul_open = True
            out.append(f"<li>{esc(b[2:])}</li>"); continue
        if ul_open: out.append("</ul>"); ul_open = False
        m = re.match(r"^(#{2,4}) (.*)", b)
        if m: lvl = min(len(m.group(1)), 3); out.append(f"<h{lvl}>{esc(m.group(2))}</h{lvl}>")
        else: out.append(f"<p>{esc(b)}</p>")
    if ul_open: out.append("</ul>")
    return "".join(out)
start("/articles")
ah = hero("Articles", f"{len(ARTICLES)} articles on soil, compost, crops and sustainable farming by Gafar Laiya and the Gujarat Bio Organics team, in English and Hindi.", [("Knowledge", "/knowledge"), ("Articles", None)])
ah += sec('<div class="chips">' + "".join(f'<a href="#{c}">{esc(t)}</a>' for c, t in ACAT) + '</div>')
for i, (c, t) in enumerate(ACAT):
    items = [a for a in ARTICLES if a["cat"] == c]
    ah += sec('<div class="grid">' + "".join(card(f"/articles/{a['slug']}", a["h1"], (a["desc"] or a["body"][:150])[:160], "Hindi" if a["lang"] == "hi" else "English") for a in items) + "</div>", t, tint=(i % 2 == 0), id=c)
render("/articles", "Farming Articles: Soil, Compost, Crops, Organic | GBO", "Articles on soil health, composting, crop problems and sustainable farming from Gujarat Bio Organics, in English and Hindi.",
       ah, None, [("Knowledge", "/knowledge"), ("Articles", None)], "0.7")
for a in ARTICLES:
    path = f"/articles/{a['slug']}"; start(path)
    rel = [x for x in ARTICLES if x["cat"] == a["cat"] and x["slug"] != a["slug"]][:3]
    body = hero(a["h1"], a["desc"] or "", [("Articles", "/articles"), (a["h1"][:40], None)], light=True)
    body += sec(f'<div class="prose">{md_html(a["body"])}<p class="note">By Gafar Laiya, founder of {SHORT}, working with farmers since 2006. {RESULTS}</p></div>')
    body += sec('<div class="grid">' + "".join(card(f"/articles/{x['slug']}", x["h1"], (x["desc"] or "")[:140], "Read next") for x in rel) + "</div>", "Read next", tint=True) + enquiry_box()
    t = a["title"] if len(a["title"]) <= 66 else a["title"][:63].rsplit(" ", 1)[0] + "..."
    render(path, t, (a["desc"] or a["h1"])[:160], body, [article_ld(path, a["h1"], a["desc"] or a["h1"])], [("Articles", "/articles"), (a["h1"][:40], None)], "0.6", a["lang"])

# ---------------------------------------------------------------- about / story / impact / quality / factory
start("/about")
about = hero("About Gujarat Bio Organics", "Working with farmers since 2006. Biostimulants, biofertilizers and organic fertilizers, made in Bhavnagar, Gujarat.", [("About", None)],
             side=media("about-factory-front.webp", "Front of our factory in Shihor, Bhavnagar with the company name board"))
about += sec(f'''<div class="prose"><p>{SHORT} started in 2006 in Bhavnagar, Gujarat. From the beginning the work has been on real farms: walking fields with growers, finding out why a crop was failing, and building formulas that solve those problems.</p>
<p>That work led to the Immunity range: Specials for 20 crops, formulas for all crops, 11 biofertilizers and soil granules.</p>
<h2>What we make</h2>{ul(["Biostimulants, our main line: humic and fulvic acid, seaweed extracts, amino acids and protein hydrolysates", "Biofertilizers: nitrogen fixers, phosphate, potash and zinc solubilisers, mycorrhiza and consortia", "Organic fertilizers and the Immunity crop formulas"])}
<h2>How we make it</h2><p>Everything is made at our own factory in Shihor, Bhavnagar. Nearly 20 years of field work have taught us which raw materials work. We extract them in-house without harsh chemicals, very high pH or heat, because the helpful substances in humus and seaweed are fragile.</p>
<h2>What we believe</h2><p>We want to make farming free of hazardous chemicals and make sustainable food growing easier for the generations to come.</p>
<h2>Founder</h2><p>Gafar Laiya founded {SHORT} and leads its product development and farmer programmes. He writes many of the guides on this site.</p>
<h2>Company details</h2><p>{NAME}<br>Factory: {FACTORY}<br>Registered office: {REGOFF}<br>CIN {CIN}</p></div>''')
about += sec('<div class="grid">' + media("about-founder-portrait.webp", "Portrait of Gafar Laiya, founder, in the field or at the factory") + media("about-team-group.webp", "Group photo of the Gujarat Bio Organics team at the factory")
             + media("about-company-video.mp4", "Two-minute company video: our story, factory and farmers", "video") + '</div><div class="btns"><a class="btn btn-leaf" href="/our-story">Our story since 2006</a><a class="btn btn-line" href="/our-impact">Our impact</a></div>', "Meet us", tint=True)
render("/about", "About Gujarat Bio Organics: Since 2006, Bhavnagar", "Gujarat Bio Organics has worked with farmers since 2006 and makes biostimulants, biofertilizers and organic fertilizers at its own factory in Shihor, Bhavnagar, Gujarat.",
       about, [ORG], [("About", None)], "0.8")

start("/our-story")
tl = '<ol class="timeline">' + "".join(f'<li><div class="yr">{esc(y)}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for y, t, d in STORY) + "</ol>"
st = hero("Our story: nearly 20 years on Indian farms", "From one company in Bhavnagar in 2006 to an Immunity range for 20 crops, every step came from a problem farmers brought to us.", [("About", "/about"), ("Our story", None)])
st += sec(f'<div class="hero-grid"><div>{tl}</div><div>{media("story-2006-early-days.webp", "Old photo from the early years: first products, first factory or first field visits")}{media("story-field-work-collage.webp", "Collage of field visits across crops and states over the years")}</div></div>', "The journey")
st += sec('<div class="grid">' + media("story-video-20-years.mp4", "Video: 20 years in the field, told by Gafar Laiya with old photos and farmer clips", "video")
          + media("story-sugarcane-south-gujarat.webp", "Photo from the sugarcane work in South Gujarat") + media("story-apple-himachal.webp", "Photo from the apple orchards in Himachal Pradesh") + "</div>", "Moments from the field", tint=True)
st += enquiry_box(title="Talk to us")
render("/our-story", "Our Story Since 2006 | Gujarat Bio Organics", "Gujarat Bio Organics' journey since 2006: from field work with sugarcane, apple, potato, mango and banana growers to the Immunity range for 20 crops.",
       st, None, [("About", "/about"), ("Our story", None)], "0.7")

start("/our-impact")
im = hero("Our impact", "Healthier soil, lower dependence on hazardous chemicals, and more food from the same land.", [("About", "/about"), ("Our impact", None)],
          side=media("impact-hero-healthy-field.webp", "Wide photo of a thriving field with the farmer family, showing healthy crop and soil"))
im += sec('<div class="stats">' + "".join(f'<div class="stat"><b>{a}</b>{esc(b)}</div>' for a, b in [("2006", "Working with farmers since"), ("20", "Crops served by the Immunity range"), ("Thousands", "Mango and apple growers who have used our Specials"), ("Add", "Farmers served in total (number to be added)")]) + "</div>")
im += sec('''<div class="grid two"><div class="prose"><h3>Eliminate hunger</h3><p>Food security starts with soil. Tired soil grows less food for more money. By rebuilding soil life and helping crops use nutrients well, farmers can keep producing food from the same land, season after season.</p></div>
<div class="prose"><h3>Healthier soil</h3><p>Every Immunity formula is made to work with living soil. Our biofertilizers add helpful microbes and our granules improve soil structure.</p></div>
<div class="prose"><h3>Fewer hazardous chemicals</h3><p>Our mission is to make farming free of hazardous chemicals. Healthier crops on healthier soil need less rescue spraying.</p></div>
<div class="prose"><h3>Farmers' income</h3><p>Many of our formulas came from growers who were no longer breaking even. Our work is judged by whether the farm pays, as farmers themselves report.</p></div></div>''', "What we work for", tint=True)
im += sec('<div class="grid">' + media("impact-before-after-soil.webp", "Before and after photo of the same field or soil after a season of soil care") + media("impact-farmer-family.webp", "Farmer family with their harvest")
          + media("impact-video.mp4", "Short video on soil health and food security, with farmers speaking", "video") + f'</div><p class="note" style="margin-top:14px">{RESULTS}</p>', "Impact on the ground")
im += sec('<div class="grid">' + "".join(card(f"/knowledge/{k['slug']}", k["h1"].split(":")[0], k["desc"], "Read") for k in KNOW) + "</div>", "Learn more", tint=True)
render("/our-impact", "Our Impact: Soil Health, Food Security, Fewer Chemicals | GBO", "How Gujarat Bio Organics works for healthier soil, fewer hazardous chemicals, better farm income and food security.",
       im, None, [("About", "/about"), ("Our impact", None)], "0.6")

start("/quality")
quality = hero("Quality and approvals", "How we make and check our products, and the approvals we hold.", [("About", "/about"), ("Quality", None)], light=True)
quality += sec(f'''<div class="prose">{answer("The Directorate of Agriculture, Government of Gujarat has issued No Objection Certificates to Gujarat Bio Organics for 36 biostimulant grades listed in Schedule VI of the Fertiliser Control Order and 11 biofertilizer types.")}
<h2>Why approvals matter</h2><p>Since June 2025 only biostimulants listed in Schedule VI of the Fertiliser Control Order can be sold in India. Before you buy any biostimulant, ask the seller which Schedule VI grade it is and for proof of approval.</p>
<h2>How we check quality</h2>{ul(["Raw materials chosen from nearly 20 years of field experience", "Made at our own factory in Shihor, Bhavnagar", "In-house quality control on every batch", "Third-party testing available for bulk buyers"])}
{media("quality-lab-testing.webp", "Photo of our quality control lab with a technician testing a sample")}
<p>Full grade lists and specifications are on our <a href="{B2B}/quality-compliance">business site</a>.</p></div>''')
render("/quality", "Quality and Approvals | Gujarat Bio Organics", "Gujarat Bio Organics holds NOCs from the Directorate of Agriculture, Gujarat for 36 Schedule VI biostimulant grades and 11 biofertilizer types. How we check quality.",
       quality, None, [("About", "/about"), ("Quality", None)], "0.6")

start("/factory-and-rd")
fr = hero("Factory and R&D", "Everything we sell is made at our own factory in Shihor, Bhavnagar, Gujarat.", [("About", "/about"), ("Factory and R&D", None)],
          side=media("factory-aerial.webp", "Aerial or wide photo of the factory in Shihor"))
fr += sec(f'''<div class="grid two"><div class="prose"><h3>Our factory</h3><p>Liquid and granular production, packing from 250 mL bottles to bulk, and dispatch across India and abroad. Address: {FACTORY}.</p></div>
<div class="prose"><h3>Research and development</h3><p>Formulas are developed from field problems and tested on farms before they reach the market. Extraction is done in-house without harsh chemicals, very high pH or heat.</p></div></div>''')
fr += sec('<div class="grid">' + media("factory-liquid-line.webp", "Liquid production and bottling line") + media("factory-granules-line.webp", "Granule production line")
          + media("factory-rd-lab.webp", "R&D lab with formulation work in progress") + media("factory-packing-dispatch.webp", "Packing and dispatch area with Immunity cartons")
          + media("factory-raw-materials.webp", "Raw material store (seaweed, humus) ready for extraction") + media("factory-tour.mp4", "Two-minute factory tour video", "video") + "</div>", "Inside the factory", tint=True)
fr += sec(f'<p class="prose">Bulk, OEM and private label buyers can see grades and specifications on our <a href="{B2B}/manufacturing-facility">business site</a>.</p>')
render("/factory-and-rd", "Factory and R&D in Shihor, Bhavnagar | Gujarat Bio Organics", "Gujarat Bio Organics makes all its products at its own factory in Shihor, Bhavnagar, Gujarat, with in-house R&D and quality control.",
       fr, None, [("About", "/about"), ("Factory and R&D", None)], "0.6")

# ---------------------------------------------------------------- dealers & bulk
start("/dealers")
dl = hero("Become an Immunity dealer", "Sell a range farmers ask for: Immunity formulas for 20 crops, biofertilizers and soil granules, from a manufacturer working with farmers since 2006.", [("Dealers & Bulk", None)],
          side=media("dealer-hero-shop.webp", "Agri input shop with Immunity bottles on the shelf and the dealer at the counter"))
dl += sec('<div class="grid">' + "".join(f'<article class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for t, d in DEALER_WANTS) + "</div>", "What you get as a dealer")
dl += sec('<div class="pgrid">' + "".join(pcard(p) for p in specials[:6]) + '</div><div class="btns"><a class="btn btn-line" href="/products">See the full range</a></div>', "The range you will sell", "Pack sizes from 250 mL to 5 L; granules in 8 kg bags.", tint=True)
dform = f'''<form class="form" id="enqform"><input type="hidden" name="type" value="Dealer enquiry">
<div><label for="d1">Your name</label><input id="d1" name="name" required autocomplete="name"></div>
<div><label for="d2">Shop or company name</label><input id="d2" name="shop" required></div>
<div><label for="d3">District and state</label><input id="d3" name="location" required></div>
<div><label for="d4">Phone or WhatsApp</label><input id="d4" name="phone" required inputmode="tel" autocomplete="tel"></div>
<div><label for="d5">Brands you sell now</label><input id="d5" name="current brands"></div>
<div><label for="d6">Expected monthly purchase</label><select id="d6" name="monthly volume"><option value="">Choose</option><option>Up to 50 litres</option><option>50 to 200 litres</option><option>200 to 1000 litres</option><option>More than 1000 litres</option></select></div>
<div><button class="btn btn-wa" type="submit">{WA_SVG}Send dealer enquiry on WhatsApp</button></div></form>'''
dl += sec(dform + '<p class="note">Your details open in WhatsApp so you can check them before sending.</p>', "Apply to become a dealer")
dl += sec(faq_html([("What margin do dealers get?", "Dealer prices and margins are shared on enquiry and depend on volume and area."),
                    ("Is there a minimum order?", "Tell us your expected monthly purchase and we will suggest a starting order."),
                    ("Do you support dealers with marketing?", "Ask us about posters, crop leaflets, farmer videos and field demonstrations for your area.")]), "Dealer questions", tint=True)
render("/dealers", "Become an Immunity Dealer | Gujarat Bio Organics", "Become a dealer for Immunity crop formulas, biofertilizers and soil granules from Gujarat Bio Organics. Range, approvals, support and dealer enquiry.",
       dl, None, [("Dealers & Bulk", None)], "0.8")

start("/bulk-buyers")
bb = hero("Bulk buyers", "Farm companies, FPOs, plantations, government buyers and large growers: buy Immunity and our biostimulants in bulk, direct from the factory.", [("Dealers & Bulk", "/dealers"), ("Bulk buyers", None)], light=True)
bb += sec(f'''<div class="grid two"><div class="prose"><h3>Who buys in bulk</h3>{ul(["Farmer producer organisations (FPOs) and cooperatives", "Plantations, orchards and farm companies", "Sugar factories for their growers", "Government and institutional buyers", "Large growers"])}</div>
<div class="prose"><h3>What we offer</h3>{ul(["Direct factory supply, dispatch usually within a week", "Pack sizes from 1 L to 5 L, and larger packs on request", "Crop programmes and field support for your growers", "Third-party testing on request"])}</div></div>''')
bb += sec(f'<div class="grid two"><div class="prose"><h3>Manufacturer, formulator or brand?</h3><p>Need raw biostimulants, OEM manufacturing or your own private-label brand? See grades, specifications and export terms on our business site.</p><div class="btns"><a class="btn btn-leaf" href="{B2B}/bulk-supply">Bulk supply on the business site</a><a class="btn btn-line" href="/oem-private-label">OEM and private label</a></div></div>{media("bulk-dispatch-truck.webp", "Truck being loaded with Immunity cartons at the factory")}</div>', tint=True)
bb += enquiry_box(title="Send a bulk enquiry")
render("/bulk-buyers", "Bulk Buyers: FPOs, Plantations, Farm Companies | GBO", "Buy Immunity crop formulas and biostimulants in bulk direct from the factory: FPOs, plantations, sugar factories, farm companies and institutions.",
       bb, None, [("Dealers & Bulk", "/dealers"), ("Bulk buyers", None)], "0.7")

start("/oem-private-label")
op = hero("Need OEM or private label?", "We manufacture biostimulants and biofertilizers under your brand, at our factory in Shihor, Bhavnagar.", [("Dealers & Bulk", "/dealers"), ("OEM and private label", None)], light=True)
op += sec(f'''<div class="prose"><p>Brands, distributors and importers use Gujarat Bio Organics to make products under their own name: we formulate, manufacture, fill and label, and you sell.</p>
{ul(["36 biostimulant grades and 11 biofertilizer types covered by Gujarat NOCs", "Liquid, powder and granule formats", "Packs from 250 mL bottles to 1000 L IBC tanks", "Export by sea from Indian ports"])}
<p>Full details, grades and specifications are on our business site.</p><div class="btns"><a class="btn btn-leaf" href="{B2B}/private-label-oem">Private label and OEM details</a>{btn_enq("Send enquiry", "?type=OEM")}</div></div>''')
render("/oem-private-label", "OEM and Private Label Fertilizer Manufacturing | GBO", "Need OEM manufacturing or a private-label biostimulant or biofertilizer brand? Gujarat Bio Organics manufactures under your brand in Bhavnagar, Gujarat.",
       op, None, [("Dealers & Bulk", "/dealers"), ("OEM and private label", None)], "0.6")

start("/where-to-buy")
wb = hero("Where to buy Immunity", "Ask us for the nearest dealer, or order direct. We deliver across India.", [("Dealers & Bulk", "/dealers"), ("Where to buy", None)], light=True)
wb += sec(f'''<ol class="stages"><li><h3>Tell us your location and crop</h3><p>Send an enquiry, WhatsApp or call with your village, district, crop and the product you want.</p></li>
<li><h3>We point you to a dealer near you</h3><p>If there is an Immunity dealer near you, we share their details.</p></li>
<li><h3>Or order direct</h3><p>Where there is no dealer, we supply direct and deliver by courier or transport.</p></li></ol>
<div class="btns">{btn_enq("Find where to buy", "?type=Where+to+buy")}{btn_wa("Hello Gujarat Bio Organics, where can I buy Immunity near me? Village/District: / Crop: / Product:", "Ask on WhatsApp")}{btn_call()}</div>
<p class="note">Dealer list by district coming soon.</p>''')
render("/where-to-buy", "Where to Buy Immunity Near You | Gujarat Bio Organics", "Find the nearest Immunity dealer or order direct from Gujarat Bio Organics. Delivery across India.",
       wb, None, [("Dealers & Bulk", "/dealers"), ("Where to buy", None)], "0.7")

# ---------------------------------------------------------------- enquiry, contact
start("/enquiry")
copts = "".join(f"<option>{esc(c['name'])}</option>" for c in CRP) + "<option>Other</option>"
popts = "".join(f"<option>{esc(p['name'])}</option>" for p in PRODUCTS) + "<option>Not sure</option>"
eform = f'''<form class="form" id="enqform">
<div><label for="e0">I am a</label><select id="e0" name="type"><option>Farmer</option><option>Dealer enquiry</option><option>Bulk buyer</option><option value="OEM">OEM or private label</option><option>Where to buy</option></select></div>
<div><label for="e1">Your name</label><input id="e1" name="name" required autocomplete="name"></div>
<div><label for="e2">Phone or WhatsApp</label><input id="e2" name="phone" required inputmode="tel" autocomplete="tel"></div>
<div><label for="e3">Village, district and state</label><input id="e3" name="location" required></div>
<div><label for="e4">Crop</label><select id="e4" name="crop"><option value="">Choose</option>{copts}</select></div>
<div><label for="e5">Product (if you know)</label><select id="e5" name="product"><option value="">Choose</option>{popts}</select></div>
<div><label for="e6">Problem or question</label><textarea id="e6" name="message" rows="4" placeholder="What do you see in the field? Crop age, area in acres..."></textarea></div>
<div><button class="btn btn-wa" type="submit">{WA_SVG}Send enquiry on WhatsApp</button></div></form>'''
en = hero("Send an enquiry", "Tell us your crop, the problem and where you are. Our team replies on WhatsApp or calls you back.", [("Enquiry", None)], light=True)
en += sec(f'<div class="grid two"><div>{eform}<p class="note">Your enquiry opens in WhatsApp so you can check it, add a crop photo and send. Prefer to talk? Call {PHONE}.</p></div>'
          f'<div class="prose"><h3>What happens next</h3><ol class="stages"><li><h3>We read your enquiry</h3><p>Our team looks at your crop, problem and photo.</p></li><li><h3>We call or reply</h3><p>We tell you what to check and which product suits.</p></li><li><h3>You get a schedule</h3><p>A programme for your crop stage, and where to buy near you.</p></li></ol></div></div>')
render("/enquiry", "Send an Enquiry | Gujarat Bio Organics", "Send your crop, problem and location to Gujarat Bio Organics. Our team replies on WhatsApp or by phone with advice, product and where to buy.",
       en, None, [("Enquiry", None)], "0.7")

start("/contact")
contact = hero("Contact us", "Questions about your crop, dealership or an order? We reply on WhatsApp and by phone.", [("Contact", None)], light=True)
contact += sec(f'''<div class="grid two"><div><h2>Farmers, dealers and orders</h2><p>WhatsApp or call: <a href="tel:{TEL}">{PHONE}</a><br>Email: <a href="mailto:{MAIL}">{MAIL}</a></p><div class="btns">{btn_enq()}{btn_wa("Hello Gujarat Bio Organics, I have a question.")}{btn_call()}</div>
<h2>Bulk, OEM and export</h2><p><a href="{B2B}/contact">Business site contact page</a>.</p></div>
<div><h2>Visit us</h2><p><b>Factory</b><br>{FACTORY}</p><p><b>Registered office</b><br>{REGOFF}</p><p>{NAME}<br>CIN {CIN}</p></div></div>''')
render("/contact", "Contact Gujarat Bio Organics | WhatsApp, Phone, Address", "Contact Gujarat Bio Organics on WhatsApp or phone (+91 99787 91167), email sales@gujaratbio.com, or visit our factory in Shihor, Bhavnagar, Gujarat.",
       contact, None, [("Contact", None)], "0.7")

# ---------------------------------------------------------------- legal (drafts: confirm before online payments go live)
def legal(path, title, h, inner):
    start(path)
    render(path, title, f"{h} for {NAME}.", hero(h, NAME, [(h, None)], light=True) + sec(f'<div class="prose">{inner}</div>'), None, [(h, None)], "0.2")
legal("/shipping-and-returns", "Shipping and Returns | Gujarat Bio Organics", "Shipping and returns", f'''<h2>Shipping</h2><p>Orders are processed and dispatched within 1 to 7 working days from order confirmation, by courier, transport agency or another suitable carrier. Tracking details are shared on WhatsApp or email.</p>
<h2>Damaged or wrong items</h2><p>If your order arrives damaged, leaking or wrong, send photos of the pack and parcel on WhatsApp ({PHONE}) or to {MAIL} within 48 hours of delivery. We will replace the item or refund it after checking.</p>
<h2>Cancellations</h2><p>You can cancel an order before dispatch by contacting us. Once dispatched, an order cannot be cancelled.</p>
<h2>Refunds</h2><p>Approved refunds are paid to the original payment method within 7 working days.</p><h2>Contact</h2><p>{NAME}, {REGOFF}. {PHONE}, {MAIL}.</p>''')
legal("/terms", "Terms of Use and Sale | Gujarat Bio Organics", "Terms of use and sale", f'''<p>These terms apply to this website and to orders placed with {NAME} ("we").</p>
<h2>Products and advice</h2><p>Product information and crop guides on this site are general guidance. Results depend on soil, weather, crop and management and are not guaranteed. Always follow the label.</p>
<h2>Orders and prices</h2><p>Prices are shared on enquiry, are in Indian rupees and may change. Taxes and delivery charges are confirmed before payment.</p>
<h2>Shipping, cancellation and refunds</h2><p>See <a href="/shipping-and-returns">shipping and returns</a>.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of India. Courts in Bhavnagar, Gujarat have jurisdiction.</p><h2>Contact</h2><p>{NAME}, {REGOFF}. {PHONE}, {MAIL}. CIN {CIN}.</p>''')
legal("/privacy-policy", "Privacy Policy | Gujarat Bio Organics", "Privacy policy", f'''<p>This page explains what {NAME} collects when you use this website or contact us.</p>
<h2>What we collect</h2><ul><li>What you send us on WhatsApp, phone, email or forms: name, phone, location, crop, photos and order details.</li><li>Order and delivery details needed to deliver your order.</li><li>If you allow it, Google Analytics records how the site is used (pages viewed, device, approximate location).</li></ul>
<h2>Why</h2><p>To answer your questions, deliver orders, send crop advice you ask for, and improve the site. We do not sell your details.</p>
<h2>Your choices</h2><p>You can ask us to show, correct or delete your details, or to stop messaging you: write to {MAIL} or message us on WhatsApp. We aim to follow India's Digital Personal Data Protection Act, 2023.</p><h2>Contact</h2><p>{NAME}, {REGOFF}.</p>''')

# ---------------------------------------------------------------- 404, sitemap, robots, llms.txt, media list, redirects
start("/404")
render("/404", "Page not found | Gujarat Bio Organics", "This page was not found.", hero("Page not found", "The page you wanted is not here. Pick your crop or see our products.") + sec(picker().replace('class="picker"', 'class="picker" style="margin-top:0"')))
os.replace(os.path.join(ROOT, "404", "index.html"), os.path.join(ROOT, "404.html")); os.rmdir(os.path.join(ROOT, "404"))
for old in ("how-to-buy",):  # remove pages from the first build
    d = os.path.join(ROOT, old)
    if os.path.isdir(d): import shutil; shutil.rmtree(d)

open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{SITE}{p}</loc><priority>{pr}</priority></url>\n" for p, pr in PAGES) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(f"""# {NAME}
> Farmer website of {NAME}, Bhavnagar, Gujarat, India. Working with farmers since 2006. Makes biostimulants (main line), biofertilizers and organic fertilizers; sells the Immunity range (Specials for 20 crops, formulas for all crops, 11 biofertilizers, soil granules). Business buyers: {B2B}

- Factory: {FACTORY}
- Phone / WhatsApp: {PHONE}; email: {MAIL}
- Approvals: NOCs from the Directorate of Agriculture, Government of Gujarat for 36 Schedule VI biostimulant grades and 11 biofertilizer types.
- Prices are shared on enquiry.

## Immunity products
""" + "".join(f"- [{p['name']}]({SITE}/products/{p['slug']}): {p['line']}\n" for p in PRODUCTS) + "\n## Crop guides\n" +
    "".join(f"- [{c['name']}]({SITE}/crops/{c['slug']}): {c['hook']}\n" for c in CRP) + "\n## Knowledge\n" +
    "".join(f"- [{k['h1']}]({SITE}/knowledge/{k['slug']})\n" for k in KNOW) +
    "".join(f"- [{x['title']}]({SITE}/crop-problems/{x['slug']})\n" for x in PROBLEMS) +
    "".join(f"- [{g['title']}]({SITE}/guides/{g['slug']})\n" for g in GUIDES))

seen = set()
with open(os.path.join(ROOT, "MEDIA_LIST.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["file name", "type", "what to shoot", "first used on page", "status"])
    for fn, kind, desc, page in MEDIA:
        if fn in seen: continue
        seen.add(fn)
        here = os.path.exists(os.path.join(ROOT, "assets", "media", fn)) or os.path.exists(os.path.join(ROOT, "assets", "img", "products", fn))
        w.writerow([fn, "video (MP4)" if kind == "video" else "photo (JPG/WEBP)", desc, SITE + page, "received" if here else "needed"])

exec(open(os.path.join(ROOT, "redirects_map.py"), encoding="utf-8").read())
print(f"built {len(PAGES)} pages, {len(seen)} media slots")
