#!/usr/bin/env node
/* The independence acceptance test, as a command.   npm run acceptance
 *
 * The owner's requirement: after the shared foundation exists, Claude and ChatGPT (or a human) must each be able to
 * add a conforming lesson on their own, with no help from the other, and get the same deterministic result. This
 * proves it on a scratch copy of the working tree (your repository is never modified):
 *
 *   1. two "authors" each add a different lesson on their own branch, touching ONLY their own files
 *   2. both branches merge with no conflict, in either order
 *   3. the merged tree passes the contract validator and the seed-set check
 *   4. the hosted site data built from the two merge orders is byte-identical (deterministic build)
 *   5. a lesson that breaks the contract is rejected, and says why
 *   6. a lesson that breaks the storage-path rule in its own data is not required to exist: paths are checked at run time
 *
 * Needs: git, node, python (for build.sh). Exit 0 only if every step holds. */
const fs = require("fs"), os = require("os"), path = require("path"), crypto = require("crypto");
const { execFileSync, spawnSync } = require("child_process");

const ROOT = path.join(__dirname, "..");
const results = [];
const step = (name, ok, detail) => { results.push(ok); console.log((ok ? "PASS " : "FAIL ") + name + (detail ? "  — " + detail : "")); };
const run = (cmd, args, cwd, env) => spawnSync(cmd, args, { cwd, encoding: "utf8", env: { ...process.env, ...(env || {}) }, shell: false });
const git = (cwd, ...a) => run("git", a, cwd);

// ---- 1. a scratch copy of the CURRENT working tree (tracked + untracked, never ignored files)
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "njs-accept-"));
const base = path.join(tmp, "repo");
const files = execFileSync("git", ["ls-files", "-co", "--exclude-standard", "-z"], { cwd: ROOT }).toString("utf8").split("\0").filter(Boolean);
for (const f of files) { const src = path.join(ROOT, f); if (!fs.existsSync(src)) continue; fs.mkdirSync(path.dirname(path.join(base, f)), { recursive: true }); fs.copyFileSync(src, path.join(base, f)); }
git(base, "init", "-q", "-b", "main"); git(base, "config", "user.email", "acceptance@example.invalid"); git(base, "config", "user.name", "acceptance");
git(base, "add", "-A"); git(base, "commit", "-q", "-m", "base");
const ENV = { NODE_PATH: path.join(ROOT, "node_modules") };       // reuse the installed ajv; nothing is installed or fetched
const node = (cwd, ...a) => run(process.execPath, a, cwd, ENV);

// ---- a synthetic but fully conforming lesson, derived from a real one so every field has a valid shape
function addLesson(cwd, doc, topic, set) {
  const L = JSON.parse(fs.readFileSync(path.join(cwd, "seed", "lesson_rg5.json"), "utf8"));
  L.id = doc; L.topicId = topic; L.title = "Acceptance " + topic;
  L.scenes.forEach(s => { if (s.kind === "quiz") s.setId = set; });
  const P = JSON.parse(fs.readFileSync(path.join(cwd, "seed", "regression_t5_mastery.json"), "utf8"));
  P.topicId = topic; P.items.forEach((it, i) => { it.id = topic + "-m-" + String(i + 1).padStart(2, "0"); it.topic = topic; });
  fs.writeFileSync(path.join(cwd, "seed", "lesson_" + doc + ".json"), JSON.stringify(L));
  fs.writeFileSync(path.join(cwd, "seed", set + ".json"), JSON.stringify(P));
  return ["seed/lesson_" + doc + ".json", "seed/" + set + ".json"];
}
const authorBranch = (name, doc, topic, set) => {
  git(base, "switch", "-q", "-c", name, "main");
  const mine = addLesson(base, doc, topic, set);
  git(base, "add", "-A"); git(base, "commit", "-q", "-m", name + " adds " + topic);
  const touched = git(base, "diff", "--name-only", "main", name).stdout.split("\n").filter(Boolean);
  git(base, "switch", "-q", "main");
  return { mine, touched };
};
const A = authorBranch("claude-lesson", "acca1", "regression-t98", "regression_t98_mastery");
const B = authorBranch("gpt-lesson", "accb1", "regression-t99", "regression_t99_mastery");
step("1. each author changed only their own two files", eq(A.touched.sort(), A.mine.sort()) && eq(B.touched.sort(), B.mine.sort()), "A: " + A.touched.join(", ") + " | B: " + B.touched.join(", "));
function eq(x, y) { return JSON.stringify(x) === JSON.stringify(y); }

