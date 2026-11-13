#!/usr/bin/env node
/* Tests tools/content.js against a small made-up content set, so each claim it makes is checked against a known answer:
 * the join from catalog to lesson to pool to June question, the gaps it reports, and the problems `check` must catch.
 *   node tests/content.test.js
 * It never touches the real seed/ (the tool reads CONTENT_ROOT). */
const fs = require("fs"), os = require("os"), path = require("path"), { spawnSync } = require("child_process");
const TOOL = path.join(__dirname, "..", "tools", "content.js");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "content-test-"));
const w = (rel, data) => { const f = path.join(tmp, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, typeof data === "string" ? data : JSON.stringify(data)); };
const run = (...args) => { const r = spawnSync(process.execPath, [TOOL, ...args], { env: Object.assign({}, process.env, { CONTENT_ROOT: tmp }), encoding: "utf8" }); return { code: r.status, out: (r.stdout || "") + (r.stderr || "") }; };
let failed = 0, total = 0;
const expect = (name, ok, detail) => { total++; if (!ok) { failed++; console.log("FAIL " + name + (detail ? "  — " + String(detail).slice(0, 200) : "")); } else console.log("ok   " + name); };

const item = (id, ans, extra) => Object.assign({ id, format: "single", topic: "t", diff: "easy", stem: "stem " + id, options: ["a", "b", "c", "d"], answer: ans, explanation: "e" }, extra || {});
w("seed/catalog.json", { updated: "x", modules: [{ id: "alpha", paper: 2, name: "Alpha", marks: 10, order: 1, baseline: "1/5", passPct: 80, targetQ: 20,
  topics: [{ id: "alpha-t1", name: "First", extent: "Derive", imp: 3, qs: 1, marks: 6 }, { id: "alpha-t2", name: "Second", extent: "State", imp: 1, qs: 1, marks: 4 }] }] });
w("seed/meta_syllabus.json", { cycle: "c", source: "s", note: "n", order: { alpha: 1 }, units: { alpha: { no: "1", title: "Alpha", label: "Unit 1" } }, updated: "x" });
w("seed/lesson_a1.json", { id: "alphat1", topicId: "alpha-t1", moduleId: "alpha", title: "First lesson", version: "2.0", status: "approved", estMin: 60,
  objectives: ["Explain the widget"], traps: ["Confusing widgets"], prereq: [], provenance: "Anchor: Q2, and Q3.", scenes: [{ kind: "theory", id: "s1" }, { kind: "quiz", id: "s2", setId: "alpha_t1_mastery" }] });
w("seed/alpha_t1_mastery.json", { moduleId: "alpha", topicId: "alpha-t1", count: 12, items: Array.from({ length: 12 }, (_, i) => item("m" + i, "ABC"[i % 3])) }); // never D: a spread problem
w("seed/pyq_j26_full.json", { moduleId: "x", source: "pyq", count: 3, items: [
  item("j26-q01", "A", { topic: "June 2026 Paper 2 · Q1", youMarked: "A", paper: 2 }),
  item("j26-q02", "B", { topic: "June 2026 Paper 2 · Q2", youMarked: "C", paper: 2 }),
  item("j26-q03", "D", { topic: "June 2026 Paper 2 · Q3", youMarked: "D", paper: 2 })] });
w("seed/alpha_pyq_variants.json", { moduleId: "alpha", count: 1, items: [item("j26v-q02-01", "A", { srcQ: 2 })] });
w("lesson_a1.py", 'OUT = "seed/lesson_a1.json"\n');
w("verify_alpha.py", '# checks the numbers for "alpha-t1"\n');

let r = run("check");
expect("check passes on consistent content", r.code === 0 && /agree \(1 lessons, 2 topics\)/.test(r.out), r.out);

r = run("map", "--out", path.join(tmp, "out"));
const md = fs.existsSync(path.join(tmp, "out", "CONTENT_MAP.md")) ? fs.readFileSync(path.join(tmp, "out", "CONTENT_MAP.md"), "utf8") : "";
const js = fs.existsSync(path.join(tmp, "out", "content-map.json")) ? JSON.parse(fs.readFileSync(path.join(tmp, "out", "content-map.json"), "utf8")) : {};
expect("the map is written", r.code === 0 && md.length > 200 && js.modules, r.out);
expect("it counts 1 lesson of 2 topics", /\*\*1 lessons\*\* cover \*\*1 of 2 catalog topics\*\*/.test(md), md.split("\n").slice(5, 9).join(" | "));
expect("marks without a lesson are the uncovered topic's 4", js.modules && js.modules[0].exposedMarks === 4, js.modules && js.modules[0].exposedMarks);
const t1 = js.modules && js.modules[0].topics[0];
expect("the lesson is joined to its pool, authoring script and verification script",
  t1 && t1.lesson.id === "alphat1" && t1.pool.count === 12 && t1.authoring === "lesson_a1.py" && t1.verification[0] === "verify_alpha.py", JSON.stringify(t1 && { a: t1.authoring, v: t1.verification }));
