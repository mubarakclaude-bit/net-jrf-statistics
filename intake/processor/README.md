# Generic Processor Service

A document-agnostic processing Worker for educational and reference material, including question banks, textbooks, notes, articles, exams, manuals, slide decks, worksheets and mixed documents.

It accepts authenticated jobs and retrieves source files from private storage. Extraction adapters may be configured for supported formats. A generic structure/source audit can identify candidate questions, answers, concepts, explanations, objectives and other content while retaining provenance. Optional workspace configuration may provide taxonomies, knowledge maps, resource indexes, output types or integrations; none are hard-coded into the processor.

## Bindings/secrets
- `SOURCE_BUCKET`: private source storage
- `ARTIFACT_BUCKET`: private processed-artifact storage
- `PROCESSOR_TOKEN`: authentication
- `EXTRACTOR_URL` and `EXTRACTOR_TOKEN`: trusted extraction adapter
- Optional `TAXONOMY_JSON`, `RESOURCE_INDEX_JSON`, `WORKSPACE_CONFIG_JSON`: configuration inputs (must not be upload-controlled)

## Adapter contract
POST JSON containing job ID, source hash, name and file bytes to a configured trusted adapter. Adapter output is page/section/chunk indexed. Limit request/response sizes and validate returned structure. Use adapters for formats beyond PDF when configured.

Analysis outputs are candidate findings only, not guaranteed ground truth. Downstream outputs (lesson, summary, questions, etc.) are configurable and not hard-coded. Authoring, verification and packaging integrations must be separately implemented and validated before production.
