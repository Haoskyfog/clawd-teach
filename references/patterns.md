# Animation pattern library (any subject)

A menu of ten ways to make an idea *move*, with the subjects each one suits and
a code skeleton for the less obvious ones. Read this before planning the deck.
It is a menu, not a quota: pick the pattern that makes **this** idea visible,
and invent a new one when none fits.

## Contents
0. The one test every demo slide must pass
1. Picking a pattern by subject
2. The patterns (P1–P10)
3. Skeletons (P2 toggle, P3 sweep, P5 clock, P8 particles, P10 break-and-fix)
4. What is NOT an animation

---

## 0. The one test every demo slide must pass

Before writing a scene, finish this sentence for it:

> **"At step 1 the student sees ___; by the last step they see ___; the change
> is caused by ___, and the number ___ moves from ___ to ___."**

If you can't fill the blanks with things that are *drawn and moving* (not words
written in boxes), you don't have a scene yet. Common good shapes:
- **before → after**: the same picture, changed by the concept (pizza → rectangle).
- **wrong → right**: show the failure, then the fix (key sentence cut in half → overlap rescues it).
- **without → with**: one switch, two worlds (closed book → hallucination, open book → cited answer).
- **coarse → fine**: refine a parameter and watch an error shrink (5 → 10 → 100 rectangles).

## 1. Picking a pattern by subject

| subject | strong patterns | example scenes |
|---|---|---|
| Science (physics, chemistry, biology, earth) | P8 particles · P3 sweep · P5 clock · P9 balance | gas molecules hit walls → pressure; photons trapped by CO₂; enzyme + substrate; predator–prey |
| Engineering | P3 sweep · P10 break-and-fix · P5 clock · P1 flow | feedback loop overshoots then settles; beam bends under load until it cracks; queue builds at a bottleneck |
| Finance / economics | P5 clock · P2 toggle · P6 race · P8 many paths · P9 balance | compound interest snowball; 1 stock vs 20 stocks as 50 random paths; supply/demand curves shift to a new price |
| Maths | P4 converge · P7 decompose · P3 sweep | Riemann rectangles; secant → tangent; pizza → rectangle |
| Programming / CS | P6 race · P1 flow · P10 break-and-fix · P4 converge | binary vs linear search; packets through a network; race condition corrupts a counter |
| History / geography | P5 clock · P1 flow · P9 balance | a timeline drives a map: borders, trade routes, population dots |
| Language / literature | P7 decompose · P2 toggle · P1 flow | a sentence splits into parts that fly to labelled slots; swap one word and the meaning flips |
| AI / data | P6b map · P1 flow · P2 toggle · P4 converge | embeddings cluster by meaning; ball rolls down a loss curve; RAG open/closed book |

## 2. The patterns

**P1 Flow / pipeline**: tokens travel through stages and change at each one.
Per step: one more stage lights up and the token visibly transforms there.
*Wrong version*: boxes with arrows and no token. Use for: digestion, compilers,
supply chains, RAG pipeline, a bill becoming law. Example: `rag.html` SC.pipeline (scan → fly → type).

**P2 Toggle / A-B compare**: one picture, one switch (`.seg`), two worlds blended by a tween.
The switch is the lesson: same inputs, one factor different. Use for: with/without
friction, with/without CO₂, open/closed book, fixed vs floating rate. Skeleton §3.1; example: `rag.html` SC.prompt (开卷 / 闭卷).

**P3 Parameter sweep**: a control changes one parameter; the curve, picture and
readout all respond together. Use for: launch angle → range, interest rate → final
balance, gain Kp → overshoot, chunk size → recall. Skeleton §3.2; example: `rag.html` SC.chunk.

**P4 Converge / refine**: n grows (step by step), the approximation visibly
approaches the truth and an error readout shrinks. Pick an example where it really
converges (scenes.md §5). Use for: Riemann sums, Monte Carlo π, Newton's method,
sample size → poll accuracy. Examples: `calculus-intro.html` SC.area, SC.tangent.

**P5 Clock / accumulation**: a `clock` advances a quantity over time; the history
draws itself as a curve while the object moves. Use for: compound interest,
radioactive decay, charging a capacitor, population growth, a war's front line
over months. Skeleton §3.3.

**P6b Meaning map**: items fly from a list onto a 2-D map where distance = similarity,
then cluster; the query lands among its neighbours. Use for: embeddings, species
relatedness, market segments. Example: `rag.html` SC.embed + SC.search.

**P6 Race / side-by-side**: two strategies run on the same input with live
counters; the gap is the point. Use for: binary vs linear search, O(n) vs O(n²),
saving early vs late, diversified vs concentrated. Example: `binary-search.html` SC.race.

