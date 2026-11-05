#!/usr/bin/env python3
# Compare the catalog against the official UGC NET Statistics (107) syllabus and add
# the topics it does not cover. Every entry below is a phrase that appears in the
# official syllabus text and had no matching catalog topic. Weightage is left to the
# module's even split (imp 2, "not reviewed") rather than invented, and weightage.py
# is re-run afterwards so each module's marks still add up.
import json, io, datetime, subprocess

GAPS = {
 # Unit I
 "probability": [
   ("Bayes theorem and conditional probability", "Apply"),
   ("Sampling distributions: t, chi-square and F", "Derive"),
 ],
 # Unit II — the syllabus asks for far more of this than the catalog carried
 "maths": [
   ("Taylor's theorem, L'Hôpital's rule, uniform continuity", "Apply"),
   ("Functions of two variables: partial and total derivatives", "Apply"),
   ("Saddle points and Lagrange multipliers", "Apply"),
   ("Double and triple integrals and their applications", "Apply"),
   ("Vector spaces, basis, dimension, row and column space", "Recall"),
   ("Systems of linear equations and row reduced echelon form", "Apply"),
   ("Gram–Schmidt orthogonalisation and orthogonal matrices", "Apply"),
   ("Trace, determinant and inverse of a matrix", "Apply"),
 ],
 # Unit III
 "sampling": [
   ("Nonnegative variance estimation, ordered and unordered estimators", "Derive"),
 ],
 "design": [
   ("Missing plot technique", "Apply"),
   ("Connectedness and orthogonality of block designs", "Recall"),
 ],
 # Units IV and V
 "inference": [
   ("Contingency tables: independence and homogeneity", "Apply"),
   ("UMP unbiased and UMP invariant tests", "Derive"),
 ],
 "nonparam": [
   ("Empirical distribution function and its properties", "Derive"),
   ("Linear rank tests for location and scale", "Apply"),
 ],
 # Unit VI
 "regression": [
   ("Indicator and dummy variables", "Apply"),
   ("Logistic regression models", "Apply"),
   ("Restricted regression: exact, stochastic and mixed restrictions", "Derive"),
   ("Errors in variables and stochastic regressors", "Derive"),
   ("k-class estimators", "Recall"),
 ],
 # Unit VII
 "timeseries": [
   ("Ergodicity", "Recall"),
   ("General linear process and Wold decomposition", "Derive"),
   ("Forecasting with stationary and invertible processes", "Apply"),
 ],
 # Unit X
 "rprog": [
   ("Lists, factors, display and formatting", "Recall"),
   ("Data frames, data input and output, graphics and plots", "Apply"),
   ("LaTeX and word processing software", "Recall"),
 ],
}

C = json.load(io.open("seed/catalog.json", encoding="utf-8"))
added = []
for m in C["modules"]:
    g = GAPS.get(m["id"])
    if not g: continue
    have = {t["name"].lower() for t in m["topics"]}
    nums = [int(t["id"].split("-t")[1]) for t in m["topics"] if "-t" in t["id"]]
    nxt = max(nums) + 1 if nums else 1
    for name, extent in g:
        if name.lower() in have: continue
        tid = "%s-t%d" % (m["id"], nxt); nxt += 1
        m["topics"].append({"id": tid, "name": name, "extent": extent,
                            "fromSyllabus": "2026 syllabus audit"})
        added.append((m["id"], tid, name))
C["updated"] = datetime.date.today().isoformat()
json.dump(C, io.open("seed/catalog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("added %d topics" % len(added))
for a in added: print("   %-13s %-16s %s" % a)

# redistribute the per-topic weightage so each module's marks still add up
print()
print(subprocess.run(["python3", "weightage.py"], capture_output=True, text=True).stdout.strip()[-600:])