expect("anchors are read from the provenance text as paper j26 (Q2 and Q3), marked as prose", t1 && JSON.stringify(t1.lesson.anchors.map(a => a.paper + ":" + a.q + ":" + a.via)) === JSON.stringify(["j26:2:prose", "j26:3:prose"]), t1 && JSON.stringify(t1.lesson.anchors));
const q = (js.papers && js.papers.j26 && js.papers.j26.questions) || [];
expect("a June question the candidate got wrong is flagged, and one that was right is not", q.find(x => x.n === 2).wrong === true && q.find(x => x.n === 3).wrong === false);
expect("a question named by the lesson and one with a variant bank are both recorded", q.find(x => x.n === 2).lessons[0] === "alpha-t1" && q.find(x => x.n === 2).variantBanks[0] === "alpha_pyq_variants");
expect("Q1 has neither, so it is a gap", js.gaps.papers.j26.some(x => x.n === 1) && !js.gaps.papers.j26.some(x => x.n === 3));
expect("gaps list the topic with no lesson", js.gaps.topics.length === 1 && js.gaps.topics[0].id === "alpha-t2");
expect("gaps flag a pool whose answer keys never include D, and one that is not 20 items",
  js.gaps.pools.some(x => /fewer than 2/.test(x.issue)) && js.gaps.pools.some(x => /standard is 20/.test(x.issue)), JSON.stringify(js.gaps.pools));

r = run("topic", "alpha-t1");
expect("topic prints where the lesson, script and pool live", /seed\/lesson_a1\.json/.test(r.out) && /lesson_a1\.py/.test(r.out) && /seed\/alpha_t1_mastery\.json/.test(r.out) && /j26 Q2 \(answered wrongly\)/.test(r.out), r.out);
r = run("topic", "nope");
expect("an unknown topic says so and points to the next step", /No topic 'nope'/.test(r.out));
r = run("pyq", "2");
expect("pyq shows the key and what was marked", /key B, candidate marked C/.test(r.out) && /answered wrongly/.test(r.out), r.out);
r = run("search", "widget");
expect("search finds a word in a lesson objective", /seed\/lesson_a1\.json/.test(r.out) && /widget/i.test(r.out), r.out);

// a second past paper, a lesson that names it through the machine-readable anchors field, and a variant bank made from it
w("seed/pyq_d25_full.json", { moduleId: "x", source: "pyq", label: "December 2025 test paper", count: 2, items: [
  item("d25-q01", "C", { topic: "December 2025 Paper 2 \u00b7 Q1", youMarked: "B", paper: 2 }),
  item("d25-q02", "D", { topic: "December 2025 Paper 2 \u00b7 Q2", youMarked: "D", paper: 2 })] });
w("seed/alpha_pyq_variants.json", { moduleId: "alpha", count: 2, items: [item("j26v-q02-01", "A", { srcQ: 2 }), item("d25v-q01-01", "B", { srcPaper: "d25", srcQ: 1 })] });
const L1 = JSON.parse(fs.readFileSync(path.join(tmp, "seed", "lesson_a1.json"), "utf8")); L1.anchors = [{ paper: "d25", q: 2 }, { paper: "j26", q: 2 }];
w("seed/lesson_a1.json", L1);
r = run("check");
expect("check passes with two papers, anchors and srcPaper", r.code === 0, r.out);
r = run("papers");
expect("papers lists both, found by file name", /j26 /.test(r.out) && /d25 /.test(r.out) && /December 2025 test paper/.test(r.out) && /seed\/pyq_d25_full\.json/.test(r.out), r.out);
run("map", "--out", path.join(tmp, "out2"));
const js2 = JSON.parse(fs.readFileSync(path.join(tmp, "out2", "content-map.json"), "utf8")), md2 = fs.readFileSync(path.join(tmp, "out2", "CONTENT_MAP.md"), "utf8");
const dq = js2.papers.d25.questions;
expect("the map holds each paper separately", Object.keys(js2.papers).sort().join() === "d25,j26" && dq.length === 2);
expect("a lesson's anchors field names the second paper's question 2, and it is recorded", dq.find(x => x.n === 2).lessons[0] === "alpha-t1", JSON.stringify(dq));
expect("a variant bank's srcPaper links its item to the second paper's question 1; the same number in paper j26 is untouched",
  dq.find(x => x.n === 1).variantBanks[0] === "alpha_pyq_variants" && !js2.papers.j26.questions.find(x => x.n === 1).variantBanks.length, JSON.stringify(dq));
