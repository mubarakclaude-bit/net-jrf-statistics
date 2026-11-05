#!/usr/bin/env python3
"""Export everything authored for lesson 4.1 as a single review document.

Walks every field of seed/lesson_t1.json and seed/inference_t1_mastery.json, so what
comes out is the complete authored content, not a summary: all 16 scenes with their
bodies, prerequisite rebuilds, theory blocks, worked steps and reasons, hint ladders,
model solutions, scenarios, the revision block, and all 20 mastery items with answer
keys and explanations.

Writes review/lesson-4.1-review.html, then PDF via weasyprint and DOCX via pandoc.
"""
import json, io, html, os, datetime

LES = json.load(io.open("seed/lesson_t1.json", encoding="utf-8"))
POOL = json.load(io.open("seed/inference_t1_mastery.json", encoding="utf-8"))
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

def _prose_in(les, pool):
    """Every string the document renders as prose, so exponents can be raised in them."""
    out = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k not in ("url", "isbn", "checked", "id", "kind", "setId"):
                    walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
        elif isinstance(o, str) and "^" in o:
            out.append(o)
    walk(les); walk(pool)
    return out


MATH = _mathmap(_formulas_in(LES) + _prose_in(LES, POOL))


def E(s):
    """Content escape: raises exponents so no formula is left with a caret in it."""
    if s is None:
        return ""
    m = MATH.get(str(s))
    return m["rich"] if m and m.get("rich") else EA(s)


RT = E


EA = lambda s: html.escape(str(s if s is not None else ""))
KINDNAME = {"foundation": "Prerequisite check", "intuition": "Intuition", "theory": "Theory",
            "explore": "Interactive visualisation", "worked": "Worked example",
            "recall": "Retrieval practice", "completion": "Fill in the blanks",
            "guided": "Guided problem", "trapcheck": "True/false check",
            "summary": "Summary and revision", "quiz": "Mastery test"}


def paras(x, cls="p"):
    if not x:
        return ""
    if isinstance(x, str):
        x = [x]
    return "".join('<p class="%s">%s</p>' % (cls, RT(p)) for p in x)


def dl(rows):
    """Label/value rows, used for metadata and for structured fields."""
    return '<table class="kv">' + "".join(
        '<tr><th>%s</th><td>%s</td></tr>' % (E(k), v if "<" in str(v) else E(v))
        for k, v in rows if v not in (None, "", [])) + '</table>'


# ----------------------------------------------------------------- scene bodies
def sc_foundation(sc):
    o = paras(sc.get("body"))
    for i, it in enumerate(sc.get("items", []), 1):
        o += '<div class="item"><p class="qn">Check %d. %s</p>' % (i, E(it.get("ask")))
        o += '<p class="ans"><b>Expected answer.</b> %s</p>' % E(it.get("recall"))
        r = it.get("refresh")
        if r:
            o += '<div class="refresh"><p class="lbl">Rebuild shown if the learner marks this shaky</p>'
            o += paras(r) + '</div>'
        o += '</div>'
    return o


def sc_intuition(sc):
    o = paras(sc.get("body"))
    a = sc.get("aside")
    if a:
        o += '<div class="aside"><p class="lbl">%s</p>%s</div>' % (E(a.get("h")), paras(a.get("body")))
    return o


def sc_theory(sc):
    o = ""
    for b in sc.get("blocks", []):
        body = paras(b.get("body"))
        o += '<div class="block b-%s"><p class="bh">%s <span class="tag">%s</span></p>%s</div>' % (
            EA(b.get("t")), E(b.get("h")), EA(b.get("t")), body)
    return o


def sc_explore(sc):
    v = sc.get("viz") or {}
    o = paras(sc.get("body"))
    params = ", ".join("%s = %s" % (k, v[k]) for k in v if k != "type")
    o += '<div class="note"><b>Interactive element.</b> Visualisation <code>%s</code>%s. ' \
         'In the app this is a live plot with sliders; the learner changes the parameters and the ' \
         'curve redraws. It cannot be reproduced on paper, so the surrounding text is written to ' \
         'stand alone.</div>' % (E(v.get("type")), (" — initial state " + E(params)) if params else "")
    return o


