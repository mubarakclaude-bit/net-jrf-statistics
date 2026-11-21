# Queue lifecycle and recovery policy

This subsystem is domain-agnostic. Job lifecycle data is the ledger; queue delivery is a transport signal.

## Dispatch failure behavior
- Worker dispatch failures increment the durable `attempts` counter and write a safe event code.
- Up to five recorded dispatch failures remain retryable. The consumer uses queue retry delivery; the queue's configured retry ceiling is also five.
- At the bounded threshold, the ledger moves to `failed_terminal` and the message is acknowledged to prevent infinite retry loops.
- Infrastructure configuration failures are recorded as `blocked_infrastructure` and acknowledged. Owner action is required before manually re-enqueueing.
- The ledger is marked `processing` before the synchronous processor call so a fast callback cannot race the state transition. Completion is accepted only from `processing`; duplicate callbacks after completion are acknowledged without a second transition.
- If queue acceptance fails after the durable job row is created, the source object is preserved and the job is moved to `blocked_infrastructure` with a safe recovery code instead of deleting a source still referenced by the ledger.
- User-facing error strings do not include upstream exception details, credentials, document text, or provider responses.

## Recovery checklist
1. Review job status and recent events using the authenticated status API.
2. For `blocked_infrastructure` or `failed_retryable`, repair configuration and use the authenticated `POST /jobs/{id}/retry` route after review. The endpoint rechecks source existence, size and SHA-256 before queueing; if queueing fails, it restores an owner-action blocked state.
3. For `failed_terminal`, review failure history and source integrity before an owner-authorized retry/new job.
4. Confirm callback token and worker Access policies before replaying any message.
5. Never replay arbitrary callbacks or queue messages from untrusted sources.

## Current limitations
The lifecycle guard is a small policy module. Dispatch leases conditionally claim jobs and fence ledger updates; callback validation restricts completion to the current processing state and job-scoped artifact keys. These are race and integrity mitigations, not full processor idempotency: a lease can expire while a processor request is running, and external side effects may still be duplicated. DLQ replay runbook and monitoring, a manual recovery endpoint, upload scanning/quarantine, retention/deletion and deployment remain owner/infrastructure work.

## Reconciliation procedure (operator review; not yet automated)

Run a periodic ledger audit against queue delivery and storage; never mark a job completed solely because an artifact object exists.

| Observed condition | Operator action | Safe disposition |
|---|---|---|
| queued, dispatch lease expired | Inspect event history and queue state; retry dispatch after confirming no active lease | Remain queued or blocked if queue configuration is broken |
| processing, callback absent, lease/expected runtime expired | Verify processor activity, source hash and artifact manifest; check for duplicate execution before retry | Block for review until fencing protocol is implemented |
| completed, manifest missing/unreadable | Verify ledger callback event and artifacts; restrict download access | Treat as integrity incident; do not auto-reopen |
| manifest references missing or hash-mismatched object | Preserve evidence, deny download, report integrity incident | Quarantine job for review |
| retryable failure at attempt limit | Review safe failure codes and configuration | Terminalize or owner-approved new attempt |
| blocked infrastructure | Fix deployment binding/secret/policy and confirm health checks | Owner-approved retry |

The table is operational guidance only. There is no automated reconciler, DLQ consumer or quarantine action currently implemented.
