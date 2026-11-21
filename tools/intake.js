#!/usr/bin/env node
/* Local source-document intake: register a PDF, lay out its pages for reading, check the worksheet an assistant writes
 * from it, and report what it adds against the content already in seed/. Standard library only. It never writes to seed/
 * and never copies a source into the repository: everything it makes lives in .cache/intake/ (gitignored).
 *
 *   node tools/intake.js add <file.pdf> --kind questions|learning [--title "..."] [--render all]
 *                                          questions: every page is rendered as an image; learning: only pages whose
 *                                          text layer is empty or lost its maths symbols (--render all for every page)
 *   node tools/intake.js list
 *   node tools/intake.js check <id>        exit 1 if the worksheet is incomplete or wrong (every question accounted for,
 *                                          topic ids real, four options, a keyNote wherever the answer differs from the key)
 *   node tools/intake.js gaps <id>         write .cache/intake/<id>/report.md: near-duplicates already in the banks,
 *                                          topics with no lesson, and (learning material) what each concept adds
 *
 * The two kinds of document and what happens after this tool is in docs/SOURCE_INTAKE.md. In short: a question document
 * ends as a pyq_bank_<source>.py file built and verified like the CSIR banks; learning material ends as edits to lesson
 * JSON. Reading the pages and judging them is the assistant's work; this tool keeps that work complete and checkable.
 *
 * Needs pdfinfo, pdftotext and pdftoppm (poppler; Git Bash and MiKTeX both ship them) for `add` only.
 * Environment: CONTENT_ROOT (the repository, default: this tool's parent) and INTAKE_DIR (default: CONTENT_ROOT/.cache/intake),
 * both for tests. */
const fs = require("fs"), path = require("path"), crypto = require("crypto"), { spawnSync } = require("child_process");

const ROOT = process.env.CONTENT_ROOT ? path.resolve(process.env.CONTENT_ROOT) : path.join(__dirname, "..");
const SEED = path.join(ROOT, "seed");
const DIR = process.env.INTAKE_DIR ? path.resolve(process.env.INTAKE_DIR) : path.join(ROOT, ".cache", "intake");
const KINDS = { questions: "questions.json", learning: "concepts.json" };
const TEXT_PAGE = 150;            // fewer non-space characters than this and the page is treated as an image to read
/* Measured on the CSIR multivariate compilation against the merged banks (IDF-weighted word overlap): four known repeats
   scored 0.57-0.66 even as loose ASCII paraphrases; six made-up new questions scored at most 0.41. A fifth repeat scored
   0.22 paraphrased and 0.87 transcribed as printed, in Unicode, as the banks are: so transcribe, do not paraphrase. */
const DUPLICATE = 0.5, POSSIBLE = 0.4;
const LETTERS = "ABCD";

const readJSON = f => JSON.parse(fs.readFileSync(f, "utf8"));
const writeJSON = (f, d) => fs.writeFileSync(f, JSON.stringify(d, null, 1) + "\n");
const pad3 = n => String(n).padStart(3, "0");
const isStr = s => typeof s === "string" && s.trim().length > 0;

/* ------------------------------------------------------------------ the content already in the repository */
function loadSeed() {
  const cat = readJSON(path.join(SEED, "catalog.json"));
  const topics = {};
  cat.modules.forEach(m => m.topics.forEach(t => { topics[t.id] = { id: t.id, name: t.name, module: m.id, marks: t.marks || 0 }; }));
  const lessons = {}, lessonByTopic = {}, items = [];
  for (const f of fs.readdirSync(SEED).filter(x => x.endsWith(".json")).sort()) {
    const stem = f.slice(0, -5);
    if (stem === "catalog" || stem.startsWith("meta_")) continue;
    let d; try { d = readJSON(path.join(SEED, f)); } catch (e) { continue; }
    if (d && d.id && Array.isArray(d.scenes)) {
      const l = { id: d.id, topicId: d.topicId, title: d.title || d.id, file: "seed/" + f, objectives: d.objectives || [] };
      lessons[d.id] = l; (lessonByTopic[d.topicId] = lessonByTopic[d.topicId] || []).push(l);
    } else if (d && Array.isArray(d.items)) {
      const kind = /_mastery$/.test(stem) ? "mastery" : "bank";
      d.items.forEach(i => items.push({ id: i.id, file: "seed/" + f, kind, topic: i.topic, text: itemText(i), ref: i.ref || "" }));
    }
  }
  return { topics, lessons, lessonByTopic, items };
}

