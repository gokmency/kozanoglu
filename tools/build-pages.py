# Kozanoğlu alt sayfa + blog üretici.
# Kullanım (repo kökünde): python3 -I tools/build-pages.py . && python3 -I tools/sitemap.py .
# Blog yazıları: content/blog/*.md  (yeni yazı için POSTS listesine satır ekleyin)
import json, sys, os, html

OUT = sys.argv[1]
__file__ = os.path.abspath(__file__)
SITE = "https://kozanogluhukuk.com"
TEL = "+902422445420"
TEL_TXT = "(0242) 244 54 20"
MAP = "https://share.google/ynnFKMV5p0aNbcGuE"
ORG_ID = SITE + "/#organization"

FONTS = """<link rel="preload" href="/assets/fonts/cabinet-grotesk-500.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/general-sans-400.woff2" as="font" type="font/woff2" crossorigin>
  <style>@font-face{font-family:"Cabinet Grotesk";src:url(/assets/fonts/cabinet-grotesk-500.woff2) format("woff2");font-weight:500;font-display:swap}@font-face{font-family:"General Sans";src:url(/assets/fonts/general-sans-400.woff2) format("woff2");font-weight:400;font-display:swap}@font-face{font-family:"General Sans";src:url(/assets/fonts/general-sans-500.woff2) format("woff2");font-weight:500;font-display:swap}@font-face{font-family:"Satoshi";src:url(/assets/fonts/satoshi-500.woff2) format("woff2");font-weight:500;font-display:swap}</style>"""

BOOT = """<script>(()=>{try{const entry=performance.getEntriesByType('navigation')[0],type=entry?entry.type:'navigate',mobile=['(max-width: 720px)','(orientation: portrait) and (max-width: 1024px)','(orientation: portrait) and (pointer: coarse)','(orientation: landscape) and (pointer: coarse) and (max-height: 560px)','(prefers-reduced-motion: reduce)'].some(query=>matchMedia(query).matches),incoming=sessionStorage.getItem('kozanoglu-page-transition')==='1';sessionStorage.removeItem('kozanoglu-page-transition');if(!mobile){if(incoming&&type!=='back_forward')document.documentElement.classList.add('page-arriving');else if(type==='reload')document.documentElement.classList.add('page-reloading')}}catch(error){}})();</script>"""

ORG = {
    "@type": ["LegalService", "Organization"], "@id": ORG_ID,
    "name": "Kozanoğlu Hukuk Bürosu", "url": SITE + "/",
    "logo": SITE + "/assets/logo-white-optimized.png", "image": SITE + "/assets/og-kozanoglu.jpg",
    "telephone": "+90 242 244 54 20",
    "address": {"@type": "PostalAddress", "streetAddress": "Emek Mah. Yeşilırmak Cd. No:19/2", "postalCode": "07030", "addressLocality": "Kepez", "addressRegion": "Antalya", "addressCountry": "TR"},
    "hasMap": MAP,
    "areaServed": [{"@type": "AdministrativeArea", "name": "Kepez"}, {"@type": "Place", "name": "Varsak, Kepez"}, {"@type": "City", "name": "Antalya"}],
    "knowsAbout": ["Aile hukuku", "Boşanma", "Ceza hukuku", "Gayrimenkul hukuku", "Kira hukuku", "Miras hukuku", "İş hukuku", "İcra ve iflas hukuku", "Ticaret hukuku"],
    "employee": [{"@type": "Person", "name": n, "jobTitle": t} for n, t in [("Osman Kozanoğlu", "Avukat"), ("Hüseyin Kozanoğlu", "Avukat"), ("Beyza Kozanoğlu", "Avukat"), ("Abdullah Kozanoğlu", "Stajyer Avukat")]],
}

NAV = [("/hakkimizda", "Hakkımızda", None), ("/calisma-alanlari", "Çalışma Alanları", "Alanlar"), ("/blog", "Blog", None), ("/iletisim", "İletişim", None)]

AREAS = [
    ("/aile-hukuku", "Boşanma ve aile hukuku", "Anlaşmalı ve çekişmeli boşanma, velayet, nafaka, mal paylaşımı"),
    ("/ceza-hukuku", "Ceza hukuku", "İfade ve gözaltı, asliye ve ağır ceza davaları, mağdur vekilliği"),
    ("/gayrimenkul-kira-miras", "Gayrimenkul, kira ve miras", "Kira artışı ve tahliye, tapu, ortaklığın giderilmesi, miras paylaşımı"),
    ("/is-icra-ticaret", "İş, icra ve ticaret hukuku", "İşçi alacakları, işe iade, icra takibi, alacak ve sözleşme işleri"),
]

def e(s):
    return html.escape(s, quote=True)

def nav(current):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>' + (f'<span class="l-full">{t}</span><span class="l-short">{s}</span>' if s else t) + "</a>"
        for h, t, s in NAV)
    return f'<nav class="site-nav" aria-label="Ana navigasyon"><a class="brand" href="/" aria-label="Kozanoğlu Hukuk Bürosu ana sayfa"><img src="/assets/logo.webp" width="724" height="543" fetchpriority="high" alt="Kozanoğlu Hukuk Bürosu"></a><div class="nav-links">{links}</div><span class="nav-spacer" aria-hidden="true"></span></nav>'

def footer():
    area_links = "".join(f'<a href="{h}">{t}</a>' for h, t, _ in AREAS)
    return f'''<footer class="site-footer">
    <div class="footer-grid">
      <div><p class="footer-title">Kozanoğlu Hukuk Bürosu</p><address>Emek Mah. Yeşilırmak Cd. No:19/2<br>07030 Kepez / Antalya</address><a class="footer-tel" href="tel:{TEL}">{TEL_TXT}</a></div>
      <nav aria-label="Çalışma alanları"><p class="footer-title">Çalışma alanları</p>{area_links}</nav>
      <nav aria-label="Site"><p class="footer-title">Büro</p><a href="/hakkimizda">Hakkımızda</a><a href="/kepez-varsak-avukat">Kepez ve Varsak</a><a href="/blog">Hukuk notları</a><a href="/iletisim">İletişim ve yol tarifi</a></nav>
    </div>
    <p class="footer-legal">Bu sitedeki içerikler genel bilgilendirme amaçlıdır, hukuki görüş yerine geçmez. Avukatlık meslek kuralları gereği sonuç vaadinde bulunmayız.</p>
    <div class="footer-row"><span>© 2026 Kozanoğlu Hukuk Bürosu · Kepez, Antalya</span><a class="grainz" href="https://grainzdigital.com" target="_blank" rel="noopener noreferrer">Dijital deneyim · <strong>Grainz Digital</strong></a><a href="tel:{TEL}">{TEL_TXT}</a></div>
  </footer>'''

