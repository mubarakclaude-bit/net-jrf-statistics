#!/usr/bin/env node
/* Build the static hosted copy into site/ (gitignored; deploy that folder).
 *   ./build.sh && node build_site.js
 * site/index.html = app.html with web/shim.js inlined ahead of the app script.
 * site/data.json  = every store document the app reads, built from seed/.
 * site/manifest.json = which lessons and pools this deployment holds (version, hash, pool size, commit).
 * Personal data never enters the bundle: the answers/marks in the June paper are scrubbed,
 * and the test-profile list (meta/users) is left out. */
const fs = require("fs"), path = require("path");
const W = __dirname, OUT = path.join(W, "site");
// Every store document comes from tools/seed-docs.js, the one place that scans seed/. The lesson
// index is generated there from the lesson files, so adding a lesson never edits a shared file.
const { buildDocs } = require("./tools/seed-docs");
const built = buildDocs();
if (built.problems.length) { built.problems.forEach(p => console.error("PROBLEM " + p)); console.error("FAILED: the seeds have problems"); process.exit(1); }
const docs = built.docs;

// scrub the candidate's own answers out of EVERY previous-year paper (source "pyq"), not one named file: a paper added later
// is covered the moment its file exists (tools/papers.js).
const { scrubPaper } = require("./tools/papers");
for (const k of Object.keys(docs)) if (/^qsets\//.test(k) && docs[k] && docs[k].source === "pyq") scrubPaper(docs[k]);
// The candidate's per-module June scores ("3/11") and the "projected" figure built from them are
// personal. The hosted copy starts everyone at zero: keep the denominator, drop the numerator.
docs["meta/catalog"].modules.forEach(m => {
  const den = String(m.baseline || "0/1").split("/")[1] || "1";
  m.baseline = "0/" + den;
});
// Drop any sentence that says which option the candidate marked or how they were scored.
const PERSONAL = /response sheet|\bmarked (option )?[A-D]\b|\byou marked\b|answered (it )?wrongly|marked wrong|\bI scored\b|candidate scored|your own answer/i;
let dropped = [];
function scrubText(s) {
  if (!PERSONAL.test(s)) return s;
  const parts = s.split(/(?<=[.!?])\s+/);
  const keep = parts.filter(p => { if (PERSONAL.test(p)) { dropped.push(p.slice(0, 110)); return false; } return true; });
  return keep.join(" ");
}
function scrubDeep(o) {
  if (typeof o === "string") return scrubText(o);
  if (Array.isArray(o)) return o.map(scrubDeep);
  if (o && typeof o === "object") { for (const k of Object.keys(o)) o[k] = scrubDeep(o[k]); return o; }
  return o;
}
for (const k of Object.keys(docs)) if (k.startsWith("lessons/")) docs[k] = scrubDeep(docs[k]);
console.log("scrubbed " + dropped.length + " personal sentence(s) from lesson text");
if (process.env.SHOW_SCRUBBED) dropped.forEach(d => console.log("  - " + d));

const leak = JSON.stringify(docs).match(/youMarked|you marked/i);
if (leak) { console.error("FAILED: personal answer data still in the bundle:", leak[0]); process.exit(1); }
// Lesson prose and provenance notes sometimes say which wrong option was marked on the June paper.
// That is not structured data, so it is reported rather than rewritten: decide before deploying.
const prose = Object.keys(docs).filter(k => /^lessons\//.test(k) &&
  /response sheet|marked (option )?[A-D](?![A-Za-z])/i.test(JSON.stringify(docs[k])));
if (prose.length) console.warn("WARNING: " + prose.length + " lesson(s) mention the candidate's marked answers in prose: " + prose.join(", "));

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "data.json"), JSON.stringify(docs));

// site/manifest.json: what this deployment contains, so "is the lesson live?" is answered by one file instead of by opening the
// app. The hash covers the content only (never a date), so the same repository state always yields the same manifest.
const crypto = require("crypto");
const sha = s => crypto.createHash("sha256").update(s).digest("hex");
const lessonsOut = Object.keys(docs).filter(k => k.startsWith("lessons/")).sort().map(k => {
  const l = docs[k], quiz = (l.scenes || []).find(s => s.kind === "quiz");
  const pool = quiz && docs["qsets/" + quiz.setId];
  return { id: l.id, topicId: l.topicId, moduleId: l.moduleId, version: l.version, status: l.status, scenes: l.scenes.length,
           pool: quiz ? quiz.setId : null, poolItems: pool ? pool.items.length : 0, hash: sha(JSON.stringify(l)).slice(0, 12) };
});
const manifest = {
  commit: process.env.VERCEL_GIT_COMMIT_SHA || process.env.GITHUB_SHA || null,
  contentHash: sha(JSON.stringify(docs)).slice(0, 16),
  counts: { lessons: lessonsOut.length, qsets: Object.keys(docs).filter(k => k.startsWith("qsets/")).length },
  lessons: lessonsOut
};
const unwired = lessonsOut.filter(l => !l.pool || l.poolItems === 0);
if (unwired.length) console.warn("WARNING: lesson(s) with no mastery pool in the bundle: " + unwired.map(l => l.id).join(", "));
fs.writeFileSync(path.join(OUT, "manifest.json"), JSON.stringify(manifest, null, 1));

const app = path.join(W, "app.html");
if (!fs.existsSync(app)) { console.error("FAILED: app.html missing, run ./build.sh first"); process.exit(1); }
let html = fs.readFileSync(app, "utf8");
const shim = fs.readFileSync(path.join(W, "web", "shim.js"), "utf8");
const i = html.indexOf("<script>");
if (i < 0) { console.error("FAILED: no <script> in app.html"); process.exit(1); }
// The storage-path checker is injected ahead of the shim so the hosted adapter enforces the same contract as the tests.
const pathChecker = require("./tools/storage-paths").browserSource();
html = html.slice(0, i) + "<script>\n" + pathChecker + "\n" + shim + "\n</script>\n" + html.slice(i);
// app.html is a fragment (the artifact host supplies the document shell); a standalone page needs its own.
html = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n' +
  (/name=["']viewport["']/.test(html) ? "" : '<meta name="viewport" content="width=device-width, initial-scale=1">\n') +
  html + "\n</html>\n";
fs.writeFileSync(path.join(OUT, "index.html"), html);
fs.writeFileSync(path.join(OUT, "vercel.json"), JSON.stringify({
  cleanUrls: true,
  headers: [{ source: "/data.json", headers: [{ key: "Cache-Control", value: "public, max-age=0, must-revalidate" }] }]
}, null, 1));

const n = k => Object.keys(docs).filter(x => x.startsWith(k)).length;
console.log("site/: lessons " + n("lessons/") + ", qsets " + n("qsets/") + ", meta " + n("meta/") +
  ", data.json " + (fs.statSync(path.join(OUT, "data.json")).size / 1e6).toFixed(2) + " MB, index.html " +
  (fs.statSync(path.join(OUT, "index.html")).size / 1e3).toFixed(0) + " kB");
