#!/usr/bin/env python3
"""Import the accepted parts of the third-party Module 4 review.

Operates on the seed JSON, not the authoring scripts, because six of the nine scripts are
STALE: lesson_t2/t3/mle/t5/t6/t9 all declare version 1.0 while their seeds are at 1.2, and
the text this import has to change is not present in lesson_mle.py at all. The seeds were
enriched after generation and the scripts never caught up, so running one of those six
would quietly revert its lesson. The seed is what the app serves and what the store holds,
so the seed is the source of truth being edited here. That drift is reported separately.

ACCEPTED
  1. 28 per-scene quick checks for 4.2-4.9, on theory, worked and explore scenes, filling
     a gap already recorded as outstanding. All 28 were read and checked before import.
     One nudge (4.2 scene 8) is reworded: "non-zero unbiased functions of the statistic
     with expectation zero" garbles the condition - completeness concerns non-zero
     functions whose expectation is zero, and "unbiased" does not belong in it.
  2. The MLE overclaim qualified where the reviewer found it: 4.1 revision sheet and
     summary scene, 4.4 prerequisite and revision sheet. v4.2 of 4.1 had qualified this in
     one place and left the blanket claim standing elsewhere, so the inconsistency was mine.

DECLINED, with reasons
  3. 24 further quick checks on completion and guided scenes. Both already end with the
     learner writing something - five graded blanks, or a model solution behind a hint
     ladder with a "Your answer" box - so a second question box there is clutter, and the
     standard exempts scenes that are themselves exercises.
  4. The rewritten `howto` for 4.1: it drops the sentence telling the learner that one
     section is an optional JRF extension and the topic completes without it.
  5. The 13-part companion references. Their own upgrade report states that theorem
     conditions, numerical claims, answer keys and every MCQ distractor are unvalidated,
     and they carry 90 new MCQs on that footing. They are also written against a 13-part
     lesson specification this project has never been given.

FOUND BY APPLYING THE REVIEWER'S PRINCIPLE MORE WIDELY (not among its findings)
  6. A third copy of the unqualified MLE claim in 4.4, in a prerequisite-check recall.
  7. 4.3 asserts MLE invariance "holds always" with no existence caveat.
  8. 4.7 says the posterior "always" lies between the prior mean and the MLE and the prior
     "always" washes out as n grows. Both hold for the conjugate families in that scenario;
     neither holds in general, since a prior whose support excludes the truth never washes
     out.
"""
import io, json, os

INC = "/tmp/claude-0/m4in/source"
SELF = ["recall", "completion", "trapcheck", "guided", "summary", "quiz"]
M = {"4.2": "lesson_t2", "4.3": "lesson_t3", "4.4": "lesson_mle", "4.5": "lesson_t5",
     "4.6": "lesson_t6", "4.7": "lesson_t7", "4.8": "lesson_t8", "4.9": "lesson_t9"}
REWORD = {("4.2", 8):
          "Completeness rules out any non-zero function of the statistic whose expectation is zero for every θ. "
          "Basu then pairs a COMPLETE sufficient statistic with an ancillary one; drop completeness and the "
          "independence conclusion is not available."}

added = {}
fixed = []


def load(f):
    return json.load(io.open(f, encoding="utf-8"))


