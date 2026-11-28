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
expect("a text layer that lost maths symbols is detected (empty brackets, U+FFFD)",
  T.symbolsLost("We need P(A|B). () = 0.2 , () = 0.4") && T.symbolsLost("parameters (�, �2)") && !T.symbolsLost("P(A) = 0.2 and f(x) = 2x; one stray �"));
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
expect("symbols turned into '?' by a non-UTF-8 write are detected, plain question marks are not",
  ["P(A?)=0.3", "P(A?B?)=0.5", "1+2q?p", "x�y"].every(T.symbolsMangled) && !["Which one is correct?", "is it true? Then", "P(Aᶜ) = 0.3 and P(A ∩ Bᶜ) = 0.5", "what is P(B)?"].some(T.symbolsMangled));
expect("the forms that slipped past the first check in PR #154 are detected too",
  ["(C(52,26) ? 1)/(2^51 ? 1)", "P(A ? B)=0.8", "the probability that a? ? b? is divisible", "{1, 2, 3, ?, 3n}", "in 4!?3!?2! ways", "Let E? denote the event", "+(2/3)^3(1/3)+?=(2/3)"].every(T.symbolsMangled) &&
  !["What is the probability that none of them will be selected?", "Which of these is true? (Standard deviation uses n.)", "Then x = ?"].some(T.symbolsMangled));
expect("UTF-8 read back as cp1252 (PowerShell Get-Content) is detected as well",
  ["E[X(Xâˆ’1)]=5/3", "E[XÂ²]=34/3"].every(T.symbolsMangled) && !["café", "x − 1", "σ² and Σ"].some(T.symbolsMangled));
sheet([keep(1, { stem: "If P(A?)=0.3 and P(B)=0.4, then P(A?B?) is", answer: "A" }), keep(2), keep(3), keep(4, { topic: "alpha-t2" })]);
r = run("check", id);
expect("check rejects a worksheet whose maths symbols were lost as '?'", r.code === 1 && /maths symbols were lost/.test(r.out), r.out);
sheet([keep(1, { answer: "B", keyNote: "The key is wrong because …" }),
  keep(2, { stem: "Let X₁ and X₂ be independent Poisson variables with means 2 and 3. Find the variance of X₁ given X₁ + X₂ = 2.", options: ["12/25", "6/25", "2/5", "1"] }),
  { n: 3, page: 2, decision: "repeat", note: "Same as Q2" }, keep(4, { topic: "alpha-t2" })]);
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

// scan's decisions, from gathered facts (no PDF needed)
const reg = [{ title: "Known compilation", outputs: ["seed/x.json"], sha256: ["aaa"], files: ["Known Copy.pdf"] }];
const fact = (name, o) => Object.assign({ name, sha256: name + "-hash", pages: 20, text: "", textChars: 2000, inProgress: null }, o || {});
const dec = (f, seen) => T.classify(f, reg, seen || {});
expect("a registered hash is skipped as already in the app", /already in the app: Known compilation/.test(dec(fact("other name.pdf", { sha256: "aaa" })).why));
expect("a registered file name is skipped even when the copy's hash differs", dec(fact("known copy.pdf")).decision === "skip");
expect("a second copy of the same file is a duplicate", /duplicate of first\.pdf/.test(dec(fact("second.pdf", { sha256: "s" }), { s: "first.pdf" }).why));
expect("a receipt is personal and never processed", /personal/.test(dec(fact("Online Application Receipt.pdf")).why));
expect("a first page with a roll number is personal", /personal/.test(dec(fact("scan 01.pdf", { text: "Roll No: 1234  Date of Birth: 01-01-2000" })).why));
expect("an unreadable PDF is skipped with advice", /download it again/.test(dec(fact("broken.pdf", { pages: 0 })).why));
expect("a document already started here comes first", dec(fact("half done.pdf", { inProgress: { kind: "questions", done: 4 } })).score === 100);
const gate = dec(fact("GATE statistics paper 2025.pdf", { text: "Q.1 Even though ... Q.2 ... (A) (B)" }));
const quiz = dec(fact("Day 9 Quiz Solution.pdf", { text: "(1) Suppose that ... (a) 0.2 (b) 0.5 (2) Let X ..." }));
const notes = dec(fact("Time Series notes.pdf", { text: "1 Models for time series. A time series is a set of statistics, usually collected at regular intervals." }));
expect("a past paper is a question document", gate.kind === "questions" && /past paper/.test(gate.why), JSON.stringify(gate));
expect("a quiz is a question document", quiz.kind === "questions", JSON.stringify(quiz));
expect("notes are learning material", notes.kind === "learning", JSON.stringify(notes));
expect("a question name with image-only questions still counts as questions", dec(fact("Unit 5 practice questions.pdf", { text: "DEEP INSTITUTE coaching watermark text" })).kind === "questions");
expect("numbered headings in notes do not make them questions", dec(fact("Markov notes.pdf", { text: "1. Definitions\n2. Basic properties\n3. Transition matrix\n4. Hitting times\n5. Strong Markov\n6. Recurrence\n7. Invariant\n8. Convergence\n9. Reversibility" })).kind === "learning");
expect("past papers rank above quizzes, and quizzes above learning material", gate.score > quiz.score && quiz.score > notes.score);
expect("within a kind, the shorter document ranks first", dec(fact("a quiz.pdf", { pages: 10 })).score > dec(fact("b quiz.pdf", { pages: 40 })).score);
expect("a file with no statistics words is marked down and says why", /check it is in the syllabus/.test(dec(fact("Population studies quiz.pdf", { text: "(1) census (a) (b)" })).why));
expect("a file it cannot place asks for a look", dec(fact("scan 7.pdf", { textChars: 40 })).decision === "look");

