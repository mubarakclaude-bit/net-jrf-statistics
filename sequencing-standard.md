# Lesson sequencing standard — for a learner with a long gap

Companion to `claude/app-build-state.md`. Where the two disagree on the ORDER of scenes,
this document wins; the house standard there still governs counts, validators and pipeline.

Written after reading 4.1 v2.0 as a beginner would. The audience is the one already
described in `AUDIENCE` in src/62-gen.js: someone passionate about clearing JRF who has
been away from the subject for years and whose basics are not solid. 4.1 v3.0
(page Version 33, `lessons/inferencet1` v8) is the reference implementation.

## What was wrong, and it was ordering rather than writing

v2.0 was mathematically correct, fully checked, and at JRF depth — and still unreadable
cold, for four reasons that cost almost nothing to fix:

1. **The foundation drill opened with four questions a rusty learner cannot answer**
   ("write the joint density of an iid sample"; "write the densities of five families").
   The first ninety seconds of the heaviest topic in the syllabus produced four failures.
2. **The best explanations were buried inside those checks' collapsed `refresh` text** —
   including the Bernoulli 1/C(n,t) cancellation, which is the one concrete proof a
   beginner needs. Filed as remediation, behind a gate they fail, so nobody reads it.
3. **The intuition scene asserted the key claim without a single number.** It said the
   total carries all the information about p and never showed a coin.
4. **The general theorem came before the worked case**, and skipped the index-law step
   `(1−p)^(n−Σx) = (1−p)ⁿ/(1−p)^Σx`. One missing line turns a derivation into a trick.

## The order to author in

For a mathematical topic (engine B), 16 scenes:

1. `foundation` — four checks the learner CAN answer, which together constitute the proof
   that opens the lesson. Framed as "nothing here is a gate", not as a prerequisite exam.
2. `intuition` — the idea on a concrete case with real numbers, worked to a conclusion.
   No new notation. This scene must contain an actual computation, not an assertion.
3. `theory` — the one piece of machinery the topic needs, with a block glossing every
   symbol the lesson will use, once each.
4. `explore` — the same fact as a picture, with any new density introduced in two lines
   before the slider appears.
5. `worked` — the full exam-form treatment of the case from scene 2. BEFORE the theorem.
6. `theory` — the general theorem, presented as a generalisation of what they just did
   by hand, plus the flow diagram.
7. `intuition` — the one conceptual point that separates understanding from memorising,
   with the scenario attached.
8. `recall` → 9. `completion` → 10. `theory` (the harder half) → 11. `explore` →
   12. `guided` (+ the hardest counterexample as its scenario) → 13. `trapcheck` →
   14. `guided` (transfer) → 15. `summary` → 16. `quiz`.

Estimated minutes land near 100 rather than 90; that is the honest cost of the three
added scenes and it is worth it.

## Rules that follow from this

- **Nothing good lives in a collapsed reveal.** If a passage teaches, it is a scene. The
  `refresh` text of a foundation check is for genuine revision only.
- **A foundation check must be answerable by the intended audience.** If it cannot be,
  it is lesson content wearing a prerequisite's clothes — promote it.
- **The first sixty seconds must produce one satisfying "oh", not four failures.**
- **Concrete before general, always.** The worked case precedes the theorem it instances.
- **Counterexamples come last.** The Cauchy at scene 2 teaches "this topic is full of
  horrors"; at scene 12, after the clean cases, it teaches what the theorem detects.
- **Carry every algebraic step**, including the index laws and the expansions. The gap,
  not the difficulty, is what makes a derivation unreadable.
- **Motivate in words the learner already has.** v2.0 opened by invoking Rao–Blackwell,
  completeness and exponential families — three things the reader does not know yet, so
  the motivation read as a list of further intimidations.
- **One exam-recognition line per teaching scene**, and a "recognising the question"
  paragraph in the summary. For 4.1: 'sufficient' → factorise; 'minimal'/'smallest' →
  ratio; 'from the definition' → conditional distribution. Three phrasings, three
  different pieces of work, and the marks go to the one that was asked.
- **Name what the concept is NOT**, where a plausible teaching shortcut plants an error.
  4.1 now says explicitly that a statistic is not an estimator, because the common
  shortcut "count the heads, so p̂ = 0.7" teaches sufficiency and that error together.

## Where a critique from outside was right, and where it was not

