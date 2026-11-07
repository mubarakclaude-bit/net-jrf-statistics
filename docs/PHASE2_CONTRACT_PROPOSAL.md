# Phase 2 — contract design proposal (GPT draft)

Status: **proposal only; not an authoritative contract**.
Base: `multi-author-hosting`.
This document is deliberately outside `contracts/`. The architecture assigns contract changes to
both authors for approval. Claude and the owner should review this proposal before schemas become
binding or CI starts rejecting contributions.

## Purpose

Make independently authored lessons, question pools, and learner-progress backups predictable.
A valid contribution from GPT, Claude, or a human should have the same meaning and pass the same
checks before it is merged.

## Ground rules

1. Derive schemas from the committed seed data and the app's actual readers/writers, not from an
   idealised redesign.
2. Separate **structural validity** (JSON shape and types) from **authoring quality** (scene counts,
   pedagogical requirements, answer balance, explanation quality). Keep the current lesson
   validator as the quality gate; schemas must not silently replace it.
3. Start permissive where legacy lessons demonstrably vary. Tighten only after an audit reports
   that every existing seed satisfies the proposed rule.
4. Version every externally exchanged record. A progress backup must identify its format version,
   app schema version, and selected learner profile.
5. Define valid document paths separately from collection paths. In particular, a document path
   must have an even number of segments in the current document-store model.
6. Keep profile-scoped feedback separate. A learner's feedback record must be keyed by both learner
   and profile so one profile cannot overwrite another profile's feedback.
7. No schema or path-contract change is authoritative until both authors approve it.

## Proposed contract files

| File | Responsibility |
|---|---|
| `contracts/lesson.schema.json` | Structural shape of a lesson seed, including scene variants |
| `contracts/pool.schema.json` | Question-set envelope and supported item variants |
| `contracts/progress-backup.schema.json` | Portable backup envelope and the nine current progress records |
| `contracts/storage-paths.json` | Named document paths, path builders, ownership/profile rules |
| `contracts/README.md` | Versioning, compatibility and change-approval rules |

Use JSON Schema Draft 2020-12 unless the repository's eventual validator choice requires a
documented compatible subset.

## Inventory required before writing binding schemas

A first read-only storage inventory is recorded in [`PHASE2_STORAGE_INVENTORY.md`](./PHASE2_STORAGE_INVENTORY.md). A corresponding lesson and question-pool inventory is recorded in [`PHASE2_CONTENT_INVENTORY.md`](./PHASE2_CONTENT_INVENTORY.md). It captures the nine current progress records, profile-aware path convention, and two unresolved points: the current progress-backup draft omits `profileId`, and feedback is currently learner-scoped rather than profile-scoped. This inventory is a draft for review, not a binding contract.


- Enumerate every `seed/lesson_*.json` and every question-set seed discovered by
  `tools/seed-docs.js`.
- Collect top-level keys, required keys, types, enum values, and optional fields across all seeds.
- Enumerate all scene `kind` values and each kind's actual shape. Do not assume one scene schema
  covers all scene types.
- Enumerate question `format` values and their conditional fields (for example, multi-statement,
  match, order, numeric).
- Read all progress save/load call sites and document the current record envelopes before defining
  their schema.
- Run the candidate schemas against the complete existing seed set and report every failure.
  Do not fix legacy content as a side effect of introducing schemas.

## Validation plan

1. Add a deterministic Node validator that loads the schemas and validates all lesson and pool
   seeds discovered by `tools/seed-docs.js`.
2. Keep `vcheck.js` for pedagogical/house-standard checks. The schema validator complements it.
3. Run the same checks locally and in `.github/workflows/validate.yml`.
4. Add negative fixtures for missing required fields, wrong types, unsupported enums, malformed
   question variants, and invalid document paths.
5. Add compatibility fixtures for optional legacy fields and every valid scene/item variant found
   in the inventory.
