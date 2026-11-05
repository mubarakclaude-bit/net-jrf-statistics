#!/usr/bin/env python3
"""v3.0 -> v4.0 of lesson 4.1: merge in the reviewed rewrite's structure.

Adopted from the review document:
  - a "How to use this lesson" note on the overview
  - statistic / estimator / estimate as its own scene, promoted out of a theory block
  - a family -> statistic reference table, in the theorem scene and again in the summary
  - a quick check on every teaching scene, not only the three that had one
  - concrete numbers in the Uniform scene so it reads without the interactive plot
  - the Cauchy and Uniform(theta, theta+1) material gathered into one scene marked
    "JRF extension", so the core path completes without it

Kept from v3.0 against the rewrite: the exponential-family block, the general
conditional-distribution derivation, the Cauchy ratio argument, the likelihood-principle
line, the map of where sufficiency is used later, and the 20-item mastery pool.

Every replacement asserts its match count: a silent no-op patch has cost us a day before.
"""
import io

P = "lesson_t1.py"
s = io.open(P, encoding="utf-8").read()
n_applied = 0


def sub(old, new, count=1, label=""):
    global s, n_applied
    got = s.count(old)
    assert got == count, "patch %r matched %d times, wanted %d" % (label or old[:50], got, count)
    s = s.replace(old, new)
    n_applied += 1


# ---------------------------------------------------------------- 1. foundation: quick check
sub('''definitions stop being frightening."))]))''',
    '''definitions stop being frightening."))],
  ask=dict(q="X₁, X₂, X₃ are three independent tosses of a coin whose chance of heads is p, and the "
             "result comes out H, T, H. What is the probability of exactly that sequence?",
    nudge="One factor per toss — p for a head, (1 − p) for a tail — multiplied together, because "
          "the tosses are independent.")))''', label="foundation ask")

# ------------------------------------------------- 3. NEW scene: statistic vs estimator
sub('''# ---------------------------------------------------------------- 3. likelihood
SC.append(dict(
  kind="theory", id="s2", title="The likelihood — one formula, read backwards", mins=6,''',
    '''# ------------------------------------------------- 3. statistic, estimator, estimate
SC.append(dict(
  kind="theory", id="s1b", title="A statistic is not an estimate", mins=4,
  objective="Separate three words the exam keeps apart — statistic, estimator, estimate — before "
            "they can be confused.",
  blocks=[
   dict(t="def", h="Why this scene is here, this early",
     body="You have just produced the number 7 from ten tosses, and the natural next thought is "
          "'so my answer for p is 0.7'. That thought is correct arithmetic and the wrong topic. "
          "Sufficiency is about which SUMMARY of the data keeps the information. Estimation — what "
          "to guess, and how good the guess is — is topic 4.4. Candidates who meet sufficiency "
          "through the sentence 'count the heads, so p̂ = 0.7' carry the confusion into the exam "
          "hall, so it is worth four minutes now."),
   dict(t="assume", h="The three words, with the coin as the example",
     body="A STATISTIC is any quantity computed from the sample and nothing else: the number of "
          "heads (7), the sample proportion (0.7), the maximum, the whole sample. It may not use "
          "an unknown parameter. An ESTIMATOR is a statistic you have chosen in order to guess a "
          "parameter — the proportion, used for p. An ESTIMATE is the number that estimator "
          "returns for the sample in hand: 0.7. So 7 and 0.7 are both statistics; only 0.7 is an "
          "estimate of p, and 7 could not be one, because a probability cannot be 7."),
   dict(t="step", h="Both can be sufficient, and sufficiency does not care which",
     body="Σxᵢ = 7 is sufficient for p. So is x̄ = 0.7, because each can be computed from the "
          "other once n is fixed. Sufficiency is a property of the information a summary carries, "
          "not of whether the summary is on the right scale to be an answer. That is why the "
          "sufficient statistic for an exponential sample is Σxᵢ and not n/Σx, even though n/Σx "
          "is the thing you would quote as an estimate of the rate."),
   dict(t="trap", h="What follows, and what does not",
     body="A sufficient statistic need not be unbiased, need not have small variance, and need "
          "not estimate θ at all. Nothing about sufficiency makes a statistic a good estimator, "
          "and nothing about being a good estimator makes a statistic sufficient. The two "
          "properties travel together often enough in the standard families that the exam tests "
          "whether you know they are separate.")],
  ask=dict(q="Ten tosses give seven heads. Is ΣXᵢ an estimate of p?",
    nudge="Write down the value ΣXᵢ takes, and ask whether that number could be a probability."))

# ---------------------------------------------------------------- 4. likelihood
SC.append(dict(
  kind="theory", id="s2", title="The likelihood — one formula, read backwards", mins=5,''',
    label="new statistic/estimator scene")

