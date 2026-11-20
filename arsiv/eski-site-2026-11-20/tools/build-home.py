# Ana sayfa üretici: tools/home/{style.css,body.html,script.js} + mevcut <head> meta/JSON-LD -> index.html
# Kullanım (repo kökünde): python3 -I tools/build-home.py
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "tools", "home")
rd = lambda p: open(p, encoding="utf-8").read()
def mincss(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    return "\n".join(l.strip() for l in s.splitlines() if l.strip())
def minjs(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    return "\n".join(l.strip() for l in s.splitlines() if l.strip())
head = rd(os.path.join(H, "head.html")).rstrip()
out = f"{head}\n  <style>\n{mincss(rd(os.path.join(H, 'style.css')))}\n  </style>\n</head>\n{rd(os.path.join(H, 'body.html')).rstrip()}\n  <script>\n{minjs(rd(os.path.join(H, 'script.js')))}\n  </script>\n</body>\n</html>\n"
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print("index.html", len(out.encode()), "bytes")
