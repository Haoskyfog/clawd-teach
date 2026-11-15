# Design system: Swiss Style B (as used by clawd-teach)

Everything below already exists in `assets/template.html`. This file explains the
rules and lists the components so you can compose new slides without
re-inventing CSS. Do not restyle the template's tokens: they are the look.

## Contents
1. Non-negotiable rules
2. Tokens
3. Type classes
4. Step reveal system
5. Components (snippets)
6. Slide layouts
7. Fitting at 1024×576 (overflow lessons)

---

## 1. Non-negotiable rules

| Rule | Why |
|---|---|
| Sans-serif only (Inter + Noto Sans SC; mono = JetBrains Mono for labels and numbers) | Swiss style; serif breaks the look instantly |
| **One** accent: `#D97757` (Clawd orange). Everything else is ink, paper or grey | The accent marks "the important thing"; a second hue dilutes it |
| No border-radius, no shadows, no gradients | Flat, square, printed-poster feel |
| Big type is **light** (weight 200–300); emphasis comes from size and colour, not from bold | Bold headlines look like a corporate PPT |
| Minimum sizes: body 18px, caption 16px, meta/mono 14px (all via `max(Npx, …vw)`) | Must stay legible on a projector and at 1024×576 |
| Grid-plus-dot background canvas (`#bg`) that turns orange near the mouse | Part of the signature look; keep it |
| Sizes use `min(Xvw, Yvh)` so slides scale with both width and height | Decks get shown on laptops, projectors and phones |

`scripts/check_deck.py` flags most violations.

## 2. Tokens (CSS variables in `:root`)

```
--paper #fafaf8   --grey-1 #f0f0ee (card bg)   --grey-2 #d4d4d2 (lines)   --grey-3 #737373
--ink #0a0a0a     --text-body #252524   --text-secondary #525252   --text-helper #737373
--accent #D97757  --accent-ink #B0502C (accent text on paper; better contrast)
--ease  cubic-bezier(.22,1,.36,1)      element motion
--ease-page cubic-bezier(.77,0,.175,1) slide transition (1s horizontal translate)
--pop   cubic-bezier(.34,1.56,.64,1)   stamps / badges
```
Canvas colours mirror these in `const C={accent,accentInk,ink,paper,g1,g2,g3}`.

## 3. Type classes

| class | use |
|---|---|
| `.k` | kicker above titles: mono, uppercase, accent-ink, e.g. `Example 02 · 微分 → 速度` |
| `.h1x` | slide title, weight 200, `min(5.8vw,10.2vh)` (shrink inline to `min(4.6vw,8.2vh)` for long titles) |
| `.h2x` | sub-title / title in two-column slides, weight 300 |
| `.h3x` | card titles, one-liners |
| `.giant` | single huge word (`Calculus`) |
| `.p` | body 18px+ |
| `.ps` | secondary body 16px+, weight 500 |
| `.sm-note` | helper note |
| `.mono` `.acc` `.b` | mono font / accent-ink colour / weight 600 |

Chrome bar at the top of every slide:
`<div class="chrome"><span>Part 02 · 章节名</span><span class="pg"></span></div>`.
`.pg` is filled automatically with `04 / 16`. Clawd's *perch* stands on this line.

## 4. Step reveal system

Each click advances one **step** within the slide before moving to the next slide.

| attribute | effect |
|---|---|
| `data-s="k"` | hidden until step k, then fades/slides in (`.on`); gets `.cur` exactly at step k |
| `data-fx="left|right|pop|fade"` | entrance direction / style (default: up 18px) |
| `style="--dl:.2s"` | stagger delay within the same step |
| `data-until="k"` | element leaves after step k (`.gone`); use with `grid-area:1/1` to swap two things in the same spot |
| `data-hl="k"` | `.hl` highlighter sweep turns on at step k |

Step count of a slide = max(highest `data-s`/`data-hl`, `CL[id].length-1`). Canvas
scenes receive the same step number via `setStep`, so a canvas can have more
steps than the DOM (e.g. n = 3 → 8 → 40 segments).

