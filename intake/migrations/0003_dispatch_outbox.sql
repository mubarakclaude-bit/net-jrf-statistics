-- Durable queue intent. Producers must create the job and outbox row atomically in D1.
CREATE TABLE IF NOT EXISTS intake_outbox (
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
  retry_after TEXT,
  UNIQUE(job_id)
);
CREATE INDEX IF NOT EXISTS intake_outbox_pending ON intake_outbox(state,created_at);
CREATE INDEX IF NOT EXISTS intake_outbox_claim_expiry ON intake_outbox(state,claim_until);
