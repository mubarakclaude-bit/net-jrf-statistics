#!/usr/bin/env node
/* Tests tools/check-ids.js in a throwaway git repository, so each rule is checked against a known answer.
 *   node tests/check-ids.test.js                                                                                  */
const fs = require("fs"), os = require("os"), path = require("path"), { execFileSync, spawnSync } = require("child_process");
const TOOL = path.join(__dirname, "..", "tools", "check-ids.js");
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "ids-test-"));
const git = (...a) => execFileSync("git", ["-C", dir, ...a], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
const w = (rel, data) => { const f = path.join(dir, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, typeof data === "string" ? data : JSON.stringify(data, null, 1)); };
const run = () => { const r = spawnSync(process.execPath, [TOOL, "base"], { env: Object.assign({}, process.env, { IDS_ROOT: dir }), encoding: "utf8" }); return { code: r.status, out: (r.stdout || "") + (r.stderr || "") }; };
let failed = 0, total = 0;
const expect = (name, ok, detail) => { total++; if (!ok) { failed++; console.log("FAIL " + name + (detail ? "  — " + String(detail).slice(0, 220) : "")); } else console.log("ok   " + name); };

const lesson = (over) => Object.assign({ id: "alphat1", topicId: "alpha-t1", moduleId: "alpha", title: "T", version: "1", status: "approved", estMin: 5,
  scenes: [{ id: "s0", kind: "foundation", title: "a" }, { id: "s1", kind: "theory", title: "b" }, { id: "s2", kind: "quiz", setId: "alpha_t1_mastery" }] }, over || {});
const pool = (ids, over) => Object.assign({ moduleId: "alpha", items: ids.map(i => ({ id: i, answer: "A", stem: "s" })) }, over || {});
const reset = () => { git("checkout", "-q", "base"); git("checkout", "-q", "-B", "work"); };

git("init", "-q", "-b", "base"); git("config", "user.email", "t@t"); git("config", "user.name", "t");
w("seed/lesson_a1.json", lesson()); w("seed/alpha_t1_mastery.json", pool(["q1", "q2", "q3"])); w("seed/catalog.json", { modules: [] });
git("add", "-A"); git("commit", "-q", "-m", "base");
git("checkout", "-q", "-b", "work");
const commit = () => { git("add", "-A"); git("commit", "-q", "-m", "change", "--allow-empty"); };

let r = (commit(), run());
expect("no change: passes", r.code === 0 && /no id lost/.test(r.out), r.out);

w("seed/lesson_a1.json", lesson({ title: "Edited", version: "2", scenes: [{ id: "s0", kind: "foundation", title: "new words" }, { id: "s1", kind: "theory" }, { id: "s2", kind: "quiz", setId: "alpha_t1_mastery" }, { id: "s3", kind: "summary" }] }));
w("seed/alpha_t1_mastery.json", pool(["q1", "q2", "q3", "q4"])); w("seed/lesson_new.json", lesson({ id: "other", topicId: "alpha-t2" })); w("seed/catalog.json", { modules: [{ id: "x" }] });
r = (commit(), run());
expect("editing text, adding a scene, a question and a new lesson, and changing the catalog: passes", r.code === 0, r.out);

reset(); w("seed/lesson_a1.json", lesson({ scenes: [{ id: "s0", kind: "foundation" }, { id: "s2", kind: "quiz", setId: "alpha_t1_mastery" }] }));
r = (commit(), run());
expect("removing a scene id fails, names the scene", r.code === 1 && /scene 's1'/.test(r.out) && /seen/.test(r.out), r.out);

reset(); w("seed/alpha_t1_mastery.json", pool(["q1", "q3"]));
r = (commit(), run());
expect("removing a question id fails, names the question", r.code === 1 && /question 'q2'/.test(r.out), r.out);

reset(); w("seed/lesson_a1.json", lesson({ id: "renamed" }));
r = (commit(), run());
expect("changing the lesson id fails", r.code === 1 && /lesson id changed from 'alphat1' to 'renamed'/.test(r.out), r.out);

reset(); w("seed/lesson_a1.json", lesson({ topicId: "alpha-t9" }));
r = (commit(), run());
expect("changing the topicId fails", r.code === 1 && /topicId changed/.test(r.out), r.out);

reset(); fs.unlinkSync(path.join(dir, "seed", "alpha_t1_mastery.json"));
r = (commit(), run());
expect("deleting a question set fails", r.code === 1 && /deleted \(or renamed\)/.test(r.out), r.out);

reset(); git("mv", "seed/lesson_a1.json", "seed/lesson_renamed.json");
r = (commit(), run());
expect("renaming a lesson file fails (its store document would move)", r.code === 1 && /deleted \(or renamed\)/.test(r.out), r.out);

reset(); w("seed/alpha_t1_mastery.json", Object.assign(pool(["q1", "q2", "q3"]), { items: [{ id: "q1", answer: "B" }, { id: "q2", answer: "A" }, { id: "q3", answer: "A" }] }));
r = (commit(), run());
expect("changing an answer key is allowed, with a note", r.code === 0 && /q1' answer key changed A -> B/.test(r.out), r.out);

reset(); w("seed/lesson_a1.json", lesson({ scenes: [{ id: "s0", kind: "foundation" }, { id: "s2", kind: "quiz", setId: "alpha_t1_mastery" }] }));
w("contracts/id-exceptions.json", { removed: [{ file: "seed/lesson_a1.json", ids: ["s1"], reason: "merged into s0" }] });
r = (commit(), run());
expect("a removal the owner listed in contracts/id-exceptions.json passes", r.code === 0, r.out);

reset(); fs.unlinkSync(path.join(dir, "seed", "alpha_t1_mastery.json"));
w("contracts/id-exceptions.json", { removed: [{ file: "seed/alpha_t1_mastery.json", ids: ["*"], reason: "replaced" }] });
r = (commit(), run());
expect("a whole-file removal is excused only by an explicit * entry", r.code === 0, r.out);

reset(); w("seed/lesson_a1.json", lesson({ scenes: [{ id: "s0", kind: "foundation" }, { id: "s2", kind: "quiz", setId: "alpha_t1_mastery" }] }));
w("contracts/id-exceptions.json", { removed: [{ file: "seed/lesson_other.json", ids: ["s1"], reason: "wrong file" }] });
r = (commit(), run());
expect("an exception for a different file does not excuse it", r.code === 1, r.out);

fs.rmSync(dir, { recursive: true, force: true });
console.log("\n" + total + " checks, " + failed + " failed");
process.exit(failed ? 1 : 0);
