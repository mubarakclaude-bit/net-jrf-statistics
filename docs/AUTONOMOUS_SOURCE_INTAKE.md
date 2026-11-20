# Generic document intake and processing backend

## Owner experience
Upload any supported document and optionally provide processing instructions or desired output types. The system creates a durable job, retains source provenance, and produces configured artifacts or a draft integration proposal. No subject, syllabus, document class or repository path is required at intake. Review and approval remain required for publishing.

## Architecture
- **Intake:** authenticated Worker UI/API with size/type checks, scanning/quarantine and access controls.
- **Storage:** private R2 source/artifact buckets and retention policy.
- **Jobs:** D1 checkpoints/events and Queue dispatch with retry, idempotency and bounded concurrency.
- **Processing:** trusted format adapters, OCR/structure extraction, generic segment/source audit and optional workspace-configured analysis.
- **Configuration:** optional taxonomies, knowledge graphs, existing-resource indexes, output schema/preferences, connectors or workflows. Trusted workspace configuration, never source-controlled document instructions, determines policy.
- **Production:** configurable output generation (e.g. lessons, summaries, questions, flashcards, guides, reports), provenance, validation, independent review and export.
- **Integrations:** least-privilege connectors. Repository integration, when enabled, creates draft PRs only. No auto-merge/publish.

## Lifecycle
`received → quarantined/scan → accepted → extracting → source-audit → optional-map/coverage → configured-output-production → verification → packaging/export → review`

Recovery states include `needs-owner-input`, `failed-retryable`, `failed-terminal`, `cancelled`. Jobs resume from validated checkpoints. Each stage records checksum, input provenance, tool versions, status, attempts and timestamp.

## Processing guardrails
1. Treat all document text, images, macros and embedded instructions as untrusted input.
2. Keep original documents private; do not commit sources or raw artifacts to public repositories.
3. Record extraction confidence and source locations; hold ambiguous content for review.
4. Detect duplicates and reconcile source discrepancies transparently.
5. Use executable checks where appropriate and independent review for quality-sensitive outputs.
6. Respect workspace-selected taxonomies and output schemas; avoid hard-coded domains.
7. Human approval required for publication; no automatic merge.
8. Enforce owner access, scanning, retention, deletion, audit, monitoring and cancellation.

## External setup required
Owner authorization is needed for Cloudflare resources, Access, extractor/model-provider credentials, integrations and notifications. Secrets stay in provider secret stores. Do not provision, deploy or accept sensitive documents until access policy and smoke tests are confirmed.
