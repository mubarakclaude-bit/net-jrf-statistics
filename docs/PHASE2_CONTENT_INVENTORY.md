# Phase 2 — lesson and question-pool inventory (GPT draft)

Status: **observed-shape inventory for joint review; not a binding schema**.
Source inspected: Phase 1 seed layout on `multi-author-hosting`, using `tools/seed-docs.js` and representative lesson and pool documents.

## 1. How seeds become hosted documents

The source-of-truth rules in `tools/seed-docs.js` are:

- Every `seed/lesson_*.json` is considered a lesson seed and becomes `lessons/<lesson.id>` when it has an `id` and a `scenes` array.
- Every other JSON seed with an `items` array becomes `qsets/<file stem>`.
- `seed/catalog.json` and `seed/meta_syllabus.json` become `meta/catalog` and `meta/syllabus`.
- `meta/lessons` is generated from lesson seeds; it is not manually authored.
- `listSeeds()` records malformed lesson JSON as an error. Non-lesson JSON without an `items` array is not classified as a qset.

This classification is important: do not invent a second file-to-document mapping in the schemas or CI.

## 2. Lesson envelope — observed required and optional fields

The current seed builder's explicit minimum is:

`id`, `title`, `moduleId`, `estMin`, `scenes`, `status`, `version`, `topicId`.

It additionally requires `scenes` to be an array. It checks duplicate `topicId` and duplicate store document `id`. Quiz scenes whose `setId` does not match a question-pool filename and topic IDs absent from the catalog are warnings, not errors, in the current generator.

Observed lesson documents also use a richer set of fields, including:

- identity / navigation: `breadcrumb`, `engine`, `engineName`
- teaching structure: `objectives`, `prereq`, `traps`, `revision`, `howto`
- academic provenance: `refs`, `provenance`
- assessment policy: `mastery`
- scene content: `scenes`

These richer fields are not all present in every sampled generation. For example, an earlier lesson generation includes `howto` while a later time-series lesson carries `objectives`, `prereq`, `traps`, `revision`, `refs`, and `mastery`. The eventual schema must not make a field mandatory merely because it appears in one recent lesson.

## 3. Scene envelope — deliberately extensible

Observed scene kinds include:

`foundation`, `intuition`, `theory`, `recall`, `completion`, `guided`, `trapcheck`, `summary`, `quiz`, `explore`, and `worked`.

Observed scene properties include:

`id`, `kind`, `title`, `mins`, `objective`, `intro`, `body`, `blocks`, `ask`, `problem`, `solution`, `steps`, `answer`, `check`, `hints`, `items`, `flow`, `scenario`, `setId`, `after`, `ext`, `table`, and `viz`.

These are not one uniform shape: the properties depend on the scene kind and on the teaching interaction. A future schema should use a common scene base plus kind-specific optional structures or a carefully designed discriminated union. It must preserve unknown extension fields during validation/migration until the authoring team has mapped every existing scene variant. A strict `additionalProperties: false` at the first rollout would risk rejecting existing lesson content.

## 4. Question-pool envelope

Observed pool documents use:

- `moduleId`
- `source` (observed values include `variant`, `pyq`, and `mastery`)
- `label`
- `count`
- `items` (array)

Some pools additionally carry `topicId`. Do not require it for every pool based on the current samples.

The item `format` determines its content:

| Format | Observed structure |
|---|---|
| `single` | `stem`, `options`, `answer`, `explanation` |
| `numeric` | `stem`, `answer`, `explanation`, `check`, with `options: []` |
| `multi` | `stem`, `statements`, `options`, `answer`, `verdicts`, `explanation` |
| additional formats | Must be inventoried across all seed files before a closed enum is approved |

Other observed item fields include `id`, `topic`, `paper`, `year`, `pno`, `diff`, `pairs`, `items`, and `needsReview`. Their use varies by item and format. For a `multi` item, `verdicts` is keyed by answer letter and each entry has `tf` and `why`. Numerical items may carry a textual answer and validation hint in `check`; do not constrain answers to numbers only.

## 5. Cross-document relationships

- A lesson's `topicId` is expected to match a topic in `seed/catalog.json`; currently this is a warning.
- A lesson quiz scene's `setId` is expected to match a qset filename stem; currently this is a warning.
- `tools/gen-index.js --expect <topicId> <storeDocId> <masterySetStem>` checks the named lesson, quiz scene and pool. It additionally expects exactly 20 items in that pool.
- The current lesson index uses the topic ID as its key and stores `id`, `title`, `moduleId`, `estMin`, scene count, `status`, and `version`.

The 20-item expectation belongs to the strict authoring command's mastery-set workflow. It should not automatically become a universal rule for all question pools.

## 6. Contract design recommendations for joint review

1. Keep the eight current lesson minimum fields as the compatibility baseline, then add kind-aware checks only after all 48 lesson seeds have been inventoried.
2. Define qset envelope and item formats separately. Do not apply a single item shape to single-choice, numeric, multi-statement, matching, ordering, or any additional formats discovered in the full audit.
3. Keep warning-level relationships warning-level during initial rollout. Convert to errors only after legacy exceptions are enumerated and fixed deliberately.
4. Validate IDs, array/object types, answer references, and safe path identifiers without changing content.
5. Preserve source fields and extensions. The first schema rollout should be additive and non-destructive.
6. Add representative fixtures for every scene kind and question format to the conformance suite.
7. Run the inventory over the complete seed set before finalising the closed format enum or strict per-kind scene rules.

## 7. Scope and safety

This document records observed structures only. It does not edit seed files, rewrite lesson content, alter the live database, enforce schemas in production, or merge the separate progress-transfer PR. The full seed scan and both authors' review are still required before the contracts become binding.
