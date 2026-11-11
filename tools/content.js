#!/usr/bin/env node
/* Learn the existing content, and see what is missing, from the files themselves. Standard library only; read-only; the
 * output is deterministic (no dates), so it can be regenerated and compared.
 *
 *   node tools/content.js map [--out <dir>]   write CONTENT_MAP.md and content-map.json (default: .cache/content-map/)
 *   node tools/content.js module <id>         one module: its topics, which have a lesson, what is missing
 *   node tools/content.js topic <id>          everything about one topic and where each piece lives
 *   node tools/content.js papers             the past papers found (seed/pyq_<id>_full.json) and how much of each is covered
 *   node tools/content.js pyq [paper] <n>     one past-paper question: the key, what was marked, and what anchors it
 *   node tools/content.js search <text>       find a word or phrase in titles, objectives, traps, stems and explanations
 *   node tools/content.js gaps                what to build or fix next, ranked
 *   node tools/content.js check               exit 1 if the files disagree with each other (CI runs this)
 *
 * What is derived and how. Everything comes from seed/: catalog.json (modules, topics, marks), meta_syllabus.json (unit
 * numbers), lesson_*.json (lessons), every other seed file with an items array (question sets), and the authoring and
 * verification scripts in the repository root. A lesson is "anchored" to a June 2026 question when its provenance text names
 * it (for example "Anchor: Q38"); a question is also covered when a variant bank item names it in srcQ. These links are read
 * from prose and ids, so they are a guide and not a guarantee: the tool says which source each link came from. */
const fs = require("fs"), path = require("path");
const { DEFAULT_PAPER, paperIdOf, questionNumber } = require("./papers");
const ROOT = process.env.CONTENT_ROOT ? path.resolve(process.env.CONTENT_ROOT) : path.join(__dirname, "..");  // CONTENT_ROOT: tests only
const SEED = path.join(ROOT, "seed");
const rd = f => JSON.parse(fs.readFileSync(path.join(SEED, f), "utf8"));
const pad = (s, n) => String(s).padEnd(n).slice(0, Math.max(n, String(s).length));
const num = (x, d = 1) => (Math.round(x * 10 ** d) / 10 ** d).toFixed(d);

/* ------------------------------------------------------------------ load */
function load() {
  const cat = rd("catalog.json"), syl = rd("meta_syllabus.json");
  const files = fs.readdirSync(SEED).filter(f => f.endsWith(".json")).sort();
  const lessons = {}, pools = {};
  const problems = [];
  for (const f of files) {
    const stem = f.slice(0, -5);
    if (stem === "catalog" || stem.startsWith("meta_")) continue;
    let d; try { d = rd(f); } catch (e) { problems.push(f + " is not valid JSON"); continue; }
    if (d && d.id && Array.isArray(d.scenes)) lessons[d.id] = Object.assign({ file: "seed/" + f, stem }, d);
    else if (d && Array.isArray(d.items)) {
      const kind = /_mastery$/.test(stem) ? "mastery" : /_pyq_variants$/.test(stem) ? "variants" : paperIdOf(stem) ? "paper" : "practice";
      pools[stem] = { stem, file: "seed/" + f, kind, source: d.source || "", moduleId: d.moduleId || "", topicId: d.topicId || "", label: d.label || "", items: d.items };
    }
  }
  // Authoring scripts in the repository root. They differ in style (an OUT constant, io.open("seed/..."), or a Path that
  // is read and patched), so a script is taken to author a lesson when it names that lesson's seed file, seed/<stem>.json.
  const scripts = {};
  for (const f of fs.readdirSync(ROOT).filter(x => /^lesson_.*\.py$/.test(x)).sort()) {
    const t = fs.readFileSync(path.join(ROOT, f), "utf8");
    t.replace(/seed\/(lesson_[A-Za-z0-9_]+)\.json/g, (_, stem) => { if (!scripts[stem]) scripts[stem] = { file: f }; return _; });
  }
  const verifiers = fs.readdirSync(ROOT).filter(x => /^verify_.*\.py$/.test(x)).sort().map(f => ({ file: f, text: fs.readFileSync(path.join(ROOT, f), "utf8") }));
  // Past papers: every seed/pyq_<id>_full.json (tools/papers.js). A paper exists because its file does.
  const papers = {};
  Object.values(pools).filter(p => p.kind === "paper").forEach(p => {
    const id = paperIdOf(p.stem);
    papers[id] = { id, file: p.file, label: p.label, source: p.source, questions: p.items.map(q => ({ n: questionNumber(q), id: q.id, format: q.format, paperNo: q.paper, stem: q.stem, answer: q.answer, marked: q.youMarked, options: q.options, explanation: q.explanation, wrong: !!q.youMarked && q.youMarked !== q.answer })) };
  });
  return { cat, syl, lessons, pools, scripts, verifiers, papers, problems };
}

