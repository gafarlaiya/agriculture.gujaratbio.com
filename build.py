#!/usr/bin/env python3
"""Builds agriculture.gujaratbio.com (later www.gujaratbio.com): plain HTML, no dependencies.
Edit the content_*.py files, then run: python3 build.py"""
import os, json, html as H, re, hashlib
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://agriculture.gujaratbio.com"   # change to https://www.gujaratbio.com at launch
TRIAL = True                                   # True: every page is noindex and a trial banner shows
B2B = "https://b2b.gujaratbio.com"
GTM_ID = "GTM-5JDXGL2S"
WA = "919978791167"; PHONE = "+91 99787 91167"; TEL = "+919978791167"; MAIL = "sales@gujaratbio.com"
NAME = "Gujarat Bio Organics Pvt. Ltd."; SHORT = "Gujarat Bio Organics"
CIN = "U24123GJ2009PTC058701"
FACTORY = "Plot No. 321, GIDC 2, Ghanghali Road, Shihor, Bhavnagar, Gujarat 364240"
REGOFF = "First Floor, 110 Shoppers Plaza, Parimal Chowk, Waghawadi Road, Bhavnagar, Gujarat 364002"
SOCIAL = ["https://www.facebook.com/gujaratbio", "https://www.youtube.com/@Gujaratbio"]
RESULTS = "Results differ from farm to farm with soil, weather, crop and management. Farmer experiences on this site are their own reports, not a promise of results."

for _f in ("content_products.py", "content_crops.py", "content_knowledge.py"):
    exec(open(os.path.join(ROOT, _f), encoding="utf-8").read())

def esc(s): return H.escape(str(s), quote=True)
def wa(msg): return f"https://wa.me/{WA}?text={quote(msg)}"
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1-.7-.3-1.5-.7-2.2-1.5-.6-.5-1-1.2-1.2-1.4-.1-.2 0-.4.1-.5l.4-.4.3-.5v-.5l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
TEL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'

def btn_wa(msg, label="WhatsApp us"): return f'<a class="btn btn-wa" href="{wa(msg)}" data-ev="click_whatsapp">{WA_SVG}{esc(label)}</a>'
def btn_call(label="Call us"): return f'<a class="btn btn-line" href="tel:{TEL}" data-ev="click_phone">{TEL_SVG}{esc(label)}</a>'

NAV = [("/crops", "Crops"), ("/crop-problems", "Crop problems"), ("/products", "Immunity products"),
       ("/farmer-stories", "Farmer stories"), ("/guides", "Guides"), ("/about", "About us"), ("/contact", "Contact")]

def header(path):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if path == h or path.startswith(h + "/") else ""}>{t}</a>' for h, t in NAV)
    trial = '<div class="trial">Trial version of the new Gujarat Bio Organics website.</div>' if TRIAL else ""
    return f'''<a class="skip" href="#main">Skip to content</a>{trial}<header class="top"><div class="wrap">
<a class="brand" href="/"><b>Gujarat Bio Organics</b><span>Working with farmers since 2006</span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button><nav class="nav" id="nav" aria-label="Main">{links}</nav></div></header>'''

