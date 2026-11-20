# Intake Worker

Owner-authenticated upload/status API scaffold. Accepts PDFs, stores them privately in R2, records jobs/events in D1 and dispatches a queue message. It is not production-ready.

## API
- `GET /health`
- `GET /`: upload/status portal (protect with owner-only Cloudflare Access before use)
- `POST /upload`: bearer-token authenticated multipart PDF; 20 MB hard cap, signature check, SHA-256 deduplication.
- `GET /jobs/{id}`: bearer-authenticated job/event status.

## Infrastructure
See `DEPLOYMENT.md`. Bind private R2, D1, Queue. Queue consumer dispatches the full processor contract to `PROCESSOR_URL` with `PROCESSOR_TOKEN`.

## Processor
A new `processor/` worker scaffold accepts jobs, verifies source hash, sends the PDF to the configured extractor adapter and stores page-indexed provenance in a private artifact bucket. It stops after extraction; later content-production stages are not implemented. No source PDFs are committed.

Before deployment: owner identity gate, malware quarantine, restricted extractor, data retention, logging/observability, secret rotation and security review.