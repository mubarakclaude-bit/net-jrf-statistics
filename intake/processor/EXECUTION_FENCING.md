# Durable processor execution fencing

The D1 migration `migrations/0001_execution_claims.sql` creates the durable claim ledger. Bind it as `PROCESSOR_DB` in the processor Worker. Apply the migration before enabling processing.

## Ownership protocol
- Each execution creates a fresh unpredictable claim token.
- A conditional D1 update increments the fencing number and acquires the lease only if the source hash matches, the previous lease has expired/released, and the row is not completed.
- Renew/checkpoint/settle operations are conditional on job, source hash, fencing number, claim token, state and lease expiry.
- A stale claimant receives no successful checkpoint/settlement after a new fencing number is issued.
- This helper does **not** itself make R2 writes or external adapter side effects transactional. Production adapter idempotency keys and attempt-specific object prefixes are still required before claiming end-to-end safety.

## Deployment
1. Create a private D1 database and apply the migration.
2. Add a D1 binding named `PROCESSOR_DB` in Worker deployment configuration.
3. Test lease expiry, competing claims, renewal and stale settlement in a non-production environment.
4. Until the main processing route uses these helpers before artifact writes and adapters, this is a partial implementation only; it is not a completed fencing rollout.
