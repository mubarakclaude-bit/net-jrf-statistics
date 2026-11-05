"""Tag every mastery item with a difficulty band.

easy      — one definition recalled, or one formula with one substitution.
moderate  — two or three steps, or choosing the right tool before applying it.
hard      — four independent verdicts to get right together, or a derivation
            plus a judgement (attainment, admissibility, legality of an estimate).

The bands are the author's, set per item rather than by a rule on the format,
because an "easy" multi-statement item and a "hard" single-answer item both exist.
"""
import json, collections

DIFF = {
 # t1 — sufficiency
 "inf-t1-m-01":"moderate","inf-t1-m-02":"moderate","inf-t1-m-03":"hard","inf-t1-m-04":"moderate",
 "inf-t1-m-05":"easy","inf-t1-m-06":"easy","inf-t1-m-07":"easy","inf-t1-m-08":"hard",
 "inf-t1-m-09":"moderate","inf-t1-m-10":"moderate",
 # t2 — completeness, Basu
 "inf-t2-m-01":"easy","inf-t2-m-02":"moderate","inf-t2-m-03":"hard","inf-t2-m-04":"hard",
 "inf-t2-m-05":"easy","inf-t2-m-06":"moderate","inf-t2-m-07":"hard","inf-t2-m-08":"moderate",
 "inf-t2-m-09":"moderate","inf-t2-m-10":"moderate",
 # t3 — Rao-Blackwell, Lehmann-Scheffe
 "inf-t3-m-01":"easy","inf-t3-m-02":"moderate","inf-t3-m-03":"hard","inf-t3-m-04":"moderate",
 "inf-t3-m-05":"moderate","inf-t3-m-06":"moderate","inf-t3-m-07":"hard","inf-t3-m-08":"moderate",
 "inf-t3-m-09":"hard","inf-t3-m-10":"easy",
 # t4 — MLE
 "mle-m-01":"moderate","mle-m-02":"moderate","mle-m-03":"hard","mle-m-04":"moderate",
 "mle-m-05":"easy","mle-m-06":"hard","mle-m-07":"moderate","mle-m-08":"easy",
 "mle-m-09":"easy","mle-m-10":"moderate",
 # t5 — method of moments
 "inf-t5-m-01":"easy","inf-t5-m-02":"moderate","inf-t5-m-03":"hard","inf-t5-m-04":"moderate",
 "inf-t5-m-05":"easy","inf-t5-m-06":"moderate","inf-t5-m-07":"hard","inf-t5-m-08":"moderate",
 "inf-t5-m-09":"hard","inf-t5-m-10":"easy",
 # t6 — Cramer-Rao
 "inf-t6-m-01":"easy","inf-t6-m-02":"moderate","inf-t6-m-03":"hard","inf-t6-m-04":"moderate",
 "inf-t6-m-05":"easy","inf-t6-m-06":"moderate","inf-t6-m-07":"hard","inf-t6-m-08":"hard",
 "inf-t6-m-09":"moderate","inf-t6-m-10":"easy",
}

import glob, os
tot=collections.Counter(); missing=[]
for p in sorted(glob.glob("seed/inference_*.json")):
    d=json.load(open(p,encoding="utf-8"))
    items=d.get("items") or []
    if not items or d.get("source")!="mastery": continue
    c=collections.Counter()
    for q in items:
        dd=DIFF.get(q["id"])
        if not dd: missing.append(q["id"]); continue
        q["diff"]=dd; c[dd]+=1; tot[dd]+=1
    json.dump(d,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print("%-28s easy %d  moderate %d  hard %d"%(os.path.basename(p)[:-5],c["easy"],c["moderate"],c["hard"]))
print("total:",dict(tot))
if missing: print("UNTAGGED:",missing)
