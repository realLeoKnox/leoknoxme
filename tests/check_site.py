#!/usr/bin/env python3
"""Checks the built dist/ (run scripts/build.py first)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import base64, hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
BASE = 'https://www.leoknox.me/'
LANGS = {'en': '', 'zh-Hant': 'zh-hant/', 'zh-Hans': 'zh-hans/'}
TG = 'https://t.me/leospmbot'


class Doc(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs = []; self.ids = set(); self.links = []; self.meta = {}; self.lang = None; self.h1 = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'h1': self.h1 += 1
        if tag == 'link': self.links.append(a)
        if tag == 'meta': self.meta[a.get('name') or a.get('property', '')] = a.get('content', '')
        if 'id' in a:
            assert a['id'] not in self.ids, ('duplicate id', a['id']); self.ids.add(a['id'])
        for k in ('href', 'src'):
            if k in a: self.refs.append(a[k])


headers = (DIST / '_headers').read_text()
assert 'Strict-Transport-Security' not in headers  # HSTS comes from the Cloudflare zone setting
pages = [(lang, route, DIST / route / 'index.html') for lang, route in LANGS.items()] + [('en', '404.html', DIST / '404.html')]
count = 0
for lang, route, path in pages:
    src = path.read_text(); d = Doc(); d.feed(src)
    assert d.lang == lang and d.h1 == 1, path
    assert 'https://leoknox.me/' not in src and 'https://leoknox.dev/' not in src, (path, 'apex URL left')
    canonical = next(x['href'] for x in d.links if x.get('rel') == 'canonical')
    assert canonical == BASE + route, (path, canonical)
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
        json.loads(block)
        assert base64.b64encode(hashlib.sha256(block.encode()).digest()).decode() in headers, (path, 'CSP hash')
    assert 'leo@leosoffice.com' in src and TG in src, path
    if route == '404.html':
        assert 'noindex' in d.meta.get('robots', '')
        assert all(r.startswith(('/', '#', 'mailto:', 'https://')) for r in d.refs), '404 refs must be absolute'
    else:
        expected = {l: BASE + p for l, p in LANGS.items()} | {'x-default': BASE}
        assert {x['hreflang']: x['href'] for x in d.links if x.get('rel') == 'alternate'} == expected, path
    for ref in d.refs:
        u = urlsplit(ref)
        if u.scheme or u.netloc: continue
        if not u.path: target = path
        elif u.path.startswith('/'): target = DIST / unquote(u.path).lstrip('/')
        else: target = path.parent / unquote(u.path)
        if target.is_dir(): target = target / 'index.html'
        assert target.exists(), (path, ref)
        if u.fragment:
            other = Doc(); other.feed(target.read_text()); assert u.fragment in other.ids, (path, ref)
        if re.search(r'\.(css|js)$', u.path): assert re.fullmatch(r'v=[0-9a-f]{10}', u.query), (path, ref, 'unversioned')
        count += 1
    print('PASS:', lang, route or '/')
for leaked in ['README.md', 'VALIDATION.md', 'content', 'scripts', 'tests', 'wrangler.jsonc', 'preview.command']:
    assert not (DIST / leaked).exists(), ('not public', leaked)
assert f'{BASE}sitemap.xml' in (DIST / 'robots.txt').read_text()
print(f'PASS: 3 locales + 404, {count} local references, canonical/hreflang on www, CSP hashes, versioned assets, no private files in dist/.')