The user brought a critique of 4.1 written from two screenshots. It was right that the
exam connection was missing, that the theory scenes were too dense, that symbols arrived
unexplained, and that "zero all along" should be "zero almost surely". It was wrong that
the lesson lacked an intuition/worked/practice layer — those existed; the critic had seen
two of fourteen scenes. Its own replacement text would have introduced three errors worth
refusing:

- "The order doesn't matter, therefore ΣXᵢ is sufficient" is a non-sequitur.
  Order-irrelevance gives sufficiency of the ORDER STATISTIC, true for every iid model
  including the Cauchy. ΣXᵢ is sufficient because the likelihood factors through it.
- It computed p̂ = 7/10 under the heading "what information do you need?", conflating the
  sufficient statistic with the estimator.
- Its completeness warm-up (Y = ±1 with probability ½) drops the quantifier over θ, which
  is the entire content of completeness.

The lesson: adopt a critique's diagnosis of SYMPTOMS readily, and check its prescriptions
against the mathematics before shipping them.

## Verification for a re-sequenced lesson

- `node vcheck.js seed/lesson_<id>.json` — runs the app's own `vScene` plus the house
  standard checks statically, with no browser. Added for this rebuild.
- `node t1clicks.js` — drives 4.1 using ONLY real clicks: the start button, the footer
  Next through every scene, contents-panel jumps, the foundation rating buttons. No call
  to `gotoScene`. This is the test class that catches a dead control; the per-topic
  `t*test.js` files cannot, because they navigate programmatically.
- Check progress at `S.topics[tid]` (NOT `S.prog`): `seen.length` and `s` (0 not started,
  1 in progress, 2 complete). `s` stuck at 0 with a high document version is the
  signature of a click that never reached `markSeen`.

## The JRF-extension tier (added in v4.0, from an external review)

The best idea to come out of a pedagogical review of v3.0, and now part of the standard.

A scene may carry `ext: true`. It then renders with a "✦ JRF extension · optional" chip, an
opt-out banner, and an "optional" marker in both the contents rail and the overview route
list; the overview states the core path's section count and minutes before the learner
commits. Crucially, `markSeen` counts only non-`ext` scenes toward completion, so skipping
an extension still finishes the topic — otherwise the marking would be a lie.

Rules:
- Put the hard theory a pass does not need, but a JRF rank does, into ONE extension scene
  per topic rather than scattering it. In 4.1 that is Uniform(θ, θ+1) plus the Cauchy.
- The foundation, summary and quiz scenes can never be extensions. `vcheck.js` enforces it.
- The house range of 11–16 scenes now governs the CORE path; extensions sit outside it, and
  the whole lesson is capped at 18.

Two further additions from the same review, now standard:
- **A quick check on every teaching scene.** `askPane` moved out of the three scene
  renderers that had it and into `scenePane`, so any scene with an `ask` shows one.
  `vcheck.js` requires one on every scene except those that are themselves checks (recall,
  completion, trapcheck, guided, summary, quiz).
- **A `table` field** on any scene — `{head, rows, caption}` — rendered by `tableHTML`.
  Used for the family → statistic grid in the theorem scene and the summary. Prefer it to
  prose wherever the content is genuinely a grid; 4.15 will need it badly.

## What was declined from that review, and why

Worth recording, because the same arguments will recur:
- Its replacement mastery set of 10 single-answer recall items, in place of the 20-item
  pool across four formats. JRF is decided by the hard discriminating items.
- Removing the exponential-family block. It is what explains why sums recur, and 4.2
  (completeness) and 4.9 (Karlin–Rubin) both lean on it.
- Its verbal Cauchy treatment ("in general these terms cannot be reduced") in place of the
  ratio argument.
- Losing the likelihood-principle line and the map of where sufficiency is used later.

Two defects in its question set, as a reminder of what to check in any contributed items:
- Its Q6 offered (Σxᵢ, Σxᵢ²) as a distractor for a sufficient statistic with σ² known — but
  that pair IS sufficient there, merely not minimal, so the item is unsound as worded.
- Its keys ran C,B,A,C,D,B,C,C,D,C: five of ten on C, which the 40%-per-letter cap rejects.

The general lesson, same as before: take a critique's diagnosis of symptoms readily, and
check its prescriptions against the mathematics and the validators before shipping them.

## Mathematical precision: errors a second review caught in v4.0

Three were real, and they are the kind that survive a validator because the structure is
fine and only the mathematics is wrong. Worth checking for in every lesson:

