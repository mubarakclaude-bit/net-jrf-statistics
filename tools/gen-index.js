#!/usr/bin/env node
/* The lesson index is GENERATED. Nothing commits it and nothing edits it by hand.
 *
 *   node tools/gen-index.js                 write .cache/meta_lessons.generated.json (what gets pushed to the store)
 *   node tools/gen-index.js --check         validate every seed as a set; exit 1 on a real problem
 *   node tools/gen-index.js --expect <topicId> <storeDocId> <masterySetStem>
 *                                           assert one lesson is wired the way an author says it is
 *
 * Problems (exit 1): invalid JSON, missing required fields, duplicate topicId or store doc id.
 * Warnings (printed, exit 0): a quiz pointing at a missing set, a topic missing from the catalog.
 * Older lessons may carry warnings; --expect is strict about the lesson it is given.
 */
const fs = require("fs"), path = require("path");
const { ROOT, buildDocs } = require("./seed-docs");
const args = process.argv.slice(2);
const { docs, seeds, index, problems, warnings } = buildDocs();

const show = (label, list) => list.forEach(x => console.log(label + " " + x));
show("PROBLEM", problems);
if (args.includes("--warnings") || args[0] === "--check") show("warning", warnings);

if (args[0] === "--expect") {
  const [, tid, doc, set] = args;
  const ent = index.topics[tid];
  const fails = [];
  if (!ent) fails.push("topic " + tid + " is not in the generated index: no seed/lesson_*.json has topicId '" + tid + "'");
  else {
    if (ent.id !== doc) fails.push("store doc id is '" + ent.id + "' but you passed '" + doc + "'");
    const lesson = docs["lessons/" + ent.id];
    const quiz = lesson && lesson.scenes.find(s => s.kind === "quiz");
    if (!quiz) fails.push("lesson has no quiz scene");
    else if (quiz.setId !== set) fails.push("quiz scene points at '" + quiz.setId + "' but you passed '" + set + "'");
    if (!docs["qsets/" + set]) fails.push("seed/" + set + ".json is not a question set");
    else if (docs["qsets/" + set].items.length !== 20) fails.push("pool " + set + " has " + docs["qsets/" + set].items.length + " items, expected 20");
  }
  if (problems.length) fails.push("the seed set has problems (above)");
  if (fails.length) { fails.forEach(f => console.log("FAILED: " + f)); process.exit(1); }
  console.log("indexed " + tid + ": " + ent.estMin + " min, " + ent.scenes + " scenes | store doc lessons/" + ent.id + ", qset " + set + " | generated index has " + index.count + " lessons");
  process.exit(0);
}

if (args[0] === "--check") {
  console.log((problems.length ? "FAILED: " + problems.length + " problem(s)" : "clean: " + index.count + " lessons, " +
    Object.keys(docs).filter(k => k.startsWith("qsets/")).length + " question sets, index generated from the seeds") +
    (warnings.length ? " (" + warnings.length + " warning(s))" : ""));
  process.exit(problems.length ? 1 : 0);
}

fs.mkdirSync(path.join(ROOT, ".cache"), { recursive: true });
const out = path.join(ROOT, ".cache", "meta_lessons.generated.json");
fs.writeFileSync(out, JSON.stringify(index, null, 1));
console.log("wrote .cache/meta_lessons.generated.json: " + index.count + " lessons" + (problems.length ? " (with " + problems.length + " problem(s))" : ""));
process.exit(problems.length ? 1 : 0);
