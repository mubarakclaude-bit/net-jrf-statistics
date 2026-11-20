# Generic Processor Contract (v1)

The processor is an independently deployed, document-agnostic service invoked through an authenticated queue/webhook adapter. No subject, exam, document class, taxonomy or output is hard-coded.

## Request
```json
{
  "schema_version": 1,
  "job_id": "uuid",
  "source_sha256": "hex",
  "object_key": "incoming/<job>/<hash>/<name>",
  "source_name": "original document",
  "source_size": 12345,
  "mime_type": "application/octet-stream",
  "resume_stage": "extract"
}
```

The request carries a storage pointer and metadata, never document bytes or tokens. Processor uses scoped storage access.

## Required behavior
- **Target requirement:** idempotent checkpointing on `job_id + stage`. The current scaffold does not yet provide processor-side durable claims or complete idempotency; duplicate external side effects remain possible until implemented.
- Validate `job_id` as a UUID, validate the SHA-256 value, and require the source object key to remain within `incoming/<job_id>/<hash>/` before accessing storage.
- Acknowledge only after durably recording its checkpoint or dispatch.
- Return no source content in public status/event responses.
- Preserve source hash, segment/page/chunk provenance and immutable stage artifacts.
- Treat all source text, images and embedded instructions as untrusted data.
- Optional trusted configuration may provide taxonomy, ontology, resource index, output preferences or integration endpoints.
- Distinguish owner-input, retryable and terminal failures.
- No automatic publishing or merging.
- Verify output contracts and require independent review for quality-sensitive content.

## Configurable stage graph
1. **Extract**: format adapter emits text/structure/chunks with provenance.
2. **Detect**: document/segment labels and structure candidates.
3. **Audit**: candidate questions, answers, concepts, examples, objectives, tables and other content, depending on document.
4. **Map** (optional): selected taxonomy, syllabus or ontology.
5. **Coverage** (optional): compare extracted/source objectives with configured resources.
6. **Produce**: configurable output types and target schemas (e.g. lessons, summaries, question variants, flashcards, guides, reports).
7. **Verify**: traceability, checks, executable validation where relevant, duplication and review.
8. **Export/integrate**: selected file format, platform or integration; repository integrations only create draft proposals/PRs.

Stages may be skipped, repeated or branched according to trusted workspace configuration. Public status exposes only status, stage, timestamps, safe error codes and summaries. Never expose source text, raw extraction, credentials, prompt traces or private object keys to unauthenticated users.