- **Overclaiming a converse.** v4.0 said in two places that ONLY one-to-one functions of a
  sufficient statistic are sufficient. False, with a counterexample one line away: the
  whole sample is sufficient, and Σxᵢ is a many-to-one function of it that is sufficient
  too. The right statement is that one-to-one GUARANTEES preservation and many-to-one must
  be checked. Note the claim being judged in the trapcheck ("every function of a
  sufficient statistic is sufficient") was still false — the verdict was right and the
  reason was wrong, which no structural check can catch.
- **A dropped side condition.** (x̄, s²) ↔ (Σxᵢ, Σxᵢ²) needs n ≥ 2, because s² divides by
  n − 1.
- **A skipped step in a counterexample.** "The range has an expectation free of θ, so
  completeness fails" is not an argument. The range is ancillary with constant expectation
  c; it is the CENTRED g(T) = (max − min) − c, with E_θ[g(T)] = 0 for all θ and g ≢ 0, that
  violates completeness. State the centring.

Two statements also tightened: the Lehmann–Scheffé ratio criterion now carries its support
proviso (which is what makes the Uniform cases work, the ratio being of indicators), and
the Cauchy root argument is stated over multisets.

## The sufficient-versus-minimal item defect, now machine-checked

v4.0 declined to import a contributed question whose distractor was itself a valid
sufficient statistic. The second review pointed out that the app's own pool had the same
defect: `inf-t1-m-01` asked for "a sufficient statistic" for a Gamma rate while offering
(Σxᵢ, ∏xᵢ) as a distractor — and that pair IS sufficient, since anything determining a
sufficient statistic is sufficient. Two correct keys.

The rule: **a stem asking only for "a sufficient statistic" must not offer, as a wrong
answer, any statistic that determines a sufficient one** — a pair containing the right
summary being the usual trap. Either ask for the minimal statistic or change the option.
`vcheck.js` now flags it, and the check was verified against the defective pool before the
fix was accepted; a validator that cannot catch the bug it was written for is worthless.

`vcheck.js` also now validates the mastery pool named by the quiz scene (20 items, 6/10/4
difficulty, 40% key cap, format minima, numeric items carrying an arithmetic check, multi
items carrying four statements with verdicts), and scopes its house rules: engine A has no
worked scene, and the v4.1 standards (a quick check on every teaching scene, the how-to
note) are reported as advisories rather than failures on lessons authored before them, so
real errors stay visible.

### Open findings from sweeping every lesson with it

Not fixed — out of scope for the 4.1 work, and recorded here so they are not lost:
- 4.2 mastery pool difficulty mix is 4 easy / 11 moderate / 5 hard, not 6 / 10 / 4.
- 4.5 mastery pool mix is 6 / 9 / 5.
- 4.3, 4.6 and 4.9 carry fewer than three references each.
No other pool has the sufficient-versus-minimal defect.

## Round three: the one-to-one transform trap, and the confession check

The reviewer returned the pool as a JSON file with two stem corrections and every other
byte unchanged — the disciplined form the brief asked for, and both corrections were real.

The defect class is worth naming because it is easy to write and hard to see. **A
one-to-one function of a minimal sufficient statistic is itself minimal sufficient.** So
an item asking for "the value of the minimal sufficient statistic" has a second correct
answer the moment any distractor is such a transform — x̄ beside Σxᵢ for fixed n, or
(Σxᵢ/n, Σxᵢ²/n) beside (Σxᵢ, Σxᵢ²), or (x̄, s²) beside the natural pair.

**The fix:** name the statistic in the stem ("Taking T = ΣXᵢ, give its value"), or pin the
convention so the distractor's VALUE is wrong (defining s² with divisor n − 1 makes
(4, 2.0) wrong, since the unbiased value is 2.5).

**The confession check, now in `vcheck.js`.** The defect leaves evidence: the author
noticed and wrote it into the explanation as "a valid one-to-one transform" without fixing
the stem. The validator fails any item whose explanation concedes that while the stem asks
loosely for "the minimal sufficient statistic" and does not name it. Applying it across the
pool found the same defect in two items the reviewer had NOT flagged — m-04 and m-07 — so
a principle is worth applying everywhere it holds, not only where the reviewer applied it.
Verified by running the check against the pre-fix pool: it fires on all three and passes
on the corrected one. No other topic's pool has it.

Two of my own errors surfaced while working through their file, neither reachable by any
structural check:
- `m-03` verdict B called the dimension mismatch "the same mismatch that defines a curved
  family". U(θ, θ+1) is not an exponential family at all — its support moves with θ. A
  curved family also has dim(T) > dim(θ), but for an unrelated reason. Do not let the two
  explanations merge; the reviewer flagged the same conflation independently.
