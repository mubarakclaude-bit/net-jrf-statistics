#!/usr/bin/env node
/* Validate the repository against its contracts (contracts/). This is the machine-checkable definition of
 * "a conforming contribution", and it is what CI runs. Either author, or a human, runs the same command from
 * a clean checkout and gets the same answer:   npm ci && npm run contracts
 *
 *   node tools/validate-contracts.js                     everything
 *   node tools/validate-contracts.js --files seed/lesson_rg6.json seed/regression_t6_mastery.json
 *                                                        only these seeds (CI passes the files a PR changed)
 *   node tools/validate-contracts.js --file backup.json --as progress-backup
 *                                                        any one file against one contract
 *                                                        (--as: lesson | pool | mastery-pool | progress-backup | progress-snapshot | feedback)
 *
 * It checks, in order: (1) the contracts agree with the source they mirror (VIZ_OK, MODES, SCHEMA);
 * (2) the contracts accept every valid fixture and reject every invalid one; (3) the storage-path rule;
 * (4) every literal document path in src/; (5) every lesson and question-set seed. Exit 1 on any failure.
 * Known deviations live in contracts/legacy-exceptions.json and are reported on every run. */
const fs = require("fs"), path = require("path");
let Ajv2020;
try { Ajv2020 = require("ajv/dist/2020"); }
catch (e) { console.error("FAILED: the 'ajv' package is not installed. Run:  npm ci"); process.exit(2); }
const { checkDocPath } = require("./storage-paths");
let analyzeFeatureCode;
try { ({ analyzeFeatureCode } = require("./feature-code")); }
catch (e) { console.error("FAILED: the 'acorn' package is not installed. Run:  npm ci"); process.exit(2); }
const { listSeeds } = require("./seed-docs");

const ROOT = path.join(__dirname, "..");
const read = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), "utf8"));
const text = f => fs.readFileSync(path.join(ROOT, f), "utf8");
const args = process.argv.slice(2);
const flag = n => { const i = args.indexOf(n); return i < 0 ? null : args[i + 1]; };
const filesArg = args.includes("--files") ? args.slice(args.indexOf("--files") + 1).filter(a => !a.startsWith("--")) : null;

const errors = [], notes = [];
const fail = m => errors.push(m);

// ---- load the contracts
const ajv = new Ajv2020({ allErrors: true, strict: true, strictTypes: false, strictRequired: false });
const NAMES = ["lesson", "pool", "mastery-pool", "progress-backup", "progress-snapshot", "feedback", "feature"];
const SCHEMAS = {};
for (const n of NAMES) { SCHEMAS[n] = read("contracts/" + n + ".schema.json"); ajv.addSchema(SCHEMAS[n]); }
const V = n => ajv.getSchema(SCHEMAS[n].$id);
const BASE = "https://net-jrf-statistics/contracts/";
const sceneV = ajv.getSchema(BASE + "lesson.schema.json#/$defs/scene");
const itemV = ajv.getSchema(BASE + "pool.schema.json#/$defs/item");
const brief = errs => (errs || []).slice(0, 4).map(e => (e.instancePath || "/") + " " + e.message + (e.params && e.params.missingProperty ? " (" + e.params.missingProperty + ")" : "")).join("; ");

// ---- single-file mode
if (flag("--file")) {
  const as = flag("--as");
  if (!SCHEMAS[as]) { console.error("--as must be one of: " + NAMES.join(", ")); process.exit(2); }
  const data = JSON.parse(fs.readFileSync(flag("--file"), "utf8"));
  const v = V(as); const ok = v(data);
  console.log(ok ? "VALID: " + flag("--file") + " conforms to " + as : "INVALID: " + flag("--file") + " against " + as + "\n  " + (v.errors || []).map(e => (e.instancePath || "/") + " " + e.message).join("\n  "));
  process.exit(ok ? 0 : 1);
}