function qsIn(text) { const s = new Set(); String(text || "").replace(/\bQ\s?(\d{1,2})\b/g, (_, n) => { s.add(+n); return _; }); return [...s].sort((a, b) => a - b); }

/* The past-paper questions a lesson is built on: its machine-readable "anchors" field first, then the prose in its provenance
   (read as DEFAULT_PAPER, because that prose predates any other paper). Each is { paper, q, via }. */
function anchorsOf(l) {
  const out = [], seen = new Set(), add = (paper, q, via) => { const k = paper + ":" + q; if (!seen.has(k)) { seen.add(k); out.push({ paper, q, via }); } };
  (Array.isArray(l.anchors) ? l.anchors : []).forEach(a => { if (a && typeof a.paper === "string" && Number.isInteger(a.q)) add(a.paper, a.q, "field"); });
  qsIn(l.provenance).forEach(q => add(DEFAULT_PAPER, q, "prose"));
  return out.sort((x, y) => x.paper.localeCompare(y.paper) || x.q - y.q);
}
const aText = a => a.paper + " Q" + a.q;

function build() {
  const D = load();
  const lessonByTopic = {};
  Object.values(D.lessons).forEach(l => { (lessonByTopic[l.topicId] = lessonByTopic[l.topicId] || []).push(l); });
  const variantQs = {};                    // "paper:question" -> variant banks that name it (srcQ, and srcPaper when not the original paper)
  Object.values(D.pools).filter(p => p.kind === "variants").forEach(p => p.items.forEach(i => { if (i.srcQ) { const k = (i.srcPaper || DEFAULT_PAPER) + ":" + i.srcQ; (variantQs[k] = variantQs[k] || new Set()).add(p.stem); } }));
  const modules = D.cat.modules.map(m => {
    const topics = m.topics.map(t => {
      const ls = lessonByTopic[t.id] || [], l = ls[0] || null;
      const poolStem = l ? (l.scenes.find(s => s.kind === "quiz") || {}).setId : "";
      const pool = poolStem ? D.pools[poolStem] : null;
      const script = l ? D.scripts[l.stem] : null;  /* may patch an existing seed instead of building one */
      const ver = l ? D.verifiers.filter(v => v.text.includes('"' + t.id + '"') || v.text.includes("'" + t.id + "'") || v.text.includes(l.stem) || v.text.includes(t.id)).map(v => v.file) : [];
      const keys = { A: 0, B: 0, C: 0, D: 0 }; if (pool) pool.items.forEach(i => { if (keys[i.answer] !== undefined) keys[i.answer]++; });
      return {
        id: t.id, name: t.name, extent: t.extent, importance: t.imp, questionShare: t.qs, marks: t.marks,
        lesson: l ? { id: l.id, title: l.title, version: l.version, status: l.status, estMin: l.estMin, scenes: l.scenes.length, file: l.file, anchors: anchorsOf(l), objectives: l.objectives || [], traps: l.traps || [], prereq: (l.prereq || []).map(p => p.id) } : null,
        pool: pool ? { stem: pool.stem, file: pool.file, count: pool.items.length, keys, formats: pool.items.reduce((o, i) => (o[i.format] = (o[i.format] || 0) + 1, o), {}), difficulty: pool.items.reduce((o, i) => (o[i.diff] = (o[i.diff] || 0) + 1, o), {}) } : null,
        authoring: script ? script.file : null, verification: ver
      };
    });
    const cov = topics.filter(t => t.lesson).length, exposed = topics.filter(t => !t.lesson).reduce((s, t) => s + (t.marks || 0), 0);
    const u = D.syl.units[m.id] || {};
    return { id: m.id, name: m.name, paper: m.paper, marks: m.marks, unit: u.label || u.no || "", baseline: m.baseline, passPct: m.passPct, targetQ: m.targetQ, topics, covered: cov, total: topics.length, exposedMarks: exposed };
  });
  const anchoredBy = {};                   // "paper:question" -> topic ids whose lesson names it
  modules.forEach(m => m.topics.forEach(t => t.lesson && t.lesson.anchors.forEach(a => (anchoredBy[a.paper + ":" + a.q] = anchoredBy[a.paper + ":" + a.q] || []).push(t.id))));
  const papers = {};
  Object.values(D.papers).forEach(P => { papers[P.id] = { id: P.id, file: P.file, label: P.label, questions: P.questions.map(q => ({ n: q.n, format: q.format, paperNo: q.paperNo, answer: q.answer, marked: q.marked, wrong: q.wrong, stem: q.stem,
    lessons: (anchoredBy[P.id + ":" + q.n] || []).sort(), variantBanks: [...(variantQs[P.id + ":" + q.n] || [])].sort() })) }; });
  return { D, modules, papers, variantQs };
}