/* ------------------------------------------------------------------ similarity of two question texts */
/* Words are compared after Unicode folding (X₁ → x1), with spelled-out Greek mapped to the letter (rho → ρ), so a plain
   ASCII transcription still meets the Unicode text in seed/. Each shared word counts by its rarity across seed/ (IDF):
   "random" and "let" say little, "wishart" or "hotelling" say a lot. */
const GREEK = { alpha: "α", beta: "β", gamma: "γ", delta: "δ", epsilon: "ε", theta: "θ", lambda: "λ", mu: "μ", nu: "ν", pi: "π",
  rho: "ρ", sigma: "σ", tau: "τ", phi: "φ", chi: "χ", psi: "ψ", omega: "ω" };
function itemText(i) { return [i.stem, ...(i.statements || []), ...(i.options || [])].filter(s => typeof s === "string").join(" "); }
function tokens(s) {
  const out = new Set();
  String(s || "").normalize("NFKC").toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").split(" ").forEach(w => {
    w = GREEK[w] || w;
    if (w.length > 1 || /[\p{N}\p{Script=Greek}]/u.test(w)) out.add(w);
  });
  return out;
}
function jaccard(a, b, weight) {
  const wt = weight || (() => 1);
  let inter = 0, union = 0;
  for (const x of a) { const v = wt(x); union += v; if (b.has(x)) inter += v; }
  for (const x of b) if (!a.has(x)) union += wt(x);
  return union ? inter / union : 0;
}
/* Index seed items once: token sets and the IDF weight of every word. */
function indexItems(seedItems) {
  const df = new Map();
  seedItems.forEach(s => { s.tok = s.tok || tokens(s.text); s.tok.forEach(w => df.set(w, (df.get(w) || 0) + 1)); });
  const N = seedItems.length, idf = new Map();
  df.forEach((n, w) => idf.set(w, Math.log((N + 1) / (n + 1))));
  const unseen = Math.log(N + 1);
  return { items: seedItems, weight: w => idf.has(w) ? idf.get(w) : unseen };
}
function nearest(text, index) {
  const t = tokens(text); let best = null;
  for (const s of index.items) {
    const v = jaccard(t, s.tok, index.weight);
    if (!best || v > best.score) best = { score: v, item: s };
  }
  return best;
}

/* ------------------------------------------------------------------ workspaces */
const wsDir = id => path.join(DIR, id);
function openWorkspace(id) {
  if (!/^[0-9a-f]{12}$/.test(id || "")) throw new Error("A workspace id is the 12 hex characters `add` printed. `list` shows them.");
  const f = path.join(wsDir(id), "source.json");
  if (!fs.existsSync(f)) throw new Error("No workspace " + id + " in " + DIR + ". `list` shows the ones there are.");
  const src = readJSON(f), sheetFile = path.join(wsDir(id), KINDS[src.kind]);
  return { src, sheetFile, sheet: fs.existsSync(sheetFile) ? readJSON(sheetFile) : null };
}

/* pdftotext drops glyphs it cannot map (maths fonts): they come out as U+FFFD, or as empty brackets where P(A) or f(x) was.
   Measured: a quiz PDF showed 13 empty "( )" on one page; a textbook page lost 23 Greek letters as U+FFFD. */
function symbolsLost(text) {
  return (text.match(/�/g) || []).length >= 2 || (text.match(/\(\s*\)/g) || []).length >= 2;
}

