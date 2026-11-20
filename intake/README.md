# Intake Worker (MVP scaffold)

This is a private, owner-authenticated intake API scaffold. It accepts PDFs, stores them in private R2, records durable jobs in D1, and dispatches processing to a Queue. The consumer currently checkpoints a safe placeholder; extraction/authoring/GitHub PR stages are not implemented yet.

## Local/deployment setup

1. Create Cloudflare Worker, R2 bucket, D1 database and Queue.
2. Apply `schema.sql` to D1.
3. Bind `SOURCE_BUCKET`, `JOBS_DB`, `PROCESSING_QUEUE` in `wrangler.toml`.
4. Set `INTAKE_TOKEN` as a Worker secret (do not put in source).
5. Configure `MAX_UPLOAD_BYTES` and allowed origin.
6. Deploy only after reviewing Cloudflare account scope and costs.

## API

- `GET /health`: health check (no secrets exposed).
- `POST /upload`: requires `Authorization: Bearer <INTAKE_TOKEN>`, multipart `file`; PDF only.

No source PDFs are written to Git. Queue processing is idempotent using job ID and stage checkpoints. This scaffold is not yet production-ready: add account/domain authentication, malware scanning, retention, observability, and deployment review before accepting real documents.

See `docs/AUTONOMOUS_SOURCE_INTAKE.md` for full target architecture.
