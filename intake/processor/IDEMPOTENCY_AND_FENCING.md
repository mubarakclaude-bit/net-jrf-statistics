# Processor Idempotency and Execution Fencing

## Current risk
The processor endpoint is stateless at the HTTP layer. Artifact keys are job-scoped and overwritten deterministically, but concurrent requests for the same job can invoke the extractor and optional production adapter more than once. Deterministic artifact names alone do not prevent duplicate external side effects.

## Required invariant
A job must have one authoritative execution attempt at a time, and a stale attempt must not be able to publish a completion result or callback after ownership has been superseded.

## Recommended claim protocol
1. Intake ledger assigns a monotonically increasing attempt/fencing number and a short execution lease before queue dispatch.
2. Queue payload includes job ID, source hash, attempt number, and lease token; secrets never appear in payloads.
3. Processor validates that the payload and source namespace are correct, then claims execution in a durable store using a conditional update that succeeds only if the stored attempt/token matches and the claim is unexpired or reclaimable.
4. Processor renews its lease during long extraction/production steps. Renewal must be conditional on the same attempt number and token.
5. Every durable checkpoint and completion callback carries the fencing number/token. Intake accepts only the current number/token, in the expected lifecycle state, with verified artifacts.
6. A stale execution may write temporary artifacts under an attempt-specific prefix but may not overwrite canonical artifacts or mark the job completed.
7. After verification, a fenced promotion step atomically selects the canonical manifest for the current attempt. If the store cannot provide conditional promotion, do not claim the protocol is safe; use a transactional D1 ledger as the authority.

## Artifact layout proposal
- Temporary: `jobs/<job_id>/attempts/<attempt>/...`
- Canonical manifest: `jobs/<job_id>/manifest.json`
- Manifest includes attempt/fencing number, source hash, and all artifact hashes/sizes.
- Download endpoints only expose artifacts referenced by the verified canonical manifest.

## Retry and idempotency
- Retries reuse job ID but increment attempt number.
- Adapter side-effect idempotency key: `<job_id>:<attempt>:<requested_output>`; adapters should additionally support job-level deduplication when side effects are not intended to repeat.
- No retry may bypass source-hash verification or review gating.
- Reconciliation should inspect lease expiry and state, not assume queue delivery is exactly once.

## Not yet implemented
This is a design contract, not a claim of implementation. Processor-side durable claims, lease renewal, attempt-scoped storage, canonical manifest promotion, and fenced external adapter calls remain pending.
