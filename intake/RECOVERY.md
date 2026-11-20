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
2. For `blocked_infrastructure`, repair configuration and explicitly re-enqueue after review.
3. For `failed_terminal`, review failure history and source integrity before an owner-authorized retry/new job.
4. Confirm callback token and worker Access policies before replaying any message.
5. Never replay arbitrary callbacks or queue messages from untrusted sources.

## Current limitations
The lifecycle guard is a small policy module. Dispatch leases conditionally claim jobs and fence ledger updates; callback validation restricts completion to the current processing state and job-scoped artifact keys. These are race and integrity mitigations, not full processor idempotency: a lease can expire while a processor request is running, and external side effects may still be duplicated. DLQ wiring, a manual recovery endpoint, upload scanning/quarantine, retention/deletion and deployment remain owner/infrastructure work.
