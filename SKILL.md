---
name: clawd-teach
description: Turn any topic into a single-file animated HTML teaching deck in Swiss "Style B" (one orange accent, light sans-serif type, grid-dot background) where Clawd, the orange pixel mascot, walks around, reacts and cracks jokes while live canvas animations show the idea happening, plus a per-step teacher script (台词 .txt). Use this whenever the user wants to teach, explain, tutor or present a concept to a student or audience, e.g. 做课件, 讲解/教学 HTML, 导论课, 给学生讲某个知识点, "explain X with Clawd", lively/funny lesson slides, 有趣诙谐生动的讲解. Use it for any subject (maths, physics, programming, history, economics, biology…), even if the user doesn't mention Clawd or Swiss style, and when they ask for "the same style as before" for a new lesson.
---

# Clawd Teach

Make a lesson that a teacher can project and click through: one HTML file
(horizontal slides, per-step reveals, canvas animations, Clawd as a funny teaching
assistant) plus a teacher script for every step. The reference implementation
is `examples/calculus-intro.html`, a 16-slide 高数导论课 for a 专升本 student. Its
script is `examples/calculus-intro_script.txt`. A shorter second example on a
programming topic, an 8-slide 二分查找 lesson with a race animation, is
`examples/binary-search.html` plus its script. A third, on an AI topic (RAG), is
`examples/rag.html` plus `examples/rag_script.txt`: a pipeline, a chunk-size control, an
embedding map and an open-book/closed-book switch. When in doubt, do what they do.

## What "the same style" means

1. **Swiss Style B look**
   - Paper background with a dot grid. Ink-black light-weight type. One orange accent `#D97757`.
   - Square corners, no shadows, no gradients.
   - Mono uppercase kickers, and a thin chrome rule at the top of every slide with a `04 / 16` page counter.
2. **Smooth motion**
   - Slides glide horizontally. Content reveals step by step with staggered easing.
   - Canvas scenes animate between states rather than jumping.
3. **Clawd**
   - The pixel mascot walks between positions, perches on the chrome rule on content slides, and stands big on cover and divider slides.
   - It types short funny lines in a speech bubble, jumps on aha moments, sweats on hard parts and waves goodbye.
4. **Teaching arc**
   - A joke hook, then the real definition, then intuition you can *see*.
   - Then concrete examples, then real-world uses, then the "why do we need the next idea" section.
   - Ends with a one-sentence summary that has highlighted keywords, and a game-style roadmap with homework.
