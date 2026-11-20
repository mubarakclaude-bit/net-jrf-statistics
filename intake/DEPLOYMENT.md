# Cloudflare Provisioning and Deployment Runbook

## Required one-time owner-side authorization

This project cannot provision resources or access account secrets from repository code. Provision the following in Cloudflare:

- Worker: `net-jrf-source-intake`
- R2 bucket: `net-jrf-private-source` (private; no public access)
- D1 database: `net-jrf-intake-jobs`
- Queue: `net-jrf-source-processing`
- Worker secrets: `INTAKE_TOKEN` (long random secret), optional `MAX_UPLOAD_BYTES`
- Bind the bucket, database and queue using `intake/wrangler.toml`; replace the placeholder D1 ID.
- Apply `intake/schema.sql` to D1.

## Deployment commands

From the intake directory, after installing Wrangler and authorizing the Cloudflare account:

```sh
npx wrangler d1 execute net-jrf-intake-jobs --remote --file schema.sql
npx wrangler secret put INTAKE_TOKEN
npx wrangler deploy
```

These are instructions only; not executed here.

## Smoke checks

1. `GET /health` returns `{"ok":true,"service":"intake"}`.
2. Open the Worker root page (`/`) and upload a small valid PDF.
3. `POST /upload` should return HTTP 202 and a job ID.
4. Upload the same PDF again: should return the same job ID with duplicate=true.
5. `GET /jobs/<id>` with bearer token returns status and event trail.
6. Unauthorized requests return 401.
7. Invalid file signatures and oversized files are rejected.
8. Confirm R2 bucket is not public; inspect D1 records and Queue delivery.

## Current functional limitation

The queue consumer deliberately marks the job as `needs_worker` with `worker_scaffold`. It is not yet connected to PDF extraction/OCR, syllabus mapping, question auditing, solution generation, independent review, packaging, or GitHub PR creation. These stages require a processing runtime and configured AI/provider integration, followed by tests and deployment.

## Security and retention before accepting confidential material

- Protect the portal with a stronger user identity gate (Cloudflare Access or equivalent), not just a shared bearer token.
- Restrict Access policies to the owner.
- Add malware scanning and OCR/parser sandboxing.
- Add retention/deletion policy and backup policy.
- Avoid logging source content, tokens or full PDF text.
- Rotate secrets and review resource cost/limits.
