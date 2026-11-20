# Recovery review procedure (diagnostic SQL)

This procedure is **manual and read-only**. It is not an autonomous reconciler.

1. Use the authenticated status API to inspect job events.
2. Verify the source object's size and SHA-256 against the ledger.
3. Run `recovery/reconcile_candidates.sql` against D1 to list aged or blocked jobs.
4. For queued/processing candidates, inspect queue activity and processor claims before taking action. A stale timestamp alone is not proof the worker stopped.
5. For `failed_retryable` or `blocked_infrastructure`, use the authenticated retry endpoint only after repairing the underlying issue and confirming source integrity.
6. If a completion manifest is found, independently verify its attempt identity and hashes. Never mark completion solely based on artifact existence.
7. Escalate integrity conflicts or uncertain external side effects; do not replay.

The query is bounded to 50 records and does not modify any row. Its timeout is a conservative diagnostic default, not a proof of failure. Current automated reconciliation remains unimplemented.
