-- Store a pointer to the immutable, fenced processor attempt manifest.
ALTER TABLE intake_jobs ADD COLUMN manifest_key TEXT;
