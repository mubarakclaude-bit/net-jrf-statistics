#!/usr/bin/env python3
"""Export lesson 4.1 as Markdown for review by a language model.

Different target from export_t1.py, which makes a document for a human to read and
annotate. A model reading a PDF gets a layout-extraction of it: tables lose their shape,
column order can scramble, and sub/superscripts can be dropped silently. Markdown is read
as written, so nothing is lost on the way in.

The important difference is not the format though — it is that every field carries its
JSON path. A finding of the form "scenes[10].blocks[1].body overstates the criterion" can
be applied mechanically; "the minimal sufficiency section is too strong" has to be hunted
for by hand, which is how the version-label drift and the re-typing losses happened in the
first two review rounds.

Maths is left exactly as the content files hold it, in Unicode. It is not transliterated
to LaTeX: a blind conversion of x₍ₙ₎, Σxᵢ², (1−p)^(n−Σx) and the like is a chance to
introduce errors into the very text being checked for errors, and the previous review read
the Unicode without difficulty.
"""
import json, io, os, sys

SEED = sys.argv[1] if len(sys.argv) > 1 else "seed/lesson_t1.json"
LES = json.load(io.open(SEED, encoding="utf-8"))
_q = [s for s in LES["scenes"] if s["kind"] == "quiz" and s.get("setId")]
_pool = "seed/%s.json" % _q[0]["setId"] if _q else None
POOL = json.load(io.open(_pool, encoding="utf-8")) if _pool and os.path.exists(_pool) else {"items": []}
TOPNO = os.environ.get("TOPNO", "")
OUT = "review"
os.makedirs(OUT, exist_ok=True)

def _mathmap(strings):
    """Lay formulas out using the app's own parser (mathrender.js), so the documents and
    the app cannot disagree about what a formula means."""
    import subprocess, tempfile
    xs = sorted({s for s in strings if s})
    if not xs:
        return {}
    fi = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(xs, fi, ensure_ascii=False); fi.close()
    fo = fi.name + ".out"
    subprocess.run(["node", "mathrender.js", fi.name, fo], check=True)
    return json.load(io.open(fo, encoding="utf-8"))


def _formulas_in(les):
    out = []
    for sc in les["scenes"]:
        for st in (sc.get("steps") or []) + (sc.get("solution") or []):
            if st.get("math"):
                out.append(st["math"])
        for b in sc.get("blocks") or []:
            if b.get("t") == "formula" and b.get("body"):
                out.append(b["body"])
    return out

MATH = _mathmap(_formulas_in(LES))
L = []
A = L.append

KIND = {"foundation": "prerequisite check", "intuition": "intuition", "theory": "theory",
        "explore": "interactive visualisation", "worked": "worked example",
        "recall": "retrieval practice", "completion": "fill in the blanks",
        "guided": "guided problem", "trapcheck": "true/false check",
        "summary": "summary", "quiz": "mastery test"}


def f(path, label, val, block=False):
    """One field, with its JSON path, so a finding can name exactly what to change."""
    if val in (None, "", []):
        return
    A("**%s** `%s`" % (label, path))
    A("")
    if isinstance(val, (list, tuple)):
        for i, v in enumerate(val):
            A("%s" % v if not block else "> %s" % v)
            A("")
    else:
        A("%s" % val)
        A("")


A("# Lesson %s — %s" % (TOPNO or LES.get("topicId"), LES.get("title")))
A("")
A("Complete authored content of one lesson from a UGC-NET Statistics (Code 107) "
  "preparation application, extracted from the application's own content files.")
A("")
A("| | |")
A("|---|---|")
for k, v in [("Content version", LES.get("version")),
             ("Scenes", len(LES["scenes"])),
             ("Core scenes", len([s for s in LES["scenes"] if not s.get("ext")])),
             ("Optional JRF-extension scenes", len([s for s in LES["scenes"] if s.get("ext")])),
             ("Estimated learner time", "%s minutes" % LES.get("estMin")),
             ("Mastery pool", "%d items" % len(POOL.get("items", []))),
             ("Position in the app", LES.get("breadcrumb")),
             ("Engine", LES.get("engineName")),
             ("Pool label", POOL.get("label")),
             ("Unit", "IV — Statistical Inference"),
             ("Audience", "JRF-target candidates, many returning after several years away")]:
    A("| %s | %s |" % (k, v))
