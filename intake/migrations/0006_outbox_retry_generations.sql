-- Remove the one-outbox-row-per-job constraint so manual retry can create a new durable intent.
-- Preserve existing outbox records and their retry/claim state.
DROP INDEX IF EXISTS intake_outbox_pending;
DROP INDEX IF EXISTS intake_outbox_claim_expiry;
ALTER TABLE intake_outbox RENAME TO intake_outbox_old;
CREATE TABLE intake_outbox (
  id TEXT PRIMARY KEY,
  job_id TEXT NOT NULL REFERENCES intake_jobs(id),
  payload_json TEXT NOT NULL,
  state TEXT NOT NULL DEFAULT 'pending' CHECK(state IN ('pending','claimed','sent','blocked')),
  attempts INTEGER NOT NULL DEFAULT 0,
  claim_token TEXT,
  claim_until TEXT,
  last_error TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  sent_at TEXT,
  retry_after TEXT
);
INSERT INTO intake_outbox (id,job_id,payload_json,state,attempts,claim_token,claim_until,last_error,created_at,updated_at,sent_at,retry_after)
SELECT id,job_id,payload_json,state,attempts,claim_token,claim_until,last_error,created_at,updated_at,sent_at,retry_after FROM intake_outbox_old;
DROP TABLE intake_outbox_old;
CREATE INDEX IF NOT EXISTS intake_outbox_pending ON intake_outbox(state,created_at);
CREATE INDEX IF NOT EXISTS intake_outbox_claim_expiry ON intake_outbox(state,claim_until);
