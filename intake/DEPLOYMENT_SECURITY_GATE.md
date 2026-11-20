# Intake deployment security gate

This checklist is a release gate for owner-managed Cloudflare provisioning. It is not evidence that any resource exists or has been deployed.

## Identity and perimeter
- [ ] Owner-only Cloudflare Access policy protects portal, API, status, retry and artifact retrieval; test deny-by-default with an unauthenticated client.
- [ ] Service-to-service processor and callback tokens are distinct, high entropy, secret-store managed and rotated.
- [ ] No public bypass route exists around Access or bearer-token checks.
- [ ] Health routes expose only service identity and readiness, not bindings, configuration, source names or secret values.

## Storage and ledger
- [ ] Source and artifact R2 buckets are private; public bucket access is disabled.
- [ ] D1 databases have least-privilege binding scope and backup/export procedures.
- [ ] Lifecycle retention and deletion policy is approved and tested, including deletion of source, artifacts and ledger references.
- [ ] Verify checksum and manifest before downloads; artifact access must be limited to completed jobs and manifest entries.
- [ ] Validate race conditions, duplicate uploads, callback replay and retry behavior against live D1/R2 in a sandbox.

## Processor/extractor controls
- [ ] Extractor is trusted, isolated, patched and bounded for CPU, memory, wall-clock time, response size and concurrency.
- [ ] Uploaded content and extracted text are treated as untrusted data; prompt injection or embedded instructions must not change system configuration or trigger external actions.
- [ ] External adapter outputs are schema-validated and provenance-checked; publication remains human gated.
- [ ] Durable processor fencing is integrated in the execution path before artifact writes or side effects. Current fencing helpers are not yet integrated.
- [ ] Attempt-specific artifact storage and canonical manifest promotion are implemented and tested; deterministic job-scoped overwrites are not sufficient for stale-worker protection.
- [ ] Adapter idempotency and side-effect deduplication behavior are documented and tested.

## Operations
- [ ] Rate limiting, upload abuse controls, scanning/quarantine and cost/concurrency limits are enabled.
- [ ] Queue retry ceiling, DLQ and manual recovery procedure are tested.
- [ ] Stuck-job reconciler uses ledger state and fencing protocol; it never marks completion from artifact presence alone.
- [ ] Alerts cover queue depth, stuck processing, repeated dispatch failures, callback failures, extractor failures and integrity mismatches.
- [ ] Incident response, access review, token rotation and owner recovery runbooks are available.
- [ ] End-to-end sandbox test: upload -> queue -> extractor -> audit -> artifacts -> manifest -> callback -> authenticated download, including failure/retry and stale execution scenarios.

## Authorization boundary
Do not merge, deploy, provision live resources, create credentials, or publish generated content without explicit owner authorization. Until all gates are satisfied, treat the implementation as development-only.
