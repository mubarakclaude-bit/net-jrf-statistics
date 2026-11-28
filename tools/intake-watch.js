#!/usr/bin/env node
/* Watch the owner's source folder and start an unattended intake run when a new PDF is ready.
 *
 *   node tools/intake-watch.js [--folder "<dir>"] [--agent codex|claude|none] [--model <name>] [--command "<cmd>"]
 *                              [--interval 300] [--settle 30] [--max-runs-per-day 6] [--once] [--merge | --no-merge]
 *
 * What it does, on a folder change or every --interval seconds:
 *   1. waits until every PDF in the folder has stopped changing (its mtime is at least --settle seconds old and its size
 *      holds steady), so a half-copied download is never read;
 *   2. asks tools/intake.js plan() what is left to process: new files, files already started; it skips what is already
 *      in the app (tools/intake-sources*), personal, unreadable or duplicate files;
 *   3. if anything is left and no run is active, prepares a fresh worktree on a new branch (tools/intake-publish.js), and
 *      starts ONE agent run there with the brief in tools/intake-run.md. The agent processes one document: reads, solves,
 *      verifies, builds and commits locally, then writes a result file. It never touches GitHub;
 *   4. after the agent exits, re-runs the agent's verification script and check.sh itself, and only then pushes, opens
 *      the PR, waits for CI on that commit, and merges when green and merging is on. Anything that fails stays local,
 *      with a note in .cache/intake/watch-notes.md.
 *
 * Settings: .cache/intake/watch.json (local, never committed) holds the defaults, so the engine, the model or the folder
 * can be changed by editing one file, with no change to how the watcher is started:
 *   { "folder": "C:/Muhavin/NET JRF", "agent": "codex", "model": null, "reasoningEffort": "high", "sandbox": "workspace-write", "merge": null,
 *     "interval": 300, "settle": 30, "maxRunsPerDay": 6 }
 * A command-line flag overrides the file for that start; --show-settings prints what is in force and exits.
 * "model": null lets the engine use its own default (Codex: the model in ~/.codex/config.toml, else its built-in one).
 *
 * Engines (--agent; the default is codex):
 *   claude   Claude Code's CLI:  claude -p --permission-mode acceptEdits --allowedTools ...  (brief on stdin)
 *   codex    OpenAI Codex CLI:   codex exec -s workspace-write -c approval_policy="never" (network on) -  (brief on stdin)
 *            (the owner's OpenAI key or ChatGPT login; needs Codex's Windows sandbox set up, else see "sandbox")
 *   none     only report what would run
 *   --command "<cmd>" runs any other command through the shell, with the brief's path in INTAKE_PROMPT_FILE.
 * The engine must be installed and logged in by the owner; this script never handles a key.
 *
 * Merging: the watcher merges a run's green PR only when merging is on. It is on by default for claude and off by
 * default for codex, until a few Codex runs have been checked: --merge / --no-merge / "merge" in watch.json override.
 * With merging off each PR is left open and listed in .cache/intake/watch-notes.md.
 *
 * --once checks one time and exits (for Windows Task Scheduler or any other scheduler). Without it, it keeps watching.
 * Everything it writes stays in .cache/intake/: watch.log, run.lock, runs/<time>.log. Standard library only. */
const fs = require("fs"), path = require("path"), { spawn } = require("child_process");

const ROOT = process.env.CONTENT_ROOT ? path.resolve(process.env.CONTENT_ROOT) : path.join(__dirname, "..");
const DIR = process.env.INTAKE_DIR ? path.resolve(process.env.INTAKE_DIR) : path.join(ROOT, ".cache", "intake");
const BRIEF = path.join(ROOT, "tools", "intake-run.md");
const LOCK = () => path.join(DIR, "run.lock");
const LOG = () => path.join(DIR, "watch.log");
const STALE_LOCK_MS = 8 * 3600 * 1000;           // a run that has not finished in 8 hours is treated as dead