def save(f, d):
    json.dump(d, io.open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def setfield(d, path, old, new, label):
    """Replace an exact string at a dotted/indexed path, asserting the old value."""
    cur = d
    parts = path.replace("]", "").split(".")
    for seg in parts[:-1]:
        if "[" in seg:
            k, i = seg.split("[")
            cur = cur[k][int(i)]
        else:
            cur = cur[seg]
    last = parts[-1]
    if "[" in last:
        k, i = last.split("[")
        i = int(i)
        assert cur[k][i] == old, "%s: value is not as expected:\n  %r" % (label, cur[k][i])
        cur[k][i] = new
    else:
        assert cur[last] == old, "%s: value is not as expected:\n  %r" % (label, cur[last])
        cur[last] = new
    fixed.append(label)


# ----------------------------------------------- 1. the 28 accepted quick checks
for k in sorted(M):
    f = "seed/%s.json" % M[k]
    mine = load(f)
    theirs = load(os.path.join(INC, "lesson-%s.json" % k))
    n = 0
    for i, (sa, sb) in enumerate(zip(mine["scenes"], theirs["scenes"])):
        if (sa.get("ask") or {}).get("q"):
            continue
        ask = sb.get("ask") or {}
        if not ask.get("q") or sb["kind"] in SELF:
            continue
        assert sa["title"] == sb["title"], "%s scene %d title drift" % (k, i + 1)
        assert sa["kind"] == sb["kind"], "%s scene %d kind drift" % (k, i + 1)
        sa["ask"] = {"q": ask["q"], "nudge": REWORD.get((k, i + 1), ask["nudge"])}
        n += 1
    added[k] = n
    save(f, mine)

# ----------------------------------------------- 2+6. the MLE overclaim, every instance
t1 = load("seed/lesson_t1.json")
setfield(t1, "revision.sheet[28]",
         "Used later: Rao–Blackwell (4.3) conditions on it; Lehmann–Scheffé needs completeness too (4.2); the MLE is "
         "always a function of it (4.4); Basu's theorem pairs it with an ancillary statistic.",
         "Used later: Rao–Blackwell (4.3) conditions on it; Lehmann–Scheffé needs completeness too (4.2); a unique "
         "MLE is a function of it (4.4); Basu's theorem pairs it with an ancillary statistic.",
         "4.1 revision sheet")
old = t1["scenes"][15]["body"][8]
assert "the MLE is always a function of a sufficient statistic because the likelihood is" in old, old[:120]
t1["scenes"][15]["body"][8] = old.replace(
    "the MLE is always a function of a sufficient statistic because the likelihood is",
    "an MLE that exists and is unique is a function of a sufficient statistic because the likelihood is, and "
    "otherwise the sufficient statistic determines the set of maximisers")
fixed.append("4.1 summary scene")
t1["version"] = "4.3"
t1["provenance"] = (
    "v4.3, October 2026. A third-party review of the whole module found that v4.2's qualification of the MLE claim "
    "had been applied in one place and not in two others — the revision sheet and the summary scene both still said "
    "the MLE is ALWAYS a function of a sufficient statistic. Correct finding, and the inconsistency was introduced by "
    "v4.2 itself; both are now qualified to a unique MLE, with the set-of-maximisers case stated. The same review's "
    "rewritten 'how to use this lesson' note was declined: it drops the sentence telling the learner that one section "
    "is an optional JRF extension and that the topic completes without it. " + t1["provenance"])
save("seed/lesson_t1.json", t1)

mle = load("seed/lesson_mle.json")
setfield(mle, "prereq[2].why",
         "The MLE always comes out as a function of the sufficient statistic — that is a free check on your answer.",
         "When an MLE exists and is unique it comes out as a function of the sufficient statistic — a free check on "
         "your answer. If the maximiser is not unique, the sufficient statistic determines the whole set of maximisers.",
         "4.4 prerequisite")
setfield(mle, "revision.sheet[5]",
         "The MLE is always a function of the sufficient statistic.",
         "A unique MLE is a function of the sufficient statistic; if maximisers are not unique, the statistic "
         "determines the set of them.",
         "4.4 revision sheet")
old = mle["scenes"][0]["items"][3]["recall"]
assert old.endswith("so the MLE is always a function of a sufficient statistic."), old[-80:]
mle["scenes"][0]["items"][3]["recall"] = old.replace(
    "so the MLE is always a function of a sufficient statistic.",
    "so an MLE that exists and is unique is a function of a sufficient statistic — and if the maximiser is not "
    "unique, the sufficient statistic still determines the set of maximisers.")
fixed.append("4.4 prerequisite recall (MISSED by the review)")
save("seed/lesson_mle.json", mle)

# ----------------------------------------------- 7. 4.3 invariance existence caveat
t3 = load("seed/lesson_t3.json")
old = t3["scenes"][7]["blocks"][4]["body"]
assert old.startswith("The MLE of g(θ) is g(θ̂) — that is invariance, and it holds always."), old[:90]
t3["scenes"][7]["blocks"][4]["body"] = old.replace(
    "The MLE of g(θ) is g(θ̂) — that is invariance, and it holds always.",
    "The MLE of g(θ) is g(θ̂) — that is invariance, and it holds for any g, under the usual induced-likelihood "
    "convention, whenever an MLE of θ exists.")
fixed.append("4.3 invariance caveat (not in the review)")
save("seed/lesson_t3.json", t3)

# ----------------------------------------------- 8. 4.7 two unscoped "always" claims
t7 = load("seed/lesson_t7.json")
old = t7["scenes"][1]["scenario"]["body"][3]
assert old.startswith("Note what the three Bayesians agree on. The posterior always lies between"), old[:90]
t7["scenes"][1]["scenario"]["body"][3] = (
    "Note what the three Bayesians agree on. For the conjugate families in this scene the posterior mean lies between "
    "the prior mean and the MLE, because it is a weighted average of the two; and the prior washes out as n grows, "
    "provided it puts positive density near the true value — a prior whose support excludes the truth never does. And "
    "every one of them can state exactly how much their prior contributed. " +
    old.split("The disagreement", 1)[1].join(["The disagreement", ""]))
fixed.append("4.7 conjugate scoping (not in the review)")
save("seed/lesson_t7.json", t7)

# ----------------------------------------------- version bumps and provenance
NOTE = ("Review pass, October 2026: %d per-scene quick checks added on theory, worked and explore scenes from a "
        "third-party module review, each read for correctness before import; a further set offered for completion and "
        "guided scenes was declined, since those scenes already end with the learner writing an answer. ")
for k in sorted(M):
    if k == "4.4":
        continue
    f = "seed/%s.json" % M[k]
    d = load(f)
    maj, mnr = d["version"].split(".")
    d["version"] = "%s.%d" % (maj, int(mnr) + 1)
    extra = ""
    if k == "4.3":
        extra = ("The same pass qualified an unrelated overclaim the review did not flag: MLE invariance was stated as "
                 "holding 'always', which needs the existence of an MLE and the induced-likelihood convention. ")
    if k == "4.7":
        extra = ("The same pass scoped two 'always' claims in the three-Bayesians scenario that the review did not "
                 "flag: the posterior mean lying between the prior mean and the MLE, and the prior washing out as n "
                 "grows, both hold for the conjugate families in that scene but not in general. ")
    d["provenance"] = (NOTE % added[k]) + extra + d["provenance"]
    save(f, d)

mle = load("seed/lesson_mle.json")
mle["version"] = "1.3"
mle["provenance"] = ((NOTE % added["4.4"]) +
                     "The review also found the MLE described as ALWAYS a function of the sufficient statistic in the "
                     "prerequisite and the revision sheet; applying that finding across the lesson turned up a third "
                     "copy in a prerequisite-check recall, which the review had not flagged. All three now qualify "
                     "the claim to an MLE that exists and is unique, and state that otherwise the sufficient "
                     "statistic determines the set of maximisers. " + mle["provenance"])
save("seed/lesson_mle.json", mle)

print("quick checks added per lesson: " + ", ".join("%s:%d" % (k, added[k]) for k in sorted(added)))
print("total added: %d" % sum(added.values()))
print("text corrections (%d):" % len(fixed))
for x in fixed:
    print("  - " + x)
