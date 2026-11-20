import sys,glob,os
root=sys.argv[1]
pri={"/":"1.0","/hakkimizda":"0.8","/iletisim":"0.8","/blog":"0.8"}
LASTMOD="2026-11-20"
urls=list(pri)+sorted("/blog/"+os.path.basename(f)[:-5] for f in glob.glob(os.path.join(root,"blog","*.html")))
x='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f'  <url>\n    <loc>https://kozanogluhukuk.com{u}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n    <priority>{pri.get(u,"0.7")}</priority>\n  </url>\n' for u in urls)+'</urlset>\n'
open(os.path.join(root,'sitemap.xml'),'w').write(x); print(len(urls),'urls')
