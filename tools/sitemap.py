import sys,glob,os
root=sys.argv[1]
pri={"/":"1.0","/gayrimenkul-hukuku":"0.95","/tapu-iptali-ortakligin-giderilmesi":"0.9","/kat-karsiligi-insaat":"0.9","/kira-hukuku":"0.9","/kamulastirma-imar":"0.9","/calisma-alanlari":"0.8","/icra-hukuku":"0.7","/kepez-varsak-avukat":"0.9","/blog":"0.8","/iletisim":"0.8","/hakkimizda":"0.7"}
OLD={"/blog/"+x for x in ("anlasmali-bosanma-rehberi","ifadeye-cagrildiniz","isten-cikarildim-haklarim","kira-artisi-ve-kira-tespit-davasi","miras-kalan-tasinmaz","odeme-emri-geldi")}
urls=list(pri)+sorted("/blog/"+os.path.basename(f)[:-5] for f in glob.glob(os.path.join(root,"blog","*.html")))
x='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f'  <url>\n    <loc>https://kozanogluhukuk.com{u}</loc>\n    <lastmod>{"2026-11-04" if u in OLD else "2026-11-13"}</lastmod>\n    <priority>{pri.get(u,"0.7")}</priority>\n  </url>\n' for u in urls)+'</urlset>\n'
open(os.path.join(root,'sitemap.xml'),'w').write(x); print(len(urls),'urls')
