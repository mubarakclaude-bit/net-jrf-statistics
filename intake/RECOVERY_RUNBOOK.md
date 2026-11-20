# Intake recovery runbook

This is an operator checklist, not autonomous repair authorization.

## Triage
1. Authenticate through owner-only access; inspect job state and event history.
2. Verify source exists and matches recorded SHA-256 and byte length.
3. Check queue/dispatch lease, processor/extractor/callback configuration, D1 and R2.
4. Inspect manifest and artifact digests/sizes. Artifact existence alone does not prove completion.
5. Confirm active claim/lease and attempt before retrying. Avoid duplicate workers while a lease is live.

## Disposition
- Retryable infrastructure failure: retry only after integrity and readiness checks.
- Stale processing: elapsed time alone is insufficient; verify lease expiry, queue, callback and active attempt. Record operator event.
- Integrity mismatch: preserve evidence, quarantine and do not retry automatically.
- Validation failure: route to review.
- Terminal state: owner decision with documented reason.

## Evidence
Record job ID, source hash, state, timeline, attempt/fencing token, incident, checks, action, operator, timestamp and resulting state.

## Prohibited
No status edits without audit events; don't delete original sources to force retry; don't trust unverified callbacks; don't mark completed merely because files exist.
