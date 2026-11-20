# Repository-native content production runbook

**Scope:** UGC NET/JRF Statistics Paper 2 only. The repository is the source of truth. This runbook operationalizes document-driven production without adding a server, watcher, database, dashboard, or alternate publishing store.

## Operating model

There are two routes, with a shared review and release gate:

- **Path A — question documents:** extract and check questions/keys; map each question to catalog topic IDs; enrich the existing question-bank/practice structures; verify all numerical outputs with executed Python; report concept gaps.
- **Path B — learning material:** use source material to discover concepts and page evidence; compare concept-by-concept with the existing lesson; propose missing or weak coverage; author fresh prose and examples; review pedagogy and visuals.

A mixed document may enter both paths. Source material is evidence for discovery, not a prose source. Do not commit copyrighted PDFs or copy/closely paraphrase their text.

## Roles and limits

| Stage | Actor | Work |
|---|---|---|
| Supply and scope | Owner | Supply PDFs/keys, resolve source-status policy and approve contract proposals/release. |
| Extract | Shell-enabled session (Claude Code) | OCR/extract, inspect page/figure fidelity, run Python verification scripts and local commands. |
| Author and package | GitHub-capable assistant | Read repository files via GitHub API; draft seed JSON, scripts, reports and PR commits. No shell execution. |
| Independent review | Other assistant | Review PR against AGENTS.md checklist; read verification code and independently recompute/check content. |
| Automated gate | GitHub Actions | Run existing validate/browser/acceptance jobs. |
| Release | Owner | Merge approved PR to main. Only main deploys. |

The GitHub PR/issues are the tracking system. Keep a source register and report in the PR or approved repository documentation; do not invent a dashboard.

## Path A — question document checklist

1. **Register intake.** Record title, edition/date if known, SHA-256 file hash, supplied answer-key source, and processing purpose. Keep the PDF outside Git.
2. **Extract (shell session).** Create an extraction working file outside seed: page, question number, full stem, four options (if applicable), equations/figures, key, and page. Preserve source page references. Mark OCR uncertainty instead of guessing.
3. **Extraction checks (shell session).** Report question count, options count per question, missing/duplicate question numbers, answer-key count and mismatches, missing/unclear figures and pages. For four-option MCQs, check four options per item.
4. **Map (assistant via GitHub API).** Map each question to an existing topic ID in seed/catalog.json. Use seed/meta_syllabus.json for unit labels. Do not invent topic IDs or use free-text mapping in place of IDs. Flag multi-topic items for review.
5. **Coverage (assistant via GitHub API).** Inspect relevant existing lessons, anchors, provenance, PYQ variant/practice bank. Use existing commands as the guide: `npm run content -- gaps`, `topic <topicId>`, and `pyq <n>` where applicable. Compare the actual concept, not only the topic title.
6. **Solutions and variants (assistant via GitHub API).** Author original, beginner-friendly solutions and the agreed variants. Preserve `srcQ` and `srcPaper` for variants. Other-exam syllabus overlap is a comparison, not a claim that the question appeared in another exam.
7. **Verification (shell session).** Write one verification script per coherent group before/alongside prose; execute it. Every numerical result in solutions or variants must be computed by the script. Record commands, assertions, and result. Do not treat a second model call as executed verification.
8. **Independent review (other assistant).** Review the source/key, topic mapping, solution logic, distractors, verification code, and learner clarity against AGENTS.md checklist.
9. **Gap report (assistant via GitHub API).** Report concepts taught, partially taught, missing, and out-of-syllabus; tie each finding to question IDs/pages and existing lesson sections. A lesson change is proposed only when justified.
10. **Package.** Add question/variants to `seed/<module>_pyq_variants.json` or the correct practice bank. Edit an existing lesson's seed JSON directly per CONTENT_GUIDE §3a. Mastery pools remain exactly 20 items with the prescribed 6/10/4 difficulty split and answer-letter spread; do not append PYQs to mastery pools.
11. **Validate and PR.** Use existing contracts, `npm run check`, audits, verifiers and CI. Batch related work as one PR per module and one commit per push. Do not merge.

### Answer-key status convention (pending owner approval)

- **Official key:** source record is a past question (`source: "pyq"`) and the key is supported by the supplied official key. Retain evidence.
- **Provisional:** official key is absent/unreadable or verification is not yet complete; clearly label it provisional in the review record.
- **Disputed:** preserve the official key and separately document the mathematically supported answer and dispute. Proposed learner display: “Official key disputed” with both key and explanation. Do not silently replace the key.
- **Derived variant:** `source: "variant"`; answer comes from executed verification code, not an external key.

Use `answer` for the recorded key and `youMarked` only for the learner's/candidate's response in actual-paper records; never use `youMarked` to encode a key dispute. The display/field contract for provisional and disputed status is an owner decision; do not introduce fields without approval.

## Path B — learning material checklist

