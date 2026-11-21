#!/usr/bin/env node
/* Tests tools/intake.js on a made-up content set and made-up worksheets, so it never needs a PDF or the real seed/:
 * the checks that keep a worksheet complete, the near-duplicate finder, and the report.
 *   node tests/intake.test.js
 * `add` (which needs poppler and a PDF) is exercised by hand; see docs/SOURCE_INTAKE.md. */
const fs = require("fs"), os = require("os"), path = require("path"), { spawnSync } = require("child_process");
const TOOL = path.join(__dirname, "..", "tools", "intake.js");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "intake-test-"));
process.env.CONTENT_ROOT = tmp; process.env.INTAKE_DIR = path.join(tmp, "ws");
const w = (rel, data) => { const f = path.join(tmp, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, typeof data === "string" ? data : JSON.stringify(data)); };
const run = (...args) => { const r = spawnSync(process.execPath, [TOOL, ...args], { env: process.env, encoding: "utf8" }); return { code: r.status, out: (r.stdout || "") + (r.stderr || "") }; };
let failed = 0, total = 0;
const expect = (name, ok, detail) => { total++; if (!ok) { failed++; console.log("FAIL " + name + (detail ? "  — " + String(detail).slice(0, 300) : "")); } else console.log("ok   " + name); };

w("seed/catalog.json", { updated: "x", modules: [{ id: "alpha", name: "Alpha", topics: [{ id: "alpha-t1", name: "Widgets", marks: 6 }, { id: "alpha-t2", name: "Gadgets", marks: 4 }] }] });
w("seed/lesson_a1.json", { id: "alphat1", topicId: "alpha-t1", title: "Widgets", objectives: ["Count widgets"], scenes: [{ kind: "summary" }] });
w("seed/alpha_bank.json", { moduleId: "alpha", items: [
  { id: "b1", format: "single", topic: "alpha-t1", stem: "Let X₁ and X₂ be independent Poisson variables with means 2 and 3. Find the variance of X₁ given X₁ + X₂ = 2.", options: ["12/25", "6/25", "2/5", "1"], answer: "A" },
  { id: "b2", format: "single", topic: "alpha-t1", stem: "A fair coin is tossed three times. Find the probability of exactly two heads.", options: ["3/8", "1/8", "1/2", "1/4"], answer: "A" }] });

const T = require(TOOL);
const S = T.loadSeed();
expect("the seed loader finds topics, the lesson and the bank items", S.topics["alpha-t1"] && S.lessons.alphat1 && S.items.length === 2);
expect("Unicode subscripts and spelled Greek fold to the same words", [...T.tokens("X₁ ρ")].join() === [...T.tokens("x1 rho")].join(), [...T.tokens("X₁ ρ")]);
const ix = T.indexItems(S.items);
const near = T.nearest("X1 and X2 are independent Poisson variables, means 2 and 3. Find Var(X1 | X1 + X2 = 2). 12/25 6/25 2/5 1", ix);
expect("a repeat written differently still finds its item", near.item.id === "b1" && near.score >= 0.5, JSON.stringify({ id: near.item.id, s: near.score }));
expect("an unrelated question scores low", T.nearest("Define a Wishart matrix and its degrees of freedom.", ix).score < 0.4);

// a questions workspace, written by hand as `add` would leave it
const id = "abcdef012345", ws = path.join(tmp, "ws", id);
w("ws/" + id + "/source.json", { schema: 1, id, sha256: id + "0".repeat(52), file: "q.pdf", pages: 4, kind: "questions", title: "Made-up compilation", imagePages: [] });
const keep = (n, extra) => Object.assign({ n, page: 1, format: "single", decision: "keep", topic: "alpha-t1", stem: "stem " + n, options: ["a", "b", "c", "d"], printedKey: "A", answer: "A" }, extra || {});
const sheet = items => w("ws/" + id + "/questions.json", { source: id, covers: { from: 1, to: 4 }, items });
sheet([keep(1), keep(2, { page: 9 }), keep(2), keep(4, { topic: "nope" })]);
let r = run("check", id);
expect("check fails, exit 1", r.code === 1, r.out);
expect("a missing question number is reported", /not accounted for: Q3/.test(r.out), r.out);
expect("a duplicate number is reported", /Q2 appears twice/.test(r.out), r.out);
expect("a page outside the document is reported", /page must be .* 1 to 4/.test(r.out), r.out);
expect("an unknown topic id is reported", /topic 'nope' is not a topic id/.test(r.out), r.out);

sheet([keep(1, { answer: "B" }), keep(2, { options: ["a", "a", "c", "d"] }), { n: 3, page: 2, decision: "left-out" },
  keep(4, { format: "multi", options: undefined, statements: ["s1", "s2", "s3"], printedKey: "AC", answer: "CA" })]);
