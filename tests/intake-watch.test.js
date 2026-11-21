#!/usr/bin/env node
/* Tests tools/intake-watch.js with a fake planner and a fake agent, so no PDF, model or network is needed:
 * when a file counts as finished copying, when a run starts or waits, the run lock, the daily limit, and that a started
 * run gets the folder and the brief and cleans up after itself.
 *   node tests/intake-watch.test.js */
const fs = require("fs"), os = require("os"), path = require("path");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "intake-watch-"));
process.env.INTAKE_DIR = path.join(tmp, "state");
const W = require(path.join(__dirname, "..", "tools", "intake-watch.js"));
let failed = 0, total = 0;
const expect = (name, ok, detail) => { total++; if (!ok) { failed++; console.log("FAIL " + name + (detail ? "  — " + String(detail).slice(0, 300) : "")); } else console.log("ok   " + name); };

const now = Date.now();
expect("an old file of steady size has settled", W.settled({ mtimeMs: now - 60000, size: 10 }, now, 30, 10));
expect("a file written seconds ago has not", !W.settled({ mtimeMs: now - 5000, size: 10 }, now, 30, 10));
expect("a file whose size is still changing has not", !W.settled({ mtimeMs: now - 60000, size: 10 }, now, 30, 12));
expect("an empty file has not", !W.settled({ mtimeMs: now - 60000, size: 0 }, now, 30, 0));

const t1 = [{ name: "a.pdf", kind: "questions" }];
expect("work, no lock, under the limit: start", W.decide({ todo: t1, unsettled: [], locked: false, today: 0, max: 6 }).start);
expect("a file still copying: wait", /waiting for b\.pdf/.test(W.decide({ todo: t1, unsettled: ["b.pdf"], locked: false, today: 0, max: 6 }).why));
expect("a run already active: wait", /already active/.test(W.decide({ todo: t1, unsettled: [], locked: true, today: 0, max: 6 }).why));
expect("nothing new: no run", W.decide({ todo: [], unsettled: [], locked: false, today: 0, max: 6 }).why === "nothing to process");
expect("daily limit reached: wait for tomorrow", /daily limit of 6/.test(W.decide({ todo: t1, unsettled: [], locked: false, today: 6, max: 6 }).why));

const noShim = { APPDATA: path.join(tmp, "no-appdata") };
const c = W.engineCommand("claude", "BRIEF", undefined, undefined, noShim);
expect("claude runs headless (-p) with the brief on stdin, not in its arguments", c.cmd === "claude" && c.args[0] === "-p" && c.stdin === "BRIEF" && !c.args.includes("BRIEF"));
const x = W.engineCommand("codex", "BRIEF", undefined, "C:/src", noShim);
expect("codex runs exec reading the brief from stdin ('-')", x.cmd === "codex" && x.args[0] === "exec" && x.args[x.args.length - 1] === "-" && x.stdin === "BRIEF");
expect("codex runs sandboxed to the workspace, with network, and can read the source folder",
  x.args.join(" ").includes("-s workspace-write") && x.args.includes("sandbox_workspace_write.network_access=true") && x.args.join(" ").includes("--add-dir C:/src"));
expect("codex runs with approvals off and never with the rejected --approve-for-me / --full-auto flags",
  x.args.includes('approval_policy="never"') && !x.args.includes("--approve-for-me") && !x.args.includes("--full-auto") && !x.args.includes("--sandbox"));
const xf = W.engineCommand("codex", "BRIEF", undefined, "C:/src", noShim, null, "danger-full-access");
expect("the owner's danger-full-access choice drops the sandbox confinement flags", xf.args.join(" ").includes("-s danger-full-access") && !xf.args.includes("--add-dir") && !xf.args.includes("sandbox_workspace_write.network_access=true"));
expect("a disabled sandbox backend stops a workspace-write codex run", W.codexPreflight({ agent: "codex" }, () => "  sandbox backend          disabled\n").ok === false);
expect("an enabled sandbox backend lets it start", W.codexPreflight({ agent: "codex" }, () => "  sandbox backend          restricted-token\n").ok === true);
expect("the pre-check does not apply to danger-full-access, claude or a custom command",
  W.codexPreflight({ agent: "codex", sandbox: "danger-full-access" }, () => "sandbox backend disabled").ok && W.codexPreflight({ agent: "claude" }, () => "sandbox backend disabled").ok && W.codexPreflight({ agent: "codex", command: "x" }, () => "sandbox backend disabled").ok);
