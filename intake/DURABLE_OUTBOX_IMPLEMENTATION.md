# Durable outbox implementation

Migration 0003 adds an indexed, uniquely job-scoped outbox. Fresh database setup also includes the table in `schema.sql`. `src/outbox.js` provides bounded claims with claim-token fencing and delivery to the Cloudflare Queue producer, recording sent/pending/blocked outcomes. Expired claims can be reclaimed. Malformed payloads are blocked, queue failures return rows to pending, and claim updates are token-conditional.

## Producer and dispatcher integration
Upload acceptance now stores the source object before creating the job ledger, event, and durable dispatch intent in a D1 batch. The job is created as queued; the queue send is not performed in the HTTP handler. Retry verifies source integrity and records a retry event/outbox intent before returning accepted. A scheduled Worker handler runs every two minutes and delivers up to 25 rows per tick. Missing D1/Queue bindings fail closed.

## Crash-window and idempotency boundary
Queue sends can be duplicated after a send-before-settlement crash. Consumers must remain idempotent and processor execution must be fenced. The current producer integration has not yet been verified against a live D1/Queue runtime, and callback authority remains a separate hardening task.

## Operator guardrails
No R2/D1/Queue resources are provisioned by this change. Migration must be applied in the configured D1 environment before use. Deployment and owner-controlled configuration remain gated.