/* ------------------------------------------------------------------- gaps */
function gaps(B) {
  const out = { topics: [], papers: {}, lessons: [], pools: [] };
  B.modules.forEach(m => m.topics.filter(t => !t.lesson).forEach(t => out.topics.push({ module: m.id, id: t.id, name: t.name, marks: t.marks, extent: t.extent })));
  out.topics.sort((a, b) => (b.marks || 0) - (a.marks || 0) || a.id.localeCompare(b.id));
  Object.values(B.papers).forEach(P => {
    const list = [];
    P.questions.filter(q => !q.lessons.length && !q.variantBanks.length).forEach(q => list.push({ n: q.n, wrong: q.wrong, format: q.format, stem: q.stem }));
    P.questions.filter(q => q.wrong && !q.lessons.length).forEach(q => { if (!list.find(x => x.n === q.n)) list.push({ n: q.n, wrong: true, format: q.format, stem: q.stem, note: "answered wrongly; has a variant bank but no lesson names it" }); });
    list.sort((a, b) => (b.wrong - a.wrong) || a.n - b.n); out.papers[P.id] = list;
  });
  B.modules.forEach(m => m.topics.filter(t => t.lesson).forEach(t => {
    if (!t.verification.length) out.lessons.push({ id: t.id, issue: "no verification script mentions this topic" });
    if (t.pool) { const low = Object.entries(t.pool.keys).filter(([, v]) => v < 2).map(([k]) => k); if (low.length && t.pool.count >= 10) out.pools.push({ id: t.id, issue: "answer keys " + JSON.stringify(t.pool.keys) + ": " + low.join(",") + " are the answer to fewer than 2 questions" }); if (t.pool.count !== 20) out.pools.push({ id: t.id, issue: "pool has " + t.pool.count + " items, the standard is 20" }); }
    else out.pools.push({ id: t.id, issue: "the lesson's quiz points at a pool that does not exist" });
  }));
  return out;
}

