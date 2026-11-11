# Mathematics T10 verification report

Date: 12 November 2026

## Package
- 15 core scenes, required app scene types, two applied scenarios, derivative-selection flow, revision sheet and three references.
- 20 mastery questions: 6 easy, 10 moderate, 4 hard; 9 numeric and 2 multi-statement.
- Answer key spread: A=5, B=5, C=5, D=5.
- Evidence map: evidence/mathst10.md.

## Automated verification — PASS
- Exact anchors: polynomial partials, mixed partials, chain rule along a path, gradient and directional derivative.
- App vScene validator: PASS.
- Mastery pool validator: PASS.
- Formula renderer: 133 formula lines across T2/T3/T5–T10, zero parser refusals.
- JSON syntax: PASS.
- Lesson index and test harness consistency: PASS; 52 lesson seeds indexed and wired.
- Application build: PASS.
- Full Playwright browser regression suite: PASS; no harness errors.

GitHub Actions run: https://github.com/mubarakclaude-bit/net-jrf-statistics/actions/runs/43091171595

Status: VALIDATED ON DEVELOPMENT BRANCH. Kept as draft pending consolidated Mathematics release and final human approval. Not yet in production.
