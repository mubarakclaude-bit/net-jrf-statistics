#!/usr/bin/env node
/* Local source-document intake: register a PDF, lay out its pages for reading, check the worksheet an assistant writes
 * from it, and report what it adds against the content already in seed/. Standard library only. It never copies a source
 * into the repository, and only `build` writes outside .cache/intake/ (gitignored): the bank made from a finished
 * worksheet.
 *
 *   node tools/intake.js scan <folder> [--add]
 *                                          decide what to process next: skips what is already in the app
 *                                          (tools/intake-sources.json), personal, unreadable or duplicate files, works out
 *                                          each file's kind and ranks the rest; --add registers the top pick
 *   node tools/intake.js add <file.pdf> --kind questions|learning [--title "..."] [--render all]
 *                                          questions: every page is rendered as an image; learning: only pages whose
 *                                          text layer is empty or lost its maths symbols (--render all for every page)
 *   node tools/intake.js list
 *   node tools/intake.js check <id>        exit 1 if the worksheet is incomplete or wrong (every question accounted for,
 *                                          topic ids real, four options, a keyNote wherever the answer differs from the key)
 *   node tools/intake.js gaps <id>         write .cache/intake/<id>/report.md: near-duplicates already in the banks,
 *                                          topics with no lesson, and (learning material) what each concept adds
 *   node tools/intake.js explain <id> [--batch 30]
 *                                          the second pass over a finished question worksheet, also done in batches:
 *                                          how many kept questions have an `explanation` and a q<n>() in the workspace's
 *                                          verify_work.py; runs those functions and exit 1 if one disagrees with the
 *                                          worksheet's answer; lists the next batch to do
 *   node tools/intake.js build <id> --name <snake_name> [--title "..."]
 *                                          once explain is finished: write <name>_bank.py and verify_<name>.py from the
 *                                          worksheet and verify_work.py, run both (the bank lands in seed/), register the
 *                                          source in tools/intake-sources.json and write the PR description to pr-body.md
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
/* A path as the reader should type it: relative when it is inside the repository, absolute otherwise. An unattended run
   works in a worktree while INTAKE_DIR points elsewhere, and a relative path would send it to the wrong folder. */
function shownPath(p) {
  const rel = path.relative(ROOT, p);
  return (rel && !rel.startsWith("..") && !path.isAbsolute(rel) ? rel : path.resolve(p)).split(path.sep).join("/");
}
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
  const rel = shownPath(dir);
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

/* ------------------------------------------------------------------ scan: decide what to process next */
/* The owner drops PDFs in one folder; `scan` decides. For every PDF it works out, from the file name and the text of its
   first pages, whether it is already turned into content (tools/intake-sources.json), personal, unreadable, a duplicate,
   in progress here, a question document or learning material, and ranks what is left. The rules are plain and printed
   with every decision, so a wrong call is easy to see and to override with `add --kind`. */
const REGISTER = path.join(ROOT, "tools", "intake-sources.json");
const RX = {
  personalName: /receipt|application|admit.?card|aadha+r|pan.?card|mark.?sheet|certificate|invoice|bank.?statement|resume|\bcv\b|passport|id.?card|salary|payslip/i,
  personalText: /application\s*(no|number)|roll\s*(no|number)|date\s*of\s*birth|father'?s\s*name|registration\s*(no|number)|candidate'?s\s*name|aadha+r/i,
  paperName: /\bpyq|previous.?year|question.?paper|\bpaper\b|\bgate\b|\bcsir\b|\bugc\b|\bnet\b|\bjam\b|\b20\d\d\b/i,
  practiceName: /quiz|\btest\b|mock|assignment|practi[cs]e|question|exercise|problem|solution/i,
  learningName: /notes?|book|guide|course|chapter|cheat|formula|lecture|introduction|methods|theory|handbook/i,
  question: /\bq\.?\s?\d{1,3}\b|question\s*[:\-–]*\s*\d+|^\s*\(\d{1,3}\)|\(\s?[a-d]\s?\)\s/gim,
  numbered: /^\s*\d{1,3}[.)]\s+[A-Z][a-z]/gm,      // "1. Two coins are tossed": counted only when the name says questions
  syllabus: /probab|statist|distribut|estimat|regress|varian|random|sampl|hypothes|markov|stochastic|inference|time.?series|bayes|anova|design|multivariate|nonparametric/i,
};

