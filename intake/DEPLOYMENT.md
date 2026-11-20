# Cloudflare Provisioning and Deployment Runbook

## Owner authorization
Provision private R2 buckets for source and artifacts, D1 intake jobs, processing Queue, and two Workers. Enforce owner-only Cloudflare Access before deployment.

### Intake Worker
- Configure bindings from `intake/wrangler.toml`; replace D1 IDs and queue bindings.
- For a fresh database, apply `schema.sql`. For an existing database, apply migrations in order (currently `migrations/0001_dispatch_leases.sql`) before deploying the updated Worker.
- Set secret `INTAKE_TOKEN`.
- Configure owner-only Access and review upload limits, scanning and retention.
- Deploy only after security and cost review.

### Processor Worker
- Deploy separately from `intake/processor/`.
- Bind source storage and private artifact storage.
- Set `PROCESSOR_TOKEN`, `EXTRACTOR_TOKEN`.
- Configure reviewed trusted `EXTRACTOR_URL`.
- Configure optional trusted workspace taxonomy/resource/output variables.
- Set intake `PROCESSOR_URL` and processor token.

## Deployment commands (not executed)
From intake directory:
```sh
npx wrangler d1 execute net-jrf-intake-jobs --remote --file schema.sql
npx wrangler secret put INTAKE_TOKEN
npx wrangler deploy
```
Processor directory:
```sh
npx wrangler secret put PROCESSOR_TOKEN
npx wrangler secret put EXTRACTOR_TOKEN
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
This scaffold is not production-ready or deployed. Extraction requires a provisioned adapter. Coverage and optional output adapter are wired; artifact verification, integrity manifest and a generic bundle builder are implemented in the processor. However, a user-facing artifact export/download route, draft repository PR automation, and end-to-end review orchestration are not yet implemented. Owner Access, scanning/quarantine, retention, sandboxing, monitoring, deployment verification and security review are required before accepting sensitive documents.


## Verification scaffold
The configured output adapter is checked for content bounds and source-segment provenance references. Deterministic reports are stored separately. These checks do not establish semantic accuracy, citation correctness or domain validity; outputs remain review-required. Intake and processor smoke tests are wired to CI, pending an actual successful run.
