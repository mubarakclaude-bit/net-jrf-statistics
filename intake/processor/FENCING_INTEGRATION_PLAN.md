# Fencing integration plan (implementation gate)

## Required protocol for src/index.js
The worker must not claim production-safe fencing until these items are implemented and failure-injection tested. D1 claims are authority; R2 and HTTP side effects are not transactional.

1. Claim before side effects: validate contract and bindings; generate an unpredictable claim token; claim via PROCESSOR_DB. If no claim, return busy. Do not write outputs or invoke adapters before claiming.
2. Attempt namespace: every extraction, audit, taxonomy, coverage, production and verification artifact uses jobs/<job>/attempts/<fence>-<attempt>/; never overwrite other attempts.
3. Checkpoint stages: fence before and after external calls and before artifact batches. Renew leases around slow calls. Lost lease means abandon the attempt.
4. Manifest promotion: create immutable attempt manifests. Mutable canonical promotion requires an authoritative conditional D1 active-attempt pointer protocol; a fence-check followed by an unguarded R2 write is not safe because D1 and R2 are not transactional.
5. Callback: include attempt ID, fencing token and manifest digest. Callback validates current attempt against D1 authority, verifies artifacts and settles once. Stale attempts cannot settle or publish.
6. Settlement: retry callback delivery idempotently; don't treat callback rejection as success.
7. Cleanup: garbage-collect inactive attempts only after a grace period, retaining audit evidence.

## Deployment gate
Verify PROCESSOR_DB binding/migration, cross-system promotion protocol, stale-worker failure tests, replay-safe attempt-bound callback, concurrency/outage tests. Do not deploy before passing.