**P7 Decompose / reassemble**: a whole breaks into labelled parts that fly apart,
then reassemble differently (staggered `u` per piece, arc jump). Use for: pizza →
rectangle, a molecule's atoms, a sentence's grammar, a balance sheet, an engine.
Example: `calculus-intro.html` SC.circle.

**P8 Particles / many agents**: dozens of seeded particles (`mulberry`) follow one
simple rule; the macro behaviour emerges. Showing *many* random runs is also how to
show risk (50 price paths, not one). Use for: diffusion, gas pressure, heat,
epidemics, traffic jams, bank runs, portfolio outcomes. Skeleton §3.4.

**P9 Balance / equilibrium**: two forces or curves; adding something tips the
picture until it settles at a new equilibrium marked by the accent square. Use for:
supply and demand, chemical equilibrium, energy in = energy out, lever, accounting
equation.

**P10 Break-and-fix**: run the naive version until it visibly fails (crack, overshoot,
crash, cut sentence, hallucination stamp), then apply the fix and replay. The failure
is what students remember. Use for: resonance, overfitting, margin call, race
conditions, bad chunking. Skeleton §3.5.

## 3. Skeletons

All use the template helpers (`Tw`, `Lin`, `fit`, `ease`, `lerp`, `clamp`, `mulberry`,
`C`, `MONO`, `SANS`, `setText`). Fill the drawing in; keep the structure.

### 3.1 P2 toggle

```js
SC.toggle=(()=>{
  const cv=$('#cv-toggle'),R={v:$('#tg-v')},mode=new Tw(0,4),show=new Tw(0,4);
  const btns=$$('#tg-ctl button');                          // <button data-m="0">无</button><button data-m="1">有</button>
  function setMode(m){mode.set(m);btns.forEach(b=>b.classList.toggle('sel',+b.dataset.m===m))}
  btns.forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();setMode(+b.dataset.m)}));
  const ST=[{sh:0,m:0},{sh:1,m:0},{sh:1,m:1}];               // step 2 flips the switch for the class
  function apply(s,snap){const c=ST[Math.min(s,2)],k=snap?'snap':'set';show[k](c.sh);mode[k](c.m);btns.forEach(b=>b.classList.toggle('sel',+b.dataset.m===c.m))}
  return{enter(s){apply(s,true)},setStep(s){apply(s,false)},
    frame(d,now,active){[mode,show].forEach(o=>o.upd(d));const{ctx,w,h}=fit(cv);
      const m=mode.v;                                        // 0 = world A, 1 = world B, in between = morph
      // draw the shared scene once, then the part that differs with lerp(a,b,m) / alpha m
      const out=lerp(10,25,m);                               // e.g. a quantity that depends on the switch
      if(active)setText(R.v,out.toFixed(1))}};
})();
```

### 3.2 P3 sweep (curve + object + readout move together)

```js
SC.sweep=(()=>{
  const cv=$('#cv-sweep'),R={p:$('#sw-p'),y:$('#sw-y')},p=new Tw(1,4),draw=new Lin(0,.8);
  const btns=$$('#sw-ctl button');                          // data-p="0.5" "1" "2"
  btns.forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();p.set(+b.dataset.p);btns.forEach(o=>o.classList.toggle('sel',o===b))}));
  const ST=[{p:1,d:0},{p:1,d:1},{p:2.5,d:1}];
  function apply(s,snap){const c=ST[Math.min(s,2)],k=snap?'snap':'set';p[k](c.p);draw[k](c.d)}
  const f=(x,p)=>1-Math.exp(-p*x);                          // the model being taught
  return{enter(s){apply(s,true)},setStep(s){apply(s,false)},
    frame(d,now,active){[p,draw].forEach(o=>o.upd(d));const{ctx,w,h}=fit(cv);const g=graph(w,h,5,1.2,30);
      axes(ctx,g,5,1.2,1,.2,'t','y');
      ctx.strokeStyle=C.accent;ctx.lineWidth=2.5;ctx.beginPath();
      for(let i=0;i<=160;i++){const x=5*draw.v*i/160;i?ctx.lineTo(g.X(x),g.Y(f(x,p.v))):ctx.moveTo(g.X(x),g.Y(f(x,p.v)))}ctx.stroke();
      if(active){setText(R.p,p.v.toFixed(2));setText(R.y,f(5,p.v).toFixed(3))}}};
})();
```

### 3.3 P5 clock (time drives the object and draws the history)