# ---------------- likelihood scene: drop the block now covered by the new scene, add a check
A = '   dict(t="trap", h="A statistic is not an estimator'
END = 'Estimation is topic 4.4'
assert s.count(A) == 1, "estimator-block start anchor is not unique"
assert s.count(END) == 1, "estimator-block end anchor is not unique"
a = s.index(A)
b = s.index("\n", s.index(END)) + 1          # through the end of that line
assert b > a and s[a:b].count("dict(t=") == 1, "estimator block spans more than one block"
s = s[:a] + s[b:]
n_applied += 1

sub('''          "question, applied.")]))

# ---------------------------------------------------------------- 4. explore''',
    '''          "question, applied.")],
  ask=dict(q="A factor of the joint density that contains no θ can be discarded when you are "
             "hunting for a sufficient statistic. Why does throwing it away cost nothing?",
    nudge="Picture the likelihood curve. Ask what multiplying every point of it by the same "
          "number does to the position of its peak.")))

# ---------------------------------------------------------------- 5. explore''',
    label="likelihood ask")

# ---------------------------------------------------------------- explore 1: trim time
sub('''title="Two different samples, one identical curve", mins=5,''',
    '''title="Two different samples, one identical curve", mins=4,''', label="explore mins")

# ---------------------------------------------------------------- worked: quick check
sub('''        "exam hall, make it step 7 — the ratio is the tool that hands you the answer instead of asking you to guess "
        "it."))''',
    '''        "exam hall, make it step 7 — the ratio is the tool that hands you the answer instead of asking you to guess "
        "it.",
  ask=dict(q="Part (d) found that (ΣXᵢ, X₁) is sufficient but not minimal. In one sentence, what "
             "is wrong with it?",
    nudge="Ask what you could still throw away from that pair without losing anything about p.")))''',
    label="worked ask")

# ---------------------------------- factorisation scene: the family table and a quick check
sub('''           dict({"from":"b","to":"m"}), dict({"from":"n2","to":"m"}), dict({"from":"u","to":"m"})])))

# ---------------------------------------------------------------- 7. the model''',
    '''           dict({"from":"b","to":"m"}), dict({"from":"n2","to":"m"}), dict({"from":"u","to":"m"})]),
  table=dict(
    head=["Family", "Sufficient statistic", "Where θ meets the data"],
    rows=[["Bernoulli(p)", "Σxᵢ", "the exponent, after splitting (1−p)ⁿ out"],
          ["Poisson(λ)", "Σxᵢ", "the exponent; the factorials are h(x)"],
          ["Exponential, rate λ", "Σxᵢ", "the exponent; h(x) = 1"],
          ["Normal, σ² known", "Σxᵢ, equivalently x̄", "the exponent's cross term only"],
          ["Normal, both unknown", "(Σxᵢ, Σxᵢ²), equivalently (x̄, s²)", "both exponent terms"],
          ["Uniform(0, θ)", "max xᵢ", "the support indicator I(max ≤ θ)"]],
    caption="The six to know cold. Learn the third column rather than the second: the question "
            "'where does θ touch the data' reproduces the middle column every time, and it also "
            "handles the families that are not in this table."),
  ask=dict(q="The theorem has two conditions. If you factorise a density and your h(x) turns out "
             "to contain θ, have you shown that your T is sufficient?",
    nudge="Read the statement again and check both halves of it, not just the one about g.")))

# ---------------------------------------------------------------- 8. the model''',
    label="family table + theorem ask")

# ---------------------------------------------------------------- model scene: trim time
sub('''title="Change the model and the answer changes", mins=5,''',
    '''title="Change the model and the answer changes", mins=4,''', label="model mins")

# ---------------------------------------------------- minimal sufficiency: a quick check
sub('''          "'sufficient', factorisation is enough and several options may be right.")]))''',
    '''          "'sufficient', factorisation is enough and several options may be right.")],
  ask=dict(q="The whole sample is always sufficient. Why is that not a useful answer to 'find a "
             "sufficient statistic for p'?",
    nudge="Nothing is wrong with it as a statement. Ask what the point of looking for a sufficient "
          "statistic was in the first place.")))''', label="minimality ask")

