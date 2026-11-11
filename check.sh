#!/usr/bin/env bash
# Read-only repository gate. The generated index is the source of lesson discovery;
# the metadata manifest remains the versioned store-facing release inventory.
set -euo pipefail
cd "$(dirname "$0")"

node tools/gen-index.js --check
node tools/validate-contracts.js
node tests/content.test.js
node tools/content.js check
node tests/changed-topics.test.js
node tests/check-ids.test.js
node tests/papers.test.js

# Keep the store-facing manifest consistent with every checked-in lesson seed.
node - <<'NODE'
const fs = require("fs");
const path = require("path");
const manifest = JSON.parse(fs.readFileSync("seed/meta_lessons.json", "utf8"));
const files = fs.readdirSync("seed").filter(f => /^lesson_.*\.json$/.test(f)).sort();
const seen = new Set();
const problems = [];
for (const file of files) {
  const lesson = JSON.parse(fs.readFileSync(path.join("seed", file), "utf8"));
  const id = lesson.topicId;
  if (!id || seen.has(id)) { problems.push(`duplicate or missing topicId in ${file}: ${id}`); continue; }
  seen.add(id);
  const entry = manifest.topics[id];
  if (!entry) { problems.push(`not registered in meta_lessons.json: ${id}`); continue; }
  for (const key of ["id", "title", "moduleId", "estMin", "status", "version"]) {
    if (entry[key] !== lesson[key]) problems.push(`${id}: manifest ${key}=${entry[key]} but lesson has ${lesson[key]}`);
  }
  if (entry.scenes !== lesson.scenes.length) problems.push(`${id}: manifest scene count differs from lesson`);
}
for (const id of Object.keys(manifest.topics)) if (!seen.has(id)) problems.push(`manifest entry has no lesson seed: ${id}`);
if (manifest.count !== Object.keys(manifest.topics).length) problems.push("manifest count does not match topic entries");
if (problems.length) { console.error(problems.join("\n")); process.exit(1); }
console.log(`manifest clean: ${seen.size} lesson seeds, ${manifest.count} registered topics`);
NODE
