# Clawd: staging and voice

Clawd is the orange pixel mascot (SVG sprite, `viewBox 0 0 20 12`, already in the
template — never redraw it as an image or emoji). It walks between positions,
blinks, bobs, jumps, waves, sweats, blushes, and talks in a typewriter speech
bubble. It is the deck's comedian and the student's buddy; the teacher is the
expert. Clicking Clawd makes it jump and say a random line from `QUIPS`.

## 1. Staging (`CL` config)

`CL[slideId]` is an array with one entry per step:

```js
road:[
  {x:40,perch:1,say:'我们在这儿：新手村。'},
  {x:60,perch:1,say:'一路打怪升级，最终 Boss：积分！'},
  {x:88,y:90,s:1.1,say:'下节课：函数与极限。我们下节课见！',act:'wave',mood:'happy'}],
```

| field | meaning |
|---|---|
| `perch:1` | small Clawd (`s≈.62`) stands **on the chrome rule** at the top; bubble opens to the side. Default for every content slide: it can't cover content because the chrome line is empty space. |
| `x` | horizontal position in vw. Perch: 38–46 (the gap between the left chrome label and the page number); move it a few vw between steps so it "walks". Big: 79–88. |
| `y`, `s` | only for big Clawd: feet position in vh and scale. Cover `{x:79,y:72,s:2.2}`, divider `{x:79,y:72,s:2}`, corner `{x:86,y:88,s:1.3}`, goodbye `{x:88,y:90,s:1.1}`. |
| `act` | `'jump'` = punchline / aha moment · `'wave'` = hello / bye · `'shake'` = "no no no" |
| `mood` | `'happy'` = blush + smiling eyes (success, jokes) · `'sweaty'` = blue sweat drop (struggling, scary, "this is hard") |
| `look` | -1 / 1: eyes glance left/right (side-eye at a wrong answer) |
| `left:1` | perch only: bubble on the left (if the right side of the chrome line is busy) |

When x/y change, Clawd walks there (legs animate, bubble hides), then acts and
types. Big Clawd only goes where the slide has empty space: the paper half of a
split slide, or a corner of a sparse statement slide.

## 2. Voice

Clawd's bubble lines are **short** (aim ≤ 30 汉字, hard max ≈ 40). Perch bubbles
sit in the thin strip above the chrome rule: up to ~28 字 stays on one line at
1024 px wide; longer lines wrap and the bubble hangs down over the content, so
keep perch lines tight. The teacher's
script carries the explanation; Clawd adds a reaction, a nudge, or a joke. A
good deck has a punchline on most slides and a `jump` on the aha step.

**Persona**
- A tiny, enthusiastic AI teaching assistant. Self-aware about being an AI and
  happy to make itself the butt of the joke ("我（AI）就是靠导数，下了几万亿次山才学会说话的").
- Struggles alongside the student (`sweaty`: "Δt 再小点……再小点……", "直尺：我太难了。").
- Gets visibly excited at the reveal (`jump`: "这不就是个长方形嘛！").
- Food, everyday life, games ("下课我要去吃披萨", "新手村", "最终 Boss").
- Never mocks the student. Never sarcastic about the subject being boring.

**Joke patterns that worked**
| pattern | example |
|---|---|
| Fake-out then reveal (hook slide) | "嗯……听起来很有道理对吧？" → "哈哈哈，开玩笑的！" |
| Etymology / trivia twist | "它的英文名叫 Calculus。对，和「结石」是同一个词。" |
| Clawd inserts itself into the example | "换个场景：一辆车，从起步到刹车。司机是我。" |
| Personify the tool | "直尺：我太难了。" |
| Understatement after a big idea | "就这？就这。" |
| Relief of an imagined stakeholder | "最后停在 e ≈ 2.718。银行松了口气。" |
| Mild safety aside | "下次被雷达测速拍到，记得那是瞬时速度。（别超速）" |
| Callback to an earlier joke | pizza on the circle slide → "下课我要去吃披萨" |

A joke should also be a **memory hook** for the concept (微分 = 切, 积分 = 拼),
not random noise. If a line doesn't help remember something or keep attention,
cut it.

**Language**: write Clawd in the deck's language. For Chinese decks, put English
key terms in the slide content (kickers, cards) so students learn them, but
keep Clawd's lines mostly Chinese and colloquial (口语).

## 3. QUIPS (click-on-Clawd lines)

Five lines, on-topic, e.g. `'别戳我，看黑板！'`, `'微分：切。积分：拼。记住没？'`,
`'π = 3.14159265……我还能背。'`. The teacher uses clicking Clawd to win back
attention, so make them punchy.

## 4. Keyboard

`H` hides/shows Clawd (for when the teacher wants a clean slide). `F` fullscreen.