function loadRegister() {
  try { return readJSON(REGISTER).sources || []; } catch (e) { return []; }
}

/* Decide one file from facts already gathered, so it can be tested without a PDF. f: { name, sha256, pages (0 if unreadable),
   text (first pages), textChars, inProgress: {kind, done, total} | null }. */
function classify(f, register, seen) {
  const name = f.name, text = f.text || "";
  const banked = register.find(s => (s.sha256 || []).includes(f.sha256) || (s.files || []).some(n => n.toLowerCase() === name.toLowerCase()));
  if (banked) return { decision: "skip", why: "already in the app: " + banked.title + " → " + (banked.outputs || []).join(", ") };
  if (seen[f.sha256]) return { decision: "skip", why: "duplicate of " + seen[f.sha256] };
  if (RX.personalName.test(name) || RX.personalText.test(text.slice(0, 4000))) return { decision: "skip", why: "looks personal (name or first page); never processed" };
  if (!f.pages) return { decision: "skip", why: "unreadable PDF (pdfinfo failed); download it again" };
  if (f.inProgress) {
    const p = f.inProgress;
    return { decision: "process", kind: p.kind, score: 100, why: "already started here (" + p.done + " entries" + (p.passes ? ", worksheet passes check" : "") + "); finish it first" };
  }
  const imageOnly = f.textChars < 300;
  const paper = RX.paperName.test(name), practice = RX.practiceName.test(name), learning = RX.learningName.test(name);
  const qs = (text.match(RX.question) || []).length + (paper || practice ? (text.match(RX.numbered) || []).length : 0);
  const inSyllabus = RX.syllabus.test(name) || RX.syllabus.test(text);
  let kind = null, score = 0, why;
  if (paper || practice || qs >= 8 && !learning) {
    kind = "questions";
    score = paper ? 40 : 30;
    const evidence = qs >= 2 ? qs + " question markers in the first pages" : imageOnly ? "pages are images" : "the name says so; the first pages' text shows no questions, so they are probably images";
    why = (paper ? "a past paper or PYQ set" : practice || qs < 8 ? "a quiz, test or question set" : "a question set") + " (" + evidence + ")";
  } else if (f.textChars >= 600 || learning) {
    kind = "learning";
    score = 10;
    why = "learning material (" + (learning ? "name says notes, book or course" : "running text, few question markers") + ")";
  } else return { decision: "look", why: "cannot tell what it is from its name or first pages; open it and use add --kind" };
  if (!inSyllabus) { score -= 8; why += "; no Paper 2 statistics words found, so check it is in the syllabus"; }
  // smaller first within a tier: a finished small document is worth more today than a half-read large one
  score -= Math.min(f.pages, 300) / 100;
  return { decision: "process", kind, score: Math.round(score * 100) / 100, why };
}

function sha256File(file) {
  const h = crypto.createHash("sha256"), fd = fs.openSync(file, "r"), buf = Buffer.alloc(1 << 20);
  let n; while ((n = fs.readSync(fd, buf, 0, buf.length, null)) > 0) h.update(buf.subarray(0, n));
  fs.closeSync(fd);
  return h.digest("hex");
}

function facts(file) {
  const name = path.basename(file), sha256 = sha256File(file);
  let pages = 0, text = "";
  const info = spawnSync("pdfinfo", [file], { encoding: "utf8" });
  if (info.error) throw new Error("pdfinfo is not available (" + info.error.code + "). Install poppler, or run from Git Bash, which ships it.");
  if (info.status === 0) pages = +((info.stdout.match(/^Pages:\s+(\d+)/m) || [])[1] || 0);
  if (pages) { const t = spawnSync("pdftotext", ["-l", "3", "-layout", file, "-"], { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 }); text = t.stdout || ""; }
  let inProgress = null;
  const ws = path.join(DIR, sha256.slice(0, 12), "source.json");
  if (fs.existsSync(ws)) {
    const { src, sheet } = openWorkspace(sha256.slice(0, 12));
    inProgress = { kind: src.kind, done: sheet && Array.isArray(sheet.items) ? sheet.items.length : 0 };
  }
  return { name, file, sha256, pages, text, textChars: text.replace(/\s+/g, "").length, inProgress };
}