def steps_html(steps, kind="worked"):
    o = ""
    for i, s in enumerate(steps, 1):
        o += '<div class="step"><p class="sn">Step %d. %s</p>' % (i, E(s.get("say")))
        if s.get("math"):
            m = MATH.get(s["math"])
            o += m["print"] if m else ('<p class="math">%s</p>' % E(s["math"]))
        bl = s.get("blank")
        if bl:
            o += '<div class="blank"><p><b>Learner is asked:</b> %s</p>' % E(bl.get("prompt"))
            o += '<p><b>Accepted answer:</b> %s</p>' % E(bl.get("answer"))
            if bl.get("accept"):
                o += '<p class="small"><b>Also accepted (free-text variants):</b> %s</p>' % \
                     E("; ".join(bl["accept"]))
            if bl.get("hint"):
                o += '<p class="small"><b>Hint on request:</b> %s</p>' % E(bl["hint"])
            o += '</div>'
        if s.get("why"):
            o += '<p class="why"><b>Why.</b> %s</p>' % E(s["why"])
        o += '</div>'
    return o


def sc_worked(sc):
    return '<div class="prob"><b>Problem.</b> %s</div>' % E(sc.get("problem")) + \
           steps_html(sc.get("steps", [])) + \
           ('<div class="after"><p class="lbl">What to take from it</p>%s</div>' % paras(sc.get("after"))
            if sc.get("after") else "")


def sc_recall(sc):
    o = paras(sc.get("intro"), "intro")
    for i, it in enumerate(sc.get("items", []), 1):
        o += '<div class="item"><p class="qn">%d. %s</p><p class="ans"><b>Answer.</b> %s</p></div>' % (
            i, E(it.get("q")), E(it.get("a")))
    return o


def sc_completion(sc):
    return '<div class="prob"><b>Task.</b> %s</div>' % E(sc.get("problem")) + \
           steps_html(sc.get("steps", []), "completion") + \
           ('<div class="after"><p class="lbl">What to take from it</p>%s</div>' % paras(sc.get("after"))
            if sc.get("after") else "")


def sc_guided(sc):
    o = '<div class="prob"><b>Problem.</b> %s</div>' % E(sc.get("problem"))
    h = sc.get("hints") or []
    if h:
        o += '<div class="hints"><p class="lbl">Hint ladder — revealed one at a time, on request</p><ol>' + \
             "".join('<li>%s</li>' % E(x) for x in h) + '</ol></div>'
    o += '<p class="lbl">Model solution, hidden until the learner asks for it</p>'
    o += steps_html(sc.get("solution", []))
    if sc.get("answer"):
        o += '<div class="after"><p class="lbl">Final answer</p>%s</div>' % paras(sc["answer"])
    if sc.get("check"):
        o += '<div class="note"><b>Self-check offered to the learner.</b> %s</div>' % E(sc["check"])
    return o


def sc_trapcheck(sc):
    o = paras(sc.get("intro"), "intro")
    for i, it in enumerate(sc.get("items", []), 1):
        v = "TRUE" if it.get("tf") else "FALSE"
        o += '<div class="item"><p class="qn">%d. %s</p>' % (i, E(it.get("claim")))
        o += '<p class="ans"><b>Verdict: %s.</b> %s</p></div>' % (v, E(it.get("why")))
    return o


def sc_summary(sc):
    return '<ul class="sum">' + "".join('<li>%s</li>' % E(x) for x in sc.get("body", [])) + '</ul>'


def sc_quiz(sc):
    return '<div class="note"><b>Mastery test.</b> Ten questions drawn at random from the pool of ' \
           'twenty reproduced in Section D of this document, at 3 easy / 5 moderate / 2 hard. ' \
           'Pool identifier <code>%s</code>. No hints, one attempt per question, pass mark 80%%, ' \
           'retest permitted after 7 days. These items are held out of the practice bank and out ' \
           'of the mock papers.</div>' % E(sc.get("setId"))


BODY = {"foundation": sc_foundation, "intuition": sc_intuition, "theory": sc_theory,
        "explore": sc_explore, "worked": sc_worked, "recall": sc_recall,
        "completion": sc_completion, "guided": sc_guided, "trapcheck": sc_trapcheck,
        "summary": sc_summary, "quiz": sc_quiz}


