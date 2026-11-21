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

const c = W.engineCommand("claude", "BRIEF");
expect("claude runs headless with the brief", c.cmd === "claude" && c.args[0] === "-p" && c.args[1] === "BRIEF");
const x = W.engineCommand("codex", "BRIEF");
expect("codex runs exec with the brief", x.cmd === "codex" && x.args[0] === "exec" && x.args.includes("BRIEF"));
expect("a custom command runs through the shell", W.engineCommand("none", "B", "my-agent --go").shell === true);
expect("no engine means nothing is started", W.engineCommand("none", "B") === null);
expect("merging is off by default for codex and on for claude", !W.mergeOn({ agent: "codex" }) && W.mergeOn({ agent: "claude" }));
expect("--merge and --no-merge override the default", W.mergeOn(W.parse(["--agent", "codex", "--merge"])) && !W.mergeOn(W.parse(["--agent", "claude", "--no-merge"])));
const p = W.parse(["--folder", "F", "--agent", "codex", "--once", "--max-runs-per-day", "3"]);
expect("options are parsed", p.folder === "F" && p.agent === "codex" && p.once && p.max === 3 && p.settle === 30);

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
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log((total - failed) + "/" + total + " intake-watch checks passed");
  process.exit(failed ? 1 : 0);
});