/* The decisions for a folder, without printing: { rows, todo (best first), rest }. tools/intake-watch.js calls this. */
function plan(folder) {
  if (!folder || !fs.existsSync(folder) || !fs.statSync(folder).isDirectory()) throw new Error("Give the folder that holds the PDFs: node tools/intake.js scan \"<folder>\"");
  const register = loadRegister(), seen = {}, rows = [];
  for (const n of fs.readdirSync(folder).filter(x => /\.pdf$/i.test(x)).sort()) {
    const f = facts(path.join(folder, n));
    if (f.inProgress) { try { f.inProgress.passes = check(f.sha256.slice(0, 12), loadSeed()).length === 0; } catch (e) { /* report as started */ } }
    const c = classify(f, register, seen);
    if (!seen[f.sha256]) seen[f.sha256] = n;
    rows.push(Object.assign({ name: n, file: f.file, pages: f.pages, sha256: f.sha256 }, c));
  }
  const todo = rows.filter(r => r.decision === "process").sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));
  return { rows, todo, rest: rows.filter(r => r.decision !== "process") };
}

function scan(folder, opts) {
  const { rows, todo, rest } = plan(folder);
  console.log("To process, best first:");
  todo.forEach((r, k) => console.log(String(k + 1).padStart(3) + ". " + r.name + "  [" + r.kind + ", " + r.pages + " pp]  " + r.why));
  if (!todo.length) console.log("  nothing new.");
  console.log("\nSkipped or needing a look:");
  rest.forEach(r => console.log("   - " + r.name + ": " + r.why));
  if (!rest.length) console.log("   none.");
  const next = todo[0];
  if (!next) return { rows, next: null };
  console.log("\nNext: " + next.name + " as " + next.kind + ".");
  if (next.why.startsWith("already started")) console.log("Finish its worksheet in " + shownPath(wsDir(sha256File(next.file).slice(0, 12))) + "/, then check and gaps.");
  else if (opts.add) { console.log(""); add(next.file, { kind: next.kind }); }
  else console.log("Run: node tools/intake.js add \"" + next.file + "\" --kind " + next.kind + "    (or: scan \"" + folder + "\" --add)");
  return { rows, next };
}

/* ------------------------------------------------------------------ the worksheet checks */
/* A file written by Windows PowerShell in the console code page turns every symbol it cannot encode (∩ ∪ ᶜ − ≤)
   into "?", so "P(Aᶜ)" arrives as "P(A?)". A question mark between symbols, or U+FFFD, means the text was mangled. */
function symbolsMangled(text) {
  return typeof text === "string" && (/\uFFFD/.test(text) || /[\w)\]]\?[\w(=)\]+\-*\/]/.test(text) || /\?\?/.test(text));
}

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
    const prose = [q.explanation, q.keyNote, q.note, q.check].concat(Array.isArray(q.whys) ? q.whys : []);
    if (prose.some(symbolsMangled)) P.push(at + ": maths symbols in its explanation or notes were lost as '?' (not written as UTF-8); write them again and save with Python, encoding='utf-8'");
    if (q.decision !== "keep") { if (!isStr(q.note)) P.push(at + ": a " + (q.decision || "non-kept") + " question needs a note (which item it repeats, or why it is left out)"); return; }
    if (!isStr(q.stem)) P.push(at + ": stem is empty");
    if ([q.stem].concat(q.options || [], q.statements || []).some(symbolsMangled))
      P.push(at + ": maths symbols were lost as '?' (the file was not written as UTF-8); transcribe again and save with Python, encoding='utf-8'");
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

/* ------------------------------------------------------------------ explanations and recomputation, in batches
   A long worksheet cannot be explained and independently re-solved in one run, so the second pass is also batched and
   kept in the workspace: each kept item gets an `explanation`, and verify_work.py gets a q<n>() that recomputes its answer
   by a route of its own. The final run turns the two into the bank's build and verification scripts. */