def footer():
    crops = "".join(f'<li><a href="/crops/{c["slug"]}">{c["name"]}</a></li>' for c in CROPS)
    prods = "".join(f'<li><a href="/products/{p["slug"]}">{p["name"]}</a></li>' for p in PRODUCTS)
    return f'''<div class="biz"><div class="wrap"><h2>Buying for a business?</h2><p>Distributors, brands and importers: bulk supply, private label, OEM and export are on our business site.</p><a class="btn" href="{B2B}/?utm_source=agriculture.gujaratbio.com&amp;utm_medium=referral&amp;utm_campaign=farmer_site">Go to the business site</a></div></div>
<footer class="foot"><div class="wrap"><div class="cols">
<div><h2>{NAME}</h2><p>Biostimulants, biofertilizers and organic fertilizers, made in Bhavnagar, Gujarat. Working with farmers since 2006.</p>
<p>Factory: {FACTORY}<br>Office: {REGOFF}<br>CIN {CIN}</p><p><a href="tel:{TEL}">{PHONE}</a> &middot; <a href="mailto:{MAIL}">{MAIL}</a></p>
<p><a href="{SOCIAL[0]}" rel="noopener">Facebook</a> &middot; <a href="{SOCIAL[1]}" rel="noopener">YouTube</a></p></div>
<div><h2>Crops</h2><ul>{crops}</ul></div><div><h2>Immunity</h2><ul>{prods}<li><a href="/how-to-buy">How to buy</a></li></ul></div>
<div><h2>Company</h2><ul><li><a href="/about">About us</a></li><li><a href="/quality">Quality and approvals</a></li><li><a href="/farmer-stories">Farmer stories</a></li><li><a href="/guides">Guides</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy-policy">Privacy</a></li><li><a href="/terms">Terms</a></li><li><a href="/shipping-and-returns">Shipping and returns</a></li></ul></div>
</div><p class="note" style="color:#bfb3a5;margin-top:20px">{RESULTS}</p><p class="note" style="color:#bfb3a5">&copy; 2026 {NAME}</p></div></footer>
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
      "document.addEventListener('click',function(e){var a=e.target.closest('[data-ev]');if(a){window.dataLayer=window.dataLayer||[];dataLayer.push({event:a.dataset.ev,link_url:a.href,page_path:location.pathname})}});")

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": SITE + "/#org", "name": NAME, "alternateName": ["Gujarat Bio Organics", "GBO"],
       "url": SITE + "/", "foundingDate": "2006", "email": MAIL, "telephone": TEL, "sameAs": SOCIAL + [B2B + "/"],
       "address": {"@type": "PostalAddress", "streetAddress": "Plot No. 321, GIDC 2, Ghanghali Road, Shihor", "addressLocality": "Bhavnagar", "addressRegion": "Gujarat", "postalCode": "364240", "addressCountry": "IN"},
       "brand": {"@type": "Brand", "name": "Immunity"}}

PAGES = []
def render(path, title, desc, body, schemas=None, crumbs=None, prio="0.6"):
    url = SITE + path
    ld = [ORG] if path == "/" else []
    if crumbs:
        items = [("Home", "/")] + crumbs
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or path)} for i, (n, u) in enumerate(items)]})
    ld += schemas or []
    ldh = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = "noindex,follow" if TRIAL else "index,follow,max-image-preview:large"
    assert len(title) <= 65, (path, len(title), title)
    out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">{tracking()}<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="{robots}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{SHORT}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta name="theme-color" content="#1c4720"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="{FONT}">
<style>{CSS}</style>{ldh}</head><body><noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
{header(path)}<main id="main">{body}</main>{footer()}<script>{JS}</script></body></html>'''
    d = ROOT if path == "/" else os.path.join(ROOT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
    if path != "/404": PAGES.append((path, prio))

# ---------------------------------------------------------------- building blocks
def hero(title, lead, crumbs=None, light=False):
    cr = ""
    if crumbs:
        cr = '<div class="crumbs"><a href="/">Home</a>' + "".join(f' / <a href="{u}">{esc(n)}</a>' if u else f' / {esc(n)}' for n, u in crumbs) + "</div>"
    return f'<section class="hero{" light" if light else ""}"><div class="wrap">{cr}<h1>{esc(title)}</h1><p class="lead">{esc(lead)}</p></div></section>'
def sec(inner, title=None, sub=None, tint=False):
    t = f"<h2>{esc(title)}</h2>" if title else ""
    s = f'<p class="sub">{esc(sub)}</p>' if sub else ""
    return f'<section class="sec{" tint" if tint else ""}"><div class="wrap">{t}{s}{inner}</div></section>'
def ul(items, cls="ticks"): return f'<ul class="{cls}">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"
def answer(t): return f'<p class="answer">{esc(t)}</p>'
def faq_html(qs): return '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in qs) + "</div>"
def faq_ld(qs): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}
def video_slot(label): return f'<div class="slot video" role="img" aria-label="Video coming soon: {esc(label)}"><span>Farmer video coming soon</span><span class="note">{esc(label)}</span></div>'
def card(href, title, text, meta="", more="Read more"):
    m = f'<div class="meta">{esc(meta)}</div>' if meta else ""
    return f'<article class="card">{m}<h3><a href="{href}">{esc(title)}</a></h3><p>{esc(text)}</p><a class="more" href="{href}">{esc(more)}</a></article>'
def help_box(crop=""):
    msg = f"Hello Gujarat Bio Organics, I grow {crop}. I need help with my crop." if crop else "Hello Gujarat Bio Organics, I need help with my crop."
    return sec(f'<p class="prose">Send a photo of the crop, your location and what you see. Our team replies on WhatsApp with what to check and a programme for your field.</p><div class="btns">{btn_wa(msg, "Send a photo on WhatsApp")}{btn_call()}</div>', "Ask us about your crop", tint=True)
def article_ld(path, headline, desc):
    return {"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": desc, "mainEntityOfPage": SITE + path,
            "author": {"@type": "Person", "name": "Gafar Laiya", "jobTitle": "Founder, Gujarat Bio Organics", "url": SITE + "/about"},
            "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-IN"}