## 5. Components (snippets)

**Cards** — `.card` (grey), `.card-ink` (black, use for "the conclusion"), `.card-acc` (orange, use for "the formula / the answer"; max one per slide).
```html
<div class="card" data-s="1"><div class="k" style="color:var(--text-helper)">Business · 商科</div>
  <div class="h3x" style="margin:.8vh 0">老板最爱的导数</div><p class="ps">…</p></div>
```

**Numbered steps** with an accent bar on the current one:
```html
<ol class="steps-list"><li data-s="1"><span class="n">01</span><span class="p"><b>切</b> 成 8 块 <span class="tag">微分</span></span></li>…</ol>
```

**Readout table** (live numbers written by a canvas scene via `setText`):
```html
<div class="ro"><div class="l">时间间隔 Δt</div><div class="v"><span id="st-dt">5.00</span> s</div>…</div>
```

**Segmented control** for in-class play (buttons must `e.stopPropagation()` — the global click advances slides):
```html
<div class="seg" id="circle-ctl"><span class="lab">切成</span><button data-n="4">4</button>…<button class="go">拼 / 还原</button></div>
```

**Tags / square bullet**: `<span class="tag">微分</span>`, `<span class="tag a">…</span>`, `<span class="sq"></span>`.

**Strike + stamp joke** (hook slides): `.strike-wrap` + `.strike[data-s]` + `.stamp[data-fx=pop]` — see template slide `hook`.

**Cut / join bars** (pure CSS idea illustration): `.bar.cut` / `.bar.join` with 14 `<i style="--j:i">` (join also `--r` random offsets) — see example deck slide `idea`.

**SVG network** (everything connects to the concept): `<svg class="net" data-s="1">` with `<line pathLength="1">` + `.nd` nodes — lines draw in, nodes fade in. See example slide `important`.

**Highlighter sentence** (summary): `<span class="hl" data-hl="1">极限</span>` inside `.sum-text`.

**Roadmap**: `.road` grid of 5 `.node` (`.here` = today, accent top border). Game language: LV.0 新手村 → Boss.

**Rule columns**: `<div class="rule" style="padding-top:1.4vh">` — three short takeaways under a summary.

## 6. Slide layouts

| layout | structure | Clawd |
|---|---|---|
| **split** (cover, section divider) | `section.slide.split` > `.half.acc` 58% + `.half` 42% | big (no perch), stands in the right half, `s:2–2.2` |
| **statement** (hook, concept, summary) | full width `.main`, title + 1–2 content rows | perch, or big in a corner if the slide is sparse |
| **demo** (the core of the deck) | `.main` row: left column 27–31% text + right `flex:1` canvas | perch, x ≈ 38–42 |
| **canvas-wide** | title block on top, canvas `flex:1`, readouts row below | perch |
| **grid** (apps, uses) | 3 columns or 2×2 cards, one card per step | perch |
| **roadmap/ending** | road + homework card | perch → big wave goodbye on last step |

Rhythm: alternate dense demo slides with airy statement slides. Use a split divider
every 4–6 slides to mark a new Part.

## 7. Fitting at 1024×576 (lessons learned)

The deck must fit with nothing clipped at **1024×576** and look good at 1920×1080.
What went wrong before and the fixes:
- *Left column overflow on demo slides* → shorten text; reduce list padding; put the
  readout and the result card in the same grid cell (`grid-area:1/1`) with
  `data-until` on the readout so they swap instead of stacking.
- *Title wraps to 3 lines* → `white-space:nowrap` + smaller inline font-size, move the explanation into a `.ps` below.
- *Grid of cards clipped* → don't set a `max-height` on the grid; let cards size to content, cut words instead.
- *Summary sentence wraps badly* → `font-size:min(3.7vw,6.6vh)` and explicit `<br>`s.
- *Clawd's bubble covers content* → use perch mode on content slides (see clawd.md).
- Demo-slide titles in the 29% left column: ≤ ~7 汉字 per line at `.h2x`, or they wrap to 3 lines.
- Long headlines: prefer two short lines with `<br>` over one long line.
