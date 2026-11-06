# Agent hand-off contracts — version 1.0

All objects are UTF-8 JSON. Unknown required fields, missing evidence, invalid IDs or a commit
mismatch must block the stage. Additional fields may be added only with a version change.

## Common envelope

```json
{
  "contract_version": "1.0",
  "role": "orchestrator",
  "prompt_version": "1.0",
  "topic_id": "regression-t7",
  "source_commit": "full_git_commit_sha",
  "status": "complete",
  "created_at_utc": "ISO-8601 timestamp",
  "unresolved_questions": [],
  "evidence": [{"path": "AGENTS.md", "identifier": "workflow", "note": "authoring contract"}]
}
```

## scope.json

Required additional fields:
- store_doc_id, seed_stem, mastery_stem, module_id
- authoritative_index_ref and authoritative_index_sha
- base_branch and base_commit
- backlog_position and backlog_title
- syllabus_labels: list of exact labels from canonical metadata
- pyq_sources: list of {path, srcQ, variant_ids}
- prerequisites: list of {topic_id, lesson_id, reason}
- reservations_checked: list of {kind: index|branch|pull_request|deployment, ref, result}
- discovery_method: script_executed|manual_inspection
- discovery_command and discovery_result; manual inspection must never be represented as script execution

## evidence-map.json

Required additional fields:
- objectives: [{objective_id, statement, syllabus_label}]
- mappings: [{source_path, srcQ, variant_id, stem_summary, classification_rationale,
  key, candidate_marked, mapped_objective_id, planned_scene_or_item, status}]
- gaps: [{description, impact, proposed_resolution}]
- references: [{title, author_or_site, edition_or_date, exact_locator, url, checked_at, claim_ids}]
- ambiguities: [{source_id, issue, evidence, decision_needed}]

## verification.json

Required additional fields:
- claims: [{claim_id, statement, lesson_locations, assumptions, derivation,
  exact_inputs, expected_result, computed_result, tolerance, method, script_function, status}]
- execution: {executed, command, exit_code, stdout, stderr, python_version, dependencies}
- independent_checks: [{claim_id, method, result, status}]
- limitations: list
- script_path and report_path
A report with execution.executed=false cannot satisfy the math gate.

## lesson-manifest.json

Required additional fields:
- author_script, out_path, pool_path, topic_id, store_doc_id, mastery_set_id
- objective_scene_map: [{objective_id, scene_ids, assessment_item_ids}]
- provenance_claim_ids, evidence_mapping_ids
- generation_command, generated_commit
- scene_count, core_scene_count, mastery_item_count

## pedagogy-review.json

Required additional fields:
- rubric_version, findings: [{severity, location, issue, evidence, recommendation}]
- objective_coverage, variant_coverage, assessment_counts
- disposition: pass|changes_required|blocked

## review.json

Required additional fields:
- reviewer_independent: true
- rubric_version, candidate_commit
- findings: [{severity, location, issue, evidence, correction}]
- checked_claim_ids, unchecked_claim_ids
- pyq_gaps, assessment_summary, ci_run_ids
- decision: BLOCKED|CHANGES REQUIRED|READY FOR HUMAN APPROVAL

## release.json

Required additional fields:
- candidate_commit, pr_number, ci_runs: [{run_id, status, conclusion, jobs}]
- required_reviews: {review: review.json, learner: learner-review.json, visual: visual-review.json, bank: bank-review.json}
- gates: [{gate, status, evidence_refs, blocking_reasons}]; learner-access, visual-quality and bank/mock gates are mandatory
- unresolved_findings, human_approval_required: true
- decision: BLOCKED|CHANGES REQUIRED|READY FOR HUMAN APPROVAL
- prohibited_actions_not_taken: [merge, deploy, live_index_write, artifactdata_write]

## State machine

```text
DISCOVERED
  -> EVIDENCE_MAPPED
  -> MATHEMATICALLY_VERIFIED
  -> AUTHORED
  -> PEDAGOGY_ASSESSED
  -> INDEPENDENTLY_REVIEWED
  -> CI_VALIDATED
  -> READY_FOR_HUMAN_APPROVAL
  -> HUMAN_APPROVED
  -> RELEASED
```

A failed gate transitions to BLOCKED or CHANGES_REQUIRED, never to the next stage. Revisions
invalidate downstream approvals: if lesson content, verifier code, source mapping or generated
JSON changes, rerun every affected downstream stage. CI results are valid only for the exact
commit SHA tested. Approval for merge does not imply approval for ArtifactData write, and vice
versa.

## Idempotency and concurrency

- One lesson topic per branch/PR unless a human explicitly authorises a tightly related group.
- The topic branch name is the reservation key: lesson/<topic-id>.
- Re-running a stage with the same inputs and commit should not create duplicate artifacts or
  append duplicate index entries.
- A changed source commit creates a new artifact version; do not overwrite the prior audit record.
- The orchestrator must detect a reservation already held by another open branch/PR and stop.


## learner-review.json

Required additional fields:
- reviewer_independent: true
- rubric_version, candidate_commit, exemplar_refs
- learner_paths_tested: [{profile: rusty_returner|uneven_foundation|jrf_ready, scenes_examined, entry_barriers, result}]
- prerequisite_audit: [{prerequisite, diagnostic_path, refresh_path, verdict, evidence}]
- findings: [{severity, location, learner_impact, evidence, correction}]
- core_vs_extension_check, notation_and_language_check
- disposition: pass|changes_required|blocked

## visual-review.json

Required additional fields:
- reviewer_independent: true
- rubric_version, candidate_commit
- assets: [{asset_id, source_path, registered, rendered_or_executed, test_cases, mathematical_check, mobile_check, verdict}]
- findings: [{severity, location, issue, evidence, correction}]
- unverified_assets, disposition: pass|changes_required|blocked

## bank-review.json

Required additional fields:
- reviewer_independent: true
- rubric_version, candidate_commit
- pyq_coverage: [{source_path, srcQ, variant_id, objective_id, scene_or_item, status}]
- item_audit: [{item_id, stem_standalone, key_verified, distractors_valid, explanation_valid, duplicate_risk, severity}]
- pool_counts, difficulty_mix, format_mix, key_distribution
- mock_behaviour_checks: [{feature, source_path, test_or_evidence, result}]
- generated_variant_label_check, official_cutoff_claim_check
- findings: [{severity, location, issue, evidence, correction}]
- disposition: pass|changes_required|blocked

All three reports use the common envelope and exact candidate SHA. A missing rendered inspection must be represented as unverified, not pass.