expect("the sandbox setting comes from watch.json or --sandbox", W.parse([], { sandbox: "danger-full-access" }).sandbox === "danger-full-access" && W.parse(["--sandbox", "workspace-write"], { sandbox: "danger-full-access" }).sandbox === "workspace-write");
const fakeJs = path.join(tmp, "fake-codex.js"); fs.writeFileSync(fakeJs, "");
const viaJs = W.engineCommand("codex", "BRIEF", undefined, "C:/src", { INTAKE_CODEX_JS: fakeJs });
expect("when the package launcher is found, it runs with this Node (no .cmd shim, no shell)", viaJs.cmd === process.execPath && viaJs.args[0] === fakeJs && viaJs.args[1] === "exec");
expect("a custom command runs through the shell", W.engineCommand("none", "B", "my-agent --go").shell === true);
expect("no engine means nothing is started", W.engineCommand("none", "B") === null);
expect("merging is off by default for codex and on for claude", !W.mergeOn({ agent: "codex" }) && W.mergeOn({ agent: "claude" }));
expect("--merge and --no-merge override the default", W.mergeOn(W.parse(["--agent", "codex", "--merge"])) && !W.mergeOn(W.parse(["--agent", "claude", "--no-merge"])));
const p = W.parse(["--folder", "F", "--agent", "claude", "--once", "--max-runs-per-day", "3"], {});
expect("options are parsed", p.folder === "F" && p.agent === "claude" && p.once && p.max === 3 && p.settle === 30);
expect("GPT (codex) is the default engine", W.parse([], {}).agent === "codex");
const fileSet = { folder: "C:/src", agent: "codex", model: "gpt-5.6-terra", maxRunsPerDay: 2 };
const ps = W.parse([], fileSet);
expect("the settings file supplies folder, engine, model and limit", ps.folder === "C:/src" && ps.model === "gpt-5.6-terra" && ps.max === 2);
expect("a flag overrides the settings file", W.parse(["--model", "gpt-6-luna", "--agent", "claude"], fileSet).model === "gpt-6-luna" && W.parse(["--agent", "claude"], fileSet).agent === "claude");
fs.mkdirSync(process.env.INTAKE_DIR, { recursive: true });
fs.writeFileSync(path.join(process.env.INTAKE_DIR, "watch.json"), JSON.stringify({ model: "gpt-5.6-luna", merge: false }));
expect("watch.json is read from .cache/intake", W.loadSettings().model === "gpt-5.6-luna" && W.loadSettings().merge === false);
fs.writeFileSync(path.join(process.env.INTAKE_DIR, "watch.json"), '{ "folder": "C:\Muhavin" ');
expect("a broken watch.json is reported, not silently ignored", /not valid JSON/.test(W.loadSettings().error || "") && /not valid JSON/.test(W.parse([]).error || ""));
fs.unlinkSync(path.join(process.env.INTAKE_DIR, "watch.json"));
expect("no watch.json means plain defaults", !W.loadSettings().error && W.parse([]).agent === "codex");
const xm = W.engineCommand("codex", "BRIEF", undefined, "C:/src", { APPDATA: path.join(tmp, "no-appdata") }, "gpt-5.6-terra");
expect("a chosen model reaches codex as -m", xm.args.join(" ").includes("-m gpt-5.6-terra"));
expect("no model means the engine's own default (no -m)", !W.engineCommand("codex", "B", undefined, "C:/src", { APPDATA: tmp }).args.includes("-m"));

// tick() over a real folder, with a fake planner
const folder = path.join(tmp, "src"); fs.mkdirSync(folder);
const old = new Date(now - 120000);
fs.writeFileSync(path.join(folder, "old.pdf"), "x"); fs.utimesSync(path.join(folder, "old.pdf"), old, old);
const planner = () => ({ todo: [{ name: "old.pdf", kind: "questions" }] });
let r = W.tick({ folder, settle: 30, max: 6 }, planner);
expect("a settled new file triggers a run", r.start, JSON.stringify(r));
fs.writeFileSync(path.join(folder, "fresh.pdf"), "y");
let planned = false;
r = W.tick({ folder, settle: 30, max: 6 }, () => { planned = true; return planner(); });
expect("a file still being copied holds everything back, and the planner is not even asked", !r.start && /fresh\.pdf/.test(r.why) && !planned, JSON.stringify(r));
fs.unlinkSync(path.join(folder, "fresh.pdf"));

// lock: a live pid blocks, a dead one is cleared
fs.mkdirSync(process.env.INTAKE_DIR, { recursive: true });
const lockFile = path.join(process.env.INTAKE_DIR, "run.lock");
fs.writeFileSync(lockFile, JSON.stringify({ pid: process.pid, started: now }));
r = W.tick({ folder, settle: 30, max: 6 }, planner);
expect("a live run's lock blocks a second run", !r.start && /already active/.test(r.why));
fs.writeFileSync(lockFile, JSON.stringify({ pid: 2147483646, started: now }));
r = W.tick({ folder, settle: 30, max: 6 }, planner);
expect("a dead run's lock is cleared and work starts", r.start && !fs.existsSync(lockFile), JSON.stringify(r));

