# Cloudflare Provisioning and Deployment Runbook

## Owner authorization
Provision private R2 buckets for source and artifacts, D1 intake jobs, processing Queue, and two Workers. Enforce owner-only Cloudflare Access before deployment.

### Intake Worker
- Configure bindings from `intake/wrangler.toml`; replace D1 IDs and queue bindings. Bind the private artifact R2 bucket as `ARTIFACT_BUCKET` in addition to the source bucket.
- For a fresh database, apply `schema.sql`. For an existing database, apply migrations in order (currently `migrations/0001_dispatch_leases.sql`, `migrations/0003_dispatch_outbox.sql`, `migrations/0004_outbox_retry_after.sql`, `migrations/0005_active_attempt_id.sql`, `migrations/0006_outbox_retry_generations.sql`) before deploying the updated Worker.
- Set secret `INTAKE_TOKEN` for portal/API access and `PROCESSOR_CALLBACK_TOKEN` for processor-to-intake completion callbacks.
- Configure `PROCESSOR_URL` and secret `PROCESSOR_TOKEN` on the intake Worker; the token must match the processor's bearer-token secret.
- Configure owner-only Access and review upload limits, scanning and retention.
- Deploy only after security and cost review.

### Processor Worker
- Deploy separately from `intake/processor/`.
- Bind the private source and artifact R2 buckets.
- Provision the processor-claims D1 database, bind it as `PROCESSOR_DB`, and apply `processor/migrations/0001_execution_claims.sql`.
- Set `PROCESSOR_TOKEN` (must match intake's secret), `EXTRACTOR_TOKEN`, and `CALLBACK_TOKEN` (must match intake's `PROCESSOR_CALLBACK_TOKEN`).
- Configure `INTAKE_CALLBACK_URL` to the intake Worker `/internal/processor-result` endpoint and reviewed trusted `EXTRACTOR_URL`.
- Configure optional trusted workspace taxonomy/resource/output variables.
- Callback configuration is required for ledger completion; callback failure/retry recovery is not yet durable and remains a release blocker.

## Deployment commands (not executed)
From intake directory:
```sh
npx wrangler d1 execute net-jrf-intake-jobs --remote --file schema.sql
npx wrangler secret put INTAKE_TOKEN
npx wrangler secret put PROCESSOR_CALLBACK_TOKEN
# Configure PROCESSOR_URL and PROCESSOR_TOKEN in the intake Worker
npx wrangler deploy
```
Processor directory:
```sh
npx wrangler d1 execute net-jrf-processor-claims --remote --file migrations/0001_execution_claims.sql
npx wrangler secret put PROCESSOR_TOKEN
npx wrangler secret put EXTRACTOR_TOKEN
npx wrangler secret put CALLBACK_TOKEN
# Configure INTAKE_CALLBACK_URL and EXTRACTOR_URL
npx wrangler deploy
```

## Smoke checks
1. Health endpoints return service identifiers.
2. Unauthorized requests are rejected.
3. Upload supported file and confirm durable job ID.
4. Duplicate upload is deduplicated.
5. Adapter processing and private artifacts confirmed.
6. Status/event trail, retry and failure handling reviewed.
7. R2 is private and Access gate enforced.
8. Test scanning/quarantine, retention, deletion and cancellation.

## Current boundary
This scaffold is not production-ready or deployed. Extraction requires a provisioned adapter. Coverage and optional output adapter are wired; artifact verification, integrity manifest and a generic bundle builder are implemented in the processor. Authenticated artifact download routes are implemented with manifest/hash/size checks. Draft repository PR automation and end-to-end review orchestration are not yet implemented. Owner Access, scanning/quarantine, retention, sandboxing, monitoring, deployment verification and security review are required before accepting sensitive documents.


## Verification scaffold
The configured output adapter is checked for content bounds and source-segment provenance references. Deterministic reports are stored separately. These checks do not establish semantic accuracy, citation correctness or domain validity; outputs remain review-required. Intake and processor smoke tests are wired to CI, pending CI confirmation for the latest commit. The local/CI suite does not substitute for a live Cloudflare end-to-end test.