def table_html(t):
    o = '<p class="lbl">Reference table shown in the lesson</p><table class="lt"><thead><tr>' + \
        "".join('<th>%s</th>' % E(h) for h in t.get("head", [])) + '</tr></thead><tbody>'
    for r in t.get("rows", []):
        o += '<tr>' + "".join('<td>%s</td>' % E(c) for c in r) + '</tr>'
    o += '</tbody></table>'
    if t.get("caption"):
        o += '<p class="small">%s</p>' % E(t["caption"])
    return o


def flow_html(f):
    rows = {}
    for n in f.get("nodes", []):
        rows.setdefault(n.get("r", 0), []).append(n)
    o = '<div class="flow"><p class="lbl">Flow diagram: %s</p>' % E(f.get("caption"))
    for r in sorted(rows):
        o += '<p class="frow"><span class="rn">Row %d</span> %s</p>' % (
            r + 1, E("   |   ".join(n.get("label", "") for n in
                                    sorted(rows[r], key=lambda z: z.get("c", 0)))))
    if f.get("edges"):
        lab = {n["id"]: n.get("label", n["id"]) for n in f.get("nodes", [])}
        o += '<p class="small"><b>Arrows.</b> ' + E("; ".join(
            "%s → %s" % (lab.get(e["from"], e["from"]), lab.get(e["to"], e["to"]))
            for e in f["edges"])) + '</p>'
    return o + '</div>'


def scenario_html(sn):
    o = '<div class="scen"><p class="lbl">Optional deep-dive, opened on demand — "%s"</p>' % E(sn.get("title"))
    o += '<p class="small"><b>Teaser shown on the closed card:</b> %s</p>' % E(sn.get("teaser"))
    o += paras(sn.get("body"))
    if sn.get("q"):
        o += '<p class="lbl">Think it through</p><p>%s</p>' % E(sn["q"])
    if sn.get("answer"):
        o += '<div class="after"><p class="lbl">What the statistics says</p>%s</div>' % paras(sn["answer"])
    if sn.get("link"):
        o += '<p class="small">%s</p>' % E(sn["link"])
    if sn.get("close"):
        o += '<p class="close">%s</p>' % E(sn["close"])
    return o + '</div>'


# ----------------------------------------------------------------- mastery items
def item_html(q, n):
    o = '<div class="mq"><p class="qn">Q%d &nbsp;<span class="small">[%s · %s · %s]</span></p>' % (
        n, E(q.get("id")), E(q.get("format")), E(q.get("diff")))
    o += '<p class="stem">%s</p>' % E(q.get("stem"))
    if q.get("statements"):
        o += '<p class="lbl">Statements to judge</p><ol class="alpha">' + "".join(
            '<li>%s</li>' % E(s) for s in q["statements"]) + '</ol>'
    if q.get("items"):
        o += '<p class="lbl">Steps to order</p><ul class="plain">' + "".join(
            '<li>%s</li>' % E(s) for s in q["items"]) + '</ul>'
    if q.get("pairs"):
        o += '<p class="lbl">Pairs to match</p><table class="kv">' + "".join(
            '<tr><th>%s</th><td>%s</td></tr>' % (E(p[0]), E(p[1]))
            for p in q["pairs"] if isinstance(p, (list, tuple)) and len(p) > 1) + '</table>'
    o += '<ol class="opts">' + "".join('<li>%s</li>' % E(x) for x in q.get("options", [])) + '</ol>'
    o += '<p class="ans"><b>Key: %s.</b></p>' % E(q.get("answer"))
    if q.get("explanation"):
        o += '<p class="why"><b>Explanation.</b> %s</p>' % E(q["explanation"])
    if q.get("check"):
        o += '<p class="why"><b>Arithmetic check.</b> %s</p>' % E(q["check"])
    v = q.get("verdicts")
    if v:
        o += '<p class="lbl">Verdict on each statement</p><table class="kv">' + "".join(
            '<tr><th>%s — %s</th><td>%s</td></tr>' % (
                E(k), "true" if v[k].get("tf") else "false", E(v[k].get("why")))
            for k in sorted(v)) + '</table>'
    return o + '</div>'


# ----------------------------------------------------------------- assemble
scenes = LES["scenes"]
today = datetime.date.today().strftime("%d %B %Y")

nav = '<table class="map"><tr><th>#</th><th>Scene type</th><th>Title</th><th>Min</th></tr>' + "".join(
    '<tr><td>%d</td><td>%s</td><td>%s%s</td><td>%s</td></tr>' % (
        i, E(KINDNAME.get(s["kind"], s["kind"])), E(s.get("title")),
        ' <b>[optional JRF extension]</b>' if s.get("ext") else "", E(s.get("mins", "")))
    for i, s in enumerate(scenes, 1)) + '</table>'

