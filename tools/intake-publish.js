/* Before and after an unattended intake run: everything that touches GitHub, done as the owner, never by the agent.
 *
 * Codex's Windows sandbox runs the agent as a separate sandbox user, with no access to the owner's GitHub credentials
 * (and an AI agent should not hold them anyway). It cannot write git's metadata either: a worktree's index lives in the
 * main repository's .git, outside the sandbox. So the agent only prepares content in a worktree this module creates and
 * lists its files in the result; this module commits them, re-checks the work itself and publishes it:
 *
 *   prepare()  fetch origin, create a fresh worktree on a new branch from origin/main, npm ci in it, set the commit identity
 *   publish()  read the agent's result file; commit the files it lists (or accept the one commit an engine made itself);
 *              require a clean tree; re-run the agent's
 *              verification script (only a plain `python <script>.py` is accepted) and check.sh; then push, open the PR,
 *              wait for the Validate workflow on that exact commit, and merge only when it is green and merging is on
 *   cleanup()  remove the worktree (and the local branch, unless it was kept for the owner to inspect); a run that failed
 *              with unpublished changes keeps its worktree, so no work is thrown away
 *
 * A long document is done in batches: a run that adds part of the worksheet returns {status: "progress", done, total},
 * and a run that explains and re-solves part of a finished worksheet adds stage: "explain"; nothing is published, and the
 * watcher starts the next batch.
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

/* Windows PowerShell writes UTF-8 with a byte-order mark (Set-Content) or UTF-16LE (Out-File, >). Accept all three. */
function decodeText(buf) {
  if (buf.length >= 2 && buf[0] === 0xff && buf[1] === 0xfe) return buf.slice(2).toString("utf16le");
  if (buf.length >= 2 && buf[0] === 0xfe && buf[1] === 0xff) return Buffer.from(buf.slice(2)).swap16().toString("utf16le");
  const s = buf.toString("utf8");
  return s.charCodeAt(0) === 0xfeff ? s.slice(1) : s;
}

/* What the agent may claim, checked before any of it is used. */
function readResult(file) {
  let r;
  try { r = JSON.parse(decodeText(fs.readFileSync(file))); } catch (e) { return { status: "invalid", reason: "no readable result file (" + e.message + ")" }; }
  if (!["ready", "stopped", "nothing", "progress"].includes(r.status)) return { status: "invalid", reason: "result status must be ready, progress, stopped or nothing" };
  if (r.status === "progress" && !(Number.isInteger(r.done) && Number.isInteger(r.total) && r.done >= 0 && r.total > 0 && r.done <= r.total))
    return { status: "invalid", reason: "a progress result needs whole numbers done and total, with done <= total" };
  if (r.status !== "ready") return r;
  if (typeof r.title !== "string" || !r.title.trim()) return { status: "invalid", reason: "a ready result needs a title" };
  /* bodyFile: the pr-body.md that `intake.js build` wrote, read here as UTF-8. An agent that copied it through
     PowerShell's Get-Content turned "−" into "âˆ’" in the PR description (28 Nov 2026). Only a pr-body.md inside the
     intake folder is accepted, so a result cannot publish some other local file. */
  if (r.bodyFile !== undefined) {
    const dir = path.resolve(process.env.INTAKE_DIR || path.join(__dirname, "..", ".cache", "intake")), f = path.resolve(String(r.bodyFile));
    const rel = path.relative(dir, f);
    if (path.basename(f) !== "pr-body.md" || !rel || rel.startsWith("..") || path.isAbsolute(rel) || !fs.existsSync(f))
      return { status: "invalid", reason: "bodyFile must be the pr-body.md that build wrote in the intake folder" };
    r = Object.assign({}, r, { body: decodeText(fs.readFileSync(f)) + (typeof r.body === "string" && r.body.trim() ? "\n\n" + r.body.trim() : "") });
  }
  if (typeof r.body !== "string" || r.body.length < 40) return { status: "invalid", reason: "a ready result needs a PR body" };
  if (typeof r.verify !== "string" || !/^python3? [A-Za-z0-9_\-/]+\.py$/.test(r.verify.trim())) return { status: "invalid", reason: "verify must be exactly `python <script>.py`" };
  if (r.files !== undefined && !(Array.isArray(r.files) && r.files.length && r.files.every(okPath)))
    return { status: "invalid", reason: "files must be a list of repository paths, with nothing under .cache/ and no PDF, image or page text" };
  const files = r.files && r.files.map(p => p.trim().replace(/\\/g, "/"));
  return Object.assign({}, r, { title: r.title.trim().slice(0, 120), verify: r.verify.trim() }, files ? { files } : {});
}

/* A path the agent may ask to commit: relative, inside the worktree, and never source material or local state. */
function okPath(p) {
  if (typeof p !== "string" || !p.trim()) return false;
  const q = p.trim().replace(/\\/g, "/");
  return !q.startsWith("/") && !q.startsWith("-") && !/^[A-Za-z]:/.test(q) && !q.split("/").includes("..") &&
    !/^(\.cache|\.git|node_modules)(\/|$)/.test(q) && !/\.(pdf|png|jpe?g|gif|webp|txt)$/i.test(q);
}

/* Returns { outcome, pr?, note } where outcome is one of: nothing, stopped, rejected, checks-failed, push-failed,
   pr-failed, ci-failed, left-open, merged. The worktree is always removed by the caller through cleanup(). */
