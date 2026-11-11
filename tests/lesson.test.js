#!/usr/bin/env node
/* tools/lesson.js against real seeds: derived wiring, queue, brief and check exit codes. */
const cp = require("child_process"), path = require("path"), assert = require("assert");
const ROOT = path.join(__dirname, ".."), run = a => cp.spawnSync("node", ["tools/lesson.js", ...a], { cwd: ROOT, encoding: "utf8" });
const { wiring, load } = require("../tools/lesson");
const L = load();
const unwritten = Object.keys(L.topics).find(id => !L.byTopic[id]);
assert(unwritten, "fixture needs at least one unwritten syllabus topic");
const topic = L.topics[unwritten], match = unwritten.match(/-t(\d+)$/), nTopic = match ? match[1] : "";
const expected = [unwritten.replace(/-/g, ""), "lesson_" + topic.moduleId + "_t" + nTopic, topic.moduleId + "_t" + nTopic + "_mastery", false];
let n = 0; const t = (name, f) => { f(); n++; };

t("an unwritten topic gets convention-derived wiring", () => {
  const w = wiring(unwritten, L);
  assert.deepStrictEqual([w.docId, w.seedStem, w.poolStem, w.exists], expected);
});
t("a written topic keeps its existing names", () => {
  const w = wiring("nonparam-t4", L);
  assert.deepStrictEqual([w.docId, w.seedStem, w.poolStem, w.exists], ["nonparamt4", "lesson_np4", "nonparam_t4_mastery", true]);
});
t("an unknown topic is refused with exit 2", () => assert.strictEqual(run(["brief", "nope-t9"]).status, 2));
t("the queue includes an unwritten topic and omits the written one", () => {
  const r = run(["queue", topic.moduleId]); assert.strictEqual(r.status, 0);
  assert(r.stdout.includes(unwritten) && !r.stdout.includes("nonparam-t4"));
});
t("the brief names the derived files for an unwritten topic", () => {
  const o = run(["brief", unwritten]).stdout;
  for (const s of ["seed/" + expected[1] + ".json", "seed/" + expected[2] + ".json", "verify_" + topic.moduleId + "_t" + nTopic + ".py", "lesson/" + unwritten]) assert(o.includes(s), s);
});
t("check fails for an unwritten topic and passes for a finished one", () => {
  assert.strictEqual(run(["check", unwritten]).status, 1);
  assert.strictEqual(run(["check", "nonparam-t4"]).status, 0);
});
console.log("lesson tool: " + n + " checks passed");
