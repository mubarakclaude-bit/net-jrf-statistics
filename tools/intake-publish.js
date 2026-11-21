/* Before and after an unattended intake run: everything that touches GitHub, done as the owner, never by the agent.
 *
 * Codex's Windows sandbox runs the agent as a separate sandbox user, with no access to the owner's GitHub credentials
 * (and an AI agent should not hold them anyway). So the agent only prepares content and commits it locally in a worktree
 * this module creates; this module then re-checks the work itself and publishes it:
 *
 *   prepare()  fetch origin, create a fresh worktree on a new branch from origin/main, npm ci in it, set the commit identity
 *   publish()  read the agent's result file; require exactly one new commit and a clean tree; re-run the agent's
 *              verification script (only a plain `python <script>.py` is accepted) and check.sh; then push, open the PR,
 *              wait for the Validate workflow on that exact commit, and merge only when it is green and merging is on
 *   cleanup()  remove the worktree (and the local branch, unless it was kept for the owner to inspect)
 *
 * Every command goes through an injectable runner, so tests drive it with a fake git, gh and npm. Standard library only. */
const fs = require("fs"), path = require("path"), { spawnSync } = require("child_process");

const WIN = process.platform === "win32";

/* The default runner. npm is a .cmd shim on Windows, which needs a shell; everything else runs directly. */
function realSh(cmd, args, opts) {
  const shell = WIN && cmd === "npm";
  const r = spawnSync(shell ? "npm.cmd" : cmd, shell ? args.map(a => /\s/.test(a) ? '"' + a + '"' : a) : args,
    { cwd: opts && opts.cwd, encoding: "utf8", maxBuffer: 64 * 1024 * 1024, timeout: (opts && opts.timeout) || 30 * 60 * 1000, windowsHide: true, shell });
  return { code: r.error ? -1 : r.status, out: ((r.stdout || "") + (r.stderr || "")).trim(), error: r.error && r.error.message };
}

function bashPath(env) {
  const e = env || process.env;
  if (e.INTAKE_BASH) return e.INTAKE_BASH;
  for (const p of ["C:/Program Files/Git/bin/bash.exe", "C:/Program Files/Git/usr/bin/bash.exe"]) if (WIN && fs.existsSync(p)) return p;
  return "bash";
}

const stampOf = d => d.toISOString().replace(/[-:]/g, "").replace(/\..*/, "").replace("T", "-");

function prepare(root, sh, now) {
  sh = sh || realSh;
  const stamp = stampOf(now || new Date()), branch = "content/intake-" + stamp, wt = path.join(root, ".cache", "run-" + stamp);
  const step = (what, cmd, args, cwd) => { const r = sh(cmd, args, { cwd }); if (r.code !== 0) throw new Error(what + " failed: " + (r.error || r.out).slice(0, 400)); return r; };
  step("git fetch", "git", ["fetch", "origin", "main"], root);
  step("git worktree add", "git", ["worktree", "add", wt, "-b", branch, "origin/main"], root);
  // The sandbox user cannot see the owner's global git config, so give the repository its own commit identity.
  for (const k of ["user.name", "user.email"]) {
    const local = sh("git", ["config", "--local", "--get", k], { cwd: root });
    if (local.code !== 0 || !local.out) {
      const g = sh("git", ["config", "--get", k], { cwd: root });
      if (g.code === 0 && g.out) step("git config " + k, "git", ["config", "--local", k, g.out], root);
    }
  }
  step("npm ci", "npm", ["ci", "--no-audit", "--no-fund"], wt);
  return { stamp, branch, wt };
}

/* What the agent may claim, checked before any of it is used. */
function readResult(file) {
  let r;
  try { r = JSON.parse(fs.readFileSync(file, "utf8")); } catch (e) { return { status: "invalid", reason: "no readable result file (" + e.message + ")" }; }
  if (!["ready", "stopped", "nothing"].includes(r.status)) return { status: "invalid", reason: "result status must be ready, stopped or nothing" };
  if (r.status !== "ready") return r;
  if (typeof r.title !== "string" || !r.title.trim()) return { status: "invalid", reason: "a ready result needs a title" };
  if (typeof r.body !== "string" || r.body.length < 40) return { status: "invalid", reason: "a ready result needs a PR body" };
  if (typeof r.verify !== "string" || !/^python3? [A-Za-z0-9_\-/]+\.py$/.test(r.verify.trim())) return { status: "invalid", reason: "verify must be exactly `python <script>.py`" };
  return Object.assign({}, r, { title: r.title.trim().slice(0, 120), verify: r.verify.trim() });
}

/* Returns { outcome, pr?, note } where outcome is one of: nothing, stopped, rejected, checks-failed, push-failed,
   pr-failed, ci-failed, left-open, merged. The worktree is always removed by the caller through cleanup(). */