A("")
ver = float(LES.get("version") or 0)
if ver < 4.1:
    A("## Before you start: where this lesson sits")
    A("")
    A("This lesson is at content version **%s**. The application's current authoring "
      "standard is 4.1, and three of its requirements are **known** to be unmet here, so "
      "please do not spend effort reporting them — they are scheduled work, not "
      "findings:" % LES.get("version"))
    A("")
    A("- no short \"how to use this lesson\" note on the overview;")
    A("- a quick check on only some teaching scenes rather than all of them;")
    A("- no family-to-statistic style reference table where one would help.")
    A("")
    if (LES.get("estMin") or 0) < 75:
        A("This lesson is also **%d minutes against a house standard of about 90**, so it "
          "is thinner than intended. Comments on what is MISSING in substance are "
          "therefore especially useful — but please flag omissions rather than proposing "
          "to shorten what is there." % LES.get("estMin"))
        A("")
    if len(LES.get("refs", [])) < 3:
        A("It carries %d references against a minimum of three; suggestions for a free "
          "university course page or a standard textbook chapter at this level are "
          "welcome." % len(LES.get("refs", [])))
        A("")
    A("What follows is the complete authored content as it stands.")
    A("")
A("## How to review this, and what to send back")
A("")
A("Please return **a list of findings, not a rewritten lesson.** The two previous review "
  "rounds came back as complete rewrites, and both times material was lost in the "
  "re-typing that nobody intended to drop — the exponential-family derivation in one "
  "round, a version label left inconsistent in the other. A findings list avoids that "
  "entirely.")
A("")
A("Each field below carries its **JSON path** in the content file. Please cite it. One "
  "finding per item, in this shape:")
A("")
A("```")
A("path:      scenes[10].blocks[1].body")
A("severity:  error | imprecision | suggestion")
A("issue:     what is wrong, in one sentence")
A("evidence:  the counterexample, condition or source that shows it")
A("proposed:  the replacement text, if you have one")
A("```")
A("")
A("What is most worth your attention, in order:")
A("")
A("1. **Mathematical errors and overclaims.** Statements true in the examples shown but "
  "false in general; converses asserted; side conditions omitted (sample-size "
  "requirements, support conditions, regularity assumptions); steps skipped in a "
  "counterexample so that it does not actually establish what it claims.")
A("2. **Items in the mastery pool with more than one defensible answer**, especially any "
  "stem asking for \"a sufficient statistic\" where a distractor is itself sufficient.")
A("3. **Places where the explanation is correct but would not survive contact with a "
  "candidate who has been away from the subject for years.**")
A("4. Anything examinable for this syllabus that is missing.")
A("")
A("Please do **not** recommend removing depth to make the lesson shorter. The target is "
  "JRF, which is decided by the harder theoretical questions, and the optional-extension "
  "mechanism already exists for material a bare pass does not need.")
A("")
A("Notation is Unicode as the application stores it: `Σxᵢ` is a sum over the sample, "
  "`x̄` the sample mean, `x₍₁₎` and `x₍ₙ₎` the smallest and largest observations, "
  "`I(·)` an indicator, `∝` proportionality up to a factor free of the parameter, and "
  "`⟺` logical equivalence.")
A("")
A("---")
A("")
A("## Lesson-level fields")
A("")
f("howto", "Shown to the learner before they begin", LES.get("howto"))
f("objectives[]", "Learning objectives", ["%d. %s" % (i, o) for i, o in enumerate(LES.get("objectives", []), 1)])
A("**Assumed prior knowledge** `prereq[]`")
A("")
for i, p in enumerate(LES.get("prereq", [])):
    A("- `prereq[%d]` **%s** — %s" % (i, p.get("name"), p.get("why")))
A("")
f("traps[]", "Misconceptions the lesson is built to pre-empt",
  ["- %s" % t for t in LES.get("traps", [])])
A("**Assessment policy** `mastery`")
A("")
m = LES.get("mastery", {})
A("- %d items drawn per attempt from a pool of %d, mix %s" % (
    m.get("draw", 0), len(POOL.get("items", [])),
    ", ".join("%s %s" % (v, k) for k, v in (m.get("diffMix") or {}).items())))
