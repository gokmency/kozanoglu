#!/bin/bash
# Tüm sayfaları yeniden üretir. Kullanım (repo kökünde): bash tools/build.sh
# Yayın: main'e push -> Cloudflare Workers Builds `npx wrangler deploy` çalıştırır (wrangler.jsonc + .assetsignore).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -I tools/build-home.py
python3 -I tools/build-pages.py .
python3 -I tools/sitemap.py .
