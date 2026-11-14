# Kozanoğlu alt sayfa + blog üretici.
# Kullanım (repo kökünde): python3 -I tools/build-pages.py . && python3 -I tools/sitemap.py .
# Blog yazıları: content/blog/*.md  (yeni yazı için POSTS listesine satır ekleyin)
import json, sys, os, html

OUT = sys.argv[1]
__file__ = os.path.abspath(__file__)
SITE = "https://kozanogluhukuk.com"
TEL = "+902422445420"
TEL_TXT = "(0242) 244 54 20"
MAIL = "avkozanoglu@hotmail.com"
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
    "email": "avkozanoglu@hotmail.com",
    "address": {"@type": "PostalAddress", "streetAddress": "Emek Mah. Yeşilırmak Cd. No:19/2", "postalCode": "07030", "addressLocality": "Kepez", "addressRegion": "Antalya", "addressCountry": "TR"},
    "hasMap": MAP,
    "areaServed": [{"@type": "AdministrativeArea", "name": "Kepez"}, {"@type": "Place", "name": "Varsak, Kepez"}, {"@type": "City", "name": "Antalya"}],
    "knowsAbout": ["Gayrimenkul hukuku", "Taşınmaz hukuku", "Tapu iptal ve tescil", "Ortaklığın giderilmesi", "Kat karşılığı inşaat sözleşmesi", "Kat mülkiyeti", "Kira hukuku", "Kamulaştırma", "İmar hukuku", "Yabancıların taşınmaz edinimi", "İcra ve iflas hukuku"],
    "employee": [{"@type": "Person", "name": n, "jobTitle": t} for n, t in [("Osman Kozanoğlu", "Avukat"), ("Hüseyin Kozanoğlu", "Avukat"), ("Havva Beyza Kozanoğlu Oya", "Avukat")]],
}

NAV = [("/hakkimizda", "Hakkımızda", None), ("/calisma-alanlari", "Çalışma Alanları", "Alanlar"), ("/blog", "Blog", None), ("/iletisim", "İletişim", None)]

RE_HUB = ("/gayrimenkul-hukuku", "Gayrimenkul ve taşınmaz hukuku", "Tapu, hisseli taşınmazlar, inşaat, kira, kamulaştırma ve imar")
RE_AREAS = [
    ("/tapu-iptali-ortakligin-giderilmesi", "Tapu iptali, ortaklığın giderilmesi ve el atma", "Tapu iptal ve tescil, izale-i şuyu, müdahalenin men'i, ecrimisil, önalım, miras kalan taşınmaz"),
    ("/kat-karsiligi-insaat", "Kat karşılığı inşaat ve kat mülkiyeti", "Müteahhit sözleşmeleri, geç teslim, ayıplı daire, site yönetimi ve aidat"),
    ("/kira-hukuku", "Kira hukuku", "Kira artışı, kira tespiti, tahliye davaları ve takipleri"),
    ("/kamulastirma-imar", "Kamulaştırma, imar ve yabancılara satış", "Kamulaştırma bedeli, kamulaştırmasız el atma, imar ve yapı, yabancıların taşınmaz edinimi"),
]
OTHER_AREAS = [
    ("/icra-hukuku", "İcra hukuku", "İcra takibi, çek ve senet, haciz, ödeme emrine itiraz, ipotekli takip"),
]
AREAS = [RE_HUB] + RE_AREAS + OTHER_AREAS

def e(s):
    return html.escape(s, quote=True)

def nav(current):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>' + (f'<span class="l-full">{t}</span><span class="l-short">{s}</span>' if s else t) + "</a>"
        for h, t, s in NAV)
    return f'<nav class="site-nav" aria-label="Ana navigasyon"><a class="brand" href="/" aria-label="Kozanoğlu Hukuk Bürosu ana sayfa"><img src="/assets/logo.webp" width="724" height="543" fetchpriority="high" alt="Kozanoğlu Hukuk Bürosu"></a><div class="nav-links">{links}</div><a class="nav-call" href="tel:{TEL}" aria-label="Büroyu arayın: {TEL_TXT}">{TEL_TXT}</a></nav>'