/* ------------------------------------------------------------------ check */
function check(B) {
  const bad = [], tid = new Set(B.modules.flatMap(m => m.topics.map(t => t.id)));
  Object.values(B.D.lessons).forEach(l => { if (!tid.has(l.topicId)) bad.push("lesson " + l.id + ": topicId '" + l.topicId + "' is not in seed/catalog.json"); });
  const per = {}; Object.values(B.D.lessons).forEach(l => (per[l.topicId] = per[l.topicId] || []).push(l.id));
  Object.entries(per).forEach(([t, ids]) => { if (ids.length > 1) bad.push("topic " + t + " has " + ids.length + " lessons (" + ids.join(", ") + "); the map shows the first"); });
  Object.values(B.D.papers).forEach(P => {
    if (P.source !== "pyq") bad.push(P.file + ": a past paper (seed/pyq_<id>_full.json) must have \"source\": \"pyq\"; that is what keeps the candidate's own answers out of the public build");
    const seen = {};
    P.questions.forEach(q => { if (!q.n) bad.push(P.file + ": question '" + q.id + "' has no readable number (topic '... \u00b7 Q9' or an id ending -q09)"); else if (seen[q.n]) bad.push(P.file + ": question number " + q.n + " appears twice ('" + seen[q.n] + "', '" + q.id + "')"); else seen[q.n] = q.id; });
  });
  const has = (paper, q) => !!B.papers[paper] && B.papers[paper].questions.some(x => x.n === q);
  Object.keys(B.variantQs).forEach(k => {
    const [paper, q] = k.split(":");
    if (!B.papers[paper]) bad.push("a variant bank names paper '" + paper + "' (srcPaper), but seed/pyq_" + paper + "_full.json does not exist");
    else if (!has(paper, +q)) bad.push("a variant bank names question " + q + " of paper '" + paper + "', which is not in " + B.papers[paper].file);
  });
  Object.values(B.D.lessons).forEach(l => {
    if (l.anchors === undefined) return;
    if (!Array.isArray(l.anchors)) { bad.push("lesson " + l.id + ": anchors must be an array of { paper, q }"); return; }
    l.anchors.forEach((a, i) => {
      if (!a || typeof a.paper !== "string" || !Number.isInteger(a.q)) bad.push("lesson " + l.id + ": anchors[" + i + "] must look like { \"paper\": \"j26\", \"q\": 38 }");
      else if (!B.papers[a.paper]) bad.push("lesson " + l.id + ": anchors[" + i + "] names paper '" + a.paper + "', which has no seed/pyq_" + a.paper + "_full.json");
      else if (!has(a.paper, a.q)) bad.push("lesson " + l.id + ": anchors[" + i + "] names question " + a.q + " of '" + a.paper + "', which is not in " + B.papers[a.paper].file);
    });
  });
  B.D.problems.forEach(p => bad.push(p));
  return bad;
}

