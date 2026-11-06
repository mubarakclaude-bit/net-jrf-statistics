---
name: Author a lesson
about: Queue one topic to be written into the app
title: "Author <module>-t<n> — <topic name>"
labels: lesson
---

**Topic id:** `<module>-t<n>`  (e.g. `regression-t2`)

**Why now:** <marks exposed, anchor question, or "next in BACKLOG.md">

**Anchor, if any:** Q<n> — <n> variants, key <X>, marked <Y>

**Anything specific:** <a trap to cover, a visualisation to reuse, a cross-reference>

---
*To action this, give any AI author (Claude, ChatGPT, Codex) or a person this:*

> Clone https://github.com/mubarakclaude-bit/net-jrf-statistics and read AGENTS.md, then SPEC.md.
> Author the topic named in open issue #<this issue number>. Verify every figure by computing it.
> Run addlesson.sh until it passes clean, run both test suites, and open a pull request. A
> different author reviews it before it merges.