def footer():
    re_links = "".join(f'<a href="{h}">{t}</a>' for h, t, _ in [RE_HUB] + RE_AREAS)
    other_links = "".join(f'<a href="{h}">{t}</a>' for h, t, _ in OTHER_AREAS)
    return f'''<footer class="site-footer">
    <div class="footer-grid">
      <div><p class="footer-title">Kozanoğlu Hukuk Bürosu</p><address>Emek Mah. Yeşilırmak Cd. No:19/2<br>07030 Kepez / Antalya</address><div class="footer-contact"><div><a class="footer-tel" href="tel:{TEL}">{TEL_TXT}</a></div><div><a class="footer-mail" href="mailto:{MAIL}">{MAIL}</a></div></div></div>
      <nav aria-label="Gayrimenkul hukuku"><p class="footer-title">Gayrimenkul hukuku</p>{re_links}</nav>
      <nav aria-label="Site"><p class="footer-title">İcra hukuku</p>{other_links}<p class="footer-title" style="margin-top:28px">Büro</p><a href="/hakkimizda">Hakkımızda</a><a href="/kepez-varsak-avukat">Kepez ve Varsak</a><a href="/blog">Hukuk notları</a><a href="/iletisim">İletişim ve yol tarifi</a></nav>
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
  <link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/pages.css?v=20261113">
  {BOOT}
  <link rel="stylesheet" href="/transitions.css?v=20261113"><script defer src="/transitions.js?v=20261113"></script>
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
  <a class="call-fab" href="tel:{TEL}" aria-label="Büroyu arayın: {TEL_TXT}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>Arayın</a>
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

def area_rows(exclude=None, items=None):
    rows = ""
    for i, (h, t, d) in enumerate(items or AREAS, 1):
        if h == exclude:
            continue
        rows += f'<a class="area-row" href="{h}"><span class="area-index">{i:02d}</span><span class="area-text"><strong>{t}</strong><span>{d}</span></span><span class="area-arrow" aria-hidden="true">↗</span></a>'
    return f'<div class="area-list">{rows}</div>'

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

# ---------------------------------------------------------------- Blog
import re as _re
BLOG_DATE = "2026-11-04"
NEW_DATE = "2026-11-10"
D3 = "2026-11-14"
TAPU = ("/tapu-iptali-ortakligin-giderilmesi", "Tapu, ortaklık ve el atma")
INSAAT = ("/kat-karsiligi-insaat", "Kat karşılığı inşaat ve kat mülkiyeti")
KAMU = ("/kamulastirma-imar", "Kamulaştırma, imar ve yabancılara satış")
POSTS = [
    # slug, md, kategori, alan linki, alan adı, görsel, görsel alt, [tarih]
    ("tapu-iptal-ve-tescil-davasi", "tapu-iptal.md", "Tapu", *TAPU, "blog-tapu-iptal", "Ceviz bir masada kapalı eski bir defter, dolma kalem ve pirinç bir anahtar", D3),
    ("kat-karsiligi-insaat-sozlesmesi", "kat-karsiligi.md", "İnşaat", *INSAAT, "blog-kat-karsiligi", "Gün batımında iskeleli, kaba inşaat hâlindeki bir apartman ve bir kule vinç", D3),
    ("kamulastirma-bedeli-itiraz", "kamulastirma.md", "Kamulaştırma", *KAMU, "blog-kamulastirma", "Zeytinlik tepelerin arasından kıvrılarak geçen yeni bir asfalt yol", D3),
    ("muris-muvazaasi-davasi", "muris.md", "Miras", *TAPU, "blog-muris", "Eski bir köy evinin taş pencere pervazında duran demir bir anahtar", D3),
    ("ev-alirken-kapora-ve-satis-vaadi", "kapora.md", "Alım-satım", *KAMU, "blog-kapora", "Boş ve aydınlık bir dairede travertin tezgâh üzerinde pirinç bir anahtar ve kapalı bir zarf", D3),
    ("muteahhit-daireyi-gec-teslim-ederse", "gec-teslim.md", "İnşaat", *INSAAT, "blog-gec-teslim", "Yeni yapılmış boş bir odada pencerenin yanındaki duvarda ince bir çatlak", D3),
    ("hisseli-tapuda-onalim-hakki", "onalim.md", "Tapu", *TAPU, "blog-onalim", "Antalya kırsalında alçak bir kuru taş duvarla bölünmüş zeytinli bir tarla", D3),
    ("kamulastirmasiz-el-atma", "el-atma.md", "Kamulaştırma", *KAMU, "blog-el-atma", "Bir bahçenin taş sınır duvarını kesip geçen dar bir yol", D3),
    ("ecrimisil-nedir", "ecrimisil.md", "Tapu", *TAPU, "blog-ecrimisil", "Taş bir bahçe duvarında eski bir asma kilitle kapatılmış ahşap kapı", D3),
    ("yabancilara-konut-satisi", "yabanci.md", "Alım-satım", *KAMU, "blog-yabanci", "Antalya'da denize ve Toros dağlarına bakan sakin bir balkon ve iki boş sandalye", D3),
    ("ev-sahibi-kiraciyi-nasil-cikarir", "tahliye.md", "Kira", "/kira-hukuku", "Kira hukuku","blog-tahliye", "Boş bir odada açık kapının yanında üst üste duran koliler ve üzerinde bir anahtar", NEW_DATE),
    ("kira-artisi-ve-kira-tespit-davasi", "kira.md", "Kira", "/kira-hukuku", "Kira hukuku","blog-kira", "Travertin bir rafın üzerinde pirinç ev anahtarları ve katlanmış boş bir kâğıt"),
    ("odeme-emri-geldi", "odeme.md", "İcra", "/icra-hukuku", "İcra hukuku", "blog-odeme", "Travertin bir yüzeyde üst üste duran zarflar ve pirinç bir mektup açacağı"),
    ("miras-kalan-tasinmaz", "miras.md", "Miras", "/tapu-iptali-ortakligin-giderilmesi", "Tapu, ortaklık ve miras kalan taşınmaz","blog-miras", "Önünde yaşlı bir zeytin ağacı olan eski taş bir köy evi"),
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
TR_AY = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
for slug, md, cat, alink, aname, img, alt, *rest in POSTS:
    date = rest[0] if rest else BLOG_DATE
    title, summary, tldr, sections, faqs = parse_md(os.path.join(OUT, "content", "blog", md))
    parsed.append(dict(date=date, slug=slug, cat=cat, alink=alink, aname=aname, img=img, alt=alt, title=title, summary=summary, tldr=tldr, sections=sections, faqs=faqs, mins=max(3, round(words(sections, tldr, faqs) / 200))))

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
        <p class="disclaimer">Bu yazı genel bilgilendirme amacıyla hazırlanmıştır ve hukuki görüş niteliğinde değildir. Mevzuat ve uygulama değişebilir; kendi durumunuz için bir avukatla görüşün. Son güncelleme: {int(p["date"][8:])} {TR_AY[int(p["date"][5:7])]} {p["date"][:4]}.</p>
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
             {"@type": "BlogPosting", "@id": SITE + path + "#article", "headline": p["title"], "description": desc, "image": SITE + f"/assets/blog/{p['img']}.webp", "datePublished": p["date"], "dateModified": p["date"], "inLanguage": "tr-TR", "articleSection": p["cat"], "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "mainEntityOfPage": {"@id": SITE + path + "#webpage"}, "about": {"@id": SITE + p["alink"] + "#service"}},
             crumbs(("Hukuk Notları", "/blog"), (p["title"], path))]
    if faqs: graph.append(faq_ld(faqs))
    html_out = page(path, ttl, desc, f"blog/{p['img']}.webp", graph, body, og_img=f"/assets/blog/{p['img']}-og.jpg", og_type="article")
    write(os.path.join("blog", p["slug"] + ".html"), html_out)

# blog index
path = "/blog"
t = "Gayrimenkul Hukuku Notları: Tapu, Kira, Kamulaştırma | Kozanoğlu Hukuk"
d = "Tapu iptali, muris muvazaası, önalım, kat karşılığı inşaat, kamulaştırma, ecrimisil, kapora, kira ve icra: süreleri ve adımları örneklerle anlatan yazılar."
feat, rest = parsed[0], parsed[1:]
cards = "".join(f'<a class="post-card" href="/blog/{o["slug"]}"><img src="/assets/blog/{o["img"]}-card.webp" width="800" height="450" loading="lazy" decoding="async" alt="{e(o["alt"])}"><span class="post-meta"><span>{o["cat"]}</span><span>{o["mins"]} dk.</span></span><h2>{_inline(o["title"])}</h2><p>{_inline(o["summary"])}</p><span class="read">Yazıyı okuyun ↗</span></a>' for o in rest)
body = "\n".join([
    hero("interior-logo.webp", "Hukuk notları", "Süreler, adımlar, sık yapılan hatalar.", "Taşınmaz dosyalarında en sık sorulan konular. Her yazıda kanun maddesi, kaçırılmaması gereken süre ve gündelik hayattan birer örnek var."),
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
    paths = area_path if isinstance(area_path, (list, tuple)) else [area_path]
    rel = [o for o in parsed if o["alink"] in paths]
    if not rel: return ""
    cards = "".join(f'<a class="post-card" href="/blog/{o["slug"]}"><img src="/assets/blog/{o["img"]}-card.webp" width="800" height="450" loading="lazy" decoding="async" alt=""><span class="post-meta"><span>{o["cat"]}</span><span>{o["mins"]} dk.</span></span><h3>{_inline(o["title"])}</h3><p>{_inline(o["summary"])}</p><span class="read">Yazıyı okuyun ↗</span></a>' for o in rel)
    return f'''    <section class="section">
      {head("Hukuk notları", "Bu konuda yazdıklarımız.")}
      <div class="blog-grid">{cards}</div>
    </section>'''

# ---------------------------------------------------------------- Area pages
def area_page(slug, img, title, desc, eyebrow, h1, lead, topics_h2, topics_intro, topics, notes_h2, notes, faqs, local, cta_h2, service, docs=None, re_sub=False):
    path = "/" + slug
    if re_sub:
        crumb = [("/calisma-alanlari", "Çalışma alanları"), (RE_HUB[0], "Gayrimenkul hukuku")]
        crumb_ld = [("Çalışma Alanları", "/calisma-alanlari"), ("Gayrimenkul Hukuku", RE_HUB[0])]
        others = f'''    <section class="section alt">
      {head("Gayrimenkul hukuku", "Diğer taşınmaz konuları.")}
      {area_rows(exclude=path, items=[RE_HUB] + RE_AREAS)}
    </section>'''
    else:
        crumb = [("/calisma-alanlari", "Çalışma alanları")]
        crumb_ld = [("Çalışma Alanları", "/calisma-alanlari")]
        others = f'''    <section class="section alt">
      {head("Ana alanımız", "Gayrimenkul ve taşınmaz hukuku.", "Büromuzun ağırlıklı çalıştığı alan. Tapu, hisseli taşınmaz, inşaat, kira ve kamulaştırma dosyaları.")}
      {area_rows(items=[RE_HUB] + RE_AREAS)}
    </section>'''
    topic_html = "".join(f'<li><strong>{t}</strong><span>{d}</span></li>' for t, d in topics)
    notes_html = "".join(f'<h3>{t}</h3><p>{p}</p>' for t, p in notes)
    docs_html = ""
    if docs:
        d_intro, d_items = docs
        docs_html = f'''    <section class="section">
      {head("İlk görüşme", "Yanınızda getirirseniz işimiz hızlanır.", d_intro)}
      <ol class="doc-list">{"".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in d_items)}</ol>
    </section>'''
    body = "\n".join([
        hero(img, eyebrow, h1, lead, crumb=crumb),
        f'''    <section class="section">
      {head("Neler yapıyoruz", topics_h2, topics_intro)}
      <ul class="topic-grid">{topic_html}</ul>
    </section>''',
        f'''    <section class="section alt article-section"><div><p class="section-label">Bilmeniz gerekenler</p><h2>{notes_h2}</h2></div><div class="article-body">{notes_html}<p class="disclaimer">Süreler ve kurallar mevzuat değişikliğiyle güncellenebilir. Kendi durumunuz için bizimle görüşün.</p></div></section>''',
        f'''    <section class="section local-note"><div class="local-grid"><p class="section-label">Pratikte</p><div><p class="local-lead">{local}</p><a class="text-link" href="/kepez-varsak-avukat">Kepez ve Varsak sayfası ↗</a></div></div></section>''',
        docs_html,
        faq_html(faqs),
        related_posts(path),
        others,
        cta(cta_h2),
    ])
    svc = {"@type": "Service", "@id": SITE + path + "#service", "serviceType": service, "name": h1.rstrip("."), "provider": {"@id": ORG_ID}, "areaServed": [{"@type": "AdministrativeArea", "name": "Kepez"}, {"@type": "City", "name": "Antalya"}], "url": SITE + path}
    if re_sub:
        svc["isRelatedTo"] = {"@id": SITE + RE_HUB[0] + "#service"}
    graph = [webpage(path, "WebPage", title, desc), svc,
             crumbs(*crumb_ld, (h1.rstrip("."), path)), faq_ld(faqs)]
    write(slug + ".html", page(path, title, desc, img, graph, body))

# ---------------------------------------------------------------- Gayrimenkul hub
RE_PATHS = [h for h, _, _ in RE_AREAS]
path = RE_HUB[0]
t = "Antalya Gayrimenkul Avukatı | Kozanoğlu Hukuk, Kepez"
d = "Antalya'da gayrimenkul ve taşınmaz hukuku: tapu iptal ve tescil, ortaklığın giderilmesi, kat karşılığı inşaat, kira, kamulaştırma, imar ve yabancılara satış. Kepez, (0242) 244 54 20."
hub_faqs = [
    ("Taşınmaz davası hangi mahkemede açılır?", "Tapu iptal ve tescil, el atmanın önlenmesi gibi aynı hakka ilişkin davalar taşınmazın bulunduğu yer mahkemesinde açılır; bu yetki kesindir. Antalya'daki bir taşınmaz için dava, siz başka şehirde otursanız da Antalya'da görülür."),
    ("Her taşınmaz uyuşmazlığında arabulucuya gitmek gerekir mi?", "Hayır. Kira, ortaklığın giderilmesi, kat mülkiyeti ve komşuluk uyuşmazlıklarında dava öncesi arabuluculuk zorunludur. Tapu iptal ve tescil davaları için böyle bir zorunluluk yoktur."),
    ("Tapuda şerh, ipotek ya da haciz olup olmadığını nasıl öğrenirim?", "Malik iseniz e-Devlet üzerinden tapu kaydınızı görebilirsiniz. Satın almayı düşündüğünüz bir taşınmaz için satıcıdan güncel tapu kaydını isteyin; alım öncesinde kaydı birlikte inceleriz."),
    ("Antalya dışında yaşıyorum, dosyamı yürütebilir misiniz?", "Evet. Herhangi bir noterden vekaletname çıkarmanız yeterlidir. Keşif, bilirkişi incelemesi ve duruşmalara biz katılırız; gelişmeleri size düzenli olarak bildiririz."),
    ("Dava ne kadar sürer?", "Dosyanın türüne, keşif ve bilirkişi aşamasına ve mahkemenin iş yüküne göre değişir. İlk görüşmede sizinkine benzer dosyaların ortalama ne kadar sürdüğünü açıkça söyleriz; kesin bir tarih vermeyiz."),
]
hub_steps = '<div class="steps"><article class="step"><span>01 · Kayıt</span><h3>Önce tapuya bakarız</h3><p>Tapu kaydı, hisse oranları, şerh ve beyanlar, imar durumu. Çoğu dosyanın yönünü kayıtların kendisi belirler.</p></article><article class="step"><span>02 · Yol</span><h3>Dava mı, arabulucu mu?</h3><p>İhtarname, arabuluculuk, tespit ya da dava. Hangisinin ne kadar süreceğini ve masrafını ilk görüşmede konuşuruz.</p></article><article class="step"><span>03 · Tescil</span><h3>Karar tapuya işlenene kadar</h3><p>Kararı alıp bırakmayız. Kesinleşme, tapuya tescil ya da tahliye adımına kadar dosyanın başındayız.</p></article></div>'
hub_notes = [
    ("Taşınmaz satışı resmi şekle bağlıdır", "Taşınmaz satışı tapu müdürlüğünde, satış vaadi ve kat karşılığı inşaat sözleşmesi ise noterde düzenleme şeklinde yapılmalıdır. Elden yapılan sözleşmeler ve adi yazılı belgeler mülkiyeti geçirmez; çoğu zaman yalnızca ödenen paranın iadesi istenebilir."),
    ("Tapu kaydına güvenilir, ama her zaman değil", "Tapuya güvenerek iyi niyetle taşınmaz edinen kişi korunur. Kayıt hileli bir işlemle oluşmuşsa ya da alıcı durumu biliyorsa, tapu iptal ve tescil davası açılabilir. İyi niyetin varlığı dosyanın en çok tartışılan konusudur."),
    ("İhtiyati tedbir taşınmazı korur", "Dava sürerken taşınmazın üçüncü kişilere satılmasını önlemek için tapuya ihtiyati tedbir şerhi konulması istenebilir. Tedbir olmadan dava sırasında yapılan bir satış, dosyayı çok daha zor hale getirir."),
    ("Keşif ve bilirkişi dosyanın merkezindedir", "Taşınmaz davalarının çoğunda mahkeme yerinde keşif yapar, bilirkişiden değer ya da teknik rapor alır. Rapora itiraz süresi kısadır; raporu tebliğ aldığımız gün inceleriz."),
]
hub_body = "\n".join([
    hero("hero-poster.webp", "Ana çalışma alanı", "Gayrimenkul ve taşınmaz hukuku.", "Tapu iptali ve tescil, hisseli taşınmazlar, kat karşılığı inşaat, kira, kamulaştırma ve imar. Bir taşınmazın alımından paylaşımına kadar her aşamada danışmanlık veriyor, davaları yürütüyoruz.", crumb=[("/calisma-alanlari", "Çalışma alanları")]),
    f'''    <section class="section">
      {head("Dört başlık", "Taşınmaz dosyalarını dört başlıkta topluyoruz.", "Her başlığın kendi sayfasında kaçırılmaması gereken süreler, sık sorulan sorular ve görüşmeye getirmeniz gereken belgeler var. Konunuzun hangisine girdiğinden emin değilseniz arayın, telefonda söyleyelim.")}
      {area_rows(items=RE_AREAS)}
    </section>''',
    f'''    <section class="section alt">
      {head("Nasıl ilerleriz", "Her taşınmaz dosyası kayıtla başlar.")}
      {hub_steps}
    </section>''',
    f'''    <section class="section article-section"><div><p class="section-label">Bilmeniz gerekenler</p><h2>Taşınmaz işlerinde dört temel kural.</h2></div><div class="article-body">{"".join(f"<h3>{a}</h3><p>{b}</p>" for a, b in hub_notes)}<p class="disclaimer">Süreler ve kurallar mevzuat değişikliğiyle güncellenebilir. Kendi durumunuz için bizimle görüşün.</p></div></section>''',
    f'''    <section class="section local-note alt"><div class="local-grid"><p class="section-label">Antalya'da</p><div><p class="local-lead">Antalya'da taşınmaz dosyalarının kendine özgü bir rengi var: Varsak gibi 2008'e kadar ayrı belediye olan bölgelerde eski ve hisseli tapular, hızla yükselen yeni siteler, imar planı değişiklikleri ve yabancılara yapılan satışlar. Dosyalarımızın büyük bölümü bu başlıklardan birine dokunuyor.</p><a class="text-link" href="/kepez-varsak-avukat">Kepez ve Varsak sayfası ↗</a></div></div></section>''',
    f'''    <section class="section">
      {head("İlk görüşme", "Yanınızda getirirseniz işimiz hızlanır.", "Hepsi elinizde olmayabilir. Olanları getirin, eksikleri görüşmede birlikte çıkarırız.")}
      <ol class="doc-list">{"".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in [
          ("Güncel tapu kaydı", "e-Devlet ya da Web Tapu'dan alınan kayıt; hisse oranları, şerh ve beyanlarla birlikte."),
          ("Sözleşmeler", "Satış vaadi, kat karşılığı inşaat, kira ya da ortaklık sözleşmesi; noter onaylıysa yevmiye numarasıyla."),
          ("İmar ve yapı belgeleri", "İmar durumu, ruhsat, iskân, proje ve varsa belediyeden gelen yazılar."),
          ("Tebligatlar", "İhtarname, dava dilekçesi, kamulaştırma ya da arabuluculuk davetleri; zarflarıyla birlikte."),
          ("Mirasçılık belgesi", "Taşınmaz miras kaldıysa noterden ya da sulh hukuk mahkemesinden alınan veraset ilamı."),
          ("Ödeme kayıtları ve yazışmalar", "Banka dekontları, makbuzlar, karşı tarafla yapılan mesajlaşmalar."),
      ])}</ol>
    </section>''',
    faq_html(hub_faqs),
    related_posts(RE_PATHS),
    f'''    <section class="section alt">
      {head("Ayrıca", "İcra hukuku.", "Kira alacağı, ipotekli takip ya da bir taşınmaza konan haciz. İcra dosyalarını da üstleniyoruz.")}
      {area_rows(items=OTHER_AREAS)}
    </section>''',
    cta("Tapu, hisse, inşaat ya da kira: önce kayıtlara bakalım."),
])
hub_graph = [webpage(path, "WebPage", t, d),
             {"@type": "Service", "@id": SITE + path + "#service", "serviceType": "Gayrimenkul ve taşınmaz hukuku", "name": "Gayrimenkul ve taşınmaz hukuku", "provider": {"@id": ORG_ID}, "areaServed": [{"@type": "AdministrativeArea", "name": "Kepez"}, {"@type": "City", "name": "Antalya"}], "url": SITE + path,
              "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Gayrimenkul hukuku", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": SITE + h}} for h, n, _ in RE_AREAS]}},
             crumbs(("Çalışma Alanları", "/calisma-alanlari"), ("Gayrimenkul Hukuku", path)), faq_ld(hub_faqs)]
write("gayrimenkul-hukuku.html", page(path, t, d, "hero-poster.webp", hub_graph, hub_body))

# ---------------------------------------------------------------- Tapu, ortaklık, el atma
area_page(
    "tapu-iptali-ortakligin-giderilmesi", "footer-table.webp",
    "Tapu İptal ve Tescil, Ortaklığın Giderilmesi Avukatı | Kozanoğlu Hukuk Antalya",
    "Antalya'da tapu iptal ve tescil, muris muvazaası, ortaklığın giderilmesi (izale-i şuyu), el atmanın önlenmesi, ecrimisil, önalım ve miras kalan taşınmaz davaları. Kepez, (0242) 244 54 20.",
    "Gayrimenkul hukuku · Tapu ve ortaklık", "Tapu iptali, ortaklığın giderilmesi ve el atma.",
    "Yanlış ya da haksız tescil, anlaşamayan hissedarlar, izinsiz kullanılan arsa ve miras kalan taşınmazlar.",
    "Bu başlıkta üstlendiğimiz işler.",
    "Bu dosyaların çoğunda karşı taraf tanıdık biridir: kardeş, akraba, komşu ya da eski ortak. Önce anlaşma yolunu deneriz; olmazsa davayı açar, karar tapuya işlenene kadar takip ederiz.",
    [("Tapu iptal ve tescil", "Muvazaalı satış, vekâletin kötüye kullanılması, hile ya da hatayla yapılan devirlerin iptali."),
     ("Muris muvazaası", "Mirasçılardan mal kaçırmak için satış gibi gösterilen bağışların iptali."),
     ("Ortaklığın giderilmesi", "Hisseli taşınmazların aynen bölünmesi ya da satılarak bedelin paylaştırılması (izale-i şuyu)."),
     ("El atmanın önlenmesi ve ecrimisil", "Taşınmazınızı izinsiz kullanan kişinin çıkarılması ve geçmiş kullanım bedelinin istenmesi."),
     ("Önalım (şufa) hakkı", "Hissedarlardan biri payını üçüncü kişiye sattığında, o payı aynı bedelle alma hakkı."),
     ("Kadastro ve zilyetlik", "Kadastro tespitine itiraz, tapusuz taşınmazların zilyetlik yoluyla tescili, sınır ve yüzölçümü düzeltmeleri.")],
    "Dava açmadan önce bilmeniz gerekenler.",
    [("Muris muvazaasında süre sınırı yok", "Murisin sağlığında mirasçılardan mal kaçırmak amacıyla yaptığı ‘satış görünümlü bağış’lara karşı açılan davalar zamanaşımına tabi değildir. Ancak tanıkların ve belgelerin kaybolmaması için beklememek gerekir."),
     ("Ortaklığın giderilmesinde önce arabulucu", "1 Eylül 2023'ten bu yana ortaklığın giderilmesi davasından önce arabulucuya başvurmak zorunludur. Anlaşma olmazsa sulh hukuk mahkemesi önce aynen bölmeyi değerlendirir; mümkün değilse taşınmazın satışına karar verir."),
     ("Önalım için üç ay ve iki yıl", "Pay satışını öğrendiğiniz tarihten itibaren üç ay, her halde satıştan itibaren iki yıl içinde önalım davası açılmalıdır. Mahkemenin belirlediği süre içinde satış bedeli ve tapu masrafları depo edilmezse dava reddedilir."),
     ("Ecrimisil geriye dönük beş yıl", "Taşınmazınızı izinsiz kullanan kişiden geçmişe dönük beş yıla kadar kullanım bedeli istenebilir. Paydaşlar arasında ecrimisil istemek için ise kural olarak önce kullanımın engellendiğini gösteren bir ihtar gerekir."),
     ("Kadastro tespitine itiraz için on yıl", "Kadastro tutanağının kesinleşmesinden itibaren on yıl geçtikten sonra, tespitten önceki sebeplere dayanarak itiraz edilemez. Askı ilanı süresindeki otuz günlük itiraz ise kadastro komisyonuna yapılır.")],
    [("Babam evi kardeşime satmış gibi göstermiş, ne yapabilirim?", "Satış gerçekte bir bağışsa ve amaç diğer mirasçılardan mal kaçırmaksa muris muvazaası nedeniyle tapu iptal ve tescil davası açılabilir. Bedelin gerçekten ödenip ödenmediği, taşınmazın değeri ve aile içi ilişkiler birlikte değerlendirilir."),
     ("Miras kalan tarlayı kardeşlerle paylaşamıyoruz.", "Önce arabulucuya başvurulur. Anlaşma çıkmazsa ortaklığın giderilmesi davası açılır; bölünmesi mümkün değilse taşınmaz ihaleyle satılır ve bedel paylar oranında dağıtılır. Satıştan önce aranızda anlaşmak çoğu zaman daha iyi bir bedel getirir."),
     ("Hissedarlardan biri payını yabancı birine sattı.", "Satışı öğrendiğiniz günden itibaren üç ay içinde önalım davası açarak o payı aynı bedelle alabilirsiniz. Süre kısa olduğu için tapu kaydını hemen inceleyelim."),
     ("Komşu arsama duvar çekti, ne yapabilirim?", "El atmanın önlenmesi ve yıkım davası açılabilir; izinsiz kullanım süresi için ecrimisil de istenebilir. Sınırın tam yeri genellikle keşif ve fen bilirkişisi raporuyla belirlenir."),
     ("Tapusu olmayan bir arazi için ne yapabilirim?", "Tapuda kayıtlı olmayan bir taşınmazı yirmi yıl boyunca çekişmesiz ve aralıksız, malik gibi kullandıysanız zilyetliğe dayalı tescil davası açılabilir. Taşınmazın niteliği ve kadastro durumu önce incelenir."),
     ("Vekâlet verdiğim kişi evimi düşük bedelle satmış.", "Vekil, yetkisini kötüye kullanarak taşınmazı gerçek değerinin çok altında ya da alıcıyla anlaşarak sattıysa tapu iptal ve tescil davası açılabilir. Alıcının durumu bilip bilmediği belirleyicidir.")],
    "Varsak'ta ve Kepez'in kırsal mahallelerinde kuşaklardır bölünmemiş hisseli tarlalar ve eski tarihli kayıtlar sık görülür. Bu dosyalarda önce veraset durumunu ve tapu geçmişini çıkarır, kimin hangi payda olduğunu netleştiririz.",
    "Tapu, hisse ya da miras: önce kayıtlara bakalım.", "Tapu iptal ve tescil, ortaklığın giderilmesi",
    docs=("Bu dosyalar kayıt üzerinden yürür. Tapu geçmişi ne kadar eksiksiz olursa ilk görüşmede o kadar net konuşuruz.",
          [("Güncel tapu kaydı", "Hisse oranları, şerh ve beyanlar görünecek şekilde."),
           ("Tapu geçmişi", "Taşınmazın önceki malikleri ve satış tarihleri; tapu müdürlüğünden alınabilir."),
           ("Mirasçılık belgesi", "Noterden ya da sulh hukuk mahkemesinden alınan veraset ilamı."),
           ("Satış ve vekâlet belgeleri", "Resmi senet, vekâletname ve varsa ödeme dekontları."),
           ("Kadastro ve harita", "Kadastro tutanağı, çap ya da aplikasyon krokisi."),
           ("Fotoğraflar ve tanıklar", "Taşınmazın kullanımını gösteren fotoğraflar ve durumu bilen kişilerin adları.")]),
    re_sub=True)

# ---------------------------------------------------------------- Kat karşılığı inşaat, kat mülkiyeti
area_page(
    "kat-karsiligi-insaat", "interior-logo.webp",
    "Kat Karşılığı İnşaat ve Kat Mülkiyeti Avukatı | Kozanoğlu Hukuk Antalya",
    "Antalya'da kat karşılığı inşaat sözleşmeleri, müteahhit uyuşmazlıkları, geç teslim, ayıplı konut, kat mülkiyeti, site yönetimi ve aidat davaları. Kepez, (0242) 244 54 20.",
    "Gayrimenkul hukuku · İnşaat ve kat mülkiyeti", "Kat karşılığı inşaat ve kat mülkiyeti.",
    "Müteahhitle sözleşme, geç teslim, ayıplı daire, site yönetimi ve aidat.",
    "Bu başlıkta üstlendiğimiz işler.",
    "Arsa sahibi, müteahhit, daire alan ya da site sakini. Hangi taraftaysanız, uyuşmazlığın kaynağı çoğunlukla sözleşmedeki bir maddedir. Bu yüzden işe imzadan önce başlamak, en ucuz çözümdür.",
    [("Kat karşılığı inşaat sözleşmesi", "Sözleşmenin hazırlanması ve incelenmesi; arsa payı, teslim süresi, ceza koşulu ve teminat maddeleri."),
     ("Geç teslim ve sözleşmeden dönme", "Gecikme tazminatı, kira kaybı, ceza koşulu ve sözleşmenin feshi davaları."),
     ("Ayıplı konut", "Eksik ve kusurlu imalat, projeye aykırılık, ayıp tespiti ve bedel indirimi."),
     ("Tapu devri ve tescil", "Müteahhide geçen dairelerin tescili ya da iptali, üçüncü kişilere satılan bağımsız bölümler."),
     ("Kat mülkiyeti ve site yönetimi", "Yönetim planı, kat malikleri kurulu kararlarına itiraz, ortak alan kullanımı."),
     ("Aidat ve ortak gider", "Ödenmeyen aidatların takibi ya da haksız aidat taleplerine itiraz.")],
    "Sözleşmeden önce ve sonra bilmeniz gerekenler.",
    [("Sözleşme noterde düzenleme şeklinde yapılmalı", "Kat karşılığı inşaat sözleşmesi arsa payının devri vaadini içerdiğinden noterde düzenleme şeklinde yapılmalıdır. Adi yazılı ya da yalnızca imzası onaylanmış sözleşmeler, kural olarak tapu devrini istemeye yetmez."),
     ("Teslim tarihi ve ceza koşulu net yazılmalı", "Teslim tarihi, gecikme halinde ödenecek tazminat ve hangi durumların gecikme sayılmayacağı sözleşmede açıkça yazılmazsa, her gecikme ayrı bir tartışma konusu olur."),
     ("Ayıbı gecikmeden bildirin", "Teslimde görülebilen ayıplar uygun süre içinde, sonradan ortaya çıkan gizli ayıplar ise fark edildiği anda müteahhide yazılı olarak bildirilmelidir. Daireyi konut olarak satın aldıysanız uyuşmazlık tüketici mahkemesinde görülür ve çoğu durumda önce arabulucuya gidilir."),
     ("Kurul kararına itiraz için bir ay", "Kat malikleri kurulu kararına karşı iptal davası, toplantıda karşı oy verdiyseniz karar tarihinden, katılmadıysanız öğrendiğiniz tarihten itibaren bir ay, her halde altı ay içinde açılmalıdır. Kat mülkiyeti uyuşmazlıklarında dava öncesi arabuluculuk zorunludur."),
     ("Aidatı geciken için yüzde beş", "Kat mülkiyeti kanununa göre ortak gider ve avans payını zamanında ödemeyen kat maliki, geciken her ay için yüzde beş gecikme tazminatı öder. Yönetim bu alacak için doğrudan icra takibi başlatabilir.")],
    [("Müteahhit inşaatı yarıda bıraktı, ne yapabilirim?", "Sözleşmeden dönülerek arsa payının iadesi ve tazminat istenebilir ya da inşaatın başka bir yükleniciyle tamamlanması için mahkemeden yetki alınabilir. Hangisinin uygun olduğu, inşaatın seviyesine ve tapuda müteahhide ne kadar pay geçtiğine bağlıdır."),
     ("Daire teslim tarihi geçti, tazminat alabilir miyim?", "Sözleşmede ceza koşulu varsa onu, yoksa gecikme süresince kira kaybınızı isteyebilirsiniz. Teslim alırken ihtirazi kayıt koymazsanız ceza koşulunu sonradan istemek zorlaşır."),
     ("Aldığım dairede rutubet ve çatlaklar çıktı.", "Önce ayıbı müteahhide yazılı olarak bildirin. Mahkemeden delil tespiti istenerek ayıbın kaynağı ve onarım bedeli bilirkişiyle belirlenebilir. Ayıba göre bedel indirimi, onarım ya da sözleşmeden dönme talep edilir."),
     ("Kat irtifakından kat mülkiyetine nasıl geçilir?", "Yapı kullanma izni (iskân) alındıktan sonra tapu müdürlüğüne başvurularak kat irtifakı kat mülkiyetine çevrilir. İskân alınamıyorsa nedeni ve sorumlusu ayrıca incelenmelidir."),
     ("Site yönetimi ortak alanı tek bir daireye bıraktı.", "Ortak alanların kullanımı yönetim planına ve kat malikleri kurulu kararına bağlıdır. Usule aykırı alınmış bir karara karşı süresi içinde iptal davası açılabilir; önce arabulucuya başvurulur."),
     ("Arsa sahibi olarak sözleşmeyi imzalamadan önce neye dikkat etmeliyim?", "Arsa payı oranı, dairelerin hangi katta ve cephede olacağı, teslim tarihi, teminat ve tapu devrinin inşaatın ilerlemesine bağlanması. Sözleşmeyi imzadan önce inceler, riskli maddeleri işaretleriz.")],
    "Kepez ve Varsak'ta son yıllarda yükselen sitelerin çoğu kat karşılığı inşaat modeliyle yapıldı. Gelen dosyaların önemli bir bölümü geç teslim, iskân sorunları ve site yönetimiyle ilgili.",
    "Müteahhitle, arsa sahibiyle ya da yönetimle sorun mu var? Konuşalım.", "Kat karşılığı inşaat ve kat mülkiyeti hukuku",
    docs=("Bu dosyalarda her şey sözleşmeye ve tarihlere bağlıdır. Elinizdeki belgeleri eksiksiz getirin.",
          [("İnşaat sözleşmesi", "Noter yevmiye numarasıyla birlikte; varsa ek protokoller."),
           ("Satış belgeleri", "Daireyi müteahhitten aldıysanız satış vaadi, resmi senet ve ödeme dekontları."),
           ("Proje ve ruhsat", "Onaylı proje, yapı ruhsatı, varsa iskân belgesi."),
           ("Fotoğraflar", "Ayıpları ve inşaatın durumunu gösteren tarihli fotoğraflar."),
           ("Yazışmalar ve ihtarlar", "Müteahhit, arsa sahibi ya da yönetimle yazışmalar, gönderilen ihtarnameler."),
           ("Site belgeleri", "Yönetim planı, karar defteri sayfaları, aidat dökümü.")]),
    re_sub=True)

# ---------------------------------------------------------------- Kira hukuku
area_page(
    "kira-hukuku", "meeting-room.webp",
    "Antalya Kira Avukatı: Kira Tespiti ve Tahliye | Kozanoğlu Hukuk",
    "Antalya ve Kepez'de kira hukuku: kira artışı, kira tespit davası, ihtiyaç ve temerrüt nedeniyle tahliye, tahliye taahhüdü, arabuluculuk. Ev sahibi ve kiracı tarafında. (0242) 244 54 20.",
    "Gayrimenkul hukuku · Kira", "Kira hukuku.",
    "Kira artışı, kira tespiti ve tahliye; ev sahibi ve kiracı tarafında.",
    "Kira dosyalarında üstlendiğimiz işler.",
    "Kira uyuşmazlıklarında süreler çok kısadır ve bir ayı kaçırmak, davayı bir yıl ertelemek demektir. Ev sahibi ya da kiracı, ilk iş tarihlerinizi çıkarırız.",
    [("Kira artışı", "Yasal sınır içinde artış ve sınırı aşan taleplere karşı kiracının hakları."),
     ("Kira tespit davası", "Beş yılı dolan sözleşmelerde kira bedelinin emsallere göre belirlenmesi."),
     ("İhtiyaç nedeniyle tahliye", "Malikin ya da yakınlarının konut veya işyeri ihtiyacına dayalı tahliye davaları."),
     ("Temerrüt ve iki haklı ihtar", "Kiranın ödenmemesi nedeniyle icra yoluyla ya da dava açılarak tahliye."),
     ("Tahliye taahhüdü", "Yazılı taahhüde dayalı tahliye takipleri ve taahhüdün geçerliliğinin incelenmesi."),
     ("Kira sözleşmesi ve ihtarname", "Sözleşmenin hazırlanması, ihtarname, depozito ve hasar uyuşmazlıkları.")],
    "Kaçırılmaması gereken süreler.",
    [("Önce arabulucu", "1 Eylül 2023'ten bu yana kira ilişkisinden doğan uyuşmazlıklarda dava açmadan önce arabulucuya başvurmak zorunludur. Tahliye taahhüdüne ya da kira borcuna dayalı icra takipleri ise doğrudan başlatılabilir."),
     ("Konut kirasında artışın sınırı", "Konut kiralarında yıllık artış, bir önceki kira yılının on iki aylık TÜFE ortalamasını geçemez. Beş yılı dolduran sözleşmelerde ise kira bedeli mahkemece emsallere göre yeniden belirlenebilir."),
     ("Kira tespitinde otuz gün", "Kira tespit davası yeni kira döneminin başlamasından en az otuz gün önce açılır ya da ev sahibi bu süre içinde kiracıya yazılı olarak artış bildirirse, belirlenen kira yeni dönemin başından itibaren geçerli olur."),
     ("İhtiyaç davası için bir ay", "Belirli süreli sözleşmede ihtiyaç nedeniyle tahliye davası, sözleşme süresinin bitiminden itibaren bir ay içinde açılmalıdır. Evi yeni satın alan malik ise edinmeden itibaren bir ay içinde kiracıya bildirim yapmalı, altı ay sonra dava açabilir."),
     ("On yıl kuralı", "Konut ve çatılı işyeri kiralarında on yıllık uzama süresi dolduktan sonra ev sahibi, her uzama yılının bitiminden en az üç ay önce bildirimde bulunarak sebep göstermeden sözleşmeyi sona erdirebilir.")],
    [("Ev sahibim kirayı yasal sınırın üzerinde artırmak istiyor.", "Konut kiralarında on iki aylık TÜFE ortalamasının üzerindeki artışı kabul etmek zorunda değilsiniz. Ancak sözleşmeniz beş yılı doldurduysa ev sahibi kira tespit davası açabilir."),
     ("Oturduğum ev satıldı, yeni ev sahibi beni çıkarabilir mi?", "Satış kira sözleşmesini bitirmez. Yeni malik evi kendisi kullanacaksa, tapuyu aldıktan sonra bir ay içinde size yazılı bildirim yapmak ve altı ay sonra dava açmak zorundadır."),
     ("Sözleşme süresi doldu, ev sahibi çıkmamı istiyor.", "Konut kiralarında sürenin dolması tek başına tahliye sebebi değildir. Siz çıkmak istemedikçe sözleşme birer yıl uzar; ev sahibi ancak kanunda sayılan sebeplerle dava açabilir."),
     ("Kiracım kirayı ödemiyor, ne yapmalıyım?", "Kira borcu için icra takibi başlatılarak kiracıya otuz gün süre verilir; bu sürede ödeme yapılmazsa icra mahkemesinden tahliye istenebilir. Bir kira yılı içinde iki haklı ihtar çekildiyse, yıl bitiminden itibaren bir ay içinde tahliye davası da açılabilir."),
     ("Sözleşmeyle birlikte imzalatılan tahliye taahhüdü geçerli mi?", "Kira sözleşmesiyle aynı anda, kiracı henüz eve girmeden alınan tahliye taahhütleri Yargıtay uygulamasına göre geçersiz sayılır. Taahhüdün tarihi ve kim tarafından doldurulduğu bu yüzden önemlidir."),
     ("Depozitomu geri vermiyorlar.", "Ev teslim edildiğinde kira borcu ve kiracıdan kaynaklanan bir hasar yoksa depozito iade edilmelidir. Evi teslim ederken tutanak tutup fotoğraf çekmek, sonradan çıkacak tartışmayı büyük ölçüde önler.")],
    "Kepez ve Varsak'ta kira uyuşmazlıkları arabuluculuk aşamasında sık çözülür. Arabuluculuk toplantısına sizinle birlikte katılır, anlaşma çıkmazsa sulh hukuk mahkemesinde davayı açarız.",
    "Kira artışı mı, tahliye mi? Süre dolmadan konuşalım.", "Kira hukuku",
    docs=("Kira dosyaları kâğıt üzerinde yürür. Sözlü anlaşmaların çoğu ancak bir dekont ya da mesajla ispatlanabilir.",
          [("Kira sözleşmesi", "Yazılı sözleşme yoksa kiranın ödendiğini gösteren banka dekontları."),
           ("Ödeme kayıtları", "Son dönemin kira ödemelerini gösteren hesap hareketleri."),
           ("İhtarname ve tebligatlar", "Zarflarıyla birlikte. Süreler tebliğ tarihinden başlar."),
           ("Tahliye taahhüdü", "Varsa aslı ya da okunaklı bir kopyası."),
           ("Tapu kaydı", "Ev sahibiyseniz güncel tapu kaydı; ev yeni satın alındıysa edinme tarihi."),
           ("Yazışmalar", "Ev sahibi ya da kiracıyla yapılan mesajlaşmalar.")]),
    re_sub=True)

# ---------------------------------------------------------------- Kamulaştırma, imar, yabancılar
area_page(
    "kamulastirma-imar", "rear-entrance.webp",
    "Kamulaştırma, İmar ve Yabancılara Taşınmaz Satışı | Kozanoğlu Hukuk Antalya",
    "Antalya'da kamulaştırma bedeli, kamulaştırmasız el atma, imar planı ve yapı uyuşmazlıkları, yabancıların taşınmaz edinimi ve alım-satım danışmanlığı. Kepez, (0242) 244 54 20.",
    "Gayrimenkul hukuku · Kamulaştırma ve imar", "Kamulaştırma, imar ve yabancılara satış.",
    "Kamulaştırma bedeli, kamulaştırmasız el atma, imar ve yapı sorunları, yabancıların taşınmaz edinimi.",
    "Bu başlıkta üstlendiğimiz işler.",
    "Bu dosyalarda karşınızda çoğu zaman bir idare ya da bir alım-satım işlemi vardır. Süreler idari ve kısadır; doğru yere doğru zamanda başvurmak, davanın kendisi kadar önemlidir.",
    [("Kamulaştırma bedeli", "Uzlaşma görüşmeleri ve idarenin açtığı bedel tespiti ve tescil davalarında gerçek değerin savunulması."),
     ("Kamulaştırmasız el atma", "İdarenin kamulaştırmadan yol, kanal ya da başka bir amaçla kullandığı taşınmazlar için tazminat."),
     ("İmar planı uyuşmazlıkları", "Plan değişikliklerine itiraz ve iptal davaları, kamu alanına ayrılan taşınmazlar."),
     ("Yapı ve ruhsat", "Ruhsat, iskân, yapı tatil tutanağı, yıkım kararı ve imar para cezalarına itiraz."),
     ("Yabancılara taşınmaz satışı", "Yabancı alıcı ve satıcılar için hukuki inceleme, tapu işlemleri, vatandaşlık ve ikamet bağlantılı alımlar."),
     ("Alım-satım danışmanlığı", "Satın almadan önce tapu, imar ve şerh incelemesi, satış vaadi ve kapora sözleşmeleri.")],
    "Bilmeniz gerekenler.",
    [("Uzlaşma teklifini hemen imzalamayın", "İdare kamulaştırmadan önce malikle uzlaşma görüşmesi yapar. Teklif edilen bedel kabul edilmezse idare bedelin mahkemece belirlenmesi için dava açar. Teklifi kabul etmeden önce taşınmazın gerçek değerini ve emsal satışları inceleyin."),
     ("Kamulaştırma işlemine karşı otuz gün", "Kamulaştırma işleminin kendisine, yani kamu yararı kararına ve işlemin hukuka uygunluğuna karşı tebliğden itibaren otuz gün içinde idare mahkemesinde iptal davası açılabilir. Bedel ise adli yargıda tartışılır."),
     ("İmar planına karşı altmış gün", "Onaylanan imar planları bir ay askıya çıkarılır ve bu sürede belediyeye itiraz edilebilir. Plana karşı iptal davası ise ilan tarihinden itibaren altmış gün içinde idare mahkemesinde açılır."),
     ("Satış vaadi noterde yapılmalı", "Taşınmaz satış vaadi sözleşmesi noterde düzenleme şeklinde yapılmazsa geçersizdir. Elden imzalanan bir kapora belgesi mülkiyet hakkı vermez; çoğu zaman yalnızca ödenen paranın iadesi istenebilir."),
     ("Yabancılar için sınırlar ve şartlar", "Yabancı gerçek kişiler ülke genelinde otuz hektara kadar taşınmaz edinebilir; askeri ve güvenlik bölgelerinde edinim yasaktır. Vatandaşlık ya da ikamet amaçlı alımlarda değerleme raporu, ödeme şekli ve taşınmazın bulunduğu mahallenin durumu önceden kontrol edilmelidir.")],
    [("İdare arazime yol geçirdi ama kamulaştırma yapmadı.", "Kamulaştırma yapılmadan fiilen el atılan taşınmazlar için bedel ya da el atmanın önlenmesi istenebilir. El atmanın tarihi ve şekli hangi yolun açık olduğunu belirler; önce tapu kaydı ve haritalar incelenir."),
     ("Kamulaştırma bedeli düşük, ne yapabilirim?", "Uzlaşma teklifini kabul etmek zorunda değilsiniz. İdarenin açtığı bedel tespiti davasında keşif ve bilirkişi incelemesi yapılır; emsal satışlarla gerçek değer savunulur."),
     ("Arsam imar planında park alanına ayrıldı.", "Kamu alanına ayrılan ve uzun süre kamulaştırılmayan taşınmazlar için idareye başvurularak kamulaştırma ya da plan değişikliği istenebilir; olumsuz cevaba karşı dava yolu açıktır. Planın onay tarihi ve askı süresi önce kontrol edilir."),
     ("Yabancıyım, Antalya'da daire almak istiyorum.", "Satın almadan önce tapu kaydı, imar durumu, iskân ve borç şerhleri incelenmelidir. Vatandaşlık ya da ikamet planlıyorsanız şartlar ayrıca kontrol edilir. Tapu işlemlerinde yeminli tercüman bulunur; vekâletle de işlem yapılabilir."),
     ("Kapora verdim, satıcı vazgeçti.", "Noterde yapılmamış bir satış vaadi geçersiz olduğu için satışın zorla yaptırılması istenemez; ancak ödenen kapora ve uğranılan zarar istenebilir. Kapora belgesindeki ifadeler ve ödeme kaydı belirleyicidir."),
     ("Belediye binama yıkım kararı verdi.", "Yapı tatil tutanağı, yıkım kararı ve imar para cezalarına karşı itiraz ve dava süreleri kısadır. Tebligatı aldığınız gün belgeyi bize getirin.")],
    "Antalya, yabancılara en çok taşınmaz satılan illerin başında geliyor; Kepez ve çevresinde ise yol, kanal ve imar planı değişiklikleri birçok arsa sahibini kamulaştırma süreciyle karşı karşıya bırakıyor. Bu dosyalarda hem tapu müdürlüğüyle hem belediye ve idareyle yazışmaları biz yürütürüz.",
    "Bir tebligat, bir teklif ya da bir alım: önce kayıtlara bakalım.", "Kamulaştırma, imar hukuku ve gayrimenkul alım-satım danışmanlığı",
    docs=("İdari süreçlerde tebliğ tarihi her şeydir. Zarfları atmayın.",
          [("Tebligat ve zarfı", "Kamulaştırma kararı, uzlaşma daveti, yıkım ya da ceza kararı; tebliğ tarihiyle birlikte."),
           ("Tapu kaydı", "Güncel kayıt, şerh ve beyanlarla birlikte."),
           ("İmar durumu", "Belediyeden alınan imar durumu belgesi ve plan notları."),
           ("Harita ve fotoğraflar", "El atılan bölümü gösteren kroki ve tarihli fotoğraflar."),
           ("Satış belgeleri", "Kapora belgesi, satış vaadi, ödeme dekontları."),
           ("Kimlik ve pasaport", "Yabancı alıcılar için pasaport ve yeminli tercümesi; vergi numarası.")]),
    re_sub=True)

area_page(
    "icra-hukuku", "interior-logo.webp",
    "Antalya İcra Avukatı: İcra Takibi ve Ödeme Emrine İtiraz | Kozanoğlu Hukuk",
    "Antalya ve Kepez'de icra hukuku: ilamlı ve ilamsız takip, çek ve senede dayalı takip, haciz, ödeme emrine itiraz, itirazın iptali, ipotekli takip ve ihalenin feshi. (0242) 244 54 20.",
    "Çalışma alanı · İcra hukuku", "İcra hukuku.",
    "Alacağını tahsil edemeyen alacaklı ya da kapısına ödeme emri gelen borçlu. İki tarafta da ilk soru aynı: süre ne zaman doluyor?",
    "İcra dosyalarında üstlendiğimiz işler.",
    "İcra hukukunda süreler günlerle ölçülür. Bir ödeme emrini ya da haciz tutanağını birkaç gün bekletmek, itiraz hakkını tamamen kaybettirebilir.",
    [("İlamsız icra takibi", "Fatura, sözleşme ya da yazılı belgeye dayanan para alacakları için takip."),
     ("Çek ve senede dayalı takip", "Kambiyo senetlerine özgü hızlı takip yolu ve karşılıksız çek dosyaları."),
     ("İlamlı takip", "Mahkeme kararlarının ve kira tahliye ilamlarının icra yoluyla yerine getirilmesi."),
     ("İpotek ve rehin", "İpotekli taşınmazlar için rehnin paraya çevrilmesi yoluyla takip ve bu takiplere itiraz."),
     ("Haciz ve satış", "Taşınır, taşınmaz, maaş ve banka hesabı haczi; ihale süreci ve ihalenin feshi."),
     ("Borçlu tarafında itiraz", "Ödeme emrine, borca ve imzaya itiraz; menfi tespit ve istirdat davaları.")],
    "Kaçırılmaması gereken süreler.",
    [("Ödeme emrine itiraz için yedi gün", "İlamsız takipte ödeme emrine tebliğden itibaren yedi gün içinde itiraz edilebilir. Çek ve senede dayalı takiplerde bu süre beş gündür. Süre geçerse takip kesinleşir ve haciz aşamasına geçilir."),
     ("İtirazın iptali için bir yıl", "Borçlu itiraz ettiyse takip durur. Alacaklı, itirazın tebliğinden itibaren bir yıl içinde itirazın iptali davası açabilir; elinde imzalı bir belge varsa altı ay içinde icra mahkemesinden itirazın kaldırılmasını isteyebilir."),
     ("Ticari alacaklarda önce arabulucu", "Ticari bir para alacağı için itirazın iptali davası açılacaksa, dava öncesinde arabulucuya başvurmak zorunludur."),
     ("İhalenin feshi için yedi gün", "Haczedilen bir malın ihalesinde usulsüzlük varsa, ihaleyi öğrenmeden itibaren yedi gün, her halde ihaleden itibaren bir yıl içinde icra mahkemesinden ihalenin feshi istenebilir."),
     ("Maaşın dörtte biri", "Maaş haczinde, borçlu ayrıca rıza göstermedikçe uygulamada maaşın dörtte biri kesilir. Birden fazla haciz varsa sıraya konur. Nafaka alacaklarında bu sınır uygulanmaz.")],
    [("Alacağım için icra takibi mi açmalıyım, dava mı?", "Elinizde fatura, imzalı belge ya da çek varsa çoğu zaman icra takibiyle başlanır. Borçlu itiraz ederse itirazın iptali davası ve öncesinde, ticari alacaklarda, arabuluculuk gündeme gelir."),
     ("Bana gelen ödeme emrindeki borcu tanımıyorum.", "Süresi içinde borca itiraz edin; itiraz edilmeyen takip kesinleşir. Takip kesinleştikten sonra borcun olmadığını ancak menfi tespit ya da istirdat davasıyla ileri sürebilirsiniz."),
     ("Maaşıma haciz geldi, ne kadarı kesilebilir?", "Siz ayrıca muvafakat vermedikçe uygulamada maaşın dörtte biri kesilir. Birden fazla haciz varsa sıraya konur; biri bitmeden diğeri başlamaz."),
     ("Oturduğum ev haczedilebilir mi?", "Borçlunun haline uygun konutu kural olarak haczedilemez; ancak ev ipotekliyse ya da borç o evin alımından kaynaklanıyorsa bu koruma uygulanmaz. Haczedilmezlik şikâyeti için süre kısadır."),
     ("Senedin altındaki imza bana ait değil.", "Kambiyo senedine dayalı takipte imzaya itiraz, ödeme emrinin tebliğinden itibaren beş gün içinde icra mahkemesine yapılır. İtiraz haksız çıkarsa para cezası söz konusu olabileceği için önce belgeyi birlikte inceleyelim."),
     ("Evim icradan düşük bedelle satıldı.", "İhalede usulsüzlük varsa, örneğin satış ilanı tebliğ edilmediyse ya da değer yanlış belirlendiyse, ihalenin feshi istenebilir. Süre ihaleyi öğrenmeden itibaren yedi gündür.")],
    "Takip, itiraz ve haciz işlemlerinin çoğunu UYAP üzerinden yürütürüz. Çoğu adım için icra dairesine ya da adliyeye gitmeniz gerekmez; size düşen, tebligatı aldığınız gün bizi aramak.",
    "Bir ödeme emri mi geldi? Süre dolmadan arayın.", "İcra ve iflas hukuku",
    docs=("İcra dosyalarında ilk baktığımız şey tarihtir: tebligatın geldiği gün, senedin vadesi, haczin yapıldığı gün.",
          [("Ödeme emri ve zarfı", "Tebliğ tarihi zarfın üzerindedir; itiraz süresi o günden sayılır."),
           ("Senet, çek, fatura", "Alacağın ya da borcun dayandığı belgenin aslı ya da okunaklı fotoğrafı."),
           ("Sözleşme ve yazışmalar", "Borcun kaynağını gösteren sözleşme, e-posta ve mesajlar."),
           ("Ödeme kayıtları", "Yapılmış ödemeleri gösteren dekontlar ve makbuzlar."),
           ("Haciz tutanağı", "Haciz yapıldıysa size bırakılan tutanak."),
           ("Tapu ve ipotek belgeleri", "İpotekli takiplerde tapu kaydı ve ipotek akit tablosu.")]))

# ---------------------------------------------------------------- Çalışma alanları hub
path = "/calisma-alanlari"
t = "Çalışma Alanları | Kozanoğlu Hukuk Bürosu Kepez, Antalya"
d = "Kozanoğlu Hukuk Bürosu'nun ana çalışma alanı gayrimenkul ve taşınmaz hukuku: tapu iptal ve tescil, ortaklığın giderilmesi, kat karşılığı inşaat, kira, kamulaştırma ve imar. Ayrıca icra hukuku."
body = "\n".join([
    hero("footer-table.webp", "Çalışma alanları", "Ağırlığımız taşınmaz dosyalarında.", "Büromuzun ana çalışma alanı gayrimenkul ve taşınmaz hukuku. Tapu, hisse, inşaat, kira, kamulaştırma ve imar dosyalarının yanında icra dosyalarını da üstleniyoruz."),
    f'''    <section class="section">
      {head("Ana alan", "Gayrimenkul ve taşınmaz hukuku.", "Dört başlıkta topladığımız taşınmaz dosyaları. Her başlığın kendi sayfasında kaçırılmaması gereken süreler, sık sorulan sorular ve getirmeniz gereken belgeler var.")}
      {area_rows(items=[RE_HUB] + RE_AREAS)}
    </section>''',
    f'''    <section class="section alt">
      {head("Ayrıca", "İcra hukuku.", "Alacak takibi, ödeme emrine itiraz ve haciz işlemleri. Konunuzun hangi başlığa girdiğinden emin değilseniz arayın, telefonda söyleriz.")}
      {area_rows(items=OTHER_AREAS)}
    </section>''',
    f'''    <section class="section">
      {head("Ortak nokta", "Her dosyada aynı ilk adım.")}
      <div class="steps"><article class="step"><span>01 · Dinlemek</span><h3>Olayı baştan anlatın</h3><p>Ne oldu, ne zaman oldu, kimler var. Kesin tarih bilmiyorsanız yaklaşık dönem de yeter.</p></article><article class="step"><span>02 · Kayıt</span><h3>Elinizdekileri getirin</h3><p>Tapu kaydı, sözleşme, tebligat, mesaj kayıtları. Önemsiz görünen bir kâğıt bazen dosyanın yönünü değiştirir.</p></article><article class="step"><span>03 · Yol</span><h3>Seçenekleri konuşalım</h3><p>Dava, arabuluculuk, ihtarname ya da beklemek. Her birinin süresini ve masrafını açıkça söyleriz.</p></article></div>
    </section>''',
    cta("Taşınmazınızla ilgili bir sorun mu var? Önce arayın."),
])
write("calisma-alanlari.html", page(path, t, d, "footer-table.webp",
      [webpage(path, "CollectionPage", t, d), crumbs(("Çalışma Alanları", path)),
       {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + h, "name": n} for i, (h, n, _) in enumerate(AREAS)]}], body))

