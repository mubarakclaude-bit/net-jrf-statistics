# Generic Document Intake

Authenticated document upload/status API scaffold. Supported formats are deployment-configured (currently allowlisted: PDF, TXT, Markdown, CSV, HTML, RTF, DOCX, PPTX, XLSX and image MIME types). 20 MB hard limit. Stores private source files, D1 job/events and queue-dispatches processing.

The processing stages and output types are configurable; no subject, exam, curriculum, answer-key, question-bank or learning-content format is assumed. Extraction adapters determine format-specific extraction. Optional workspace taxonomy and resource index may be supplied by trusted configuration.

## API
- `GET /health`
- `GET /`: portal (owner-only Cloudflare Access required before deployment)
- `POST /upload`: authenticated multipart document
- `GET /jobs/{id}`: authenticated job/event status
- `GET /jobs/{id}/artifacts/{filename}`: authenticated, completed-job artifact downloads. Allowed files are manifest, extraction, audit, taxonomy, coverage, production and verification artifacts. Downloaded files are checked against the private integrity manifest.

No files are committed to the repository. See deployment and processor documentation.