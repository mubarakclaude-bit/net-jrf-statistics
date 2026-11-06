#!/usr/bin/env node
/* Build the static hosted copy into site/ (gitignored; deploy that folder).
 *   ./build.sh && node build_site.js
 * site/index.html = app.html with web/shim.js inlined ahead of the app script.
 * site/data.json  = every store document the app reads, built from seed/.
 * Personal data never enters the bundle: the answers/marks in the June paper are scrubbed,
 * and the test-profile list (meta/users) is left out. */
const fs = require("fs"), path = require("path");
const W = __dirname, SEED = path.join(W, "seed"), OUT = path.join(W, "site");
const J = f => JSON.parse(fs.readFileSync(path.join(SEED, f), "utf8"));

const docs = {};
docs["meta/catalog"] = J("catalog.json");
docs["meta/lessons"] = J("meta_lessons.json");
docs["meta/syllabus"] = J("meta_syllabus.json");
docs["meta/app"] = { url: "", title: "NET JRF Statistics", v: 4 };

for (const f of fs.readdirSync(SEED).filter(x => x.endsWith(".json")).sort()) {
  const stem = f.slice(0, -5);
  if (stem.startsWith("meta_") || stem === "catalog") continue;
  const d = J(f);
  if (stem.startsWith("lesson_")) {
    if (d.id && Array.isArray(d.scenes)) docs["lessons/" + d.id] = d;
    continue;
  }
  if (d && Array.isArray(d.items)) docs["qsets/" + stem] = d;
}

// scrub the candidate's own answers out of the previous-year paper
const pq = docs["qsets/pyq_j26_full"];
if (pq) pq.items.forEach(it => {
  delete it.youMarked; delete it.responseSheet;
  if (typeof it.explanation === "string")
    it.explanation = it.explanation.replace(/\s*Response sheet Q\d+;[^]*$/, "").trim();
});
const leak = JSON.stringify(docs).match(/youMarked|you marked/i);
if (leak) { console.error("FAILED: personal answer data still in the bundle:", leak[0]); process.exit(1); }
// Lesson prose and provenance notes sometimes say which wrong option was marked on the June paper.
// That is not structured data, so it is reported rather than rewritten: decide before deploying.
const prose = Object.keys(docs).filter(k => /^lessons\//.test(k) &&
  /response sheet|marked (option )?[A-D](?![A-Za-z])/i.test(JSON.stringify(docs[k])));
if (prose.length) console.warn("WARNING: " + prose.length + " lesson(s) mention the candidate's marked answers in prose: " + prose.join(", "));

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "data.json"), JSON.stringify(docs));

const app = path.join(W, "app.html");
if (!fs.existsSync(app)) { console.error("FAILED: app.html missing, run ./build.sh first"); process.exit(1); }
let html = fs.readFileSync(app, "utf8");
const shim = fs.readFileSync(path.join(W, "web", "shim.js"), "utf8");
const i = html.indexOf("<script>");
if (i < 0) { console.error("FAILED: no <script> in app.html"); process.exit(1); }
html = html.slice(0, i) + "<script>\n" + shim + "\n</script>\n" + html.slice(i);
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
