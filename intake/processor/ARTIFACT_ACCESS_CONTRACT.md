# Private artifact retrieval contract

## Goal
Expose generated artifacts to an authenticated owner without making the R2 bucket public or trusting arbitrary client-supplied object keys.

## Required route shape
A future authenticated processor/owner API may expose a job-scoped artifact route. The route must accept a job identifier and artifact key, but the key is not authorization by itself.

## Mandatory checks
1. Authenticate using the dedicated artifact-access credential. Never reuse the public health route as authorization.
2. Validate the job identifier against the expected format and reject path traversal, control characters, encoded separators, and ambiguous decoding.
3. Load the job manifest from private storage. The manifest is the allowlist of artifacts for the job.
4. Only allow retrieval of keys listed in the manifest; reject arbitrary R2 keys and keys outside the job namespace.
5. Verify the source hash in the manifest matches the job's recorded source hash before returning an artifact.
6. Verify artifact byte length and SHA-256 against the manifest before response delivery. Fail closed if missing, malformed or mismatched.
7. Set safe content type, `Cache-Control: no-store`, and `X-Content-Type-Options: nosniff`. Never inline HTML or executable content; prefer attachment disposition.
8. Do not expose bucket names, raw upstream errors, secrets, or source contents in logs or error responses.
9. Keep downloads bounded and rate-limited; implement explicit audit events for retrieval.
10. Include a deletion/retention policy that removes source, artifacts and related events consistently.

## Expected response behavior
- 401: missing or invalid credentials.
- 400: malformed job/key input.
- 404: job or manifest unavailable, or key not allowlisted (avoid revealing whether arbitrary objects exist).
- 409: manifest/job metadata conflict.
- 422: integrity verification failure.
- 200: verified bytes with safe download headers.

## Implementation status
This document is a contract only. The artifact-access route is not implemented yet. No private artifact retrieval endpoint should be considered available until code, tests and owner security review verify the checks above.