// the second pass: explanations and an independent recomputation, batch by batch, kept in the workspace
const vw = lines => w("ws/" + id + "/verify_work.py", lines.join("\n") + "\n");
vw(["def q1():", "    return 'B'", "", "def q2():", "    return chr(65)"]);
r = run("explain", id, "--batch", "1");
expect("explain counts a question done only with both an explanation and a q<n>()", r.code === 0 && /Explained and recomputed: 0 of 3/.test(r.out) && /Next batch: Q1 \(2 more/.test(r.out), r.out);
sheet([keep(1, { answer: "B", keyNote: "The key is wrong because …", explanation: "Because …" }), keep(2, { explanation: "Count …" }),
  { n: 3, page: 2, decision: "repeat", note: "Same as Q2" }, keep(4, { topic: "alpha-t2" })]);
r = run("explain", id);
expect("explain runs the functions, agrees, and lists what is left", r.code === 0 && /2 of 3 kept/.test(r.out) && /Next batch: Q4\s*$/m.test(r.out), r.out);
vw(["def q1():", "    return 'C'", "", "def q2():", "    return 'A'", "", "def q3():", "    return 'A'"]);
r = run("explain", id);
expect("a recomputed answer that disagrees with the worksheet fails", r.code === 1 && /Q1: q1\(\) gives C but the worksheet's answer is B/.test(r.out), r.out);
expect("a function for a question that is not kept is reported", /q3\(\) in verify_work\.py match no kept question/.test(r.out), r.out);
vw(["import json", "A = json.load(open('questions.json'))", "def q1():", "    return 'B'"]);
r = run("explain", id);
expect("verify_work.py may not read the worksheet", r.code === 1 && /may not read the worksheet/.test(r.out), r.out);
vw(["def q1():", "    return 'B'", "", "def q2():", "    return 'A'", "", "def q4():", "    return 'A'"]);
sheet([keep(1, { answer: "B", keyNote: "k", explanation: "e" }), keep(2, { explanation: "e" }), { n: 3, page: 2, decision: "repeat", note: "Same as Q2" }, keep(4, { topic: "alpha-t2", explanation: "e" })]);
r = run("explain", id);
expect("when every kept question is done, explain says to build", r.code === 0 && /All kept questions are explained/.test(r.out), r.out);
sheet([keep(1, { answer: "B", keyNote: "k", explanation: "P(A??B)=1?P(A)" }), keep(2, { explanation: "e" }), { n: 3, page: 2, decision: "repeat", note: "Same as Q2" }, keep(4, { topic: "alpha-t2", explanation: "e" })]);
r = run("explain", id);
expect("an explanation whose symbols were lost as '?' is not done, and says how to save", r.code === 1 && /2 of 3 kept/.test(r.out) && /explanation of Q1: write them again/.test(r.out) && /Next batch: Q1\s*$/m.test(r.out), r.out);
r = run("check", id);
expect("check also rejects lost symbols in an explanation", r.code === 1 && /explanation or notes were lost/.test(r.out), r.out);
sheet([keep(1, { answer: "B", keyNote: "k", explanation: "e" }), keep(2, { explanation: "e" }), { n: 3, page: 2, decision: "repeat", note: "Same as Q2" }, keep(4, { topic: "alpha-t2", explanation: "e" })]);
// build: the bank's two scripts are generated from the worksheet and verify_work.py, then run
w("pyq_bank_common.py", fs.readFileSync(path.join(__dirname, "..", "pyq_bank_common.py"), "utf8"));
w("tools/intake-sources.json", { schema: 1, sources: [] });
r = run("build", id);
expect("build needs a bank name", r.code === 2 && /--name must be/.test(r.out), r.out);
r = run("build", id, "--name", "made_up_quiz");
const built = (() => { try { return JSON.parse(fs.readFileSync(path.join(tmp, "seed", "alpha_made_up_quiz.json"), "utf8")); } catch (e) { return null; } })();
expect("build writes and runs both scripts, and the bank holds every kept question", r.code === 0 && built && built.count === 3 &&
  built.items.map(i => i.id).join() === "made-up-quiz-q001,made-up-quiz-q002,made-up-quiz-q004" && built.items[0].answer === "B" && built.items[0].explanation === "e", r.out);
expect("the generated verifier passes and says what it checked", /Verified 3 answers independently/.test(r.out), r.out);
const reg2 = JSON.parse(fs.readFileSync(path.join(tmp, "tools", "intake-sources", id + ".json"), "utf8"));
expect("build registers the source in a file of its own (no shared file for open PRs to conflict on)",
  reg2.outputs[0] === "seed/alpha_made_up_quiz.json" && reg2.sha256[0] === id + "0".repeat(52) &&
  JSON.parse(fs.readFileSync(path.join(tmp, "tools", "intake-sources.json"), "utf8")).sources.length === 0, JSON.stringify(reg2));
expect("scan sees sources registered in either place", (() => { const R = require(TOOL); return R.classify({ name: "x.pdf", sha256: id + "0".repeat(52), pages: 3, text: "", textChars: 0 }, R.loadRegister(), {}).decision === "skip"; })());
expect("build lists the files for the run's result and writes a PR description with the key differences",
  /files: \["made_up_quiz_bank.py","verify_made_up_quiz.py","seed\/alpha_made_up_quiz.json","tools\/intake-sources\/abcdef012345.json"\]/.test(r.out) &&
  /Q1 \(kept, answer B, key A\)/.test(fs.readFileSync(path.join(ws, "pr-body.md"), "utf8")) && /Q3 \(repeat\)/.test(fs.readFileSync(path.join(ws, "pr-body.md"), "utf8")), r.out);
r = spawnSync("python", ["-X", "utf8", "made_up_quiz_bank.py", "--check"], { cwd: tmp, encoding: "utf8" });
expect("the generated build script's --check agrees with what it wrote", r.status === 0, (r.stdout || "") + (r.stderr || ""));
fs.writeFileSync(path.join(tmp, "seed", "alpha_made_up_quiz.json"), JSON.stringify(Object.assign({}, built, { items: built.items.map((i, k) => k ? i : Object.assign({}, i, { answer: "D" })) })));
r = spawnSync("python", ["-X", "utf8", "verify_made_up_quiz.py"], { cwd: tmp, encoding: "utf8" });
expect("the generated verifier fails on a bank answer its function disagrees with", r.status !== 0 && /AssertionError/.test(r.stderr), (r.stdout || "") + (r.stderr || ""));
sheet([keep(1, { answer: "B", keyNote: "k", explanation: "e" }), keep(2, { explanation: "e", format: "multi", options: undefined, statements: ["s1", "s2", "s3", "s4"], printedKey: "A", answer: "A" }),
  { n: 3, page: 2, decision: "repeat", note: "Same as Q2" }, keep(4, { topic: "alpha-t2", explanation: "e" })]);
r = run("build", id, "--name", "made_up_quiz");
expect("a multiple-correct question needs a reason per statement before build", r.code === 2 && /explain is not finished: 1 kept/.test(r.out), r.out);
// next and put: one batch at a time, saved from UTF-8 files rather than by editing the worksheet
const bf = (name, data) => { const f = path.join(tmp, name); fs.writeFileSync(f, typeof data === "string" ? data : JSON.stringify(data)); return f; };
r = run("put", id, bf("b1.json", { items: [{ n: 2, whys: ["w1", "w2 uses P(Aᶜ ∩ B) = 0.2", "w3", "w4"] }] }), "--verify", bf("b1.py", "from fractions import Fraction\n\ndef q2():\n    return 'A' if Fraction(1, 2) else '?'\n"));
const vw2 = fs.readFileSync(path.join(ws, "verify_work.py"), "utf8");
expect("put merges fields into an item and replaces its q<n>() in verify_work.py, adding the import once",
  r.code === 0 && /Saved 1 item\(s\) and 1 q<n>\(\)/.test(r.out) && /^from fractions import Fraction$/m.test(vw2) && (vw2.match(/^def q2\(/gm) || []).length === 1 && /Fraction\(1, 2\)/.test(vw2) && /^def q4\(/m.test(vw2), r.out + vw2);
expect("the merged worksheet keeps the symbols, and explain now passes", /P\(Aᶜ ∩ B\)/.test(fs.readFileSync(path.join(ws, "questions.json"), "utf8")) && run("explain", id).code === 0, run("explain", id).out);
r = run("put", id, bf("b1h.json", { items: [] }), "--verify", bf("b1h.py", "import math\n\ndef _twice(x):\n    y = x\n    y = y\n    return 2 * y\n\ndef q4():\n    return 'A' if _twice(1) == 2 else '?'\n"));
const vw3 = fs.readFileSync(path.join(ws, "verify_work.py"), "utf8");
expect("put adds a helper whole (a repeated line inside it survives) and puts imports together at the top",
  r.code === 0 && /    y = y\n/.test(vw3) && /^from fractions import Fraction\nimport math$/m.test(vw3) && vw3.indexOf("def _twice") < vw3.indexOf("def q2") && run("explain", id).code === 0, vw3);
r = run("put", id, bf("b2.json", { items: [{ n: 4, explanation: "1?P(A??B)" }] }));
expect("put refuses a batch whose symbols were lost, and writes nothing", r.code === 2 && /lost as '\?' in Q4/.test(r.out) && !/1\?P/.test(fs.readFileSync(path.join(ws, "questions.json"), "utf8")), r.out);
r = run("put", id, bf("b3.json", { items: [{ n: 4, keyNote: null }, { n: 3, note: "Same as Q2 (both ask for the variance)" }] }));
expect("put removes a field given as null and edits a non-kept entry", r.code === 0 && !("keyNote" in JSON.parse(fs.readFileSync(path.join(ws, "questions.json"), "utf8")).items[3]), r.out);
r = run("next", id);
expect("next on a finished worksheet says to build", r.code === 0 && /Nothing left to explain. Next: node tools\/intake.js build/.test(r.out), r.out);
const id2 = "0123456789ab";
w("ws/" + id2 + "/source.json", { schema: 1, id: id2, sha256: id2 + "1".repeat(52), file: "q2.pdf", pages: 4, kind: "questions", title: "Another", imagePages: [] });
w("ws/" + id2 + "/questions.json", { source: id2, covers: { from: 1, to: 40 }, items: [keep(1, { page: 2 }), keep(2, { page: [2, 3] })] });
r = run("next", id2);
expect("next mid-transcription says where to continue and shows only the last entry", r.code === 0 && /2 entries of Q1-Q40/.test(r.out) && /from Q3 \(38 still missing\), starting on page 3 of 4/.test(r.out) && (r.out.match(/"stem"/g) || []).length === 1, r.out);
expect("numeric answers compare as numbers, multi answers as sets",
  T.sameAnswer({ format: "numeric", answer: "1/4" }, "0.25") && T.sameAnswer({ format: "multi", answer: "AC" }, "CA") && !T.sameAnswer({ format: "single", answer: "A" }, "a"));

fs.rmSync(tmp, { recursive: true, force: true });
console.log((total - failed) + "/" + total + " intake checks passed");
process.exit(failed ? 1 : 0);