// ---- 1. the contracts agree with the source they mirror
function enumOf(schema, ptr) { return ptr.reduce((o, k) => o[k], schema).enum; }
const sameSet = (a, b) => a.length === b.length && a.every(x => b.includes(x));
{
  const gen = text("src/62-gen.js");
  const viz = (gen.match(/const VIZ_OK\s*=\s*\[([^\]]*)\]/) || [])[1];
  const vizSrc = viz ? [...viz.matchAll(/"([^"]+)"/g)].map(m => m[1]) : null;
  const vizContract = enumOf(SCHEMAS.lesson, ["$defs", "viz", "properties", "type"]);
  if (!vizSrc) fail("DRIFT: cannot read VIZ_OK from src/62-gen.js");
  else if (!sameSet(vizSrc, vizContract)) fail("DRIFT: lesson.schema.json viz names differ from VIZ_OK in src/62-gen.js. Only in source: " + vizSrc.filter(x => !vizContract.includes(x)).join(",") + "; only in contract: " + vizContract.filter(x => !vizSrc.includes(x)).join(","));
  const learn = text("src/45-learn.js");
  const modesBlock = (learn.match(/const MODES\s*=\s*\{([\s\S]*?)\n\};?/) || [])[1];
  const modes = modesBlock ? [...modesBlock.matchAll(/^\s{1,4}([A-Za-z]+):\s*\{/gm)].map(m => m[1]) : null;
  const modesContract = SCHEMAS["progress-backup"].$defs.records.properties.config.oneOf[1].properties.mode.enum;
  if (!modes || !modes.length) fail("DRIFT: cannot read MODES from src/45-learn.js");
  else if (!sameSet(modes, modesContract)) fail("DRIFT: progress-backup.schema.json config.mode differs from MODES in src/45-learn.js (" + modes.join(",") + " vs " + modesContract.join(",") + ")");
  const schemaN = +((text("src/10-const.js").match(/const SCHEMA\s*=\s*(\d+)/) || [])[1]);
  notes.push("source mirrors: " + (vizSrc ? vizSrc.length : "?") + " viz names, " + (modes ? modes.length : "?") + " modes, progress SCHEMA=" + schemaN);
  const forder = (text("src/10-const.js").match(/const FORDER\s*=\s*\[([^\]]*)\]/) || [])[1];
  const fmtSrc = forder ? [...forder.matchAll(/"([^"]+)"/g)].map(m => m[1]) : null;
  const fmtContract = enumOf(SCHEMAS.pool, ["$defs", "item", "properties", "format"]);
  if (!fmtSrc) fail("DRIFT: cannot read FORDER (the question formats) from src/10-const.js");
  else if (!sameSet(fmtSrc, fmtContract)) fail("DRIFT: pool.schema.json formats (" + fmtContract.join(",") + ") differ from FORDER in src/10-const.js (" + fmtSrc.join(",") + ")");
  const schemaContract = SCHEMAS["progress-backup"].properties.schemaVersion.const;
  if (!Number.isInteger(schemaN)) fail("DRIFT: cannot read SCHEMA from src/10-const.js");
  else if (schemaContract !== schemaN) fail("DRIFT: progress-backup.schema.json pins schemaVersion " + schemaContract + " but SCHEMA in src/10-const.js is " + schemaN + ". Bump the contract in the same PR and document a migration for any older value that must stay importable.");
}