# ---------------------------------------------------------------- Kepez / Varsak
path = "/kepez-varsak-avukat"
t = "Kepez ve Varsak Avukat | Kozanoğlu Hukuk Bürosu, Emek Mah."
d = "Kepez Emek Mahallesi'nde gayrimenkul ağırlıklı hukuk bürosu. Varsak ve Kepez'de hisseli tapu, ortaklığın giderilmesi, kat karşılığı inşaat, site yönetimi, kira ve kamulaştırma dosyaları."
faqs = [
    ("Ofise gelmeden dosyamı size verebilir miyim?", "İlk değerlendirmeyi telefonda başlatabiliriz. Dosyayı üstlenmemiz için herhangi bir noterden avukat adına vekaletname çıkarmanız yeterlidir; bunun için ofise gelmeniz şart değildir."),
    ("Kepez'deki davalar hangi adliyede görülür?", "Kepez ve Varsak'ı ilgilendiren davaların ve icra işlemlerinin büyük bölümü Muratpaşa Meltem'deki Antalya Adliyesi'nde yürür."),
    ("Duruşmalara benim de gitmem gerekir mi?", "Çoğu duruşmaya ve keşfe vekil olarak biz katılırız. Kanunun ya da mahkemenin bizzat katılımınızı istediği durumlarda size önceden haber veririz."),
    ("Görüşme için randevu gerekiyor mu?", "Evet. Gelmeden önce (0242) 244 54 20 numarasını arayın, görüşme için uygun bir saat belirleyelim."),
]
hoods = ["Emek", "Varsak Karşıyaka", "Varsak Esentepe", "Varsak Menderes", "Altıayak", "Teomanpaşa", "Fabrikalar", "Odabaşı", "Kepez'in diğer mahalleleri"]
hood_html = "".join(f"<li>{h}</li>" for h in hoods)
body = "\n".join([
    hero("mobile-hero.webp", "Bölge rehberi", "Kepez ve Varsak: büro, adliye, mahalleler.", "Taşınmazınızın davası nerede görülür, bu bölgede hangi tapu ve inşaat sorunları sık çıkar, bize nasıl ulaşırsınız. Kısa ve pratik."),
    f'''    <section class="section">
      <div class="section-head"><p class="section-label">Büro ve adliye</p><div><h2>Duruşmaya biz gideriz.</h2><p class="section-intro">Kepez ve Varsak'taki taşınmazlarla ilgili davaların ve icra takiplerinin büyük bölümü Muratpaşa Meltem'deki Antalya Adliyesi'nde yürür. Duruşmalara, keşiflere ve bilirkişi incelemelerine biz gideriz. Dosyadaki her hareketi UYAP üzerinden takip eder, size bildiririz.</p></div></div>
      <div class="split-facts"><div><span>Ofis</span><strong>Emek Mah. Yeşilırmak Cd. No:19/2, 07030 Kepez / Antalya</strong><a class="text-link" href="{MAP}" target="_blank" rel="noopener noreferrer">Google Haritalar'da açın ↗</a></div><div><span>Adliye</span><strong>Antalya Adliyesi, Meltem Mah. Dumlupınar Blv., Muratpaşa</strong><p>Kepez'deki hukuk, ceza ve icra dosyalarının görüldüğü yer.</p></div><div><span>Telefon</span><strong>{TEL_TXT}</strong><a class="text-link" href="tel:{TEL}">Arayın ↗</a></div></div>
    </section>''',
    f'''    <section class="section alt">
      {head("Sık çıkan konular", "Eski tapular, yeni siteler.", "Bölgeden gelen dosyaların çoğu bir taşınmaza dokunuyor: kuşaklardır bölünmemiş tarlalar, yükselen siteler ve kiracı ile ev sahibi.")}
      <div class="cards"><article class="card"><span class="number">01</span><h3>Hisseli tapular</h3><p>Varsak 2008'e kadar ayrı bir belediyeydi. Eski tapu kayıtları, miras kalan hisseli tarlalar ve ortaklığın giderilmesi bu yüzden sık gündeme gelir. <a class="inline-link" href="/tapu-iptali-ortakligin-giderilmesi">Ayrıntılar</a></p></article><article class="card"><span class="number">02</span><h3>Kat karşılığı inşaat ve siteler</h3><p>Geç teslim, iskân sorunları, ayıplı daireler, aidat ve ortak alan uyuşmazlıkları. <a class="inline-link" href="/kat-karsiligi-insaat">Ayrıntılar</a></p></article><article class="card"><span class="number">03</span><h3>Kira ve tahliye</h3><p>Kira artışı, kira tespiti ve tahliye. Dava açmadan önce zorunlu arabuluculuk aşaması. <a class="inline-link" href="/kira-hukuku">Ayrıntılar</a></p></article></div>
    </section>''',
    f'''    <section class="section">
      {head("Mahalleler", "Dosyalar en çok buradan geliyor.", "Antalya'nın diğer ilçelerindeki dosyaları da üstleniyoruz.")}
      <ul class="hood-list">{hood_html}</ul>
    </section>''',
    f'''    <section class="section alt">
      {head("Çalışma alanları", "Konuya göre sayfalar.")}
      {area_rows(items=[RE_HUB] + RE_AREAS + OTHER_AREAS)}
    </section>''',
    faq_html(faqs),
    cta("Önce arayın, sonra gelin.", sub="Randevuyla, sizi bekletmeden görüşelim."),
])
write("kepez-varsak-avukat.html", page(path, t, d, "mobile-hero.webp",
      [webpage(path, "WebPage", t, d), crumbs(("Kepez ve Varsak", path)), faq_ld(faqs)], body))

