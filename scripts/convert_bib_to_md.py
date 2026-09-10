#!/usr/bin/env python3
import re
import os
from pathlib import Path

BIB_PATH = Path('/Users/sandra.mitrovic/Downloads/works.bib')
OUT_DIR = Path(__file__).resolve().parents[1] / '_publications'

text = BIB_PATH.read_text(encoding='utf-8')

# Find entries by parsing braces to handle nested braces robustly
entries = []
idx = 0
while True:
    m = re.search(r'@', text[idx:])
    if not m:
        break
    start = idx + m.start()
    # find the first '{' after start
    brace_pos = text.find('{', start)
    if brace_pos == -1:
        break
    # now find matching closing brace
    depth = 0
    i = brace_pos
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                end = i
                break
        i += 1
    entry_text = text[start:end+1]
    entries.append(entry_text.strip())
    idx = end+1

print(f'Found {len(entries)} entries')

field_re = re.compile(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"(?:[^\"])*\"|[^,}\n]+)", re.S)

os.makedirs(OUT_DIR, exist_ok=True)

for entry in entries:
    # get type and key
    m = re.match(r'@(\w+)\s*\{\s*([^,\s]+)\s*,', entry, re.S)
    if not m:
        print('Skip malformed entry:', entry[:80])
        continue
    entry_type = m.group(1).lower()
    key = m.group(2).strip()
    fields = dict()
    for fm in field_re.finditer(entry):
        k = fm.group(1).lower()
        v = fm.group(2).strip()
        if v.startswith('{') and v.endswith('}'):
            v = v[1:-1]
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        v = v.replace('\n', ' ').strip()
        fields[k] = v
    # prepare front matter
    title = fields.get('title', '')
    authors_raw = fields.get('author', '')
    authors = []
    if authors_raw:
        # split on ' and ' (bibtex separator)
        parts = re.split(r'\s+ and \s+', authors_raw)
        for p in parts:
            p = p.strip()
            # if in form Last, First
            if ',' in p:
                comps = [c.strip() for c in p.split(',')]
                if len(comps) >= 2:
                    name = comps[1] + ' ' + comps[0]
                else:
                    name = p
            else:
                name = p
            authors.append(name)
    venue = fields.get('journal') or fields.get('booktitle') or fields.get('publisher') or ''
    year = fields.get('year','')
    doi = fields.get('doi','')
    url = fields.get('url','')
    arxiv = fields.get('arxiv','')
    abstract = fields.get('abstract','')

    # type heuristics
    if 'journal' in fields:
        ptype = 'journal'
    elif 'booktitle' in fields or entry_type in ('inproceedings','incollection','inbook'):
        ptype = 'conference'
    elif entry_type == 'article' and 'journal' not in fields:
        ptype = 'article'
    else:
        ptype = entry_type

    # filename from key
    fname = re.sub(r'[^a-zA-Z0-9_\-]', '_', key).lower() + '.md'
    out_path = OUT_DIR / fname

    # build markdown
    fm_lines = []
    fm_lines.append('---')
    fm_lines.append('layout: publication')
    fm_lines.append(f'title: "{title.replace("\"","\\\"")}"')
    fm_lines.append('authors:')
    for a in authors:
        fm_lines.append(f'  - {a}')
    fm_lines.append(f'venue: "{venue}"' if venue else 'venue:')
    fm_lines.append(f'year: {year}')
    fm_lines.append(f'type: {ptype}')
    if abstract:
        fm_lines.append('abstract: >')
        # wrap abstract to ~80 chars
        wrapped = re.sub(r'\s+', ' ', abstract).strip()
        fm_lines.append(f'  {wrapped}')
    else:
        fm_lines.append('abstract:')
    fm_lines.append(f'pdf: {url if url.endswith(".pdf") else ""}')
    fm_lines.append('code:')
    fm_lines.append(f'arxiv: {arxiv}')
    fm_lines.append(f'doi: {doi}')
    fm_lines.append('tags:')
    fm_lines.append('  -')
    fm_lines.append('plotly: false')
    fm_lines.append('---')
    fm_lines.append('\n## BibTeX\n')
    fm_lines.append('```bibtex')
    fm_lines.append(entry)
    fm_lines.append('```')

    out_text = '\n'.join(fm_lines)
    out_path.write_text(out_text, encoding='utf-8')
    print('Wrote', out_path)

print('Done')
