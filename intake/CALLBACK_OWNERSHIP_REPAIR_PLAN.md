# Intake callback ownership binding — repair design

Status: partial implementation in draft PR; not live-tested or production validated.\n\nThe intake dispatcher now generates and persists `active_attempt_id` at the processing transition, sends it to the processor, and callback settlement checks the identity against the ledger. The processor adopts this authorized ID for its artifact prefix and manifest. Migration 0005 adds the field. Remaining verification: callback race fixtures, failure/rotation policy, schema/migration execution, live runtime.

## Problem
The processor callback currently carries an attempt ID and fencing token, and the manifest repeats them, but the intake ledger has no durable active-attempt identity to compare against. Integrity validation alone is not ownership validation. A callback can therefore pass manifest integrity checks without proving that the attempt is the intake ledger's current authorized attempt.

## Proposed ownership protocol
1. The intake dispatcher creates a fresh random `active_attempt_id` before changing a job to `processing`. Persist it in the intake ledger in the same conditional update that claims processing. The active identity must not be inferred from a processor callback.
2. Send `active_attempt_id` in the processor dispatch payload. The processor must use this externally authorized attempt ID (not mint a replacement) for its artifact prefix, manifest, callback and idempotency key. It still uses its own fencing token to protect its processor D1 execution claim.
3. Intake callback must compare callback `attempt_id` against ledger `active_attempt_id` before manifest retrieval and again in a conditional completion update. Reject mismatch with 409. Callback completion SQL should include `id=? AND status='processing' AND active_attempt_id=?`; changes must equal one.
4. Attempt IDs are rotated when a new dispatch is authorized. Failed/retryable transitions clear or replace active-attempt identity according to the lifecycle contract. Completed jobs remain immutable.
5. Never use callback-supplied attempt IDs to set the ledger's authoritative identity. The manifest is evidence of artifact integrity, not proof of current ownership.

## Schema/migration
Add nullable `active_attempt_id TEXT` to intake_jobs. Migration must be idempotent only insofar as the migration runner supports it; SQLite ALTER TABLE duplicate-column behavior must be handled by deployment migration tracking, not blind repeated application.

## Required regression cases
- Current authorized attempt: callback succeeds.
- Wrong attempt ID with otherwise correct job/hash/manifest: rejected, no completion.
- Previous attempt ID after rotation: rejected, no completion.
- Two concurrent callbacks: at most one settlement/event; second is duplicate or conflict.
- Attempt rotation during manifest verification: final conditional settlement fails.
- Completed ledger row: immutable duplicate handling only if the callback is for the completed active attempt; otherwise reject.
- Manifest attempt ID and fencing token mismatch: rejected.
- Callback with valid processor auth but unauthorized attempt: rejected.

## Implementation gates
- Add migration and test fixtures.
- Update dispatch to persist/send identity atomically.
- Update processor contract and artifact paths.
- Update callback validation and conditional SQL.
- Add worker tests with fake D1 and object bucket covering the cases above.
- Run intake tests and processor tests; exact-head CI; owner-gated infrastructure tests later.

Do not deploy or merge on the basis of this design note.
