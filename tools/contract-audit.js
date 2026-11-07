#!/usr/bin/env node
/* Read-only inventory of lesson and question-pool seeds before Phase 2 schemas.
   It reports observed shapes; it does not impose a new contract or rewrite seeds. */
"use strict";
const { listSeeds, lessonIndex } = require("./seed-docs");

const { lessons, qsets } = listSeeds();
const audit = lessonIndex({ lessons, qsets });
const index = audit.index;
const counts = xs => xs.reduce((a, x) => (a[x] = (a[x] || 0) + 1, a), {});
const unionKeys = xs => [...new Set(xs.flatMap(x => Object.keys(x || {})))].sort();
const lessonData = lessons.filter(x => x.data).map(x => x.data);
const poolData = qsets.filter(x => x.data).map(x => x.data);
const sceneKinds = counts(lessonData.flatMap(x => (x.scenes || []).map(s => s.kind || "(missing)")));
const itemFormats = counts(poolData.flatMap(x => (x.items || []).map(q => q.format || "(missing)")));
const sceneKeys = unionKeys(lessonData.flatMap(x => x.scenes || []));
const itemKeys = unionKeys(poolData.flatMap(x => x.items || []));
const topLevelKeys = unionKeys([...lessonData, ...poolData]);
const topLevelByType = {};
for (const d of [...lessonData, ...poolData]) {
  for (const [k, v] of Object.entries(d)) {
    const type = Array.isArray(v) ? "array" : v === null ? "null" : typeof v;
    (topLevelByType[k] ||= new Set()).add(type);
  }
}
const report = {
  source: "seed/ via tools/seed-docs.js (read-only)",
  files: {
    lessons: lessonData.length,
    pools: poolData.length,
    malformed: lessons.filter(x => x.error).length
  },
  lessonIds: lessonData.map(x => x.id).sort(),
  topLevelKeys,
  topLevelTypes: Object.fromEntries(Object.entries(topLevelByType).map(([k, v]) => [k, [...v].sort()])),
  sceneKinds,
  sceneKeys,
  poolEnvelopes: [...new Set(poolData.map(x => Object.keys(x).sort().join(",")))].sort(),
  itemFormats,
  itemKeys,
  duplicateOrMissing: {
    lessonIndexProblems: audit.problems,
    lessonIndexWarnings: audit.warnings
  },
  generatedIndexCount: index.count
};
console.log(JSON.stringify(report, null, 2));
if (report.files.malformed || audit.problems.length) process.exitCode = 1;
