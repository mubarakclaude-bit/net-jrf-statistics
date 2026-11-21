CREATE TABLE IF NOT EXISTS intake_jobs (
  id TEXT PRIMARY KEY,
  source_name TEXT NOT NULL,
  source_sha256 TEXT NOT NULL UNIQUE,
  object_key TEXT NOT NULL UNIQUE,
  source_size INTEGER NOT NULL,
  mime_type TEXT NOT NULL DEFAULT 'application/octet-stream',
  status TEXT NOT NULL,
  stage TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  error_code TEXT,
  error_message TEXT,
  dispatch_lease_until TEXT,
  dispatch_lease_token TEXT,
  manifest_key TEXT
);
CREATE INDEX IF NOT EXISTS intake_jobs_status_created ON intake_jobs(status, created_at);
CREATE TABLE IF NOT EXISTS intake_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_id TEXT NOT NULL REFERENCES intake_jobs(id),
  event TEXT NOT NULL,
  stage TEXT NOT NULL,
  details_json TEXT,
  created_at TEXT NOT NULL
);\nCREATE TABLE IF NOT EXISTS intake_outbox (
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
  sent_at TEXT,\n  retry_after TEXT,
  UNIQUE(job_id)
);
CREATE INDEX IF NOT EXISTS intake_outbox_pending ON intake_outbox(state,created_at);
CREATE INDEX IF NOT EXISTS intake_outbox_claim_expiry ON intake_outbox(state,claim_until);