r = run("check", id);
expect("an answer that differs from the printed key needs a keyNote", /computed answer B differs from the printed key A/.test(r.out), r.out);
expect("identical options are caught", /two options are identical/.test(r.out), r.out);
expect("a left-out question needs its reason", /left-out question needs a note/.test(r.out), r.out);
expect("a multi item needs four statements", /four printed statements/.test(r.out), r.out);
expect("multi keys compare as sets (AC equals CA)", !/computed answer CA/.test(r.out), r.out);

sheet([keep(1, { answer: "B", keyNote: "The key is wrong because …" }),
  keep(2, { stem: "Let X₁ and X₂ be independent Poisson variables with means 2 and 3. Find the variance of X₁ given X₁ + X₂ = 2.", options: ["12/25", "6/25", "2/5", "1"] }),
  { n: 3, page: 2, decision: "repeat", note: "Same as Q2" }, keep(4, { topic: "alpha-t2" })]);
r = run("check", id);
expect("a complete worksheet passes", r.code === 0 && /passes: 4 entries/.test(r.out), r.out);
r = run("gaps", id);
const rep = fs.existsSync(path.join(ws, "report.md")) ? fs.readFileSync(path.join(ws, "report.md"), "utf8") : "";
expect("gaps writes report.md and exits 0", r.code === 0 && rep.length > 200, r.out);
expect("the repeat of a bank item is flagged", /\| Q2 \| `b1` \| seed\/alpha_bank\.json \| [01]\.\d\d \| \*\*likely a repeat\*\* \|/.test(rep), rep);
expect("a topic with no lesson is called a Learn gap", /`alpha-t2` Gadgets \| Q4 \| \*\*none: a Learn gap\*\*/.test(rep), rep);
expect("the topic's lesson objectives are shown for comparison", /`alphat1` \(seed\/lesson_a1\.json\): Count widgets/.test(rep), rep);

// a learning-material workspace
const lid = "fedcba543210";
w("ws/" + lid + "/source.json", { schema: 1, id: lid, sha256: lid + "0".repeat(52), file: "book.pdf", pages: 30, kind: "learning", title: "Made-up textbook", imagePages: [] });
const csheet = items => w("ws/" + lid + "/concepts.json", { source: lid, items });
csheet([{ concept: "Widget counting", pages: [3], topic: "alpha-t1", status: "covered", lesson: "nope" },
  { concept: "Widget sums", pages: [40], topic: "alpha-t2", status: "partial", lesson: "alphat1" },
  { concept: "Gadget theory", pages: [5], topic: "alpha-t2", status: "missing" },
  { concept: "Measure theory", pages: [6], status: "outside" }]);
r = run("check", lid);
expect("a concept must name a real covering lesson", /lesson 'nope' does not exist/.test(r.out), r.out);
expect("a lesson from another topic is caught", /lesson alphat1 belongs to alpha-t1, not alpha-t2/.test(r.out), r.out);
expect("pages beyond the document are caught", /1 to 30/.test(r.out), r.out);
expect("missing and outside concepts need a note", /missing concept needs a note/.test(r.out) && /outside the Paper 2 syllabus/.test(r.out), r.out);
csheet([{ concept: "Widget counting", pages: [3], topic: "alpha-t1", status: "covered", lesson: "alphat1" },
  { concept: "Widget sums by hand", pages: [4, 5], topic: "alpha-t1", status: "partial", lesson: "alphat1", note: "No worked sum (p. 5)" },
  { concept: "Gadget theory", pages: [5], topic: "alpha-t2", status: "missing", note: "Nothing teaches gadgets (p. 5)" },
  { concept: "Measure theory", pages: [6], status: "outside", note: "Beyond the syllabus" }]);
r = run("check", lid);
expect("a complete concepts worksheet passes", r.code === 0, r.out);
r = run("gaps", lid);
expect("the learning report counts each status", /\| 1 \| 1 \| 1 \| 1 \|/.test(r.out), r.out);
expect("it lists the proposed changes with their pages", /Widget sums by hand \| partial \| `alpha-t1` \| `alphat1` \| 4, 5 \| No worked sum/.test(r.out) && /Gadget theory \| missing \| `alpha-t2` \| none/.test(r.out), r.out);

r = run("list");
expect("list shows both workspaces", r.out.includes(id) && r.out.includes(lid), r.out);
r = run("check", "zzz");
expect("a bad workspace id is explained, exit 2", r.code === 2 && /12 hex characters/.test(r.out), r.out);
r = run("add", path.join(tmp, "seed", "catalog.json"), "--kind", "questions");
expect("add refuses a file that is not a PDF", r.code === 2 && /Only PDF files/.test(r.out), r.out);
r = run("add", path.join(tmp, "seed", "catalog.json"));
expect("add asks what kind of document it is", r.code === 2 && /--kind questions/.test(r.out), r.out);

fs.rmSync(tmp, { recursive: true, force: true });
console.log((total - failed) + "/" + total + " intake checks passed");
process.exit(failed ? 1 : 0);