/* ----------------------------------------------------------------- render */
function mapMarkdown(B) {
  const L = [], g = gaps(B), nL = Object.keys(B.D.lessons).length, nT = B.modules.reduce((s, m) => s + m.total, 0);
  const pools = Object.values(B.D.pools), papers = Object.values(B.papers);
  L.push("# Content map", "",
    "Generated from `seed/` by `node tools/content.js map`; never edit by hand. It is rebuilt from production after every merge and published on the `content-map` branch.",
    "Past-paper links come from a lesson's `anchors` field, its provenance text (read as paper `" + DEFAULT_PAPER + "`) and variant-bank `srcQ`/`srcPaper` fields, so treat them as a guide.", "",
    "## At a glance", "",
    "- **" + nL + " lessons** cover **" + B.modules.reduce((s, m) => s + m.covered, 0) + " of " + nT + " catalog topics** in " + B.modules.length + " modules (" + B.modules.filter(m => m.covered).length + " have at least one lesson).",
    "- **" + pools.filter(p => p.kind === "mastery").length + " mastery pools** (" + pools.filter(p => p.kind === "mastery").reduce((s, p) => s + p.items.length, 0) + " questions), **" + pools.filter(p => p.kind === "variants").length + " previous-year variant banks** (" + pools.filter(p => p.kind === "variants").reduce((s, p) => s + p.items.length, 0) + " questions), **" + pools.filter(p => p.kind === "practice").length + " practice sets**, and **" + papers.length + " past paper" + (papers.length === 1 ? "" : "s") + "** (`" + papers.map(P => P.id).join("`, `") + "`).",
    ...papers.map(P => "- Past paper `" + P.id + "` (" + P.label + "): " + P.questions.length + " questions, " + P.questions.filter(q => q.wrong).length + " answered wrongly; named by a lesson **" + P.questions.filter(q => q.lessons.length).length + "/" + P.questions.length + "**; with a variant bank **" + P.questions.filter(q => q.variantBanks.length).length + "/" + P.questions.length + "**; with neither **" + g.papers[P.id].filter(q => !q.note).length + "**."), "",
    "## Modules, ranked by marks still without a lesson", "",
    "| Module | Unit | Marks | Topics | With lesson | Marks without a lesson |", "|---|---|---|---|---|---|");
  B.modules.slice().sort((a, b) => b.exposedMarks - a.exposedMarks || a.id.localeCompare(b.id)).forEach(m => L.push("| `" + m.id + "` " + m.name + " | " + m.unit + " | " + m.marks + " | " + m.total + " | " + m.covered + " | " + num(m.exposedMarks) + " |"));
  L.push("", "## Topics (one row per catalog topic)", "", "`extent` and `imp` come from the catalog; `marks` is the topic's expected marks.", "",
    "| Topic | Name | Extent | Imp | Marks | Lesson | Pool | Past-paper Qs named | Authoring script | Verification |", "|---|---|---|---|---|---|---|---|---|---|");
  B.modules.forEach(m => m.topics.forEach(t => L.push("| `" + t.id + "` | " + t.name + " | " + (t.extent || "") + " | " + (t.importance || "") + " | " + (t.marks || "") + " | " +
    (t.lesson ? "v" + t.lesson.version + " · " + t.lesson.estMin + " min · " + t.lesson.scenes + " scenes (`" + t.lesson.file + "`)" : "—") + " | " + (t.pool ? t.pool.count + " items (`" + t.pool.file + "`)" : "—") + " | " +
    (t.lesson && t.lesson.anchors.length ? t.lesson.anchors.map(aText).join(", ") : "") + " | " + (t.authoring ? "`" + t.authoring + "`" : (t.lesson ? "none" : "")) + " | " + (t.verification.length ? t.verification.map(v => "`" + v + "`").join(", ") : (t.lesson ? "none" : "")) + " |")));
  papers.forEach(P => {
    L.push("", "## Past paper `" + P.id + "`: " + P.label + ", question by question", "", "`marked` is what the candidate marked; a question is a priority when it was answered wrongly.", "",
      "| Q | Format | Key | Marked | Named by lesson | Variant bank |", "|---|---|---|---|---|---|");
    P.questions.slice().sort((a, b) => a.n - b.n).forEach(q => L.push("| " + q.n + " | " + q.format + " | " + q.answer + " | " + q.marked + (q.wrong ? " \u2717" : "") + " | " + (q.lessons.join(", ") || "\u2014") + " | " + (q.variantBanks.join(", ") || "\u2014") + " |"));
  });
  L.push("", "## What to build or fix next", "", "### Topics without a lesson, most marks first (top 25)", "", "| Topic | Module | Marks | Extent |", "|---|---|---|---|");
  g.topics.slice(0, 25).forEach(t => L.push("| `" + t.id + "` " + t.name + " | " + t.module + " | " + (t.marks || "") + " | " + (t.extent || "") + " |"));
  papers.forEach(P => {
    const none = g.papers[P.id].filter(q => !q.note);
    L.push("", "### Past paper `" + P.id + "`: questions with no lesson and no variant bank", "", none.length ? none.map(q => "- Q" + q.n + (q.wrong ? " (answered wrongly)" : "") + ": " + String(q.stem).replace(/\s+/g, " ").slice(0, 110)).join("\n") : "None.");
  });
  L.push("", "### Lessons and pools to tighten", "", g.lessons.length + g.pools.length ? g.lessons.concat(g.pools).map(x => "- `" + x.id + "`: " + x.issue).join("\n") : "None.");
  L.push("", "## Where things live", "",
    "| What | Where | Edit by |", "|---|---|---|",
    "| A lesson, once merged | `seed/lesson_<stem>.json` | edit the JSON directly (docs/CONTENT_GUIDE.md, 3a); a new lesson starts from `lessons/TEMPLATE.py` and `./addlesson.sh` |",
    "| A lesson's mastery pool (20 questions) | `seed/<topic>_mastery.json` | the same: edit the JSON once merged |",
    "| Previous-year variant banks | `seed/<module>_pyq_variants.json` | edit the JSON; `npm run check` validates it |",
    "| A past paper, with keys and what was marked | `seed/pyq_<id>_full.json` (`source: \"pyq\"`); `pyq_j26_full.json` is June 2026 | rarely; keys are facts. A new paper is a new file; see docs/CONTENT_GUIDE.md, 3d |",
    "| Which past questions a lesson is built on | the lesson's `anchors` field: `[{ \"paper\": \"j26\", \"q\": 38 }]` | edit the lesson JSON; CI checks every anchor exists |",
    "| Modules, topics, marks, extent | `seed/catalog.json`; unit numbers in `seed/meta_syllabus.json` | the owner; changes move marks |",
    "| Numbers a lesson relies on | `verify_<group>.py` | whoever authors the lesson |", "");
  return L.join("\n") + "\n";
}

