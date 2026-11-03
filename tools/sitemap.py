import sys,glob,os
root=sys.argv[1]
pri={"/":"1.0","/calisma-alanlari":"0.9","/aile-hukuku":"0.9","/ceza-hukuku":"0.9","/gayrimenkul-kira-miras":"0.9","/is-icra-ticaret":"0.9","/kepez-varsak-avukat":"0.9","/blog":"0.8","/iletisim":"0.8","/hakkimizda":"0.7"}
urls=list(pri)+sorted("/blog/"+os.path.basename(f)[:-5] for f in glob.glob(os.path.join(root,"blog","*.html")))
x='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f'  <url>\n    <loc>https://kozanogluhukuk.com{u}</loc>\n    <lastmod>2026-11-04</lastmod>\n    <priority>{pri.get(u,"0.7")}</priority>\n  </url>\n' for u in urls)+'</urlset>\n'
open(os.path.join(root,'sitemap.xml'),'w').write(x); print(len(urls),'urls')