6. CI should fail on invalid new or changed seeds; the initial full-repository audit should be
   reported separately so pre-existing legacy issues are visible rather than hidden.

## Progress backup envelope — proposed semantics

The envelope should include:

- `format`: stable identifier, e.g. `net-jrf-statistics-progress`
- `version`: backup-format version (independent of app schema version)
- `schemaVersion`: app progress-record schema version
- `exportedAt`: ISO-8601 timestamp
- `sourceUserId`: informational origin only; never use it as the destination identity on import
- `profileId`: the profile whose records are exported (including an explicit value for the default
  profile)
- `records`: the exact, documented set of progress records

Import must always write under the currently authenticated learner and currently selected profile,
never under `sourceUserId`. Replacement versus merge semantics must be explicit in the UI and
contract. Until merge rules are designed, replacement-only is safer.

## Storage-path contract — proposed semantics

For each path, record its purpose, owner, scope, document/collection kind, and path builder.
A conformance test should reject odd-segment document paths and verify profile scoping.

Known design issue to resolve: current `fbPath()` is `feedback/<uid>`, while profile-scoped
progress uses `data/users/<uid>/p/<profile>/<record>`. The contract should decide whether feedback
is profile-specific and, if so, define a backwards-compatible migration/read strategy rather than
simply changing the path and losing visibility of old feedback.

## Decisions for joint review

- Whether the default profile is represented as `"me"` or a distinct stable profile key in backup
  files. The app currently uses `"me"` internally for the default profile.
- Whether schemas are strict (`additionalProperties: false`) or allow documented extension fields.
  Recommendation: strict at stable envelopes; scene/item variant objects should allow only fields
  supported by the app, with an explicit extension mechanism if needed.
- Whether CI validates all seeds on every PR or only changed seeds plus a scheduled full audit.
  Recommendation: changed seeds on PR, full audit on demand/nightly.
- Whether progress record validation lives in JSON Schema only or also has runtime validation before
  export/import. Recommendation: both, sharing the same schema definitions.

## Out of scope for this draft

- No changes to app runtime, storage adapter, learner data, production branch, or Vercel settings.
- No attempt to migrate Claude ArtifactData records.
- No changes to PR #4 or any other author's branch.
- No authoritative files under `contracts/` until joint approval.


## Post-bootstrap independence requirement (owner's explicit requirement)

Once the initial shared foundation is complete and jointly accepted, neither GPT nor Claude
may be a runtime, authoring, validation, or release dependency of the other.

That means:

- **No author-specific tooling:** lesson and feature contributions use repository contracts and
  documented commands, not private prompts, hidden scripts, session state, or one author's memory.
- **Self-contained contributions:** a lesson carries its own content, pool, authoring/verification
  material; a feature carries its own module, storage-key declaration, tests and documentation.
- **Stable machine-readable contracts:** schemas and storage interfaces are versioned, committed,
  and validated in CI. Either author can independently produce a conforming contribution.
- **Automated integration:** discovery, index generation, test registration, bundling and validation
  are deterministic repository processes; no other author has to manually wire a contribution.
- **Independent tests:** each contribution has tests that run from a clean checkout. Shared adapter
  conformance tests run against every supported backend.
- **No cross-author approval bottleneck for ordinary work:** after the foundation is approved,
  either author may add a conforming lesson or an isolated feature without the other author
  changing files, preparing data, or being online. Review remains required by the repository's
  normal PR policy, but review must not require the other author's private environment.
- **Compatibility policy:** breaking changes to shared contracts require a new version and an
  explicit migration path. Existing conforming lessons/features must continue to validate against
  the supported contract version.
- **Reproducible release:** CI builds from repository contents alone. The Claude artifact is an
  optional generated output and must not be required for hosted-site builds, tests, or learner data.

The acceptance test for the architecture is practical: after a clean clone, either author can
independently add a valid lesson and a valid feature, run the documented checks, open a PR, and
obtain the same deterministic build without contacting the other author or transferring files.
