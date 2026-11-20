# Cancellation, retention and deletion specification

Status: policy design only; routes and cloud lifecycle rules are not implemented.

## Cancellation semantics
- Cancellation is owner-authenticated and conditional on current state.
- Accepted/queued jobs: prevent dispatch where possible, acknowledge queue messages for cancelled jobs and record audit events.
- Processing jobs: cancellation signal is persisted. Processor checks it at stage boundaries and stops further external side effects. No worker may convert cancelled to completed.
- External adapters may not support cancellation; isolate them, impose deadlines and mark outcome uncertain for operator review.
- Preserve immutable audit evidence of the cancellation and completed work until retention policy permits deletion.

## Data classes
Source file, extracted text, derived artifacts, manifests, event logs, identifiers and provider metadata. Treat all as potentially sensitive.

## Retention controls
- Owner-approved retention period and explicit configuration.
- Deletion propagation across source R2, artifact R2, derived caches, provider systems where contract permits, D1 and backup lifecycle.
- Legal/operational retention exception must be explicit and logged.
- Deletion is idempotent and has a tombstone/event trail. Avoid storing the source or text in deletion logs.
- Do not delete active attempts or sources during retry/reconciliation.

## Acceptance tests
Cancel before dispatch, during processing, callback racing cancellation, repeated cancellation, deletion of missing objects, partial deletion failure, retention expiration and backup policy review.