# ---------------------------------------------------------------- home
picker = '<div class="picker">' + "".join(f'<a href="/crops/{c["slug"]}"><b>{c["name"]}</b><span>{esc(c["hook"])}</span></a>' for c in CROPS) + "</div>"
home_faq = [("Who is Gujarat Bio Organics?", f"{NAME} makes biostimulants, biofertilizers and organic fertilizers at its own factory in Shihor, Bhavnagar, Gujarat. We have worked with farmers since 2006 and sell crop formulas under the Immunity brand."),
            ("Which crops do Immunity products cover?", "Immunity has Specials for sugarcane, potato, mango and apple. Immunity Gold is for all other crops, and Immunity Granules go into the soil for any crop."),
            ("How do I buy Immunity?", "Order on WhatsApp or by phone, or buy online from the product page. We deliver across India."),
            ("Can you tell me what to use on my crop?", "Yes. Send a photo, your location and the problem on WhatsApp. Our team replies with what to check and a programme for your field.")]
home = f'''<section class="hero"><div class="wrap"><h1>What do you grow?</h1>
<p class="lead">Pick your crop for a stage-by-stage guide, the problems farmers face, and what has worked for them. From {SHORT}, working with farmers since 2006.</p>{picker}</div></section>'''
home += sec('<div class="grid">' + "".join(card(f"/products/{p['slug']}", p["name"], p["line"], p["price"], "See product") for p in PRODUCTS) + "</div>",
            "Immunity crop formulas", "Specials for sugarcane, potato, mango and apple; Gold for every other crop; Granules for the soil.")
home += sec('<div class="grid">' + "".join(card(f"/crop-problems/{p['slug']}", p["h1"][0].upper() + p["h1"][1:], p["answer"][:140].rsplit(" ", 1)[0] + "...", CBY[p["crop"]]["name"]) for p in PROBLEMS[:6]) + "</div>",
            "Common crop problems", "What you see in the field, why it happens and what growers can do.", tint=True)
home += sec('<div class="grid">' + video_slot("Sugarcane grower, South Gujarat") + video_slot("Mango grower") + video_slot("Apple grower, Himachal Pradesh") + '</div><p class="btns"><a class="btn btn-line" href="/farmer-stories">All farmer stories</a></p>',
            "Farmers in their own words", "Growers tell what they faced and what changed on their farm.")
home += sec(f'''<div class="grid two"><div class="prose"><p>{SHORT} started in 2006 in Bhavnagar, Gujarat. For nearly 20 years we have worked on real farms, with sugarcane growers in South Gujarat, potato growers in Punjab and Haryana, apple growers in Himachal Pradesh and Jammu and Kashmir, and mango growers across India.</p>
<p>We make biostimulants, biofertilizers and organic fertilizers at our own factory in Shihor. Biostimulants are our main line: humic and fulvic acid, seaweed extract and amino acids.</p><p><a class="btn btn-leaf" href="/about">About us</a></p></div>
<div><ul class="ticks"><li>Working with farmers since 2006</li><li>Own factory in Shihor, Bhavnagar, Gujarat</li><li>36 biostimulant grades and 11 biofertilizer types covered by NOCs from the Directorate of Agriculture, Government of Gujarat</li><li>In-house R&amp;D and quality control</li></ul></div></div>''', "Nearly 20 years on Indian farms", tint=True)
home += sec('<div class="grid">' + "".join(card(f"/guides/{g['slug']}", g["h1"], g["desc"], "Guide") for g in GUIDES[:3]) + "</div>", "Farming guides")
home += sec(faq_html(home_faq), "Questions farmers ask", tint=True)
render("/", "Gujarat Bio Organics: Crop Guides & Immunity Formulas",
       "Crop guides for sugarcane, potato, mango, apple and more, and Immunity biostimulant formulas from Gujarat Bio Organics, Bhavnagar. Working with farmers since 2006.",
       home, [faq_ld(home_faq), {"@context": "https://schema.org", "@type": "WebSite", "url": SITE + "/", "name": SHORT, "publisher": {"@id": SITE + "/#org"}}], None, "1.0")

# ---------------------------------------------------------------- crops
render("/crops", "Crop Guides: Sugarcane, Potato, Mango, Apple & More | GBO",
       "Stage-by-stage crop guides with common problems and what to check, for sugarcane, potato, mango, apple, banana, citrus, coconut and cotton.",
       hero("Crop guides", "Each guide follows the crop stage by stage, lists the problems farmers bring to us, and what to check in the field.", [("Crops", None)])
       + sec(picker.replace('class="picker"', 'class="picker" style="margin-top:0"')) + help_box(), None, [("Crops", None)], "0.9")

