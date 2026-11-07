#!/usr/bin/env node
/* Deterministic, read-only inventory of every lesson and question-pool seed.
   This is evidence gathering for Phase 2, not schema enforcement. */
"use strict";
const { listSeeds, lessonIndex } = require("./seed-docs");

const { lessons, qsets } = listSeeds();
const audit = lessonIndex({ lessons, qsets });
const index = audit.index;
const lessonData = lessons.filter(x => x.data).map(x => ({ file: x.file, data: x.data }));
const poolData = qsets.filter(x => x.data).map(x => ({ file: x.file, data: x.data }));
const counts = xs => xs.reduce((a, x) => (a[x] = (a[x] || 0) + 1, a), {});
const sorted = xs => [...new Set(xs)].sort();
const keys = xs => sorted(xs.flatMap(x => Object.keys(x || {})));
const typeOf = v => Array.isArray(v) ? "array" : v === null ? "null" : typeof v;
const fieldTypes = xs => {
  const result = {};
  for (const obj of xs) for (const [key, value] of Object.entries(obj || {})) {
    (result[key] ||= new Set()).add(typeOf(value));
  }
  return Object.fromEntries(Object.entries(result).sort(([a], [b]) => a.localeCompare(b))
    .map(([key, types]) => [key, [...types].sort()]));
};
const grouped = (records, selector) => {
  const groups = {};
  for (const record of records) {
    const name = selector(record) || "(missing)";
    (groups[name] ||= []).push(record);
  }
  return Object.fromEntries(Object.entries(groups).sort(([a], [b]) => a.localeCompare(b)).map(([name, rows]) => [name, {
    count: rows.length,
    files: sorted(rows.map(x => x.file)),
    keys: keys(rows.map(x => x.data)),
    fieldTypes: fieldTypes(rows.map(x => x.data))
  }]));
};
const requiredLessonKeys = ["id", "title", "moduleId", "estMin", "scenes", "status", "version", "topicId"];
const lessonKeyCoverage = Object.fromEntries(requiredLessonKeys.map(key => [key, lessonData.filter(x => Object.hasOwn(x.data, key)).length]));
const sceneRecords = lessonData.flatMap(({file, data}) => (Array.isArray(data.scenes) ? data.scenes : []).map(scene => ({file, data:scene})));
const itemRecords = poolData.flatMap(({file, data}) => (Array.isArray(data.items) ? data.items : []).map(item => ({file, data:item})));
const malformed = lessons.filter(x => x.error).map(x => ({file:x.file,error:x.error}));
const report = {
  source: "all seed/*.json discovered by tools/seed-docs.js; read-only",
  totals: {
    jsonFilesDiscovered: lessons.length + qsets.length + 3,
    lessonFiles: lessonData.length,
    questionPoolFiles: poolData.length,
    malformedJsonFiles: malformed.length,
    scenes: sceneRecords.length,
    questionItems: itemRecords.length
  },
  malformed,
  lessonRequiredKeyCoverage: lessonKeyCoverage,
  lessonTopLevel: { keys: keys(lessonData.map(x => x.data)), fieldTypes: fieldTypes(lessonData.map(x => x.data)) },
  sceneVariants: grouped(sceneRecords, x => x.data.kind),
  poolEnvelopes: grouped(poolData, x => "pool"),
  itemVariants: grouped(itemRecords, x => x.data.format),
  duplicateOrMissing: { problems: audit.problems, warnings: audit.warnings },
  generatedIndexCount: index.count
};
console.log(JSON.stringify(report, null, 2));
if (malformed.length || audit.problems.length) process.exitCode = 1;