```js
SC.clock=(()=>{
  const cv=$('#cv-clock'),R={t:$('#ck-t'),v:$('#ck-v')};let clock=0,run=0;const hist=[];
  const ST=[{run:0},{run:1},{run:1}];
  function apply(s,snap){run=ST[Math.min(s,2)].run;if(snap){clock=0;hist.length=0}}
  return{enter(s){apply(s,true)},setStep(s){apply(s,false)},
    frame(d,now,active){const T=30;if(run&&clock<T)clock=Math.min(T,clock+d*3);  // 3 sim-years per second
      const v=1000*Math.pow(1.08,clock);                     // the accumulating quantity
      if(!hist.length||clock-hist[hist.length-1][0]>.1)hist.push([clock,v]);
      const{ctx,w,h}=fit(cv);const g=graph(w,h,T,12000,30);axes(ctx,g,T,12000,5,2000,'年','元');
      ctx.strokeStyle=C.ink;ctx.lineWidth=2;ctx.beginPath();hist.forEach(([t,y],i)=>i?ctx.lineTo(g.X(t),g.Y(y)):ctx.moveTo(g.X(t),g.Y(y)));ctx.stroke();
      ctx.fillStyle=C.accent;ctx.fillRect(g.X(clock)-6,g.Y(v)-6,12,12);
      if(active){setText(R.t,clock.toFixed(0));setText(R.v,Math.round(v).toLocaleString())}}};
})();
```
Reset `clock` and `hist` when the student presses a replay button, not every frame.

### 3.4 P8 particles (seeded, one rule, emergent result)

```js
SC.particles=(()=>{
  const cv=$('#cv-particles'),R={n:$('#pt-n')},rnd=mulberry(7),N=80;
  const P=[...Array(N)].map(()=>({x:rnd(),y:rnd(),vx:rnd()-.5,vy:rnd()-.5}));
  const heat=new Tw(.3,3);let hits=0,acc=0;
  const ST=[{h:.3},{h:.3},{h:1}];                            // step 2: heat it up
  function apply(s,snap){heat[snap?'snap':'set'](ST[Math.min(s,2)].h)}
  return{enter(s){apply(s,true)},setStep(s){apply(s,false)},
    frame(d,now,active){heat.upd(d);const{ctx,w,h}=fit(cv);
      P.forEach(p=>{p.x+=p.vx*heat.v*d;p.y+=p.vy*heat.v*d;
        if(p.x<0||p.x>1){p.vx*=-1;p.x=clamp(p.x,0,1);if(p.x===1)hits++}if(p.y<0||p.y>1){p.vy*=-1;p.y=clamp(p.y,0,1)}
        ctx.fillStyle=C.ink;ctx.fillRect(10+p.x*(w-20)-2,10+p.y*(h-20)-2,4,4)});
      acc+=d;if(acc>1){if(active)setText(R.n,String(hits));hits=0;acc=0}}};   // hits per second on the right wall = "pressure"
})();
```
Keep N ≤ ~300 and draw with `fillRect`; it stays smooth on a laptop projector.

### 3.5 P10 break-and-fix (fail first, then the fix replays)

```js
SC.fix=(()=>{
  const cv=$('#cv-fix'),run=new Lin(0,.5),fixed=new Tw(0,3);
  const ST=[{r:0,f:0},{r:1,f:0},{r:0,f:1},{r:1,f:1}];        // run naive → it fails → apply fix → run again
  function apply(s,snap){const c=ST[Math.min(s,3)];fixed[snap?'snap':'set'](c.f);if(snap)run.snap(c.r);else{run.snap(0);run.set(c.r)}}
  return{enter(s){apply(s,true)},setStep(s){apply(s,false)},
    frame(d,now,active){[run,fixed].forEach(o=>o.upd(d));const{ctx,w,h}=fit(cv);
      const failAt=.6,t=run.v,f=fixed.v>.5;
      const broken=!f&&t>failAt;                              // draw the system; when broken, draw the crack / crash
      if(broken){ctx.fillStyle=C.accent;ctx.font=SANS(600,18);ctx.fillText('✗',w/2,h/2)}
      if(f&&t>=1){ctx.fillStyle=C.accentInk;ctx.font=SANS(600,18);ctx.fillText('✓',w/2,h/2)}}};
})();
```

## 4. What is NOT an animation

These look like scenes but teach nothing that a sentence wouldn't. `check_deck.py`
warns about some of them.

- **Boxes with labels and arrows** (a flowchart drawn on a canvas). If the canvas only
  holds words in rectangles, it's a diagram: make the *thing* travel through it (P1)
  or delete the canvas.
- **One scene function reused for every slide** with different labels. Each concept
  moves differently; each `SC.<id>` is written for its own slide.
- **Text that slides in or fades in.** That is the DOM reveal system's job, not a scene.
- **Random motion with no meaning** (floating dots behind a title). Every moving thing
  must stand for something in the lesson.
- **A single run of something random** (one stock path, one coin flip sequence).
  Show many runs, or the student learns an anecdote instead of the rule.
