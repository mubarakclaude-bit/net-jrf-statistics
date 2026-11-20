-- Apply to an existing intake_jobs table before deploying lease-aware intake worker.
ALTER TABLE intake_jobs ADD COLUMN dispatch_lease_until TEXT;
ALTER TABLE intake_jobs ADD COLUMN dispatch_lease_token TEXT;