for c in CROPS:
    p = PBY[c["product"]]
    path = f"/crops/{c['slug']}"
    probs = [x for x in PROBLEMS if x["crop"] == c["slug"]]
    stages = '<ol class="stages">' + "".join(f'<li><h3>{esc(n)}</h3><div class="when">{esc(w)}</div><p>{esc(t)}</p></li>' for n, w, t in c["stages"]) + "</ol>"
    body = hero(f"{c['name']} guide", c["hook"], [("Crops", "/crops"), (c["name"], None)])
    body += sec(answer(c["intro"]) + f'<p class="prose">Main growing areas: {esc(c["where"])}.</p>' + stages, f"{c['name']} stage by stage")
    body += sec(f'<div class="grid two"><div><h3>Problems farmers bring to us</h3>{ul(c["problems"])}</div><div><h3>What to check first</h3>{ul(c["checks"])}</div></div>'
                + ("<h3>Read more</h3><ul>" + "".join(f'<li><a href="/crop-problems/{x["slug"]}">{esc(x["h1"][0].upper() + x["h1"][1:])}</a></li>' for x in probs) + "</ul>" if probs else ""),
                f"Common {c['name'].lower()} problems", tint=True)
    special = p["crop"] == c["slug"]
    lead = (f"{p['name']} was made for {c['name'].lower()}. {p['story']}" if special else
            f"There is no Immunity Special for {c['name'].lower()} yet. Growers use Immunity Gold on the crop and Immunity Granules in the soil, as part of a balanced programme.")
    body += sec(f'<div class="grid two"><div class="prose"><p>{esc(lead)}</p><div class="btns"><a class="btn btn-leaf" href="/products/{p["slug"]}">See {esc(p["name"])}</a>{btn_wa(f"Hello Gujarat Bio Organics, I grow {c["name"].lower()}. Please send a programme.", "Ask for a programme")}</div>'
                f'<p class="note">{RESULTS}</p></div>{video_slot(c["name"] + " grower")}</div>', f"What we offer {c['name'].lower()} growers")
    body += sec(faq_html(c["faq"]), f"{c['name']} questions", tint=True) + help_box(c["name"].lower())
    render(path, f"{c['name']} Farming Guide: Stages, Problems & Care | GBO",
           f"{c['name']} guide for growers in {c['where'].split(' and ')[0]}: stage-by-stage care, common problems, what to check and how Immunity formulas fit.",
           body, [faq_ld(c["faq"]), article_ld(path, f"{c['name']} farming guide", c["intro"])], [("Crops", "/crops"), (c["name"], None)], "0.8")

# ---------------------------------------------------------------- crop problems
render("/crop-problems", "Crop Problems: Causes, Signs and What to Do | GBO",
       "Plain guides to common crop problems: apple root rot, mango fruit drop and alternate bearing, sugarcane poor germination, small potatoes and citrus dieback.",
       hero("Crop problems", "What you see in the field, why it happens, and what growers can do.", [("Crop problems", None)])
       + sec('<div class="grid">' + "".join(card(f"/crop-problems/{x['slug']}", x["h1"][0].upper() + x["h1"][1:], x["answer"][:150].rsplit(" ", 1)[0] + "...", CBY[x["crop"]]["name"]) for x in PROBLEMS) + "</div>")
       + help_box(), None, [("Crop problems", None)], "0.8")

def article_page(base, basename, x, crop=None):
    path = f"/{base}/{x['slug']}"
    body = hero(x["h1"][0].upper() + x["h1"][1:], x["desc"], [(basename, f"/{base}"), (x["h1"].split(":")[0][:40], None)], light=True)
    inner = answer(x["answer"]) + "".join(f"<h2>{esc(h)}</h2>" + ul(items, "") for h, items in x["sections"])
    if crop:
        c = CBY[crop]; p = PBY[c["product"]]
        inner += f'<p>See the full <a href="/crops/{crop}">{c["name"].lower()} guide</a> and <a href="/products/{p["slug"]}">{p["name"]}</a>.</p>'
    inner += f'<p class="note">Written by Gafar Laiya, founder of {SHORT}, working with farmers since 2006. {RESULTS}</p>'
    body += sec(f'<div class="prose">{inner}</div>') + sec(faq_html(x["faq"]), "Questions", tint=True) + help_box(CBY[crop]["name"].lower() if crop else "")
    render(path, x["title"] if len(x["title"]) <= 65 else x["title"][:62], x["desc"], body, [faq_ld(x["faq"]), article_ld(path, x["h1"], x["desc"])],
           [(basename, f"/{base}"), (x["h1"].split(":")[0][:40], None)], "0.7")

