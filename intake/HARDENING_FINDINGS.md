# Source intake hardening findings and implementation gate

Status: engineering review; not a test report. This document records issues identified by inspecting the intake and processor implementation at PR head and separates fixes that can be made in code from owner-dependent operations.

## Priority 0 — must resolve before deployment

### 1. Intake callback is not fenced against processor claim ownership
The callback validates the manifest and its artifacts, then updates the intake job with a conditional transition from processing to completed. It validates manifest identity (job, source hash, attempt ID and fencing token against the submitted callback/manifest) but intake has no durable current-attempt claim record against which it can compare the fencing token. The processor's claim database is separate. A callback from a superseded attempt therefore needs an explicit cross-service authoritative attempt/claim mechanism before it can be considered protected from stale completion.

**Required fix:** persist an authoritative active attempt/fencing record in the intake ledger or establish a signed, verified attempt-claim protocol. Callback acceptance must compare the callback's attempt and fencing token with the authoritative active claim. State transition and claim check must be atomic.

**Acceptance tests:** stale callback after takeover; callbacks from old attempts; callback racing a retry; concurrent callback; valid current callback; callback after terminal state.

### 2. Processor fencing does not make R2 writes atomic
The processor checks its claim immediately before and after R2 writes. R2 writes cannot be included in the D1 fencing transaction. A worker could lose its lease between the pre-write check and the object write. Attempt-specific namespaces reduce collision risk, but a stale attempt can still leave unreferenced artifacts.

**Required fix:** ensure the authoritative manifest pointer is promoted only through a claim-guarded operation; stale attempt objects must remain non-authoritative and be safely garbage-collected only after a conservative grace period and reference check.

**Acceptance tests:** lease takeover during write; stale worker write after takeover; old manifest promotion attempt; cleanup/reference safety.

### 3. Transactional outbox and queue reconciliation are absent
Upload and manual retry currently make ledger state changes and send queue messages across separate systems. Failure handling blocks jobs in some cases, but a transactional outbox and periodic reconciler are not implemented. Queue delivery is at-least-once.

**Required fix:** D1 transaction writes job/event/outbox intent. A bounded leased outbox dispatcher sends with stable message keys. Consumer claims use authoritative fencing and idempotency. A periodic reconciler repairs stale outbox and job records with conditional transitions.

**Acceptance tests:** crash before send; send then crash before mark-sent; repeated send; concurrent dispatcher; exhausted retry; source preservation; duplicate consumer delivery.

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