def page(path, title, desc, hero_img, graph, body, og_desc=None, og_img=None, og_type="website"):
    url = SITE + path
    graph = [ORG, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Kozanoğlu Hukuk Bürosu", "inLanguage": "tr-TR", "publisher": {"@id": ORG_ID}}] + graph
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    og = e(og_desc or desc)
    return f'''<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <link rel="canonical" href="{url}"><meta name="theme-color" content="#171717">
  <meta name="geo.region" content="TR-07"><meta name="geo.placename" content="Kepez, Antalya">
  <meta property="og:locale" content="tr_TR"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Kozanoğlu Hukuk Bürosu"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{og}"><meta property="og:image" content="{SITE}{og_img or '/assets/og-kozanoglu.jpg'}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:url" content="{url}">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{og}"><meta name="twitter:image" content="{SITE}{og_img or '/assets/og-kozanoglu.jpg'}">
  <link rel="preload" as="image" href="/assets/{hero_img}" fetchpriority="high">
  {FONTS}
  <link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/pages.css">
  {BOOT}
  <link rel="stylesheet" href="/transitions.css"><script defer src="/transitions.js"></script>
  <script type="application/ld+json">{ld}</script>
</head>
<body>
  <div class="page-transition" aria-hidden="true"><img src="/assets/logo.webp" width="724" height="543" decoding="async" alt=""></div>
  <a class="skip" href="#main">İçeriğe geç</a>
  {nav(path)}
  <main id="main" tabindex="-1">
{body}
  </main>
  {footer()}
</body>
</html>
'''

def crumbs(*items):
    lst = [("Ana Sayfa", SITE + "/")] + [(n, SITE + p) for n, p in items]
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(lst)]}

def webpage(path, kind, name, desc):
    return {"@type": kind, "@id": SITE + path + "#webpage", "url": SITE + path, "name": name, "description": desc, "about": {"@id": ORG_ID}, "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "tr-TR"}

def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def hero(img, eyebrow, h1, lead, crumb=None):
    c = ""
    if crumb:
        c = '<nav class="crumbs" aria-label="Sayfa yolu"><a href="/">Ana sayfa</a>' + "".join(f'<span aria-hidden="true">/</span><a href="{h}">{t}</a>' for h, t in crumb) + "</nav>"
    return f'''    <header class="page-hero" style="--hero-image:url('/assets/{img}')">
      <div class="hero-copy">{c}<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lead">{lead}</p></div>
    </header>'''

def head(label, h2, intro=None):
    i = f'<p class="section-intro">{intro}</p>' if intro else ""
    return f'<div class="section-head"><p class="section-label">{label}</p><div><h2>{h2}</h2>{i}</div></div>'

def faq_html(faqs, label="Sık sorulanlar", h2="Bize en çok sorulanlar."):
    items = "".join(f'<details class="faq-item"><summary><span>{q}</span><span class="faq-icon" aria-hidden="true"></span></summary><p>{a}</p></details>' for q, a in faqs)
    return f'''    <section class="section">
      {head(label, h2)}
      <div class="faq">{items}</div>
    </section>'''

def cta(h2, label="Arayın", sub=None):
    s = f'<p>{sub}</p>' if sub else ""
    return f'''    <section class="cta"><div><h2>{h2}</h2>{s}</div><a class="button" href="tel:{TEL}">{TEL_TXT} · {label} ↗</a></section>'''

def area_rows(exclude=None):
    rows = ""
    for i, (h, t, d) in enumerate(AREAS, 1):
        if h == exclude:
            continue
        rows += f'<a class="area-row" href="{h}"><span class="area-index">0{i}</span><span class="area-text"><strong>{t}</strong><span>{d}</span></span><span class="area-arrow" aria-hidden="true">↗</span></a>'
    return f'<div class="area-list">{rows}</div>'

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

# ---------------------------------------------------------------- Blog
import re as _re
BLOG_DATE = "2026-11-04"
POSTS = [
    # slug, md, kategori, alan linki, alan adı, görsel, görsel alt
    ("kira-artisi-ve-kira-tespit-davasi", "kira.md", "Kira", "/gayrimenkul-kira-miras", "Gayrimenkul, kira ve miras", "blog-kira", "Travertin bir rafın üzerinde pirinç ev anahtarları ve katlanmış boş bir kâğıt"),
    ("anlasmali-bosanma-rehberi", "bosanma.md", "Aile", "/aile-hukuku", "Boşanma ve aile hukuku", "blog-bosanma", "Ceviz bir masanın iki ucunda birbirinden uzak duran iki seramik fincan"),
    ("ifadeye-cagrildiniz", "ifade.md", "Ceza", "/ceza-hukuku", "Ceza hukuku", "blog-ifade", "Koyu bir masada dar bir ışık huzmesinin altında açılmamış bir zarf ve okuma gözlüğü"),
    ("isten-cikarildim-haklarim", "isten.md", "İş", "/is-icra-ticaret", "İş, icra ve ticaret hukuku", "blog-isten", "Kozanoğlu Hukuk Bürosu'nda boş bir görüşme odası"),
    ("odeme-emri-geldi", "odeme.md", "İcra", "/is-icra-ticaret", "İş, icra ve ticaret hukuku", "blog-odeme", "Ceviz masa üzerinde kâğıt ve kalem, görüşme masası"),
    ("miras-kalan-tasinmaz", "miras.md", "Miras", "/gayrimenkul-kira-miras", "Gayrimenkul, kira ve miras", "blog-miras", "Kozanoğlu Hukuk Bürosu binasının girişi"),
]

def _inline(t):
    t = e(t)
    t = _re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = _re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    return t

def _slugify(t):
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    t = t.translate(tr).lower()
    return _re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60]

def parse_md(path):
    lines = open(path, encoding="utf-8").read().strip().splitlines()
    title = summary = None; tldr = []; sections = []; faqs = []; cur = None; mode = None; q = None
    for raw in lines:
        l = raw.rstrip()
        if l.startswith("# ") and title is None:
            title = l[2:].strip(); continue
        if l.startswith("> ") and summary is None:
            summary = l[2:].strip(); continue
        if l.startswith("## "):
            h = l[3:].strip()
            if h.lower() == "kısaca": mode = "tldr"; continue
            if h.lower().startswith("sık sorulan"): mode = "faq"; continue
            mode = "body"; cur = {"h": h, "blocks": []}; sections.append(cur); continue
        if not l.strip():
            continue
        if mode == "tldr" and l.lstrip().startswith(("- ", "* ")):
            tldr.append(l.lstrip()[2:].strip()); continue
        if mode == "faq":
            m = _re.match(r"^\*\*(.+?)\*\*\s*(.*)$", l.strip())
            if m:
                q = m.group(1).strip(); faqs.append([q, m.group(2).strip()]); continue
            if faqs:
                faqs[-1][1] = (faqs[-1][1] + " " + l.strip()).strip()
            continue
        if mode == "body" and cur is not None:
            st = l.strip()
            if st.startswith("### "):
                cur["blocks"].append(("h3", st[4:]))
            elif st.startswith(("- ", "* ")) or _re.match(r"^\d+\.\s", st):
                item = _re.sub(r"^(- |\* |\d+\.\s)", "", st)
                kind = "ol" if _re.match(r"^\d+\.\s", st) else "ul"
                if cur["blocks"] and cur["blocks"][-1][0] == kind:
                    cur["blocks"][-1][1].append(item)
                else:
                    cur["blocks"].append((kind, [item]))
            else:
                cur["blocks"].append(("p", st))
    return title, summary, tldr, sections, faqs

def render_sections(sections):
    out = []
    for s in sections:
        sid = _slugify(s["h"])
        inner = ""
        for kind, val in s["blocks"]:
            if kind == "p": inner += f"<p>{_inline(val)}</p>"
            elif kind == "h3": inner += f"<h3>{_inline(val)}</h3>"
            else: inner += f"<{kind}>" + "".join(f"<li>{_inline(i)}</li>" for i in val) + f"</{kind}>"
        out.append((sid, s["h"], f'<section class="post-section" id="{sid}"><h2>{_inline(s["h"])}</h2>{inner}</section>'))
    return out

