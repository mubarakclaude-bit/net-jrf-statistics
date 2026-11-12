#!/usr/bin/env node
/* Decides how much of the lesson click-test a pull request needs, so the cost stops growing with every lesson.
 *
 *   node tools/changed-topics.js <base-ref-or-sha>
 *
 * Prints one line:
 *   FULL            the change reaches beyond lesson content (app code, build, tests, workflows, the catalog, the index ...),
 *                   so every lesson is walked, as before
 *   a,b,c           a content-only change: only these topic ids need walking (lessons it changed, and the lessons whose
 *                   mastery pool it changed)
 *   NONE            a content-only change that touches no lesson (docs, a variant bank, a script): a one-lesson smoke run
 *
 * "Content-only" means every changed file is under seed/ (a lesson, a mastery pool, a variant bank or practice set), a
 * lesson_*.py or verify_*.py script, a *.md file, or docs/. The catalog and the meta_* files in seed/ change the lesson tree
 * itself, so they count as FULL. Pushes to production and manual runs never call this: they always walk everything.
 * IDS_ROOT overrides the repository root (tests only). Standard library only. */
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const ROOT = process.env.IDS_ROOT ? path.resolve(process.env.IDS_ROOT) : path.join(__dirname, "..");
const base = process.argv[2];
if (!base) { console.error("usage: node tools/changed-topics.js <base-ref-or-sha>"); process.exit(2); }
let files;
try { files = execFileSync("git", ["-C", ROOT, "diff", "--name-only", "--no-renames", base + "...HEAD"], { encoding: "utf8" }).split("\n").filter(Boolean); }
catch (e) { console.log("FULL"); process.exit(0); }          // cannot tell what changed: be safe

const contentOnly = f => /^seed\/[^/]+\.json$/.test(f) || /^(lesson|verify)_[^/]*\.py$/.test(f) || /^[^/]*\.md$/.test(f) || /^docs\//.test(f);
if (!files.every(contentOnly)) { console.log("FULL"); process.exit(0); }
if (files.some(f => f === "seed/catalog.json" || /^seed\/meta_/.test(f))) { console.log("FULL"); process.exit(0); }

const rd = f => { try { return JSON.parse(fs.readFileSync(path.join(ROOT, f), "utf8")); } catch (e) { return null; } };
const seeds = fs.readdirSync(path.join(ROOT, "seed")).filter(f => f.endsWith(".json"));
const lessons = {};                                           // file -> { topicId, setId }
for (const f of seeds) { const d = rd("seed/" + f); if (d && d.id && Array.isArray(d.scenes)) lessons["seed/" + f] = { topicId: d.topicId, setId: ((d.scenes.find(s => s.kind === "quiz") || {}).setId) || "" }; }
const topics = new Set();
for (const f of files.filter(x => /^seed\//.test(x))) {
  if (lessons[f]) { topics.add(lessons[f].topicId); continue; }                       // a changed lesson
  const stem = path.basename(f, ".json");
  Object.values(lessons).filter(l => l.setId === stem).forEach(l => topics.add(l.topicId));   // a changed mastery pool
}
console.log(topics.size ? [...topics].sort().join(",") : "NONE");
