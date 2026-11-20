# Cloudflare Provisioning and Deployment Runbook

## Owner authorization
Create private R2 buckets `net-jrf-private-source` and `net-jrf-private-artifacts`, D1 `net-jrf-intake-jobs`, Queue `net-jrf-source-processing`, and two Workers.

### Intake Worker
- Configure intake bindings from `intake/wrangler.toml`, replace D1 ID.
- Apply `schema.sql`.
- Set secret `INTAKE_TOKEN`.
- Configure owner-only Cloudflare Access for portal and worker routes.
- Deploy only after security/cost review.

### Processor Worker
- Deploy separately from `intake/processor/`.
- Bind source bucket (prefer read-only scoped access) and private artifact bucket.
- Set secrets `PROCESSOR_TOKEN` (matching intake's token), `EXTRACTOR_TOKEN`.
- Configure `EXTRACTOR_URL` only for a reviewed, trusted extraction service.
- Configure intake `PROCESSOR_URL` to the processor endpoint and `PROCESSOR_TOKEN` as a secret.

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
2. Unauthorized processor/intake requests return 401.
3. Upload small valid PDF and confirm 202/job ID.
4. Re-upload same PDF; dedupe returns original job.
5. Processor hash validation and extraction adapter run, artifact lands in private R2.
6. Status/event trail, retry and failure handling reviewed.
7. R2 public access disabled; Access gate enforced.

## Current boundary
The processor currently performs **extraction only** (through a configured adapter) and persists page-indexed provenance. Source audit, Paper 2 syllabus mapping, coverage-gap analysis, authoring, numerical/independent verification, packaging, and draft PR generation are still not implemented. Do not accept sensitive documents until owner access policies, scanning/quarantine, retention, sandboxing, monitoring, and deployment verification are in place.