for x in PROBLEMS: article_page("crop-problems", "Crop problems", x, x["crop"])

# ---------------------------------------------------------------- guides
render("/guides", "Farming Guides: Soil Health, Biostimulants & More | GBO",
       "Plain farming guides from Gujarat Bio Organics: biostimulants, tired soil, compost and humic acid, and how to take a soil sample.",
       hero("Farming guides", "Plain answers to the questions farmers ask us most.", [("Guides", None)])
       + sec('<div class="grid">' + "".join(card(f"/guides/{g['slug']}", g["h1"], g["desc"], "Guide") for g in GUIDES) + "</div>"
             + '<p class="note" style="margin-top:20px">More guides from our old website are being checked and moved here.</p>') + help_box(), None, [("Guides", None)], "0.8")
for g in GUIDES: article_page("guides", "Guides", g)

# ---------------------------------------------------------------- products
render("/products", "Immunity Crop Formulas: Mango, Sugarcane, Potato, Apple | GBO",
       "Immunity Sugarcane, Potato, Mango and Apple Special, Immunity Gold for all crops and Immunity Granules for the soil. Order on WhatsApp or online.",
       hero("Immunity crop formulas", "Specials for four crops, Gold for every other crop, and Granules for the soil. Made by Gujarat Bio Organics in Bhavnagar, Gujarat.", [("Immunity products", None)])
       + sec('<div class="grid">' + "".join(card(f"/products/{p['slug']}", p["name"], p["line"], p["price"], "See product") for p in PRODUCTS) + "</div>"
             + f'<p class="note" style="margin-top:18px">Prices include the current online offer and may change. The price is confirmed when you order. <a href="/how-to-buy">How to buy</a>.</p>')
       + help_box(), None, [("Immunity products", None)], "0.9")

for p in PRODUCTS:
    path = f"/products/{p['slug']}"
    rows = "".join(f'<tr><td>{esc(a)}</td><td>{(esc(b) + (" <s>" + esc(c) + "</s>" if c else "")) if b else "Ask for price"}</td></tr>' for a, b, c in p["packs"]) if p["packs"] else '<tr><td colspan="2">Pack sizes and price on request</td></tr>'
    buy = p["pay"] or p["store"]
    msg = f"Hello Gujarat Bio Organics, I want to order {p['name']}. Pack size: / Quantity: / Delivery pincode:"
    crop_link = f'<p>Made for: <a href="/crops/{p["crop"]}">{CBY[p["crop"]]["name"]}</a>.</p>' if p["crop"] else '<p>For all crops. See the <a href="/crops">crop guides</a>.</p>'
    body = hero(p["name"], p["line"], [("Immunity products", "/products"), (p["short"], None)])
    body += sec(f'''<div class="pbox"><div class="slot" role="img" aria-label="Product photo coming soon">Product photo and label coming soon</div>
<div><p><b>Form:</b> {esc(p["form"])}</p>{crop_link}<table class="packs"><thead><tr><th>Pack</th><th>Price</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">Price shown includes the current online offer; confirmed when you order.</p>
<div class="btns">{btn_wa(msg, "Order on WhatsApp")}<a class="btn btn-leaf" href="{buy}" data-ev="begin_checkout" rel="nofollow">Buy online</a>{btn_call()}</div>
<p class="note">Delivery across India. See <a href="/how-to-buy">how to buy</a> and <a href="/shipping-and-returns">shipping and returns</a>.</p></div></div>''')
    body += sec(f'<div class="grid two"><div><h3>Made for</h3>{ul(p["made_for"])}</div><div class="prose"><h3>How it was developed</h3><p>{esc(p["story"])}</p></div></div>', "Who it is for", tint=True)
    body += sec(f'<div class="prose"><p>The right amount and timing depend on your crop, its stage and your soil. Every pack carries the label dose. Send us your crop, stage and location on WhatsApp and our team will send a schedule for your field.</p></div><div class="btns">{btn_wa(f"Hello Gujarat Bio Organics, please send the schedule for {p["name"]}. Crop: / Stage: / Location:", "Get a schedule on WhatsApp")}</div>', "How to use it")
    body += sec('<div class="grid">' + video_slot(p["name"] + ": farmer story") + video_slot(p["name"] + ": how to apply") + video_slot(p["name"] + ": field visit") + f'</div><p class="note" style="margin-top:14px">{RESULTS}</p>', "Farmer videos", tint=True)
    pfaq = [(f"What is {p['name']}?", f"{p['line']} It is made by {NAME} in Bhavnagar, Gujarat."),
            (f"How do I order {p['name']}?", "Order on WhatsApp or by phone, or tap Buy online. We deliver across India."),
            ("How much should I use?", "The dose depends on crop, stage and soil. Follow the label, or ask us on WhatsApp for a schedule for your field."),
            ("Can I use it with my other fertilizers and sprays?", "Usually yes, as part of a balanced programme. Ask us before mixing it with any specific product.")]
    body += sec(faq_html(pfaq), "Questions")
    prod_ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["line"], "brand": {"@type": "Brand", "name": "Immunity"},
               "manufacturer": {"@id": SITE + "/#org"}, "category": "Organic fertilizer / biostimulant"}
    render(path, f"{p['name']}: Price, Packs & How to Order | GBO"[:65], f"{p['line']} Packs, price, who it is for and how to order on WhatsApp or online.",
           body, [prod_ld, faq_ld(pfaq)], [("Immunity products", "/products"), (p["short"], None)], "0.8")