5. **Tone**: funny, lively, concrete (有趣诙谐生动). Everyday stories (pizza, a car, a mountain road, the classroom's air) instead of abstract symbols.

All the CSS, the Clawd sprite and controller, the deck engine and the background
are already in `assets/template.html`. Build from it; don't rewrite the engine.

## Read before you plan (required)

Read these before step 2. They are short, and the deck is judged on what's in them:
1. `references/patterns.md`: the cross-subject animation menu and the one test every demo slide must pass.
2. `references/scenes.md`: how a scene is wired, plus the pitfalls.
3. `references/clawd.md`: Clawd's staging and voice.
4. One worked example, end to end: grep `examples/binary-search.html` (or `examples/rag.html` for a tech topic) for one demo slide's `<section>`, its `SC.<id>=` and its `CL` entry, and read all three.

## Workflow

### 1. Pin down the brief
Extract from the request, and ask only if the topic itself is unclear:
- **Topic and outline.** If the user gives an outline, follow it in order. You may add content; say what you added.
- **Audience and level.** Default to a beginner who is smart but new to the topic.
- **Length.** Default is a 40–50 minute lesson, which is about 12–16 slides with 2–5 steps each.
- **Language.** Match the user. Chinese decks keep English key terms in kickers and cards.
- **Context worth using.** For example, the teacher's and student's backgrounds can become jokes or examples.

### 2. Plan the lesson before writing HTML
Pick **one running example** that carries the whole lesson (the HR bot's 「年假几天？」 in
`rag.html`, the pizza and the car in `calculus-intro.html`). Then write the slide list as a
table and show it in your reply before building (then carry on; don't wait for approval). Columns:

| data-id | layout | pattern (P1–P10) | what moves: step 1 → last step | number that moves | control | Clawd's beat |
|---|---|---|---|---|---|---|

The "what moves" cell is the sentence from `references/patterns.md` §0. If a demo row's cell
only describes text appearing or boxes with labels, it isn't a scene yet: go back to the
pattern menu. Statement and grid slides may write "—".

Typical arc:

| # | slide | layout |
|---|---|---|
| 1 | Cover with a hook subtitle ("从一块披萨开始") | split, big Clawd waves |
| 2 | Hook: the naive answer gets struck through, "✗ 开玩笑的" | statement |
| 3 | Real name / definition, trivia, two contrast cards | statement |
| 4–8 | Core intuition + 2–4 worked visual examples (canvas scenes) | demo |
| 9–10 | Applications (3 domains) / why it matters | grid |
| 11 | Section divider: "为什么需要 X？" | split |
| 12–14 | The deeper concept + its everyday uses | demo / grid |
| 15 | One-sentence summary, keywords highlighted per step | statement |
| 16 | Roadmap LV.0 → Boss + homework, Clawd waves bye | roadmap |

Adapt it freely. A history lesson's "canvas scene" might be an animated timeline or a map, and a programming lesson's might be an array being sorted step by step. Every core concept gets something that *moves*. `references/patterns.md` §1 lists strong patterns per subject.

### 3. Build the deck
1. Copy `assets/template.html` to the output path, `<topic>.html` in the user's working directory. Fill in the `<title>`.
2. Build slides from the template's slide library: cover, hook, concept, demo, cards, divider, summary and road.
   - Duplicate, reorder and delete them as needed. Each `<section>` needs a unique `data-id`.
   - Read `references/design-system.md` for components, layouts and the fitting rules.
3. Write a canvas scene `SC.<id>` for each demo slide, by hand, for that slide's idea.
   - Never build slides or scenes from a shared generator, loop or factory function. Two concepts never move the same way.
   - Give at least one scene a `.seg` control (a parameter or an A/B switch) the teacher can play with in class.
   - Delete the template's `SC.demo` if you don't use it.
4. Write `CL` (Clawd's line, position and act per step) and `QUIPS`. Read `references/clawd.md` for staging and voice.
5. Replace every 【placeholder】.

The example deck is ~80 KB. Read the parts you need (grep for a slide's `data-id`, or `SC.circle=` etc.) rather than the whole file.

### 4. Check
```bash
python3 <skill-dir>/scripts/check_deck.py <deck>.html
```
Fix every ERROR. Read each WARN and fix it. The quality WARNs (duplicate scenes, static
scenes, repeated layouts, uniform Clawd) are the ones weaker decks trip; if you keep one,
say why in your reply.

Then look at it in the browser at **1024×576**, and at a wide size if you can.
- Open the file from inside the project folder, so the pane runs its scripts.
- Jump to slides with `go(slideIndex, step)` through the JS tool.
- Wait 5–10 s before screenshotting, because a hidden pane throttles animation.
- On every slide's **last step**, check that nothing is clipped, that Clawd's bubble doesn't cover content, and that titles don't wrap into 3 lines.
- Check the browser console for errors.

### 5. Self-review
Before writing the script, fill this table for every slide and show it in your reply:

| slide | what moves (or "—") | the joke / Clawd's beat | memory hook the student keeps |
|---|---|---|---|

Any demo slide with nothing moving, or any slide with neither a joke nor a hook, gets
redone, not explained away.

### 6. Write the teacher script
Write `<topic>_台词.txt` next to the deck in the format of `references/script-format.md`.
- One section per slide and one block per step.
- Copy Clawd's lines from `CL`, and include 【互动】 prompts and time estimates.
- Skip the script only if the user says they don't want one.

### 7. Deliver
Give clickable paths to both files. Mention the controls:
- → / space for next, ← for back.
- F for fullscreen, H to hide Clawd.
- Click Clawd for a joke.
- Any in-slide buttons the teacher can play with.

Say briefly what you added beyond their outline.

## Anti-patterns (seen in real failed decks)

| don't | do instead |
|---|---|
| One scene function reused for every canvas, with different labels | One hand-written `SC.<id>` per idea, from the pattern menu |
| A canvas of labelled boxes and "↓" arrows | Make the thing travel through the stages (P1), or use DOM and drop the canvas |
| Generic kickers on every card: `01 · THINK`, `02 · REMEMBER` | Kickers that name the content: `R · Retrieval`, `Example 02 · 微分 → 速度` |
| The same two-card layout on most slides; summary and roadmap built from cards | Use the template library: hook strike, giant name, divider, `.sum-text` with `data-hl`, `.road` |
| Clawd at the same x on every slide, every last step `jump + happy` | Move it, sweat on hard steps, shake at wrong answers, jump only on the aha |
| Hedging in Clawd's voice: 「虚构示例」「可选步骤」「不一定」 | Clawd jokes; precision and caveats go in the teacher script |
| Writing slides with a Python script that loops over a list | Write each slide; they differ because the ideas differ |

## Quality bar
- **Show, don't tell.** If a slide is only text, ask whether an animation could make the point instead.
- **Fail first, then fix.** Where the concept fixes a problem, show the problem happening (P10) before the fix.
- **Every number on screen should move toward the answer.** Pick examples where convergence is visible; `references/scenes.md` §5 explains why.
- **Clawd lines stay short** (≤ ~40 字).
  - Most slides have a punchline. Aha steps get `act:'jump'`, hard steps get `mood:'sweaty'`.
  - Jokes double as memory hooks. Call back to the running example.
- **One accent colour.** Emphasis comes from orange, size and weight 200 vs 400, never from new colours.
- **It works offline, except for fonts.** Google Fonts falls back to PingFang / system sans if blocked, which is fine in China.
