#!/usr/bin/env node
/* The independence acceptance test.   npm run acceptance      (what it proves, and when it counts: docs/INDEPENDENCE.md)
 *
 * Each scenario copies the repository's tracked + untracked-but-not-ignored files into a scratch directory, puts each
 * "author" on their own git branch where they touch only their own files, merges the branches in BOTH orders, then
 * validates, builds, and (for features) runs every feature's own browser test. A scenario passes only if the merges are
 * clean, everything validates and builds, nothing either author did is lost, and the build is byte-identical whichever
 * order was used. Your working tree is never modified.
 *
 *   S1  two authors each create a lesson                                      merge either order
 *   S2  one modifies an existing lesson, the other adds one; also two modify two different lessons
 *   S3  one author creates a feature, touching nothing outside its own folder (so: no shared wiring)
 *   S4  one modifies an existing feature, the other creates a different feature
 *   S5  a lesson or a feature that breaks its contract is rejected, with a reason
 *   S6  the whole thing runs from a clean copy and never touches the Claude artifact
 *
 * Needs git, node, python (build.sh). Run  npm ci  first (the features' browser tests need Playwright). */
const fs = require("fs"), os = require("os"), path = require("path"), crypto = require("crypto");
const { execFileSync, spawnSync } = require("child_process");

const ROOT = path.join(__dirname, "..");
const ENV = { NODE_PATH: path.join(ROOT, "node_modules") };      // reuse the installed packages; nothing is fetched
const results = []; let scene = "";
const step = (name, ok, detail) => { results.push({ scene, ok: !!ok }); console.log((ok ? "PASS " : "FAIL ") + "[" + scene + "] " + name + (detail ? "  — " + detail : "")); };
const want = sc => !process.env.ACCEPT_ONLY || process.env.ACCEPT_ONLY.split(",").includes(sc);   // e.g. ACCEPT_ONLY=S3,S4
const sameSet = (a, b) => JSON.stringify([...a].sort()) === JSON.stringify([...b].sort());
const sha = f => fs.existsSync(f) ? crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex") : null;
const short = h => (h || "none").slice(0, 10);

// ---------------------------------------------------------------- the scratch repository
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "njs-accept-"));
const base = path.join(tmp, "repo");
const files = execFileSync("git", ["ls-files", "-co", "--exclude-standard", "-z"], { cwd: ROOT }).toString("utf8").split("\0").filter(Boolean);
for (const f of files) { const src = path.join(ROOT, f); if (!fs.existsSync(src)) continue; fs.mkdirSync(path.dirname(path.join(base, f)), { recursive: true }); fs.copyFileSync(src, path.join(base, f)); }
const run = (cmd, args, extraEnv) => spawnSync(cmd, args, { cwd: base, encoding: "utf8", env: { ...process.env, ...ENV, ...(extraEnv || {}) }, maxBuffer: 64 * 1024 * 1024 });
const git = (...a) => run("git", a);
const node = (...a) => run(process.execPath, a);
git("init", "-q", "-b", "main"); git("config", "user.email", "acceptance@example.invalid"); git("config", "user.name", "acceptance");
git("add", "-A"); git("commit", "-q", "-m", "base");