// ---- 2. fixtures: every valid one passes, every invalid one fails
function runFixtures(file, label, validate) {
  if (!fs.existsSync(path.join(ROOT, file))) { fail("MISSING fixtures: " + file); return; }
  const fx = read(file); let nv = 0, ni = 0;
  for (const [name, doc] of Object.entries(fx.valid || {})) { nv++; if (!validate(doc)) fail("FIXTURE should be VALID but is rejected: " + label + " / " + name + ": " + brief(validate.errors || validate.lastErrors)); }
  for (const bad of fx.invalid || []) { ni++; if (validate(bad.doc)) fail("FIXTURE should be INVALID but is accepted: " + label + " / " + bad.name); else if (bad.expect && !JSON.stringify(validate.errors || validate.lastErrors).includes(bad.expect)) fail("FIXTURE rejected for the wrong reason: " + label + " / " + bad.name + " (expected '" + bad.expect + "', got " + brief(validate.errors) + ")"); }
  notes.push("fixtures " + label + ": " + nv + " valid accepted, " + ni + " invalid rejected");
}
runFixtures("contracts/fixtures/lesson-scenes.json", "lesson scenes", sceneV);
runFixtures("contracts/fixtures/pool-items.json", "pool items", itemV);
runFixtures("contracts/fixtures/progress-backup.json", "progress backup", V("progress-backup"));
runFixtures("contracts/fixtures/progress-snapshot.json", "progress snapshot", V("progress-snapshot"));
runFixtures("contracts/fixtures/feedback.json", "feedback", V("feedback"));
runFixtures("contracts/fixtures/pools.json", "pool envelope", V("pool"));
runFixtures("contracts/fixtures/mastery-pools.json", "mastery pool", V("mastery-pool"));
runFixtures("contracts/fixtures/features.json", "feature manifest", V("feature"));

// ---- 2b. the feature storage rule's own fixtures: every valid snippet passes, every bypass is rejected for the stated reason
{
  const fx = read("contracts/fixtures/feature-code.json"); let nv = 0, ni = 0;
  for (const [name, code] of Object.entries(fx.valid)) { nv++; const p = analyzeFeatureCode(code, fx.declared); if (p.length) fail("FEATURE-CODE fixture should be VALID but is rejected: " + name + ": " + p[0]); }
  for (const b of fx.invalid) {
    ni++; const p = analyzeFeatureCode(b.code, fx.declared);
    if (!p.length) fail("FEATURE-CODE fixture should be INVALID but is accepted (a storage bypass): " + b.name);
    else if (!p.some(x => x.includes(b.expect))) fail("FEATURE-CODE fixture rejected for the wrong reason: " + b.name + " (expected '" + b.expect + "', got " + p[0].slice(0, 100) + ")");
  }
  notes.push("feature storage rule: " + nv + " valid snippets accepted, " + ni + " bypass attempts rejected");
}

// ---- 3. the storage-path rule
{
  const fx = read("contracts/fixtures/storage-paths.json"); let nv = 0, ni = 0;
  for (const p of fx.valid) { nv++; const r = checkDocPath(p); if (!r.ok) fail("PATH should be valid: " + p + " (" + r.reason + ")"); }
  for (const b of fx.invalid) { ni++; const r = checkDocPath(b.path); if (r.ok) fail("PATH should be invalid: " + b.path); else if (b.expect && !r.reason.includes(b.expect)) fail("PATH rejected for the wrong reason: " + b.path + " (" + r.reason + ")"); }
  notes.push("storage paths: " + nv + " valid accepted, " + ni + " invalid rejected");
}

// ---- 4. every literal document path in src/ is allowed
{
  let n = 0;
  for (const f of fs.readdirSync(path.join(ROOT, "src")).filter(x => x.endsWith(".js")).sort()) {
    const src = text("src/" + f);
    for (const m of src.matchAll(/\.doc\(\s*["']([^"']+)["']\s*\)/g)) { n++; const r = checkDocPath(m[1]); if (!r.ok) fail("src/" + f + ": document path '" + m[1] + "' violates the contract: " + r.reason); }
  }
  notes.push("src/: " + n + " literal document paths checked");
}