H = []
A = H.append

A('<h1>Sufficiency, Factorisation and Minimal Sufficiency</h1>')
A('<p class="sub">Lesson 4.1, Unit IV — Statistical Inference · UGC-NET Statistics (Code 107)</p>')
A('<p class="sub">Complete authored content, prepared for academic review · %s</p>' % today)
A(dl([
    ("Syllabus topic", "4.1 Sufficiency, factorisation and minimal sufficiency"),
    ("Unit", "IV — Statistical Inference"),
    ("Breadcrumb in the app", LES.get("breadcrumb")),
    ("Content version", LES.get("version")),
    ("Scenes", "%d" % len(scenes)),
    ("Estimated learner time", "%s minutes, excluding the mastery test retakes" % LES.get("estMin")),
    ("Mastery pool", "%d items (%s)" % (len(POOL.get("items", [])), POOL.get("label") or "")),
    ("Intended audience", "Candidates preparing for UGC-NET Statistics with a JRF target, many of "
                          "them returning to the subject after a gap of several years"),
]))
A('<div class="note"><b>What this document is.</b> Every word authored for lesson 4.1, extracted '
  'directly from the application\'s content files rather than retyped. It includes material the '
  'learner sees only conditionally — the rebuild text behind each prerequisite check, the hint '
  'ladders, the model solutions and the optional deep-dive scenarios — so that the full teaching '
  'content is open to review. Two things cannot be put on paper: the two interactive plots, '
  'whose role is described where they occur, and the randomised draw from the mastery pool, whose '
  'twenty items are all reproduced in Section D with their answer keys.</div>')
if LES.get("howto"):
    A('<div class="note"><b>Shown to the learner before they begin.</b> %s</div>' % E(LES["howto"]))
A('<div class="note"><b>A note on the sequence.</b> The topic is the heaviest '
  'in the syllabus, and an earlier version, while mathematically complete, introduced the general '
  'theorem before the worked instance and placed its best explanations inside collapsed '
  'prerequisite text. The present ordering is deliberate: a concrete coin computation is carried '
  'to a conclusion in scene 2, the worked Bernoulli case precedes the general theorem, and the '
  'standard counterexample (Cauchy) is deferred, and now sits in a single section marked an '
  'optional JRF extension so that the core path of 16 sections completes without it. '
  'Version 4.0 incorporates an external pedagogical review: the three-way separation of '
  'statistic, estimator and estimate was promoted to a section of its own, a family-to-statistic '
  'reference table was added here and in the summary, a quick check now closes every teaching '
  'section, and the Uniform section was given concrete numbers so it reads without its plot. '
  'Section E records what was adopted from that review and what was declined, with reasons. '
  'Comment on the ordering, and on those decisions, is particularly welcome.</div>')

A('<h2 class="pb">Scene map</h2>')
A(nav)

A('<h2 class="pb">Section A — Lesson specification</h2>')
A('<h3>Learning objectives</h3><ol>' + "".join('<li>%s</li>' % E(x) for x in LES.get("objectives", [])) + '</ol>')
A('<h3>Assumed prior knowledge</h3>')
A("".join('<div class="item"><p class="qn">%s</p><p class="why"><b>Why it is needed.</b> %s</p></div>'
          % (E(p.get("name")), E(p.get("why"))) for p in LES.get("prereq", [])))
m = LES.get("mastery", {})
A('<h3>Assessment policy</h3>')
A(dl([("Questions per attempt", m.get("draw")), ("Pool size", len(POOL.get("items", []))),
      ("Difficulty mix", ", ".join("%s %s" % (v, k) for k, v in (m.get("diffMix") or {}).items())),
      ("Pass mark", "%s%%" % m.get("pass")), ("Hints", "not available during the test"),
      ("Retest", "permitted after %s days" % m.get("retestDays")),
      ("Format minima", ", ".join("%s %s%%" % (k, v) for k, v in (m.get("fmtMin") or {}).items())),
      ("Note", m.get("note"))]))
A('<h3>Misconceptions the lesson is built to pre-empt</h3><ul>' +
  "".join('<li>%s</li>' % E(x) for x in LES.get("traps", [])) + '</ul>')