A("- pass mark %s%%, no hints during the test, retest after %s days" % (m.get("pass"), m.get("retestDays")))
A("- `mastery.note`: %s" % m.get("note"))
A("")
A("**Sources** `refs[]`")
A("")
for i, r in enumerate(LES.get("refs", [])):
    A("- `refs[%d]` **%s** — %s, %s (%s%s). %s" % (
        i, r.get("title"), r.get("site"), r.get("where"), r.get("type"),
        ", free" if r.get("free") else "", r.get("why")))
A("")
A("---")
A("")
A("## The lesson, scene by scene")
A("")

for i, s in enumerate(LES["scenes"]):
    p = "scenes[%d]" % i
    A("### Scene %d of %d — %s" % (i + 1, len(LES["scenes"]), s.get("title")))
    A("")
    A("`%s` · id `%s` · type `%s` (%s) · %s minutes%s" % (
        p, s.get("id"), s.get("kind"), KIND.get(s["kind"], ""), s.get("mins"),
        " · **optional JRF extension, core path completes without it**" if s.get("ext") else ""))
    A("")
    if s.get("objective"):
        f(p + ".objective", "Purpose", s["objective"])
    if s.get("body"):
        f(p + ".body[]", "Body", s["body"])
    if s.get("intro"):
        f(p + ".intro", "Intro", s["intro"])
    if s.get("problem"):
        f(p + ".problem", "Problem put to the learner", s["problem"])

    for k, it in enumerate(s.get("items", [])):
        if s["kind"] == "foundation":
            A("**Check %d** `%s.items[%d]`" % (k + 1, p, k))
            A("")
            A("- *asks:* %s" % it.get("ask"))
            A("- *expected answer* `.recall`: %s" % it.get("recall"))
            A("")
            rf = it.get("refresh") or []
            A("*Rebuild shown if the learner marks this shaky* `.refresh[]`:")
            A("")
            for z in (rf if isinstance(rf, list) else [rf]):
                A("> %s" % z)
                A("")
        elif s["kind"] == "recall":
            A("- `%s.items[%d]` **Q:** %s  \n  **A:** %s" % (p, k, it.get("q"), it.get("a")))
        elif s["kind"] == "trapcheck":
            A("- `%s.items[%d]` **Claim:** %s  \n  **Verdict: %s.** %s" % (
                p, k, it.get("claim"), "TRUE" if it.get("tf") else "FALSE", it.get("why")))
    if s["kind"] in ("recall", "trapcheck"):
        A("")

    for k, b in enumerate(s.get("blocks", [])):
        A("**Block %d — %s** `%s.blocks[%d]` *(type `%s`)*" % (k + 1, b.get("h"), p, k, b.get("t")))
        A("")
        A("%s" % b.get("body"))
        A("")

    if s.get("hints"):
        A("**Hint ladder, revealed one at a time** `%s.hints[]`" % p)
        A("")
        for k, h in enumerate(s["hints"]):
            A("%d. %s" % (k + 1, h))
        A("")

    steps = s.get("steps") or s.get("solution") or []
    key = "steps" if s.get("steps") else "solution"
    if steps:
        A("**%s** `%s.%s[]`" % ("Worked steps" if key == "steps" else "Model solution, hidden until requested", p, key))
        A("")
        for k, st in enumerate(steps):
            A("%d. `%s.%s[%d]` %s" % (k + 1, p, key, k, st.get("say")))
            if st.get("math"):
                A("")
                A("   ```")
                A("   %s" % st["math"])
                A("   ```")
                m = MATH.get(st["math"])
                if m and m.get("latex") and ("\\frac" in m["latex"] or "^{" in m["latex"]):
                    A("")
                    A("   Laid out:")
                    A("")
                    A("   $$" + m["latex"].replace("\n    ", " ") + "$$")
            bl = st.get("blank")
            if bl:
                A("")
                A("   - *learner is asked:* %s" % bl.get("prompt"))
                A("   - *accepted answer* `.blank.answer`: %s" % bl.get("answer"))
                if bl.get("accept"):
                    A("   - *also accepted:* %s" % "; ".join(bl["accept"]))
                if bl.get("hint"):
                    A("   - *hint:* %s" % bl.get("hint"))
            if st.get("why"):
                A("")
                A("   *why* `.why`: %s" % st["why"])
            A("")

    if s.get("table"):
        t = s["table"]
        A("**Reference table** `%s.table`" % p)
        A("")
        A("| " + " | ".join(t.get("head", [])) + " |")
        A("|" + "---|" * len(t.get("head", [])))
        for r in t.get("rows", []):
            A("| " + " | ".join(str(c) for c in r) + " |")
        A("")
        if t.get("caption"):
            A("*caption* `.caption`: %s" % t["caption"])
            A("")

    if s.get("flow"):
        fl = s["flow"]
        A("**Flow diagram** `%s.flow` — %s" % (p, fl.get("title") or fl.get("caption")))
        A("")
        if fl.get("caption") and fl.get("title"):
            A("*caption:* %s" % fl["caption"]); A("")
        if fl.get("alt"):
            A("*alt text* `.alt`: %s" % fl["alt"]); A("")
        lab = {n["id"]: n.get("label", n["id"]) for n in fl.get("nodes", [])}
        rows = {}
        for n in fl.get("nodes", []):
            rows.setdefault(n.get("r", 0), []).append(n)
        for r in sorted(rows):
            A("- row %d: %s" % (r + 1, "  |  ".join(
                n.get("label", "") for n in sorted(rows[r], key=lambda z: z.get("c", 0)))))
        A("- arrows: %s" % "; ".join(
            "%s →%s %s" % (lab.get(e["from"], e["from"]),
                           (" [" + e["label"] + "]") if e.get("label") else "",
                           lab.get(e["to"], e["to"]))
            for e in fl.get("edges", [])))
        A("")
        if fl.get("note"):
            A("*note shown under the diagram* `.note`: %s" % fl["note"]); A("")

    if s.get("answer"):
        f(p + ".answer", "Final answer given to the learner", s["answer"])
    if s.get("check"):
        f(p + ".check", "Self-check offered", s["check"])
    if s.get("after"):
        f(p + ".after", "What to take from it", s["after"])
    if s.get("aside"):
        A("**Aside — %s** `%s.aside.body`" % (s["aside"].get("h"), p))
        A("")
        A("%s" % s["aside"].get("body"))
        A("")
    if s.get("viz"):
        A("**Interactive element** `%s.viz` — live plot of type `%s`%s. Not reproducible in "
          "text; the surrounding body is written to stand alone, and whether it succeeds in "
          "doing so is worth your comment." % (
              p, s["viz"].get("type"),
              ", initial state " + ", ".join("%s=%s" % (k, v) for k, v in s["viz"].items() if k != "type")))
        A("")
    if s.get("ask") and s["ask"].get("q"):
        A("**Quick check before moving on** `%s.ask`" % p)
        A("")
        A("- *question:* %s" % s["ask"].get("q"))
        A("- *hint on request:* %s" % s["ask"].get("nudge"))
        A("")
    elif s.get("ask") and s["ask"].get("prompt"):
        A("**Suggested question to put to the assistant** `%s.ask` *(legacy shape: a "
          "pre-written prompt, not a self-test question — this scene has no quick check)*" % p)
        A("")
        A("- *button label* `.label`: %s" % s["ask"].get("label"))
        A("- *prompt* `.prompt`: %s" % s["ask"].get("prompt"))
        if s["ask"].get("tier"):
            A("- *model tier requested* `.tier`: %s *(configuration, not content)*" % s["ask"]["tier"])
        A("")
    if s.get("scenario"):
        sn = s["scenario"]
        A("**Optional deep-dive, opened on demand — %s** `%s.scenario`" % (sn.get("title"), p))
        A("")
        A("*teaser on the closed card:* %s" % sn.get("teaser"))
        A("")
        for z in sn.get("body", []):
            A("> %s" % z)
            A("")
        if sn.get("q"):
            A("*think-it-through question* `.q`: %s" % sn["q"])
            A("")
        if sn.get("answer"):
            A("*what the statistics says* `.answer`: %s" % sn["answer"])
            A("")
        if sn.get("link"):
            A("*link line* `.link`: %s" % sn["link"])
            A("")
        if sn.get("close"):
            A("*closing line:* %s" % sn["close"])
            A("")
    if s.get("setId"):
        A("Draws from the pool reproduced below. `%s.setId` = `%s`" % (p, s["setId"]))
        A("")
    A("---")
    A("")