function tool(name, args) {
  const r = spawnSync(name, args, { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
  if (r.error) throw new Error(name + " is not available (" + r.error.code + "). Install poppler, or run from Git Bash, which ships it.");
  if (r.status !== 0) throw new Error(name + " failed: " + (r.stderr || "").trim().slice(0, 300));
  return r.stdout;
}

function add(file, opts) {
  if (!file || !fs.existsSync(file)) throw new Error("No such file: " + file);
  if (!KINDS[opts.kind]) throw new Error("Say what the document is: --kind questions (a past paper, compilation or answer key) or --kind learning (a textbook, notes, lecture).");
  const bytes = fs.readFileSync(file);
  if (bytes.slice(0, 5).toString("latin1") !== "%PDF-") throw new Error("Only PDF files are supported; " + path.basename(file) + " does not start with %PDF-.");
  const sha256 = crypto.createHash("sha256").update(bytes).digest("hex"), id = sha256.slice(0, 12), dir = wsDir(id);
  if (fs.existsSync(path.join(dir, "source.json"))) {
    const s = readJSON(path.join(dir, "source.json"));
    console.log("Already registered as " + id + " (" + s.kind + ", " + s.pages + " pages, first added as " + s.file + "). Nothing changed.");
    return s;
  }
  const info = tool("pdfinfo", [file]), pages = +((info.match(/^Pages:\s+(\d+)/m) || [])[1] || 0);
  if (!pages) throw new Error("pdfinfo could not read a page count from " + file);
  fs.mkdirSync(path.join(dir, "pages"), { recursive: true });
  // Which pages to render as images. A question document: every page, because a page with plenty of text can still carry
  // its question as a pasted picture, and its maths may be in fonts the text layer cannot decode. Learning material: pages
  // with no usable text, and pages where the text layer visibly lost symbols. Pass --render all to render everything.
  const renderAll = opts.render === "all" || opts.kind === "questions";
  const imagePages = [], symbolPages = [], rendered = [];
  for (let p = 1; p <= pages; p++) {
    const text = tool("pdftotext", ["-f", String(p), "-l", String(p), "-layout", file, "-"]);
    fs.writeFileSync(path.join(dir, "pages", "p" + pad3(p) + ".txt"), text);
    const chars = text.replace(/\s+/g, "").length;
    if (chars < TEXT_PAGE) imagePages.push(p);
    else if (symbolsLost(text)) symbolPages.push(p);
    if (renderAll || chars < TEXT_PAGE || symbolsLost(text)) {
      tool("pdftoppm", ["-f", String(p), "-l", String(p), "-r", "110", "-png", "-singlefile", file, path.join(dir, "pages", "p" + pad3(p))]);
      rendered.push(p);
    }
  }
  const src = { schema: 1, id, sha256, file: path.basename(file), path: path.resolve(file), size: bytes.length, pages, kind: opts.kind,
    title: opts.title || path.basename(file, path.extname(file)), imagePages, symbolPages, rendered };
  writeJSON(path.join(dir, "source.json"), src);
  const sheet = opts.kind === "questions" ? { source: id, covers: { from: 1, to: null }, items: [] } : { source: id, items: [] };
  writeJSON(path.join(dir, KINDS[opts.kind]), sheet);
  const rel = path.relative(ROOT, dir).split(path.sep).join("/");
  console.log("Registered " + id + ": " + src.title + " (" + pages + " pages, " + opts.kind + ").");
  const notes = [];
  if (imagePages.length) notes.push(imagePages.length + " with no usable text layer");
  if (symbolPages.length) notes.push(symbolPages.length + " whose text layer lost maths symbols");
  console.log(rendered.length === pages ? "All " + pages + " pages rendered as images to read" + (notes.length ? " (" + notes.join(", ") + ")" : "") + ": " + rel + "/pages/p###.png. Read the images; the .txt files are for searching only."
    : rendered.length ? rendered.length + " page(s) rendered as images to read (" + notes.join(", ") + "): " + rel + "/pages/p###.png. The rest have a clean text layer: p###.txt"
    : "Every page has a clean text layer: " + rel + "/pages/p###.txt");
  console.log("Next: read the pages and fill " + rel + "/" + KINDS[opts.kind] + " (docs/SOURCE_INTAKE.md), then run: node tools/intake.js check " + id);
  return src;
}

function list() {
  if (!fs.existsSync(DIR)) { console.log("No sources registered yet. Start with: node tools/intake.js add <file.pdf> --kind questions|learning"); return []; }
  const rows = fs.readdirSync(DIR).filter(d => fs.existsSync(path.join(DIR, d, "source.json"))).sort().map(d => {
    const { src, sheet } = openWorkspace(d), n = sheet && Array.isArray(sheet.items) ? sheet.items.length : 0;
    return { id: d, kind: src.kind, pages: src.pages, entries: n, title: src.title };
  });
  rows.forEach(r => console.log(r.id + "  " + r.kind.padEnd(9) + "  " + String(r.pages).padStart(4) + " pp  " + String(r.entries).padStart(4) + " entries  " + r.title));
  if (!rows.length) console.log("No sources registered yet.");
  return rows;
}

/* ------------------------------------------------------------------ the worksheet checks */
function checkQuestions(src, sheet, S) {
  const P = [], items = Array.isArray(sheet.items) ? sheet.items : null;
  if (!items) return ["questions.json needs an items array"];
  const cov = sheet.covers || {};
  if (!Number.isInteger(cov.from) || !Number.isInteger(cov.to) || cov.to < cov.from)
    P.push("covers must give the question numbers this worksheet accounts for, e.g. {\"from\": 1, \"to\": 88}: set `to` to the last question number printed in the source");
  const seen = {};
  items.forEach((q, k) => {
    const at = "item " + (k + 1) + (Number.isInteger(q.n) ? " (Q" + q.n + ")" : "");
    if (!Number.isInteger(q.n)) { P.push(at + ": n must be the question number printed in the source"); return; }
    if (seen[q.n]) P.push(at + ": Q" + q.n + " appears twice"); seen[q.n] = true;
    const pages = [].concat(q.page);
    if (!pages.length || pages.some(p => !Number.isInteger(p) || p < 1 || p > src.pages)) P.push(at + ": page must be the page (or pages) it is printed on, 1 to " + src.pages);
    if (!["keep", "repeat", "left-out"].includes(q.decision)) P.push(at + ": decision must be keep, repeat or left-out");
    if (q.decision !== "keep") { if (!isStr(q.note)) P.push(at + ": a " + (q.decision || "non-kept") + " question needs a note (which item it repeats, or why it is left out)"); return; }
    if (!isStr(q.stem)) P.push(at + ": stem is empty");
    if (!S.topics[q.topic]) P.push(at + ": topic '" + q.topic + "' is not a topic id in seed/catalog.json");
    if (q.format === "single") {
      if (!Array.isArray(q.options) || q.options.length !== 4 || q.options.some(o => !isStr(o))) P.push(at + ": a single-answer question needs its four printed options");
      else if (new Set(q.options.map(o => o.trim())).size !== 4) P.push(at + ": two options are identical; check the reading");
      if (q.printedKey != null && !(typeof q.printedKey === "string" && q.printedKey.length === 1 && LETTERS.includes(q.printedKey))) P.push(at + ": printedKey must be one letter A-D");
    } else if (q.format === "multi") {
      if (!Array.isArray(q.statements) || q.statements.length !== 4 || q.statements.some(o => !isStr(o))) P.push(at + ": a multiple-correct question needs its four printed statements");
      if (q.printedKey != null && !(typeof q.printedKey === "string" && /^[ABCD]{1,4}$/.test(q.printedKey))) P.push(at + ": printedKey must be the true letters, e.g. AC");
    } else if (q.format === "numeric") {
      if (q.printedKey != null && !isStr(String(q.printedKey))) P.push(at + ": printedKey is empty");
    } else P.push(at + ": format must be single, multi or numeric");
    if (q.answer != null && q.printedKey != null) {
      const norm = x => q.format === "multi" ? [...String(x)].sort().join("") : String(x).trim();
      if (norm(q.answer) !== norm(q.printedKey) && !isStr(q.keyNote)) P.push(at + ": the computed answer " + q.answer + " differs from the printed key " + q.printedKey + ", so it needs a keyNote saying why");
    }
  });
  if (Number.isInteger(cov.from) && Number.isInteger(cov.to)) {
    const missing = []; for (let n = cov.from; n <= cov.to; n++) if (!seen[n]) missing.push(n);
    if (missing.length) P.push("not accounted for: Q" + missing.slice(0, 20).join(", Q") + (missing.length > 20 ? " and " + (missing.length - 20) + " more" : "") + ". Every question is kept, a repeat or left out with a note");
    const outside = Object.keys(seen).map(Number).filter(n => n < cov.from || n > cov.to);
    if (outside.length) P.push("Q" + outside.join(", Q") + " lie outside covers " + cov.from + "-" + cov.to);
  }
  return P;
}

function checkConcepts(src, sheet, S) {
  const P = [], items = Array.isArray(sheet.items) ? sheet.items : null;
  if (!items) return ["concepts.json needs an items array"];
  if (!items.length) P.push("concepts.json has no concepts yet");
  items.forEach((c, k) => {
    const at = "concept " + (k + 1) + (isStr(c.concept) ? " (" + c.concept.slice(0, 40) + ")" : "");
    if (!isStr(c.concept)) P.push(at + ": name the concept");
    if (!Array.isArray(c.pages) || !c.pages.length || c.pages.some(p => !Number.isInteger(p) || p < 1 || p > src.pages)) P.push(at + ": pages must list where the source treats it, 1 to " + src.pages);
    if (!["covered", "partial", "missing", "outside"].includes(c.status)) { P.push(at + ": status must be covered, partial, missing or outside"); return; }
    if (c.status === "outside") { if (!isStr(c.note)) P.push(at + ": say why it is outside the Paper 2 syllabus"); return; }
    if (!S.topics[c.topic]) P.push(at + ": topic '" + c.topic + "' is not a topic id in seed/catalog.json");
    if (c.status === "covered" || c.status === "partial") {
      const l = S.lessons[c.lesson];
      if (!l) P.push(at + ": name the lesson id that covers it (lesson '" + c.lesson + "' does not exist)");
      else if (S.topics[c.topic] && l.topicId !== c.topic) P.push(at + ": lesson " + c.lesson + " belongs to " + l.topicId + ", not " + c.topic);
    }
    if (c.status !== "covered" && !isStr(c.note)) P.push(at + ": a " + c.status + " concept needs a note: what the lesson lacks, with the source's page");
  });
  return P;
}

function check(id, S) {
  const { src, sheet, sheetFile } = openWorkspace(id);
  if (!sheet) return ["missing " + path.basename(sheetFile)];
  if (sheet.source !== id) return [path.basename(sheetFile) + " says it belongs to " + sheet.source + ", not " + id];
  return src.kind === "questions" ? checkQuestions(src, sheet, S) : checkConcepts(src, sheet, S);
}

/* ------------------------------------------------------------------ the report */
function gaps(id, S) {
  const { src, sheet } = openWorkspace(id);
  const problems = check(id, S);
  const L = ["# Intake report: " + src.title, "", "Source `" + src.file + "`, " + src.pages + " pages, sha256 `" + src.sha256 + "`. Kind: " + src.kind + ".", ""];
  if (problems.length) L.push("**The worksheet does not pass `check` yet (" + problems.length + " problem(s)); this report is partial.**", "");
  const objectives = topic => (S.lessonByTopic[topic] || []).map(l => "  - `" + l.id + "` (" + l.file + "): " + (l.objectives.length ? l.objectives.join("; ") : "no objectives listed"));
  if (src.kind === "questions") {
    const items = (sheet.items || []).filter(q => q && q.decision === "keep");
    const index = indexItems(S.items);
    const near = items.map(q => ({ q, b: nearest(itemText(q), index) })).filter(x => x.b).sort((x, y) => y.b.score - x.b.score);
    const verdict = s => s >= DUPLICATE ? "**likely a repeat**" : s >= POSSIBLE ? "check" : "new";
    const dup = near.filter(x => x.b.score >= DUPLICATE), possible = near.filter(x => x.b.score >= POSSIBLE && x.b.score < DUPLICATE);
    const byTopic = {};
    items.forEach(q => (byTopic[q.topic] = byTopic[q.topic] || []).push(q.n));
    L.push("## Summary", "", "| | |", "|---|---|",
      "| Questions accounted for | " + (sheet.items || []).length + " |", "| Kept | " + items.length + " |",
      "| Repeats | " + (sheet.items || []).filter(q => q.decision === "repeat").length + " |", "| Left out | " + (sheet.items || []).filter(q => q.decision === "left-out").length + " |",
      "| Already in a bank (similarity ≥ " + DUPLICATE + ") | " + dup.length + " |", "| Possibly in a bank (" + POSSIBLE + "–" + DUPLICATE + ") | " + possible.length + " |",
      "| Key differs from the printed key | " + (sheet.items || []).filter(q => isStr(q.keyNote)).length + " |", "");
    L.push("## Already in the banks?", "", "The nearest existing item for every kept question, most similar first. Read both for anything not marked new:",
      "a repeat goes in the `ref` of the item that has it, not in a new item. The score is a guide, not a verdict.", "");
    if (near.length) L.push("| Question | Nearest item | File | Similarity | |", "|---|---|---|---|---|",
      ...near.map(x => "| Q" + x.q.n + " | `" + x.b.item.id + "` | " + x.b.item.file + " | " + x.b.score.toFixed(2) + " | " + verdict(x.b.score) + " |"));
    else L.push("No kept questions yet.");
    L.push("", "## By topic", "", "| Topic | Questions | Lesson | Items already on the topic |", "|---|---|---|---|");
    Object.keys(byTopic).sort().forEach(t => {
      const ls = S.lessonByTopic[t] || [], have = S.items.filter(i => i.topic === t).length;
      L.push("| `" + t + "` " + (S.topics[t] ? S.topics[t].name : "(unknown)") + " | Q" + byTopic[t].join(", Q") + " | " + (ls.length ? ls.map(l => "`" + l.id + "`").join(", ") : "**none: a Learn gap**") + " | " + have + " |");
    });
    L.push("", "## Does the lesson teach what these questions test?", "",
      "This needs a reader: compare each question with the objectives of its topic's lesson. A question whose method the lesson never",
      "shows is a Learn gap even when the topic has a lesson; record it as a `missing` or `partial` concept of the topic.", "");
    Object.keys(byTopic).sort().forEach(t => { L.push("- `" + t + "` (Q" + byTopic[t].join(", Q") + ")"); L.push(...(objectives(t).length ? objectives(t) : ["  - no lesson"])); });
  } else {
    const items = sheet.items || [], count = s => items.filter(c => c.status === s).length;
    L.push("## Summary", "", "| Covered | Partial | Missing | Outside the syllabus |", "|---|---|---|---|",
      "| " + count("covered") + " | " + count("partial") + " | " + count("missing") + " | " + count("outside") + " |", "");
    const act = items.filter(c => c.status === "partial" || c.status === "missing");
    L.push("## Proposed changes", "", "Each one becomes an edit to the named lesson's seed JSON (docs/CONTENT_GUIDE.md, 3a) or, for a concept with no",
      "lesson to hold it, a note for `BACKLOG.md`. The prose is written fresh: the source shows what is missing, it is not copied.", "");
    if (act.length) {
      L.push("| Concept | Status | Topic | Lesson | Pages | What is missing |", "|---|---|---|---|---|---|");
      act.forEach(c => L.push("| " + c.concept + " | " + c.status + " | `" + c.topic + "` | " + (c.lesson ? "`" + c.lesson + "`" : "none") + " | " + c.pages.join(", ") + " | " + String(c.note || "").replace(/\|/g, "\\|") + " |"));
    } else L.push("None: the lessons already cover everything this source treats.");
    const out = items.filter(c => c.status === "outside");
    if (out.length) L.push("", "## Outside the syllabus (not used)", "", ...out.map(c => "- " + c.concept + " (pp. " + c.pages.join(", ") + "): " + c.note));
    const touched = [...new Set(act.map(c => c.topic))].sort();
    if (touched.length) { L.push("", "## The lessons as they stand", ""); touched.forEach(t => { L.push("- `" + t + "`"); L.push(...(objectives(t).length ? objectives(t) : ["  - no lesson"])); }); }
  }
  const text = L.join("\n") + "\n";
  fs.writeFileSync(path.join(wsDir(id), "report.md"), text);
  return { text, problems };
}

/* ------------------------------------------------------------------ command line */
function main(argv) {
  const [cmd, ...rest] = argv, opts = {}, pos = [];
  for (let i = 0; i < rest.length; i++) { if (rest[i].startsWith("--")) opts[rest[i].slice(2)] = rest[++i]; else pos.push(rest[i]); }
  try {
    if (cmd === "add") { add(pos[0], opts); return 0; }
    if (cmd === "list") { list(); return 0; }
    if (cmd === "check") {
      const P = check(pos[0], loadSeed());
      if (P.length) { console.log(P.length + " problem(s):"); P.forEach(p => console.log("  - " + p)); return 1; }
      const { sheet } = openWorkspace(pos[0]);
      console.log("Worksheet " + pos[0] + " passes: " + sheet.items.length + " entries. Next: node tools/intake.js gaps " + pos[0]);
      return 0;
    }
    if (cmd === "gaps") {
      const { text, problems } = gaps(pos[0], loadSeed());
      console.log(text);
      console.log("Written to " + path.relative(ROOT, path.join(wsDir(pos[0]), "report.md")).split(path.sep).join("/"));
      return problems.length ? 1 : 0;
    }
  } catch (e) { console.error(e.message); return 2; }
  console.log(fs.readFileSync(__filename, "utf8").split("*/")[0].replace(/^#!.*\n\/\* ?/, "").replace(/^ \* ?/gm, ""));
  return cmd ? 2 : 0;
}

if (require.main === module) process.exit(main(process.argv.slice(2)));
module.exports = { tokens, jaccard, indexItems, nearest, checkQuestions, checkConcepts, loadSeed, symbolsLost };
