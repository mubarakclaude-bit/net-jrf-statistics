# Document intake threat model

## Assets
Sources, hashes, extracted text/OCR, mappings, generated outputs, manifests, ledger, secrets and owner controls.

## Trust boundaries
Browser-to-intake; intake-to-queue/D1/R2; processor-to-extractor; processor-to-adapter; callback; operator controls; source content to model stages.

## Threats and controls
| Threat | Required control |
|---|---|
| Unauthorized upload/status/retry | Strong token, owner-only Access, rate limits |
| Malformed/oversized file | Strict limits/signatures, parser limits, quarantine, timeout |
| Prompt injection | Source is untrusted data; never grants tool permissions |
| SSRF | No source-driven arbitrary URLs; outbound allowlist/isolation |
| Secret leakage | Protected runtime, redaction, rotation, no client/repository secrets |
| Stale/concurrent worker | Fencing, attempt paths, authoritative promotion |
| Forged/replayed callback | Authenticated, attempt/fence-bound, idempotent settlement |
| Artifact tampering | Manifest allowlist, digest/size validation, private buckets |
| Duplicate submissions | Explicit dedupe semantics and concurrency-safe uniqueness |
| Availability abuse | Rate limits, bounded retries/backoff, DLQ, alerts |
| Retention/privacy | Configurable retention, deletion propagation, access logging |
| Operator error | Runbook, audited actions, review and sandbox gates |

## Residual risk
D1 and R2 are not transactional. Claims alone cannot protect subsequent unguarded R2 writes. The route currently has incomplete fencing integration; this threat model is not a deployment-safety assertion.
