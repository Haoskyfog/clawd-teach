#!/usr/bin/env python3
"""Static sanity check for a clawd-teach deck.

usage: python3 check_deck.py path/to/deck.html

Catches the mistakes that are easy to make when editing the single-file deck:
slide ids without a Clawd script, step counts that don't line up, missing
canvas ids, leftover 【placeholders】, and Swiss-style violations (rounded
corners, shadows, gradients, serif fonts, tiny text, off-palette colours).
It also prints advisory QUALITY warnings for the patterns that make a deck
dull: copy-pasted or static canvas scenes, one layout repeated everywhere,
generic kickers, unused template components and a uniform Clawd.
Exit code 1 if any ERROR, 0 otherwise (WARNs are advisory).
"""
import difflib
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
    cl_entries = {}
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
            cl_entries[km.group(1)] = re.findall(r'\{[^{}]*\}', seg)

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

    quality(js, markup, ids, bodies, cl_entries, warns)

    print(f'slides: {len(ids)}  ->  ' + ' · '.join(ids))
    for e in errs:
        print('ERROR', e)
    for w in warns:
        print('WARN ', w)
    if not errs and not warns:
        print('OK — no issues found')
    return 1 if errs else 0


MOTION = re.compile(r'\blerp\(|\bease\(|Math\.(sin|cos|exp|pow|hypot|atan2)|\bclock\b|\bnow\b|mulberry\(')


def quality(js, markup, ids, bodies, cl_entries, warns):
    """Advisory checks for decks that are valid but dull."""
    q = lambda msg: warns.append('QUALITY ' + msg)

    # -- canvas scenes: copy-pasted or static
    scenes = {m.group(1): m.group(2) for m in
              re.finditer(r'^SC\.(\w+)=(.*?)\}\)\(\);', js, re.M | re.S)}

    def norm(sid, body):
        b = body.replace(sid, 'ID')
        b = re.sub(r'''\'(?:[^'\\]|\\.)*\'|"(?:[^"\\]|\\.)*"|`[^`]*`''', 'S', b)
        b = re.sub(r'\b\d+(\.\d+)?\b|\.\d+', 'N', b)
        return re.sub(r'\s+', '', b)

    keys = list(scenes)
    normed = {k: norm(k, scenes[k]) for k in keys}
    dup = set()
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if difflib.SequenceMatcher(None, normed[a], normed[b], autojunk=False).ratio() > .85:
                dup |= {a, b}
    if dup:
        q(f'scenes {sorted(dup)} are near-identical code: each idea needs its own hand-written scene (references/patterns.md §4)')
    for k in keys:
        if not MOTION.search(scenes[k]):
            q(f'SC.{k} uses no interpolation (lerp/ease), maths or clock: it probably just places text in boxes. Pick a pattern from references/patterns.md')
    if len(ids) >= 10 and len(keys) < 3:
        q(f'{len(ids)} slides but only {len(keys)} canvas scenes: core concepts should move')
    if keys and 'class="seg"' not in markup:
        q('no .seg control anywhere: give at least one scene a parameter or A/B switch to play with in class')

    # -- layouts: one skeleton repeated
    sig = {}
    for sid in ids:
        classes = re.findall(r'class="([^"]+)"', bodies[sid])
        sig.setdefault(' '.join(classes), []).append(sid)
    for s, group in sig.items():
        if len(group) >= 4:
            q(f'{len(group)} slides share one identical layout skeleton {group}: vary layouts (template library: hook, concept, demo, cards, divider, summary, road)')

    # -- kickers: generic labels reused
    kick = {}
    for m in re.finditer(r'class="k"[^>]*>(.*?)</div>', markup, re.S):
        txt = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if txt and '【' not in txt:
            kick[txt] = kick.get(txt, 0) + 1
    for txt, n in kick.items():
        if n >= 3:
            q(f'kicker "{txt}" used {n} times: kickers should name the content')

    # -- template components left unused
    if len(ids) >= 6:
        if 'class="strike"' not in markup:
            q('no hook strike-through joke (template slide "hook")')
        if 'data-hl=' not in markup:
            q('no highlighted summary sentence (template slide "summary", data-hl)')
        if 'class="road"' not in markup:
            q('no roadmap (template slide "road")')
    if len(ids) >= 10 and len(re.findall(r'<section class="slide split"', markup)) < 2:
        q('no section divider: add a split divider every 4–6 slides')

    # -- Clawd: uniform staging
    entries = [e for es in cl_entries.values() for e in es]
    perch_x = {re.search(r'x:([\d.]+)', e).group(1) for e in entries if 'perch:1' in e and re.search(r'x:([\d.]+)', e)}
    if sum('perch:1' in e for e in entries) >= 8 and len(perch_x) <= 1:
        q('Clawd perches at the same x on every slide: let it walk a few vw between steps')
    if len(cl_entries) >= 6 and not any("'sweaty'" in e for e in entries):
        q("Clawd never sweats: use mood:'sweaty' on the hard steps")
    lasts = [es[-1] for es in cl_entries.values() if es]
    same = sum("act:'jump'" in e and "mood:'happy'" in e for e in lasts)
    if len(lasts) >= 6 and same / len(lasts) >= .7:
        q(f"{same}/{len(lasts)} slides end with jump + happy: save the jump for the real aha steps")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