# ---------------------------------------------------------------- farmer stories
stories = [("Last year I did 3 times re-transplanting of my sugarcane crop.", "Jagdish Bhai", "Sugarcane grower, on the problem he faced before working with us"),
           ("Reported a single sugarcane of 4.5 kg from his field, shown in his Facebook video.", "Dharmesh Patel", "Sugarcane grower, South Gujarat. Farmer reported")]
sq = '<div class="grid two">' + "".join(f'<blockquote class="quote"><p>{esc(t)}</p><cite>{esc(n)}</cite><span class="tag">{esc(r)}</span></blockquote>' for t, n, r in stories) + "</div>"
render("/farmer-stories", "Farmer Stories and Videos | Gujarat Bio Organics",
       "Farmers growing sugarcane, potato, mango and apple tell what they faced on their farms and what changed. Videos and farmer reports.",
       hero("Farmer stories", "Growers tell, in their own words, what they faced and what changed on their farm.", [("Farmer stories", None)])
       + sec('<div class="grid">' + "".join(video_slot(f"{c['name']} grower") for c in CROPS[:6]) + "</div>", "Farmer videos", "Videos from our field visits are being added.")
       + sec(sq + f'<p class="note" style="margin-top:16px">{RESULTS}</p>', "What farmers told us", tint=True)
       + sec(f'<p class="prose">Have you used Immunity on your farm? Send us your story and photos on WhatsApp. With your permission, we will share it to help other farmers.</p><div class="btns">{btn_wa("Hello Gujarat Bio Organics, I want to share my farm story.", "Share your story")}</div>', "Share your story"),
       None, [("Farmer stories", None)], "0.7")

# ---------------------------------------------------------------- company
about = hero("About Gujarat Bio Organics", "Working with farmers since 2006. Biostimulants, biofertilizers and organic fertilizers, made in Bhavnagar, Gujarat.", [("About us", None)])
about += sec(f'''<div class="prose"><p>{SHORT} started in 2006 in Bhavnagar, Gujarat. From the beginning the work has been on real farms: walking fields with growers, finding out why a crop was failing, and building formulas that solve those problems.</p>
<p>That work led to the Immunity crop formulas. Sugarcane Special came from growers in South Gujarat whose land had grown sugarcane for about five decades. Potato Special came from growers in Punjab and Haryana. Apple Special came from orchards in Himachal Pradesh and Jammu and Kashmir. Mango Special came from mango growers across India.</p>
<h2>What we make</h2>{ul(["Biostimulants, our main line: humic and fulvic acid, seaweed extracts, amino acids and protein hydrolysates", "Biofertilizers: nitrogen fixers, phosphate, potash and zinc solubilisers, mycorrhiza and consortia", "Organic fertilizers and the Immunity crop formulas"])}
<h2>How we make it</h2><p>Everything is made at our own factory in Shihor, Bhavnagar. Nearly 20 years of field work have taught us which raw materials work. We extract them in-house without harsh chemicals, very high pH or heat, because the helpful substances in humus and seaweed are fragile.</p>
<h2>What we believe</h2><p>We want to make farming free of hazardous chemicals and make sustainable food growing easier for the generations to come.</p>
<h2>Founder</h2><p>Gafar Laiya founded {SHORT} and leads its product development and farmer programmes. He writes many of the guides on this site.</p>
<h2>Company details</h2><p>{NAME}<br>Factory: {FACTORY}<br>Registered office: {REGOFF}<br>CIN {CIN}</p></div>''')
about += sec(f'<div class="grid">{video_slot("Our factory in Shihor")}{video_slot("20 years in the field")}{video_slot("Our R&amp;D lab".replace("&amp;", "&"))}</div>', "See our work", tint=True)
render("/about", "About Gujarat Bio Organics: Since 2006, Bhavnagar", "Gujarat Bio Organics has worked with farmers since 2006 and makes biostimulants, biofertilizers and organic fertilizers at its own factory in Shihor, Bhavnagar, Gujarat.",
       about, [ORG], [("About us", None)], "0.8")