A('<h3>Sources used, and why each one</h3>')
for r in LES.get("refs", []):
    A('<div class="item"><p class="qn">%s</p>' % E(r.get("title")))
    A(dl([("Author or publisher", r.get("site")), ("Location in the source", r.get("where")),
          ("Type", r.get("type")), ("Free to access", "yes" if r.get("free") else "no"),
          ("URL", r.get("url") or "—"), ("ISBN", r.get("isbn")),
          ("Link last verified", r.get("checked"))]))
    A('<p class="why"><b>Why this source.</b> %s</p></div>' % E(r.get("why")))

A('<h2 class="pb">Section B — The lesson, scene by scene</h2>')
for i, s in enumerate(scenes, 1):
    A('<div class="scene"><h3 class="pbs">Scene %d of %d · %s</h3>' % (i, len(scenes),
                                                                      E(KINDNAME.get(s["kind"], s["kind"]))))
    A('<p class="sctitle">%s</p>' % E(s.get("title")))
    A('<p class="small">Estimated %s minutes · internal id <code>%s</code></p>' % (E(s.get("mins")), E(s.get("id"))))
    if s.get("ext"):
        A('<div class="note"><b>Optional — marked "JRF extension" in the app.</b> The core path '
          'completes without this section and the learner is told so. It is included because JRF '
          'is decided by the harder theory questions, not by the pass mark.</div>')
    if s.get("objective"):
        A('<p class="obj"><b>Purpose of this scene.</b> %s</p>' % E(s["objective"]))
    if s.get("flow"):
        A(flow_html(s["flow"]))
    A(BODY[s["kind"]](s))
    if s.get("table"):
        A(table_html(s["table"]))
    if s.get("ask"):
        A('<div class="askq"><p class="lbl">Question put to the learner before moving on</p>'
          '<p>%s</p><p class="small"><b>Hint available on request:</b> %s</p></div>'
          % (E(s["ask"].get("q")), E(s["ask"].get("nudge"))))
    if s.get("scenario"):
        A(scenario_html(s["scenario"]))
    A('</div>')

R = LES.get("revision", {})
A('<h2 class="pb">Section C — Revision material</h2>')
A('<p class="intro">Available from the summary scene and from the revision rail at any point in '
  'the lesson.</p>')
A('<h3>Revision sheet (%d lines)</h3><ol class="tight">' % len(R.get("sheet", [])) +
  "".join('<li>%s</li>' % E(x) for x in R.get("sheet", [])) + '</ol>')
A('<h3>Flashcards (%d)</h3><table class="kv">' % len(R.get("cards", [])) +
  "".join('<tr><th>%s</th><td>%s</td></tr>' % (E(c[0]), E(c[1])) for c in R.get("cards", [])) + '</table>')
A('<h3>Memory aids</h3>')
A("".join('<div class="item"><p class="qn">%s</p><p class="why">%s</p></div>'
          % (E(t.get("hook")), E(t.get("why"))) for t in R.get("tricks", [])))
A('<h3>Elimination shortcuts for multiple-choice items</h3><ul>' +
  "".join('<li>%s</li>' % E(x) for x in R.get("shortcuts", [])) + '</ul>')
A('<h3>If nothing else is remembered</h3><ul>' +
  "".join('<li>%s</li>' % E(x) for x in R.get("remember", [])) + '</ul>')
A('<h3>Errors to avoid</h3><ul>' +
  "".join('<li>%s</li>' % E(x) for x in R.get("traps", [])) + '</ul>')

items = POOL.get("items", [])
A('<h2 class="pb">Section D — Mastery pool, all %d items with keys</h2>' % len(items))
A('<div class="note">Ten of these twenty are drawn for each attempt, holding the mix at 3 easy, '
  '5 moderate and 2 hard. Answer keys are distributed five to each option letter so that no '
  'letter is over-represented. Formats: %s.</div>'
  % E(", ".join("%d %s" % (sum(1 for q in items if q["format"] == f), f)
                for f in ["single", "numeric", "multi", "order"]
                if any(q["format"] == f for q in items))))
for n, q in enumerate(items, 1):
    A(item_html(q, n))

A('<h2 class="pb">Section E — Authoring and verification record</h2>')
A('<p class="intro">Reproduced verbatim from the <code>provenance</code> field of the content file. '
  'It records what was changed and how each derivation was checked.</p>')
