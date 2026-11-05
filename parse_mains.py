"""The 50 actual questions of the June 2026 paper, anchored backwards from each
'Correct: (X)' marker. Strict: an item is kept only if its four options sit
between its own Qn. header and its key."""
import re, json, collections
t = open("/home/claude/bk.txt", encoding="utf-8").read()
t = t.replace("‐\n", "").replace("‑\n", "").replace("-\n", "")
t = re.sub(r"(?m)^\s*\d+\s*/\s*83\s*$", "", t)

heads = [(m.start(), m.end(), int(m.group(1))) for m in re.finditer(r"(?m)^Q(\d{1,2})\.\s*(.*)$", t)]
keys  = list(re.finditer(r"Correct:\s*\(([A-D])\)([^·\n]*)·\s*Response\s*\n?sheet\s*Q?(\d+)\s*·\s*You\s*\n?marked\s*\(([A-D])\)", t))
print("headers %d   keys %d" % (len(heads), len(keys)))

def clean(s): return re.sub(r"\s+", " ", s.replace("\n", " ")).strip(" ·;,")

items, rej = [], collections.Counter()
for km in keys:
    # the question this key belongs to is the last Qn. header before it
    h = None
    for s, e, n in heads:
        if s < km.start(): h = (s, e, n)
        else: break
    if not h: rej["no header"] += 1; continue
    region = t[h[1]:km.start()]
    # last run of (A)(B)(C)(D) before the key
    pos, ok, last = {}, True, len(region)
    for L in "DCBA":
        m = None
        for mm in re.finditer(r"\(%s\)" % L, region[:last]): m = mm
        if not m: ok = False; break
        pos[L] = m; last = m.start()
    if not ok: rej["options not found"] += 1; continue
    bnd = {"A": pos["B"].start(), "B": pos["C"].start(), "C": pos["D"].start(), "D": len(region)}
    opts = [clean(region[pos[L].end():bnd[L]]) for L in "ABCD"]
    stem = clean(region[:pos["A"].start()])
    # drop any practice-item text that interleaved ahead of the real stem
    for pat in (r"→\s*\([A-D]\)\.?", r"Ten practice questions", r"Concept notes"):
        for m in re.finditer(pat, stem): stem = stem[m.end():]
    stem = re.sub(r"^\d{1,2}\.\s*", "", clean(stem))
    extra, rs, marked = clean(km.group(2)), km.group(3), km.group(4)
    if not (10 <= len(stem) <= 700):   rej["stem length"] += 1; continue
    if any(not o or len(o) > 300 for o in opts): rej["option length"] += 1; continue
    if len(set(opts)) != 4:            rej["duplicate options"] += 1; continue
    items.append({"q": h[2], "title": clean(t[h[0]:h[1]])[len("Q%d." % h[2]):].strip(),
                  "stem": stem, "options": opts, "answer": km.group(1),
                  "extra": extra, "responseSheet": rs, "youMarked": marked})
items = {i["q"]: i for i in items}
items = [items[k] for k in sorted(items)]
print("parsed %d of 50  rejected %s" % (len(items), dict(rej) or "none"))
print("missing:", [q for q in range(1, 51) if q not in {i['q'] for i in items}] or "none")
got = sum(1 for i in items if i["answer"] == i["youMarked"])
print("your score on the parsed ones: %d right of %d" % (got, len(items)))
json.dump(items, open("/tmp/claude-0/mains.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for i in items[:2]:
    print("\nQ%d %s\n  %s" % (i["q"], i["title"], i["stem"][:160]))
    for k, o in enumerate(i["options"]): print("   (%s) %s" % ("ABCD"[k], o[:80]))
    print("   key %s  you marked %s  (response sheet Q%s)" % (i["answer"], i["youMarked"], i["responseSheet"]))
