# Kozanoğlu alt sayfa üretici (Hakkımızda, İletişim, 404).
# Kullanım (repo kökünde): python3 -I tools/build-pages.py . && python3 -I tools/sitemap.py .
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

NAV = [("/hakkimizda", "Hakkımızda", None), ("/iletisim", "İletişim", None)]
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
      <nav aria-label="Site"><p class="footer-title">Büro</p><a href="/hakkimizda">Hakkımızda</a><a href="/iletisim">İletişim ve yol tarifi</a></nav>
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
      <div class="story-grid"><img src="/assets/meeting-room.webp" width="1440" height="804" loading="lazy" decoding="async" alt="Kozanoğlu Hukuk Bürosu görüşme odası"><div class="story-copy"><p class="quote">Emek Mahallesi, Kepez.</p><p>Görüşmeler büroda, randevu ile yapılır.</p><p>Avukatlık hizmeti; 1136 sayılı Avukatlık Kanunu, Türkiye Barolar Birliği Meslek Kuralları ve ilgili mevzuat çerçevesinde yürütülür.</p><p>Bu sitedeki bilgiler genel bilgilendirme amaçlıdır ve hukuki görüş niteliği taşımaz.</p></div></div>
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
SITE_PAGES = [("/", "Ana sayfa", "Kozanoğlu Hukuk Bürosu"), ("/hakkimizda", "Hakkımızda", "Büro bilgisi ve avukatlar"), ("/iletisim", "İletişim", "Adres, telefon, e-posta ve harita")]
path = "/404"; t = "Sayfa bulunamadı | Kozanoğlu Hukuk Bürosu"; d = "Aradığınız sayfa taşınmış ya da kaldırılmış olabilir."
body = hero("meeting-room.webp", "404", "Bu sayfayı bulamadık.", "Adres değişmiş, sayfa kaldırılmış ya da yanlış yazılmış olabilir. Aşağıdaki sayfalardan devam edebilirsiniz.") + f"""
    <section class="section">
      {head("Devam edin", "Site sayfaları.")}
      {link_rows(SITE_PAGES)}
    </section>"""
out404 = page(path, t, d, "meeting-room.webp", [], body).replace('content="index,follow,max-image-preview:large,max-snippet:-1"', 'content="noindex,follow"').replace(f'<link rel="canonical" href="{SITE}/404">', "")
write("404.html", out404)
print("ok")
