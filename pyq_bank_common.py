# -*- coding: utf-8 -*-
"""Shared helpers for the CSIR NET 2011-2025 previous-year practice banks.

The four pyq_bank_<pdf>.py files each hold the questions of one source PDF (MathStats Classes compilations of CSIR NET
questions). pyq_bank_build.py routes every item to the bank of the module it belongs to and writes
seed/<module>_pyq_2011_2025.json. verify_pyq_distributions.py recomputes every number and audits the written files.

Two item shapes are used:
  S(...)  single-correct: the four printed options, one answer letter.
  M(...)  multiple-correct ("which of the following are true"): the four printed statements become `statements`, each
          gets a verdict with its reason, and the learner picks the right combination from four option strings.
"""

LETTERS = "ABCD"


def _combo_text(s):
    s = "".join(sorted(s))
    if len(s) == 4:
        return "A, B, C and D"
    if len(s) == 1:
        return s + " only"
    return ", ".join(s[:-1]) + " and " + s[-1] + " only"


def _distractors(truth):
    """Three wrong combinations, deterministic: drop one true letter, add one false letter, then the complement,
    then singletons. Near misses first, so a learner who got three of the four verdicts right is still caught."""
    t = set(truth)
    cands = []
    for x in sorted(t):
        cands.append(t - {x})
    for x in LETTERS:
        if x not in t:
            cands.append(t | {x})
    cands.append(set(LETTERS) - t)
    for x in LETTERS:
        cands.append({x})
    for x in LETTERS:
        for y in LETTERS:
            if x < y:
                cands.append({x, y})
    out, seen = [], {frozenset(t)}
    for c in cands:
        if not c or frozenset(c) in seen:
            continue
        seen.add(frozenset(c))
        out.append(c)
        if len(out) == 3:
            break
    return out


def S(id, module, topic, ref, stem, options, answer, explanation, year=None, diff="moderate", **extra):
    assert len(options) == 4 and answer in LETTERS, id
    it = {"id": id, "format": "single", "topic": topic, "diff": diff, "stem": stem, "options": list(options),
          "answer": answer, "explanation": explanation, "ref": ref}
    if year:
        it["year"] = year
    it.update(extra)
    return {"module": module, "item": it}


def N(id, module, topic, ref, stem, answer, explanation, check, year=None, diff="moderate", **extra):
    """A write-in numerical item: no options, the answer as text, and a `check` line usable under exam pressure."""
    it = {"id": id, "format": "numeric", "topic": topic, "diff": diff, "stem": stem, "options": [], "answer": answer,
          "explanation": explanation, "check": check, "ref": ref}
    if year:
        it["year"] = year
    it.update(extra)
    return {"module": module, "item": it}


def M(id, module, topic, ref, stem, statements, truth, whys, key, explanation, year=None, diff="moderate", **extra):
    """truth: the letters of the true statements, e.g. "AC". key: the option letter under which the right
    combination is listed (chosen so that the answer keys of a bank are spread over A-D)."""
    assert len(statements) == 4 and len(whys) == 4 and key in LETTERS, id
    truth = "".join(sorted(set(truth)))
    assert truth and all(c in LETTERS for c in truth), id
    combos = _distractors(truth)
    opts = [None] * 4
    opts[LETTERS.index(key)] = _combo_text(truth)
    k = 0
    for i in range(4):
        if opts[i] is None:
            opts[i] = _combo_text(combos[k]); k += 1
    verdicts = {}
    for i, L in enumerate(LETTERS):
        verdicts[L] = {"tf": L in truth, "why": whys[i]}
    it = {"id": id, "format": "multi", "topic": topic, "diff": diff, "stem": stem, "statements": list(statements),
          "options": opts, "answer": key, "explanation": explanation, "verdicts": verdicts, "ref": ref}
    if year:
        it["year"] = year
    it.update(extra)
    return {"module": module, "item": it}
