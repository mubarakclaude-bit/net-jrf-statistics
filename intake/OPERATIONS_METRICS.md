# Intake operational metrics and alerts

Status: proposed; not wired to a metrics backend.

## Counters and gauges
- accepted/upload bytes, rejected by reason, deduplicated submissions
- queue depth, oldest message age, dispatch retries
- jobs by lifecycle state and age, active dispatch/processor/reconciler leases
- extraction/adapter durations, failures and response-size rejections
- callback latency/rejections/replays
- artifact integrity failures, manifest failures and retrieval-denials
- retry/terminal/DLQ volume, cancellation and deletion outcomes

## Alert conditions
- queue age or processing age above SLA
- repeated dispatch/extractor/callback failure spikes
- blocked-infrastructure accumulation
- terminal failure spike or DLQ growth
- fencing/claim conflict spike
- manifest integrity mismatch or unauthorized access anomaly
- retention/deletion failures

## Logging
Structured, correlation by job ID, attempt/fencing token and stage; never log bearer tokens, full source text, document contents, or unredacted provider responses. Keep sensitive identifiers minimized.
