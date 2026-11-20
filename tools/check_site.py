#!/usr/bin/env python3
"""Offline release check: internal links, bilingual content, public contact links and PDFs."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import re
import fitz
import sys

root = Path(__file__).resolve().parents[1]
cvdir = root / 'assets' / 'cv'
allowed = {'https://antoniohernandezpinto.com/', 'https://www.linkedin.com/in/antonio-hernandez-pinto/'}
email_re = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
issues = []

for p in root.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.html', '.md', '.js', '.css', '.py', '.xml', '.txt'}:
        content = p.read_text(encoding='utf-8')
        if email_re.search(content):
            issues.append(f'{p.relative_to(root)}: contains an email address')

for page in (root / 'index.html', root / 'en' / 'index.html'):
    raw = page.read_text(encoding='utf-8')
    soup = BeautifulSoup(raw, 'html.parser')
    if not soup.html or soup.html.get('lang') not in {'es','en'}:
        issues.append(f'{page.relative_to(root)}: missing language')
    for el in soup.select('[href], [src]'):
        key = 'href' if el.has_attr('href') else 'src'
        val = el.get(key,'')
        if val.lower().startswith('mailto:'):
            issues.append(f'{page.relative_to(root)}: mailto link remains')
        if val.startswith(('#', 'https:', 'http:', 'tel:', 'data:')) or not val:
            continue
        resolved = (page.parent / unquote(urlsplit(val).path)).resolve()
        if not resolved.exists():
            issues.append(f'{page.relative_to(root)}: missing local file {val}')
    for el in soup.select('[href^="#"]'):
        if not soup.find(id=el['href'][1:]):
            issues.append(f'{page.relative_to(root)}: broken anchor {el["href"]}')
    contact = soup.find(id='contacto')
    links = [a.get('href') for a in contact.select('a[href]')] if contact else []
    if len(links) != 2 or set(links) != allowed:
        issues.append(f'{page.relative_to(root)}: contact links {links} not the two approved links')
    if 'github.com/' in raw.lower():
        issues.append(f'{page.relative_to(root)}: public GitHub contact remains')
    if len(soup.select('a[download]')) != 4:
        issues.append(f'{page.relative_to(root)}: expected four downloadable resumes')
    if not soup.find('link',rel='canonical'):
        issues.append(f'{page.relative_to(root)}: canonical missing')
    for keyword in ('Telefónica Tech','Thanos','BBVA'):
        if keyword not in raw:
            issues.append(f'{page.relative_to(root)}: expected content {keyword} missing')

cv_files = sorted(cvdir.glob('*.pdf'))
if len(cv_files)!=5:
    issues.append('Expected four bilingual resumes and one legacy compatible PDF')

for path in cv_files:
    d=fitz.open(path)
    extracted=' '.join(p.get_text() for p in d)
    expected_pages = 1 if any(k in path.name for k in ['1pagina','1page']) else 2
    if len(d) != expected_pages:
        issues.append(f'{path.name}: expected {expected_pages} pages, got {len(d)}')
    if email_re.search(extracted):
        issues.append(f'{path.name}: email text remains')
    for k in ('Telefónica Tech','BBVA','2026','2007','2019','Playwright', 'antoniohernandezpinto.com'):
        if k not in extracted: issues.append(f'{path.name}: missing {k}')
    urls=set()
    for pg in d:
        for link in pg.get_links():
            if link.get('uri'): urls.add(link['uri'])
    if urls != allowed:
        issues.append(f'{path.name}: unapproved or missing PDF URLs: {urls}')
    binary = path.read_bytes().lower()
    if b'mailto:' in binary:
        issues.append(f'{path.name}: unapproved contact link in raw PDF')
    print(f'OK {path.name}: {len(d)} page(s), approved URLs only')

for issue in issues:
    print('FAIL',issue)
if issues:
    sys.exit(1)
print('PASS - No email addresses in source or PDF text; correct HTML links, PDFs and chronology.')
