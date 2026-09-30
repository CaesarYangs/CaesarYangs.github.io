"""Optional: python3 tests/browser_smoke.py --output /workspace/site-preview."""
import argparse
import json
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright, expect

parser = argparse.ArgumentParser()
parser.add_argument('--base-url', default='http://127.0.0.1:8000')
parser.add_argument('--browser', default='/usr/bin/chromium')
parser.add_argument('--output', default='/tmp/paperbox-preview')
args = parser.parse_args()
out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[1]
base = args.base_url.rstrip('/')

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.browser, headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1050})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(base+'/', wait_until='networkidle')
    expect(page.locator('h1')).to_have_text("Cyrus' Paperbox")
    expect(page.locator('.post-list-item')).to_have_count(4)
    page.screenshot(path=str(out/'simple-home-desktop.png'), full_page=True)
    page.locator('.post-list-item a').first.click()
    expect(page.locator('article > h1')).to_contain_text('雅思备考')
    expect(page.locator('article > h1')).to_have_count(1)
    expect(page.locator('.post-meta')).to_contain_text('June 9, 2023')
    page.screenshot(path=str(out/'simple-article-desktop.png'))
    page.locator('.prose h2 .anchor').first.click()
    assert page.evaluate('Boolean(document.getElementById(decodeURIComponent(location.hash.slice(1))))')
    print('PASS: homepage, post navigation, one post title, metadata, original anchors')
    for width in [320, 390, 768, 1024]:
        page.set_viewport_size({'width': width, 'height': 844})
        for path in ['/', '/blogs/', '/docs/', '/blogs/IELTS_2023/', '/blogs/YOLOv5_HNet/', '/docs/Algo/3-DP/']:
            page.goto(base+quote(path), wait_until='domcontentloaded')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, path)
        if width == 390:
            page.goto(base+'/', wait_until='networkidle')
            page.screenshot(path=str(out/'simple-home-mobile.png'), full_page=True)
            page.goto(base+'/blogs/IELTS_2023/', wait_until='domcontentloaded')
            page.screenshot(path=str(out/'simple-article-mobile.png'))
    print('PASS: 320/390/768/1024px home, archives, long articles and code without overflow')
    context = browser.new_context(java_script_enabled=False)
    plain = context.new_page()
    for path in json.loads((root/'tests/content-baseline.json').read_text()):
        response = plain.goto(base+'/'+quote(path), wait_until='domcontentloaded')
        assert response.status == 200
        expect(plain.locator('article')).to_be_visible()
        expect(plain.locator('.main-nav').get_by_role('link',name='博客',exact=True)).to_be_visible()
    print('PASS: all 17 articles and navigation work without JavaScript')
    page.goto(base+'/docs/Algo/5-Search/',wait_until='domcontentloaded')
    expect(page.locator('.katex-display')).to_have_count(3)
    assert not errors, errors
    print('PASS: formula rendering; no uncaught JavaScript errors')
    browser.close()
print('Screenshots:', out)
