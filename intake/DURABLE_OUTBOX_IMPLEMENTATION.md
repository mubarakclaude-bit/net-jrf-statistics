# Durable outbox implementation slice

Migration 0003 adds an indexed, uniquely job-scoped outbox. `src/outbox.js` provides bounded claims with claim-token fencing and delivery to the Cloudflare Queue producer, recording sent/pending/blocked outcomes. Expired claims can be reclaimed. Malformed payloads are blocked, queue failures return rows to pending, and claim updates are token-conditional.

## Integration boundary (not yet complete)
The intake upload/retry HTTP handlers still dispatch directly. To complete the integration, they must create the ledger and outbox intent in a D1 atomic batch (after source storage is safely established), and a scheduled/triggered dispatcher must call `deliverOutbox`. Queue sends can be duplicated after a send-before-settlement crash; queue consumers therefore remain idempotent. This slice is executable helper code and regression tests, not an assertion that intake is already fully outbox-driven.

## Operator guardrails
No R2/D1/Queue resources are provisioned by this change. Migration must be applied in the configured D1 environment before use. Deployment and owner-controlled configuration remain gated.
