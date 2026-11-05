#!/usr/bin/env python3
"""v4.0 -> v4.1: corrections from the second-round academic review.

Three of the review's findings are real errors in v4.0, and they are fixed here:

1. OVERCLAIM, twice: the trapcheck reason and one elimination shortcut said that ONLY
   one-to-one functions of a sufficient statistic are sufficient. That is false, and the
   counterexample is embarrassingly close to hand — the whole sample X is sufficient, and
   Σxᵢ is a MANY-to-one function of it that is also sufficient. The correct statement is
   that a one-to-one function is GUARANTEED to stay sufficient while a many-to-one
   function may or may not. The claim being judged ("every function of a sufficient
   statistic is sufficient") is still false, so the verdict is unchanged; the reason for
   it was wrong. The lesson's `traps` list already said "guaranteed" and was correct.

2. MISSING CONDITION: the (x̄, s²) <-> (Σxᵢ, Σxᵢ²) equivalence needs n >= 2, since s²
   divides by n − 1.

3. LOOSE ARGUMENT in the Uniform(θ, θ+1) incompleteness note: an expectation free of θ is
   not itself a failure of completeness. The function has to be centred first — it is
   g(T) = (max − min) − E(range) that has zero expectation for every θ while not being
   zero, and that is what completeness forbids.

Two tightenings also adopted:
4. The ratio criterion is stated with its support condition, instead of baldly.
5. The Cauchy root argument is stated over multisets, so equal roots with multiplicity is
   what "permutation" means.

The review also, correctly, turned v4.0's own criticism back on the app: mastery item
inf-t1-m-01 asked for "a sufficient statistic" while offering (Σxᵢ, ∏xᵢ) as a distractor,
and that pair IS sufficient — merely not minimal. Exactly the defect v4.0 declined to
import from the previous rewrite. The stem now asks for the minimal statistic and the
explanation names the trap. Fixed in the seed JSON, since 4.1's pool predates the
qset_*.py convention and has no authoring script.

Declined, with reasons, in the reply to the user — not everything in the review needed a
change: the mastery policy is already labelled "Platform settings, not an NTA rule", the
prerequisite teaching was already moved out of collapsed blocks in v3.0, and scene
completion is already stored separately from mastery performance.
"""
import io, json

n = 0


def patch(path, pairs):
    global n
    s = io.open(path, encoding="utf-8").read()
    for old, new, label in pairs:
        got = s.count(old)
        assert got == 1, "%s: %r matched %d times" % (path, label, got)
        s = s.replace(old, new)
        n += 1
    io.open(path, "w", encoding="utf-8").write(s)


