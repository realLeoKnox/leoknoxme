#!/usr/bin/env python3
"""Build the publishable dist/ for leoknox.me (Python stdlib only).

Source HTML is hand-written per language. This script:
  * copies only public files into dist/ (no README, notes or content snapshots),
  * appends content-hash ?v= to CSS/JS references (and the language.mjs import),
  * recomputes the CSP script-src hashes for inline JSON-LD in _headers,
  * regenerates sitemap.xml and robots.txt from BASE.
Run: python3 scripts/build.py
"""
from pathlib import Path
import base64, hashlib, re, shutil

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
# Canonical public origin. The apex leoknox.me 301-redirects here at the Cloudflare zone level.
BASE = 'https://www.leoknox.me/'
PAGES = ['', 'zh-hant/', 'zh-hans/']          # canonical routes (sitemap order)
HTML = ['index.html', 'zh-hant/index.html', 'zh-hans/index.html', '404.html']
PUBLIC = HTML + ['robots.txt', 'sitemap.xml', '_headers', '_redirects']


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10]


def write_generated():
    (ROOT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + ''.join(f'<url><loc>{BASE}{p}</loc></url>' for p in PAGES) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    hashes = []
    for name in HTML:
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', (ROOT / name).read_text(), re.S):
            h = "'sha256-" + base64.b64encode(hashlib.sha256(block.encode()).digest()).decode() + "'"
            if h not in hashes:
                hashes.append(h)
    headers = (ROOT / '_headers').read_text()
    headers = re.sub(r"script-src [^;]+;", "script-src 'self' " + ' '.join(hashes) + ';', headers)
    (ROOT / '_headers').write_text(headers)


def build_dist():
    shutil.rmtree(DIST, ignore_errors=True)
    for name in PUBLIC:
        (DIST / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, DIST / name)
    shutil.copytree(ROOT / 'assets', DIST / 'assets')
    # Version the module import first, so main.js's own hash reflects language.mjs changes.
    main = DIST / 'assets/main.js'
    main.write_text(main.read_text().replace("from './language.mjs'",
                                             f"from './language.mjs?v={digest(DIST / 'assets/language.mjs')}'", 1))

    def version(match):
        attr, ref = match.group(1), match.group(2)
        asset = re.sub(r'^(\.\./|\./|/)+', '', ref)
        return f'{attr}="{ref}?v={digest(DIST / asset)}"'
    for name in HTML:
        page = DIST / name
        page.write_text(re.sub(r'\b(href|src)="((?:\.\./|\./|/)?assets/[^"?#]+\.(?:css|js))"', version, page.read_text()))


if __name__ == '__main__':
    write_generated()
    build_dist()
    print(f'Built dist/ with {len(HTML)} pages for {BASE}')
