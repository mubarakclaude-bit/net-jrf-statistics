# Phase 2 — observed storage inventory (GPT draft)

Status: **read-only inventory for joint review; not an authoritative contract**.
Runtime source inspected: `multi-author-hosting` at the Phase 1 baseline.
Progress-backup implementation inspected separately in the open progress-transfer PR (#4); that PR is not merged and is not part of the hosted baseline.

## 1. Current learner/profile model

The hosted baseline keeps the authenticated learner ID in `S.uid` and the selected profile in `S.profile`. The default profile is represented internally by `"me"`.

The path builder in `src/13-db.js` preserves the original unprofiled paths for the default profile. For a non-default profile, it inserts `p/<profileId>/` before the record name.

## 2. Observed document paths

| Document path | Purpose | Scope / notes |
|---|---|---|
| `meta/catalog` | syllabus/catalog | shared app data |
| `meta/index` | question-bank index | shared generated app data |
| `meta/app` | app configuration | shared app data |
| `meta/lessons` | lesson index | shared generated app data |
| `meta/personal` | personal metadata | shared app data; reader exists in boot |
| `meta/syllabus` | syllabus ordering | shared app data |
| `lessons/<lessonId>` | lesson document | shared content |
| `qsets/<setId>` | question-set document | shared content |
| `data/users/<uid>/<record>` | learner progress record | default profile |
| `data/users/<uid>/p/<profileId>/<record>` | learner progress record | non-default profile |
| `feedback/<uid>` | learner asks/requests | shared feedback document, currently learner-scoped rather than profile-scoped |

The nine progress record names currently loaded by `loadProfileData()` are:

`attempts`, `mocks`, `topics`, `errors`, `config`, `mastery`, `requests`, `notes`, and `asks`.

Observed record envelopes in `src/13-db.js`:

| Record | Stored envelope |
|---|---|
| attempts | `{ a: S.att, v: SCHEMA }` |
| mocks | `{ list: S.mocks.slice(-60) }` |
| topics | `{ t: S.topics }` |
| errors | `{ list: S.errs.slice(-400) }` |
| config | `S.cfg` |
| mastery | `{ m: S.mastery, v: SCHEMA }` |
| requests | `{ list: S.reqs.slice(-300) }` |
| notes | `{ n: S.notes }` |
| asks | `{ list: S.asks.slice(-400) }` |

These are observed shapes, not proposed schema guarantees. Some fields are optional and legacy records may differ.

## 3. Progress-backup proposal gap found in PR #4

The open progress-transfer PR currently proposes a backup envelope with:

- `format: "net-jrf-statistics-progress"`
- `version: 1`
- `schemaVersion: SCHEMA`
- `exportedAt`
- `sourceUserId`
- `records` containing the nine record names above

**It does not currently export a `profileId`.** The import path does write into the currently selected profile because it uses the existing profile-aware path builder; it does not use `sourceUserId` as the destination identity. However, without `profileId`, a backup does not say which source profile it represents. The contract should require a profile identifier, including an explicit default-profile value, before the feature is considered complete.

The PR also creates a pre-import snapshot at:

`data/users/<uid>/progress-snapshots/<snapshotId>`

Its snapshot envelope currently includes `format`, `version`, `createdAt`, `learnerId`, `profile`, and `records`. The snapshot path has an even number of segments and is a document path under the current document-store convention.

## 4. Feedback scope issue

The current `fbPath()` is `feedback/<uid>`, and the document stores asks/requests with a `label` for the selected profile. This means the feedback document itself is learner-scoped, not profile-scoped. The contract must decide whether feedback should remain learner-wide with profile labels or become profile-specific. If it changes, preserve visibility of existing feedback through an explicit read/migration strategy.

## 5. Path parity rule

The observed document paths above have an even number of slash-separated segments. The proposed path validator should distinguish document paths from collection paths and enforce even segment counts only for document paths. It should also test that non-default profile records cannot collide with the default profile or another profile.

## 6. Review boundaries and next work

- This inventory does not change runtime code, stored learner data, or PR #4.
- It does not establish a final JSON Schema.
- Before writing binding schemas, inspect the actual export/import implementation and agree on the missing `profileId`, snapshot retention, replacement/rollback behavior, and feedback scope.
- After joint approval, add schemas and conformance tests for all nine record envelopes and path builders. Keep the initial audit informational until existing records have been checked.