# ------------------------------------------------------------------ the lesson
patch("lesson_t1.py", [
    # 1a. the trapcheck reason
    ('''     why="Only one-to-one functions. A many-to-one function discards information: collapsing distinct values of T "
         "together can destroy sufficiency, and in the Bernoulli case a statistic that recorded only whether Σxᵢ was "
         "even would plainly not do."),''',
     '''     why="A one-to-one function is GUARANTEED to stay sufficient; a many-to-one function may or may not, so the "
         "claim as stated is false. Be careful not to overcorrect into 'only one-to-one functions are sufficient', "
         "which is also false — the whole sample X is sufficient, and Σxᵢ is a many-to-one function of it that is "
         "sufficient too. What a many-to-one function risks is collapsing values of T that the likelihood "
         "distinguishes: a statistic recording only whether Σxᵢ is even would plainly not do for the Bernoulli."),''',
     "trapcheck overclaim"),

    # 1b. the elimination shortcut
    ('''      "Any option saying every function of a sufficient statistic is sufficient is wrong — only one-to-one ones.",''',
     '''      "Any option saying EVERY function of a sufficient statistic is sufficient is wrong; so is any option saying "
      "only the one-to-one ones are. One-to-one is what guarantees it.",''',
     "shortcut overclaim"),

    # 1c. the recall item
    ('''   dict(q="Which transformations of a sufficient statistic preserve sufficiency?",
     a="One-to-one ones. A many-to-one function of a sufficient statistic need not be sufficient."),''',
     '''   dict(q="Which transformations of a sufficient statistic are guaranteed to preserve sufficiency?",
     a="The one-to-one ones. A many-to-one function may or may not — Σxᵢ is a many-to-one function of the whole "
       "sample and is sufficient, while the parity of Σxᵢ is not."),''',
     "recall item wording"),

    # 1d. the theory block, with the concrete illustration
    ('''          "sufficient' may have several correct answers unless it asks for the minimal one. A many-to-one function of "
          "a sufficient statistic need NOT be sufficient, which is the trap in the other direction."),''',
     '''          "sufficient' may have several correct answers unless it asks for the minimal one. A many-to-one function of "
          "a sufficient statistic need NOT be sufficient, which is the trap in the other direction — but note that it "
          "need not fail either: the whole sample is sufficient, and Σxᵢ is a many-to-one function of it that is also "
          "sufficient. One-to-one is what GUARANTEES sufficiency is preserved; many-to-one has to be checked."),''',
     "theory block illustration"),

    # 2. n >= 2 for the (xbar, s2) equivalence, in the guided scene
    ('''     math="(x̄, s²) is a one-to-one function of (Σxᵢ, Σxᵢ²), so it is minimal sufficient too",''',
     '''     math="(x̄, s²) is a one-to-one function of (Σxᵢ, Σxᵢ²) for n ≥ 2, so it is minimal sufficient too",''',
     "n>=2 in the guided scene"),

    # 2b. and in the trapcheck item that asserts it
    ('''     why="It is a one-to-one function of (Σxᵢ, Σxᵢ²), which the ratio criterion identifies as minimal sufficient. With "''',
     '''     why="For n ≥ 2 it is a one-to-one function of (Σxᵢ, Σxᵢ²) — s² divides by n − 1, so a single observation has "
         "no s² — and the ratio criterion identifies that pair as minimal sufficient. With "''',
     "n>=2 in the trapcheck"),

    # 3. the incompleteness argument, centred properly
    ('''     why="The range max − min has an expectation free of θ, so a non-trivial function of T has constant expectation "
         "and completeness fails. This is the standard counterexample to 'minimal sufficient implies complete', and "
         "it is the same family that supplies it.")],''',
     '''     why="The reason needs one more step than it is usually given. The range max − min is ancillary: shifting θ "
         "shifts both extremes equally, so the range has the same distribution, and therefore the same expectation c, "
         "for every θ. Now CENTRE it. Put g(T) = (max − min) − c. Then E_θ[g(T)] = 0 for every θ while g is not "
         "identically zero — which is exactly what completeness forbids. An expectation that happens to be free of θ "
         "is not by itself a failure of completeness; the centred function is what demonstrates it. This is the "
         "standard counterexample to 'minimal sufficient implies complete', and it is the same family that supplies "
         "the dimension mismatch.")],''',
     "centred function for incompleteness"),

    # 4. the ratio criterion, with its support condition
    ('''     body="Suppose T satisfies: f(x | θ)/f(y | θ) is free of θ  ⟺  T(x) = T(y). Then T is minimal sufficient. In "
          "practice you form the ratio, simplify, and read off which functions of the data must agree for θ to "''',
     '''     body="Suppose T satisfies: f(x | θ)/f(y | θ) is free of θ  ⟺  T(x) = T(y), the ratio being taken over the x "
          "and y the family gives positive density to. Then T is minimal sufficient. (That support proviso is what "
          "makes the Uniform cases work: there the ratio is a ratio of indicators, and the comparison is between the "
          "sets of θ each sample permits rather than between two positive numbers.) In "
          "practice you form the ratio, simplify, and read off which functions of the data must agree for θ to "''',
     "ratio criterion support proviso"),

    # 5. the Cauchy argument over multisets
    ('''      "if the two polynomials are identical, which happens only if the two samples have the same roots — that is, only "
      "if the two samples are permutations of each other. So T(x) = T(y) exactly when the sorted samples agree, and "''',
     '''      "if the two polynomials are identical, which happens only if the two samples give the same roots WITH THE SAME "
      "MULTIPLICITIES — that is, only if the two samples are the same multiset, which is to say permutations of each "
      "other. So T(x) = T(y) exactly when the sorted samples agree, and "''',
     "Cauchy multiset wording"),
])

# ------------------------------------------------- the mastery pool: item 01's stem
POOL = "seed/inference_t1_mastery.json"
d = json.load(io.open(POOL, encoding="utf-8"))
q = [x for x in d["items"] if x["id"] == "inf-t1-m-01"]
assert len(q) == 1, "inf-t1-m-01 not found"
q = q[0]
assert q["stem"].endswith("A sufficient statistic for β is:"), "m-01 stem is not as expected"
assert "(Σxᵢ, ∏xᵢ)" in q["options"], "m-01 no longer carries the pair distractor"
q["stem"] = q["stem"].replace("A sufficient statistic for β is:",
                              "The minimal sufficient statistic for β is:")
q["explanation"] = (
    "The joint density is β^(nα)/Γ(α)ⁿ · (∏xᵢ)^(α−1) · e^(−βΣxᵢ). The only factor containing β beyond the "
    "constant β^(nα) is e^(−βΣxᵢ), so g depends on the data through Σxᵢ alone, and Σxᵢ is minimal sufficient. "
    "The product (∏xᵢ)^(α−1) contains no β — α is known — so it belongs in h, which rules out B and the pair in D. "
    "Read D carefully, because it is the instructive distractor: (Σxᵢ, ∏xᵢ) IS sufficient, since anything that "
    "determines a sufficient statistic is itself sufficient. It is simply not minimal — Σxᵢ is a function of it and "
    "not conversely. That is why this stem asks for the MINIMAL statistic: had it asked only for 'a sufficient "
    "statistic', both A and D would have been correct answers.")
json.dump(d, io.open(POOL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n += 1

print("applied %d corrections" % n)
