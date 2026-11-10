#!/usr/bin/env node
// Runs the verification scripts (verify_*.py) a change touched, so CI enforces the rule "numbers are computed by a script,
// never by hand" for an assistant that cannot run a shell.
//   node tools/run-verifiers.js [--all] [<base-ref>]      (default base: origin/main)
// A verifier counts as touched when its own file changed against the base. Exit 1 if any fails. With nothing touched it
// says so and exits 0.
const { execFileSync, spawnSync } = require("child_process");
const fs = require("fs");

const args = process.argv.slice(2);
const all = args.includes("--all");
const base = args.find(a => !a.startsWith("--")) || "origin/main";

let files;
if (all) files = fs.readdirSync(".").filter(f => /^verify_.*\.py$/.test(f));
else {
  let out;
  try { out = execFileSync("git", ["diff", "--name-only", base + "...HEAD"], { encoding: "utf8" }); }
  catch (e) { console.error("FAILED: cannot diff against " + base + ": " + String(e.message).split("\n")[0]); process.exit(1); }
  files = out.split("\n").filter(f => /^verify_[^/]*\.py$/.test(f) && fs.existsSync(f));
}
if (!files.length) { console.log("no verification scripts changed; nothing to run"); process.exit(0); }

const py = ["python3", "python"].find(c => spawnSync(c, ["-c", "import sys;sys.exit(0 if sys.version_info[0]==3 else 1)"]).status === 0);
if (!py) { console.error("FAILED: no working Python 3"); process.exit(1); }

let bad = 0;
for (const f of files) {
  const r = spawnSync(py, [f], { encoding: "utf8", env: Object.assign({}, process.env, { PYTHONIOENCODING: "utf-8" }) });
  const ok = r.status === 0;
  console.log((ok ? "ok    " : "FAIL  ") + f);
  if (!ok) { bad++; console.log(((r.stdout || "") + (r.stderr || "")).split("\n").slice(-15).join("\n")); }
}
process.exit(bad ? 1 : 0);
