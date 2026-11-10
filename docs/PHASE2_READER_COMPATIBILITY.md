# Phase 2 — reader compatibility inventory (GPT draft)

Status: **read-only findings for joint review; not a binding contract**.
Code inspected on `multi-author-hosting`: `src/10-const.js`, `src/40-render.js`,
`src/52-bank.js`, `src/53-drill.js`, `src/54-mock.js`, `src/62-gen.js`,
`src/70-wire.js`, and `vcheck.js`.

## 1. Scene kinds: the app's structural validator

The app's `vScene()` in `src/62-gen.js` explicitly recognizes these kinds and requires
the following base fields (in addition to a title):

| Kind | Required fields checked by `vScene()` |
|---|---|
| foundation | `body`, `items` |
| intuition | `body` |
| explore | `body`, `viz` |
| theory | `blocks` |
| worked | `problem`, `steps` |
| recall | `intro`, `items` |
| completion | `problem`, `steps` |
| guided | `problem`, `hints`, `solution`, `answer` |
| trapcheck | `intro`, `items` |
| summary | `body` |
| quiz | `setId` |

The same validator adds deeper checks for foundation prerequisite checks, guided hint count,
worked-step fields, completion blanks, trapcheck verdicts, recall question/answer pairs,
flow diagrams, scenarios, and allowed visualization types. Those rules are pedagogical and
structural checks implemented in application code; they should not all be copied blindly into
a JSON Schema. In particular, the lesson-wide house standard in `vcheck.js` is a separate
quality gate and is not the general shape of every lesson record.

## 2. Question formats: app behavior and validation

`src/10-const.js` defines the five supported formats and their learner-facing labels:
`single`, `numeric`, `multi`, `match`, and `order`.

Observed reader behavior in `src/53-drill.js`:
- `multi`: learner must record a true/false verdict for every statement before reveal.
- `numeric`: learner must confirm written working and check the requested quantity.
- `match` and `order`: learner must confirm they worked out the rows/order before reveal.
- `single` uses the ordinary four-option interaction.
- Matching reads `pairs`; ordering reads `items`; multi-statement reads `statements` and
  `verdicts`; all formats may show `check` and `explanation`.

`src/62-gen.js`'s `vQset()` checks general item identity, stem, explanation and difficulty,
then adds format-specific checks:
- `multi`: four statements and a boolean verdict plus reason for A–D.
- `numeric`: a terminal-check line.
- `match`: four pairs.
- `order`: four ordered steps.
- Pools with `source === "mastery"` have extra machine-scoring, count, format-mix and answer-key
  distribution rules. These mastery-only rules must not become universal pool rules.

The separate `vcheck.js` script also checks a named lesson's quiz pool against its strict
20-question mastery authoring pattern. That is not a universal requirement for every qset.

## 3. Contract implications

1. Keep the schema's current permissive extension policy until every legacy shape is tested.
2. A future schema can use conditional branches for the five formats and eleven scene kinds,
   but should distinguish universally required fields from mastery-only or house-standard rules.
3. Keep `vScene()`, `vQset()`, and `vcheck.js` as the existing behavior/quality references
   until a deliberate, tested migration replaces or shares their rules.
4. Add one valid and invalid fixture per scene kind and item format before enabling schema
   enforcement.
5. Confirm whether any consumer outside the inspected files relies on fields not listed here
   before declaring this inventory complete.

No runtime files, seeds, learner data, PR #4, production branch, or deployment settings were changed.
