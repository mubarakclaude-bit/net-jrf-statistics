#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SKELETON for an authoring script. Copy this, do not read EXAMPLE.py unless you need to see
prose style — EXAMPLE.py is a fully worked lesson and costs about 19k tokens to read, while this
file costs about 3k and carries the same structure.

THIS DOES NOT RUN AS-IS. Every <...> is yours to fill, and the floors noted inline are enforced
by addlesson.sh — it will tell you precisely which one you missed.

Order of work (SPEC.md section 6 explains why):
  1. Read the variant bank for the topic: seed/*_pyq_variants.json, filtered on srcQ.
  2. VERIFY EVERY FIGURE by computing it, in one script. Then write prose around verified numbers.
  3. Fill this in. 4. ./addlesson.sh. 5. Push. 6. node test.js && node clicktest.py
"""
import json, io, os, re

OUT  = "seed/lesson_<stem>.json"        # MUST match the <seed-stem> argument to addlesson.sh
POOL = "seed/<module>_t<n>_mastery.json"

S = []   # scenes, in this order. 11-16 of them, excluding any marked ext.

# 1 ── foundation. 3-5 prereq checks, each ask / recall / refresh. refresh must teach, not hint.
S.append({"kind":"foundation","id":"s0","mins":7,"title":"<...>","objective":"<...>",
 "ask":{"q":"<...>","nudge":"<...>"},
 "body":["<two or three paragraphs: what this topic is for, before any symbol>"],
 "items":[{"ask":"<question>","recall":"<one-line answer>",
           "refresh":["<rebuild it from the base, for someone who marked this shaky>","<...>"]}]})

# 2 ── intuition. The idea in words, plus the first of at least TWO scenarios (400+ chars body).
S.append({"kind":"intuition","id":"s1","mins":7,"title":"<...>","objective":"<...>",
 "body":["<...>"],
 "scenario":{"teaser":"<one line, shown collapsed>","title":"<...>",
             "body":["<400+ characters across these strings — a real situation, not a word problem>"],
             "q":"<...>","answer":"<...>"},
 "ask":{"q":"<...>","nudge":"<...>"}})

# 3 ── explore. Needs a viz whose type is in VIZ_OK (SPEC.md section 5 lists all 18). PREFER REUSE.
S.append({"kind":"explore","id":"s2","mins":7,"title":"<...>","objective":"<...>",
 "viz":{"type":"<one of VIZ_OK>","caption":"<what to notice>"},
 "body":["<walk them through two or three settings and what each shows>"],
 "ask":{"q":"<...>","nudge":"<...>"}})

# 4 ── theory. blocks[].t is "formula" | "step" | "def". At least one scene carries a flow diagram.
S.append({"kind":"theory","id":"s3","mins":9,"title":"<...>","objective":"<...>",
 "blocks":[{"t":"formula","h":"<...>","body":"<the statement, exactly>"},
           {"t":"step","h":"<...>","body":"<...>"},
           {"t":"def","h":"<...>","body":"<...>"}],
 "table":{"caption":"<...>","head":["<...>"],"rows":[["<...>"]]},
 "flow":{"title":"<...>","alt":"<describe it for a screen reader>",
         "nodes":[{"id":"a","r":0,"c":1,"label":"<...>","kind":"start"},
                  {"id":"b","r":1,"c":1,"label":"<...>","kind":"step"},
                  {"id":"c","r":2,"c":1,"label":"<...>","kind":"end"}],
         "edges":[{"from":"a","to":"b"},{"from":"b","to":"c"}],
         "note":"<...>"},
 "ask":{"q":"<...>","nudge":"<...>"}})

# 5 ── worked. Every step shown. say / math / why on each.
S.append({"kind":"worked","id":"s4","mins":8,"title":"<...>","objective":"<...>",
 "ask":{"q":"<...>","nudge":"<...>"},
 "problem":"<...>",
 "steps":[{"say":"<what we are about to do>","math":"<the algebra, carried in full>",
           "why":"<why this step, and the check that it is right>"}],
 "after":"<answer the scene's own ask, and name the transferable habit>"})

# 6 ── recall. Retrieval before the harder half. 5-6 items.
S.append({"kind":"recall","id":"s5","mins":2,"title":"Pause and recall","objective":"<...>",
 "intro":"Answer each before revealing it.",
 "items":[{"q":"<...>","a":"<...>"}]})

# 7 ── completion. Steps WITH GAPS: the fade begins. accept[] holds the wordings to allow.
S.append({"kind":"completion","id":"s6","mins":8,"title":"Your turn","objective":"<...>",
 "problem":"<...>",
 "steps":[{"say":"<the setup>",
           "blank":{"prompt":"<what to supply>","answer":"<the expected answer>",
                    "accept":["<other acceptable wordings>"],"hint":"<a nudge, not the answer>"},
           "why":"<...>"}],
 "after":"<the structure to carry away>"})

# 8 ── theory (second pass: the harder result, or the reason the first one works).
S.append({"kind":"theory","id":"s7","mins":7,"title":"<...>","objective":"<...>",
 "blocks":[{"t":"step","h":"<...>","body":"<...>"}],
 "ask":{"q":"<...>","nudge":"<...>"}})

# 9 ── guided. Hints only: 3 rungs, direction -> method -> next step. NEVER the answer.
#      Carries the second scenario. At least TWO guided scenes in the lesson.
S.append({"kind":"guided","id":"s8","mins":8,"title":"On your own","objective":"<...>",
 "problem":"<...>",
 "hints":["<direction: what to identify first>","<method: which result applies>",
          "<next step: the one operation>"],
 "answer":"<...>",
 "check":"<the part that looks wrong and is not, or the sanity test>",
 "scenario":{"teaser":"<...>","title":"<...>","body":["<400+ chars>"],"q":"<...>","answer":"<...>"},
 "solution":[{"say":"<...>","math":"<...>","why":"<...>"}]})

# 10 ── trapcheck. 6 claims, each tf a real boolean, each why explaining the error.
S.append({"kind":"trapcheck","id":"s9","mins":6,"title":"Six statements","objective":"<...>",
 "intro":"Decide true or false on all six before revealing any.",
 "items":[{"claim":"<...>","tf":False,"why":"<why it is wrong, and what is true instead>"}]})

# 11 ── guided (TRANSFER). A case the lesson has NOT shown, so it tests method selection.
S.append({"kind":"guided","id":"s10","mins":8,"title":"<...>","objective":"<...>",
 "problem":"<...>","hints":["<...>"],"answer":"<...>","check":"<...>",
 "solution":[{"say":"<...>","math":"<...>","why":"<...>"}]})

# 12 ── theory. Where this sits against the rest of the syllabus. Cross-reference, never repeat.
S.append({"kind":"theory","id":"s11","mins":6,"title":"<...>","objective":"<...>",
 "blocks":[{"t":"step","h":"<...>","body":"<...>"}],
 "ask":{"q":"<...>","nudge":"<...>"}})

# 13 ── recall (second). The parts most likely to fade.
S.append({"kind":"recall","id":"s12","mins":2,"title":"Second recall","objective":"<...>",
 "intro":"Answer, then reveal.","items":[{"q":"<...>","a":"<...>"}]})

# 14 ── summary. What they can now do UNAIDED.
S.append({"kind":"summary","id":"s13","mins":3,"title":"What you should now be able to do",
 "objective":"<...>","body":["<one line per capability>"]})

# 15 ── optional. ext:True keeps it out of the core count and out of estMin.
S.append({"kind":"theory","id":"s14","mins":8,"ext":True,"title":"<the derivation, in full>",
 "objective":"<...>","blocks":[{"t":"step","h":"<...>","body":"<...>"}],
 "ask":{"q":"<...>","nudge":"<...>"}})

# 16 ── quiz. setId must equal the POOL stem.
S.append({"kind":"quiz","id":"s15","mins":12,"title":"Mastery test",
 "objective":"Demonstrate it independently, on questions you have not seen.",
 "setId":"<module>_t<n>_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id":"<storeDocId>", "topicId":"<module>-t<n>", "moduleId":"<module>",
 "title":"<...>", "breadcrumb":"<Module> → <area> → <this topic>",
 "engine":"B", "engineName":"<one line: the one move this topic is about>",
 "version":"1.0", "status":"approved",
 "estMin":sum(s["mins"] for s in CORE),
 "objectives":["<4-6, each something they can DO>"],
 "prereq":[{"id":"p1","name":"<...>","why":"<why this lesson needs it>"}],   # 3-4, feed scene 1
 "traps":["<the errors this topic actually produces, one line each>"],
 "revision":{
   "sheet":["<the whole lesson as scannable lines, with the verified figures>"],
   "cards":[["<front>","<back>"]],              # [front, back] pairs only
   "tricks":["<3+ mnemonics>"], "shortcuts":["<3+ values worth memorising>"],
   "remember":["<2+ 'if you remember nothing else' lines>"]},
 "howto":"<how to use this lesson: which scenes are the lesson if short of time, what it "
         "deliberately does NOT cover because another topic owns it>",
 "refs":[{"title":"<...>","where":"<exact chapter or lecture>","site":"<author or site>",
          "url":"<verified, or empty>","type":"<Textbook | Free online textbook | Video course>",
          "free":False,"checked":"<YYYY-MM-DD>","why":"<what it is for, at which scene>"}],
 "mastery":{"minQ":10,"pass":80,"draw":10,"fmtMin":{"numeric":70,"multi":70},
            "diffMix":{"easy":3,"moderate":5,"hard":2},"noHints":True,"retestDays":7,
            "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on "
                   "numerical and multi-statement items, answered without hints. Each paper is "
                   "drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style "
                   "paper; NTA publishes no official difficulty split."},
 "provenance":"<the anchor question and whether it was answered wrongly; WHAT YOU VERIFIED AND "
              "HOW, with the figures; the scope boundary against neighbouring topics; anything "
              "you found wrong in the bank>",
 "scenes":S}

# ─────────────────────────────── pool: exactly 20 items ───────────────────────────────
# 6 easy / 10 moderate / 4 hard. >=4 numeric, EACH with a check. >=2 multi. 4 options each.
# No answer letter on more than 8 of 20. No explanation may cite its own answer as an option.
def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id":"<mod>-t<n>-m-%02d"%i, "format":fmt, "topic":"<module>-t<n>",
         "diff":diff, "stem":stem, "options":opts, "answer":ans, "explanation":exp}
    d.update(kw); return d

def verd(a,b,c,dd):
    return {"A":{"tf":a[0],"why":a[1]},"B":{"tf":b[0],"why":b[1]},
            "C":{"tf":c[0],"why":c[1]},"D":{"tf":dd[0],"why":dd[1]}}

I = []
# easy ×6, moderate ×10, hard ×4. Author each with the answer wherever it falls; WANT fixes it.
I.append(q(1,"single","easy","<stem>",["<correct>","<plausible>","<plausible>","<plausible>"],
           "A","<why the key is right AND why each distractor is tempting>"))
I.append(q(2,"numeric","easy","<stem>",["<...>"]*4,"A","<...>",
           check="<a terminal sanity line usable under exam pressure>"))
I.append(q(3,"multi","moderate","<stem>",
           ["A, B and C only","A and C only","B and D only","A, B, C and D"],"A","<...>",
           statements=["<s1>","<s2>","<s3>","<s4>"],
           verdicts=verd((True,"<why>"),(True,"<why>"),(True,"<why>"),(False,"<why>"))))

# Key spread: author freely, then remap. swapletters rewrites "option C" AND "options B and C"
# inside explanations and check lines — a naive version once left an item ruling out its own answer.
LET = "ABCD"
WANT = {"<mod>-t<n>-m-01":"C"}   # id -> desired letter, for about 18 of the 20

def swapletters(t, a, b):
    sw = lambda L: b if L == a else a if L == b else L
    def fix(m):
        head, body = m.group(1), m.group(2)
        return head + re.sub(r"[ABCD]", lambda n: sw(n.group(0)), body)
    return re.sub(r"([Oo]ptions?\s+)([ABCD](?:\s*(?:,|and|or)\s*[ABCD])*)", fix, t)

def relabel(items):
    for it in items:
        w = WANT.get(it["id"])
        if not w or not it.get("options"): continue
        i, j = LET.index(it["answer"]), LET.index(w)
        if i == j: continue
        o = it["options"]; o[i], o[j] = o[j], o[i]
        it["answer"] = w
        a, b = LET[i], LET[j]
        for fld in ("explanation", "check"):
            if it.get(fld): it[fld] = swapletters(it[fld], a, b)
    return items

relabel(I)
_k = {}
for _it in I: _k[_it["answer"]] = _k.get(_it["answer"], 0) + 1
print("key spread:", {L: _k.get(L, 0) for L in LET}, "cap", -(-len(I) * 2 // 5))

POOLD = {"moduleId":"<module>","topicId":"<module>-t<n>","source":"mastery",
         "label":"<topic title> — mastery test (unseen)","count":len(I),"items":I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT,"w",encoding="utf-8") as f:  json.dump(LES,f,ensure_ascii=False,indent=1)
with io.open(POOL,"w",encoding="utf-8") as f: json.dump(POOLD,f,ensure_ascii=False,indent=1)
print("wrote %s: %d scenes (%d core), estMin %d"%(OUT,len(S),len(CORE),LES["estMin"]))
print("wrote %s: %d items"%(POOL,len(I)))