def words(sections, tldr, faqs):
    txt = " ".join(" ".join(v if isinstance(v, str) else " ".join(v) for _, v in s["blocks"]) for s in sections)
    txt += " ".join(tldr) + " ".join(a for _, a in faqs)
    return len(txt.split())

parsed = []
for slug, md, cat, alink, aname, img, alt in POSTS:
    title, summary, tldr, sections, faqs = parse_md(os.path.join(OUT, "content", "blog", md))
    parsed.append(dict(slug=slug, cat=cat, alink=alink, aname=aname, img=img, alt=alt, title=title, summary=summary, tldr=tldr, sections=sections, faqs=faqs, mins=max(3, round(words(sections, tldr, faqs) / 200))))

os.makedirs(os.path.join(OUT, "blog"), exist_ok=True)
for i, p in enumerate(parsed):
    path = "/blog/" + p["slug"]
    secs = render_sections(p["sections"])
    toc = "".join(f'<li><a href="#{sid}">{_inline(h)}</a></li>' for sid, h, _ in secs)
    tl = "".join(f"<li>{_inline(t)}</li>" for t in p["tldr"])
    faqs = [(q, a) for q, a in p["faqs"] if q and a]
    faq_items = "".join(f'<details class="faq-item"><summary><span>{_inline(q)}</span><span class="faq-icon" aria-hidden="true"></span></summary><p>{_inline(a)}</p></details>' for q, a in faqs)
    others = [o for o in parsed if o is not p][:0] + [parsed[(i + k) % len(parsed)] for k in (1, 2, 3)]
    rel = "".join(f'<a class="post-card" href="/blog/{o["slug"]}"><img src="/assets/blog/{o["img"]}-card.webp" width="800" height="450" loading="lazy" decoding="async" alt=""><span class="post-meta"><span>{o["cat"]}</span><span>{o["mins"]} dk.</span></span><h3>{_inline(o["title"])}</h3></a>' for o in others)
    body = f'''    <header class="post-hero">
      <div class="post-hero-copy"><nav class="crumbs" aria-label="Sayfa yolu"><a href="/">Ana sayfa</a><span aria-hidden="true">/</span><a href="/blog">Hukuk notları</a></nav><p class="eyebrow">{p["cat"]} · {p["mins"]} dk. okuma</p><h1>{_inline(p["title"])}</h1><p class="lead">{_inline(p["summary"])}</p></div>
      <figure class="post-hero-media"><img src="/assets/blog/{p["img"]}.webp" width="1376" height="768" fetchpriority="high" decoding="async" alt="{e(p["alt"])}"></figure>
    </header>
    <div class="post-layout">
      <aside class="post-aside"><div class="post-toc"><p class="section-label">Bu yazıda</p><ol>{toc}</ol></div><a class="post-area" href="{p["alink"]}"><span class="section-label">İlgili çalışma alanı</span><strong>{p["aname"]}</strong><span aria-hidden="true">↗</span></a></aside>
      <article class="post-body">
        <div class="tldr"><p class="section-label">Kısaca</p><ul>{tl}</ul></div>
        {"".join(h for _, _, h in secs)}
        <section class="post-section" id="sik-sorulan-sorular"><h2>Sık sorulan sorular</h2><div class="faq">{faq_items}</div></section>
        <p class="disclaimer">Bu yazı genel bilgilendirme amacıyla hazırlanmıştır ve hukuki görüş niteliğinde değildir. Mevzuat ve uygulama değişebilir; kendi durumunuz için bir avukatla görüşün. Son güncelleme: 4 Kasım 2026.</p>
      </article>
    </div>
    <section class="section alt">
      {head("Diğer yazılar", "Okumaya devam edin.")}
      <div class="blog-grid">{rel}</div>
    </section>
{cta("Bu yazı sizin durumunuza ne kadar uyuyor? Konuşalım.")}'''
    desc = p["summary"][:300]
    ttl = p["title"] + " | Kozanoğlu Hukuk"
    graph = [webpage(path, "WebPage", ttl, desc),
             {"@type": "BlogPosting", "@id": SITE + path + "#article", "headline": p["title"], "description": desc, "image": SITE + f"/assets/blog/{p['img']}.webp", "datePublished": BLOG_DATE, "dateModified": BLOG_DATE, "inLanguage": "tr-TR", "articleSection": p["cat"], "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "mainEntityOfPage": {"@id": SITE + path + "#webpage"}, "about": {"@id": SITE + p["alink"] + "#service"}},
             crumbs(("Hukuk Notları", "/blog"), (p["title"], path))]
    if faqs: graph.append(faq_ld(faqs))
    html_out = page(path, ttl, desc, f"blog/{p['img']}.webp", graph, body, og_img=f"/assets/blog/{p['img']}-og.jpg", og_type="article")
    write(os.path.join("blog", p["slug"] + ".html"), html_out)

# blog index
path = "/blog"
t = "Hukuk Notları: Kira, Boşanma, İcra, Miras | Kozanoğlu Hukuk"
d = "Kira artışı, anlaşmalı boşanma, ifadeye çağrılma, işten çıkarılma, ödeme emri ve miras kalan taşınmazlar hakkında süreleri ve adımları anlatan kapsamlı yazılar."
feat, rest = parsed[0], parsed[1:]
cards = "".join(f'<a class="post-card" href="/blog/{o["slug"]}"><img src="/assets/blog/{o["img"]}-card.webp" width="800" height="450" loading="lazy" decoding="async" alt="{e(o["alt"])}"><span class="post-meta"><span>{o["cat"]}</span><span>{o["mins"]} dk.</span></span><h2>{_inline(o["title"])}</h2><p>{_inline(o["summary"])}</p><span class="read">Yazıyı okuyun ↗</span></a>' for o in rest)
body = "\n".join([
    hero("interior-logo.webp", "Hukuk notları", "Süreler, adımlar, sık yapılan hatalar.", "Bize en çok sorulan konuları uzun ve anlaşılır yazılarla anlattık. Her yazıda kaçırılmaması gereken süreler ve sık sorulan sorular var."),
    f'''    <section class="section">
      <a class="post-feature" href="/blog/{feat["slug"]}"><img src="/assets/blog/{feat["img"]}.webp" width="1376" height="768" loading="lazy" decoding="async" alt="{e(feat["alt"])}"><div><span class="post-meta"><span>{feat["cat"]}</span><span>{feat["mins"]} dk.</span></span><h2>{_inline(feat["title"])}</h2><p>{_inline(feat["summary"])}</p><span class="read">Yazıyı okuyun ↗</span></div></a>
      <div class="blog-grid">{cards}</div>
    </section>''',
    cta("Genel bilgi yetmediğinde, konuyu birlikte ele alalım."),
])
blog_graph = [webpage(path, "CollectionPage", t, d), crumbs(("Hukuk Notları", path)),
              {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/blog/" + o["slug"], "name": o["title"]} for i, o in enumerate(parsed)]}]
write("blog.html", page(path, t, d, "interior-logo.webp", blog_graph, body))
BLOG_SLUGS = [o["slug"] for o in parsed]


def related_posts(area_path):
    rel = [o for o in parsed if o["alink"] == area_path]
    if not rel: return ""
    cards = "".join(f'<a class="post-card" href="/blog/{o["slug"]}"><img src="/assets/blog/{o["img"]}-card.webp" width="800" height="450" loading="lazy" decoding="async" alt=""><span class="post-meta"><span>{o["cat"]}</span><span>{o["mins"]} dk.</span></span><h3>{_inline(o["title"])}</h3><p>{_inline(o["summary"])}</p><span class="read">Yazıyı okuyun ↗</span></a>' for o in rel)
    return f'''    <section class="section">
      {head("Hukuk notları", "Bu konuda yazdıklarımız.")}
      <div class="blog-grid">{cards}</div>
    </section>'''

# ---------------------------------------------------------------- Area pages
def area_page(slug, img, title, desc, eyebrow, h1, lead, topics_h2, topics_intro, topics, notes_h2, notes, faqs, local, cta_h2, service):
    path = "/" + slug
    topic_html = "".join(f'<li><strong>{t}</strong><span>{d}</span></li>' for t, d in topics)
    notes_html = "".join(f'<h3>{t}</h3><p>{p}</p>' for t, p in notes)
    body = "\n".join([
        hero(img, eyebrow, h1, lead, crumb=[("/calisma-alanlari", "Çalışma alanları")]),
        f'''    <section class="section">
      {head("Neler yapıyoruz", topics_h2, topics_intro)}
      <ul class="topic-grid">{topic_html}</ul>
    </section>''',
        f'''    <section class="section alt article-section"><div><p class="section-label">Bilmeniz gerekenler</p><h2>{notes_h2}</h2></div><div class="article-body">{notes_html}<p class="disclaimer">Süreler ve kurallar mevzuat değişikliğiyle güncellenebilir. Kendi durumunuz için bizimle görüşün.</p></div></section>''',
        f'''    <section class="section local-note"><div class="local-grid"><p class="section-label">Pratikte</p><div><p class="local-lead">{local}</p><a class="text-link" href="/kepez-varsak-avukat">Kepez ve Varsak sayfası ↗</a></div></div></section>''',
        faq_html(faqs),
        related_posts(path),
        f'''    <section class="section alt">
      {head("Diğer alanlar", "Başka bir konu mu?")}
      {area_rows(exclude=path)}
    </section>''',
        cta(cta_h2),
    ])
    graph = [webpage(path, "WebPage", title, desc),
             {"@type": "Service", "@id": SITE + path + "#service", "serviceType": service, "name": h1.rstrip("."), "provider": {"@id": ORG_ID}, "areaServed": [{"@type": "AdministrativeArea", "name": "Kepez"}, {"@type": "City", "name": "Antalya"}], "url": SITE + path},
             crumbs(("Çalışma Alanları", "/calisma-alanlari"), (h1.rstrip("."), path)), faq_ld(faqs)]
    write(slug + ".html", page(path, title, desc, img, graph, body))

area_page(
    "aile-hukuku", "meeting-room.webp",
    "Kepez Boşanma Avukatı, Aile Hukuku | Kozanoğlu Hukuk Antalya",
    "Kepez'de boşanma ve aile hukuku: anlaşmalı ve çekişmeli boşanma, velayet, nafaka, mal paylaşımı ve koruma kararları. Antalya Aile Mahkemeleri'ndeki davalar için (0242) 244 54 20.",
    "Çalışma alanı · Aile hukuku", "Boşanma ve aile hukuku.",
    "Anlaşmalı ya da çekişmeli boşanma, velayet, nafaka ve mal paylaşımı. Zor bir dönemde, işin hukuki tarafını sakin ve düzenli yürütürüz.",
    "Aile dosyalarında üstlendiğimiz işler.",
    "Boşanma çoğu zaman tek bir dava değildir. Velayet, nafaka ve mal paylaşımı ayrı ayrı konuşulur, bazen yıllarca sürer. Hangisinin önce ele alınacağını birlikte belirleriz.",
    [("Anlaşmalı boşanma", "Protokolün hazırlanması ve duruşmaya birlikte girilmesi."),
     ("Çekişmeli boşanma", "Dava dilekçesi, delillerin toplanması, tanık ve duruşma takibi."),
     ("Velayet ve kişisel ilişki", "Velayetin belirlenmesi, değiştirilmesi ve çocukla görüşme düzeni."),
     ("Nafaka", "Tedbir, iştirak ve yoksulluk nafakası; artırım ve azaltım davaları."),
     ("Mal paylaşımı", "Edinilmiş mallara katılma, ev ve araç gibi malların tasfiyesi."),
     ("Koruma kararları", "6284 sayılı Kanun kapsamında uzaklaştırma ve koruma tedbirleri.")],
    "Dava açmadan önce bilinmesi iyi olanlar.",
    [("Anlaşmalı boşanmanın iki şartı var", "Evliliğin en az bir yıl sürmüş olması ve iki eşin de duruşmaya bizzat gelmesi gerekir. Velayet, nafaka ve mal paylaşımı protokolde açıkça yazılmazsa, boşanmadan sonra yeni bir davanın kapısı açık kalır."),
     ("Çekişmeli davada her iddia ispat ister", "Mesaj kayıtları, banka hareketleri, tanıklar ve sağlık raporları önemlidir. Delilleri dava açılmadan önce bir araya getirmek, dava sırasında aramaktan çok daha kolaydır."),
     ("Şiddet varsa boşanmayı beklemeyin", "Şiddet ya da tehdit söz konusuysa koruma ve uzaklaştırma kararı, boşanma davasından bağımsız olarak hemen istenebilir."),
     ("Mal paylaşımının süresi sınırsız değil", "Mal rejiminin tasfiyesi için dava, boşanma kararının kesinleşmesinden sonra on yıl içinde açılmalıdır.")],
    [("Anlaşmalı boşanma ne kadar sürer?", "Protokol hazırsa ve mahkemenin takvimi uygunsa karar genellikle ilk duruşmada verilir. Kararın kesinleşmesi için ayrıca tebliğ ve itiraz sürelerinin dolması gerekir."),
     ("Kepez'de oturuyorum, boşanma davası nerede açılır?", "Dava, eşlerden birinin yerleşim yerinde ya da davadan önce son altı ay birlikte oturduğunuz yerde açılabilir. Kepez'de oturuyorsanız dava Antalya Aile Mahkemeleri'nde görülür."),
     ("Velayet kararı sonradan değiştirilebilir mi?", "Evet. Koşullar değiştiğinde ve çocuğun yararı bunu gerektirdiğinde velayetin değiştirilmesi istenebilir."),
     ("Eşim anlaşmaya yanaşmazsa ne olur?", "Çekişmeli boşanma davası açılır. Dava sürerken taraflar anlaşırsa, dava anlaşmalı boşanmaya dönüştürülebilir.")],
    "Protokolü ve ön görüşmeleri ofiste birlikte hazırlarız. Duruşmalar Antalya Adliyesi'nde yapılır; anlaşmalı boşanma dışında çoğuna sizin yerinize biz gireriz.",
    "Boşanmayı düşünüyorsanız, önce konuşalım.", "Aile hukuku")

area_page(
    "ceza-hukuku", "rear-entrance.webp",
    "Kepez Ceza Avukatı, Ceza Hukuku | Kozanoğlu Hukuk Antalya",
    "Kepez'de ceza hukuku: karakol ve savcılık ifadesi, gözaltı, tutukluluk, asliye ve ağır ceza davaları, mağdur vekilliği. Antalya Adliyesi'ndeki dosyalar için (0242) 244 54 20.",
    "Çalışma alanı · Ceza hukuku", "Ceza hukuku.",
    "İfadeden duruşmaya kadar. Şüpheli ve sanık müdafiliğinin yanında, suçtan zarar gören taraf olarak dosyası olanları da temsil ediyoruz.",
    "Ceza dosyalarında yanınızda olduğumuz aşamalar.",
    "Ceza dosyasında en kritik an çoğu zaman ilk ifadedir. Orada söylenen her cümle dosyaya girer ve sonraki her aşamada karşınıza çıkar.",
    [("İfade ve sorgu", "Karakolda, savcılıkta ve sulh ceza hakimliğinde ifade sırasında hazır bulunmak."),
     ("Gözaltı ve tutukluluk", "Gözaltı süresine, tutuklama ve adli kontrol kararlarına itiraz."),
     ("Asliye ve ağır ceza davaları", "Savunmanın hazırlanması, delil ve tanık takibi, duruşmalar."),
     ("Mağdur ve müşteki vekilliği", "Şikâyet dilekçesi, soruşturmanın takibi ve davaya katılma."),
     ("Trafik ve iş kazası dosyaları", "Taksirle yaralama ve öldürme dosyalarında hem ceza hem tazminat tarafı."),
     ("Kanun yolları", "Kararlara itiraz, istinaf ve temyiz başvuruları.")],
    "İfadeye gitmeden önce bilmeniz gerekenler.",
    [("Avukatla gitme hakkınız var", "Şüpheli olarak ifadeye çağrıldıysanız, ifade sırasında avukatınızın yanınızda bulunmasını isteyebilirsiniz. Ayrıca susma hakkınız vardır ve susmanız aleyhinize yorumlanamaz."),
     ("Bazı durumlarda avukat zorunludur", "Alt sınırı beş yıldan fazla hapis cezası öngörülen suçlarda ve şüpheli ya da sanık çocuksa müdafi atanması zorunludur. Kendi avukatınız yoksa baro tarafından görevlendirilir."),
     ("Şikâyet süresi altı ay", "Şikâyete bağlı suçlarda şikâyet, failin ve fiilin öğrenilmesinden itibaren altı ay içinde yapılmalıdır. Bu süre geçerse soruşturma başlatılamaz."),
     ("Tutanağı okumadan imzalamayın", "İfade tutanağında söylediklerinizin doğru yazıldığını kontrol edin. Eksik ya da yanlış bir ifade varsa imzalamadan önce düzeltilmesini isteyin.")],
    [("Avukatsız ifade verirsem ne olur?", "İfade geçerlidir ve dosyaya girer. Sonradan ‘yanlış anlaşıldım’ demek kolay değildir. Bu yüzden ifade öncesinde bir avukatla konuşmak çoğu zaman sonucu etkiler."),
     ("Kepez'deki bir olay hangi adliyeye gider?", "Kepez'de yaşanan olaylarla ilgili soruşturmaları Antalya Cumhuriyet Başsavcılığı yürütür. Davalar Meltem'deki Antalya Adliyesi'nde bulunan ceza mahkemelerinde görülür."),
     ("Yakınım gözaltına alındı, ne yapmalıyım?", "Önce hangi emniyet biriminde ya da jandarma karakolunda tutulduğunu öğrenin. Gözaltındaki kişinin avukatla görüşme hakkı vardır; bir avukata ulaşmak ilk adımdır."),
     ("Hakkımda şikâyet olduğunu nasıl öğrenirim?", "Çoğu zaman ifadeye çağrı kâğıdı ya da telefonla öğrenirsiniz. Çağrıyı aldığınızda ne sıfatla, yani şüpheli mi tanık mı çağrıldığınızı sorun.")],
    "İfade çoğu zaman olayın yaşandığı yerdeki emniyet ya da jandarma biriminde alınır, dosya sonra adliyeye gider. İfade tarihiniz belliyse, o günden önce bir kez konuşmamız çoğu zaman yeterlidir.",
    "İfade tarihiniz belli mi? Önce bizi arayın.", "Ceza hukuku")

area_page(
    "gayrimenkul-kira-miras", "hero-poster.webp",
    "Kepez Kira, Tapu ve Miras Avukatı | Kozanoğlu Hukuk Antalya",
    "Kepez ve Varsak'ta kira artışı, tahliye, tapu iptali, ortaklığın giderilmesi, kat mülkiyeti ve miras paylaşımı davaları. Kozanoğlu Hukuk Bürosu, Emek Mah. Kepez. (0242) 244 54 20.",
    "Çalışma alanı · Gayrimenkul, kira, miras", "Gayrimenkul, kira ve miras.",
    "Kira artışı ve tahliye, tapu, hisseli taşınmazlar, site yönetimi ve miras paylaşımı. Çoğunda karşı taraf tanıdık biri: ev sahibi, kiracı, komşu ya da kardeş.",
    "Taşınmaz ve miras dosyalarında yaptıklarımız.",
    "Bu yüzden önce anlaşma yolunu deneriz, olmazsa davayı açarız. Çoğu dosyada arabuluculuk zaten zorunlu bir ilk adım.",
    [("Kira artışı ve kira tespiti", "Yasal sınırlar içinde artış, beş yılı dolan sözleşmelerde kira bedelinin belirlenmesi."),
     ("Tahliye", "İhtiyaç, temerrüt ve tahliye taahhüdüne dayalı tahliye davaları ve takipleri."),
     ("Tapu iptal ve tescil", "Muvazaa, vekalet kötüye kullanımı ve hatalı tescil davaları."),
     ("Ortaklığın giderilmesi", "Hisseli taşınmazların aynen bölünmesi ya da satış yoluyla paylaştırılması."),
     ("Kat mülkiyeti ve site yönetimi", "Aidat, ortak alan, yönetim planı ve komşuluk uyuşmazlıkları."),
     ("Miras", "Veraset ilamı, mirasın reddi, tenkis ve muris muvazaası davaları.")],
    "Dava açmadan önce bilmeniz gerekenler.",
    [("Kira davalarında önce arabulucu", "1 Eylül 2023'ten bu yana kira ilişkisinden doğan uyuşmazlıklarda dava açmadan önce arabulucuya başvurmak zorunludur. Aynı kural ortaklığın giderilmesi ve kat mülkiyeti uyuşmazlıkları için de geçerlidir."),
     ("Konut kirasında artışın sınırı", "Konut kiralarında yıllık artış, bir önceki kira yılının on iki aylık TÜFE ortalamasını geçemez. Beş yılı dolduran sözleşmelerde ise kira bedeli mahkemece emsallere göre yeniden belirlenebilir."),
     ("İhtiyaç nedeniyle tahliyede süre", "Belirli süreli sözleşmede ihtiyaç nedeniyle tahliye davası, sözleşme süresinin bitiminden itibaren bir ay içinde açılmalıdır. Bu süre kaçarsa dava bir sonraki dönemi bekler."),
     ("Mirası reddetmenin süresi üç ay", "Borçlu bir miras söz konusuysa, mirası reddetmek için ölümü öğrendiğiniz tarihten itibaren üç ay süreniz vardır. Bu süre sulh hukuk mahkemesine başvurarak kullanılır.")],
    [("Ev sahibim kirayı yasal sınırın üzerinde artırmak istiyor.", "Konut kiralarında on iki aylık TÜFE ortalamasının üzerindeki artışı kabul etmek zorunda değilsiniz. Ancak sözleşmeniz beş yılı doldurduysa ev sahibi kira tespit davası açabilir."),
     ("Miras kalan evi kardeşlerle paylaşamıyoruz.", "Anlaşma olmazsa ortaklığın giderilmesi yoluna gidilir. Önce arabulucuya başvurulur; anlaşma çıkmazsa sulh hukuk mahkemesi taşınmazın bölünmesine ya da satışına karar verir."),
     ("Sitede aidat ödemeyen bir komşu için ne yapılabilir?", "Yönetim, ödenmeyen aidatlar için icra takibi başlatabilir. Kat mülkiyetinden doğan uyuşmazlıklarda dava açılacaksa önce arabulucuya gidilir."),
     ("Tapusu olmayan bir hisse için ne yapabilirim?", "Önce tapu kayıtları ve veraset durumu incelenir. Eski kayıtlarda isim ya da pay hataları sık görülür; çoğu zaman düzeltme ya da tescil davasıyla çözülür.")],
    "Varsak 2008'e kadar ayrı bir belediyeydi. Bu yüzden bölgede eski tarihli tapu kayıtları, hisseli tarlalar ve imar değişikliğinden etkilenen parseller sık görülür. Yeni sitelerle birlikte aidat, ortak alan ve kat karşılığı inşaat sözleşmesi uyuşmazlıkları da arttı.",
    "Kira, tapu ya da miras: önce belgelere bakalım.", "Gayrimenkul, kira ve miras hukuku")

area_page(
    "is-icra-ticaret", "interior-logo.webp",
    "Kepez İş, İcra ve Ticaret Avukatı | Kozanoğlu Hukuk Antalya",
    "Kepez'de iş, icra ve ticaret hukuku: kıdem ve ihbar tazminatı, işe iade, iş kazası, icra takibi, ödeme emrine itiraz, alacak ve sözleşme işleri. (0242) 244 54 20.",
    "Çalışma alanı · İş, icra, ticaret", "İş, icra ve ticaret hukuku.",
    "İşçi ve işveren uyuşmazlıkları, icra takipleri, alacak davaları ve işletmelerin günlük sözleşme işleri.",
    "Bu alanda üstlendiğimiz işler.",
    "Bu dosyalarda süreler kısadır. Bir tebligatı ya da fesih bildirimini birkaç gün bekletmek, hakkı tamamen kaybettirebilir.",
    [("İşçi alacakları", "Kıdem ve ihbar tazminatı, fazla mesai, yıllık izin ve ücret alacakları."),
     ("İşe iade", "Geçersiz fesih nedeniyle arabuluculuk ve işe iade davaları."),
     ("İş kazası", "İş kazası ve meslek hastalığından doğan maddi ve manevi tazminat."),
     ("İcra takibi", "İlamlı, ilamsız ve kambiyo senetlerine dayalı takipler, haciz işlemleri."),
     ("Takibe itiraz", "Ödeme emrine itiraz, borca ve imzaya itiraz, menfi tespit davaları."),
     ("Ticari işler", "Sözleşme hazırlığı ve incelemesi, ticari alacak davaları, şirket işleri.")],
    "Kaçırılmaması gereken süreler.",
    [("İşe iade için bir ay", "İş sözleşmeniz feshedildiyse, işe iade için fesih bildiriminden itibaren bir ay içinde arabulucuya başvurmanız gerekir. Arabuluculukta anlaşma olmazsa iki hafta içinde dava açılır."),
     ("İşçi alacaklarında önce arabulucu", "Kıdem, ihbar, fazla mesai gibi alacaklar için dava açmadan önce arabulucuya başvurmak zorunludur. Ticari para alacaklarında da aynı kural uygulanır."),
     ("Ödeme emrine itiraz için yedi gün", "Size bir ödeme emri geldiyse, tebliğden itibaren yedi gün içinde itiraz edebilirsiniz. Çek ve senede dayalı takiplerde bu süre beş gündür. Süre geçerse takip kesinleşir."),
     ("Kıdem tazminatı için bir yıl", "Kıdem tazminatı için aynı işverende en az bir yıl çalışmış olmak ve iş sözleşmesinin kanunda sayılan bir sebeple sona ermiş olması gerekir.")],
    [("Alacağım için icra takibi mi açmalıyım, dava mı?", "Elinizde fatura, imzalı belge ya da çek varsa çoğu zaman icra takibiyle başlanır. Borçlu itiraz ederse itirazın iptali davası ve öncesinde arabuluculuk gündeme gelir."),
     ("İşten çıkarıldım ama bana sebep söylenmedi.", "Otuz ya da daha fazla işçi çalışan bir işyerinde en az altı aylık kıdeminiz varsa, işveren feshi geçerli bir sebebe dayandırmak zorundadır. Bu durumda işe iade yolu açık olabilir."),
     ("Bana gelen ödeme emrindeki borcu tanımıyorum.", "Süresi içinde borca itiraz edin. İtiraz edilmeyen takip kesinleşir ve haciz aşamasına geçilir."),
     ("İşletmem için sözleşme incelemesi yapıyor musunuz?", "Evet. Kira, satış, hizmet ve bayilik sözleşmelerini imzadan önce inceler, riskli maddeleri işaretleriz.")],
    "Takip, itiraz ve dava işlemlerinin çoğunu UYAP üzerinden yürütürüz. Çoğu adım için adliyeye gitmeniz gerekmez; size düşen, tebligatı aldığınız gün bizi aramak.",
    "Bir tebligat mı geldi? Süre dolmadan arayın.", "İş, icra ve ticaret hukuku")

# ---------------------------------------------------------------- Çalışma alanları hub
path = "/calisma-alanlari"
t = "Çalışma Alanları | Kozanoğlu Hukuk Bürosu Kepez, Antalya"
d = "Kozanoğlu Hukuk Bürosu'nun Kepez'den yürüttüğü çalışma alanları: boşanma ve aile, ceza, gayrimenkul, kira, miras, iş, icra ve ticaret hukuku."
body = "\n".join([
    hero("footer-table.webp", "Çalışma alanları", "Hangi dosyalara bakıyoruz?", "Aile, ceza, gayrimenkul, kira, miras, iş, icra ve ticaret. Danışmanlık veriyor, dava ve takipleri yürütüyoruz. Konunuz hangi başlığa giriyor bilmiyorsanız, sorun."),
    f'''    <section class="section">
      {head("Dört başlık", "Konunuz hangisine yakın?", "Her başlığın kendi sayfasında sık sorulan sorular ve kaçırılmaması gereken süreler var. Emin değilseniz arayın, konunun hangi alana girdiğini telefonda söyleriz.")}
      {area_rows()}
    </section>''',
    f'''    <section class="section alt">
      {head("Ortak nokta", "Her dosyada aynı ilk adım.")}
      <div class="steps"><article class="step"><span>01 · Dinlemek</span><h3>Olayı baştan anlatın</h3><p>Ne oldu, ne zaman oldu, kimler var. Kesin tarih bilmiyorsanız yaklaşık dönem de yeter.</p></article><article class="step"><span>02 · Belge</span><h3>Elinizdekileri getirin</h3><p>Tebligat, sözleşme, tapu, mesaj kayıtları. Önemsiz görünen bir kâğıt bazen dosyanın yönünü değiştirir.</p></article><article class="step"><span>03 · Yol</span><h3>Seçenekleri konuşalım</h3><p>Dava, arabuluculuk, ihtarname ya da beklemek. Her birinin süresini ve masrafını açıkça söyleriz.</p></article></div>
    </section>''',
    cta("Konunuz hangi alana giriyor, telefonda söyleyelim."),
])
write("calisma-alanlari.html", page(path, t, d, "footer-table.webp",
      [webpage(path, "CollectionPage", t, d), crumbs(("Çalışma Alanları", path)),
       {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + h, "name": n} for i, (h, n, _) in enumerate(AREAS)]}], body))

# ---------------------------------------------------------------- Kepez / Varsak
path = "/kepez-varsak-avukat"
t = "Kepez ve Varsak Avukat | Kozanoğlu Hukuk Bürosu, Emek Mah."
d = "Kepez Emek Mahallesi'nde hukuk bürosu. Varsak Karşıyaka, Varsak Esentepe, Varsak Menderes ve Kepez'in diğer mahallelerinden gelen aile, ceza, kira, tapu, miras, iş ve icra dosyaları."
faqs = [
    ("Ofise gelmeden dosyamı size verebilir miyim?", "İlk değerlendirmeyi telefonda başlatabiliriz. Dosyayı üstlenmemiz için herhangi bir noterden avukat adına vekaletname çıkarmanız yeterlidir; bunun için ofise gelmeniz şart değildir."),
    ("Kepez'deki davalar hangi adliyede görülür?", "Kepez ve Varsak'ı ilgilendiren davaların ve icra işlemlerinin büyük bölümü Muratpaşa Meltem'deki Antalya Adliyesi'nde yürür."),
    ("Duruşmalara benim de gitmem gerekir mi?", "Çoğu duruşmaya vekil olarak biz gireriz. Anlaşmalı boşanma gibi kanunun bizzat katılımı aradığı durumlarda size önceden haber veririz."),
    ("Görüşme için randevu gerekiyor mu?", "Evet. Gelmeden önce (0242) 244 54 20 numarasını arayın, görüşme için uygun bir saat belirleyelim."),
]
hoods = ["Emek", "Varsak Karşıyaka", "Varsak Esentepe", "Varsak Menderes", "Altıayak", "Teomanpaşa", "Fabrikalar", "Odabaşı", "Kepez'in diğer mahalleleri"]
hood_html = "".join(f"<li>{h}</li>" for h in hoods)
body = "\n".join([
    hero("mobile-hero.webp", "Bölge rehberi", "Kepez ve Varsak: büro, adliye, mahalleler.", "Dosyanızın nerede görüleceği, bu bölgede hangi konuların sık çıktığı ve bize nasıl ulaşacağınız. Kısa ve pratik."),
    f'''    <section class="section">
      <div class="section-head"><p class="section-label">Büro ve adliye</p><div><h2>Duruşmaya biz gideriz.</h2><p class="section-intro">Kepez ve Varsak'ı ilgilendiren davaların ve icra takiplerinin büyük bölümü Muratpaşa Meltem'deki Antalya Adliyesi'nde yürür. Duruşmalara, dosya incelemesine ve icra işlemlerine biz gideriz. Dosyadaki her hareketi UYAP üzerinden takip eder, size bildiririz.</p></div></div>
      <div class="split-facts"><div><span>Ofis</span><strong>Emek Mah. Yeşilırmak Cd. No:19/2, 07030 Kepez / Antalya</strong><a class="text-link" href="{MAP}" target="_blank" rel="noopener noreferrer">Google Haritalar'da açın ↗</a></div><div><span>Adliye</span><strong>Antalya Adliyesi, Meltem Mah. Dumlupınar Blv., Muratpaşa</strong><p>Kepez'deki hukuk, ceza ve icra dosyalarının görüldüğü yer.</p></div><div><span>Telefon</span><strong>{TEL_TXT}</strong><a class="text-link" href="tel:{TEL}">Arayın ↗</a></div></div>
    </section>''',
    f'''    <section class="section alt">
      {head("Sık çıkan konular", "Üç konu, defalarca.", "Yeni siteler, eski tapular, kiracı ile ev sahibi. Buradan gelen dosyaların çoğu bu üçünden birine dokunuyor.")}
      <div class="cards"><article class="card"><span class="number">01</span><h3>Kira ve tahliye</h3><p>Kira artışı, kira tespiti ve tahliye. Dava açmadan önce zorunlu arabuluculuk aşaması. <a class="inline-link" href="/gayrimenkul-kira-miras">Ayrıntılar</a></p></article><article class="card"><span class="number">02</span><h3>Hisseli tapular</h3><p>Varsak 2008'e kadar ayrı bir belediyeydi. Eski tapu kayıtları, miras kalan hisseli tarlalar ve imar değişiklikleri bu yüzden sık gündeme gelir. <a class="inline-link" href="/gayrimenkul-kira-miras">Ayrıntılar</a></p></article><article class="card"><span class="number">03</span><h3>Site ve kat mülkiyeti</h3><p>Yeni sitelerde aidat, ortak alan kullanımı ve kat karşılığı inşaat sözleşmelerinden doğan uyuşmazlıklar. <a class="inline-link" href="/gayrimenkul-kira-miras">Ayrıntılar</a></p></article></div>
    </section>''',
    f'''    <section class="section">
      {head("Mahalleler", "Dosyalar en çok buradan geliyor.", "Antalya'nın diğer ilçelerindeki dosyaları da üstleniyoruz.")}
      <ul class="hood-list">{hood_html}</ul>
    </section>''',
    f'''    <section class="section alt">
      {head("Çalışma alanları", "Konuya göre sayfalar.")}
      {area_rows()}
    </section>''',
    faq_html(faqs),
    cta("Önce arayın, sonra gelin.", sub="Randevuyla, sizi bekletmeden görüşelim."),
])
write("kepez-varsak-avukat.html", page(path, t, d, "mobile-hero.webp",
      [webpage(path, "WebPage", t, d), crumbs(("Kepez ve Varsak", path)), faq_ld(faqs)], body))

# ---------------------------------------------------------------- Hakkımızda
path = "/hakkimizda"
t = "Hakkımızda | Kozanoğlu Hukuk Bürosu, Kepez Antalya"
d = "Kepez Emek Mahallesi'ndeki ofisimizde Av. Osman Kozanoğlu, Av. Hüseyin Kozanoğlu, Av. Beyza Kozanoğlu ve Stj. Av. Abdullah Kozanoğlu çalışıyor. Nasıl çalıştığımızı anlattık."
body = "\n".join([
    hero("rear-entrance.webp", "Hakkımızda", "Dosyanızı kimin takip ettiğini bilirsiniz.", "Kozanoğlu Hukuk Bürosu'nda üç avukat ve bir stajyer avukat çalışıyor. Aile, ceza, gayrimenkul, kira, miras, iş ve icra dosyalarına bakıyoruz."),
    f'''    <section class="section">
      {head("Nasıl çalışırız", "Önce dinleriz, sonra konuşuruz.", "Hukuki bir sorunla gelen çoğu kişi neyi soracağını bilmez. Bu çok normal. İlk görüşmede olayı sizden dinler, gereken belgeleri ve tarihleri birlikte çıkarırız.")}
      <div class="story-grid"><img src="/assets/meeting-room.webp" width="1440" height="804" loading="lazy" decoding="async" alt="Kozanoğlu Hukuk Bürosu görüşme odası, Kepez"><div class="story-copy"><p class="quote">Ne yapılabileceğini de, ne yapılamayacağını da açıkça söyleriz.</p><p>Her dosya davayla bitmez. Bazı konular bir ihtarnameyle, bazıları arabuluculuk masasında çözülür. Hangi yolun daha az masraflı, hangisinin daha uzun süreceğini görüşmede konuşuruz.</p><p>Dosya açıldıktan sonra duruşma tarihlerini, bilirkişi raporlarını ve karşı tarafın dilekçelerini size biz iletiriz. Bir gelişmeyi öğrenmek için peşimizden koşmanız gerekmez.</p></div></div>
    </section>''',
    f'''    <section class="section alt">
      {head("Alışkanlıklar", "Büroda değişmeyen üç şey.")}
      <div class="cards"><article class="card"><span class="number">01</span><h3>Sade dil</h3><p>Dilekçede ne yazdığını, kararın ne anlama geldiğini hukuk terimlerine boğmadan anlatırız.</p></article><article class="card"><span class="number">02</span><h3>Gerçekçi beklenti</h3><p>Sonuç vaadi vermeyiz. Riskleri, olası süreleri ve masrafları baştan konuşuruz.</p></article><article class="card"><span class="number">03</span><h3>Düzenli haber</h3><p>Duruşma, rapor, tebligat. Dosyanızdaki gelişmeleri gecikmeden size iletiriz.</p></article></div>
    </section>''',
    f'''    <section class="section">
      {head("Ekip", "Aynı masada dört kişi.", "Telefonu açan da, duruşmaya giren de bu ekipten biri.")}
      <div class="people" aria-label="Kozanoğlu Hukuk Bürosu ekibi"><article class="person"><span class="initials">OK</span><h3>Osman Kozanoğlu</h3><p>Avukat</p></article><article class="person"><span class="initials">HK</span><h3>Hüseyin Kozanoğlu</h3><p>Avukat</p></article><article class="person"><span class="initials">BK</span><h3>Beyza Kozanoğlu</h3><p>Avukat</p></article><article class="person"><span class="initials">AK</span><h3>Abdullah Kozanoğlu</h3><p>Stajyer Avukat</p></article></div>
    </section>''',
    f'''    <section class="section alt">
      {head("İlk görüşme", "İlk görüşme nasıl geçer?")}
      <div class="steps"><article class="step"><span>01 · Telefon</span><h3>Arayın</h3><p>Konuyu bir iki cümleyle anlatmanız yeterli. Görüşme için ofiste bir saat belirleriz.</p></article><article class="step"><span>02 · Belgeler</span><h3>Elinizdekini getirin</h3><p>Sözleşme, tebligat, mesaj kayıtları, tapu ya da nüfus kaydı. Hepsi işe yarar.</p></article><article class="step"><span>03 · Yol</span><h3>Seçenekleri konuşalım</h3><p>Dava, arabuluculuk, ihtarname ya da beklemek. Süreleri ve masrafları birlikte değerlendiririz.</p></article></div>
    </section>''',
    f'''    <section class="section">
      {head("Konum", "Ofise nasıl gelinir?", "Adresimiz aşağıda. Gelmeden önce arayın, sizi kapıda bekletmeyelim.")}
      <div class="location-block"><img src="/assets/rear-entrance.webp" width="1440" height="804" loading="lazy" decoding="async" alt="Kozanoğlu Hukuk Bürosu girişi, Yeşilırmak Caddesi Kepez"><div class="location-copy"><div><p class="section-label">Kozanoğlu Hukuk Bürosu</p><h3>Randevuyla görüşürüz.</h3><address>Emek Mah. Yeşilırmak Cd. No:19/2<br>07030 Kepez / Antalya</address></div><a class="location-link" href="{MAP}" target="_blank" rel="noopener noreferrer"><span>Yol tarifi alın</span><span aria-hidden="true">↗</span></a></div></div>
    </section>''',
    cta("Konuyu telefonda anlatın, gerisini birlikte planlayalım."),
])
write("hakkimizda.html", page(path, t, d, "rear-entrance.webp", [webpage(path, "AboutPage", t, d), crumbs(("Hakkımızda", path))], body))

# ---------------------------------------------------------------- İletişim
path = "/iletisim"
t = "İletişim ve Yol Tarifi | Kozanoğlu Hukuk Bürosu Kepez, Antalya"
d = "Kozanoğlu Hukuk Bürosu: Emek Mah. Yeşilırmak Cd. No:19/2, 07030 Kepez / Antalya. Telefon (0242) 244 54 20. Görüşme için arayın, ofiste bir saat belirleyelim."
body = "\n".join([
    hero("meeting-room.webp", "İletişim", "Arayın, bir saat belirleyelim.", f"{TEL_TXT} numaralı telefondan bize ulaşabilirsiniz. Ofisimiz Kepez Emek Mahallesi'nde, Yeşilırmak Caddesi No:19/2'de."),
    f'''    <section class="section">
      <div class="contact-layout"><div><p class="section-label">İlk görüşme</p><h2>Doğrudan ulaşın.</h2><p class="section-intro">Aradığınızda adınızı ve konuyu bir iki cümleyle söylemeniz yeterli. Görüşmeye gelirken elinizdeki belgeleri yanınıza alın.</p></div><div class="contact-panel contact-card"><div class="contact-panel-head"><p class="section-label">İletişim bilgileri</p><p>Telefon ve adres.</p></div><div class="contact-list"><div class="contact-item"><span class="contact-index">01</span><div class="contact-value"><span>Telefon</span><strong>{TEL_TXT}</strong></div><a class="contact-action" href="tel:{TEL}"><span>Arayın</span><span aria-hidden="true">↗</span></a></div><div class="contact-item"><span class="contact-index">02</span><div class="contact-value"><span>Adres</span><strong>Emek Mah. Yeşilırmak Cd. No:19/2, 07030 Kepez / Antalya</strong></div><a class="contact-action" href="{MAP}" target="_blank" rel="noopener noreferrer"><span>Yol tarifi</span><span aria-hidden="true">↗</span></a></div><div class="contact-item"><span class="contact-index">03</span><div class="contact-value"><span>Görüşme</span><strong>Ofiste, randevuyla</strong></div><a class="contact-action" href="/kepez-varsak-avukat"><span>Bölge</span><span aria-hidden="true">↗</span></a></div></div><p class="contact-note">Telefonda yapılan ön görüşme, avukatlık sözleşmesi yerine geçmez. Görüşmede paylaştığınız bilgiler sır saklama yükümlülüğümüz kapsamındadır.</p></div></div>
    </section>''',
    f'''    <section class="section alt">
      {head("Nasıl ilerler", "Telefondan dosyaya üç adım.")}
      <div class="steps"><article class="step"><span>01 · Arama</span><h3>Konuyu kısaca anlatın</h3><p>Telefonda konuyu ve acil bir süre olup olmadığını konuşuruz. Tebligat geldiyse tarihini not edin.</p></article><article class="step"><span>02 · Görüşme</span><h3>Ofiste buluşalım</h3><p>Belgeleri birlikte inceler, seçenekleri, süreleri ve masrafları konuşuruz.</p></article><article class="step"><span>03 · Vekalet</span><h3>Dosya açılır</h3><p>Devam etmeye karar verirseniz noterden vekaletname çıkarılır ve dosyanın takibine başlarız.</p></article></div>
    </section>''',
    f'''    <section class="section">
      {head("Çalışma alanları", "Hangi konuda arıyorsunuz?")}
      {area_rows()}
    </section>''',
    cta("Telefon açmak çoğu zaman en kısa yoldur."),
])
write("iletisim.html", page(path, t, d, "meeting-room.webp", [webpage(path, "ContactPage", t, d), crumbs(("İletişim", path))], body))
print("ok")