function log(msg) {
  const line = new Date().toISOString() + "  " + msg;
  console.log(line);
  try { fs.mkdirSync(DIR, { recursive: true }); fs.appendFileSync(LOG(), line + "\n"); } catch (e) { /* console is enough */ }
}

/* ------------------------------------------------------------------ the decisions, kept pure so they can be tested */
function settled(stat, now, settleSec, sizeAgain) {
  return now - stat.mtimeMs >= settleSec * 1000 && stat.size > 0 && sizeAgain === stat.size;
}

function lockState(now) {
  try {
    const l = JSON.parse(fs.readFileSync(LOCK(), "utf8"));
    if (now - l.started > STALE_LOCK_MS) return { locked: false, stale: l };
    let alive = true;
    try { process.kill(l.pid, 0); } catch (e) { alive = e.code === "EPERM"; }
    return alive ? { locked: true, lock: l } : { locked: false, stale: l };
  } catch (e) { return { locked: false }; }
}

/* Two daily limits. Publications (pushed PRs) cost Vercel deployments when merged; agent runs cost the owner's OpenAI or
   Claude allowance. Publications are recorded in published.log; agent runs are the run logs, named <yyyymmdd>-<hhmmss>.log. */
const PUBLISHED = () => path.join(DIR, "published.log");
function publishedToday(now) {
  const day = new Date(now).toISOString().slice(0, 10);
  try { return fs.readFileSync(PUBLISHED(), "utf8").split("\n").filter(l => l.startsWith(day)).length; } catch (e) { return 0; }
}
function agentRunsToday(now) {
  const day = new Date(now).toISOString().slice(0, 10).replace(/-/g, "");
  try { return fs.readdirSync(path.join(DIR, "runs")).filter(f => f.startsWith(day + "-")).length; } catch (e) { return 0; }
}

/* The engine's own usage limit. On 28 Nov 2026 the ChatGPT account behind Codex ran out ("You've hit your usage limit
   ... try again at Dec 21st, 2026 11:04 PM") and the watcher started 12 more runs in 7 minutes, each failing in seconds,
   until its daily cap stopped it; the next day would have repeated that. A run that ends with that message and no
   result pauses the watcher until the time the engine gives (6 hours if it gives none), recorded in paused.json. */
const PAUSED = () => path.join(DIR, "paused.json");
const LIMIT_RX = /hit your usage limit|usage limit (?:reached|exceeded)|quota (?:exceeded|exhausted)|insufficient_quota|rate limit reached for/i;
function usageLimit(text, now) {
  if (!LIMIT_RX.test(text || "")) return null;
  const m = String(text).match(/try again (?:at|after|on) (.+?)(?:\.\s|\.$|\n|$)/i);
  let until = m ? Date.parse(m[1].replace(/(\d+)(st|nd|rd|th)\b/, "$1").trim()) : NaN;
  if (!Number.isFinite(until) || until <= now) until = now + 6 * 3600 * 1000;
  return { until, message: (String(text).match(/[^\n]*(?:usage limit|quota|rate limit)[^\n]*/i) || [""])[0].trim().slice(0, 300) };
}
function pausedState(now) {
  try { const p = JSON.parse(fs.readFileSync(PAUSED(), "utf8")); if (p.until > now) return p; fs.unlinkSync(PAUSED()); } catch (e) { /* not paused */ }
  return null;
}

function decide({ todo, unsettled, locked, today, max, runs, maxRuns, paused }) {
  if (unsettled.length) return { start: false, why: "waiting for " + unsettled.join(", ") + " to finish copying" };
  if (locked) return { start: false, why: "a run is already active" };
  if (!todo.length) return { start: false, why: "nothing to process" };
  if (paused) return { start: false, why: "paused: " + (paused.engine || "the engine") + "'s usage limit until " + new Date(paused.until).toISOString().slice(0, 16).replace("T", " ") + " UTC; " + todo.length + " file(s) wait" };
  if (today >= max) return { start: false, why: "daily limit of " + max + " published PRs reached; " + todo.length + " file(s) wait for tomorrow" };
  if (maxRuns && runs >= maxRuns) return { start: false, why: "daily cap of " + maxRuns + " agent runs reached; " + todo.length + " file(s) wait for tomorrow" };
  return { start: true, why: todo.length + " file(s) to process, first " + todo[0].name + " (" + todo[0].kind + ")" };
}

