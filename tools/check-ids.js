#!/usr/bin/env node
/* Ids are what a learner's progress is stored against, so a change that drops one silently resets or orphans their work.
 * This compares every seed file a change touches with its version on the base branch and fails when an id has gone.
 *
 *   node tools/check-ids.js [<base-ref-or-sha>]        default base: origin/multi-author-hosting
 *
 * It fails when, compared with the base:
 *   - a lesson's id or topicId changed                          (progress is keyed by both)
 *   - a scene id of an existing lesson is gone                  (the "seen" scenes are stored by scene id)
 *   - a question id of an existing pool or bank is gone         (attempts are stored by question id)
 *   - a lesson seed or a question set was deleted or renamed    (its store document disappears)
 * It allows, and prints a note for: a changed answer key on the same question id (a correction), a changed scene kind.
 * Adding scenes, questions, lessons or pools is always fine, and so is editing any text.
 *
 * An intentional removal is recorded by the owner in contracts/id-exceptions.json, so the decision is visible in review:
 *   { "removed": [ { "file": "seed/lesson_x.json", "ids": ["s7"], "reason": "..." } ] }    ("ids": ["*"] = the whole file)
 * Run from the repository root; IDS_ROOT overrides the root (tests only). Standard library only. */
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const ROOT = process.env.IDS_ROOT ? path.resolve(process.env.IDS_ROOT) : path.join(__dirname, "..");
const base = process.argv[2] || "origin/multi-author-hosting";
const git = (...a) => execFileSync("git", ["-C", ROOT, ...a], { encoding: "utf8", maxBuffer: 1 << 28 });

let changed;
try { changed = git("diff", "--name-status", "--no-renames", base + "...HEAD", "--", "seed/").split("\n").filter(Boolean).map(l => { const [s, ...f] = l.split("\t"); return { status: s[0], file: f.join("\t") }; }); }
catch (e) { console.error("FAILED: cannot compare with '" + base + "': " + String(e.message).split("\n")[0]); process.exit(2); }
changed = changed.filter(c => /^seed\/[^/]+\.json$/.test(c.file));

let exceptions = [];
const exFile = path.join(ROOT, "contracts", "id-exceptions.json");
if (fs.existsSync(exFile)) { try { exceptions = JSON.parse(fs.readFileSync(exFile, "utf8")).removed || []; } catch (e) { console.error("FAILED: contracts/id-exceptions.json is not valid JSON"); process.exit(2); } }
const excused = (file, id) => exceptions.some(x => x.file === file && Array.isArray(x.ids) && (x.ids.includes("*") || x.ids.includes(id)));

const parse = t => { try { return JSON.parse(t); } catch (e) { return null; } };
const kindOf = d => d && d.id && Array.isArray(d.scenes) ? "lesson" : d && Array.isArray(d.items) ? "set" : "other";
const problems = [], notes = [];
const bad = (file, msg) => problems.push(file + ": " + msg);

for (const c of changed) {
  if (c.status === "A") continue;                                    // new files cannot lose an id
  let oldText; try { oldText = git("show", base + ":" + c.file); } catch (e) { continue; }
  const oldDoc = parse(oldText), k = kindOf(oldDoc);
  if (k === "other") continue;                                       // catalog and meta files have their own checks
  if (c.status === "D") { if (!excused(c.file, "*")) bad(c.file, "deleted (or renamed): the " + (k === "lesson" ? "lesson" : "question set") + " '" + (oldDoc.id || path.basename(c.file, ".json")) + "' would disappear for learners. If intended, the owner lists it in contracts/id-exceptions.json"); continue; }
  const newDoc = parse(fs.readFileSync(path.join(ROOT, c.file), "utf8"));
  if (!newDoc) continue;                                             // invalid JSON is reported by the contract check
  if (k === "lesson") {
    if (newDoc.id !== oldDoc.id && !excused(c.file, "id")) bad(c.file, "lesson id changed from '" + oldDoc.id + "' to '" + newDoc.id + "'");
    if (newDoc.topicId !== oldDoc.topicId && !excused(c.file, "topicId")) bad(c.file, "topicId changed from '" + oldDoc.topicId + "' to '" + newDoc.topicId + "'");
    const now = new Map((newDoc.scenes || []).map(s => [s.id, s]));
    for (const s of oldDoc.scenes) {
      if (!now.has(s.id)) { if (!excused(c.file, s.id)) bad(c.file, "scene '" + s.id + "' (" + s.kind + ") was removed; learners' 'seen' progress is stored by scene id. Keep the id (change its content) or add a new one"); }
      else if (now.get(s.id).kind !== s.kind) notes.push(c.file + ": scene '" + s.id + "' changed kind " + s.kind + " -> " + now.get(s.id).kind);
    }
  } else {
    const now = new Map((newDoc.items || []).map(i => [i.id, i]));
    for (const i of oldDoc.items) {
      if (!now.has(i.id)) { if (!excused(c.file, i.id)) bad(c.file, "question '" + i.id + "' was removed; attempts are stored by question id. Keep the id (change the question) or add a new one"); }
      else if (now.get(i.id).answer !== i.answer) notes.push(c.file + ": question '" + i.id + "' answer key changed " + i.answer + " -> " + now.get(i.id).answer + " (a correction; past attempts on it were scored against the old key)");
    }
  }
}
notes.forEach(n => console.log("  note: " + n));
problems.forEach(p => console.log("  FAIL " + p));
console.log(problems.length ? "id check: " + problems.length + " problem(s) against " + base : "id check: no id lost across " + changed.length + " changed seed file(s) against " + base);
process.exit(problems.length ? 1 : 0);
