#!/usr/bin/env node
/* Topic-driven lesson workflow. An author names ONE thing, the topic id, and everything else is derived from the repository.
 * Nothing here touches the Claude artifact: a lesson is published by merging its seed files, and Vercel builds the site.
 *
 *   node tools/lesson.js queue [module]    the topics still to write, in catalog order (default: every module)
 *   node tools/lesson.js brief <topicId>   the work order: wiring, files to produce, neighbour to match, previous-year items
 *   node tools/lesson.js check <topicId>   one command that runs every validator on that topic's files and says what is left
 *
 * The wiring a lesson needs used to be five positional arguments to addlesson.sh (a store document id, a pool stem, ...), which
 * authors got wrong. They are derived instead:
 *   lesson id   = topic id without the dash         nonparam-t1  -> nonparamt1
 *   pool stem   = <module>_t<n>_mastery             nonparam-t1  -> nonparam_t1_mastery
 *   seed stem   = lesson_<module>_t<n>              (an existing file for the topic wins, so lesson_np4 stays lesson_np4)
 */
const fs = require("fs"), path = require("path"), cp = require("child_process");
const { ROOT, SEED, listSeeds, readSeed } = require("./seed-docs");

function load() {
  const cat = readSeed("catalog.json");
  const topics = {};
  for (const m of cat.modules) (m.topics || []).forEach((t, i) => { topics[t.id] = Object.assign({}, t, { moduleId: m.id, moduleName: m.name, order: i }); });
  const seeds = listSeeds();
  const byTopic = {};
  for (const l of seeds.lessons) if (l.data && l.data.topicId) byTopic[l.data.topicId] = l;
  const pools = Object.fromEntries(seeds.qsets.map(q => [q.stem, q]));
  return { cat, topics, byTopic, pools, seeds };
}

/* The derived wiring for a topic. */
function wiring(topicId, L) {
  const t = L.topics[topicId];
  if (!t) return null;
  const n = (topicId.match(/-t(\d+)$/) || [])[1] || "";
  const existing = L.byTopic[topicId];
  return {
    topicId, moduleId: t.moduleId, name: t.name,
    docId: existing ? existing.data.id : topicId.replace(/-/g, ""),
    seedStem: existing ? existing.stem : "lesson_" + t.moduleId + "_t" + n,
    poolStem: existing ? ((existing.data.scenes.find(s => s.kind === "quiz") || {}).setId || t.moduleId + "_t" + n + "_mastery") : t.moduleId + "_t" + n + "_mastery",
    exists: !!existing
  };
}

function need(topicId, L) {
  const w = wiring(topicId, L);
  if (!w) {
    const near = Object.keys(L.topics).filter(k => k.startsWith((topicId || "").split("-")[0])).slice(0, 12);
    console.error("FAILED: '" + topicId + "' is not a topic in seed/catalog.json." + (near.length ? " Topics that start the same way: " + near.join(", ") : ""));
    process.exit(2);
  }
  return w;
}

function questionsFor(moduleId, L) {
  const f = moduleId + "_pyq_variants";
  return L.pools[f] ? L.pools[f].data.items : [];
}

/* ---------------------------------------------------------------- queue */
function queue(moduleId) {
  const L = load();
  const rows = Object.values(L.topics).filter(t => (!moduleId || t.moduleId === moduleId) && !L.byTopic[t.id])
    .sort((a, b) => (b.marks || 0) - (a.marks || 0) || a.id.localeCompare(b.id, undefined, { numeric: true }));
  if (!rows.length) { console.log("nothing to write" + (moduleId ? " in " + moduleId : "") + ": every topic has a lesson"); return 0; }
  const done = Object.values(L.topics).filter(t => (!moduleId || t.moduleId === moduleId) && L.byTopic[t.id]).length;
  console.log((moduleId || "all modules") + ": " + done + " written, " + rows.length + " to write (highest-marks first)\n");
  for (const t of rows) console.log(t.id.padEnd(22) + String(t.marks != null ? t.marks : "").padEnd(6) + t.name);
  return 0;
}

