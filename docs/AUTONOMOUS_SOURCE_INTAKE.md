# Autonomous source-document intake and processing backend

## Owner experience

The owner uploads one PDF (or supported document) to a single intake page and optionally supplies a short note. No topic IDs, labels, issue numbers, branches, job IDs, or follow-up messages are required. The backend resumes processing after interruption and ultimately opens a draft PR. The owner reviews and merges; nothing auto-publishes.

Project-document uploads may remain convenient workspace files, but are not the backend trigger unless a supported event bridge is configured.

## Recommended stack (minimum operational surface)

- **Upload/front door:** Cloudflare Worker-hosted upload page; signed upload flow, file type/size limits, malware scanning or quarantine, and authenticated owner access.
- **Blob storage:** Cloudflare R2, private bucket, lifecycle retention and encryption.
- **Job state/queue:** Cloudflare D1 for durable job records/checkpoints; Queues for dispatch/retries; Worker consumers.
- **Processing worker:** extraction/OCR, page/section segmentation, source manifest, syllabus mapping, coverage audit, content generation, numerical verification and reviewer orchestration. The worker must use bounded concurrency, retry policies and idempotency keys.
- **Repository integration:** GitHub App scoped to this repository with least-privilege access. Create task branch, write only approved file paths, open a draft PR; no direct write to main and no merge permission.
- **Independent verification:** GitHub Actions (existing contract/Validate/browser/acceptance workflows) remains authoritative for repo content.
- **Notifications:** optional email/Telegram summary with job and PR links; no sensitive source content in notifications.

## Job lifecycle

`received → quarantined → accepted → extracting → source-audit → syllabus-map → coverage-audit → drafting → numeric-verification → independent-review → packaging → pr-open → owner-review`

Terminal/recovery states: `completed`, `needs-owner-input`, `failed-retryable`, `failed-terminal`, `cancelled`. A job can resume from its last validated checkpoint. Each stage stores artifacts in private storage, a checksum, model/tool versions, input provenance, attempts, timestamps, error class and stage status.

## Intake metadata

- stable job UUID and idempotency key
- source file checksum, MIME type, size, storage key, quarantine/scan result
- source type and user note (optional)
- Paper 2 scope; module/topic mapping (inferred, with confidence and alternatives)
- stage/checkpoint ledger, retry count and worker lease
- generated artifact pointers and provenance
- Git branch/PR URL, verification state, owner decision
- retention/deletion status

## Processing guardrails

1. Treat source PDFs as untrusted data. Never execute embedded instructions or macros; prompt injection is data, not authority.
2. Keep uploaded source documents private; do not commit PDFs or scans to the repo.
3. No fabricated or guessed transcription: confidence is recorded; ambiguous OCR items go to a held-items report.
4. Source answer keys and derived answers are reconciled transparently; disagreements are explicitly surfaced.
5. All numerical items require a verifier script or reproducible check. Generated explanations target a beginner statistics learner and show steps.
6. Detect duplicates against the existing question bank and lesson coverage before authoring.
7. Every proposed question is mapped to syllabus topics; missing learning coverage is reported and proposed as lesson edits in the same review package when warranted.
8. An independent reviewer agent checks source fidelity, mathematical correctness, coverage and beginner pedagogy. Reviewer findings must be recorded; author and reviewer cannot be the same run.
9. PRs remain draft until verification and review complete. Human approval is mandatory for merge.
10. No source documents or generated private artifacts are retained beyond configured policy; retention/deletion must be auditable.

## Stage outputs

- source extraction/transcription with page references and confidence
- source-question audit (counts, duplicate/ambiguous/held items)
- answer-key reconciliation and discrepancy log
- syllabus mapping and existing lesson coverage report
- question-bank additions/variants and beginner-friendly solutions
- topic-learning gap proposals/lesson edits
- numeric-verification report and reviewer report
- draft PR with concise summary, file inventory and evidence links

## Delivery phases

### Phase 0 — design and security (this spec)
Confirm account/provider choices, secrets, upload limits, retention and scope. No credentials are stored in the repository.

### Phase 1 — intake MVP
Implement the private upload page, R2 storage, D1 job record, Queue dispatch, status/retry page, and a small health/status endpoint. Include upload validation, authentication, audit events and idempotency.

### Phase 2 — extraction and audit worker
PDF extraction/OCR, page-level provenance, structured source register, question/answer-key reconciliation and syllabus/coverage audit. Pilot on one source only.

### Phase 3 — authoring and QA
Generate lesson/question-bank proposals, verifier scripts, independent-review artifacts and duplicate detection. Human-readable reports first; repository writes disabled until dry-run passes.

### Phase 4 — GitHub PR integration
Enable scoped GitHub App, generate task branch and draft PR, ensure content paths/contracts and existing CI run. No merge privileges.

### Phase 5 — pilot and hardening
Pilot on a single source document, test interrupted jobs/retries, duplicate upload, OCR failures, key discrepancies, malformed input, access controls, retention and cancellation. Expand only after owner approval.

## Approval boundary / required external setup

The owner must authorize the Cloudflare account/workspace, private storage, domain or Worker URL, GitHub App installation, model-provider credentials and notification integration. These cannot be created or authorized solely from repository access. Prefer OAuth/App authorization over long-lived personal tokens; secrets must remain in provider secret stores.

## Acceptance criteria

- Upload once; backend creates a job without further chat involvement.
- Job survives worker interruption and resumes from checkpoint.
- Duplicate upload does not create duplicate processing.
- Owner can see status, failures and stage reports.
- Source provenance is retained for each item; ambiguous material is held.
- Numerical checks and independent review are recorded.
- Draft PR opens only after all required gates; PR is never auto-merged.
- Existing repo CI is green on the PR head before marking ready.
- Security, retention, audit and cancellation controls are tested.