- `m-05`'s explanation attached the support discussion to option D when it belongs to
  option B.

Two lesson statements scoped on the reviewer's advice: the MLE is a function of a
sufficient statistic **when it exists and is unique** (otherwise it is the set of
maximisers that is determined), and the likelihood-principle equivalence holds under the
same support and regularity conditions as the ratio criterion, not unconditionally.

## Formats for a model reviewer, versus a human one

The reviewer here is a language model, which changes the right deliverable:
- **Markdown, never PDF.** A model reading a PDF reads a layout extraction: tables lose
  their shape, reading order can scramble, and sub/superscripts drop silently, so `Σxᵢ²`
  can arrive as `Σxi2` — a different statistic, in a document whose purpose is checking
  precision. `export_md.py` writes the Markdown; `export_t1.py` still writes the PDF and
  Word versions for a human.
- **Every field carries its JSON path** (`scenes[10].blocks[1].body`). A finding that
  cites a path can be applied mechanically; one that describes a section has to be hunted.
- **Ask for a findings list, not a rewrite.** The first two rounds returned whole rewritten
  lessons and material was lost in the re-typing both times. The third round returned a
  JSON diff of two fields, which was worth more than either.
- **Ship the source JSON too**, so the reviewer cites something real rather than a
  transcription.
- Maths stays Unicode. Transliterating it to LaTeX is a chance to introduce errors into
  the exact text being checked for them, and the reviewers have read the Unicode fine.
- Note that a reviewer may be a round behind: round three's prose document was written
  against v4.0 and repeated findings v4.1 had already fixed. Check the version it cites
  before re-applying anything.

## Round four: a whole-module review, and a data-loss hazard it exposed

The reviewer returned the whole module. Its JSON diff was precise — pools byte-identical,
nine lesson files changed — and two things in it were worth taking:

- **28 per-scene quick checks for 4.2–4.9**, on theory, worked and explore scenes. Actual
  content production filling the gap recorded above, and all 28 checked for correctness
  before import. One nudge was reworded: "non-zero unbiased functions of the statistic
  with expectation zero" garbles the condition — completeness concerns non-zero functions
  whose expectation is zero, and "unbiased" does not belong in it.
- **The MLE overclaim**, which v4.2 of 4.1 had qualified in one place while leaving the
  blanket claim standing in the revision sheet and the summary scene. A correct finding,
  and the inconsistency was introduced by that very fix. Qualify a claim everywhere it
  appears, in the same pass, or the lesson contradicts itself.

Applying the finding more widely, as in round three, again found more than the review did:
a third copy of the same MLE claim in 4.4's prerequisite recall; 4.3 asserting MLE
invariance "holds always" with no existence caveat; and 4.7 claiming the posterior
"always" lies between the prior mean and the MLE and the prior "always" washes out as n
grows — both true for the conjugate families in that scenario, neither true in general,
since a prior whose support excludes the truth never washes out.

**Declined:** 24 further quick checks offered for completion and guided scenes. Both kinds
already end with the learner writing something — five graded blanks, or a model solution
behind a hint ladder with a "Your answer" box — so a second question box there is clutter.
Also declined: a rewritten `howto` for 4.1 that drops the sentence about the optional JRF
extension, and the nine "13-part reference" companion documents, whose own upgrade report
states that theorem conditions, numerical claims, answer keys and every MCQ distractor are
unvalidated — 90 new MCQs on that footing is a liability, not an asset.

### The hazard: authoring scripts silently behind their seeds

`check_drift.py` was added because of this round and it fails loudly: **every lesson_*.py
in Unit IV is behind its seed.** The seeds were enriched after generation (to v1.2, and now
v1.3) and the scripts were never updated — `lesson_mle.py` does not even contain the
prerequisite text this round had to change. Running one of those scripts would overwrite
its seed with older content and lose the enrichment **silently**: the JSON stays valid and
every validator still passes.

Consequences for how this project works:
- **Run `check_drift.py` before running any lesson_*.py.** It exits non-zero on drift.
- Content edits to an already-enriched lesson go to the **seed**, which is what the app
  serves and what the store holds. The seed is the source of truth, not the script.
- The scripts need regenerating from the seeds before they can be trusted again. Until
  then they are history, not build tooling.

### A live bug found while exporting the module

