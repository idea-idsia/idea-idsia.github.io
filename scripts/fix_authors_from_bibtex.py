#!/usr/bin/env python3
from pathlib import Path
import re

PUB_DIR = Path(__file__).resolve().parents[1] / '_publications'

bib_block_re = re.compile(r'```bibtex\n(.*?)\n```', re.S)
author_field_re = re.compile(r'author\s*=\s*(\{.*?\}|\".*?\"|[^,\n]+)', re.S)


def unescape_latex(s: str) -> str:
    # handle patterns like {\\' {c}} -> ć, {\\v{c}} -> č, {\\"{o}} -> ö, etc.
    mapping = {
        ("'", 'a'): 'á', ("'", 'e'): 'é', ("'", 'i'): 'í', ("'", 'o'): 'ó', ("'", 'u'): 'ú', ("'", 'c'): 'ć',
        ('`', 'a'): 'à', ('"', 'o'): 'ö', ('"', 'u'): 'ü', ('"', 'a'): 'ä', ('v', 'c'): 'č', ('v', 's'): 'š', ('v', 'z'): 'ž'
    }

    # replace nested brace pattern {\\'\{x\}} or {\\"\{x\}} etc.
    def repl_nested(m):
        acc = m.group(1)
        letter = m.group(2)
        return mapping.get((acc, letter), letter)

    s = re.sub(r"\{\\([`'\\\"v])\{([A-Za-z])\}\}\", repl_nested, s)
    # also handle simpler patterns like \\'c or \\'{c}
    s = re.sub(r"\\([`'\\\"v])\{?([A-Za-z])\}?", lambda m: mapping.get((m.group(1), m.group(2)), m.group(2)), s)
    # remove remaining braces
    s = s.replace('{', '').replace('}', '')
    return s

def normalize_name(name):
    name = name.strip()
    # unescape LaTeX accents and remove braces
    name = unescape_latex(name)
    # remove any remaining enclosing braces
    if name.startswith('{') and name.endswith('}'):
        name = name[1:-1]
    # handle 'Last, First' or 'First Last'
    if ',' in name:
        parts = [p.strip() for p in name.split(',')]
        if len(parts) >= 2:
            return parts[1] + ' ' + parts[0]
    return name

fixed = 0
for md in sorted(PUB_DIR.glob('*.md')):
    txt = md.read_text(encoding='utf-8')
    m = bib_block_re.search(txt)
    if not m:
        continue
    bib = m.group(1)
    ma = author_field_re.search(bib)
    if not ma:
        continue
    author_raw = ma.group(1).strip()
    if author_raw.startswith('{') and author_raw.endswith('}'):
        author_raw = author_raw[1:-1]
    if author_raw.startswith('"') and author_raw.endswith('"'):
        author_raw = author_raw[1:-1]
    # split on ' and ' but avoid 'And' in names (bibtex uses ' and ')
    parts = re.split(r'\s+and\s+', author_raw)
    names = [normalize_name(p) for p in parts if p.strip()]

    # build new authors block
    authors_block = 'authors:\n'
    for n in names:
        authors_block += f'  - {n}\n'

    # replace authors block inside YAML front matter (between first '---' markers)
    if txt.strip().startswith('---'):
        parts = txt.split('---', 2)
        if len(parts) >= 3:
            pre = '---'
            fm = parts[1]
            post = parts[2]
            # remove any existing authors block in front matter
            fm_new, subs = re.subn(r'(?ms)^authors:\n(?:[ \t\-].*?\n)+', authors_block, fm)
            if subs == 0:
                # if no authors present, insert after title line if possible
                if 'title:' in fm:
                    fm_new = re.sub(r'(title:.*?\n)', r"\1" + authors_block, fm, count=1)
                else:
                    fm_new = authors_block + fm
            new_txt = pre + fm_new + '---' + post
            md.write_text(new_txt, encoding='utf-8')
            fixed += 1

print(f'Fixed {fixed} files in {PUB_DIR}')
