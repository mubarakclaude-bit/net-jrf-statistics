"""The actual June 2026 Paper 2 questions.

Stems and options come from the official question paper PDF (clean, one option
per line). The keys come from the 'Correct: (X)' markers in the study set, which
were set against the response sheet, together with what was marked at the time.
"""
import re, json, collections

paper = open("/tmp/claude-0/paper.txt", encoding="utf-8").read()
study = open("/home/claude/bk.txt", encoding="utf-8").read()
study = study.replace("‐\n", "").replace("‑\n", "").replace("-\n", "")

# ---- keys, from the study set's Correct: markers ----
# The study set runs in question order, and there are exactly 50 markers, so the
# nth marker belongs to question n. Deriving the question from the nearest Qn.
# header is unsafe: the two-column extraction loses some headers, which would
# silently shift keys onto the wrong questions.
KM = re.compile(r"Correct:\s*\(([A-D])\)((?:(?!Correct:)[\s\S]){0,220})")
raw = list(KM.finditer(study))
assert len(raw) == 50, "expected 50 answer markers, found %d" % len(raw)
keys = {}
for i, km in enumerate(raw, 1):
    tail = re.sub(r"\s+", " ", km.group(2))
    note = tail.split("·")[0].strip(" —-·")
    rs = re.search(r"[Ss]heet\s*Q?(\d+)", tail)
    mk = re.search(r"marked\s*\(([A-D])\)", tail)
    keys[i] = {"ans": km.group(1), "note": note,
               "rs": rs.group(1) if rs else "", "marked": mk.group(1) if mk else ""}
print("keys recovered from the study set:", len(keys), "(mapped by position, 1-50)")

# ---- stems and options, from the official paper ----
heads = [(m.start(), m.end(), int(m.group(1))) for m in re.finditer(r"(?m)^Q(\d{1,3})\.\s", paper)]
def clean(s):
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{2,}", "\n", s).strip()
    return s

items, skipped = [], []
for i, (s, e, n) in enumerate(heads):
    if n > 50: continue
    end = heads[i + 1][0] if i + 1 < len(heads) else len(paper)
    body = paper[e:end]
    om = list(re.finditer(r"(?m)^\s*\(([A-D])\)\s", body))
    if len(om) < 4: skipped.append((n, "only %d option lines" % len(om))); continue
    om = om[-4:]                                   # the four that belong to this question
    if [m.group(1) for m in om] != ["A", "B", "C", "D"]:
        skipped.append((n, "options out of order")); continue
    stem = clean(body[:om[0].start()])
    opts = []
    for k, m in enumerate(om):
        stop = om[k + 1].start() if k + 1 < len(om) else len(body)
        opts.append(clean(body[m.end():stop]))
    k = keys.get(n)
    if not k: skipped.append((n, "no key")); continue
    if not k["marked"]: k["marked"] = "?"
    if not stem or len(stem) < 10: skipped.append((n, "no stem")); continue
    if any(not o for o in opts): skipped.append((n, "empty option")); continue
    items.append({
        "id": "j26-q%02d" % n, "format": "single", "paper": 2, "year": 2026, "pno": n,
        "topic": "June 2026 Paper 2 · Q%d" % n,
        "stem": " ".join(stem.split("\n")).strip(),
        "options": [" ".join(o.split("\n")).strip() for o in opts],
        "answer": k["ans"],
        "explanation": ("Official answer " + k["ans"] + (" — " + k["note"] if k["note"] else "") +
                        (". Response sheet Q" + k["rs"] if k["rs"] else "") +
                        ("; you marked " + k["marked"] +
                         (" — correct." if k["marked"] == k["ans"] else " — wrong.")
                         if k["marked"] != "?" else "")),
        "youMarked": k["marked"], "responseSheet": k["rs"],
    })

# Stacked fractions and matrices in the PDF do not survive text extraction. Mark
# those items rather than ship a question whose options have been scrambled.
FRAG = re.compile(r"\d\s{2,}\d|\x0c|\x12|\x13|^\s*[,;]|\s[A-Za-z]\s{2,}\d")
def broken(it):
    why = []
    o = it["options"]
    if any(len(x) <= 2 for x in o):                      why.append("an option is a fragment")
    if any(FRAG.search(x) for x in o):                   why.append("a fraction or matrix split across lines")
    if sum(1 for x in o if re.fullmatch(r"[\d\s]+", x)): why.append("an option is bare digits")
    if "\x0c" in it["stem"] or re.search(r"\x12|\x13", it["stem"]): why.append("control characters in the stem")
    return why
for it in items:
    w = broken(it)
    if w:
        it["needsReview"] = True
        it["reviewNote"] = ("The official PDF renders this question with stacked mathematics, which plain-text "
                            "extraction cannot reproduce: " + "; ".join(w) +
                            ". The stem and the official key are right; the option text needs repair against the paper.")
nb = sum(1 for i in items if i.get("needsReview"))
print("built %d of 50;  skipped: %s" % (len(items), skipped or "none"))
print("clean: %d   needing option repair: %d  -> %s" %
      (len(items) - nb, nb, [i["pno"] for i in items if i.get("needsReview")]))
got = sum(1 for i in items if i["youMarked"] == i["answer"])
print("your score on these: %d right, %d wrong" % (got, len(items) - got))
print("answer spread:", dict(collections.Counter(i["answer"] for i in items)))
body = {"moduleId": "inference", "source": "pyq", "topicId": None,
        "label": "UGC NET June 2026 — Paper 2, questions 1–50 (actual paper)",
        "count": len(items), "items": items}
json.dump(body, open("/home/claude/w1/seed/pyq_j26_full.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for i in items[:2]:
    print("\nQ%d  key %s (you marked %s)\n  %s" % (i["pno"], i["answer"], i["youMarked"], i["stem"][:150]))
    for k, o in enumerate(i["options"]): print("   (%s) %s" % ("ABCD"[k], o[:90]))
