#!/usr/bin/env node
/* tools/lesson.js against the real seeds: derived wiring, the queue, the brief, and check's exit codes. */
const cp = require("child_process"), path = require("path"), assert = require("assert");
const ROOT = path.join(__dirname, ".."), run = a => cp.spawnSync("node", ["tools/lesson.js", ...a], { cwd: ROOT, encoding: "utf8" });
const { wiring, load } = require("../tools/lesson");
const L = load();
let n = 0; const t = (name, f) => { f(); n++; };

t("an unwritten topic gets the convention", () => {
  const w = wiring("nonparam-t1", L);
  assert.deepStrictEqual([w.docId, w.seedStem, w.poolStem, w.exists], ["nonparamt1", "lesson_nonparam_t1", "nonparam_t1_mastery", false]);
});
t("a written topic keeps its existing names", () => {
  const w = wiring("nonparam-t4", L);
  assert.deepStrictEqual([w.docId, w.seedStem, w.poolStem, w.exists], ["nonparamt4", "lesson_np4", "nonparam_t4_mastery", true]);
});
t("an unknown topic is refused with exit 2", () => assert.strictEqual(run(["brief", "nope-t9"]).status, 2));
t("the queue omits written topics", () => {
  const r = run(["queue", "nonparam"]); assert.strictEqual(r.status, 0);
  assert(/nonparam-t1/.test(r.stdout) && !/nonparam-t4/.test(r.stdout));
});
t("the brief names every file the task owns", () => {
  const o = run(["brief", "nonparam-t2"]).stdout;
  for (const s of ["seed/lesson_nonparam_t2.json", "seed/nonparam_t2_mastery.json", "verify_nonparam_t2.py", "lesson/nonparam-t2"]) assert(o.includes(s), s);
});
t("check fails for an unwritten topic and passes for a finished one", () => {
  assert.strictEqual(run(["check", "nonparam-t1"]).status, 1);
  assert.strictEqual(run(["check", "nonparam-t4"]).status, 0);
});
console.log("lesson tool: " + n + " checks passed");
