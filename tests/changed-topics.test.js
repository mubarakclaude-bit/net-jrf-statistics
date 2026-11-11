#!/usr/bin/env node
/* Tests tools/changed-topics.js in a throwaway git repository: each kind of change must give the stated answer.
 *   node tests/changed-topics.test.js                                                                            */
const fs = require("fs"), os = require("os"), path = require("path"), { execFileSync, spawnSync } = require("child_process");
const TOOL = path.join(__dirname, "..", "tools", "changed-topics.js");
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "topics-test-"));
const git = (...a) => execFileSync("git", ["-C", dir, ...a], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
const w = (rel, data) => { const f = path.join(dir, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, typeof data === "string" ? data : JSON.stringify(data)); };
const run = () => spawnSync(process.execPath, [TOOL, "base"], { env: Object.assign({}, process.env, { IDS_ROOT: dir }), encoding: "utf8" }).stdout.trim();
let failed = 0, total = 0;
const expect = (name, got, want) => { total++; if (got !== want) { failed++; console.log("FAIL " + name + "  — got '" + got + "', wanted '" + want + "'"); } else console.log("ok   " + name + "  → " + got); };
const lesson = (id, topicId, setId) => ({ id, topicId, moduleId: "m", title: "t", version: "1", status: "approved", estMin: 5, scenes: [{ id: "s0", kind: "theory" }, { id: "s1", kind: "quiz", setId }] });

git("init", "-q", "-b", "base"); git("config", "user.email", "t@t"); git("config", "user.name", "t");
w("seed/lesson_a.json", lesson("a", "m-t1", "m_t1_mastery")); w("seed/lesson_b.json", lesson("b", "m-t2", "m_t2_mastery"));
w("seed/m_t1_mastery.json", { items: [{ id: "q" }] }); w("seed/m_t2_mastery.json", { items: [{ id: "q" }] }); w("seed/m_pyq_variants.json", { items: [{ id: "v" }] });
w("seed/catalog.json", { modules: [] }); w("seed/meta_syllabus.json", {}); w("src/app.js", "1"); w("README.md", "r"); w("docs/x.md", "d"); w("verify_m.py", "#"); w("lesson_a.py", "#");
git("add", "-A"); git("commit", "-q", "-m", "base"); git("checkout", "-q", "-b", "work");
const change = (fn) => { git("checkout", "-q", "base"); git("checkout", "-q", "-B", "work"); fn(); git("add", "-A"); git("commit", "-q", "-m", "c", "--allow-empty"); return run(); };

expect("a changed lesson names its topic", change(() => w("seed/lesson_a.json", Object.assign(lesson("a", "m-t1", "m_t1_mastery"), { title: "edited" }))), "m-t1");
expect("a changed mastery pool names the lesson that uses it", change(() => w("seed/m_t2_mastery.json", { items: [{ id: "q" }, { id: "q2" }] })), "m-t2");
expect("two lessons are listed together, sorted", change(() => { w("seed/lesson_b.json", Object.assign(lesson("b", "m-t2", "m_t2_mastery"), { title: "e" })); w("seed/m_t1_mastery.json", { items: [{ id: "z" }] }); }), "m-t1,m-t2");
expect("a new lesson names its topic", change(() => w("seed/lesson_c.json", lesson("c", "m-t3", "m_t3_mastery"))), "m-t3");
expect("a variant bank, docs and scripts alone need no lesson walked", change(() => { w("seed/m_pyq_variants.json", { items: [{ id: "v2" }] }); w("docs/x.md", "d2"); w("verify_m.py", "# 2"); }), "NONE");
expect("a README change alone: NONE", change(() => w("README.md", "r2")), "NONE");
expect("any app code change means FULL, even beside a lesson change", change(() => { w("src/app.js", "2"); w("seed/lesson_a.json", Object.assign(lesson("a", "m-t1", "m_t1_mastery"), { title: "e" })); }), "FULL");
expect("a workflow change means FULL", change(() => w(".github/workflows/validate.yml", "x")), "FULL");
expect("a test or tool change means FULL", change(() => w("tools/x.js", "1")), "FULL");
expect("the catalog changes the lesson tree: FULL", change(() => w("seed/catalog.json", { modules: [{ id: "n" }] })), "FULL");
expect("a meta_ file changes the lesson tree: FULL", change(() => w("seed/meta_syllabus.json", { a: 1 })), "FULL");
expect("clicktest.js itself changing means FULL", change(() => w("clicktest.js", "1")), "FULL");
total++; { const r = spawnSync(process.execPath, [TOOL, "no-such-ref"], { env: Object.assign({}, process.env, { IDS_ROOT: dir }), encoding: "utf8" }).stdout.trim(); if (r !== "FULL") { failed++; console.log("FAIL an unknown base must fall back to FULL, got '" + r + "'"); } else console.log("ok   an unknown base falls back to FULL (safe)"); }

fs.rmSync(dir, { recursive: true, force: true });
console.log("\n" + total + " checks, " + failed + " failed");
process.exit(failed ? 1 : 0);
