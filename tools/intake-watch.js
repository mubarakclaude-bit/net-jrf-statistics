#!/usr/bin/env node
/* Watch the owner's source folder and start an unattended intake run when a new PDF is ready.
 *
 *   node tools/intake-watch.js --folder "<dir>" [--agent claude|codex|none] [--command "<cmd>"]
 *                              [--interval 300] [--settle 30] [--max-runs-per-day 6] [--once] [--merge | --no-merge]
 *
 * What it does, on a folder change or every --interval seconds:
 *   1. waits until every PDF in the folder has stopped changing (its mtime is at least --settle seconds old and its size
 *      holds steady), so a half-copied download is never read;
 *   2. asks tools/intake.js plan() what is left to process: new files, files already started; it skips what is already
 *      in the app (tools/intake-sources.json), personal, unreadable or duplicate files;
 *   3. if anything is left and no run is active, starts ONE agent run with the brief in tools/intake-run.md and the folder
 *      in INTAKE_FOLDER. The agent does the reading, solving, verification, PR and merge.
 *
 * Engines (--agent):
 *   claude   Claude Code's CLI:  claude -p <brief> --permission-mode acceptEdits --allowedTools ...
 *   codex    OpenAI Codex CLI:   codex exec --sandbox workspace-write --approve-for-me (network on) <brief>
 *            (uses the owner's OpenAI API key or ChatGPT login; the first sandboxed run may ask the owner to set it up)
 *   none     only report what would run (the default: nothing is started until an engine is chosen)
 *   --command "<cmd>" runs any other command through the shell, with the brief's path in INTAKE_PROMPT_FILE.
 * The engine must be installed and logged in by the owner; this script never handles a key.
 *
 * Merging: a run merges its own green PRs only when merging is on (INTAKE_MERGE=1 in its environment). It is on by
 * default for claude and off by default for codex, until a few Codex runs have been checked: --merge / --no-merge
 * override. With merging off the run leaves each PR open and lists it in .cache/intake/watch-notes.md.
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

function runsToday(now) {
  const day = new Date(now).toISOString().slice(0, 10);
  try { return fs.readdirSync(path.join(DIR, "runs")).filter(f => f.startsWith(day)).length; } catch (e) { return 0; }
}

function decide({ todo, unsettled, locked, today, max }) {
  if (unsettled.length) return { start: false, why: "waiting for " + unsettled.join(", ") + " to finish copying" };
  if (locked) return { start: false, why: "a run is already active" };
  if (!todo.length) return { start: false, why: "nothing to process" };
  if (today >= max) return { start: false, why: "daily limit of " + max + " runs reached; " + todo.length + " file(s) wait for tomorrow" };
  return { start: true, why: todo.length + " file(s) to process, first " + todo[0].name + " (" + todo[0].kind + ")" };
}

function engineCommand(agent, briefText, custom, folder) {
  if (custom) return { shell: true, cmd: custom, args: [] };
  if (agent === "claude") return { cmd: "claude", args: ["-p", briefText, "--permission-mode", "acceptEdits",
    "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch"] };
  // Codex CLI 0.171: no --full-auto; workspace-write sandbox (writes only inside the repository and the source folder),
  // approvals reviewed automatically, network on so the run can push and open the pull request.
  if (agent === "codex") return { cmd: "codex", args: ["exec", "--sandbox", "workspace-write", "--approve-for-me",
    "-c", "sandbox_workspace_write.network_access=true", "-C", ROOT].concat(folder ? ["--add-dir", folder] : []).concat([briefText]) };
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
  const d = decide({ todo, unsettled, locked: ls.locked, today: runsToday(now), max: opts.max });
  return Object.assign({ todo }, d);
}

function start(opts, onExit) {
  const brief = fs.readFileSync(BRIEF, "utf8");
  const eng = engineCommand(opts.agent, brief, opts.command, opts.folder);
  if (!eng) { log("would start a run now, but no engine is set (--agent claude|codex or --command)"); onExit && onExit(null); return null; }
  fs.mkdirSync(path.join(DIR, "runs"), { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const out = fs.openSync(path.join(DIR, "runs", stamp + ".log"), "a");
  const env = Object.assign({}, process.env, { INTAKE_FOLDER: opts.folder, INTAKE_PROMPT_FILE: BRIEF, INTAKE_MERGE: mergeOn(opts) ? "1" : "0" });
  const child = spawn(eng.cmd, eng.args, { cwd: ROOT, env, shell: !!eng.shell, stdio: ["ignore", out, out], windowsHide: true });
  child.on("error", e => { log("could not start " + eng.cmd + ": " + e.message + " (is it installed and on PATH?)"); try { fs.unlinkSync(LOCK()); } catch (x) { /* none */ } onExit && onExit(-1); });
  fs.writeFileSync(LOCK(), JSON.stringify({ pid: child.pid, started: Date.now(), engine: opts.command || opts.agent, log: "runs/" + stamp + ".log" }));
  log("started run (" + (opts.command || opts.agent) + (mergeOn(opts) ? ", merges green PRs" : ", PRs left open for review") + "), pid " + child.pid + ", log .cache/intake/runs/" + stamp + ".log");
  child.on("exit", code => { log("run finished with exit code " + code); try { fs.unlinkSync(LOCK()); } catch (e) { /* already gone */ } onExit && onExit(code); });
  return child;
}

/* Merge only where the owner has seen enough: on for Claude, off for Codex until --merge. */
function mergeOn(opts) {
  if (opts.merge === true || opts.merge === false) return opts.merge;
  return opts.agent !== "codex";
}

/* ------------------------------------------------------------------ command line */
function parse(argv) {
  const o = { agent: "none", interval: 300, settle: 30, max: 6, once: false };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === "--once") o.once = true;
    else if (k === "--folder") o.folder = argv[++i];
    else if (k === "--agent") o.agent = argv[++i];
    else if (k === "--command") o.command = argv[++i];
    else if (k === "--interval") o.interval = +argv[++i];
    else if (k === "--settle") o.settle = +argv[++i];
    else if (k === "--max-runs-per-day") o.max = +argv[++i];
    else if (k === "--merge") o.merge = true;
    else if (k === "--no-merge") o.merge = false;
  }
  return o;
}

function main(argv) {
  const opts = parse(argv);
  if (!opts.folder || !fs.existsSync(opts.folder)) {
    console.log(fs.readFileSync(__filename, "utf8").split("*/")[0].replace(/^#!.*\n\/\* ?/, "").replace(/^ \* ?/gm, ""));
    return 2;
  }
  if (!["claude", "codex", "none"].includes(opts.agent)) { console.error("--agent must be claude, codex or none"); return 2; }
  const { plan } = require("./intake.js");
  const check = (reason) => {
    let r;
    try { r = tick(opts, plan); } catch (e) { log("check failed: " + e.message); return; }
    log((reason ? reason + ": " : "") + r.why);
    if (r.start) start(opts, () => { if (!opts.once) setTimeout(() => check("after the run"), 60 * 1000); });
  };
  if (opts.once) { check("one-off check"); return 0; }
  log("watching " + opts.folder + " (engine: " + (opts.command || opts.agent) + (mergeOn(opts) ? ", merging on" : ", merging off") + ", every " + opts.interval + " s, settle " + opts.settle + " s)");
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
module.exports = { settled, decide, engineCommand, tick, start, parse, lockState, mergeOn };
