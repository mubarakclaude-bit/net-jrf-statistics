# ARCHITECTURE

Goal: **Claude and GPT (or any human) each work independently — add content, change features — and
their work merges without either author reading the other's tooling.** Everything below serves that.

Decisions (made by the owner, 2026-11-07):
1. **The hosted site is the primary product.** The repo is the only source of truth. The Claude
   artifact becomes an optional, *generated* copy; it is never an authoring surface.
2. **A light bundler (esbuild) replaces shell-script concatenation** when the features are split (phase 4).

## What was blocking independent work

| Problem | Evidence | Fix | Phase |
|---|---|---|---|
| Every new lesson edited two shared files (`test.js`, `seed/meta_lessons.json`) | Two parallel lesson additions conflicted in both files | Generate both from `seed/`; commit neither | **1 — done** |
| The same `seed/` scan was written three times, one with a ~90-entry hand-edited list | `test.js` had silently dropped 6 inference questions | One module: `tools/seed-docs.js` | **1 — done** |
| The Claude artifact was the real backend (`ArtifactData` reachable only from a Claude session) | GPT could not read, push or test the live store | Hosted site primary; artifact generated | 1 (decision), 3 (adapter) |
| No spec for a lesson, a pool or a progress record; each author inferred it from code | PR #4 was reviewed by writing tests afterwards and found 4 contract gaps | Versioned JSON schemas + CI | **2 - done** |
| Two backends behaved differently, so a path valid in one failed in the other | PR #4's snapshot path has 5 segments, which the artifact store treats as a collection | One storage interface, one conformance suite run against both (the path rule is already enforced at run time) | 3 |
| The app is one global `S` and one giant `wireAll()` | Two features cannot be edited without touching the same functions | Feature modules with a registry, bundled by esbuild | 4 |

## Phase 1 — delivered

- `tools/seed-docs.js` is the only place that turns `seed/` into store documents:
  `lessons/<id>` from `seed/lesson_*.json`, `qsets/<stem>` from every other seed with an `items` array,
  `meta/lessons` **generated** from the lesson seeds. It is read-only.
- `tools/gen-index.js` writes the generated index (`.cache/meta_lessons.generated.json`), validates the
  set (`--check`), and asserts one lesson is wired as its author says (`--expect`).
- `test.js` and `build_site.js` use the shared builder. `addlesson.sh` edits **no** shared file; it asserts wiring.
  `check.sh` validates the seed set. `seed/meta_lessons.json` is untracked and ignored.
- Verified: the hosted bundle built the new way equals the old bundle document for document (the only difference
  is the unused `updated` and `v` keys of the index); `test.js` and `clicktest.js` pass; and a simulated
  parallel addition of two lessons merges cleanly, where the same two additions made the old way conflict in
  both shared files.

**Rule:** a lesson PR touches only its own files — `seed/lesson_<stem>.json`, its `seed/*_mastery.json`, and its
authoring and verification scripts. A lesson exists because its seed exists. Nothing lists lessons by hand.

**In-flight branches written before this change** (for example regression-t7) edit `test.js` and
`seed/meta_lessons.json`. When they merge, take the new base's `test.js`, drop their edits to it, and delete
`seed/meta_lessons.json` (modify/delete conflict: accept the deletion). Their lesson files need no change.

## Phase 2 - contracts (delivered; pending the owner's approval of the PR)

`contracts/` holds the machine-checkable definition of a conforming contribution: lesson, question pool (and the
20-item mastery profile), progress backup (version 2, with `profileId`), pre-import snapshot, feedback (per profile),
the storage-path rule, and `legacy-exceptions.json`. `npm run contracts` validates the contracts against the app source
they mirror, runs 42 valid and 77 invalid fixtures, checks every literal path in `src/`, and validates all 48 lessons
and 63 pools. The path rule is enforced at run time (the test stub, the hosted shim). `npm run acceptance` proves the
independence requirement for content. GPT's drafts (PR #5) were the starting point; see `docs/PHASE2_REVIEW.md` for
the six decisions, the disagreements and the requirements added. Rules for changing a contract: `contracts/README.md`.

## Phase 3 - storage adapter (first slice delivered)

Delivered: features reach learner data only through `ctx.store` (`get`, `set`, `remove`), which allows only the keys the
feature declares and writes to contract-valid paths (`data/users/{uid}/features/{id}/{key}`, under `p/{profile}/` for a
non-default profile). The path rule is enforced in the test stub and the hosted shim. Not yet: a formal adapter interface
with a conformance suite run against the artifact backend as well as the hosted one. The hosted backend is the supported
one and is tested on every PR; the artifact backend stays generated output and is not required for independence.

## Phase 4 - feature modules (host and mechanism delivered; extraction pending)

Delivered: `src/14-features.js` is the one-time plug-in point (registry, routes, navigation entry, error isolation).
`tools/build-features.js` discovers `src/features/<id>/` and generates the registrations, deterministically, wrapping
each feature in its own scope. `contracts/feature.schema.json` and the validator enforce the manifest, the folder name
and the storage declarations. `tests/features.test.js` runs every feature's own browser test in strict path mode. Two
reference features (`ref-counter`, `ref-about`) are the living templates. A plain generator is used and not a bundler:
it needs no installed package, which keeps the Vercel build dependency-free. esbuild stays the plan if real ES-module
imports are needed when the built-in views are migrated. Progress has been extracted (it uses `replaces` and the host interface `ctx.app`). Pending: Home, Learn,
Question bank, Mock tests and Admin, one per PR; until then two authors must not change the same built-in view.

## Lanes and rules

| Lane | Owns | Rule |
|---|---|---|
| Content | `seed/`, `lesson_*.py`, `verify_*.py`, `BACKLOG.md` | Touch only your lesson's files. Claim with a draft PR on `lesson/<topic-id>`; run `./whats-next.sh` first if it exists on your base. |
| Feature | `src/`, feature tests | One feature per PR. Add a test with it. |
| Contract | `contracts/`, `tools/`, `.github/workflows/` | Changes need approval from **both** authors, because everything else depends on them. |

Every PR is reviewed by a different author from the one who wrote it. The hosted site deploys from the
production branch; the artifact is pushed separately and is never authoritative.

## Related documents

`AGENTS.md` (how to author), `SPEC.md` (the lesson standard), `CLAUDE.md` (Claude-specific). The branch
`automation/max-pipeline` carries a review-agent workflow (`agents/CONTRACTS.md`,
`docs/LESSON_PRODUCTION_ARCHITECTURE.md`); it describes *who reviews what*, and this file describes *how the code
and data are organised*. They are complementary and should be reconciled when that branch merges.
