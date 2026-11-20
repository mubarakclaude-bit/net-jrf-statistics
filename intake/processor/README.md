# Processor Service (scaffold)

A separately deployed Cloudflare Worker that receives authenticated intake jobs, retrieves the private PDF, and performs extraction via a configured, authenticated extraction adapter. It does not generate lessons, create PRs, or merge.

## Bindings / secrets
- R2: `SOURCE_BUCKET` (same private bucket; read-only ideally)
- `PROCESSOR_TOKEN`: shared token matching intake's processor token
- `EXTRACTOR_URL`: HTTPS extraction adapter
- `EXTRACTOR_TOKEN`: secret for extraction adapter
- `ARTIFACT_BUCKET`: private R2 bucket for processor artifacts

Extraction adapter contract: POST JSON {job_id, source_sha256, source_name, pdf_base64}; response JSON {pages:[{page:number,text:string,confidence?:number,ocr?:boolean}], ...}. Limit adapter response size and require page indices. Do not send to untrusted endpoints.

This scaffold intentionally stops after extraction and durable provenance artifacts. Later stages (audit, syllabus mapping, coverage, authoring, verification, packaging, PR creation) require separately reviewed integrations and repository contracts; no fabricated completion.