const VERIFY_WORK = "verify_work.py";
function verifyFunctions(src) {
  const have = new Set(); let m; const re = /^def q(\d+)\s*\(/gm;
  while ((m = re.exec(src || ""))) have.add(+m[1]);
  return have;
}
function explainStatus(sheet, verifySrc, batch) {
  const kept = (sheet.items || []).filter(q => q.decision === "keep").sort((a, b) => a.n - b.n);
  const fns = verifyFunctions(verifySrc), problems = [];
  if (/questions\.json|printedKey|"answer"\s*:/.test(verifySrc || "")) problems.push(VERIFY_WORK + " must recompute each answer by its own route: it may not read the worksheet or copy its answers");
  /* the build also needs, for a multiple-correct item, a reason for each statement (`whys`), and for a numeric item a
     one-line `check` usable under exam pressure */
  const mangled = q => [q.explanation, q.check].concat(Array.isArray(q.whys) ? q.whys : []).some(symbolsMangled);
  const ready = q => isStr(q.explanation) && fns.has(q.n) && !mangled(q) &&
    (q.format !== "multi" || (Array.isArray(q.whys) && q.whys.length === 4 && q.whys.every(isStr))) && (q.format !== "numeric" || isStr(q.check));
  const done = kept.filter(ready), todo = kept.filter(q => !ready(q));
  const lost = kept.filter(mangled).map(q => q.n);
  if (lost.length) problems.push("maths symbols were lost as '?' (the worksheet was not written as UTF-8) in the explanation of Q" + lost.join(", Q") +
    ": write them again and save the worksheet with Python, encoding='utf-8', never a PowerShell redirect or Set-Content");
  const extra = [...fns].filter(n => !kept.some(q => q.n === n));
  if (extra.length) problems.push("q" + extra.join("(), q") + "() in " + VERIFY_WORK + " match no kept question");
  return { kept: kept.length, done: done.map(q => q.n), next: todo.slice(0, batch || 30).map(q => q.n), left: todo.length, problems };
}
/* Agreement between a recomputed value and the worksheet's answer: letters exactly (multi as a set), numbers to 1e-9. */
function sameAnswer(q, got) {
  const a = String(q.answer == null ? "" : q.answer).trim(), b = String(got == null ? "" : got).trim();
  if (q.format === "multi") return [...a.toUpperCase()].sort().join("") === [...b.toUpperCase()].sort().join("");
  if (q.format === "numeric") {
    const num = x => { const f = x.match(/^(-?\d+(?:\.\d+)?)\s*\/\s*(\d+(?:\.\d+)?)$/); return f ? +f[1] / +f[2] : (x === "" ? NaN : Number(x)); };
    const x = num(a), y = num(b);
    if (!isNaN(x) && !isNaN(y)) return Math.abs(x - y) <= 1e-9 * Math.max(1, Math.abs(x));
  }
  return a === b;
}
const RUN_VERIFY = ["import json,re,runpy,sys", "g=runpy.run_path(sys.argv[1])", "out={}",
  "for k,f in sorted(g.items()):",
  "    if re.fullmatch(r'q\\d+',k) and callable(f):",
  "        try: out[k[1:]]=str(f())",
  "        except Exception as e: out[k[1:]]='error: '+type(e).__name__+': '+str(e)[:200]",
  "print(json.dumps(out))"].join("\n");
function explain(id, opts) {
  const { src, sheet } = openWorkspace(id);
  if (src.kind !== "questions") throw new Error("explain is for question worksheets");
  if (!sheet) throw new Error("No worksheet yet in " + id);
  const vf = path.join(wsDir(id), VERIFY_WORK), vsrc = fs.existsSync(vf) ? fs.readFileSync(vf, "utf8") : "";
  const st = explainStatus(sheet, vsrc, +opts.batch || 30);
  if (vsrc && verifyFunctions(vsrc).size) {
    let r;
    for (const py of process.env.PYTHON ? [process.env.PYTHON] : ["python", "python3"]) {      // CI has only python3
      r = spawnSync(py, ["-X", "utf8", "-I", "-c", RUN_VERIFY, vf], { cwd: wsDir(id), encoding: "utf8", timeout: 10 * 60 * 1000, maxBuffer: 16 * 1024 * 1024 });
      if (!(r.error && r.error.code === "ENOENT")) break;
    }
    let got = null; try { got = JSON.parse((r.stdout || "").trim().split("\n").pop()); } catch (e) { /* reported below */ }
    if (!got) st.problems.push(VERIFY_WORK + " did not run: " + ((r.error && r.error.message) || (r.stderr || "").trim().split("\n").slice(-3).join(" ")).slice(0, 400));
    else for (const q of sheet.items) if (q.decision === "keep" && got[q.n] !== undefined && !sameAnswer(q, got[q.n]))
      st.problems.push("Q" + q.n + ": q" + q.n + "() gives " + got[q.n] + " but the worksheet's answer is " + q.answer);
  }
  return st;
}

/* ------------------------------------------------------------------ the bank, built mechanically from the worksheet
   Writing a 300-question build script by hand costs a whole agent run and invites copying slips, so a finished worksheet
   becomes the bank's two scripts here: <name>_bank.py (the questions and explanations as data, built with
   pyq_bank_common like the other banks) and verify_<name>.py (verify_work.py verbatim, then a check that every q<n>()
   agrees with the written bank). Both are then run, and the source is registered in tools/intake-sources.json. */
const pyLiteral = obj => "json.loads('" + JSON.stringify(obj).replace(/[\u007f-\uffff]/g, c => "\\u" + c.charCodeAt(0).toString(16).padStart(4, "0"))
  .replace(/\\/g, "\\\\").replace(/'/g, "\\'") + "')";
function runPython(script, cwd) {
  let r;
  for (const py of process.env.PYTHON ? [process.env.PYTHON] : ["python", "python3"]) {
    r = spawnSync(py, ["-X", "utf8", script], { cwd, encoding: "utf8", timeout: 20 * 60 * 1000, maxBuffer: 16 * 1024 * 1024 });
    if (!(r.error && r.error.code === "ENOENT")) break;
  }
  return { ok: r.status === 0, out: ((r.stdout || "") + (r.stderr || "") + (r.error ? r.error.message : "")).trim() };
}
function build(id, opts, S) {
  const name = opts.name;
  if (!/^[a-z][a-z0-9_]{2,40}$/.test(name || "")) throw new Error("--name must be a short snake_case name for the bank, e.g. jam_probability_assignment");
  const { src, sheet } = openWorkspace(id);
  if (src.kind !== "questions") throw new Error("build is for question worksheets");
  const P = check(id, S);
  if (P.length) throw new Error("the worksheet does not pass check yet:\n  - " + P.slice(0, 10).join("\n  - "));
  const st = explain(id, {});
  if (st.problems.length || st.left) throw new Error("explain is not finished: " + (st.problems[0] || st.left + " kept questions still need an explanation and a q<n>()"));
  const vwork = fs.readFileSync(path.join(wsDir(id), VERIFY_WORK), "utf8");
  const title = isStr(opts.title) ? opts.title : src.title, prefix = name.replace(/_/g, "-");
  const kept = sheet.items.filter(q => q.decision === "keep").sort((a, b) => a.n - b.n);
  const outs = {};
  kept.forEach(q => { const m = S.topics[q.topic].module; outs[m] = "seed/" + m + "_" + name + ".json"; });
  const data = kept.map(q => {
    const d = { n: q.n, format: q.format, module: S.topics[q.topic].module, topic: q.topic, stem: q.stem, answer: String(q.answer), explanation: q.explanation };
    if (q.format === "single") d.options = q.options;
    if (q.format === "multi") { d.statements = q.statements; d.whys = q.whys; }
    if (q.format === "numeric") d.check = q.check;
    return d;
  });
  const bankPy = name + "_bank.py", verifyPy = "verify_" + name + ".py";
  fs.writeFileSync(path.join(ROOT, bankPy), [
    "# -*- coding: utf-8 -*-",
    "\"\"\"Build the " + kept.length + " questions kept from: " + title.replace(/"/g, "'") + ".",
    "",
    "Generated by `node tools/intake.js build " + id + " --name " + name + "` from the intake worksheet; regenerate",
    "rather than edit by hand. `python " + bankPy + " --check` fails if the seed files differ.\"\"\"",
    "import json, os, sys",
    "ROOT = os.path.dirname(os.path.abspath(__file__))",
    "sys.path.insert(0, ROOT)",
    "from pyq_bank_common import S, M, N",
    "LABEL = " + JSON.stringify(title),
    "OUTS = " + JSON.stringify(outs),
    "QUESTIONS = " + pyLiteral(data),
    "",
    "",
    "def build():",
    "    out = {m: [] for m in OUTS}",
    "    for q in QUESTIONS:",
    "        iid, ref = \"" + prefix + "-q%03d\" % q[\"n\"], LABEL + \", Q%d\" % q[\"n\"]",
    "        if q[\"format\"] == \"single\":",
    "            it = S(iid, q[\"module\"], q[\"topic\"], ref, q[\"stem\"], q[\"options\"], q[\"answer\"], q[\"explanation\"])",
    "        elif q[\"format\"] == \"multi\":",
    "            it = M(iid, q[\"module\"], q[\"topic\"], ref, q[\"stem\"], q[\"statements\"], q[\"answer\"], q[\"whys\"], \"ABCD\"[(q[\"n\"] - 1) % 4], q[\"explanation\"])",
    "        else:",
    "            it = N(iid, q[\"module\"], q[\"topic\"], ref, q[\"stem\"], q[\"answer\"], q[\"explanation\"], q[\"check\"])",
    "        out[q[\"module\"]].append(it[\"item\"])",
    "    return {m: {\"moduleId\": m, \"source\": \"variant\", \"label\": LABEL, \"count\": len(items), \"items\": items} for m, items in out.items()}",
    "",
    "",
    "def main():",
    "    built = build()",
    "    for module, rel in OUTS.items():",
    "        target = os.path.join(ROOT, rel)",
    "        text = json.dumps(built[module], ensure_ascii=False, indent=2) + \"\\n\"",
    "        if \"--check\" in sys.argv:",
    "            with open(target, encoding=\"utf-8\") as f:",
    "                if f.read() != text:",
    "                    raise SystemExit(rel + \" differs; run python " + bankPy + "\")",
    "        else:",
    "            with open(target, \"w\", encoding=\"utf-8\", newline=\"\\n\") as f:",
    "                f.write(text)",
    "        print(rel + \": \" + str(built[module][\"count\"]) + \" items\")",
    "",
    "",
    "if __name__ == \"__main__\":",
    "    main()", ""].join("\n"));
  fs.writeFileSync(path.join(ROOT, verifyPy), [
    "# -*- coding: utf-8 -*-",
    "\"\"\"Independent recomputation of every answer in " + bankPy + ".",
    "",
    "Each q<n>() below was written while solving question n, by a route of its own (it never reads the bank). The generated",
    "check at the end runs them all against the written seed files.\"\"\"",
    vwork.replace(/^# -\*- coding: utf-8 -\*-\s*\n/, "").trimEnd(), "",
    "",
    "# ---- generated by `node tools/intake.js build`: compare every q<n>() with the bank as written",
    "def _same(fmt, want, got):",
    "    import fractions",
    "    want, got = str(want).strip(), str(got).strip()",
    "    if fmt == \"multi\":",
    "        return sorted(want.upper()) == sorted(got.upper())",
    "    if fmt == \"numeric\":",
    "        try:",
    "            return abs(float(fractions.Fraction(want)) - float(fractions.Fraction(got))) <= 1e-9 * max(1.0, abs(float(fractions.Fraction(want))))",
    "        except (ValueError, ZeroDivisionError):",
    "            pass",
    "    return want == got",
    "",
    "",
    "def _check():",
    "    import json as _json, os as _os",
    "    root = _os.path.dirname(_os.path.abspath(__file__))",
    "    items = {}",
    "    for rel in " + JSON.stringify(Object.values(outs)) + ":",
    "        with open(_os.path.join(root, rel), encoding=\"utf-8\") as f:",
    "            for it in _json.load(f)[\"items\"]:",
    "                items[int(it[\"id\"].rsplit(\"-q\", 1)[1])] = it",
    "    assert len(items) == " + kept.length + ", len(items)",
    "    for n, it in sorted(items.items()):",
    "        want = \"\".join(L for L in \"ABCD\" if it[\"verdicts\"][L][\"tf\"]) if it[\"format\"] == \"multi\" else it[\"answer\"]",
    "        got = globals()[\"q%d\" % n]()",
    "        assert _same(it[\"format\"], want, got), (n, want, got)",
    "    print(\"Verified %d answers independently against " + Object.values(outs).join(", ") + "\" % len(items))",
    "",
    "",
    "if __name__ == \"__main__\":",
    "    _check()", ""].join("\n"));
  const b = runPython(bankPy, ROOT);
  if (!b.ok) throw new Error(bankPy + " failed:\n" + b.out.slice(-1500));
  const v = runPython(verifyPy, ROOT);
  if (!v.ok) throw new Error(verifyPy + " failed:\n" + v.out.slice(-1500));
  // register the source, replacing an earlier entry for the same file
  const regFile = path.join(ROOT, "tools", "intake-sources.json"), reg = readJSON(regFile);
  reg.sources = reg.sources.filter(s => !(s.sha256 || []).includes(src.sha256));
  reg.sources.push({ title, kind: "questions", status: "banked", outputs: Object.values(outs), sha256: [src.sha256], files: [src.file] });
  writeJSON(regFile, reg);
  // a PR description the run can use as it is
  const byTopic = {}; kept.forEach(q => { const t = S.topics[q.topic]; byTopic[t.name] = (byTopic[t.name] || 0) + 1; });
  const notes = sheet.items.filter(q => q.keyNote || q.decision !== "keep");
  const body = ["Adds " + kept.length + " questions from **" + title + "** (" + src.pages + " pages, Q" + sheet.covers.from + "-Q" + sheet.covers.to + ").", "",
    "**By topic:** " + Object.entries(byTopic).sort((a, b) => b[1] - a[1]).map(([t, k]) => t + " " + k).join(", ") + ".", "",
    "**Verification:** " + v.out.split("\n").pop() + ". Every answer was recomputed by its own route while solving (`" + verifyPy + "`).", "",
    "**Answers that differ from the printed key, repeats and left-out questions (" + notes.length + "):**", "",
    ...notes.map(q => "- Q" + q.n + " (" + (q.decision === "keep" ? "kept, answer " + q.answer + ", key " + q.printedKey : q.decision) + "): " + String(q.keyNote || q.note).replace(/\s+/g, " ")), ""].join("\n");
  fs.writeFileSync(path.join(wsDir(id), "pr-body.md"), body);
  return { files: [bankPy, verifyPy, ...Object.values(outs), "tools/intake-sources.json"], verify: "python " + verifyPy, body: shownPath(path.join(wsDir(id), "pr-body.md")), built: b.out, verified: v.out };
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
  for (let i = 0; i < rest.length; i++) {
    if (!rest[i].startsWith("--")) { pos.push(rest[i]); continue; }
    const k = rest[i].slice(2), v = rest[i + 1];
    if (v === undefined || v.startsWith("--")) opts[k] = true; else { opts[k] = v; i++; }   // a bare flag such as --add is true
  }
  try {
    if (cmd === "add") { add(pos[0], opts); return 0; }
    if (cmd === "list") { list(); return 0; }
    if (cmd === "scan") { scan(pos[0], opts); return 0; }
    if (cmd === "check") {
      const P = check(pos[0], loadSeed());
      if (P.length) { console.log(P.length + " problem(s):"); P.forEach(p => console.log("  - " + p)); return 1; }
      const { sheet } = openWorkspace(pos[0]);
      console.log("Worksheet " + pos[0] + " passes: " + sheet.items.length + " entries. Next: node tools/intake.js gaps " + pos[0]);
      return 0;
    }
    if (cmd === "explain") {
      const st = explain(pos[0], opts);
      console.log("Explained and recomputed: " + st.done.length + " of " + st.kept + " kept questions.");
      st.problems.forEach(p => console.log("  - " + p));
      if (st.left) console.log("Next batch: Q" + st.next.join(", Q") + (st.left > st.next.length ? " (" + (st.left - st.next.length) + " more after these)" : ""));
      else if (!st.problems.length) console.log("All kept questions are explained and recomputed. Next: build the bank from the worksheet and " + VERIFY_WORK + ".");
      return st.problems.length ? 1 : 0;
    }
    if (cmd === "build") {
      const r = build(pos[0], opts, loadSeed());
      console.log(r.built + "\n" + r.verified);
      console.log("files: " + JSON.stringify(r.files) + "\nverify: " + r.verify + "\nPR description: " + r.body);
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
module.exports = { explainStatus, sameAnswer, verifyFunctions, tokens, jaccard, indexItems, nearest, checkQuestions, checkConcepts, loadSeed, symbolsLost, symbolsMangled, classify, plan };