/* An npm-installed CLI is a .cmd shim on Windows, which spawn() cannot start without a shell, and a shell mangles a long
   multi-line brief. So run the package's own Node launcher with this Node, and send the brief on stdin. Elsewhere, or if
   the launcher is not found, run the command by name. INTAKE_<NAME>_JS overrides the launcher path. */
function launcher(name, pkgRel, env) {
  const override = (env || process.env)["INTAKE_" + name.toUpperCase() + "_JS"];
  const roots = [override].concat(process.platform === "win32" && (env || process.env).APPDATA ? [path.join((env || process.env).APPDATA, "npm", "node_modules", pkgRel)] : []);
  const js = roots.find(r => r && fs.existsSync(r));
  return js ? { cmd: process.execPath, pre: [js] } : { cmd: name, pre: [] };
}

function engineCommand(agent, briefText, custom, folder, env, model, sandbox, workdir, extraDirs, effort) {
  if (custom) return { shell: true, cmd: custom, args: [], stdin: null };
  if (agent === "claude") {
    const l = launcher("claude", path.join("@anthropic-ai", "claude-code", "cli.js"), env);
    return { cmd: l.cmd, args: l.pre.concat(["-p", "--permission-mode", "acceptEdits",
      "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch"]).concat(model ? ["--model", model] : []), stdin: briefText };
  }
  // Codex CLI 0.171. --approve-for-me cannot be combined with --sandbox and in practice left runs read-only, so the
  // sandbox is named explicitly and approvals are off (an unattended run has nobody to ask). workspace-write: writes only
  // inside the run's worktree, the source folder and the shared intake folder. The agent never needs GitHub: the watcher
  // publishes (tools/intake-publish.js). danger-full-access: no sandbox at all, an owner-only choice in watch.json.
  // "-" reads the brief from stdin.
  if (agent === "codex") {
    const l = launcher("codex", path.join("@openai", "codex", "bin", "codex.js"), env);
    const sb = sandbox || "workspace-write";
    const dirs = [folder].concat(extraDirs || []).filter(Boolean);
    const confine = sb === "workspace-write" ? ["-c", "sandbox_workspace_write.network_access=true"].concat(...dirs.map(d => ["--add-dir", d])) : [];
    // `codex exec` otherwise runs with reasoning effort "none", which ends a long intake task after a few commands.
    const think = ["-c", "model_reasoning_effort=\"" + (effort || "high") + "\""];
    return { cmd: l.cmd, args: l.pre.concat(["exec", "-s", sb, "-c", "approval_policy=\"never\""]).concat(think).concat(confine)
      .concat(["-C", workdir || ROOT]).concat(model ? ["-m", model] : []).concat(["-"]), stdin: briefText };
  }
  return null;
}

/* ------------------------------------------------------------------ one check */
function listPdfs(folder) {
  return fs.readdirSync(folder).filter(x => /\.pdf$/i.test(x)).map(n => ({ name: n, file: path.join(folder, n), stat: fs.statSync(path.join(folder, n)) }));
}

function tick(opts, planner) {
  const now = Date.now();
  const files = listPdfs(opts.folder);
  const unsettled = files.filter(f => {
    const again = (() => { try { return fs.statSync(f.file).size; } catch (e) { return -1; } })();
    return !settled(f.stat, now, opts.settle, again);
  }).map(f => f.name);
  const ls = lockState(now);
  if (ls.stale) { log("removing a stale lock from pid " + ls.stale.pid); try { fs.unlinkSync(LOCK()); } catch (e) { /* gone */ } }
  let todo = [];
  if (!unsettled.length && !ls.locked) todo = planner(opts.folder).todo;
  const d = decide({ todo, unsettled, locked: ls.locked, today: publishedToday(now), max: opts.max, runs: agentRunsToday(now), maxRuns: opts.maxRuns, paused: pausedState(now) });
  return Object.assign({ todo }, d);
}

