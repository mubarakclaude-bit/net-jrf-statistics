# Idempotency and transactional outbox specification

Status: architectural requirement; the current queue pipeline does not yet implement a complete transactional outbox.

## Why
D1 ledger and Cloudflare Queue/R2 do not share a transaction. A send can succeed while the sender crashes before recording success; retry can duplicate messages. Queue deliveries are at-least-once.

## Intake-side acceptance
- Use a uniqueness constraint for source hash plus an explicit dedupe policy.
- Create job, event and enqueue-outbox intent in one D1 transaction.
- Upload source to private R2 before referencing it in D1; compensate only when no ledger row references the object.
- Outbox sender claims rows using conditional D1 updates and bounded leases.
- Sender retries; duplicates are expected. Consumer/processor must enforce durable idempotency.

## Processing
- Idempotency key: job ID, source hash, stage and configuration version; capture a configuration hash to avoid silently reusing outputs when trusted config changes.
- Side effects use attempt-specific namespaces and explicit provider idempotency keys where supported.
- Stage checkpoint metadata records artifact digest, input/config hash, attempt/fencing token, timestamps and tool versions.
- Retries reuse only verified checkpoints compatible with the current input/config; otherwise they start a new isolated attempt.

## Testing
Crash before queue send, after send before outbox update, duplicate deliveries, conflicting configuration hash, source hash mismatch, adapter retry and callback replay.
