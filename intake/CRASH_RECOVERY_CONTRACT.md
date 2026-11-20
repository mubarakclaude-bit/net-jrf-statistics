# Crash recovery and stuck-job reconciliation contract

## Purpose
Queue delivery and processor calls are not a complete durable recovery mechanism. A periodic reconciler must use the D1 job ledger to detect abandoned states and safely prepare owner-reviewed recovery.

## Candidate detection
- A job in `processing` with an update timestamp older than a configurable processing timeout.
- A job with a dispatch lease whose expiry has elapsed.
- A job in `failed_retryable` with retry budget remaining but no active queue signal.
- A job in `blocked_infrastructure` after owner repair, but only when explicitly selected for requeue.
- A job with artifacts present but no accepted callback, identified by a private manifest and verified hashes.

## Reconciler rules
1. Run with a dedicated, least-privilege identity and bounded batch size.
2. Acquire a reconciliation claim using a conditional D1 update; concurrent reconcilers must not process the same row.
3. Record a reconciliation event with reason, prior state, selected action and claim identifier.
4. Never blindly replay an expired processing job. Inspect whether a completion callback or verified artifact manifest exists first.
5. If a valid completed manifest exists, validate it and reconcile ledger state using a guarded transition; do not repeat production side effects.
6. If no completion evidence exists, mark the job as recovery-needed or retryable only after the configured timeout and attempt policy. Queue replay must use a durable idempotency key.
7. Preserve bounded retries and terminalization. Repeated timeout failures must not loop indefinitely.
8. If required credentials, adapter configuration, or owner policy is missing, record `blocked_infrastructure` and require owner action.
9. Ensure event writes and state transitions are conditional on claim ownership and current state.
10. Never auto-publish, auto-merge, or create external repository writes as part of reconciliation.

## Suggested states
Use existing lifecycle states where possible; avoid adding a state until transitions, schema, tests and monitoring are coordinated. A `recovery_needed` state may be introduced only as a deliberate migration.

## Test requirements before implementation is considered ready
- concurrent reconciler claim conflict
- expired lease and still-running processor conflict
- completion callback received after reconciliation claim
- manifest exists with matching hashes
- manifest missing or corrupted
- retry ceiling and terminalization
- blocked infrastructure remains owner-actionable
- replay is idempotent and external side effects are deduplicated

## Status
Contract only. Automated reconciliation, idempotent processor-side claims, lease renewal and side-effect deduplication are not implemented. Cloud infrastructure and deployment remain owner-controlled.
