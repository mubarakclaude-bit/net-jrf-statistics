/* The ONE place that turns seed/ into store documents.
 *
 * Before this module the same scan existed three times (test.js, build_site.js, addlesson.sh) with a
 * hand-edited list in test.js and a committed lesson index that every new lesson had to edit. Two
 * authors adding lessons therefore always conflicted in those shared files. Now nothing in the repo
 * lists lessons by hand: a lesson exists because seed/lesson_<stem>.json exists, its mastery pool
 * exists because the file is in seed/, and the index is computed from the lessons themselves.
 *
 *   store document            comes from
 *   lessons/<lesson.id>       seed/lesson_*.json      (any file with an id and a scenes array)
 *   qsets/<file stem>         every other seed/*.json that has an items array
 *   meta/lessons              GENERATED here from the lesson seeds (never committed)
 *   meta/catalog, meta/syllabus   seed/catalog.json, seed/meta_syllabus.json
 *
 * Contract: tools/seed-docs.js is read-only. It never writes into seed/.
 */
const fs = require("fs"), path = require("path");

const ROOT = path.join(__dirname, "..");
const SEED = path.join(ROOT, "seed");
const readSeed = f => JSON.parse(fs.readFileSync(path.join(SEED, f), "utf8"));
const REQUIRED = ["id", "title", "moduleId", "estMin", "scenes", "status", "version", "topicId"];

function listSeeds() {
  const lessons = [], qsets = [];
  for (const f of fs.readdirSync(SEED).filter(x => x.endsWith(".json")).sort()) {
    const stem = f.slice(0, -5);
    if (stem === "catalog" || stem === "pyq_j26_full" || stem.startsWith("meta_")) continue;
    let d;
    try { d = readSeed(f); } catch (e) { lessons.push({ file: f, stem, error: "not valid JSON: " + e.message }); continue; }
    if (stem.startsWith("lesson_")) lessons.push({ file: f, stem, data: d });
    else if (d && Array.isArray(d.items)) qsets.push({ file: f, stem, data: d });
  }
  return { lessons, qsets };
}

/* Validate the seeds as a set and compute the index. Returns { index, problems, warnings }. */
function lessonIndex(seeds) {
  const problems = [], warnings = [];
  const topics = {}, byDoc = {};
  const qsetStems = new Set(seeds.qsets.map(q => q.stem));
  let catalogTopics = null;
  try { catalogTopics = new Set([].concat(...readSeed("catalog.json").modules.map(m => (m.topics || []).map(t => t.id)))); } catch (e) {}
  for (const l of seeds.lessons) {
    if (l.error) { problems.push(l.file + ": " + l.error); continue; }
    const d = l.data, miss = REQUIRED.filter(k => !(k in d));
    if (miss.length) { problems.push(l.file + ": missing " + miss.join(", ")); continue; }
    if (!Array.isArray(d.scenes)) { problems.push(l.file + ": scenes is not an array"); continue; }
    if (topics[d.topicId]) problems.push("DUPLICATE topicId " + d.topicId + " in " + topics[d.topicId].__file + " and " + l.file);
    if (byDoc[d.id]) problems.push("DUPLICATE store doc id " + d.id + " in " + byDoc[d.id] + " and " + l.file);
    byDoc[d.id] = l.file;
    topics[d.topicId] = { id: d.id, title: d.title, moduleId: d.moduleId, estMin: d.estMin, scenes: d.scenes.length,
                          status: d.status, version: d.version, __file: l.file };
    for (const s of d.scenes) if (s.kind === "quiz" && !qsetStems.has(s.setId))
      warnings.push(l.file + ": quiz scene points at set '" + s.setId + "' but seed/" + s.setId + ".json is not a question set");
    if (catalogTopics && !catalogTopics.has(d.topicId)) warnings.push(l.file + ": topicId " + d.topicId + " is not in seed/catalog.json");
  }
  const sorted = {};
  for (const k of Object.keys(topics).sort()) { const { __file, ...ent } = topics[k]; sorted[k] = ent; }
  return { index: { count: Object.keys(sorted).length, topics: sorted }, problems, warnings };
}

/* All store documents the app reads, built from seed/. */
function buildDocs() {
  const seeds = listSeeds();
  const { index, problems, warnings } = lessonIndex(seeds);
  const docs = {};
  docs["meta/catalog"] = readSeed("catalog.json");
  docs["meta/syllabus"] = readSeed("meta_syllabus.json");
  docs["meta/lessons"] = index;
  docs["meta/app"] = { url: "", title: "NET JRF Statistics", v: 4 };
  for (const l of seeds.lessons) if (l.data && l.data.id && Array.isArray(l.data.scenes)) docs["lessons/" + l.data.id] = l.data;
  for (const q of seeds.qsets) docs["qsets/" + q.stem] = q.data;
  return { docs, seeds, index, problems, warnings };
}

module.exports = { ROOT, SEED, readSeed, listSeeds, lessonIndex, buildDocs };
