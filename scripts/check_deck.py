#!/usr/bin/env python3
"""Static sanity check for a clawd-teach deck.

usage: python3 check_deck.py path/to/deck.html

Catches the mistakes that are easy to make when editing the single-file deck:
slide ids without a Clawd script, step counts that don't line up, missing
canvas ids, leftover 【placeholders】, and Swiss-style violations (rounded
corners, shadows, gradients, serif fonts, tiny text, off-palette colours).
Exit code 1 if any ERROR, 0 otherwise (WARNs are advisory).
"""
import re
import sys

ALLOWED_HEX = {
    '#d97757', '#b0502c', '#0a0a0a', '#fafaf8', '#f0f0ee', '#d4d4d2', '#737373',
    '#252524', '#525252', '#a3a3a3', '#ffffff', '#fff', '#000', '#000000',
    '#bbb', '#ccc', '#aaa', '#999', '#eee', '#f2b9a3', '#6fb7ff',
}


def main(path):
    html = open(path, encoding='utf-8').read()
    errs, warns = [], []

    m = re.search(r'<script>(.*)</script>', html, re.S)
    js = m.group(1) if m else ''
    markup = html[:m.start()] if m else html
    style = ''.join(re.findall(r'<style>(.*?)</style>', html, re.S))

    # ---- slides
    sec_iter = list(re.finditer(r'<section class="slide[^"]*" data-id="([^"]+)"', markup))
    ids = [s.group(1) for s in sec_iter]
    if not ids:
        errs.append('no <section class="slide" data-id="..."> found')
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errs.append(f'duplicate slide data-id: {sorted(dup)}')
    bodies = {}
    for k, s in enumerate(sec_iter):
        end = sec_iter[k + 1].start() if k + 1 < len(sec_iter) else len(markup)
        bodies[s.group(1)] = markup[s.start():end]

    # ---- Clawd script
    cl_m = re.search(r'const CL=\{(.*?)\n\};', js, re.S)
    cl = {}
    if not cl_m:
        errs.append('const CL={...}; block not found')
    else:
        block = cl_m.group(1)
        keys = list(re.finditer(r'^\s*([A-Za-z_]\w*):\[', block, re.M))
        for k, km in enumerate(keys):
            end = keys[k + 1].start() if k + 1 < len(keys) else len(block)
            seg = block[km.end():end]
            says = re.findall(r"say:'((?:[^'\\]|\\.)*)'", seg)
            cl[km.group(1)] = says

    for sid in ids:
        body = bodies[sid]
        steps = [int(x) for x in re.findall(r'data-(?:s|hl)="(\d+)"', body)]
        mx = max(steps) if steps else 0
        says = cl.get(sid)
        if says is None:
            warns.append(f'[{sid}] no CL entry: Clawd will keep its previous pose/bubble on this slide')
            continue
        if len(says) < mx + 1:
            warns.append(f'[{sid}] content has {mx + 1} steps but CL has {len(says)}: Clawd repeats its last line on later steps')
        if len(says) > mx + 1:
            warns.append(f'[{sid}] CL has {len(says)} entries but content only {mx + 1} steps: extra clicks change only the bubble (fine if a canvas scene uses those steps)')
        for s in says:
            n = len(s)
            if n > 46:
                warns.append(f'[{sid}] bubble line is {n} chars (keep ≤ ~40): {s[:30]}…')
    for k in cl:
        if k not in ids:
            errs.append(f'CL has key "{k}" but no slide with that data-id')

    # ---- scenes
    for k in re.findall(r'^SC\.(\w+)=', js, re.M):
        if k not in ids:
            errs.append(f'SC.{k} defined but no slide with data-id="{k}"')
    dom_ids = set(re.findall(r'\bid="([^"]+)"', markup))
    for ref in sorted(set(re.findall(r"\$\('#([\w-]+)", js))):
        if ref not in dom_ids:
            errs.append(f"script references #{ref} but no element has that id")
    for ref in sorted(set(re.findall(r"\$\$\('#([\w-]+)", js))):
        if ref not in dom_ids:
            errs.append(f"script references #{ref} but no element has that id")

    # ---- placeholders
    ph = re.findall(r'【[^】]{0,30}】', html)
    if ph:
        errs.append(f'{len(ph)} unreplaced 【placeholders】, e.g. {ph[:4]}')

    # ---- Swiss style rules
    all_css = style + ' '.join(re.findall(r'style="([^"]*)"', markup))
    if re.search(r'border-radius\s*:\s*(?!0[;\s"]|0$)', all_css):
        errs.append('border-radius found — Style B uses square corners only')
    if re.search(r'box-shadow|text-shadow', all_css):
        errs.append('shadow found — Style B uses no shadows')
    if re.search(r'(linear|radial|conic)-gradient', all_css + js):
        errs.append('gradient found — Style B uses flat colour only')
    for fam in re.findall(r'font-family\s*:\s*([^;"]+)', all_css):
        if re.search(r'(?<!sans-)serif', fam) or re.search(r'Georgia|Times|Songti|SimSun|宋', fam):
            errs.append(f'serif font-family: {fam.strip()}')
    for px in re.findall(r'font-size\s*:\s*(\d+(?:\.\d+)?)px', all_css):
        if float(px) < 14:
            errs.append(f'font-size {px}px < 14px minimum')
    for hx in set(h.lower() for h in re.findall(r'#[0-9a-fA-F]{3,6}\b', style + markup + js)):
        if len(hx) in (4, 7) and hx not in ALLOWED_HEX:
            warns.append(f'off-palette colour {hx} — Style B has one accent (#D97757) plus greys')

    print(f'slides: {len(ids)}  ->  ' + ' · '.join(ids))
    for e in errs:
        print('ERROR', e)
    for w in warns:
        print('WARN ', w)
    if not errs and not warns:
        print('OK — no issues found')
    return 1 if errs else 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