// ---- 4b. features: every manifest conforms, and no feature uses a storage key it did not declare
{
  const fdir = path.join(ROOT, "src", "features");
  const ids = fs.existsSync(fdir) ? fs.readdirSync(fdir, { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name).sort() : [];
  const fv = V("feature"); let n = 0;
  for (const id of ids) {
    if (filesArg && !filesArg.some(f => f.split(String.fromCharCode(92)).join("/").startsWith("src/features/" + id + "/"))) continue;
    n++;
    const mf = path.join(fdir, id, "feature.json");
    if (!fs.existsSync(mf)) { fail("src/features/" + id + "/feature.json is missing"); continue; }
    let m; try { m = JSON.parse(fs.readFileSync(mf, "utf8")); } catch (e) { fail("src/features/" + id + "/feature.json is not valid JSON"); continue; }
    if (!fv(m)) fail("src/features/" + id + "/feature.json violates the feature contract: " + brief(fv.errors));
    if (m.id !== id) fail("src/features/" + id + ": manifest id '" + m.id + "' must equal the folder name");
    for (const f of ["index.js", "test.js"]) if (!fs.existsSync(path.join(fdir, id, f))) fail("src/features/" + id + "/" + f + " is missing");
    const idx = path.join(fdir, id, "index.js");
    if (fs.existsSync(idx)) {
      // A syntax-tree check (tools/feature-code.js), not a regular expression: dynamic keys, aliases and the other ways of
      // reaching around ctx.store are rejected, so every storage key a feature uses is a declared string literal.
      for (const p of analyzeFeatureCode(fs.readFileSync(idx, "utf8"), m.storage || [])) fail("src/features/" + id + "/index.js " + p);
    }
  }
  notes.push("features: " + n + " manifest(s) checked" + (ids.length ? " (" + ids.join(", ") + ")" : ""));
}

// ---- 5. the seeds
const seeds = listSeeds();
const want = f => !filesArg || filesArg.map(x => x.replace(/\\/g, "/")).includes("seed/" + f);
const catalog = read("seed/catalog.json"); const moduleIds = new Set(catalog.modules.map(m => m.id));
const exceptions = read("contracts/legacy-exceptions.json").exceptions;
const usedEx = new Set();
const qstems = new Set(seeds.qsets.map(q => q.stem));
const quizSets = new Set();
for (const l of seeds.lessons) if (l.data && Array.isArray(l.data.scenes)) for (const s of l.data.scenes) if (s.kind === "quiz") quizSets.add(s.setId);

let nl = 0, nq = 0, nm = 0;
for (const l of seeds.lessons) {
  if (!want(l.file)) continue;
  if (l.error) { fail("seed/" + l.file + ": " + l.error); continue; }
  nl++; const v = V("lesson");
  if (!v(l.data)) {
    const mine = exceptions.filter(x => x.file === "seed/" + l.file && x.contract === "lesson");
    const real = [], excusedParents = new Set();
    for (const e of v.errors) {
      const ex = mine.find(x => {
        if (x.pointer && e.instancePath !== x.pointer) return false;
        if (x.kind === "missing-property") return e.keyword === "required" && (e.params || {}).missingProperty === x.field;
        if (x.kind === "wrong-type") return e.keyword === "type" && (e.params || {}).type === x.expected;
        if (x.kind === "enum") return e.keyword === "enum" || e.keyword === "const";
        if (x.kind === "empty-field") return e.keyword === "minLength";
        return false;
      });
      if (ex) {
        usedEx.add(ex);
        if (ex.kind === "wrong-type") excusedParents.add(ex.pointer.split("/").slice(0, -1).join("/"));
        else excusedParents.add(ex.pointer);
      } else real.push(e);
    }
    const remaining = real.filter(e => !(e.keyword === "if" && excusedParents.has(e.instancePath) &&
      !real.some(r => r !== e && r.instancePath.startsWith(e.instancePath + "/"))));
    if (remaining.length) fail("seed/" + l.file + " violates lesson contract: " + brief(remaining));
  }
  if (!moduleIds.has(l.data.moduleId)) fail("seed/" + l.file + ": moduleId '" + l.data.moduleId + "' is not in seed/catalog.json");
  else if (!String(l.data.topicId).startsWith(l.data.moduleId + "-")) fail("seed/" + l.file + ": topicId '" + l.data.topicId + "' must start with its moduleId '" + l.data.moduleId + "-'");
  for (const s of l.data.scenes || []) if (s.kind === "quiz" && !qstems.has(s.setId)) fail("seed/" + l.file + ": quiz scene points at set '" + s.setId + "' which is not a question set");
}
for (const q of seeds.qsets) {
  if (!want(q.file)) continue;
  nq++; const mastery = /_mastery$/.test(q.stem) || quizSets.has(q.stem);
  const v = V(mastery ? "mastery-pool" : "pool"); if (mastery) nm++;
  if (!v(q.data)) {
    const mine = exceptions.filter(x => x.file === "seed/" + q.file);
    const excused = new Set(), real = [];
    const itemAt = e => { const m = /^\/items\/(\d+)/.exec(e.instancePath || ""); return m ? +m[1] : -1; };
    const matches = (e, ex) => {
      if (ex.pointer) {
        if (e.instancePath !== ex.pointer) return false;
        if (ex.kind === "wrong-type") return e.keyword === "type" && (e.params || {}).type === ex.expected;
        if (ex.kind === "enum") return e.keyword === "enum" || e.keyword === "const";
        if (ex.kind === "missing-property") return e.keyword === "required" && (e.params || {}).missingProperty === ex.field;
        if (ex.kind === "empty-field") return e.keyword === "minLength";
        return false;
      }
      const i = itemAt(e); if (i < 0) return false;
      if (ex.itemId && (q.data.items[i] || {}).id !== ex.itemId) return false;
      if (ex.kind === "missing-property") return e.keyword === "required" && (e.params || {}).missingProperty === ex.field;
      if (ex.kind === "empty-field") return e.keyword === "minLength" && e.instancePath === "/items/" + i + "/" + ex.field;
      return false;
    };
    for (const e of v.errors) { const ex = mine.find(x => matches(e, x)); if (ex) { usedEx.add(ex); excused.add(itemAt(e)); } else real.push(e); }
    // the umbrella "must match then schema" error of an item whose only real problems were excused is noise
    const remaining = real.filter(e => !(e.keyword === "if" && excused.has(itemAt(e)) && !real.some(r => r !== e && itemAt(r) === itemAt(e))));
    if (remaining.length) fail("seed/" + q.file + " violates the " + (mastery ? "mastery-pool" : "pool") + " contract: " + brief(remaining) + (remaining.length > 4 ? " (+" + (remaining.length - 4) + " more)" : ""));
  }
  if (q.data.count !== q.data.items.length) fail("seed/" + q.file + ": count " + q.data.count + " does not equal items.length " + q.data.items.length);
  const ids = q.data.items.map(i => i.id), dup = ids.filter((x, i) => ids.indexOf(x) !== i);
  if (dup.length) fail("seed/" + q.file + ": duplicate item ids " + [...new Set(dup)].join(","));
}
notes.push("seeds: " + nl + " lessons and " + nq + " question sets checked (" + nm + " against the mastery profile)" + (filesArg ? " [only the files given]" : ""));
for (const ex of exceptions) { if (usedEx.has(ex)) notes.push("known legacy exception: " + ex.file + (ex.itemId ? " " + ex.itemId : "") + " (" + ex.kind + " '" + ex.field + "')"); }
if (!filesArg) for (const ex of exceptions) if (!usedEx.has(ex)) fail("legacy exception is stale (the seed now conforms): " + ex.file + (ex.itemId ? " " + ex.itemId : "") + ". Delete it from contracts/legacy-exceptions.json.");

notes.forEach(n => console.log("  " + n));
if (errors.length) { errors.forEach(e => console.log("FAIL " + e)); console.log("FAILED: " + errors.length + " contract violation(s)"); process.exit(1); }
console.log("contracts: all checks passed");