/* Codex on Windows silently falls back to a read-only sandbox when its sandbox backend is not set up, and a read-only
   run cannot do intake. Ask `codex doctor` first and refuse to start, with a note for the owner, rather than spend a run.
   The answer is cached for 30 minutes so the 5-minute poll does not run the doctor every time. */
let preflightCache = null;
const NOTES = () => path.join(DIR, "watch-notes.md");
function codexPreflight(opts, runDoctor) {
  if (opts.command || opts.agent !== "codex" || (opts.sandbox || "workspace-write") !== "workspace-write") return { ok: true };
  if (!runDoctor && preflightCache && Date.now() - preflightCache.at < 30 * 60 * 1000) return preflightCache.result;
  let out = "";
  try {
    if (runDoctor) out = runDoctor();
    else {
      const l = launcher("codex", path.join("@openai", "codex", "bin", "codex.js"));
      out = require("child_process").spawnSync(l.cmd, l.pre.concat(["doctor"]), { encoding: "utf8", timeout: 120000, windowsHide: true }).stdout || "";
    }
  } catch (e) { out = ""; }
  const m = out.match(/sandbox backend\s+(\S+)/i);
  const result = m && /^disabled$/i.test(m[1])
    ? { ok: false, why: "Codex's sandbox backend is disabled on this computer, so a workspace-write run would fall back to read-only and could not write anything" }
    : { ok: true, why: m ? "sandbox backend " + m[1] : "sandbox backend not reported; starting anyway" };
  if (!runDoctor) preflightCache = { at: Date.now(), result };
  return result;
}

/* Anything written to watch-notes.md (a PR to review, a stop, a failure) also raises a Windows notification, so a stalled
   run is seen within minutes rather than the next morning (on 27 Nov 2026 a stop went unseen for 12 hours). The text
   goes through environment variables, never into the script. "notify": false in watch.json turns it off. */
const TOAST = [
  "$null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]",
  "$t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)",
  "$x = $t.GetElementsByTagName('text')",
  "$null = $x.Item(0).AppendChild($t.CreateTextNode($env:INTAKE_TOAST_TITLE))",
  "$null = $x.Item(1).AppendChild($t.CreateTextNode($env:INTAKE_TOAST_TEXT))",
  "$app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe'",
  "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show([Windows.UI.Notifications.ToastNotification]::new($t))"].join("; ");
