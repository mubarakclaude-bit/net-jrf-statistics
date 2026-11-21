-- Bind callbacks to the intake-authorized processor attempt.
ALTER TABLE intake_jobs ADD COLUMN active_attempt_id TEXT;
