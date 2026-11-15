# Canvas scenes: making ideas move

The best slides in the example deck are the ones where the idea *happens* on
screen: a pizza is cut into 8 → 32 → 128 slices and rearranges into a rectangle;
a secant line collapses into a tangent while a zoom box shows the curve becoming
straight; air particles get gridded until each cell is uniform. Aim for at least
one such scene per core concept. Static diagrams are the fallback, not the default.

## Contents
1. Scene contract
2. Helpers available in the template
3. Recipe
4. Animation patterns
5. Choosing examples that actually show the idea
6. Pitfalls

---

## 1. Scene contract

```js
SC.<slideId>=(()=>{
  const cv=$('#cv-<slideId>'), R={a:$('#x-a')};      // canvas + DOM readouts
  const t=new Tw(0,5), grow=new Lin(0,1);              // tweens
  const ST=[{…},{…},{…}];                              // per-step targets
  function apply(s,snap){const c=ST[Math.min(s,ST.length-1)],m=snap?'snap':'set';t[m](c.t);…}
  return{
    enter(s){apply(s,true)},          // slide entered → snap to state (no animation)
    setStep(s){apply(s,false)},       // each step → animate toward state
    frame(dt,now,active){             // every frame for current ±1 slide
      [t,grow].forEach(o=>o.upd(dt));
      const{ctx,w,h}=fit(cv);         // resizes for DPR and clears; draw in CSS px
      …draw from t.v, grow.v…
      if(active) setText(R.a, value.toFixed(2));   // only touch DOM on the active slide
    }};
})();
```

The engine calls `enter(step)` right away and `setStep(step)` ~480ms later (after
the page slide transition), so a typical "reveal on entry" is: `enter` snaps a
value to 0, `setStep` sets it to 1 → it animates in once the slide lands.

## 2. Helpers available in the template

| helper | what |
|---|---|
| `Tw(v,k)` | exponential ease toward target (`k` = stiffness, 3 slow … 8 snappy). `.set(t)` `.snap(v)` `.upd(dt)` `.v` |
| `Lin(v,speed)` | constant-speed tween (units per second). Good for "draw the curve in", morph progress 0→1 |
| `fit(cv)` | DPR-aware resize + clear; returns `{ctx,w,h}` |
| `graph(w,h,xmax,ymax,top)` | plot frame → `{L,R,T,B,X(),Y(),kx,ky}` |
| `axes(ctx,g,xmax,ymax,xtick,ytick,xlabel,ylabel)` | light grid, ticks, axis labels |
| `C` | palette: `accent, accentInk, ink, paper, g1, g2, g3` |
| `MONO`, `SANS(weight,px)` | canvas fonts |
| `ease(t)` `lerp` `clamp` | easing / maths |
| `mulberry(seed)` | seeded RNG → particle fields look the same every time |
| `dashed(ctx,on)` | toggle dashed strokes for guide lines |
| `setText(el,v)` | write only if changed |

## 3. Recipe

1. Decide the **one** visual change per step (n = 8 → 32 → 128; secant → tangent; grid 2×1 → 6×3 → 48×24).
2. Write the `ST` table, one row per step.
3. Draw the static frame (axes / room / road), then the animated layer, then labels.
4. Add live readouts in the left column (`.ro`) so the numbers move with the picture.
5. Optional: a `.seg` control so the student can play with it in class.

Keep each scene self-contained in an IIFE. Typical size: 20–50 lines.

## 4. Animation patterns (from the example deck)

- **Morph between two states with stagger**: per-item progress
  `u=ease(clamp(t*(1+S)-S*i/(N-1),0,1))` makes items move one after another
  (pizza slices fly into a row in sequence; rectangles grow left to right).
- **Cross-fade on count change**: keep previous `pn` and new `n`; draw the old set
  with alpha `1-xf.v` and the new one with `xf.v` while `xf` goes 0→1.
- **Draw-in**: `Lin` from 0→1 controls how far along x the curve is drawn.
- **Arc jump**: add `-sin(π·u)·r·.38` to y so pieces hop as they move.
- **Zoom inset**: a square that redraws the neighbourhood at ×14 — "zoom in and the curve is straight".
- **Magnifier**: highlight one cell, connect lines to a big box drawing its contents, with a ✓/✗ verdict and a bar meter.
- **Auto-loop demo**: a `clock` that loops (`(clock*1.5)%14`), e.g. a car driving the road above the graph, a ball rolling down a loss curve (gradient descent).
- **Discrete countdown**: step a value every 0.85s (halving Δx) with an auto-zooming number line, then reset after a pause.
- **Mini canvases** inside cards (3 tiny looping illustrations on an applications slide).
- **Pure CSS/SVG** is fine for simple things: cut/join bars, network lines drawing in (`stroke-dashoffset` with `pathLength="1"`).

Motion vocabulary: things *move into place* rather than appear; colour change
(ink → accent) marks "this is the part we're talking about"; the accent square
`fillRect(x-6,y-6,12,12)` is the standard "current point" marker (no circles; Style B is square).

## 5. Choosing examples that actually show the idea

The numbers on screen must visibly converge or the demo proves nothing.
- Uniform midpoint sums of `sin²` over a full period are *exact* at any n, so a
  Riemann-sum demo with it shows no improvement. The example deck switched to a
  car with `v(t)=t²−0.1t³` (accelerate, then brake), where 5 → 10 → 100 rectangles
  visibly approach 83.33.
- Pick a curve whose secant slope differs a lot from the tangent at the chosen
  point, so the shrinking Δt matters.
- Seed randomness so particle fields are reproducible and the "non-uniform" cell
  really is non-uniform.
- Prefer concrete, physical stories (pizza, a car with a broken odometer, a
  mountain road, the classroom's air, bank interest) over abstract `f(x)`.

## 6. Pitfalls

- Number formatting on auto-zoom axes: values ≥ 1 should print as integers
  (`String(Math.round(x))`); small ones with enough digits, trailing zeros trimmed.
- Budget the canvas height for *everything*: labels above rows, markers and brackets
  below the last row. Compute row heights as `(h - all fixed gaps) / rows`, or the
  bottom markers are drawn off-canvas (happened in the binary-search race).
- `C.g1` on paper is nearly invisible: good for "eliminated / discarded" items, too
  faint for "still in play". Use `C.g2` or `'#a3a3a3'` for neutral live items, ink for the focus, accent for the answer.
- Canvas text: min 14px (`MONO` is 14px). Use `SANS(500,16–20)` for labels.
- Don't write DOM readouts when `!active` — neighbour slides also get `frame()`.
- Buttons inside slides: `e.stopPropagation()` or the click also advances the deck.
- The browser pane throttles `requestAnimationFrame` while hidden — when
  verifying, wait several seconds (or use `go(i,s)` via JS and wait) before judging motion.
