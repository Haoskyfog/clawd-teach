# Teacher script (台词) format

A plain-text file, one section per slide, broken down **per step** so the teacher
knows exactly what to say before each click. Full example:
`examples/calculus-intro_script.txt`.

```
<课程名> —— 老师台词稿
配套课件：<文件名>.html
====================================================================

使用说明
- 每一页按「步」写。看到【点击 →】就按一下 → 或空格，画面会进到下一步。
- 每页标题后面的（约 X 分钟）是建议时长，全课大约 NN 分钟。
- 【互动】是停下来问学生的地方，等他回答，别急着翻页。
- 【Clawd】是这一步 Clawd 说的话（屏幕上会自动出现），你可以顺着接一句，也可以不理它。
- 括号里的英文是关键词，顺口带一下就好。
- 台词只是参考，用自己的话讲更自然。


====================================================================
第 N 页 · <页标题>（约 X 分钟）
====================================================================
—— 第 0 步 ——
【画面】<what appears on screen at this step>
【Clawd】<Clawd's bubble line, copied exactly from CL>

台词：
<what the teacher says: spoken, short sentences, one idea per line>
【互动】<a question to ask the student>
（<stage direction in parentheses>）

【点击 →】
—— 第 1 步 ——
…
【点击 →】进入第 N+1 页

====================================================================
附：课堂小技巧
- 键盘快捷键：→ / 空格 下一步；← 上一步；F 全屏；H 隐藏或显示 Clawd。
- <which slides have interactive controls and how to use them>
- 学生走神的时候，点一下 Clawd，它会跳一下、讲句冷笑话。
- <which slides to compress if short on time>
====================================================================
```

Guidelines
- Steps must match the deck exactly: same count, same Clawd lines. Write the script
  *after* the deck is final, reading `CL` and the `data-s` steps from the HTML.
- The teacher explains; Clawd jokes. The script can riff on Clawd ("Clawd 说得对……").
- Put English key terms in parentheses the first time they appear (derivative, integral, limit…).
- Include 1–2 【互动】 per slide on concept slides; accept any answer first, then guide.
- Time estimates per slide; total should match the requested lesson length.
- Single-slide steps (cover) can skip the —— 第 k 步 —— header.