Generalising the exporter to nine lessons forced a walk over every field of every one, and
that surfaced a real defect: 4.5 and 4.9 scene 2 were rendering a "Think before
continuing" box with **no question in it**, because those two lessons carry a legacy ask
shape `{label, prompt, tier}` holding a pre-written Claude prompt rather than a self-test
question. `askPane` now requires `ask.q`, and the legacy shape renders as its own "Ask
Claude this" button that opens the panel pre-filled. The navigation tests never caught it
because they only check that scenes advance — exporting everything did.

First attempt at a test for it reported 18 failures, 16 of them false: guided scenes render
their own `.think` box labelled "Your answer", which legitimately has no question. Target
askPane's box by its heading, not by the class alone.

### An unresolved question of scope

This review audits against a **13-part lesson standard** that was given to it elsewhere and
that this project has never seen. Its findings 2–7 are non-compliance with that spec, not
defects in the content: no dedicated `glossary`, `conceptMap`, `decisionFlowcharts`,
`gradedExamples` (two basic, two intermediate, two JRF), `formulaSheet` with assumptions,
or fixed 10-question practice set separate from the 20-item mastery pool. Several are
reasonable asks. None can be implemented without the spec, and implementing a guess at it
would be worse than asking. Get the 13-part specification before acting on those findings.

## Formula layout, and the lesson about where formulas actually live

The content was authored as one-line plain text — exponents as `^(...)`, denominators as
a slash — which reads as code, not as mathematics. `src/32-math.js` now lays it out.

**One parser, three renderers.** A small lexer builds a node tree (brackets, exponents,
fractions); the app renders it to stacked HTML, `mathrender.js` renders the SAME tree to
print HTML for the PDF and to LaTeX for the Markdown export. The exporters shell out to
that one implementation rather than carrying a second one that could drift.

**It refuses rather than guesses.** Anything that does not lex cleanly comes back as the
original one-line string. 282 of 287 authored formulas are handled; the 5 refusals show
plainly, which is the right trade — a formula shown plainly costs little, a formula
silently rearranged costs a mark.

**Character preservation is necessary and NOT sufficient.** The first version passed a
character check while rendering `p/p²` as `(p/p)²` — nothing lost, different formula. A
second regrouping bug, `p(1−p)/16` putting only `(1−p)` over 16, survived the same check.
Both were caught only by assertions on the output STRUCTURE. Any transformation of
authored mathematics needs structural tests, not just character counts.

### Where the formulas actually were

Three rounds of "this is still on one line" came from the same mistake: assuming formulas
live in formula fields. They do not.

1. First fix covered `steps[].math` and theory `formula` blocks — the app only.
2. Then the PDF, which still showed the authored one-line text, because the exporters were
   never touched. Fix the app and the documents together; people review the documents.
3. Then prose, which is where most of the maths actually is. Carets appear in ~25
   different fields: scene bodies, theory block bodies of every type, step reasons,
   prerequisite rebuilds, revision sheet lines, flashcards, memory aids, hints, question
   stems, options and explanations. `richText()` raises exponents in all of them.

Two related errors found on the way:
- **`formula` blocks are prose**, not display formulas. Their bodies read "T is sufficient
  for θ if and only if the joint density factorises as …". Running the display layout over
  them set a paragraph in formula type and broke it at every `=`. Theory blocks are prose
  with maths inside; only `steps[].math` is a formula by contract.
- **`step` theory blocks were rendered in monospace**, which is why they looked like code.
  They are prose too.

**Inline fractions stay slashed on purpose.** A stacked fraction mid-sentence throws the
line spacing out; books set inline fractions with a slash and display fractions stacked.
Stacking is for formulas that have a line to themselves.

**Verification that matters here:** a test that walks every scene of every lesson and
asserts no caret is visible anywhere, and that no markup leaked into the text. It found
the revision rail, the memory aids, the prerequisite cards and the provenance note after
the main sweep looked clean — the rail is persistent, so its carets appeared on every tab.

Interface wording was simplified in the same pass: "Nudge me" → "Give me a hint", "Think
before continuing" → "Try this before you go on", "Ground yourself" → "What you need
first", "Traps" → "Common mistakes", and so on. The exports carried the old wording for a
turn afterwards — when UI wording changes, change the exporters' labels too.

## Still to apply

4.2–4.9 were authored in the old order and would benefit from the same pass; it is mostly
relocation of existing prose. 4.10–4.17 should be authored in the new order from the
start, which costs nothing extra at authoring time.
