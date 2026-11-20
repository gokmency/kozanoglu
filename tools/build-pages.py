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
    "employee": [{"@type": "Person", "name": n, "jobTitle": t} for n, t in [("Osman Kozanoğlu", "Avukat"), ("Hüseyin Kozanoğlu", "Avukat"), ("Havva Beyza Kozanoğlu Oya", "Avukat")]],
}

NAV = [("/hakkimizda", "Hakkımızda", None), ("/blog", "Blog", None), ("/iletisim", "İletişim", None)]
LAWYERS = ["Osman Kozanoğlu", "Hüseyin Kozanoğlu", "Havva Beyza Kozanoğlu Oya"]
ADDR = "Emek Mah. Yeşilırmak Cd. No:19/2, 07030 Kepez / Antalya"


def e(s):
    return html.escape(s, quote=True)

def nav(current):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{h}"{cur if h == current else ""}>' + (f'<span class="l-full">{t}</span><span class="l-short">{s}</span>' if s else t) + "</a>"
        for h, t, s in NAV)
    return f'<nav class="site-nav" aria-label="Ana navigasyon"><a class="brand" href="/" aria-label="Kozanoğlu Hukuk Bürosu ana sayfa"><img src="/assets/logo.webp" width="724" height="543" fetchpriority="high" alt="Kozanoğlu Hukuk Bürosu"></a><div class="nav-links">{links}</div><a class="nav-call" href="tel:{TEL}" aria-label="Büro telefonu: {TEL_TXT}">{TEL_TXT}</a></nav>'

def footer():
    people = "".join(f'<span style="color:rgba(241,238,231,.72);font-size:14px">Av. {n}</span>' for n in LAWYERS)
    return f'''<footer class="site-footer">
    <div class="footer-grid">
      <div><p class="footer-title">Kozanoğlu Hukuk Bürosu</p><address>Emek Mah. Yeşilırmak Cd. No:19/2<br>07030 Kepez / Antalya</address><div class="footer-contact"><div><a class="footer-tel" href="tel:{TEL}">{TEL_TXT}</a></div><div><a class="footer-mail" href="mailto:{MAIL}">{MAIL}</a></div></div></div>
      <nav aria-label="Site"><p class="footer-title">Büro</p><a href="/hakkimizda">Hakkımızda</a><a href="/blog">Hukuk notları</a><a href="/iletisim">İletişim ve yol tarifi</a></nav>
      <div style="display:grid;align-content:start;gap:10px"><p class="footer-title">Avukatlar</p>{people}</div>
    </div>
    <p class="footer-legal">Bu sitedeki içerikler genel bilgilendirme amaçlıdır, hukuki görüş yerine geçmez.</p>
    <div class="footer-row"><span>© 2026 Kozanoğlu Hukuk Bürosu · Kepez, Antalya</span><a href="/iletisim">Emek Mah. Yeşilırmak Cd. No:19/2</a><a href="tel:{TEL}">{TEL_TXT}</a></div>
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
  <a class="call-fab" href="tel:{TEL}" aria-label="Büro telefonu: {TEL_TXT}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>Telefon</a>
</body>
</html>
'''

def crumbs(*items):
    lst = [("Ana Sayfa", SITE + "/")] + [(n, SITE + p) for n, p in items]
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(lst)]}

