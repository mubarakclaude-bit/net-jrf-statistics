#!/usr/bin/env node
/* Deterministic structural audit for June 2026 PYQ variant banks.
 * Run: node tools/audit-question-banks.js
 * This does not claim mathematical correctness; human/independent calculation QA is separate.
 */
const fs = require("fs");
const path = require("path");
const seed = path.join(__dirname, "..", "seed");
const originalPath = path.join(seed, "pyq_j26_full.json");
const problems = [], warnings = [];
const original = JSON.parse(fs.readFileSync(originalPath, "utf8"));
const originals = original.items || [];
if (originals.length !== 50) problems.push("Expected 50 original PYQs; found " + originals.length);
const expectedIds = new Set(Array.from({length:50}, (_,i) => "j26-q" + String(i+1).padStart(2,"0")));
for (const q of originals) {
  if (!expectedIds.has(q.id)) problems.push("Unexpected original id: " + q.id);
  if (!q.stem || !q.answer || !q.explanation) problems.push((q.id||"original") + ": missing stem, answer, or explanation");
}
for (const id of expectedIds) if (!originals.some(q => q.id === id)) problems.push("Missing original " + id);

const files = fs.readdirSync(seed).filter(f => f.endsWith("_pyq_variants.json")).sort();
const counts = new Map(), ids = new Map(), stems = new Map();
let total = 0;
for (const file of files) {
  let bank;
  try { bank = JSON.parse(fs.readFileSync(path.join(seed,file),"utf8")); }
  catch (e) { problems.push(file + ": invalid JSON: " + e.message); continue; }
  if (!Array.isArray(bank.items)) { problems.push(file + ": items must be an array"); continue; }
  for (const q of bank.items) {
    total++;
    const src = Number(q.srcQ);
    if (!Number.isInteger(src) || src < 1 || src > 50) {
      problems.push(file + "/" + (q.id||"(no id)") + ": invalid srcQ " + q.srcQ);
      continue;
    }
    counts.set(src, (counts.get(src)||0)+1);
    const id = q.id;
    if (!id) problems.push(file + ": variant missing id (srcQ " + src + ")");
    else if (ids.has(id)) problems.push("Duplicate variant id " + id + " in " + ids.get(id) + " and " + file);
    else ids.set(id,file);
    const required = ["stem","format","answer","explanation"];
    for (const key of required) if (q[key] == null || String(q[key]).trim()==="") problems.push(file+"/"+(id||"no-id")+": missing "+key);
    if (!Array.isArray(q.options) || q.options.length < 2) problems.push(file+"/"+(id||"no-id")+": options missing or too few");
    if (Array.isArray(q.options) && q.options.length) {
      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".slice(0,q.options.length);
      if (!letters.includes(String(q.answer))) problems.push(file+"/"+(id||"no-id")+": answer letter outside options: "+q.answer);
    }
    const stem = String(q.stem||"").toLowerCase().replace(/[^a-z0-9]+/g," ").trim();
    if (stem) {
      const key = src+"|"+stem;
      if (stems.has(key)) warnings.push("Possible duplicate stem for Q"+src+": "+stems.get(key)+" and "+file+"/"+id);
      else stems.set(key,file+"/"+id);
    }
    if (/^\s*\d+\.\s/.test(String(q.explanation||""))) warnings.push(file+"/"+id+": explanation may contain a following question number / fragment");
    if (String(q.explanation||"").trim().length < 18) warnings.push(file+"/"+id+": explanation unusually short");
    if (!q.topicId && !q.topic) warnings.push(file+"/"+id+": no topic/topicId metadata");
  }
}
const under=[], exact=[], over=[], none=[];
for(let n=1;n<=50;n++){
  const c=counts.get(n)||0;
  if(c===0) none.push(n);
  else if(c<10) under.push({q:n,count:c,missing:10-c});
  else if(c===10) exact.push(n);
  else over.push({q:n,count:c,excess:c-10});
}
console.log(JSON.stringify({
  originals: originals.length, variantFiles: files.length, variants: total,
  coveredOriginals: 50-none.length, exactlyTen: exact.length,
  underfilled: under, overfilled: over, noVariants: none,
  structuralProblems: problems, qualityWarnings: warnings
},null,2));
if (problems.length) process.exitCode=1;
