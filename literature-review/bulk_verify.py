#!/usr/bin/env python3
"""Bulk-verify a literature-review selection against ADS (the fabrication gate).

Usage: bulk_verify.py SELECTION_FILE OUTDIR

SELECTION_FILE lines (comments with #, blanks ignored):
    key | bibcode | arxiv_id(or -) | category | new/existing
Only rows marked "new" are fetched.

Outputs in OUTDIR:
    new_refs.bib    bibtex for every verified bibcode, keys rewritten to project keys
    abstracts.json  bibcode -> {title, abstract, author, year}
    keymap.json     [{key, bibcode, arxiv, cat, title, year, has_abs}, ...]
Prints missing-bibtex (= likely fabricated/mistyped bibcodes) and missing-abstract lists.

Token: ~/.ads/dev_key or $ADS_DEV_KEY (same as the ads-search skill).
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sel_path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)

    token = None
    keyfile = os.path.expanduser('~/.ads/dev_key')
    if os.path.exists(keyfile):
        token = open(keyfile).read().strip()
    token = token or os.environ.get('ADS_DEV_KEY')
    if not token:
        sys.exit('no ADS token (~/.ads/dev_key or ADS_DEV_KEY)')

    rows = []
    for line in open(sel_path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) != 5:
            continue
        key, bib, arx, cat, status = parts
        if status == 'new':
            rows.append((key, bib, arx, cat))
    print(f'{len(rows)} new entries to fetch')
    bibcodes = [r[1] for r in rows]

    def api(url, payload=None):
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode() if payload else None,
            headers={'Authorization': f'Bearer {token}',
                     'Content-Type': 'application/json'})
        return json.loads(urllib.request.urlopen(req, timeout=120).read())

    # bibtex export (fabrication gate), chunks of 60
    bibtex_all = {}
    for i in range(0, len(bibcodes), 60):
        chunk = bibcodes[i:i + 60]
        res = api('https://api.adsabs.harvard.edu/v1/export/bibtex',
                  {'bibcode': chunk})
        for m in re.finditer(r'@(\w+)\{([^,]+),(.*?)\n\}\n', res['export'], re.S):
            bibtex_all[m.group(2).strip()] = (m.group(1), m.group(3))
        print(f'  export chunk {i // 60}: {len(bibtex_all)} cumulative')

    # abstracts, chunks of 20
    abstracts = {}
    for i in range(0, len(bibcodes), 20):
        chunk = bibcodes[i:i + 20]
        q = ' OR '.join(f'bibcode:{b}' for b in chunk)
        url = ('https://api.adsabs.harvard.edu/v1/search/query?q=' +
               urllib.parse.quote(q) +
               '&fl=bibcode,title,abstract,author,year&rows=25')
        for doc in api(url)['response']['docs']:
            abstracts[doc['bibcode']] = doc
        print(f'  abstract chunk {i // 20}: {len(abstracts)} cumulative')

    missing_bib, missing_abs, out = [], [], []
    for key, bib, arx, cat in rows:
        if bib in bibtex_all:
            typ, body = bibtex_all[bib]
            out.append(f'@{typ}{{{key},{body}\n}}\n')
        else:
            missing_bib.append((key, bib))
        if bib not in abstracts:
            missing_abs.append((key, bib))

    open(os.path.join(outdir, 'new_refs.bib'), 'w').write('\n'.join(out))
    json.dump({r[1]: abstracts.get(r[1]) for r in rows},
              open(os.path.join(outdir, 'abstracts.json'), 'w'), indent=1)
    json.dump([{'key': k, 'bibcode': b, 'arxiv': a, 'cat': c,
                'title': (abstracts.get(b, {}).get('title') or ['?'])[0],
                'year': abstracts.get(b, {}).get('year'),
                'has_abs': bool(abstracts.get(b, {}).get('abstract'))}
               for k, b, a, c in rows],
              open(os.path.join(outdir, 'keymap.json'), 'w'), indent=1)

    print(f'\nbibtex written: {len(out)}; MISSING BIBTEX (verify these!): {missing_bib}')
    print(f'abstract coverage: {len(rows) - len(missing_abs)}/{len(rows)}; '
          'no abstract: ' + ', '.join(k for k, b in missing_abs))


if __name__ == '__main__':
    main()