function topicText(B, id) {
  const m = B.modules.find(x => x.topics.some(t => t.id === id)); if (!m) return "No topic '" + id + "'. Topic ids look like regression-t5; run `node tools/content.js module <id>` to list a module.";
  const t = m.topics.find(x => x.id === id), L = [];
  L.push(t.id + " — " + t.name, "  module: " + m.id + " (" + m.name + ", " + m.marks + " marks, unit " + m.unit + ")", "  catalog: extent " + t.extent + ", importance " + t.importance + ", question share " + t.questionShare + ", expected marks " + t.marks);
  if (!t.lesson) { L.push("  lesson: none yet", "  start from lessons/TEMPLATE.py and SPEC.md; see `node tools/content.js gaps`"); return L.join("\n"); }
  const l = t.lesson;
  L.push("  lesson: " + l.title + " — v" + l.version + ", " + l.status + ", " + l.estMin + " min, " + l.scenes + " scenes", "    file: " + l.file, "    authoring script: " + (t.authoring || "NOT FOUND"), "    verification: " + (t.verification.join(", ") || "NOT FOUND"));
  L.push("    prerequisites: " + (l.prereq.join(", ") || "none"), "    objectives:"); l.objectives.forEach(o => L.push("      - " + o)); L.push("    traps it teaches:"); l.traps.forEach(o => L.push("      - " + o));
  if (t.pool) L.push("  mastery pool: " + t.pool.count + " items (" + t.pool.file + "); keys " + JSON.stringify(t.pool.keys) + "; formats " + JSON.stringify(t.pool.formats) + "; difficulty " + JSON.stringify(t.pool.difficulty));
  const named = l.anchors.map(a => { const q = ((B.papers[a.paper] || { questions: [] }).questions).find(x => x.n === a.q); return aText(a) + (q && q.wrong ? " (answered wrongly)" : "") + (q && q.variantBanks.length ? " [variants: " + q.variantBanks.join(", ") + "]" : "") + (a.via === "prose" ? " (from the provenance text)" : ""); });
  L.push("  past-paper questions it names: " + (named.length ? named.join("; ") : "none"));
  return L.join("\n");
}

function search(B, text) {
  const q = text.toLowerCase(), hits = [], has = s => String(s || "").toLowerCase().includes(q);
  B.modules.forEach(m => m.topics.forEach(t => {
    if (has(t.name) || has(t.id)) hits.push("topic    " + t.id + "  " + t.name);
    if (t.lesson) { if (has(t.lesson.title)) hits.push("lesson   " + t.lesson.file + "  " + t.lesson.title); t.lesson.objectives.concat(t.lesson.traps).forEach(s => { if (has(s)) hits.push("lesson   " + t.lesson.file + "  … " + String(s).slice(0, 100)); }); }
  }));
  Object.values(B.D.pools).forEach(p => p.items.forEach(i => { if (has(i.stem) || has(i.explanation)) hits.push("question " + p.file + "  " + i.id + "  " + String(i.stem).replace(/\s+/g, " ").slice(0, 90)); }));
  return hits.length ? hits.slice(0, 40).join("\n") + (hits.length > 40 ? "\n… " + (hits.length - 40) + " more; narrow the search" : "") : "No match for '" + text + "'.";
}

