-- Bounded operator-led recovery candidates. This query is diagnostic only; it does not
-- requeue, terminalize, or mutate jobs. Review each candidate before action.
-- Cloudflare D1 SQL dialect.
SELECT
  id, status, stage, attempts, updated_at,
  error_code, dispatch_lease_until, dispatch_lease_token,
  source_sha256, object_key, source_size, manifest_key
FROM intake_jobs
WHERE
  (status = 'queued' AND dispatch_lease_until IS NOT NULL
     AND dispatch_lease_until < datetime('now'))
  OR (status = 'processing' AND updated_at < datetime('now', '-30 minutes'))
  OR (status = 'failed_retryable' AND attempts < 5)
  OR (status = 'blocked_infrastructure')
ORDER BY updated_at ASC
LIMIT 50;