// ---- 2. merge both ways
const merge = (name, first, second) => {
  git(base, "switch", "-q", "-c", name, "main");
  const m1 = git(base, "merge", "--no-edit", "-q", first), m2 = git(base, "merge", "--no-edit", "-q", second);
  return m1.status === 0 && m2.status === 0;
};
const ab = merge("merge-ab", "claude-lesson", "gpt-lesson");
step("2a. merging A then B has no conflict", ab);
git(base, "switch", "-q", "main"); const ba = merge("merge-ba", "gpt-lesson", "claude-lesson");
step("2b. merging B then A has no conflict", ba);

// ---- 3 and 4. validate and build each merged tree
const buildData = branch => {
  git(base, "switch", "-q", branch);
  const v = node(base, "tools/validate-contracts.js"), c = node(base, "tools/gen-index.js", "--check");
  const b = run("bash", ["build.sh"], base, ENV), s = node(base, "build_site.js");
  const dataPath = path.join(base, "site", "data.json");
  const hash = fs.existsSync(dataPath) ? crypto.createHash("sha256").update(fs.readFileSync(dataPath)).digest("hex") : null;
  const data = hash ? JSON.parse(fs.readFileSync(dataPath, "utf8")) : {};
  return { v, c, b, s, hash, lessons: Object.keys(data).filter(k => k.startsWith("lessons/")).length, hasBoth: !!(data["lessons/acca1"] && data["lessons/accb1"]) };
};
const R1 = buildData("merge-ab"), R2 = buildData("merge-ba");
step("3. the merged tree passes the contract validator", R1.v.status === 0 && R2.v.status === 0, (R1.v.stdout.trim().split("\n").pop() || R1.v.stderr.slice(0, 200)));
step("3b. the merged tree passes the seed-set check", R1.c.status === 0 && R2.c.status === 0, R1.c.stdout.trim().split("\n").pop());
step("4a. the hosted site builds from the merged tree and contains both new lessons", R1.s.status === 0 && R1.hasBoth && R2.hasBoth, "lessons in the built data: " + R1.lessons);
step("4b. the build is deterministic: identical data for either merge order", !!R1.hash && R1.hash === R2.hash, (R1.hash || "").slice(0, 12) + " vs " + (R2.hash || "").slice(0, 12));

// ---- 5. a contract-breaking lesson is rejected with a reason
git(base, "switch", "-q", "-c", "broken", "main");
addLesson(base, "accbad", "regression-t97", "regression_t97_mastery");
const bp = path.join(base, "seed", "lesson_accbad.json"), bad = JSON.parse(fs.readFileSync(bp, "utf8"));
bad.scenes.find(s => s.kind === "explore").viz = { type: "my-own-chart" }; delete bad.scenes.find(s => s.kind === "theory").blocks;
fs.writeFileSync(bp, JSON.stringify(bad));
const rej = node(base, "tools/validate-contracts.js");
step("5. a lesson with an unregistered visualisation and a theory scene without blocks is rejected", rej.status === 1 && /lesson_accbad/.test(rej.stdout) && /blocks|enum/.test(rej.stdout), (rej.stdout.split("\n").find(l => /lesson_accbad/.test(l)) || "").slice(0, 140));

// ---- 6. validating one changed file in isolation (what CI does for a pull request)
git(base, "switch", "-q", "main"); git(base, "checkout", "-q", "merge-ab");
const only = node(base, "tools/validate-contracts.js", "--files", "seed/lesson_acca1.json", "seed/regression_t98_mastery.json");
step("6. a pull request can validate just the files it changed", only.status === 0 && /2 question sets|1 lessons/.test(only.stdout), only.stdout.split("\n").find(l => /seeds:/.test(l)));

try { fs.rmSync(tmp, { recursive: true, force: true }); } catch (e) {}
const fails = results.filter(x => !x).length;
console.log("\n" + results.length + " steps, " + fails + " failed. Your working tree was not modified.");
process.exit(fails ? 1 : 0);
