# Intake crash-window regression matrix

Tests should exercise every boundary with the ledger, outbox, queue, artifact bucket and worker claims represented by controllable fakes. Integration tests must repeat these scenarios against a disposable runtime.

| Scenario | Expected behavior | Evidence |
|---|---|---|
| Transaction fails before enqueue intent | Neither job transition nor outbox/event is committed | transaction rollback test |
| Dispatcher crashes before send | Lease expires; row becomes eligible for bounded retry | expiry/reclaim test |
| Queue send fails | Outbox returns pending with backoff, or dead after cap; job remains source-safe | failure test |
| Send succeeds, dispatcher crashes before mark sent | Duplicate message may be sent; consumer idempotently handles it | duplicate dispatch test |
| Duplicate queue messages race | Exactly one live claim; others defer/ack according to policy | concurrency test |
| Worker lease expires during extraction | Stale worker cannot checkpoint, settle, or promote manifest | fencing race test |
| Worker writes artifact after lease loss | Artifact remains attempt-scoped orphan; never authoritative | late-write test |
| Current callback while processor dispatch request is pending | callback is accepted only after authoritative claim validation; job not overwritten by dispatch | callback race test |
| Stale callback from prior generation | Rejected; no ledger change | stale-generation test |
| Callback with wrong digest | Rejected; no ledger change | hash mismatch test |
| Manifest/artifact integrity failure | Rejected; ledger remains incomplete; event/alert | tamper test |
| Callback repeats after completion | Idempotent duplicate result; no repeated downstream effects | duplicate callback test |
| Reconciler sees expired lease | Conditional reread and CAS repair; repeat pass is idempotent | reconciler test |
| Retry after source object tampering | Integrity check blocks; no processor dispatch | source preservation test |
| Cancellation races with dispatch | cancellation wins only if CAS conditions match; dispatched worker becomes fenced | cancellation race test |
| Cleanup candidate is still referenced | Delete is skipped | retention/reference test |

## Test construction requirements
- Use deterministic time injection for lease/backoff tests (avoid sleeps where possible).
- Make transaction atomicity explicit; mocks that emulate SQL without rollback are not evidence of transactional behavior.
- Assert audit events and state together.
- Assert source objects are preserved across all failure and retry paths.
- Bound candidate batches and verify no cross-job mutation.
- Include a test for stale worker settlement after the new attempt completes.