expect("an anchor from the field wins over the same paper's prose, and prose still counts as j26", (() => { const a = js2.modules[0].topics[0].lesson.anchors; return a.find(x => x.paper === "d25" && x.q === 2).via === "field" && a.find(x => x.paper === "j26" && x.q === 3).via === "prose" && a.find(x => x.paper === "j26" && x.q === 2).via === "field"; })(), JSON.stringify(js2.modules[0].topics[0].lesson.anchors));
expect("the readable map has a section for each paper", /## Past paper `j26`/.test(md2) && /## Past paper `d25`/.test(md2) && /d25 Q2/.test(md2), md2.split("\n").filter(l => /^## /.test(l)).join(" | "));
expect("gaps are listed per paper, and the wrongly answered one comes first", js2.gaps.papers.d25[0].n === 1 && js2.gaps.papers.d25[0].wrong === true, JSON.stringify(js2.gaps.papers.d25));
r = run("pyq", "d25", "1");
expect("pyq <paper> <n> shows the second paper's question and what was marked", /d25 Q1/.test(r.out) && /key C, candidate marked B/.test(r.out) && /answered wrongly/.test(r.out), r.out);
r = run("pyq", "9", "9");
expect("an unknown paper is named, with the papers that do exist", run("pyq", "zzz", "1").code === 1 && /No paper 'zzz'. Papers: /.test(run("pyq", "zzz", "1").out) && r.code === 1);

// what `check` must catch about papers and anchors
const keep = JSON.parse(JSON.stringify(L1));
const bad1 = (name, mutate, re) => { const L = JSON.parse(JSON.stringify(keep)); mutate(L); w("seed/lesson_a1.json", L); const x = run("check"); expect(name, x.code === 1 && re.test(x.out), x.out); w("seed/lesson_a1.json", keep); };
bad1("check fails when a lesson anchors a paper that does not exist", L => { L.anchors = [{ paper: "zzz", q: 1 }]; }, /names paper 'zzz'/);
bad1("check fails when a lesson anchors a question that is not in the paper", L => { L.anchors = [{ paper: "d25", q: 77 }]; }, /question 77 of 'd25'/);
bad1("check fails on an anchor that is malformed", L => { L.anchors = [{ paper: "d25", q: "two" }]; }, /anchors\[0\] must look like/);
bad1("check fails when anchors is not an array", L => { L.anchors = "d25 Q1"; }, /anchors must be an array/);
w("seed/alpha_pyq_variants.json", { moduleId: "alpha", count: 1, items: [item("v1", "A", { srcPaper: "nope", srcQ: 1 })] });
r = run("check");
expect("check fails when a variant bank's srcPaper does not exist", r.code === 1 && /paper 'nope' \(srcPaper\)/.test(r.out), r.out);
w("seed/alpha_pyq_variants.json", { moduleId: "alpha", count: 1, items: [item("v1", "A", { srcPaper: "d25", srcQ: 40 })] });
r = run("check");
expect("check fails when srcQ is not a question of that paper", r.code === 1 && /question 40 of paper 'd25'/.test(r.out), r.out);
w("seed/alpha_pyq_variants.json", { moduleId: "alpha", count: 1, items: [item("j26v-q02-01", "A", { srcQ: 2 })] });
const d25 = JSON.parse(fs.readFileSync(path.join(tmp, "seed", "pyq_d25_full.json"), "utf8"));
w("seed/pyq_d25_full.json", Object.assign({}, d25, { source: "mastery" }));
r = run("check");
expect("check fails when a paper file is not marked source pyq (that mark is what keeps the candidate's answers out of the public build)", r.code === 1 && /must have "source": "pyq"/.test(r.out), r.out);
w("seed/pyq_d25_full.json", Object.assign({}, d25, { items: [d25.items[0], Object.assign({}, d25.items[1], { id: "d25-q01", topic: "December 2025 Paper 2 \u00b7 Q1" })] }));
r = run("check");
expect("check fails when two questions of a paper have the same number", r.code === 1 && /question number 1 appears twice/.test(r.out), r.out);
w("seed/pyq_d25_full.json", d25);
w("seed/lesson_a1.json", keep);

// problems `check` must catch
w("seed/lesson_bad.json", { id: "badlesson", topicId: "no-such-topic", moduleId: "alpha", title: "Bad", version: "1", status: "approved", estMin: 5, scenes: [{ kind: "theory", id: "x" }] });
r = run("check");
expect("check fails, with a reason, on a lesson whose topic is not in the catalog", r.code === 1 && /no-such-topic/.test(r.out) && /not in seed\/catalog\.json/.test(r.out), r.out);
fs.unlinkSync(path.join(tmp, "seed", "lesson_bad.json"));
w("seed/alpha_pyq_variants.json", { moduleId: "alpha", count: 1, items: [item("j26v-q99-01", "A", { srcQ: 99 })] });
r = run("check");
expect("check fails when a variant bank names a June question that does not exist", r.code === 1 && /question 99/.test(r.out), r.out);
w("seed/alpha_pyq_variants.json", "{ not json");
r = run("check");
expect("check fails on a seed file that is not valid JSON", r.code === 1 && /not valid JSON/.test(r.out), r.out);

fs.rmSync(tmp, { recursive: true, force: true });
console.log("\n" + total + " checks, " + failed + " failed");
process.exit(failed ? 1 : 0);