quality = hero("Quality and approvals", "How we make and check our products, and the approvals we hold.", [("Quality", None)], light=True)
quality += sec(f'''<div class="prose">{answer("The Directorate of Agriculture, Government of Gujarat has issued No Objection Certificates to Gujarat Bio Organics for 36 biostimulant grades listed in Schedule VI of the Fertiliser Control Order and 11 biofertilizer types.")}
<h2>Why approvals matter</h2><p>Since June 2025 only biostimulants listed in Schedule VI of the Fertiliser Control Order can be sold in India. Before you buy any biostimulant, ask the seller which Schedule VI grade it is and for proof of approval.</p>
<h2>How we check quality</h2>{ul(["Raw materials chosen from nearly 20 years of field experience", "Made at our own factory in Shihor, Bhavnagar", "In-house quality control on every batch", "Third-party testing available for bulk buyers"])}
<p>Full grade lists and specifications are on our <a href="{B2B}/quality-compliance">business site</a>.</p></div>''')
render("/quality", "Quality and Approvals | Gujarat Bio Organics", "Gujarat Bio Organics holds NOCs from the Directorate of Agriculture, Gujarat for 36 Schedule VI biostimulant grades and 11 biofertilizer types. How we check quality.",
       quality, None, [("Quality", None)], "0.6")

howbuy = hero("How to buy Immunity", "Order on WhatsApp, by phone or online. We deliver across India.", [("How to buy", None)], light=True)
howbuy += sec(f'''<ol class="stages"><li><h3>Choose your product</h3><p>Pick the <a href="/products">Immunity formula</a> for your crop. Not sure? Send a photo on WhatsApp and we will suggest one.</p></li>
<li><h3>Order</h3><p>Send the product, pack size, quantity and delivery pincode on WhatsApp, call us, or tap Buy online on the product page.</p></li>
<li><h3>Pay</h3><p>Pay online (UPI, cards, net banking) through a secure payment link. We confirm the price and delivery charge before you pay.</p></li>
<li><h3>Delivery</h3><p>Orders are dispatched within 1 to 7 working days by courier or transport. You get the tracking details on WhatsApp.</p></li></ol>
<div class="btns">{btn_wa("Hello Gujarat Bio Organics, I want to order Immunity. Product: / Pack: / Quantity: / Pincode:", "Order on WhatsApp")}{btn_call()}</div>''')
render("/how-to-buy", "How to Buy Immunity: WhatsApp, Phone or Online | GBO", "Order Immunity crop formulas on WhatsApp, by phone or online. Secure payment, dispatch within 1 to 7 working days, delivery across India.",
       howbuy, None, [("How to buy", None)], "0.6")

contact = hero("Contact us", "Questions about your crop or an order? We reply on WhatsApp and by phone.", [("Contact", None)], light=True)
contact += sec(f'''<div class="grid two"><div><h2>Farmers and orders</h2><p>WhatsApp or call: <a href="tel:{TEL}">{PHONE}</a><br>Email: <a href="mailto:{MAIL}">{MAIL}</a></p><div class="btns">{btn_wa("Hello Gujarat Bio Organics, I have a question.")}{btn_call()}</div>
<h2>Business buyers</h2><p>Bulk, private label, OEM and export: <a href="{B2B}/contact">business site contact page</a>.</p></div>
<div><h2>Visit us</h2><p><b>Factory</b><br>{FACTORY}</p><p><b>Registered office</b><br>{REGOFF}</p><p>{NAME}<br>CIN {CIN}</p></div></div>''')
render("/contact", "Contact Gujarat Bio Organics | WhatsApp, Phone, Address", "Contact Gujarat Bio Organics on WhatsApp or phone (+91 99787 91167), email sales@gujaratbio.com, or visit our factory in Shihor, Bhavnagar, Gujarat.",
       contact, None, [("Contact", None)], "0.7")

# ---------------------------------------------------------------- legal (drafts: confirm before Razorpay goes live)
def legal(path, title, h, inner):
    render(path, title, f"{h} for orders placed with {NAME}.", hero(h, f"{NAME}", [(h, None)], light=True) + sec(f'<div class="prose">{inner}</div>'), None, [(h, None)], "0.2")
