# Reconciliation implementation specification

Status: design contract; not implemented or live-tested.

## Scope
A scheduled reconciler examines the durable intake ledger, queue delivery signals, processor claim ledger and verified immutable attempt manifests. It must not infer completion from artifacts alone.

## Required candidate query
Use bounded batches, indexed status/updated_at/lease fields. Candidates: expired dispatch lease, processing timeout, retryable job without queue signal, explicit owner-selected blocked job. Exclude completed, cancelled and terminal states.

## Claim and decision
- Acquire a durable conditional reconciler lease with a unique token and expiry.
- Append an audit event identifying candidate, reason and decision.
- Verify source hash/size, queue state, callback events, processor claim lease and manifest/artifact integrity.
- A verified attempt can be adopted only through an authoritative fenced ledger transition; don't replay production adapters.
- If no valid completed attempt exists, retry only after timeout, budget and idempotency checks.
- If uncertainty remains, transition to an owner-review state rather than guessing.
- Queue enqueue must be idempotent, with a durable enqueue nonce/outbox row. Reconciler must not send then blindly retry after a crash.
- Bound batch size, concurrency, time budget and retry count; emit metrics and redact logs.

## Future D1 design
Use a dedicated reconciliation claim table and enqueue-outbox table. Outbox records include job_id, source hash, nonce, intended stage, status, created_at and sent_at. Sender claims unsent rows, dispatches and conditionally records success. Duplicate queue delivery remains possible; processors must enforce claims and idempotency.

## Safety tests
Concurrent reconciler claims; expired claim takeover; duplicate enqueue; crash before send; crash after send but before marking; completed callback arriving during reconciliation; active processor lease; stale attempt manifest; malformed manifest; retry-budget exhaustion.
