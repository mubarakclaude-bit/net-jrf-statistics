# Durable processor callback delivery — implementation contract

**Status: design-only.** This document addresses a confirmed crash/recovery gap in the current processor/intake handoff. It does not implement the outbox, run tests, provision infrastructure, or authorize deployment.

## Confirmed failure window

The processor writes attempt-scoped artifacts and a manifest, then posts a completion callback to intake. When that callback fails, the processor currently returns HTTP 202 with settlement pending. Intake treats any 2xx from the processor dispatch endpoint as successful dispatch and acknowledges its queue message. The processor execution claim can remain `claimed` until lease expiry, and there is no durable callback retry/reconciler. This can strand an intake ledger job in `processing`.

## Required design

1. **Persist callback intent before attempting delivery.** After manifest and artifact integrity evidence have been finalized, write a callback-outbox row to the processor D1 database. Store the callback body, job ID, intake attempt ID, source hash, processor fencing token and claim-token identity. The unique key must prevent duplicate intent for the same execution generation: `(job_id, intake_attempt_id, fencing_token)`.
2. **Keep callback delivery separate from document processing.** A bounded scheduled dispatcher reads due rows, claims each row with a lease and claim-token compare-and-set, and performs callback HTTP outside the D1 transaction. A short inline delivery attempt is optional; the persisted row remains the recovery authority.
3. **Classify responses.** Any accepted 2xx (including an idempotent duplicate response) marks delivery successful. Retry network errors, 408, 429 and 5xx using bounded exponential backoff with jitter and an attempt/time ceiling. Treat permanent contract/authentication failures and stale-attempt/state-conflict 409 responses as blocked or stale-terminal with an explicit audit event; do not spin indefinitely.
4. **Fence delivery and settlement.** Every dispatcher mutation is conditional on the callback-outbox claim token. Processor claim settlement must be conditional on the exact job/source hash/fencing token/claim token and claimed state, not on a mutable row belonging to a newer generation. An expired lease alone must not allow an older generation to settle a newer claim. Intake's active-attempt fence remains authoritative for accepting completion.
5. **Idempotent callback acceptance.** Intake callback retries for a completed job and matching active attempt must remain idempotent. A stale attempt must not complete the ledger. Preserve manifest and artifact hash validation before completion.
6. **Reconciliation and alerting.** Expose bounded diagnostic counts and candidates for pending, expired-lease, exhausted and blocked callback rows; record reason codes and alert on backlog/age. Owner-reviewed recovery must never publish or mutate repository content automatically.

## Suggested D1 table (adapt to migration conventions)

```sql
CREATE TABLE IF NOT EXISTS processor_callback_outbox (
  id TEXT PRIMARY KEY,
  job_id TEXT NOT NULL,
  source_sha256 TEXT NOT NULL,
  intake_attempt_id TEXT NOT NULL,
  fencing_token INTEGER NOT NULL,
  claim_token TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  state TEXT NOT NULL CHECK (state IN ('pending','claimed','delivered','blocked','stale')),
  attempts INTEGER NOT NULL DEFAULT 0,
  next_attempt_at TEXT,
  lease_token TEXT,
  lease_until TEXT,
  last_error_code TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  delivered_at TEXT,
  UNIQUE(job_id, intake_attempt_id, fencing_token)
);
CREATE INDEX IF NOT EXISTS processor_callback_due
  ON processor_callback_outbox(state, next_attempt_at, lease_until);
```

The table/fields are a proposal, not an applied migration. Confirm Cloudflare D1 query/transaction behavior and index choices against the provisioned sandbox before adopting.

## Regression tests required

- Callback succeeds on first delivery and the outbox row is marked delivered.
- Callback fails transiently, scheduled retry succeeds, and the intake job completes without reprocessing the document.
- Retry is bounded; exhaustion blocks and emits an actionable reason/alert.
- Permanent 401/403, malformed contract and stale-attempt 409 are classified without infinite retry.
- Duplicate delivery is idempotent; duplicate callback does not repeat downstream side effects.
- Outbox lease expires and is reclaimed; simultaneous dispatchers cannot own one row.
- A stale dispatcher cannot mutate a row after takeover.
- Processor claim lease expires during callback delivery; exact generation may settle if still current, but a newer claim cannot be settled or overwritten.
- Intake active attempt changes before delivery: stale callback is rejected and marked stale, not completion.
- D1 outage before callback intent persistence fails closed; the completion path must not report recoverable success without a durable callback intent.
- Callback succeeds but processor-side delivery-mark update fails: repeat callback is safe and eventually reconciled.
- D1/R2/queue failure-injection tests against a disposable Cloudflare sandbox.

## Release gate

Implement with migration, dispatcher, tests, runbook and alerting. Run both intake and processor Node test suites, then the full sandbox acceptance flow and failure matrix. This contract alone does not resolve the blocker or constitute test/deployment evidence.
