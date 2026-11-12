#!/usr/bin/env node
/* Tests tools/papers.js: finding papers by file name, reading question numbers, and scrubbing the candidate's own answers.
 *   node tests/papers.test.js                                                                                           */
const { paperIdOf, questionNumber, scrubPaper, DEFAULT_PAPER } = require("../tools/papers");
let failed = 0, total = 0;
const expect = (name, got, want) => { total++; const ok = JSON.stringify(got) === JSON.stringify(want); if (!ok) { failed++; console.log("FAIL " + name + "  — got " + JSON.stringify(got) + ", wanted " + JSON.stringify(want)); } else console.log("ok   " + name); };

expect("the original paper is j26", DEFAULT_PAPER, "j26");
expect("pyq_j26_full is paper j26", paperIdOf("pyq_j26_full"), "j26");
expect("pyq_d25_full is paper d25", paperIdOf("pyq_d25_full"), "d25");
expect("a variant bank is not a paper", paperIdOf("regression_pyq_variants"), null);
expect("a file that merely contains the words is not a paper", paperIdOf("pyq_j26_full_old"), null);
expect("capitals are not a paper id", paperIdOf("pyq_J26_full"), null);
expect("a mastery pool is not a paper", paperIdOf("regression_t5_mastery"), null);

expect("number from the topic label", questionNumber({ topic: "June 2026 Paper 2 · Q9", id: "zz" }), 9);
expect("number from an id ending -q09", questionNumber({ id: "j26-q09" }), 9);
expect("number from an id ending -q50", questionNumber({ id: "d25-q50", topic: "no number here" }), 50);
expect("the topic label wins over the id", questionNumber({ topic: "Paper · Q3", id: "x-q7" }), 3);
expect("an unreadable item is 0, which the content check reports", questionNumber({ id: "nothing" }), 0);

const doc = () => ({ source: "pyq", items: [
  { id: "a-q01", stem: "s", answer: "A", youMarked: "B", responseSheet: "x", explanation: "The key is A. Response sheet Q1; the candidate marked B. Further detail." },
  { id: "a-q02", stem: "s", answer: "C", explanation: "Plain explanation." },
  { id: "a-q03", stem: "s", answer: "D", youMarked: "D" }] });
const d = doc(), n = scrubPaper(d);
expect("scrub reports how many items it changed", n, 2);
expect("scrub removes youMarked and responseSheet everywhere", d.items.some(i => "youMarked" in i || "responseSheet" in i), false);
expect("scrub removes the 'Response sheet Qn;' tail and keeps what comes before it", d.items[0].explanation, "The key is A.");
expect("scrub leaves a plain explanation and the answer key alone", [d.items[1].explanation, d.items[0].answer, d.items[2].answer], ["Plain explanation.", "A", "D"]);
expect("scrub is idempotent", scrubPaper(d), 0);
expect("scrub tolerates a document with no items", scrubPaper({}), 0);
expect("the scrubbed paper contains no trace of the marked answers", /youMarked|responseSheet|Response sheet/.test(JSON.stringify(d)), false);

console.log("\n" + total + " checks, " + failed + " failed");
process.exit(failed ? 1 : 0);
