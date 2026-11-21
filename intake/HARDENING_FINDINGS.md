# Source intake hardening findings and implementation gate

Status: engineering review; not a test report. This document records issues identified by inspecting the intake and processor implementation at PR head and separates fixes that can be made in code from owner-dependent operations.

## Priority 0 — must resolve before deployment

### 1. Attempt-bound callback fencing is implemented but needs race verification
The dispatcher stores a fresh `active_attempt_id` on the intake job and sends it to the processor. The callback compares that ID with the intake ledger, validates manifest job/source/attempt/fencing identity and artifact hashes, and fences the completion update on the active attempt ID. This materially improves stale-callback protection. The processor's numeric fencing counter remains in a separate D1 database, however, and the full cross-service takeover/race protocol has not been proven in a live runtime.

**Required fix:** test stale callbacks after a retry/takeover, old attempts, concurrent callback, callback after terminal state and manifest promotion under lease expiry. Verify that the intake active-attempt ID remains the authoritative promotion guard.

**Acceptance tests:** valid current callback; stale callback after takeover; callback racing a retry; duplicate/concurrent callback; callback after terminal state; callback with mismatched manifest fence/attempt.

### 2. Processor fencing does not make R2 writes atomic
The processor checks its claim immediately before and after R2 writes. R2 writes cannot be included in the D1 fencing transaction. A worker could lose its lease between the pre-write check and the object write. Attempt-specific namespaces reduce collision risk, but a stale attempt can still leave unreferenced artifacts.

**Required fix:** ensure the authoritative manifest pointer is promoted only through a claim-guarded operation; stale attempt objects must remain non-authoritative and be safely garbage-collected only after a conservative grace period and reference check.

**Acceptance tests:** lease takeover during write; stale worker write after takeover; old manifest promotion attempt; cleanup/reference safety.

### 3. Outbox delivery is implemented; reconciliation and runtime proof remain absent
Upload acceptance records job/event/outbox intent in a D1 batch, and a bounded leased dispatcher retries sends with backoff. Queue delivery remains at-least-once. The manual-retry path was found to conflict with the original outbox table's unique-per-job constraint; migration 0006 removes that constraint so each retry can append a fresh dispatch intent. This fix is pending CI and migration/runtime verification. A periodic reconciler remains unimplemented.

**Required fix:** verify D1 batch/migration semantics, implement a bounded reconciler for expired outbox/job/processor leases, and use conditional repairs with event records.

**Acceptance tests:** crash before send; send then crash before mark-sent; repeated send; concurrent dispatcher; exhausted retry including expired claims; source preservation; duplicate consumer delivery; repeated manual retries.

### 4. Callback failure can strand processing jobs
The processor returns HTTP 202 when the callback is missing, rejected or unavailable, and the intake queue consumer treats any successful HTTP response as a completed dispatch and acknowledges the queue message. There is no durable callback retry or job reconciler to settle that job later. This can leave the intake ledger in `processing` without an authoritative completion pointer.

**Required fix:** persist callback-delivery intent and retry it durably, or implement a ledger-authoritative reconciler with fenced recovery. A 202 response must not silently be treated as completed job dispatch unless callback recovery is guaranteed.

**Acceptance tests:** missing callback configuration; callback timeout; response lost after callback completion; callback rejection; eventual settlement; recovery after processor lease expiry.

## Priority 1 — before sensitive-source acceptance

- **Upload scanning/quarantine:** implement scanning and quarantine before accepted/dispatch; MIME/signature checks are not malware scanning. ZIP-based Office files require bounded decompression and macro/embedded-object controls.
- **Extractor isolation:** enforce provider-side CPU, memory, response, time, concurrency and outbound-network restrictions; verify response bounds and page/text limits.
- **Portal access:** Access gate, CSRF/origin considerations for token-bearing UI, abuse/rate limits and token rotation.
- **Deletion/retention:** executable deletion propagation and retention rules; the current cancellation/retention spec is policy-only.
- **DLQ and alerts:** actual queue dead-letter routing, alarm wiring and runbooks, not merely proposed metrics.
- **Output semantics:** verification currently establishes bounded structure and segment references, not correctness or citation truth. Keep review-required.

## Priority 2 — quality and operational maturity

- Verify idempotency guarantees of external adapters with provider-specific contracts.
- Reconcile completion from manifest evidence only through the authoritative claim and ledger transition, never artifact presence alone.
- Add integration tests against a disposable Cloudflare sandbox with real D1, R2, Queue and worker bindings.
- Add independent security review and cost controls.
- Implement artifact access revocation and retention expiry, including caches and backups.

## Evidence boundary
The code review identified the risks above. This is not a CI result, local test run, deployment smoke test or security certification. CI status for the current PR head must be independently confirmed. Cloudflare provisioning, secrets, live access policies, sandbox tests and deployment remain owner-authorized activities.
