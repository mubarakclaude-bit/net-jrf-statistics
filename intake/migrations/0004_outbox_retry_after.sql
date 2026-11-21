-- Add scheduled retry timestamp to outbox for exponential backoff.
ALTER TABLE intake_outbox ADD COLUMN retry_after TEXT;