function toast(title, text) {
  if (process.platform !== "win32") return;
  try {
    const env = Object.assign({}, process.env, { INTAKE_TOAST_TITLE: title.slice(0, 120), INTAKE_TOAST_TEXT: text.slice(0, 250) });
    const p = require("child_process").spawn("powershell.exe", ["-NoProfile", "-NonInteractive", "-EncodedCommand", Buffer.from(TOAST, "utf16le").toString("base64")],
      { env, detached: true, stdio: "ignore", windowsHide: true });
    p.on("error", () => {}); p.unref();
  } catch (e) { /* a notification is a convenience; the note and the log have it */ }
}
let notifier = toast;
function setNotifier(fn) { notifier = fn || (() => {}); }
function noteOnce(text) {
  try {
    const cur = fs.existsSync(NOTES()) ? fs.readFileSync(NOTES(), "utf8") : "";
    const head = text.split("\n")[0];
    if (!cur.includes(head)) {
      fs.appendFileSync(NOTES(), (cur ? "\n" : "") + text + "\n");
      notifier("NET JRF intake: " + head.replace(/^#+\s*/, ""), text.split("\n").slice(1).join(" ").replace(/\s+/g, " ").trim() || "See .cache/intake/watch-notes.md");
    }
  } catch (e) { /* the log has it too */ }
}

/* Once a document's PR exists, move its PDF into <folder>/Done ("doneFolder" in watch.json; null keeps it in place), so
   the folder shows what is left and finished files are never hashed again. A clash gets a " (2)" suffix. */
function moveToDone(folder, file, sub) {
  const dir = path.join(folder, sub);
  fs.mkdirSync(dir, { recursive: true });
  const ext = path.extname(file), base = path.basename(file, ext);
  let target = path.join(dir, base + ext);
  for (let k = 2; fs.existsSync(target); k++) target = path.join(dir, base + " (" + k + ")" + ext);
  fs.renameSync(file, target);
  return target;
}

function start(opts, onExit, pick) {
  if (pick && !pick.file && pick.name) pick = Object.assign({}, pick, { file: path.join(opts.folder, pick.name) });
  const pf = (opts.preflight || codexPreflight)(opts);
  if (!pf.ok) {
    log("not starting: " + pf.why + ". See .cache/intake/watch-notes.md");
    noteOnce("## Codex cannot write on this computer yet\n\n" + pf.why + ". Choose one, then the watcher starts runs by itself:\n\n" +
      "- A (recommended): set up Codex's Windows sandbox once, as administrator, in your own terminal. It creates local accounts and firewall rules; then runs can write only inside the repository and the source folder.\n" +
      "- B: set \"sandbox\": \"danger-full-access\" in .cache/intake/watch.json. Codex then runs with your full user permissions and no sandbox. Your decision only.\n" +
      "- C: set \"agent\": \"claude\" after installing Claude Code's CLI.");
    onExit && onExit(null);
    return null;
  }
  const brief = fs.readFileSync(BRIEF, "utf8");
  if (!engineCommand(opts.agent, brief, opts.command, opts.folder)) { log("would start a run now, but no engine is set (--agent claude|codex or --command)"); onExit && onExit(null); return null; }
  const P = opts.publisher || require("./intake-publish.js");
  let prep;
  try { prep = P.prepare(ROOT, opts.sh); } catch (e) {
    log("could not prepare a worktree: " + e.message);
    noteOnce("## Preparing a run failed (" + new Date().toISOString().slice(0, 10) + ")\n\n" + e.message);
    onExit && onExit(null);
    return null;
  }
  fs.mkdirSync(path.join(DIR, "runs"), { recursive: true });
  fs.mkdirSync(path.join(DIR, "results"), { recursive: true });
  const stamp = prep.stamp;
  const resultFile = path.join(DIR, "results", stamp + ".json");
  const eng = engineCommand(opts.agent, brief, opts.command, opts.folder, undefined, opts.model, opts.sandbox, prep.wt, [DIR], opts.effort);
  const out = fs.openSync(path.join(DIR, "runs", stamp + ".log"), "a");
  const env = Object.assign({}, process.env, { INTAKE_FOLDER: opts.folder, INTAKE_PROMPT_FILE: path.join(prep.wt, "tools", "intake-run.md"),
    INTAKE_DIR: DIR, INTAKE_RESULT: resultFile, INTAKE_WORKTREE: prep.wt,
    // Python writes UTF-8 by default, so ∩, ∪ and ᶜ survive a worksheet saved from a script.
    PYTHONUTF8: "1", PYTHONIOENCODING: "utf-8",
    // The document the watcher chose, so the agent does not rescan the whole folder.
    INTAKE_PICK: pick ? pick.file : "", INTAKE_PICK_KIND: pick ? pick.kind || "" : "", INTAKE_PICK_ID: pick && pick.sha256 ? pick.sha256.slice(0, 12) : "" });
  /* Git Bash on the agent's PATH: Codex's shell had none, so `bash check.sh` and `npm run build` (which calls bash)
     failed and a run spent minutes looking for it (28 Nov 2026). Same key spelling as the parent ("Path" on Windows). */
  const bash = P.bashPath ? P.bashPath() : "bash";
  if (path.isAbsolute(bash)) {
    const pk = Object.keys(env).find(k => k.toUpperCase() === "PATH") || "PATH";
    env[pk] = path.dirname(bash) + path.delimiter + (env[pk] || "");
  }
  const child = spawn(eng.cmd, eng.args, { cwd: prep.wt, env, shell: !!eng.shell, stdio: [eng.stdin ? "pipe" : "ignore", out, out], windowsHide: true });
  if (eng.stdin) { child.stdin.on("error", () => { /* the engine exited early; its log says why */ }); child.stdin.end(eng.stdin); }
  let failedToStart = false;
  child.on("error", e => { failedToStart = true; log("could not start " + eng.cmd + ": " + e.message + " (is it installed and on PATH?)"); });
  fs.writeFileSync(LOCK(), JSON.stringify({ pid: child.pid, started: Date.now(), engine: opts.command || opts.agent, log: "runs/" + stamp + ".log", worktree: prep.wt }));
  log("started run (" + (opts.command || opts.agent) + (opts.model ? ", model " + opts.model : "") + (mergeOn(opts) ? ", merges green PRs" : ", PRs left open for review") + ") in " + prep.wt + ", pid " + child.pid + ", log .cache/intake/runs/" + stamp + ".log");
  child.on("close", code => {
    log("agent finished with exit code " + code + "; publishing");
    let res;
    const limited = !fs.existsSync(resultFile) && (() => { try { return usageLimit(fs.readFileSync(path.join(DIR, "runs", stamp + ".log"), "utf8").slice(-20000), Date.now()); } catch (e) { return null; } })();
    if (limited) {
      const engine = opts.command ? "the engine" : opts.agent;
      try { fs.writeFileSync(PAUSED(), JSON.stringify({ until: limited.until, engine, message: limited.message, since: new Date().toISOString() })); } catch (e) { /* the log has it */ }
      res = { outcome: "usage-limit", until: limited.until, note: engine + " reports its usage limit (" + limited.message + "); no runs until " + new Date(limited.until).toISOString().slice(0, 16).replace("T", " ") + " UTC" };
    } else {
      try { res = failedToStart ? { outcome: "rejected", note: "the engine did not start" } : P.publish(prep, resultFile, mergeOn(opts), opts.sh, { engine: opts.command || opts.agent }); }
      catch (e) { res = { outcome: "rejected", note: "publishing failed: " + e.message }; }
    }
    const pushed = ["left-open", "merged", "ci-failed", "pr-failed"].includes(res.outcome);
    // Moved once the branch is on GitHub, even if the PR or CI then failed: the work is there to finish by hand, and
    // leaving the file would make the next check start the same document again.
    if (pick && pick.file && opts.done !== null && pushed) {
      try { const to = moveToDone(opts.folder, pick.file, opts.done || "Done"); log("moved " + path.basename(pick.file) + " to " + to); res.movedTo = to; }
      catch (e) { log("could not move " + path.basename(pick.file) + " to the Done folder: " + e.message); }
    }
    const quiet = ["nothing", "stopped", "progress", "usage-limit"].includes(res.outcome);
    // A run that ended without publishing but left changes keeps its worktree, so the work is not thrown away.
    let keepTree = false;
    if (!pushed && !["progress", "nothing"].includes(res.outcome) && P.hasChanges) { try { keepTree = P.hasChanges(prep, opts.sh); } catch (e) { /* remove it */ } }
    try { P.cleanup(ROOT, prep, (!pushed && !quiet) || keepTree, opts.sh, keepTree); } catch (e) { log("cleanup: " + e.message); }
    if (keepTree) { log("kept " + prep.wt + " (branch " + prep.branch + "): it holds this run's unpublished changes"); res.kept = prep.wt; }
    if (pushed) { try { fs.appendFileSync(PUBLISHED(), new Date().toISOString() + "  " + res.outcome + "  " + (res.pr || "") + "\n"); } catch (e) { /* log has it */ } }
    log("run " + stamp + ": " + res.outcome + (res.pr ? " " + res.pr : "") + " — " + res.note);
    if (res.outcome === "usage-limit") noteOnce("## Paused until " + new Date(res.until).toISOString().slice(0, 10) + ": the engine's usage limit\n\n" + res.note +
      ". The watcher keeps polling and starts again by itself then. To go on sooner, raise that account's plan, or set \"agent\" in watch.json to the other engine and delete .cache/intake/paused.json.");
    else if (res.outcome !== "nothing" && res.outcome !== "progress") noteOnce("## Run " + stamp + ": " + res.outcome + "\n\n" + (res.pr ? "PR: " + res.pr + "\n\n" : "") + res.note +
      (pushed ? "" : res.outcome === "stopped" ? "" : "\n\nThe local branch " + prep.branch + " was kept for inspection."));
    try { fs.unlinkSync(LOCK()); } catch (e) { /* already gone */ }
    onExit && onExit(code, res);
  });
  return child;
}

/* One check: start a run if the decision says so. After a run that saved a batch ("progress"), start the next batch of
   the same document at once, even with --once, up to maxBatches in a row, so one start finishes one document. */
function makeChecker(opts, planner, startFn, schedule) {
  let batches = 0;
  const check = (reason) => {
    let r;
    try { r = tick(opts, planner); } catch (e) { log("check failed: " + e.message); return; }
    log((reason ? reason + ": " : "") + r.why);
    if (!r.start) return;
    startFn(opts, (code, res) => {
      if (res && res.outcome === "progress" && batches + 1 < (opts.maxBatches || 8)) { batches++; schedule(() => check("next batch (" + res.done + "/" + res.total + ")"), 5000); return; }
      if (res && res.outcome === "progress") log("stopping after " + (opts.maxBatches || 8) + " batches in a row; the next check resumes the document");
      batches = 0;
      if (!opts.once) schedule(() => check("after the run"), 60 * 1000);
    }, r.todo && r.todo[0]);
  };
  return check;
}

/* Merge only where the owner has seen enough: on for Claude, off for Codex until --merge. */
function mergeOn(opts) {
  if (opts.merge === true || opts.merge === false) return opts.merge;
  return opts.agent !== "codex";
}

/* ------------------------------------------------------------------ command line */
const SETTINGS = () => path.join(DIR, "watch.json");
const DEFAULTS = { agent: "codex", model: null, effort: "high", merge: null, done: "Done", interval: 300, settle: 30, max: 6, maxRuns: 30, maxBatches: 8, once: false };

function normalise(f) {
  const o = {};
  for (const k of ["folder", "agent", "model", "sandbox", "command", "merge", "interval", "settle"]) if (f && f[k] !== undefined) o[k] = f[k];
  if (f && f.doneFolder !== undefined) o.done = f.doneFolder;
  if (f && f.reasoningEffort !== undefined) o.effort = f.reasoningEffort;
  if (f && f.maxRunsPerDay !== undefined) o.max = f.maxRunsPerDay;            // the old name for the publication limit
  if (f && f.maxPublishesPerDay !== undefined) o.max = f.maxPublishesPerDay;
  if (f && f.maxAgentRunsPerDay !== undefined) o.maxRuns = f.maxAgentRunsPerDay;
  if (f && f.maxBatchesInARow !== undefined) o.maxBatches = f.maxBatchesInARow;
  if (f && f.notify !== undefined) o.notify = f.notify;
  return o;
}

/* A missing file means defaults. A broken one is an error the owner must see: the watcher refuses to start rather than
   quietly run with settings they did not choose. */
function loadSettings() {
  if (!fs.existsSync(SETTINGS())) return {};
  try { return normalise(JSON.parse(fs.readFileSync(SETTINGS(), "utf8"))); }
  catch (e) { return { error: SETTINGS() + " is not valid JSON (" + e.message + "). Use forward slashes in paths, e.g. \"C:/Muhavin/NET JRF\"." }; }
}

/* Defaults, then .cache/intake/watch.json, then command-line flags. */
function parse(argv, fileSettings) {
  const o = Object.assign({}, DEFAULTS, fileSettings === undefined ? loadSettings() : normalise(fileSettings));
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === "--once") o.once = true;
    else if (k === "--show-settings") o.show = true;
    else if (k === "--folder") o.folder = argv[++i];
    else if (k === "--agent") o.agent = argv[++i];
    else if (k === "--model") o.model = argv[++i];
    else if (k === "--sandbox") o.sandbox = argv[++i];
    else if (k === "--effort") o.effort = argv[++i];
    else if (k === "--command") o.command = argv[++i];
    else if (k === "--interval") o.interval = +argv[++i];
    else if (k === "--settle") o.settle = +argv[++i];
    else if (k === "--max-runs-per-day" || k === "--max-publishes-per-day") o.max = +argv[++i];
    else if (k === "--max-agent-runs-per-day") o.maxRuns = +argv[++i];
    else if (k === "--max-batches") o.maxBatches = +argv[++i];
    else if (k === "--merge") o.merge = true;
    else if (k === "--no-merge") o.merge = false;
  }
  return o;
}

