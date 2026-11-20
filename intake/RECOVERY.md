# Queue lifecycle and recovery policy

This subsystem is domain-agnostic. Job lifecycle data is the ledger; queue delivery is a transport signal.

## Dispatch failure behavior
- Worker dispatch failures increment the durable `attempts` counter and write a safe event code.
- Up to five recorded dispatch failures remain retryable. The consumer uses queue retry delivery; the queue's configured retry ceiling is also five.
- At the bounded threshold, the ledger moves to `failed_terminal` and the message is acknowledged to prevent infinite retry loops.
- Infrastructure configuration failures are recorded as `blocked_infrastructure` and acknowledged. Owner action is required before manually re-enqueueing.
- Successful processor dispatch moves the ledger to `processing`; authenticated completion callbacks are idempotent for already-completed jobs.
- User-facing error strings do not include upstream exception details, credentials, document text, or provider responses.

## Recovery checklist
1. Review job status and recent events using the authenticated status API.
2. For `blocked_infrastructure`, repair configuration and explicitly re-enqueue after review.
3. For `failed_terminal`, review failure history and source integrity before an owner-authorized retry/new job.
4. Confirm callback token and worker Access policies before replaying any message.
5. Never replay arbitrary callbacks or queue messages from untrusted sources.

## Current limitations
The lifecycle guard is a small policy module and callback/dispatch guard, not a full lease-based claim protocol. Queue delivery can still race; duplicate processor requests are possible. Idempotent processor execution, queue DLQ wiring, manual recovery endpoint, upload scanning/quarantine, retention/deletion and deployment remain owner/infrastructure work.