const checkout = b => { git("reset", "-q", "--hard"); git("clean", "-fdq"); git("switch", "-q", b); };
function author(name, change) {                                   // an author works on their own branch, from a clean main
  checkout("main"); git("switch", "-q", "-c", name);
  change();
  git("add", "-A"); git("commit", "-q", "-m", name);
  const touched = git("diff", "--name-only", "main", name).stdout.split("\n").filter(Boolean);
  checkout("main");
  return touched;
}
function merged(name, first, second) {                            // true if both merges are conflict-free
  checkout("main"); git("switch", "-q", "-c", name);
  const a = git("merge", "--no-edit", "-q", first); if (a.status) { git("merge", "--abort"); return false; }
  const b = git("merge", "--no-edit", "-q", second); if (b.status) { git("merge", "--abort"); return false; }
  return true;
}
function build(branch, withFeatureTests) {                        // validate + build the tree on `branch`
  checkout(branch);
  const out = { contracts: node("tools/validate-contracts.js"), index: node("tools/gen-index.js", "--check") };
  out.build = run("bash", ["build.sh"]); out.site = node("build_site.js");
  out.dataHash = sha(path.join(base, "site", "data.json")); out.featHash = sha(path.join(base, ".cache", "features.generated.js"));
  out.data = out.dataHash ? JSON.parse(fs.readFileSync(path.join(base, "site", "data.json"), "utf8")) : {};
  out.gen = fs.existsSync(path.join(base, ".cache", "features.generated.js")) ? fs.readFileSync(path.join(base, ".cache", "features.generated.js"), "utf8") : "";
  if (withFeatureTests) out.features = node("tests/features.test.js");
  out.ok = out.contracts.status === 0 && out.index.status === 0 && out.build.status === 0 && out.site.status === 0 && (!withFeatureTests || out.features.status === 0);
  return out;
}
const lastLine = r => ((r.stdout || "").trim().split("\n").pop() || (r.stderr || "").trim().slice(0, 160));
const readJ = f => JSON.parse(fs.readFileSync(path.join(base, f), "utf8"));
const writeJ = (f, o) => fs.writeFileSync(path.join(base, f), JSON.stringify(o));

// ---------------------------------------------------------------- what an author does
function addLesson(doc, topic, set) {                              // a conforming lesson, derived from a real one
  const L = readJ("seed/lesson_rg5.json"); L.id = doc; L.topicId = topic; L.title = "Acceptance " + topic;
  L.scenes.forEach(s => { if (s.kind === "quiz") s.setId = set; });
  const P = readJ("seed/regression_t5_mastery.json"); P.topicId = topic; P.items.forEach((it, i) => { it.id = topic + "-m-" + String(i + 1).padStart(2, "0"); it.topic = topic; });
  writeJ("seed/lesson_" + doc + ".json", L); writeJ("seed/" + set + ".json", P);
}
function reviseLesson(file, mark) { const L = readJ(file); L.version = "1.1"; L.traps = L.traps.concat([mark]); writeJ(file, L); }
const camel = id => id.replace(/-([a-z0-9])/g, (_, c) => c.toUpperCase());
function addFeature(id, title) {                                   // a feature, copied from the reference template and renamed
  const from = path.join(base, "src", "features", "ref-counter"), to = path.join(base, "src", "features", id);
  fs.mkdirSync(to, { recursive: true });
  for (const f of fs.readdirSync(from)) {
    let s = fs.readFileSync(path.join(from, f), "utf8");
    s = s.split("ref-counter").join(id).split("refCounter").join(camel(id)).split("Counter (reference feature)").join(title);
    fs.writeFileSync(path.join(to, f), s);
  }
}
function reviseFeature(id, mark) {
  const idx = path.join(base, "src", "features", id, "index.js"), mf = path.join(base, "src", "features", id, "feature.json");
  fs.writeFileSync(idx, fs.readFileSync(idx, "utf8").replace("A reference feature.", "A reference feature. " + mark));
  const m = JSON.parse(fs.readFileSync(mf, "utf8")); m.version = "1.1.0"; fs.writeFileSync(mf, JSON.stringify(m, null, 2) + "\n");
}
const within = (touched, prefixes) => touched.length > 0 && touched.every(f => prefixes.some(p => f === p || f.startsWith(p)));

