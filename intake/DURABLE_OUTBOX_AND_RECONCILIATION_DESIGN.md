# Durable dispatch outbox and crash recovery design

This design is the implementation contract for a follow-on change to the intake service. It is deliberately conservative: dispatch and recovery are idempotent and ledger-authoritative; recovery never assumes an object or queue message alone proves success.

## 1. Atomic enqueue intent

Within one D1 transaction (or supported batch with transactional semantics), an enqueue operation must:
1. Conditionally transition the job to queued/dispatchable.
2. Append the audit event.
3. Insert a durable outbox row with stable `outbox_id`, `job_id`, `message_key`, payload version and timestamps.

The outbox row's payload must not contain secrets. The stable message key is derived from job ID and dispatch generation, not a random delivery attempt.

## 2. Outbox schema proposal

```sql
CREATE TABLE IF NOT EXISTS intake_outbox (
  id TEXT PRIMARY KEY,
  job_id TEXT NOT NULL REFERENCES intake_jobs(id),
  generation INTEGER NOT NULL,
  message_key TEXT NOT NULL UNIQUE,
  payload_json TEXT NOT NULL,
  state TEXT NOT NULL CHECK(state IN ('pending','leased','sent','dead')),
  attempts INTEGER NOT NULL DEFAULT 0,
  lease_token TEXT,
  lease_until TEXT,
  next_attempt_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  last_error_code TEXT,
  UNIQUE(job_id,generation)
);
CREATE INDEX IF NOT EXISTS intake_outbox_due
  ON intake_outbox(state,next_attempt_at,created_at);
```

## 3. Dispatcher protocol

- Claim a bounded batch of due rows using a conditional lease token and lease expiry.
- Send messages carrying `job_id`, generation and stable `message_key`.
- If send succeeds, conditionally mark sent using the same lease token. If send fails, conditionally release to pending with exponential backoff and bounded attempts. Exhausted records move to dead with an event and alert.
- A crash after queue send but before marking sent results in repeat send; consumers must tolerate duplicates.
- Never treat sent as proof of consumer completion.

## 4. Consumer idempotency and fencing

- Every queue message is validated and treated as untrusted.
- Consumer validates job state, generation and immutable source digest.
- Consumer claim must be conditional and atomic in the durable claim table. The claim increments a fencing counter and returns a unique token.
- A current claim may renew only while its token/fence matches and the lease has not expired.
- All checkpoints and final ledger transitions require claim-token/fence predicates.
- Attempt artifacts use unique attempt-scoped keys. A stale attempt may write an orphan but cannot promote an authoritative manifest pointer.
- Callback acceptance requires matching the authoritative active attempt, not merely a self-consistent callback manifest.

## 5. Reconciliation algorithm

Run at a bounded cadence and bounded batch size. Reconciliation is read-only discovery followed by conditional repair; no unconditional bulk update.

Candidates:
- pending outbox past next_attempt_at;
- leased outbox with expired lease;
- queued jobs lacking a live dispatch/outbox;
- processing jobs whose claim is expired and whose callback/manifest is not authoritative;
- retryable jobs whose next retry time is due;
- dead outbox or infrastructure-blocked jobs (alert only, no automatic reset).

For each candidate, reread state and verify exact generation, status, claim, lease and immutable source hash. Use a compare-and-set update. Record an event for every repair. Reconciliation is idempotent.

## 6. Retry/backoff policy

Use capped exponential backoff with jitter for transient queue/processor/network failures. Distinguish:
- retryable transient failures;
- infrastructure blocked requiring owner action;
- invalid source or contract failures, terminal;
- cancellation, terminal.

No automatic retry for invalid integrity/hash results, authentication errors or policy violations unless a reviewed policy explicitly classifies them.

## 7. Callback and manifest promotion

Callback payload is not authoritative by itself. Acceptance checks:
- job and source digest match;
- current attempt ID and fencing counter match authoritative claim;
- attempt has not expired/revoked;
- manifest key is inside the job/attempt prefix;
- manifest bytes and all artifact hashes/lengths are validated;
- final state and manifest pointer are updated atomically with claim fencing.

Duplicate accepted callbacks return a stable duplicate result without repeating downstream side effects. Stale callbacks fail safely.

## 8. Orphan artifact cleanup

Cleanup must never delete artifacts based only on age or naming prefix. Before deletion:
- select objects older than conservative grace period;
- reread the job and authoritative manifest pointer;
- verify no current attempt references the object;
- verify object is not a retained audit/evidence artifact;
- use a delete ledger/event and bounded batches.
Cleanup is disabled until retention policy and backups/caches are addressed.

## 9. Rollout gates

1. Unit tests and SQL migration tests.
2. D1 transaction/batch semantics verified for the exact runtime.
3. Simulated send/crash/retry/race tests.
4. Sandbox end-to-end with queue, D1, R2, extractor and callback.
5. Alert and DLQ wiring verified.
6. Owner review of retention, source privacy, security, quotas and cost.
7. Production deployment only after explicit owner authorization.