function main(argv) {
  const opts = parse(argv);
  if (opts.error) { console.error(opts.error); return 2; }
  if (opts.show) {
    console.log("settings file: " + SETTINGS() + (fs.existsSync(SETTINGS()) ? "" : " (not found; defaults in force)"));
    console.log(JSON.stringify({ folder: opts.folder || null, engine: opts.command || opts.agent, model: opts.model || "(engine default)", sandbox: opts.agent === "codex" ? (opts.sandbox || "workspace-write") : "n/a", reasoningEffort: opts.agent === "codex" ? opts.effort : "n/a",
      merging: mergeOn(opts) ? "on" : "off", doneFolder: opts.done, interval: opts.interval, settle: opts.settle, maxPublishesPerDay: opts.max, maxAgentRunsPerDay: opts.maxRuns, maxBatchesInARow: opts.maxBatches, notify: opts.notify !== false }, null, 1));
    return 0;
  }
  if (!opts.folder || !fs.existsSync(opts.folder)) {
    console.log(fs.readFileSync(__filename, "utf8").split("*/")[0].replace(/^#!.*\n\/\* ?/, "").replace(/^ \* ?/gm, ""));
    return 2;
  }
  if (!["claude", "codex", "none"].includes(opts.agent)) { console.error("--agent must be claude, codex or none"); return 2; }
  if (opts.sandbox && !["workspace-write", "danger-full-access"].includes(opts.sandbox)) { console.error("sandbox must be workspace-write or danger-full-access"); return 2; }
  if (opts.effort && !["low", "medium", "high", "xhigh"].includes(opts.effort)) { console.error("reasoningEffort must be low, medium, high or xhigh"); return 2; }
  if (opts.notify === false) setNotifier(null);
  const { plan } = require("./intake.js");
  const check = makeChecker(opts, plan, start, setTimeout);
  if (opts.once) { check("one-off check"); return 0; }
  log("watching " + opts.folder + " (engine: " + (opts.command || opts.agent) + (opts.model ? ", model " + opts.model : "") + (mergeOn(opts) ? ", merging on" : ", merging off") + ", every " + opts.interval + " s, settle " + opts.settle + " s)");
  check("start");
  let timer = null;
  try {
    fs.watch(opts.folder, (ev, name) => {
      if (!name || !/\.pdf$/i.test(name)) return;
      clearTimeout(timer);
      timer = setTimeout(() => check("change to " + name), (opts.settle + 5) * 1000);   // re-check once the copy settles
    });
  } catch (e) { log("folder events unavailable (" + e.message + "); relying on the " + opts.interval + " s poll"); }
  setInterval(() => check("poll"), opts.interval * 1000);
  return null;   // keep running
}

if (require.main === module) { const c = main(process.argv.slice(2)); if (c !== null && c !== 0) process.exit(c); }
module.exports = { usageLimit, pausedState, setNotifier, noteOnce, settled, decide, engineCommand, launcher, tick, start, parse, lockState, mergeOn, loadSettings, codexPreflight, makeChecker, publishedToday, agentRunsToday, moveToDone };