/* ---------------------------------------------------------------- brief */
function brief(topicId) {
  const L = load(), w = need(topicId, L), t = L.topics[topicId];
  const mod = L.cat.modules.find(m => m.id === w.moduleId);
  console.log("WORK ORDER: " + topicId + " — " + t.name);
  console.log("module " + w.moduleId + " (" + mod.name + ", " + mod.marks + " marks) | extent " + t.extent + " | importance " + t.imp + " | expected marks " + t.marks);
  console.log(w.exists ? "STATUS: a lesson exists (" + w.seedStem + ".json). Edit that JSON directly; do not regenerate it.\n" : "STATUS: no lesson yet.\n");
  console.log("Files this task owns (and nothing else):");
  console.log("  seed/" + w.seedStem + ".json          the lesson   (id '" + w.docId + "', topicId '" + w.topicId + "', moduleId '" + w.moduleId + "')");
  console.log("  seed/" + w.poolStem + ".json           the 20-item mastery pool; the lesson's quiz scene has setId '" + w.poolStem + "'");
  console.log("  verify_" + w.moduleId + "_t" + (topicId.match(/(\d+)$/) || [])[1] + ".py    the verification script: every number in the lesson is computed here");
  console.log("  (optional) " + w.seedStem + ".py   the authoring script, from lessons/TEMPLATE.py; GitHub-only sessions may write the JSON directly\n");

  const sibs = Object.values(L.topics).filter(x => x.moduleId === w.moduleId && x.id !== topicId && L.byTopic[x.id]);
  const style = sibs[0] || Object.values(L.topics).find(x => L.byTopic[x.id]);
  if (style) console.log("Match the prose style of one finished lesson (read it for style only, not for shape): seed/" + L.byTopic[style.id].stem + ".json\n");

  const items = questionsFor(w.moduleId, L);
  if (items.length) {
    console.log("Previous-year questions for this module (" + items.length + " in seed/" + w.moduleId + "_pyq_variants.json). These are the specification;");
    console.log("read each full stem, and several are filed under the wrong module. Never write the candidate's marked answer into prose:");
    for (const it of items) console.log("  " + it.id + "  Q" + (it.srcQ != null ? it.srcQ : "?") + "  " + String(it.stem).replace(/\s+/g, " ").slice(0, 110));
    console.log("");
  } else console.log("No previous-year variant bank for this module (seed/" + w.moduleId + "_pyq_variants.json is absent).\n");

  const n = (topicId.match(/(\d+)$/) || [])[1];
  console.log("Steps");
  console.log("  1. Read SPEC.md (house standard) and docs/CONTENT_GUIDE.md. Take the shape from lessons/TEMPLATE.py.");
  console.log("  2. Write verify_" + w.moduleId + "_t" + n + ".py BEFORE any prose; compute every figure.");
  console.log("  3. Write the lesson and the pool with the ids above.");
  console.log("  4. node tools/lesson.js check " + topicId + "      (or push: CI runs the same checks on the PR)");
  console.log("  5. One commit with every file, branch lesson/" + topicId + ", draft PR into the production branch. Merging publishes it.");
  return 0;
}

/* ---------------------------------------------------------------- check */
function run(label, cmd, args) {
  const r = cp.spawnSync(cmd, args, { cwd: ROOT, encoding: "utf8" });
  const out = ((r.stdout || "") + (r.stderr || "")).trim();
  const ok = r.status === 0 && !/^FAILED/m.test(out);
  console.log((ok ? "PASS " : "FAIL ") + label);
  if (!ok && out) console.log(out.split("\n").slice(0, 25).map(l => "     " + l).join("\n"));
  return ok;
}

function check(topicId) {
  const L = load(), w = need(topicId, L);
  if (!w.exists) {
    console.log("FAIL no seed has topicId '" + topicId + "' yet. Expected seed/" + w.seedStem + ".json with id '" + w.docId + "'. Run: node tools/lesson.js brief " + topicId);
    return 1;
  }
  const lesson = L.byTopic[topicId].data;
  const quiz = lesson.scenes.find(s => s.kind === "quiz");
  const results = [];
  const pool = quiz && L.pools[quiz.setId];
  results.push(["lesson has a quiz scene", !!quiz]);
  results.push(["quiz points at an existing pool (seed/" + (quiz ? quiz.setId : "?") + ".json)", !!pool]);
  results.push(["pool has 20 items", !!pool && pool.data.items.length === 20]);
  for (const [l, ok] of results) console.log((ok ? "PASS " : "FAIL ") + l);
  let ok = results.every(r => r[1]);
  const py = process.env.PYBIN || (cp.spawnSync("python3", ["-c", "import sys;sys.exit(0 if sys.version_info[0]==3 else 1)"]).status === 0 ? "python3" : "python");
  const file = "seed/" + w.seedStem + ".json";
  ok = run("vcheck.js (house standard)", "node", ["vcheck.js", file]) && ok;
  ok = run("audit-lesson.py (formulas render, answers not self-cited, answer keys spread)", py, ["-I", "tools/audit-lesson.py", file]) && ok;
  if (quiz) ok = run("generated index wiring", "node", ["tools/gen-index.js", "--expect", topicId, lesson.id, quiz.setId]) && ok;
  ok = run("contracts for this topic's lesson and pool (the whole seed set is checked by npm run check)", "node", ["tools/validate-contracts.js", "--files", file].concat(quiz ? ["seed/" + quiz.setId + ".json"] : [])) && ok;
  const verifier = path.join(ROOT, "verify_" + w.moduleId + "_t" + (topicId.match(/(\d+)$/) || [])[1] + ".py");
  const anyVerifier = fs.readdirSync(ROOT).some(f => /^verify_.*\.py$/.test(f) && fs.readFileSync(path.join(ROOT, f), "utf8").includes(topicId.replace("-", "_")) );
  console.log((fs.existsSync(verifier) || anyVerifier ? "PASS " : "WARN ") + "a verification script covers this topic" + (fs.existsSync(verifier) || anyVerifier ? "" : " (expected " + path.basename(verifier) + ")"));
  console.log(ok ? "\nREADY: open the PR; CI repeats these checks." : "\nNOT READY: fix the FAIL lines above.");
  return ok ? 0 : 1;
}

if (require.main === module) {
  const [cmd, arg] = process.argv.slice(2);
  let code = 0;
  if (cmd === "queue") code = queue(arg);
  else if (cmd === "brief" && arg) code = brief(arg);
  else if (cmd === "check" && arg) code = check(arg);
  else { console.error("usage: node tools/lesson.js queue [module] | brief <topicId> | check <topicId>"); code = 2; }
  process.exit(code);
}
module.exports = { wiring, load };