// start() refuses, without spending a run, when the pre-check fails, and leaves the owner a note with the three choices
let refusedCode = "unset";
const refused = W.start({ folder, agent: "codex", preflight: () => ({ ok: false, why: "Codex's sandbox backend is disabled" }) }, c2 => { refusedCode = c2; });
const notesFile = path.join(process.env.INTAKE_DIR, "watch-notes.md");
const notes = fs.existsSync(notesFile) ? fs.readFileSync(notesFile, "utf8") : "";
expect("a failed pre-check starts nothing and creates no run log", refused === null && refusedCode === null && !fs.existsSync(path.join(process.env.INTAKE_DIR, "runs")));
expect("the owner's note explains the choices (sandbox, danger-full-access, claude)", /Codex cannot write/.test(notes) && /danger-full-access/.test(notes) && /"agent": "claude"/.test(notes), notes.slice(0, 200));
W.start({ folder, agent: "codex", preflight: () => ({ ok: false, why: "Codex's sandbox backend is disabled" }) }, () => {});
expect("the note is written once, not on every poll", (fs.readFileSync(notesFile, "utf8").match(/Codex cannot write/g) || []).length === 1);

// start(): a fake agent proves it gets the folder and the brief, and the lock and log are handled
const marker = path.join(tmp, "agent-ran.json");
const fake = "\"" + process.execPath.replace(/\\/g, "/") + "\" -e \"require('fs').writeFileSync(process.argv[1], JSON.stringify({folder: process.env.INTAKE_FOLDER, brief: require('fs').existsSync(process.env.INTAKE_PROMPT_FILE), merge: process.env.INTAKE_MERGE}))\" \"" + marker.replace(/\\/g, "/") + "\"";
W.start({ folder, agent: "none", command: fake }, code => {
  let m = {}; try { m = JSON.parse(fs.readFileSync(marker, "utf8")); } catch (e) { /* missing */ }
  expect("the run exited cleanly", code === 0, code);
  expect("the agent received the source folder and a readable brief", m.folder === folder && m.brief === true, JSON.stringify(m));
  expect("a custom engine with no --merge gets merging on (INTAKE_MERGE=1)", m.merge === "1", JSON.stringify(m));
  expect("the lock is removed when the run ends", !fs.existsSync(lockFile));
  const runs = fs.readdirSync(path.join(process.env.INTAKE_DIR, "runs"));
  expect("the run has its own log file", runs.length === 1 && /\.log$/.test(runs[0]), runs.join(","));
  // the daily limit counts today's run logs
  for (let k = 0; k < 6; k++) fs.writeFileSync(path.join(process.env.INTAKE_DIR, "runs", new Date().toISOString().slice(0, 10) + "T00-00-0" + k + ".log"), "");
  r = W.tick({ folder, settle: 30, max: 6 }, planner);
  expect("after the day's limit no further run starts", !r.start && /daily limit/.test(r.why), JSON.stringify(r));
  // a stand-in Codex launcher: proves the brief arrives on stdin and the sandbox arguments arrive intact
  const got = path.join(tmp, "codex-got.json");
  const stub = path.join(tmp, "codex-stub.js");
  fs.writeFileSync(stub, "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{require('fs').writeFileSync(" + JSON.stringify(got) +
    ",JSON.stringify({args:process.argv.slice(2),brief:s.slice(0,40),merge:process.env.INTAKE_MERGE}))})");
  process.env.INTAKE_CODEX_JS = stub;
  for (const f of fs.readdirSync(path.join(process.env.INTAKE_DIR, "runs"))) fs.unlinkSync(path.join(process.env.INTAKE_DIR, "runs", f));
  W.start({ folder, agent: "codex" }, code2 => {
    let g = {}; try { g = JSON.parse(fs.readFileSync(got, "utf8")); } catch (e) { /* missing */ }
    expect("the codex run exited cleanly", code2 === 0, code2);
    expect("the brief reached codex on stdin", /^# Unattended intake run/.test(g.brief || ""), JSON.stringify(g));
    expect("codex got exec, the sandbox flags, the source folder and '-'", (g.args || [])[0] === "exec" && (g.args || []).includes("--add-dir") && (g.args || []).includes(folder) && (g.args || []).slice(-1)[0] === "-", JSON.stringify(g.args));
    expect("a codex run has merging off by default", g.merge === "0", g.merge);
    fs.rmSync(tmp, { recursive: true, force: true });
    console.log((total - failed) + "/" + total + " intake-watch checks passed");
    process.exit(failed ? 1 : 0);
  });
});
