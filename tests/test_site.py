"""Run with python3 -m unittest discover -s tests -v (standard library only)."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Article(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.text = []
        self.ids = []
        self.images = []
        self.code = 0
        self.meta_depth = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.meta_depth:
            self.meta_depth += 1
        elif "data-post-meta" in a:
            self.meta_depth = 1
        if tag == 'article': self.inside = True
        if self.inside:
            if 'id' in a: self.ids.append(a['id'])
            if tag == 'img': self.images.append(a.get('src'))
            if tag == 'pre': self.code += 1
    def handle_endtag(self, tag):
        if self.meta_depth: self.meta_depth -= 1
        if tag == 'article': self.inside = False
    def handle_data(self, data):
        if self.inside and not self.meta_depth: self.text.append(data)
    def fingerprint(self):
        return dict(text=hashlib.sha256(' '.join(' '.join(self.text).split()).encode()).hexdigest(), ids=self.ids, images=self.images, code=self.code)

class SiteTest(unittest.TestCase):
    def test_original_article_content_and_anchors_preserved(self):
        baseline = json.loads((ROOT/'tests/content-baseline.json').read_text())
        self.assertEqual(len(baseline), 17)
        for path, expected in baseline.items():
            with self.subTest(path=path):
                p = Article(); p.feed((ROOT/path).read_text())
                self.assertEqual(p.fingerprint(), expected)
    def test_original_routes_preserved(self):
        for path in json.loads((ROOT/'tests/routes-baseline.json').read_text()):
            self.assertTrue((ROOT/path).is_file(), path)
    def test_static_pages_use_shared_readable_shell(self):
        for path in ['index.html', 'blogs/index.html', 'docs/index.html', 'blogs/regex101/index.html']:
            data = (ROOT/path).read_text()
            with self.subTest(path=path):
                self.assertIn('/assets/css/site.css', data)
                self.assertIn('<main', data)
                self.assertNotIn('book.min.', data)
                self.assertIn('href="/blogs/"', data)
    def test_simple_single_column_layout(self):
        for name in ['index.html', 'blogs/index.html', 'blogs/regex101/index.html']:
            data = (ROOT/name).read_text()
            with self.subTest(path=name):
                self.assertNotIn('paper-illustration', data)
                self.assertNotIn('entry-card', data)
                self.assertNotIn('search-dialog', data)
                self.assertNotIn('article-toc', data)

if __name__ == '__main__': unittest.main()
