"""Pull the practice variants out of the Q1-Q50 study set.

Source: text extracted from a two-column PDF, so reading order interleaves.
Parsing is anchored on each answer marker and works BACKWARDS to find (D), (C),
(B), (A) and the stem, so no item can be skipped or swallowed by its neighbour.
Nothing is guessed: an item is kept only if it yields a stem, four distinct
options and a keyed answer, and the yield is reported.
"""
import re, json, collections

SRC = "/home/claude/bk.txt"
raw = open(SRC, encoding="utf-8").read()
txt = raw.replace("‐\n", "").replace("‑\n", "").replace("-\n", "")
txt = re.sub(r"(?m)^\s*\d+\s*/\s*83\s*$", "", txt)
txt = re.sub(r"(?m)^.*UGC ?NET June 2026 · Statistics Paper 2 · Q1–Q50.*$", "", txt)

def clean(s):
    s = re.sub(r"\s+", " ", s.replace("\n", " ")).strip()
    return s.strip(" ·;,")

def cut_why(w):
    # the extractor runs one explanation into the next item; cut at anything that
    # can only belong to a following item, option markers included
    for pat in (r"\s\d{1,2}\.\s+\S.*?\(A\)", r"\sQ\d{1,2}\.\s", r"\sConcept notes",
                r"\sSolution\b", r"\sHabit to build", r"\sThe exam technique",
                r"\sTen practice questions", r"\s\([A-D]\)\s", r"\s\d{1,2}\.\s+[A-Z]"):
        m = re.search(pat, w)
        if m: w = w[:m.start()]
    if len(w) > 300:
        c = w.rfind(". ", 0, 300); w = w[:c + 1] if c > 60 else w[:300]
    return w.strip(" ·.;,")

marks = [(m.start(), int(m.group(1))) for m in re.finditer(r"(?m)^Q(\d{1,2})\.\s", txt)]
def qof(pos):
    cur = None
    for s, n in marks:
        if s <= pos: cur = n
        else: break
    return cur

arrows = [m for m in re.finditer(r"→\s*\(([A-D])\)\.?", txt)]
items, rej = [], collections.Counter()
seen = set()
prev_end = 0
for idx, am in enumerate(arrows):
    ans = am.group(1)
    # the item occupies the text between the previous arrow and this one
    region = txt[prev_end:am.start()]
    nxt = arrows[idx + 1].start() if idx + 1 < len(arrows) else len(txt)
    why = cut_why(clean(txt[am.end():nxt]))
    prev_end = am.end()
    # walk backwards for the four option markers, in order, taking the LAST run
    pos = {}
    ok = True
    last = len(region)
    for letter in "DCBA":
        m = None
        for mm in re.finditer(r"\(%s\)" % letter, region[:last]):
            m = mm
        if not m: ok = False; break
        pos[letter] = m
        last = m.start()
    if not ok: rej["option marker missing"] += 1; continue
    o = {}
    bounds = {"A": pos["B"].start(), "B": pos["C"].start(), "C": pos["D"].start(), "D": len(region)}
    for letter in "ABCD":
        o[letter] = clean(region[pos[letter].end():bounds[letter]])
    stem = clean(region[:pos["A"].start()])
    # The region begins with the tail of the PREVIOUS item's explanation. The item
    # number is the real boundary, so cut at the last one that leaves a usable stem.
    cuts = [m for m in re.finditer(r"(?:^|(?<=[\s.:;)\u2014]))(\d{1,2})\.\s+", stem)]
    for m in reversed(cuts):
        tail = stem[m.end():].strip()
        if len(tail) >= 12:
            stem = tail; break
    else:
        if len(stem) > 300:                 # no number to cut on and far too long
            for sep in (". ", "? ", ": "):
                i = stem.rfind(sep, 0, len(stem) - 20)
                if i > 0 and len(stem) - i - len(sep) >= 15:
                    stem = stem[i + len(sep):].strip(); break
    opts = [o[l] for l in "ABCD"]
    q = qof(am.start())
    if q is None:                        rej["no parent question"] += 1; continue
    if not (12 <= len(stem) <= 300):     rej["stem length"] += 1; continue
    if re.match(r"^[\u2192\)\]\.,;:]", stem): rej["stem starts mid-sentence"] += 1; continue
    if any(not x for x in opts):         rej["empty option"] += 1; continue
    if any(len(x) > 180 for x in opts):  rej["option too long"] += 1; continue
    if len(set(opts)) != 4:              rej["duplicate options"] += 1; continue
    if re.search(r"Concept notes|Solution\b|Ten practice", stem + " ".join(opts)):
                                         rej["marker bleed"] += 1; continue
    if len(why) < 4:                     rej["no explanation"] += 1; continue
    key = (stem[:70], opts[0][:40])
    if key in seen:                      rej["duplicate item"] += 1; continue
    seen.add(key)
    items.append({"q": q, "stem": stem, "options": opts, "answer": ans, "why": why})

print("arrows found: %d   items parsed: %d" % (len(arrows), len(items)))
print("rejected:", dict(rej) if rej else "none")
byq = collections.Counter(i["q"] for i in items)
print("questions covered: %d of 50;  with all 10 variants: %d" %
      (len(byq), sum(1 for n in byq.values() if n >= 10)))
print("missing entirely:", [q for q in range(1, 51) if q not in byq] or "none")
print("answer spread:", dict(collections.Counter(i["answer"] for i in items)))
json.dump(items, open("/tmp/claude-0/variants_raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