function publish(prep, resultFile, mergeOn, sh, opts) {
  sh = sh || realSh;
  opts = opts || {};
  const wt = prep.wt, branch = prep.branch;
  const r = readResult(resultFile);
  if (r.status === "nothing") return { outcome: "nothing", note: "the agent found nothing to process" };
  if (r.status === "progress") return { outcome: "progress", done: r.done, total: r.total, stage: r.stage === "explain" ? "explain" : "worksheet",
    note: "batch saved: " + r.done + " of " + r.total + (r.stage === "explain" ? " kept questions now explained and re-solved" : " questions now in the worksheet") };
  if (r.status === "stopped") return { outcome: "stopped", note: "the agent stopped: " + (r.reason || "no reason given") };
  if (r.status === "invalid") return { outcome: "rejected", note: r.reason };

  const commits = sh("git", ["rev-list", "--count", "origin/main..HEAD"], { cwd: wt });
  const n = commits.code === 0 ? commits.out.trim() : "?";
  if (n === "0") {
    if (!r.files) return { outcome: "rejected", note: "nothing was committed and the result lists no files" };
    const add = sh("git", ["add", "--"].concat(r.files), { cwd: wt });
    if (add.code !== 0) return { outcome: "rejected", note: "git add of the listed files failed: " + add.out.slice(-300) };
    const cm = sh("git", ["commit", "-m", r.title, "-m", "Source: " + (r.source || "not given") + ". Prepared by an unattended intake run (" +
      (opts.engine || "agent") + "); committed and published by tools/intake-watch.js."], { cwd: wt });
    if (cm.code !== 0) return { outcome: "rejected", note: "git commit failed: " + cm.out.slice(-300) };
    // Scratch files the agent left are removed, so the re-checks see exactly what was committed. Ignored files
    // (node_modules, __pycache__) stay.
    sh("git", ["clean", "-fd"], { cwd: wt });
  } else if (n !== "1") return { outcome: "rejected", note: "expected exactly one new commit, found " + (commits.out || "none") };
  const dirty = sh("git", ["status", "--porcelain"], { cwd: wt });
  if (dirty.code !== 0 || dirty.out.trim()) return { outcome: "rejected", note: "changes not in the commit (list them in files): " + dirty.out.trim().slice(0, 300) };

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
  /* Prefer the pull_request run. The push run for the same commit appears first and is then cancelled by the PR's run
     (one concurrency group), so watching it reported "CI failed" on PR #154 while the real run was still going. Fall
     back to the push run only when no pull_request run appears, and if the watched run ends cancelled, watch the other. */
  const runs = () => { const l = sh("gh", ["run", "list", "--branch", branch, "--workflow", "Validate", "--json", "databaseId,headSha,event"], { cwd: wt }); try { return JSON.parse(l.out || "[]").filter(x => x.headSha === sha); } catch (e) { return []; } };
  const pause = () => { if (opts.wait !== false) spawnSync(process.execPath, ["-e", "setTimeout(()=>{},5000)"]); };
  let runId = null, any = null;
  for (let k = 0; k < (opts.findTries || 24) && !runId; k++) {
    const rs = runs(), pr_ = rs.find(x => x.event === "pull_request");
    if (rs.length) any = any || rs[0].databaseId;
    if (pr_) runId = pr_.databaseId; else pause();
  }
  runId = runId || any;
  if (!runId) return { outcome: "ci-failed", pr: url, note: "no Validate run appeared for " + sha };
  const watched = new Set();
  let w;
  for (;;) {
    watched.add(runId);
    w = sh("gh", ["run", "watch", String(runId), "--exit-status"], { cwd: wt, timeout: 60 * 60 * 1000 });
    if (w.code === 0) break;
    const v = sh("gh", ["run", "view", String(runId), "--json", "conclusion"], { cwd: wt });
    let conclusion = ""; try { conclusion = JSON.parse(v.out || "{}").conclusion || ""; } catch (e) { /* treat as failed */ }
    const other = conclusion === "cancelled" && runs().find(x => !watched.has(x.databaseId));
    if (!other) break;
    runId = other.databaseId;
  }
  if (w.code !== 0) return { outcome: "ci-failed", pr: url, note: "CI failed on " + sha.slice(0, 7) + "; PR left open" };
  if (!mergeOn) return { outcome: "left-open", pr: url, note: "CI green; merging is off, so the PR waits for review" };
  const m = sh("gh", ["pr", "merge", url, "--merge", "--match-head-commit", sha], { cwd: wt });
  if (m.code !== 0) return { outcome: "left-open", pr: url, note: "CI green but the merge failed: " + m.out.slice(-300) };
  return { outcome: "merged", pr: url, note: "CI green; merged" };
}

/* Remove the worktree. Keep the local branch when the work was not published, so the owner can look at it. */
function cleanup(root, prep, keepBranch, sh, keepTree) {
  sh = sh || realSh;
  if (keepTree) return;
  sh("git", ["worktree", "remove", "--force", prep.wt], { cwd: root });
  sh("git", ["worktree", "prune"], { cwd: root });
  if (!keepBranch) sh("git", ["branch", "-D", prep.branch], { cwd: root });
}

/* Whether a run's worktree holds work that was not published (so it is worth keeping). */
function hasChanges(prep, sh) {
  const st = (sh || realSh)("git", ["status", "--porcelain"], { cwd: prep.wt });
  return st.code === 0 && !!st.out.trim();
}

module.exports = { prepare, publish, cleanup, hasChanges, okPath, readResult, decodeText, realSh, bashPath, stampOf };