# ---------------------------------------------------------------- Hakkımızda
path = "/hakkimizda"
t = "Hakkımızda | Kozanoğlu Hukuk Bürosu, Kepez Antalya"
d = "Kepez Emek Mahallesi'ndeki ofisimizde Av. Osman Kozanoğlu, Av. Hüseyin Kozanoğlu ve Av. Havva Beyza Kozanoğlu Oya çalışıyor. Ağırlıklı olarak gayrimenkul ve taşınmaz hukukuna bakıyoruz."
body = "\n".join([
    hero("rear-entrance.webp", "Hakkımızda", "Taşınmaz dosyalarına odaklanan bir büro.", "Kozanoğlu Hukuk Bürosu'nda üç avukat çalışıyor. Ağırlıklı olarak gayrimenkul ve taşınmaz hukukuna bakıyor, icra dosyalarını da üstleniyoruz."),
    f'''    <section class="section">
      {head("Nasıl çalışırız", "Önce dinleriz, sonra konuşuruz.", "Hukuki bir sorunla gelen çoğu kişi neyi soracağını bilmez. Bu çok normal. İlk görüşmede olayı sizden dinler, tapu kaydına ve belgelere birlikte bakar, tarihleri çıkarırız.")}
      <div class="story-grid"><img src="/assets/meeting-room.webp" width="1440" height="804" loading="lazy" decoding="async" alt="Kozanoğlu Hukuk Bürosu görüşme odası, Kepez"><div class="story-copy"><p class="quote">Ne yapılabileceğini de, ne yapılamayacağını da açıkça söyleriz.</p><p>Her dosya davayla bitmez. Bazı taşınmaz uyuşmazlıkları bir ihtarnameyle, bazıları arabuluculuk masasında, bazıları da hissedarlar arasında bir protokolle çözülür. Hangi yolun daha az masraflı, hangisinin daha uzun süreceğini görüşmede konuşuruz.</p><p>Dosya açıldıktan sonra duruşma ve keşif tarihlerini, bilirkişi raporlarını ve karşı tarafın dilekçelerini size biz iletiriz. Bir gelişmeyi öğrenmek için peşimizden koşmanız gerekmez.</p></div></div>
    </section>''',
    f'''    <section class="section alt">
      {head("Alışkanlıklar", "Büroda değişmeyen üç şey.")}
      <div class="cards"><article class="card"><span class="number">01</span><h3>Sade dil</h3><p>Dilekçede ne yazdığını, kararın ne anlama geldiğini hukuk terimlerine boğmadan anlatırız.</p></article><article class="card"><span class="number">02</span><h3>Gerçekçi beklenti</h3><p>Sonuç vaadi vermeyiz. Riskleri, olası süreleri ve masrafları baştan konuşuruz.</p></article><article class="card"><span class="number">03</span><h3>Sonuna kadar takip</h3><p>Duruşma, keşif, rapor, tebligat. Karar tapuya işlenene kadar gelişmeleri gecikmeden size iletiriz.</p></article></div>
    </section>''',
    f'''    <section class="section">
      {head("Ekip", "Aynı masada üç avukat.", "Telefonu açan da, duruşmaya giren de bu ekipten biri.")}
      <div class="people" aria-label="Kozanoğlu Hukuk Bürosu ekibi"><article class="person"><span class="initials">OK</span><h3>Osman Kozanoğlu</h3><p>Avukat</p></article><article class="person"><span class="initials">HK</span><h3>Hüseyin Kozanoğlu</h3><p>Avukat</p></article><article class="person"><span class="initials">HO</span><h3>Havva Beyza Kozanoğlu Oya</h3><p>Avukat</p></article></div>
    </section>''',
    f'''    <section class="section alt">
      {head("İlk görüşme", "İlk görüşme nasıl geçer?")}
      <div class="steps"><article class="step"><span>01 · Telefon</span><h3>Arayın</h3><p>Konuyu bir iki cümleyle anlatmanız yeterli. Görüşme için ofiste bir saat belirleriz.</p></article><article class="step"><span>02 · Belgeler</span><h3>Elinizdekini getirin</h3><p>Tapu kaydı, sözleşme, tebligat, mesaj kayıtları. Hepsi işe yarar.</p></article><article class="step"><span>03 · Yol</span><h3>Seçenekleri konuşalım</h3><p>Dava, arabuluculuk, ihtarname ya da beklemek. Süreleri ve masrafları birlikte değerlendiririz.</p></article></div>
    </section>''',
    faq_html([
        ("Avukatlık ücreti nasıl belirlenir?", "Ücret, işe başlamadan önce yazılı bir sözleşmeyle belirlenir. Türkiye Barolar Birliği her yıl bir asgari ücret tarifesi yayımlar; avukatlar bu tarifenin altında ücret kararlaştıramaz."),
        ("Ücret dışında hangi masraflar çıkar?", "Harç, tebligat, bilirkişi ve keşif giderleri avukatlık ücretinden ayrıdır ve mahkeme veznesine yatırılır. Dosyanın türüne göre tahmini tutarı görüşmede söyleriz."),
        ("Avukat tutacak durumum yoksa ne yapabilirim?", "Antalya Barosu'nun adli yardım bürosuna başvurabilirsiniz. Mahkemeden ayrıca harç ve masraflar için adli yardım talep edilebilir."),
    ], label="Ücret ve masraf", h2="Para konusu baştan konuşulur."),
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
d = "Kozanoğlu Hukuk Bürosu: Emek Mah. Yeşilırmak Cd. No:19/2, 07030 Kepez / Antalya. Telefon (0242) 244 54 20, e-posta avkozanoglu@hotmail.com. Görüşme için arayın, ofiste bir saat belirleyelim."
body = "\n".join([
    hero("meeting-room.webp", "İletişim", "Arayın, bir saat belirleyelim.", f"{TEL_TXT} numaralı telefondan ya da {MAIL} adresinden bize ulaşabilirsiniz. Ofisimiz Kepez Emek Mahallesi'nde, Yeşilırmak Caddesi No:19/2'de."),
    f'''    <section class="section">
      <div class="contact-layout"><div><p class="section-label">İlk görüşme</p><h2>Doğrudan ulaşın.</h2><p class="section-intro">Aradığınızda adınızı ve konuyu bir iki cümleyle söylemeniz yeterli. Bir taşınmazla ilgiliyse, görüşmeye güncel tapu kaydını ve elinizdeki sözleşmeleri getirin.</p></div><div class="contact-panel contact-card"><div class="contact-panel-head"><p class="section-label">İletişim bilgileri</p><p>Telefon, e-posta ve adres.</p></div><div class="contact-list"><div class="contact-item"><span class="contact-index">01</span><div class="contact-value"><span>Telefon</span><strong>{TEL_TXT}</strong></div><a class="contact-action" href="tel:{TEL}"><span>Arayın</span><span aria-hidden="true">↗</span></a></div><div class="contact-item"><span class="contact-index">02</span><div class="contact-value"><span>Adres</span><strong>Emek Mah. Yeşilırmak Cd. No:19/2, 07030 Kepez / Antalya</strong></div><a class="contact-action" href="{MAP}" target="_blank" rel="noopener noreferrer"><span>Yol tarifi</span><span aria-hidden="true">↗</span></a></div><div class="contact-item"><span class="contact-index">03</span><div class="contact-value"><span>E-posta</span><strong>{MAIL}</strong></div><a class="contact-action" href="mailto:{MAIL}"><span>Yazın</span><span aria-hidden="true">↗</span></a></div><div class="contact-item"><span class="contact-index">04</span><div class="contact-value"><span>Görüşme</span><strong>Ofiste, randevuyla</strong></div><a class="contact-action" href="/kepez-varsak-avukat"><span>Bölge</span><span aria-hidden="true">↗</span></a></div></div><p class="contact-note">Telefonda yapılan ön görüşme, avukatlık sözleşmesi yerine geçmez. Görüşmede paylaştığınız bilgiler sır saklama yükümlülüğümüz kapsamındadır.</p></div></div>
    </section>''',
    f'''    <section class="section alt">
      {head("Nasıl ilerler", "Telefondan dosyaya üç adım.")}
      <div class="steps"><article class="step"><span>01 · Arama</span><h3>Konuyu kısaca anlatın</h3><p>Telefonda konuyu ve acil bir süre olup olmadığını konuşuruz. Tebligat geldiyse tarihini not edin.</p></article><article class="step"><span>02 · Görüşme</span><h3>Ofiste buluşalım</h3><p>Belgeleri birlikte inceler, seçenekleri, süreleri ve masrafları konuşuruz.</p></article><article class="step"><span>03 · Vekalet</span><h3>Dosya açılır</h3><p>Devam etmeye karar verirseniz noterden vekaletname çıkarılır ve dosyanın takibine başlarız.</p></article></div>
    </section>''',
    f'''    <section class="section">
      {head("Çalışma alanları", "Hangi konuda arıyorsunuz?")}
      {area_rows(items=[RE_HUB] + RE_AREAS + OTHER_AREAS)}
    </section>''',
    cta("Telefon açmak çoğu zaman en kısa yoldur."),
])
write("iletisim.html", page(path, t, d, "meeting-room.webp", [webpage(path, "ContactPage", t, d), crumbs(("İletişim", path))], body))

# 404
path = "/404"; t = "Sayfa bulunamadı | Kozanoğlu Hukuk Bürosu"; d = "Aradığınız sayfa taşınmış ya da hiç olmamış olabilir."
body = hero("meeting-room.webp", "404", "Bu sayfayı bulamadık.", "Adres değişmiş ya da yanlış yazılmış olabilir. Aşağıdaki başlıklardan devam edebilir ya da büroyu arayabilirsiniz.") + f"""
    <section class="section">
      {head("Devam edin", "Aradığınız şey burada olabilir.")}
      {area_rows()}
      <p class="section-intro" style="margin-top:40px"><a class="inline-link" href="/">Ana sayfa</a> · <a class="inline-link" href="/blog">Hukuk notları</a> · <a class="inline-link" href="/iletisim">İletişim ve yol tarifi</a></p>
    </section>"""
out404 = page(path, t, d, "meeting-room.webp", [], body).replace('content="index,follow,max-image-preview:large,max-snippet:-1"', 'content="noindex,follow"').replace(f'<link rel="canonical" href="{SITE}/404">', "")
write("404.html", out404)
print("ok")