// ================================================================ S1
scene = "S1";
if (want("S1")) {
  const A = author("s1-a", () => addLesson("acca1", "regression-t98", "regression_t98_mastery"));
  const B = author("s1-b", () => addLesson("accb1", "regression-t99", "regression_t99_mastery"));
  step("each author changed only their own two files", within(A, ["seed/lesson_acca1.json", "seed/regression_t98_mastery.json"]) && within(B, ["seed/lesson_accb1.json", "seed/regression_t99_mastery.json"]), A.join(",") + " | " + B.join(","));
  step("merging A then B is conflict-free", merged("s1-ab", "s1-a", "s1-b")); step("merging B then A is conflict-free", merged("s1-ba", "s1-b", "s1-a"));
  const r1 = build("s1-ab", false), r2 = build("s1-ba", false);
  step("the merged tree validates and builds (either order)", r1.ok && r2.ok, lastLine(r1.contracts));
  step("both new lessons are in the built site", !!(r1.data["lessons/acca1"] && r1.data["lessons/accb1"] && r2.data["lessons/acca1"] && r2.data["lessons/accb1"]));
  step("the build is byte-identical whichever order was used", !!r1.dataHash && r1.dataHash === r2.dataHash, short(r1.dataHash) + " vs " + short(r2.dataHash));
}
// ================================================================ S2
scene = "S2";
if (want("S2")) {
  const A = author("s2-a", () => reviseLesson("seed/lesson_rg5.json", "ACCEPTANCE-REVISION-A"));
  const B = author("s2-b", () => addLesson("accb2", "regression-t97", "regression_t97_mastery"));
  step("one author revised an existing lesson and touched only it", sameSet(A, ["seed/lesson_rg5.json"]), A.join(","));
  step("merging either order is conflict-free", merged("s2-ab", "s2-a", "s2-b") && merged("s2-ba", "s2-b", "s2-a"));
  const r1 = build("s2-ab", false), r2 = build("s2-ba", false);
  const L1 = r1.data["lessons/regressiont5"] || {};
  step("the revision AND the new lesson are both present (neither contribution is lost)", L1.version === "1.1" && (L1.traps || []).includes("ACCEPTANCE-REVISION-A") && !!r1.data["lessons/accb2"], "version=" + L1.version);
  step("the merged tree validates and builds, identically in either order", r1.ok && r2.ok && r1.dataHash === r2.dataHash, short(r1.dataHash) + " vs " + short(r2.dataHash));
  const C = author("s2-c", () => reviseLesson("seed/lesson_rg4.json", "ACCEPTANCE-REVISION-C")), D = author("s2-d", () => reviseLesson("seed/lesson_rg5.json", "ACCEPTANCE-REVISION-D"));
  step("two authors revising two different existing lessons merge cleanly and keep both revisions", merged("s2-cd", "s2-c", "s2-d") && (() => { const r = build("s2-cd", false); return r.ok && (r.data["lessons/regressiont4"].traps || []).includes("ACCEPTANCE-REVISION-C") && (r.data["lessons/regressiont5"].traps || []).includes("ACCEPTANCE-REVISION-D"); })());
}
// ================================================================ S3
scene = "S3";
if (want("S3")) {
  const G = author("s3-g", () => addFeature("acc-gpt-notes", "Notes (acceptance feature)"));
  step("the new feature touched only its own folder: no other feature's files, no shared wiring", within(G, ["src/features/acc-gpt-notes/"]), G.join(", "));
  const r = build("s3-g", true);
  step("validates, builds, and every feature's own browser test passes, including the new one", r.ok && /acc-gpt-notes/.test(r.features.stdout) && /PASS feature acc-gpt-notes/.test(r.features.stdout), lastLine(r.features));
  step("the feature is in the built app, registered by the generated block (no hand-edited list)", /registerFeature\(__manifest/.test(r.gen) && /"id":"acc-gpt-notes"/.test(r.gen));
}
// ================================================================ S4
scene = "S4";
if (want("S4")) {
  const A = author("s4-a", () => reviseFeature("ref-counter", "REVISED-BY-A."));
  const B = author("s4-b", () => addFeature("acc-claude-plan", "Plan (acceptance feature)"));
  step("one author modified an existing feature, the other created a different one, with disjoint files", within(A, ["src/features/ref-counter/"]) && within(B, ["src/features/acc-claude-plan/"]), A.join(",") + " | " + B.join(","));
  step("merging either order is conflict-free", merged("s4-ab", "s4-a", "s4-b") && merged("s4-ba", "s4-b", "s4-a"));
  const r1 = build("s4-ab", true), r2 = build("s4-ba", true);
  step("the merged app validates, builds, and every feature test passes (either order)", r1.ok && r2.ok, lastLine(r1.features));
  step("the modification and the new feature are both in the build", /REVISED-BY-A\./.test(r1.gen) && /"version":"1.1.0"/.test(r1.gen) && /"id":"acc-claude-plan"/.test(r1.gen));
  step("the build is byte-identical whichever order was used", !!r1.featHash && r1.featHash === r2.featHash && r1.dataHash === r2.dataHash, short(r1.featHash) + " vs " + short(r2.featHash));
}
// ================================================================ S5
scene = "S5";
if (want("S5")) {
  const rejects = (name, change, expectText) => {
    author("s5-" + name.replace(/\W+/g, "-").slice(0, 24), change);
    checkout("s5-" + name.replace(/\W+/g, "-").slice(0, 24));
    const v = node("tools/validate-contracts.js");
    step(name + " is rejected, with a reason", v.status === 1 && expectText.test(v.stdout), (v.stdout.split("\n").find(l => expectText.test(l)) || lastLine(v)).slice(0, 150));
  };
  rejects("a lesson with an unregistered visualisation and a theory scene without blocks", () => { addLesson("accbad", "regression-t96", "regression_t96_mastery"); const f = "seed/lesson_accbad.json", L = readJ(f); L.scenes.find(s => s.kind === "explore").viz = { type: "my-own-chart" }; delete L.scenes.find(s => s.kind === "theory").blocks; writeJ(f, L); }, /lesson_accbad[^]*?(blocks|allowed values)/);
  rejects("a feature whose code uses a storage key it did not declare", () => { addFeature("acc-bad-key", "Bad key"); const f = path.join(base, "src/features/acc-bad-key/index.js"); fs.writeFileSync(f, fs.readFileSync(f, "utf8").replace('store.get("count")', 'store.get("secret_key")')); }, /acc-bad-key[^]*secret_key/);
  rejects("a feature whose manifest id differs from its folder", () => { addFeature("acc-bad-id", "Bad id"); const f = path.join(base, "src/features/acc-bad-id/feature.json"), m = JSON.parse(fs.readFileSync(f, "utf8")); m.id = "something-else"; fs.writeFileSync(f, JSON.stringify(m)); }, /acc-bad-id[^]*must equal the folder/);
  rejects("a feature manifest with an invalid id", () => { addFeature("acc-bad-manifest", "Bad manifest"); const f = path.join(base, "src/features/acc-bad-manifest/feature.json"), m = JSON.parse(fs.readFileSync(f, "utf8")); m.tab = "yes"; fs.writeFileSync(f, JSON.stringify(m)); }, /acc-bad-manifest[^]*(boolean|violates)/);
}
// ================================================================ S6
scene = "S6";
if (want("S6")) {
  checkout("main");
  step("the scratch copy had no installed packages, no build output, no cache and no session files", !fs.existsSync(path.join(base, "node_modules")) && files.every(f => !/^(\.cache|site|app\.html|node_modules)\b/.test(f)) && files.every(f => !/\.local\.json$/.test(f)));
  const tooling = ["build.sh", "build_site.js", "check.sh", "test.js", "clicktest.js", ...fs.readdirSync(path.join(base, "tools")).map(f => "tools/" + f), ...fs.readdirSync(path.join(base, "tests")).map(f => "tests/" + f)];
  const leaks = tooling.filter(f => f !== "tools/acceptance.js" && /ArtifactData|api\.anthropic\.com/.test(fs.readFileSync(path.join(base, f), "utf8")));
  step("no build, check or test tool depends on the Claude artifact or the Anthropic API", leaks.length === 0, leaks.join(", ") || "none reference it");
  step("every command a contributor is told to run exists in package.json", ["check", "contracts", "build", "test", "acceptance"].every(k => readJ("package.json").scripts[k]));
}

try { fs.rmSync(tmp, { recursive: true, force: true }); } catch (e) {}
const failed = results.filter(r => !r.ok);
const by = {}; results.forEach(r => { by[r.scene] = by[r.scene] || { n: 0, bad: 0 }; by[r.scene].n++; if (!r.ok) by[r.scene].bad++; });
console.log("\n" + Object.entries(by).map(([k, v]) => k + (v.bad ? " FAILED " + v.bad + "/" + v.n : " ok " + v.n)).join("   "));
console.log(results.length + " steps, " + failed.length + " failed. Your working tree was not modified.");
process.exit(failed.length ? 1 : 0);