/* -------------------------------------------------------------------- cli */
function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  if (!cmd || cmd === "help" || cmd === "--help") { console.log(fs.readFileSync(__filename, "utf8").split("*/")[0].replace(/^#!.*\n\/\*/, "").trim()); return 0; }
  const B = build();
  if (cmd === "map") {
    const i = rest.indexOf("--out"), dir = path.resolve(i >= 0 ? rest[i + 1] : path.join(ROOT, ".cache", "content-map"));
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, "CONTENT_MAP.md"), mapMarkdown(B));
    const slim = { modules: B.modules, papers: B.papers, gaps: gaps(B) };
    fs.writeFileSync(path.join(dir, "content-map.json"), JSON.stringify(slim, null, 1) + "\n");
    console.log("wrote " + path.join(dir, "CONTENT_MAP.md") + " and content-map.json: " + Object.keys(B.D.lessons).length + " lessons, " + B.modules.reduce((s, m) => s + m.total, 0) + " topics, " + Object.values(B.papers).map(P => P.questions.length + " questions in paper " + P.id).join(", "));
    return 0;
  }
  if (cmd === "check") { const bad = check(B); bad.forEach(b => console.log("  " + b)); console.log(bad.length ? "content check: " + bad.length + " problem(s)" : "content check: the files agree (" + Object.keys(B.D.lessons).length + " lessons, " + B.modules.reduce((s, m) => s + m.total, 0) + " topics)"); return bad.length ? 1 : 0; }
  if (cmd === "topic") { console.log(topicText(B, rest[0] || "")); return 0; }
  if (cmd === "module") {
    const m = B.modules.find(x => x.id === rest[0]); if (!m) { console.log("Modules: " + B.modules.map(x => x.id).join(", ")); return rest[0] ? 1 : 0; }
    console.log(m.id + " — " + m.name + " (" + m.marks + " marks, unit " + m.unit + "): " + m.covered + "/" + m.total + " topics have a lesson; " + num(m.exposedMarks) + " marks have none\n");
    m.topics.forEach(t => console.log(pad(t.id, 20) + pad(t.name, 46) + pad(t.marks == null ? "" : num(t.marks), 6) + (t.lesson ? "v" + t.lesson.version + " " + t.lesson.status : "—")));
    return 0;
  }
  if (cmd === "papers") {
    const ids = Object.keys(B.papers); if (!ids.length) { console.log("No past papers found (seed/pyq_<id>_full.json with source pyq)."); return 0; }
    ids.forEach(id => { const P = B.papers[id], n = P.questions.length; console.log(pad(id, 8) + pad(P.label, 70) + n + " questions, " + P.questions.filter(q => q.wrong).length + " answered wrongly, " + P.questions.filter(q => q.lessons.length).length + " named by a lesson, " + P.questions.filter(q => q.variantBanks.length).length + " with a variant bank  (" + P.file + ")"); });
    return 0;
  }
  if (cmd === "pyq") {
    const ids = Object.keys(B.papers), two = rest.length >= 2, pid = two ? rest[0] : (B.papers[DEFAULT_PAPER] ? DEFAULT_PAPER : ids[0]), n = +(two ? rest[1] : rest[0]);
    if (!B.papers[pid]) { console.log("No paper '" + pid + "'. Papers: " + (ids.join(", ") || "none")); return 1; }
    const q = B.papers[pid].questions.find(x => x.n === n); if (!q) { console.log("No question " + rest[rest.length - 1] + " in paper " + pid + ". Numbers run 1 to " + B.papers[pid].questions.length + "."); return 1; }
    const src = B.D.papers[pid].questions.find(x => x.n === n);
    console.log(pid + " Q" + q.n + " (" + q.format + ")\n" + q.stem + "\n" + (src && src.options ? src.options.map((o, i) => "  " + "ABCD"[i] + ". " + o).join("\n") : "") + "\nkey " + q.answer + ", candidate marked " + q.marked + (q.wrong ? "  \u2717 answered wrongly" : "") + "\nnamed by lessons: " + (q.lessons.join(", ") || "none") + "\nvariant banks: " + (q.variantBanks.join(", ") || "none")); return 0;
  }
  if (cmd === "search") { console.log(search(B, rest.join(" "))); return 0; }
  if (cmd === "gaps") {
    const g = gaps(B);
    console.log("TOPICS WITHOUT A LESSON, most marks first\n" + g.topics.slice(0, 20).map(t => "  " + pad(t.id, 22) + pad(t.name, 44) + pad(t.marks == null ? "" : num(t.marks), 5) + t.module).join("\n") + (g.topics.length > 20 ? "\n  … " + (g.topics.length - 20) + " more" : ""));
    Object.keys(g.papers).forEach(id => console.log("\nPAST PAPER " + id.toUpperCase() + ": QUESTIONS WITH NO LESSON AND NO VARIANT BANK\n" + (g.papers[id].filter(q => !q.note).map(q => "  Q" + q.n + (q.wrong ? " \u2717" : "") + "  " + String(q.stem).replace(/\s+/g, " ").slice(0, 90)).join("\n") || "  none")));
    console.log("\nLESSONS AND POOLS TO TIGHTEN\n" + (g.lessons.concat(g.pools).map(x => "  " + x.id + ": " + x.issue).join("\n") || "  none")); return 0;
  }
  console.log("unknown command '" + cmd + "'. Run: node tools/content.js help"); return 2;
}
process.exit(main());