def webpage(path, kind, name, desc):
    return {"@type": kind, "@id": SITE + path + "#webpage", "url": SITE + path, "name": name, "description": desc, "about": {"@id": ORG_ID}, "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "tr-TR"}

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

def contact_strip():
    return f'''    <section class="cta"><div><h2>İletişim.</h2><p>Kozanoğlu Hukuk Bürosu · {ADDR}</p></div><a class="button" href="tel:{TEL}">{TEL_TXT} ↗</a></section>'''

def link_rows(items):
    rows = "".join(f'<a class="area-row" href="{h}"><span class="area-index">{i:02d}</span><span class="area-text"><strong>{t}</strong><span>{d}</span></span><span class="area-arrow" aria-hidden="true">↗</span></a>' for i, (h, t, d) in enumerate(items, 1))
    return f'<div class="area-list">{rows}</div>'

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

# ---------------------------------------------------------------- Blog
import re as _re
BLOG_DATE = "2026-11-04"
NEW_DATE = "2026-11-10"
D3 = "2026-11-14"
D4 = "2026-11-16"
POSTS = [
    # slug, md, kategori, görsel, görsel alt, [tarih]
    ("mirasin-reddi-ve-uc-aylik-sure", "reddi-miras.md", "Miras", "blog-reddi-miras", "Taş bir avluda zeytin ağacı gölgesinde duran eski bir anahtar ve kapalı bir dosya", "2026-11-19"),
    ("bosanmada-evin-paylasimi", "bosanma-ev.md", "Aile", "blog-bosanma-ev", "Traverten masa üzerinde duran ev anahtarı, zeytin dalı ve bir dosya", "2026-11-18"),
    ("ortakligin-giderilmesi-izale-i-suyu-davasi", "izale-i-suyu.md", "Tapu", "blog-izale-i-suyu", "Ceviz bir masada katlanmış bir kadastro haritası, pirinç bir pergel ve yan yana duran iki anahtar", D4),
    ("ayipli-konut-ve-eksik-imalat-davasi", "ayipli-konut.md", "İnşaat", "blog-ayipli-konut", "Yeni yapılmış aydınlık bir odada meşe parke zeminde su terazisi ve mimari proje rulosu", D4),
    ("tahliye-taahhutnamesi-gecerlilik-sartlari", "tahliye-taahhutnamesi.md", "Kira", "blog-tahliye-taahhutnamesi", "Travertin masa üzerinde boş bir kâğıt, pirinç dolma kalem ve bir daire anahtarı", D4),
    ("apartman-ve-site-yonetiminde-aidat-ve-karar-iptali", "site-yonetimi.md", "Kat mülkiyeti", "blog-site-yonetimi", "Zeytin ve narenciye ağaçlarıyla çevrili bir konut sitesinin taş avlusu ve posta kutuları", D4),
    ("imar-planinda-park-veya-yesil-alana-ayrilan-arsa", "imar-plani.md", "İmar", "blog-imar-plani", "Ahşap masa üzerinde açık duran renkli bir imar planı paftası, büyüteç ve ölçek cetveli", D4),
    ("kiraci-kirasini-odemezse-tahliye-sureci", "kira-borcu.md", "Kira", "blog-kira-borcu", "Ceviz bir daire kapısının eşiğinde paspasın yanında duran kapalı bir zarf", D4),
    ("iskan-alinmayan-binada-kat-mulkiyeti", "iskan.md", "İnşaat", "blog-iskan", "Yeni tamamlanmış bir apartmanın gün ışığı alan travertin taşlı giriş holü", D4),
    ("yapi-tatil-tutanagi-yikim-karari-ve-imar-para-cezasi", "yikim-imar-cezasi.md", "İmar", "blog-yikim-imar-cezasi", "Gün batımında tuğla duvarları örülmüş kaba inşaat hâlindeki bir bina ve şerit çekilmiş şantiye girişi", D4),
    ("kadastro-tespitine-itiraz-ve-zilyetlik", "kadastro-zilyetlik.md", "Tapu", "blog-kadastro-zilyetlik", "Zeytin ağaçları ve dağlar önünde duran eski taş kadastro sınır işareti", D4),
    ("ev-haczi-ipotekli-takip-ve-ihalenin-feshi", "ev-haczi-ihale.md", "İcra", "blog-ev-haczi-ihale", "Ceviz bir çalışma masasında bordo deri dosya, pirinç mühür ve küçük bir pirinç ev maketi", D4),
    ("tapu-iptal-ve-tescil-davasi", "tapu-iptal.md", "Tapu", "blog-tapu-iptal", "Ceviz bir masada kapalı eski bir defter, dolma kalem ve pirinç bir anahtar", D3),
    ("kat-karsiligi-insaat-sozlesmesi", "kat-karsiligi.md", "İnşaat", "blog-kat-karsiligi", "Gün batımında iskeleli, kaba inşaat hâlindeki bir apartman ve bir kule vinç", D3),
    ("kamulastirma-bedeli-itiraz", "kamulastirma.md", "Kamulaştırma", "blog-kamulastirma", "Zeytinlik tepelerin arasından kıvrılarak geçen yeni bir asfalt yol", D3),
    ("muris-muvazaasi-davasi", "muris.md", "Miras", "blog-muris", "Eski bir köy evinin taş pencere pervazında duran demir bir anahtar", D3),
    ("ev-alirken-kapora-ve-satis-vaadi", "kapora.md", "Alım-satım", "blog-kapora", "Boş ve aydınlık bir dairede travertin tezgâh üzerinde pirinç bir anahtar ve kapalı bir zarf", D3),
    ("muteahhit-daireyi-gec-teslim-ederse", "gec-teslim.md", "İnşaat", "blog-gec-teslim", "Yeni yapılmış boş bir odada pencerenin yanındaki duvarda ince bir çatlak", D3),
    ("hisseli-tapuda-onalim-hakki", "onalim.md", "Tapu", "blog-onalim", "Alçak bir kuru taş duvarla bölünmüş zeytinli bir tarla", D3),
    ("kamulastirmasiz-el-atma", "el-atma.md", "Kamulaştırma", "blog-el-atma", "Bir bahçenin taş sınır duvarını kesip geçen dar bir yol", D3),
    ("ecrimisil-nedir", "ecrimisil.md", "Tapu", "blog-ecrimisil", "Taş bir bahçe duvarında eski bir asma kilitle kapatılmış ahşap kapı", D3),
    ("yabancilara-konut-satisi", "yabanci.md", "Alım-satım", "blog-yabanci", "Denize ve dağlara bakan sakin bir balkon ve iki boş sandalye", D3),
    ("ev-sahibi-kiraciyi-nasil-cikarir", "tahliye.md", "Kira", "blog-tahliye", "Boş bir odada açık kapının yanında üst üste duran koliler ve üzerinde bir anahtar", NEW_DATE),
    ("kira-artisi-ve-kira-tespit-davasi", "kira.md", "Kira", "blog-kira", "Travertin bir rafın üzerinde pirinç ev anahtarları ve katlanmış boş bir kâğıt"),
    ("odeme-emri-geldi", "odeme.md", "İcra", "blog-odeme", "Travertin bir yüzeyde üst üste duran zarflar ve pirinç bir mektup açacağı"),
    ("miras-kalan-tasinmaz", "miras.md", "Miras", "blog-miras", "Önünde yaşlı bir zeytin ağacı olan eski taş bir köy evi"),
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
for slug, md, cat, img, alt, *rest in POSTS:
    date = rest[0] if rest else BLOG_DATE
    title, summary, tldr, sections, faqs = parse_md(os.path.join(OUT, "content", "blog", md))
    parsed.append(dict(date=date, slug=slug, cat=cat, img=img, alt=alt, title=title, summary=summary, tldr=tldr, sections=sections, faqs=faqs, mins=max(3, round(words(sections, tldr, faqs) / 200))))

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
      <aside class="post-aside"><div class="post-toc"><p class="section-label">Bu yazıda</p><ol>{toc}</ol></div></aside>
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
    </section>'''
    desc = p["summary"][:300]
    ttl = p["title"]
    graph = [webpage(path, "WebPage", ttl, desc),
             {"@type": "BlogPosting", "@id": SITE + path + "#article", "headline": p["title"], "description": desc, "image": SITE + f"/assets/blog/{p['img']}.webp", "datePublished": p["date"], "dateModified": p["date"], "inLanguage": "tr-TR", "articleSection": p["cat"], "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "mainEntityOfPage": {"@id": SITE + path + "#webpage"}},
             crumbs(("Hukuk Notları", "/blog"), (p["title"], path))]
    html_out = page(path, ttl, desc, f"blog/{p['img']}.webp", graph, body, og_img=f"/assets/blog/{p['img']}-og.jpg", og_type="article")
    write(os.path.join("blog", p["slug"] + ".html"), html_out)

# blog index
path = "/blog"
t = "Hukuki Bilgilendirme Yazıları | Kozanoğlu Hukuk Bürosu"
d = "Kozanoğlu Hukuk Bürosu'nun mevzuat ve uygulamaya ilişkin genel bilgilendirme yazıları."
feat, rest = parsed[0], parsed[1:]
cards = "".join(f'<a class="post-card" href="/blog/{o["slug"]}"><img src="/assets/blog/{o["img"]}-card.webp" width="800" height="450" loading="lazy" decoding="async" alt="{e(o["alt"])}"><span class="post-meta"><span>{o["cat"]}</span><span>{o["mins"]} dk.</span></span><h2>{_inline(o["title"])}</h2><p>{_inline(o["summary"])}</p><span class="read">Yazıyı okuyun ↗</span></a>' for o in rest)
body = "\n".join([
    hero("interior-logo.webp", "Hukuk notları", "Hukuki bilgilendirme yazıları.", "Mevzuat ve uygulamaya ilişkin genel bilgilendirme yazıları. Yazılarda ilgili kanun maddeleri, süreler ve örnekler yer alır; hukuki görüş niteliği taşımaz."),
    f'''    <section class="section">
      <a class="post-feature" href="/blog/{feat["slug"]}"><img src="/assets/blog/{feat["img"]}.webp" width="1376" height="768" loading="lazy" decoding="async" alt="{e(feat["alt"])}"><div><span class="post-meta"><span>{feat["cat"]}</span><span>{feat["mins"]} dk.</span></span><h2>{_inline(feat["title"])}</h2><p>{_inline(feat["summary"])}</p><span class="read">Yazıyı okuyun ↗</span></div></a>
      <div class="blog-grid">{cards}</div>
    </section>''',
])
blog_graph = [webpage(path, "CollectionPage", t, d), crumbs(("Hukuk Notları", path)),
              {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/blog/" + o["slug"], "name": o["title"]} for i, o in enumerate(parsed)]}]
write("blog.html", page(path, t, d, "interior-logo.webp", blog_graph, body))

# ---------------------------------------------------------------- Hakkımızda
LAWYERS_TXT = "Av. Osman Kozanoğlu, Av. Hüseyin Kozanoğlu ve Av. Havva Beyza Kozanoğlu Oya"
path = "/hakkimizda"
t = "Hakkımızda | Kozanoğlu Hukuk Bürosu – Kepez, Antalya"
d = f"Kozanoğlu Hukuk Bürosu, {ADDR}. Büroda {LAWYERS_TXT} çalışmaktadır."
AREAS = ["Gayrimenkul ve taşınmaz hukuku", "Tapu iptal ve tescil, ortaklığın giderilmesi", "Kat karşılığı inşaat ve kat mülkiyeti", "Kira hukuku", "Kamulaştırma ve imar hukuku", "Yabancıların taşınmaz edinimi", "Miras hukuku", "İcra ve iflas hukuku"]
people = "".join(f'<article class="person"><span class="initials">{"".join(w[0] for w in (n.split()[0], n.split()[-1]))}</span><h3>{n}</h3><p>Avukat</p></article>' for n in LAWYERS)
body = "\n".join([
    hero("rear-entrance.webp", "Hakkımızda", "Kozanoğlu Hukuk Bürosu.", f"Büroda {LAWYERS_TXT} çalışmaktadır. Büro, Kepez ilçesi Emek Mahallesi'ndedir."),
    f'''    <section class="section">
      {head("Büro", "Büro bilgisi.", "Kozanoğlu Hukuk Bürosu, Kepez ilçesi Emek Mahallesi'nde, Yeşilırmak Caddesi No:19/2 adresinde bulunmaktadır.")}
      <div class="story-grid"><img src="/assets/meeting-room.webp" width="1440" height="804" loading="lazy" decoding="async" alt="Kozanoğlu Hukuk Bürosu görüşme odası"><div class="story-copy"><p class="quote">Emek Mahallesi, Kepez.</p><p>Görüşmeler büroda, randevu ile yapılır.</p><p>Avukatlık hizmeti; 1136 sayılı Avukatlık Kanunu, Türkiye Barolar Birliği Meslek Kuralları ve ilgili mevzuat çerçevesinde yürütülür.</p><p>Bu sitedeki yazılar genel bilgilendirme amaçlıdır ve hukuki görüş niteliği taşımaz.</p></div></div>
    </section>''',
    f'''    <section class="section alt">
      {head("Faaliyet alanları", "Büronun faaliyet gösterdiği alanlar.", "Bu liste, büronun faaliyet gösterdiği alanlar hakkında bilgi vermek amacıyla yer almaktadır; uzmanlık anlamına gelmez.")}
      <ul class="hood-list">{"".join(f"<li>{a}</li>" for a in AREAS)}</ul>
    </section>''',
    f'''    <section class="section">
      {head("Avukatlar", "Büroda çalışan avukatlar.")}
      <div class="people" aria-label="Kozanoğlu Hukuk Bürosu avukatları">{people}</div>
    </section>''',
    f'''    <section class="section alt">
      {head("Adres", "Büro adresi.")}
      <div class="location-block"><img src="/assets/rear-entrance.webp" width="1440" height="804" loading="lazy" decoding="async" alt="Kozanoğlu Hukuk Bürosu girişi, Yeşilırmak Caddesi Kepez"><div class="location-copy"><div><p class="section-label">Kozanoğlu Hukuk Bürosu</p><h3>Adres ve harita.</h3><address>Emek Mah. Yeşilırmak Cd. No:19/2<br>07030 Kepez / Antalya</address></div><a class="location-link" href="{MAP}" target="_blank" rel="noopener noreferrer"><span>Haritada açın</span><span aria-hidden="true">↗</span></a></div></div>
    </section>''',
    contact_strip(),
])
write("hakkimizda.html", page(path, t, d, "rear-entrance.webp", [webpage(path, "AboutPage", t, d), crumbs(("Hakkımızda", path))], body))

# ---------------------------------------------------------------- İletişim
path = "/iletisim"
t = "İletişim | Kozanoğlu Hukuk Bürosu – Kepez, Antalya"
d = f"Kozanoğlu Hukuk Bürosu: {ADDR}. Telefon {TEL_TXT}, e-posta {MAIL}."
body = "\n".join([
    hero("meeting-room.webp", "İletişim", "İletişim bilgileri.", f"Telefon: {TEL_TXT} · E-posta: {MAIL} · Adres: {ADDR}."),
    f'''    <section class="section">
      <div class="contact-layout"><div><p class="section-label">Büro</p><h2>Kozanoğlu Hukuk Bürosu.</h2><p class="section-intro">Büronun adres, telefon ve e-posta bilgileri yanda yer almaktadır. Görüşmeler büroda, randevu ile yapılır.</p></div><div class="contact-panel contact-card"><div class="contact-panel-head"><p class="section-label">İletişim bilgileri</p><p>Telefon, e-posta ve adres.</p></div><div class="contact-list"><div class="contact-item"><span class="contact-index">01</span><div class="contact-value"><span>Telefon</span><strong>{TEL_TXT}</strong></div><a class="contact-action" href="tel:{TEL}"><span>Ara</span><span aria-hidden="true">↗</span></a></div><div class="contact-item"><span class="contact-index">02</span><div class="contact-value"><span>Adres</span><strong>{ADDR}</strong></div><a class="contact-action" href="{MAP}" target="_blank" rel="noopener noreferrer"><span>Harita</span><span aria-hidden="true">↗</span></a></div><div class="contact-item"><span class="contact-index">03</span><div class="contact-value"><span>E-posta</span><strong>{MAIL}</strong></div><a class="contact-action" href="mailto:{MAIL}"><span>E-posta</span><span aria-hidden="true">↗</span></a></div><div class="contact-item"><span class="contact-index">04</span><div class="contact-value"><span>Avukatlar</span><strong>{LAWYERS_TXT}</strong></div><a class="contact-action" href="/hakkimizda"><span>Hakkımızda</span><span aria-hidden="true">↗</span></a></div></div><p class="contact-note">Telefonda yapılan ön görüşme, avukatlık sözleşmesi yerine geçmez. Görüşmede paylaştığınız bilgiler sır saklama yükümlülüğümüz kapsamındadır.</p></div></div>
    </section>''',
    contact_strip(),
])
write("iletisim.html", page(path, t, d, "meeting-room.webp", [webpage(path, "ContactPage", t, d), crumbs(("İletişim", path))], body))

# 404
SITE_PAGES = [("/", "Ana sayfa", "Kozanoğlu Hukuk Bürosu"), ("/hakkimizda", "Hakkımızda", "Büro bilgisi ve avukatlar"), ("/blog", "Hukuk notları", "Genel bilgilendirme yazıları"), ("/iletisim", "İletişim", "Adres, telefon, e-posta ve harita")]
path = "/404"; t = "Sayfa bulunamadı | Kozanoğlu Hukuk Bürosu"; d = "Aradığınız sayfa taşınmış ya da kaldırılmış olabilir."
body = hero("meeting-room.webp", "404", "Bu sayfayı bulamadık.", "Adres değişmiş, sayfa kaldırılmış ya da yanlış yazılmış olabilir. Aşağıdaki sayfalardan devam edebilirsiniz.") + f"""
    <section class="section">
      {head("Devam edin", "Site sayfaları.")}
      {link_rows(SITE_PAGES)}
    </section>"""
out404 = page(path, t, d, "meeting-room.webp", [], body).replace('content="index,follow,max-image-preview:large,max-snippet:-1"', 'content="noindex,follow"').replace(f'<link rel="canonical" href="{SITE}/404">', "")
write("404.html", out404)
print("ok")