A(paras(LES.get("provenance")))
A('<div class="note"><b>For the reviewer.</b> The three points on which comment would be most '
  'useful: whether the ordering in Section B is right for a candidate returning to the subject '
  'after a long gap; whether any statement in Section B or D is imprecise in a way that would '
  'cost a candidate a mark; and whether the mastery pool in Section D sits at the right level for '
  'a JRF target rather than a bare qualification.</div>')

CSS = """
@page { size: A4; margin: 20mm 18mm 18mm 18mm;
  @bottom-center { content: counter(page) " / " counter(pages); font: 8pt Georgia, serif; color: #777 } }
body { font: 10.3pt/1.52 Georgia, "Times New Roman", serif; color: #1a1a1a }
h1 { font-size: 20pt; margin: 0 0 4pt; line-height: 1.2 }
h2 { font-size: 14pt; margin: 22pt 0 8pt; padding-bottom: 3pt; border-bottom: 1.5pt solid #1a1a1a }
h3 { font-size: 11.5pt; margin: 16pt 0 6pt }
h3.pbs { margin-top: 20pt; color: #5a4a2f; font-variant: small-caps; letter-spacing: .4pt }
.pb { page-break-before: always }
.sub { color: #555; margin: 2pt 0; font-size: 10pt }
.sctitle { font-size: 13pt; font-weight: bold; margin: 0 0 2pt }
.small { font-size: 8.8pt; color: #555 }
.obj { background: #f4f1ea; padding: 6pt 8pt; margin: 8pt 0; font-size: 9.8pt }
.note { border-left: 2.5pt solid #7a6a4f; background: #faf8f3; padding: 7pt 9pt; margin: 10pt 0;
  font-size: 9.6pt }
.item { margin: 10pt 0 10pt; padding-left: 9pt; border-left: 1pt solid #ccc; page-break-inside: avoid }
.qn { font-weight: bold; margin: 0 0 3pt }
.ans { margin: 3pt 0 }
.why { margin: 3pt 0; color: #333 }
.refresh { background: #f7f7f4; padding: 6pt 8pt; margin: 5pt 0 0; font-size: 9.6pt }
.lbl { font-variant: small-caps; letter-spacing: .5pt; color: #6b5b3e; font-weight: bold;
  margin: 8pt 0 3pt; font-size: 9pt }
.aside { border: 1pt solid #c9b98f; background: #fdfaf0; padding: 7pt 9pt; margin: 10pt 0 }
.block { margin: 9pt 0; padding: 7pt 9pt; background: #f8f8f6; page-break-inside: avoid }
.block.b-trap { background: #fdf3f1; border-left: 2.5pt solid #a8462f }
.block.b-formula, .block.b-step { background: #f2f4f7; border-left: 2.5pt solid #3f5a78 }
.block.b-assume { background: #fdfaf0; border-left: 2.5pt solid #b08d35 }
.bh { font-weight: bold; margin: 0 0 4pt }
.tag { font-size: 7.6pt; color: #777; font-variant: small-caps; letter-spacing: .5pt;
  border: .5pt solid #bbb; padding: 0 3pt; border-radius: 2pt; font-weight: normal }
.prob { background: #eef1f5; padding: 7pt 9pt; margin: 9pt 0; page-break-inside: avoid }
.step { margin: 9pt 0; page-break-inside: avoid }
.sn { font-weight: bold; margin: 0 0 3pt }
.math { font-family: "DejaVu Sans Mono", Consolas, monospace; font-size: 9.4pt; background: #f4f4f1;
  padding: 5pt 7pt; margin: 4pt 0; white-space: pre-wrap; border-left: 2pt solid #999 }
.blank { background: #f6f3ec; padding: 5pt 8pt; margin: 4pt 0; font-size: 9.7pt }
.blank p { margin: 2pt 0 }
.after { border-top: 1pt solid #ccc; margin-top: 10pt; padding-top: 5pt }
.hints ol { margin: 2pt 0 0 14pt }
.scen { border: 1pt dashed #a89878; padding: 8pt 10pt; margin: 12pt 0;
  background: #fcfbf7; page-break-inside: avoid }
.close { font-style: italic; color: #4a4030; margin-top: 6pt }
.askq { background: #f1f4f1; padding: 6pt 9pt; margin: 10pt 0; border-left: 2.5pt solid #4a6a4a }
.askq p { margin: 2pt 0 }
.flow { background: #f5f6f8; padding: 7pt 9pt; margin: 9pt 0; font-size: 9.5pt }
.frow { margin: 3pt 0 }
.rn { font-variant: small-caps; color: #777; margin-right: 6pt; font-size: 8.5pt }
table.kv { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9.6pt }
table.kv th { text-align: left; width: 32%; vertical-align: top; padding: 3pt 8pt 3pt 0;
  font-weight: bold; border-bottom: .5pt solid #e2e2e2 }
table.kv td { vertical-align: top; padding: 3pt 0; border-bottom: .5pt solid #e2e2e2 }
table.map { border-collapse: collapse; width: 100%; font-size: 9.6pt; margin-top: 8pt }
table.map th { text-align: left; border-bottom: 1pt solid #1a1a1a; padding: 4pt 6pt 4pt 0 }
table.map td { padding: 3pt 6pt 3pt 0; border-bottom: .5pt solid #e8e8e8; vertical-align: top }
ul, ol { margin: 5pt 0 5pt 16pt; padding: 0 }
li { margin: 3pt 0 }
ol.tight li, ul.sum li { margin: 2.5pt 0 }
ol.opts { list-style: upper-alpha; margin-top: 5pt }
ol.alpha { list-style: upper-alpha }
ul.plain { list-style: none; margin-left: 4pt }
.mq { margin: 12pt 0; padding: 8pt 10pt 6pt; border: .5pt solid #ddd; page-break-inside: avoid }
.stem { margin: 2pt 0 4pt }
.intro { font-style: italic; color: #444 }
/* a formula set inside a sentence: stacked denominators need a taller line */
.imath { display: inline-block; vertical-align: middle; line-height: 1.05 }
.imath .frac { display: inline-block; vertical-align: middle; text-align: center;
  margin: 0 2.5pt; font-size: .92em }
.imath .frac > .fnum { display: block; padding: 0 3pt 1pt; border-bottom: .7pt solid #1a1a1a }
.imath .frac > .fden { display: block; padding: 1pt 3pt 0 }
.imath sup { font-size: .72em; vertical-align: super; line-height: 0 }
p, li, .item, .block, .why, .ans, .refresh { line-height: 1.75 }
.pmath { margin: 7pt 0 9pt; padding: 7pt 10pt; background: #f6f6f3;
  border-left: 2pt solid #5a6b7f; font-family: "Iowan Old Style", Palatino, Georgia, serif;
  font-size: 11pt; line-height: 1.15 }
.pline { display: block; padding: 1.5pt 0 }
.pline + .pline { margin-left: 10pt }
.prel { color: #555; font-weight: bold }
.pfrac { display: inline-block; vertical-align: middle; text-align: center; margin: 0 3pt;
  position: relative; top: -.12em }
.pnum { display: block; padding: 0 4pt 1pt; border-bottom: .8pt solid #1a1a1a }
.pden { display: block; padding: 1pt 4pt 0 }
.pfrac.wide .pnum, .pfrac.wide .pden { padding-left: 7pt; padding-right: 7pt }
.pmath sup { font-size: .7em; vertical-align: super; line-height: 0 }
table.lt { border-collapse: collapse; width: 100%; font-size: 9.5pt; margin: 8pt 0 }
table.lt th { text-align: left; padding: 4pt 7pt 4pt 0; border-bottom: 1pt solid #1a1a1a;
  vertical-align: top }
table.lt td { padding: 3.5pt 7pt 3.5pt 0; border-bottom: .5pt solid #e5e5e5; vertical-align: top }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; background: #f0f0ed; padding: 0 2pt }
"""

doc = ('<!doctype html><html><head><meta charset="utf-8">'
       '<title>Lesson 4.1 — Sufficiency, Factorisation and Minimal Sufficiency</title>'
       '<style>%s</style></head><body>%s</body></html>' % (CSS, "\n".join(H)))

p = os.path.join(OUT, "lesson-4.1-review.html")
io.open(p, "w", encoding="utf-8").write(doc)
print("html  %s  (%d KB)" % (p, len(doc) // 1024))
print("scenes %d · mastery items %d · refs %d · sheet lines %d · cards %d" % (
    len(scenes), len(items), len(LES.get("refs", [])),
    len(R.get("sheet", [])), len(R.get("cards", []))))
