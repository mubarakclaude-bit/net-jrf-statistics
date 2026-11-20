-- Durable processor execution fencing (Cloudflare D1).
-- A claim is unique per job; monotonically increasing fencing tokens prevent
-- stale executions from checkpointing after ownership has moved.
CREATE TABLE IF NOT EXISTS processor_execution_claims (
  job_id TEXT PRIMARY KEY,
  source_sha256 TEXT NOT NULL,
  fencing_token INTEGER NOT NULL DEFAULT 0,
  claim_token TEXT,
  lease_until TEXT,
  state TEXT NOT NULL DEFAULT 'idle',
  updated_at TEXT NOT NULL,
  CHECK (state IN ('idle','claimed','completed','failed'))
);
CREATE INDEX IF NOT EXISTS processor_claim_lease ON processor_execution_claims(state, lease_until);
