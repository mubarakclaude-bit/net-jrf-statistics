# End-to-end sandbox acceptance plan

Execute only in an isolated sandbox with non-sensitive test documents and test credentials. Not executed yet.

## Happy path
1. Upload small PDF/TXT; confirm ledger, private source and hash.
2. Confirm queue consumed and processor claim acquired.
3. Extract and validate bounded pages schema.
4. Produce audit and optional mapping/coverage/production stages.
5. Write immutable attempt artifacts and manifest.
6. Callback verifies manifest/hashes and settles ledger.
7. Authenticated retrieval verifies digest.
8. Confirm unauthenticated access is denied.

## Failure injection
- Wrong token, malformed JSON, invalid UUID/hash/key.
- Oversize, invalid signature, unsupported MIME, extractor timeout/error/invalid JSON.
- Invalid pages, excessive text/pages, invalid confidence or duplicates.
- Adapter malformed payload, invalid provenance, output limits.
- Callback wrong token/replay/mismatch; manifest missing; artifact altered.
- Concurrent deliveries and paused stale worker resumed after takeover.
- D1/R2 outage, queue send failure, callback timeout.
- Retry cap, DLQ, manual retry after recovery.
- Cancellation in queued/processing state.
- Traversal/retrieval allowlist and digest mismatch.
- Retention/deletion exercise.

## Acceptance evidence
Record sandbox run IDs, environment, source hash, job/event IDs, redacted logs and results. Any security-test failure blocks deployment.