legal("/shipping-and-returns", "Shipping and Returns | Gujarat Bio Organics", "Shipping and returns", f'''<h2>Shipping</h2><p>Orders are processed and dispatched within 1 to 7 working days from order confirmation. We ship by courier, transport agency or another suitable carrier, and share tracking details on WhatsApp or email.</p>
<p>Delivery charges, if any, are confirmed before you pay.</p><h2>Damaged or wrong items</h2><p>If your order arrives damaged, leaking or wrong, send photos of the pack and the parcel on WhatsApp ({PHONE}) or to {MAIL} within 48 hours of delivery. We will replace the item or refund it after checking.</p>
<h2>Cancellations</h2><p>You can cancel an order before it is dispatched by contacting us on WhatsApp or by email. Once dispatched, an order cannot be cancelled.</p>
<h2>Refunds</h2><p>Approved refunds are paid to the original payment method within 7 working days.</p><h2>Contact</h2><p>{NAME}, {REGOFF}. {PHONE}, {MAIL}.</p>''')
legal("/terms", "Terms of Use and Sale | Gujarat Bio Organics", "Terms of use and sale", f'''<p>These terms apply to this website and to orders placed with {NAME} ("we").</p>
<h2>Products and advice</h2><p>Product information and crop guides on this site are general guidance. Results depend on soil, weather, crop and management and are not guaranteed. Always follow the label.</p>
<h2>Orders and prices</h2><p>Prices are in Indian rupees and may change. The price and any delivery charge are confirmed before payment. We may decline an order, for example if a product is out of stock, and will refund any payment received.</p>
<h2>Payment</h2><p>Online payments are processed by a secure payment provider. We do not store your card details.</p>
<h2>Shipping, cancellation and refunds</h2><p>See <a href="/shipping-and-returns">shipping and returns</a>.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of India. Courts in Bhavnagar, Gujarat have jurisdiction.</p><h2>Contact</h2><p>{NAME}, {REGOFF}. {PHONE}, {MAIL}. CIN {CIN}.</p>''')
legal("/privacy-policy", "Privacy Policy | Gujarat Bio Organics", "Privacy policy", f'''<p>This page explains what {NAME} collects when you use this website or contact us.</p>
<h2>What we collect</h2><ul><li>What you send us on WhatsApp, phone, email or forms: your name, phone number, location, crop, photos and order details.</li><li>Order and delivery details needed to deliver your order. Payments are handled by our payment provider; we do not store card details.</li><li>If you allow it, Google Analytics records how the site is used (pages viewed, device, approximate location).</li></ul>
<h2>Why</h2><p>To answer your questions, deliver orders, send crop advice you ask for, and improve the site. We do not sell your details.</p>
<h2>Your choices</h2><p>You can ask us to show, correct or delete your details, or to stop messaging you: write to {MAIL} or message us on WhatsApp. We aim to follow India's Digital Personal Data Protection Act, 2023.</p><h2>Contact</h2><p>{NAME}, {REGOFF}.</p>''')

# ---------------------------------------------------------------- 404, sitemap, robots, llms.txt
render("/404", "Page not found | Gujarat Bio Organics", "This page was not found.", hero("Page not found", "The page you wanted is not here. Try a crop guide or our products.") + sec(picker.replace('class="picker"', 'class="picker" style="margin-top:0"')))
os.replace(os.path.join(ROOT, "404", "index.html"), os.path.join(ROOT, "404.html")); os.rmdir(os.path.join(ROOT, "404"))

open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{SITE}{p if p != '/' else '/'}</loc><priority>{pr}</priority></url>\n" for p, pr in PAGES) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(f"""# {NAME}
> Farmer website of {NAME}, Bhavnagar, Gujarat, India. Working with farmers since 2006. Makes biostimulants (main line), biofertilizers and organic fertilizers; sells the Immunity crop formulas. Business buyers: {B2B}

- Factory: {FACTORY}
- Phone / WhatsApp: {PHONE}; email: {MAIL}
- Approvals: NOCs from the Directorate of Agriculture, Government of Gujarat for 36 Schedule VI biostimulant grades and 11 biofertilizer types.

## Immunity products
""" + "".join(f"- [{p['name']}]({SITE}/products/{p['slug']}): {p['line']}\n" for p in PRODUCTS) + "\n## Crop guides\n" +
    "".join(f"- [{c['name']}]({SITE}/crops/{c['slug']}): {c['hook']}\n" for c in CROPS) + "\n## Crop problems\n" +
    "".join(f"- [{x['title']}]({SITE}/crop-problems/{x['slug']})\n" for x in PROBLEMS) + "\n## Guides\n" +
    "".join(f"- [{g['title']}]({SITE}/guides/{g['slug']})\n" for g in GUIDES))
print(f"built {len(PAGES)} pages")