function publish(prep, resultFile, mergeOn, sh, opts) {
  sh = sh || realSh;
  opts = opts || {};
  const wt = prep.wt, branch = prep.branch;
  const r = readResult(resultFile);
  if (r.status === "nothing") return { outcome: "nothing", note: "the agent found nothing to process" };
  if (r.status === "stopped") return { outcome: "stopped", note: "the agent stopped: " + (r.reason || "no reason given") };
  if (r.status === "invalid") return { outcome: "rejected", note: r.reason };

  const commits = sh("git", ["rev-list", "--count", "origin/main..HEAD"], { cwd: wt });
  if (commits.code !== 0 || commits.out.trim() !== "1") return { outcome: "rejected", note: "expected exactly one new commit, found " + (commits.out || "none") };
  const dirty = sh("git", ["status", "--porcelain"], { cwd: wt });
  if (dirty.code !== 0 || dirty.out.trim()) return { outcome: "rejected", note: "uncommitted changes left in the worktree" };

  const script = r.verify.split(" ")[1];
  const v = sh("python", ["-X", "utf8", script], { cwd: wt, timeout: 20 * 60 * 1000 });
  if (v.code !== 0) return { outcome: "checks-failed", note: script + " failed when re-run: " + v.out.slice(-600) };
  const c = sh(opts.bash || bashPath(), ["check.sh"], { cwd: wt, timeout: 20 * 60 * 1000 });
  if (c.code !== 0) return { outcome: "checks-failed", note: "check.sh failed when re-run: " + c.out.slice(-600) };

  const sha = sh("git", ["rev-parse", "HEAD"], { cwd: wt }).out.trim();
  const push = sh("git", ["push", "-u", "origin", branch], { cwd: wt });
  if (push.code !== 0) return { outcome: "push-failed", note: push.out.slice(-400) };
  const bodyFile = path.join(wt, "..", "pr-body-" + prep.stamp + ".md");
  fs.writeFileSync(bodyFile, r.body + "\n\n---\nPrepared by an unattended intake run (" + (opts.engine || "agent") + "); re-verified and published by `tools/intake-watch.js`.\n");
  const pr = sh("gh", ["pr", "create", "--base", "main", "--head", branch, "--title", r.title, "--body-file", bodyFile], { cwd: wt });
  try { fs.unlinkSync(bodyFile); } catch (e) { /* fine */ }
  if (pr.code !== 0) return { outcome: "pr-failed", note: pr.out.slice(-400) };
  const url = (pr.out.match(/https:\/\/github\.com\/\S+\/pull\/\d+/) || [])[0] || pr.out.trim();

  // Find the Validate run for this exact commit (it can take a moment to appear), then wait for it.
  let runId = null;
  for (let k = 0; k < (opts.findTries || 24) && !runId; k++) {
    const l = sh("gh", ["run", "list", "--branch", branch, "--workflow", "Validate", "--json", "databaseId,headSha,event"], { cwd: wt });
    try { const hit = JSON.parse(l.out || "[]").find(x => x.headSha === sha && x.event === "pull_request") || JSON.parse(l.out || "[]").find(x => x.headSha === sha); runId = hit && hit.databaseId; } catch (e) { /* retry */ }
    if (!runId && opts.wait !== false) spawnSync(process.execPath, ["-e", "setTimeout(()=>{},5000)"]);
  }
  if (!runId) return { outcome: "ci-failed", pr: url, note: "no Validate run appeared for " + sha };
  const w = sh("gh", ["run", "watch", String(runId), "--exit-status"], { cwd: wt, timeout: 60 * 60 * 1000 });
  if (w.code !== 0) return { outcome: "ci-failed", pr: url, note: "CI failed on " + sha.slice(0, 7) + "; PR left open" };
  if (!mergeOn) return { outcome: "left-open", pr: url, note: "CI green; merging is off, so the PR waits for review" };
  const m = sh("gh", ["pr", "merge", url, "--merge", "--match-head-commit", sha], { cwd: wt });
  if (m.code !== 0) return { outcome: "left-open", pr: url, note: "CI green but the merge failed: " + m.out.slice(-300) };
  return { outcome: "merged", pr: url, note: "CI green; merged" };
}

/* Remove the worktree. Keep the local branch when the work was not published, so the owner can look at it. */
function cleanup(root, prep, keepBranch, sh) {
  sh = sh || realSh;
  sh("git", ["worktree", "remove", "--force", prep.wt], { cwd: root });
  sh("git", ["worktree", "prune"], { cwd: root });
  if (!keepBranch) sh("git", ["branch", "-D", prep.branch], { cwd: root });
}

module.exports = { prepare, publish, cleanup, readResult, realSh, bashPath, stampOf };