R = LES.get("revision", {})
A("## Revision material `revision`")
A("")
A("**Revision sheet** `revision.sheet[]` (%d lines)" % len(R.get("sheet", [])))
A("")
for i, x in enumerate(R.get("sheet", [])):
    A("%d. `[%d]` %s" % (i + 1, i, x))
A("")
A("**Flashcards** `revision.cards[]`")
A("")
A("| Front | Back |")
A("|---|---|")
for c in R.get("cards", []):
    A("| %s | %s |" % (c[0], c[1]))
A("")
A("**Memory aids** `revision.tricks[]`")
A("")
for i, t in enumerate(R.get("tricks", [])):
    A("- `[%d]` **%s** — %s" % (i, t.get("hook"), t.get("why")))
A("")
for k, lab in [("shortcuts", "Elimination shortcuts for multiple-choice items"),
               ("remember", "If nothing else is remembered"), ("traps", "Errors to avoid")]:
    A("**%s** `revision.%s[]`" % (lab, k))
    A("")
    for i, x in enumerate(R.get(k, [])):
        A("- `[%d]` %s" % (i, x))
    A("")
A("---")
A("")

items = POOL.get("items", [])
A("## Mastery pool — all %d items with answer keys `qsets/%s`" % (len(items), POOL.get("source") or "inference_t1_mastery"))
A("")
A("Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to "
  "each option letter. Please check each item for a second defensible answer as well as "
  "for the correctness of its stated key and explanation.")