1. **Register intake (owner/assistant).** Record source identity, edition and hash. The source remains outside Git.
2. **Extract and index (shell session).** Segment concepts and record page-level evidence; flag OCR uncertainty and equations/figures that need inspection.
3. **Map (assistant via GitHub API).** Map only to valid catalog topic IDs and syllabus labels.
4. **Compare (assistant via GitHub API).** Inspect actual lesson scenes, explanations, worked examples, questions, anchors and provenance. Classify each concept: covered adequately, partially covered, missing, or not in scope.
5. **Gap proposal (assistant via GitHub API).** Describe the concept-level gap, exact lesson/scene, source pages, and proposed change. Do not treat a whole topic as missing when only one concept is absent.
6. **Author (assistant via GitHub API).** Write original prose; do not copy or closely paraphrase the source. Edit merged lesson seed JSON directly. Include source-page evidence in provenance as appropriate.
7. **Pedagogy/visual review (conditional).** Trigger for a new lesson, substantial rewrite, or gap finding marked hard-to-understand. Recommend scenes and visuals using the actual lesson format and existing visualization whitelist.
8. **Verify (shell session).** Execute group verifier; render/check equations and run local checks where available.
9. **Independent review (other assistant).** Review content and verifier code using AGENTS.md checklist.
10. **Validate and PR.** Existing contracts and CI; batch one PR per module; owner approval and merge.

## Gap-report record (proposal; not a new validator yet)

Use a Markdown table or JSON in the PR review notes. Required fields:

- module and catalog topic ID
- concept (inventory item if approved; otherwise explicitly provisional)
- status: covered / partial / missing / out-of-scope
- source title, hash reference and pages
- question IDs (srcQ/srcPaper), if any
- existing lesson file and scene(s)
- evidence of gap (specific omission, not vague judgment)
- proposed action: no change / enhance scene / add section / new lesson / practice
- verification and review status

## Pedagogical & visual proposal

The reviewer returns a proposal—not fabricated scene/viz names—with:

- topic ID and trigger
- learning difficulty and reason
- scene kind(s): foundation, intuition, explore+viz, theory blocks, worked, completion, guided, trapcheck, recall, summary
- existing scene to edit or insertion point
- flow diagram proposal, if useful
- visualization name selected only from the current VIZ_OK list in src/62-gen.js; specify purpose, caption and placement
- simplification, sequencing, worked-example or comparison-table proposal
- whether a new visualization is required

A new visualization is a core change (src/30-viz.js and src/62-gen.js) and requires owner review. Prefer existing VIZ_OK visuals. Run this review only at the trigger conditions above.

## Concept inventory — approval required

**Not approved for implementation yet.** Proposed file: `seed/concepts_<module>.json` rather than expanding catalog.json. catalog.json remains the topic index; inventory files define the concepts a topic should teach.

Proposed shape:

```json
{
  "moduleId": "estimation",
  "topics": {
    "estimation-t1": {
      "topicId": "estimation-t1",
      "concepts": [
        {
          "id": "estimation-t1-c01",
          "name": "Concept label",
          "required": true,
          "depth": "application",
          "prerequisites": [],
          "expectedEvidence": ["definition", "intuition", "worked_example", "practice"]
        }
      ]
    }
  }
}
```

Populate through a draft by an assistant from syllabus topic IDs, existing lessons, PYQs and source evidence; review concept boundaries/depth with the owner; approve through a PR. Until approved, gap reports must clearly mark concept inventories as provisional and must not make the inventory a CI contract.

## Source register (proposal)

Keep PDFs out of Git. A small register should include title, edition/year, SHA-256, pages used, pipeline (question/Learn), topic IDs and PR/lesson/bank references. Location proposal: `docs/SOURCE_REGISTER.md`; owner approval required.

## Thin slice — do before automation

**Slice A: CSIR Estimation 2011–2025 PDF (blocker for PR #104).**
- Owner-supplied PDF and answer-key material.
- Shell session checks extraction: question count, four options where applicable, key count, anomalies and page references.
- Assistant maps topic IDs and reviews existing coverage.
- Author variants/solutions; shell executes verification scripts.
- Other assistant reviews; report concept gaps.
- Package a single module PR; do not merge.

**Slice B: one textbook chapter against one module.**
- Owner supplies chapter and module.
- Extract/index page evidence; map; compare with existing lesson; report concept gaps.
- Draft fresh lesson changes and conditional visual proposal.
- Verify/review/package as one module PR.

**Slice C: automate only pain points demonstrated in A and B.** Candidates are extraction audits, question/key reconciliation, topic-map drafts, gap report generation, and proposal templating. No watcher, service, database, dashboard or batch engine until evidence from the two runs justifies it.

## Deployment and release guardrails

- Paper 2 only; Paper 1 is out of scope.
- GitHub is source of truth; no Claude artifact publishing.
- One PR per module; one commit per push containing the complete related changes.
- PR CI must pass validate/browser/acceptance. CI is not a substitute for content review.
- Only main deploys; owner merges. Never merge/deploy without explicit approval.
- Keep the Vercel deployment budget (100/day) in mind; avoid unnecessary merges.