# ------------------------------- Uniform explore: concrete numbers, so it reads on paper
sub('''   "This is the likelihood for Uniform(0, θ), with sliders for n, the observed maximum, and a candidate θ. Look first "
   "at the shape: it is exactly zero to the left of the observed maximum and then decreases as θ^(−n) to the right. "
   "The cliff is at θ = max xᵢ.",''',
    '''   "Take a concrete sample before touching the slider: 2.1, 0.7, 3.6, 1.9, drawn from Uniform(0, θ). The largest "
   "observation is 3.6. Now ask which values of θ could have produced this sample. Could θ be 3? No — not unlikely, "
   "IMPOSSIBLE, because a Uniform(0, 3) never produces 3.6. Could θ be 4, or 10, or 100? Yes, each of them could, "
   "with decreasing plausibility as θ grows and the density 1/θ thins out. So the data rule out every θ below 3.6 "
   "outright, and the only thing doing the ruling out is the largest observation.",
   "This is the likelihood for Uniform(0, θ), with sliders for n, the observed maximum, and a candidate θ. Look first "
   "at the shape: it is exactly zero to the left of the observed maximum and then decreases as θ^(−n) to the right. "
   "The cliff is at θ = max xᵢ — at 3.6 for the sample above.",''',
    label="concrete Uniform numbers")

# ------------------------ guided normal: the Cauchy scenario moves to the extension scene
i0 = s.index('''  check="Two checks. The number of conditions produced by the ratio should match the number of unknown parameters — two "''')
i1 = s.index('''# ---------------------------------------------------------------- 13. trapcheck''')
old_tail = s[i0:i1]
assert "The Cauchy that refuses to be reduced" in old_tail, "Cauchy scenario not where expected"
cauchy = old_tail[old_tail.index('  scenario=dict('):]
new_tail = old_tail[:old_tail.index('  scenario=dict(')].rstrip().rstrip(',') + '))\n\n'
s = s[:i0] + new_tail + s[i1:]
n_applied += 1

# ---------------------------------------------------------------- trapcheck: trim time
sub('''title="Six statements — verdict on each before you look", mins=6,''',
    '''title="Six statements — verdict on each before you look", mins=5,''', label="trapcheck mins")

# ------------------- transfer scene becomes the single JRF extension, carrying the Cauchy
sub('''  kind="guided", id="s13", title="Transfer — when the statistic is bigger than the parameter", mins=7,
  objective="Handle a family where the minimal sufficient statistic has higher dimension than the parameter.",''',
    '''  kind="guided", id="s13", ext=True, mins=9,
  title="JRF extension — the two families where reduction behaves oddly",
  objective="Handle a family whose minimal sufficient statistic has higher dimension than the "
            "parameter, and one that admits no reduction at all.",''', label="extension scene head")

# give the extension scene the Cauchy scenario that used to sit on the guided normal scene
sub('''        "minimum and a different maximum would give a different likelihood, and the statistic cannot be sufficient."))

# ---------------------------------------------------------------- 15. summary''',
    '''        "minimum and a different maximum would give a different likelihood, and the statistic cannot be sufficient.",
''' + cauchy.rstrip().rstrip(')') + ''')))

# ---------------------------------------------------------------- 16. summary''',
    label="attach Cauchy to the extension scene")

# ---------------------------------------------------------------- summary: the table again
sub('''   "The habit. Write the family first, then the joint density including its support, then look for where the parameter "
   "touches the data.")))''',
    '''   "The habit. Write the family first, then the joint density including its support, then look for where the parameter "
   "touches the data."),
  table=dict(
    head=["Family", "Minimal sufficient statistic", "Note"],
    rows=[["Bernoulli(p)", "Σxᵢ", "exponential family"],
          ["Poisson(λ)", "Σxᵢ", "exponential family; h = 1/∏xᵢ!"],
          ["Exponential, rate λ", "Σxᵢ", "exponential family"],
          ["Normal, σ² known", "Σxᵢ, equivalently x̄", "one unknown, one component"],
          ["Normal, both unknown", "(Σxᵢ, Σxᵢ²), equivalently (x̄, s²)", "two unknowns, two components"],
          ["Uniform(0, θ)", "max xᵢ", "support depends on θ; no sum"],
          ["Uniform(θ, θ+1)  ✦", "(min xᵢ, max xᵢ)", "dimension 2 for one parameter; not complete"],
          ["Cauchy, location θ  ✦", "the full set of order statistics", "no reduction at all"]],
    caption="The last two rows, marked ✦, come from the optional JRF-extension scene. The first "
            "six are the ones a pass requires.")))''', label="summary table")

# ---------------------------------------------------------------- lesson-level fields
sub('''  estMin=sum(s["mins"] for s in SC), version="3.0", status="approved",''',
    '''  estMin=sum(s["mins"] for s in SC), version="4.0", status="approved",
  howto="You do not have to understand every formula the first time you meet it. Each section "
        "carries one idea, and most of them end with a question — try it before you open the "
        "answer, because the attempt is what makes it stick. If a formula feels opaque, the "
        "example just above it is where to go back to. One section is marked an optional JRF "
        "extension; the topic is complete without it, and it will still be here when you want it.",''',
    label="version and howto")

io.open(P, "w", encoding="utf-8").write(s)
print("applied %d patches to %s" % (n_applied, P))