A("")
for n, q in enumerate(items, 1):
    A("### Q%d — `%s` *(%s, %s)*" % (n, q.get("id"), q.get("format"), q.get("diff")))
    A("")
    A("%s" % q.get("stem"))
    A("")
    if q.get("statements"):
        A("*Statements to judge* `.statements[]`:")
        A("")
        for L_, z in zip("ABCD", q["statements"]):
            A("- **%s.** %s" % (L_, z))
        A("")
    if q.get("items"):
        A("*Steps to order* `.items[]`:")
        A("")
        for z in q["items"]:
            A("- %s" % z)
        A("")
    if q.get("pairs"):
        A("*Pairs to match* `.pairs[]`:")
        A("")
        A("| Left | Right |")
        A("|---|---|")
        for pr in q["pairs"]:
            A("| %s | %s |" % (pr[0], pr[1]) if isinstance(pr, (list, tuple)) and len(pr) > 1
              else "| %s | |" % pr)
        A("")
    A("*Options* `.options[]`:")
    A("")
    for L_, o in zip("ABCD", q.get("options", [])):
        A("- **%s.** %s%s" % (L_, o, "  ← key" if L_ == q.get("answer") else ""))
    A("")
    if q.get("explanation"):
        A("*Explanation* `.explanation`: %s" % q["explanation"])
        A("")
    if q.get("check"):
        A("*Arithmetic check* `.check`: %s" % q["check"])
        A("")
    if q.get("verdicts"):
        A("*Verdict on each statement* `.verdicts`:")
        A("")
        for L_ in sorted(q["verdicts"]):
            v = q["verdicts"][L_]
            A("- **%s — %s.** %s" % (L_, "true" if v.get("tf") else "false", v.get("why")))
        A("")
A("---")
A("")
A("## Authoring and verification record `provenance`")
A("")
A("Reproduced verbatim. It records what changed in each version and how each derivation "
  "was checked, including the findings of the two previous review rounds and the reasons "
  "some of their recommendations were declined.")
A("")
A("> %s" % LES.get("provenance"))
A("")

slug = (TOPNO or LES.get("topicId")).replace(".", "-")
p = os.path.join(OUT, "lesson-%s-for-model-review.md" % slug)
io.open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("markdown  %s  (%d KB, %d lines)" % (p, len(("\n".join(L)).encode()) // 1024, len(L)))
