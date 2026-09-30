#!/usr/bin/env python3
"""Check local HTML links, resources, and fragments; no third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for key in ('href', 'src'):
            if key in a: self.refs.append(a[key])


def check():
    pages = {}
    for path in ROOT.rglob('*.html'):
        if any(p.startswith('.') for p in path.relative_to(ROOT).parts): continue
        parser = Links(); parser.feed(path.read_text(encoding='utf-8'))
        pages[path.resolve()] = parser
    errors = []
    total = 0
    for path, parser in pages.items():
        for ref in parser.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc: continue
            total += 1
            if not url.path: target = path
            elif url.path.startswith('/'): target = ROOT/unquote(url.path.lstrip('/'))
            else: target = path.parent/unquote(url.path)
            target = target.resolve()
            if target.is_dir(): target /= 'index.html'
            if not target.exists(): errors.append(f'{path.relative_to(ROOT)}: missing {ref}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(ROOT)}: missing fragment {ref}')
    for css in (ROOT/'assets/css').glob('*.css'):
        for url in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css.read_text()):
            if url.startswith('/') and not (ROOT/url.lstrip('/')).exists(): errors.append(f'{css.name}: missing {url}')
    if errors: raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(pages)} HTML routes, {total} local links/resources and their fragments.')

if __name__ == '__main__': check()
