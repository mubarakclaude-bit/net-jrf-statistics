# Independent lesson review rubric

The reviewer must inspect the lesson, source evidence, verification code/output and generated JSON. Do not accept the author's self-assessment as proof. Record every finding with file/scene/item, severity, evidence and a concrete correction.

## Severity
- **Critical:** wrong theorem, formula or key; serious release/security/data issue. Blocks release.
- **High:** material mathematical error, false assumption, misleading PYQ mapping, multiple/no correct answers, broken teaching flow or missing required evidence. Blocks release.
- **Medium:** material ambiguity, weak distractor, incomplete explanation, accessibility issue or objective/assessment mismatch. Resolve or obtain explicit human acceptance.
- **Low:** wording, formatting or minor polish. May be deferred with rationale.

## Review dimensions

### Statistical correctness
- Are definitions, assumptions, theorem statements and conclusions exact?
- Are dimensions, notation, conditioning, degrees of freedom and boundary cases correct?
- Are derivations complete and valid?
- Are numerical values independently reproducible?
- Are asymptotic, approximate and exact results labelled correctly?
- Are counterexamples and edge cases handled?

### Evidence and syllabus alignment
- Does each PYQ mapping use the full stem and actual content, not merely a bank label?
- Are source keys and candidate-marked answers represented accurately?
- Does every relevant variant map to an objective, scene or mastery item?
- Are syllabus labels checked against canonical metadata?
- Are prerequisites real and sufficient?

### Teaching quality
- Does the lesson begin with purpose and plain language before symbols?
- Does the foundation check every assumed prerequisite and teach shaky prerequisites?
- Does intuition precede formalism?
- Are there at least two substantial, realistic scenarios?
- Does the worked example show every step, then fade through completion and guided transfer?
- Are hints progressive without revealing answers?
- Are misconceptions explained rather than merely named?
- Can each scene be understood without hidden context?

### Assessment validity
- Does every item have one defensible correct answer?
- Is each stem standalone and free of accidental clues?
- Are distractors plausible and distinguishable?
- Are calculations, options, keys, explanations and checks consistent?
- Are numeric and multi-statement formats valid?
- Is answer-letter distribution within project limits?
- Do explanations teach the principle rather than merely restate the key?

### Technical integrity
- Do IDs, topicId, moduleId, setId, OUT and POOL agree?
- Are required fields and scene types valid?
- Are formulas renderable and visualisation names registered?
- Are provenance and verification reports included?
- Did the exact candidate commit pass all required scripts and browser suites?
- Are generated seeds attached and consistent with the index and harness?

## Required review output
Return exactly one decision: BLOCKED, CHANGES REQUIRED or READY FOR HUMAN APPROVAL. Then report:
1. Critical/high findings (must be zero for readiness).
2. Medium/low findings.
3. PYQ and syllabus coverage gaps.
4. Mathematical claims independently checked and not checked.
5. Assessment audit summary.
6. Exact CI/test evidence inspected, including run ID and commit SHA.
7. Explicit limitations. Never claim a test passed without its actual result.

The reviewer cannot change release state or merge the PR.
