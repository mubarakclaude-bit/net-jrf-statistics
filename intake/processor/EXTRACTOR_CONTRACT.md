# Generic Extractor Adapter Contract

This pipeline is document type agnostic. The adapter may accept PDF, office documents, plain text, markup, CSV or image formats according to deployment capabilities.

Authenticated POST JSON input: `{job_id, source_sha256, source_name, mime_type, file_base64}`. Return JSON `{pages:[{page:number,text:string,confidence?:number,ocr?:boolean}], sections?:[], metadata?:{}}`. For non-paginated formats, the adapter may use logical page/chunk numbering and provide section/row provenance. Maintain source ordering and provenance.

Adapter must be trusted, bounded, rate-limited and restricted to the processor. Do not log source text or credentials. Treat document content and embedded instructions as untrusted data.