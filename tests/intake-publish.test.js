#!/usr/bin/env node
/* Tests tools/intake-publish.js with a scripted fake git, gh, npm, python and bash, so nothing touches GitHub:
 * worktree preparation, what an agent's result file may claim, the independent re-checks, and when the watcher pushes,
 * opens a PR, waits for CI and merges.
 *   node tests/intake-publish.test.js */
const fs = require("fs"), os = require("os"), path = require("path");
const P = require(path.join(__dirname, "..", "tools", "intake-publish.js"));
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "intake-publish-"));
let failed = 0, total = 0;
const expect = (name, ok, detail) => { total++; if (!ok) { failed++; console.log("FAIL " + name + (detail ? "  — " + String(detail).slice(0, 400) : "")); } else console.log("ok   " + name); };

/* A fake shell: rules are [regex on "cmd args…", result]; the first match wins; anything else succeeds with no output. */
function fakeSh(rules) {
  const log = [];
  const sh = (cmd, args) => {
    const line = [path.basename(cmd)].concat(args).join(" ");
    log.push(line);
    for (const [re, res] of rules) if (re.test(line)) return Object.assign({ code: 0, out: "" }, typeof res === "function" ? res(line) : res);
    return { code: 0, out: "" };
  };
  sh.log = log;
  return sh;
}
const ran = (sh, re) => sh.log.some(l => re.test(l));

// prepare()
let sh = fakeSh([[/config --local --get/, { code: 1, out: "" }], [/^git config --get user\.name/, { out: "Owner Name" }], [/^git config --get user\.email/, { out: "owner@example.com" }]]);
const prep = P.prepare(tmp, sh, new Date("2026-11-22T01:02:03Z"));
expect("prepare names the branch and worktree from the time", prep.branch === "content/intake-20261122-010203" && /run-20261122-010203$/.test(prep.wt), JSON.stringify(prep));
expect("prepare fetches origin and adds the worktree from origin/main", sh.log[0] === "git fetch origin main" && ran(sh, /^git worktree add .*run-20261122-010203 -b content\/intake-20261122-010203 origin\/main$/), sh.log.join(" | "));
expect("prepare gives the repository its own commit identity for the sandbox user", ran(sh, /^git config --local user\.name Owner Name$/) && ran(sh, /^git config --local user\.email owner@example\.com$/));
expect("prepare runs npm ci in the worktree, last", /^npm ci/.test(sh.log[sh.log.length - 1]));
sh = fakeSh([[/config --local --get user\.name/, { out: "Already Set" }], [/config --local --get user\.email/, { out: "set@example.com" }]]);
P.prepare(tmp, sh, new Date());
expect("an identity already set is left alone", !ran(sh, /^git config --local user\.name /));
let threw = "";
try { P.prepare(tmp, fakeSh([[/^git fetch/, { code: 128, out: "could not resolve host" }]])); } catch (e) { threw = e.message; }
expect("a failed fetch stops preparation with the reason", /git fetch failed: could not resolve host/.test(threw), threw);

// readResult()
const rf = (name, obj) => { const f = path.join(tmp, name + ".json"); fs.writeFileSync(f, typeof obj === "string" ? obj : JSON.stringify(obj)); return f; };
const good = { status: "ready", title: "Probability practice set: 20 questions", body: "Adds 20 probability items; verify_x.py: 140 checks, 0 failed. No key notes.", verify: "python verify_prob_practice.py", source: "x.pdf" };
expect("a missing or broken result file is invalid", P.readResult(path.join(tmp, "none.json")).status === "invalid" && P.readResult(rf("broken", "{oops")).status === "invalid");
expect("nothing and stopped pass through", P.readResult(rf("nothing", { status: "nothing" })).status === "nothing" && P.readResult(rf("stopped", { status: "stopped", reason: "unreadable" })).reason === "unreadable");
expect("a ready result needs a title and a real body", P.readResult(rf("notitle", Object.assign({}, good, { title: "" }))).status === "invalid" && P.readResult(rf("nobody", Object.assign({}, good, { body: "short" }))).status === "invalid");
expect("a verify command that is not a plain `python <script>.py` is refused (no command injection)",
  ["python verify.py; rm -rf .", "bash evil.sh", "python ../outside.py && x", "python verify.py --flag"].every(v => P.readResult(rf("inj", Object.assign({}, good, { verify: v }))).status === "invalid"));
expect("a good result is accepted", P.readResult(rf("good", good)).status === "ready");
const withFiles = Object.assign({}, good, { files: ["quiz_bank_pp.py", "verify_pp.py", "seed\\pp_quiz.json", "tools/intake-sources.json"] });
expect("a files list of repository paths is accepted, with backslashes normalised", JSON.stringify(P.readResult(rf("files", withFiles)).files) ===
  JSON.stringify(["quiz_bank_pp.py", "verify_pp.py", "seed/pp_quiz.json", "tools/intake-sources.json"]));
expect("files may not name local state, source material, or anything outside the worktree",
  [[".cache/intake/x/questions.json"], ["paper.pdf"], ["pages/p1.png"], ["p1.txt"], ["../x.py"], ["C:/x.py"], ["/etc/x"], ["--force"], [".git/config"], []]
    .every(fl => P.readResult(rf("badfiles", Object.assign({}, good, { files: fl }))).status === "invalid"));
const bomFile = path.join(tmp, "bom.json"); fs.writeFileSync(bomFile, Buffer.concat([Buffer.from([0xef, 0xbb, 0xbf]), Buffer.from(JSON.stringify({ status: "stopped", reason: "r" }))]));
expect("a UTF-8 file with a byte-order mark (PowerShell Set-Content) is read", P.readResult(bomFile).status === "stopped");
const u16File = path.join(tmp, "u16.json"); fs.writeFileSync(u16File, Buffer.concat([Buffer.from([0xff, 0xfe]), Buffer.from(JSON.stringify({ status: "nothing" }), "utf16le")]));
expect("a UTF-16LE file (PowerShell Out-File or >) is read", P.readResult(u16File).status === "nothing");

// publish(): the happy path, merging on
const SHA = "abc1234def5678";
const happy = () => fakeSh([
  [/^git rev-list --count/, { out: "1" }],
  [/^git status --porcelain/, { out: "" }],
  [/^git rev-parse HEAD/, { out: SHA }],
  [/^gh pr create/, { out: "https://github.com/o/r/pull/77" }],
  [/^gh run list/, { out: JSON.stringify([{ databaseId: 555, headSha: SHA, event: "pull_request" }]) }],
]);
const prepX = { stamp: "s1", branch: "content/intake-s1", wt: path.join(tmp, "wtX") };
fs.mkdirSync(prepX.wt, { recursive: true });
sh = happy();
let res = P.publish(prepX, rf("good", good), true, sh, { bash: "bash", wait: false });
expect("happy path with merging on: merged", res.outcome === "merged" && res.pr === "https://github.com/o/r/pull/77", JSON.stringify(res));
const order = ["python -X utf8 verify_prob_practice.py", "bash check.sh", "git push -u origin content/intake-s1", "gh pr create", "gh run watch 555 --exit-status", "gh pr merge https://github.com/o/r/pull/77 --merge --match-head-commit " + SHA];
const idx = order.map(o => sh.log.findIndex(l => l.startsWith(o)));
expect("it re-checks, then pushes, opens the PR, waits for CI on that commit and merges, in that order", idx.every(i => i >= 0) && idx.every((v, k) => k === 0 || v > idx[k - 1]), sh.log.join(" | "));
expect("the PR title and branch come from the result and the prepared run", ran(sh, /^gh pr create --base main --head content\/intake-s1 --title Probability practice set: 20 questions --body-file /));

// merging off
sh = happy();
res = P.publish(prepX, rf("good", good), false, sh, { bash: "bash", wait: false });
expect("merging off: CI green leaves the PR open, no merge", res.outcome === "left-open" && !ran(sh, /^gh pr merge/), JSON.stringify(res));

// failures that must stop before anything is published
const failing = (rule, note) => {
  const s = fakeSh([rule].concat([[/^git rev-list --count/, { out: "1" }], [/^git status --porcelain/, { out: "" }], [/^git rev-parse HEAD/, { out: SHA }]]));
  const r = P.publish(prepX, rf("good", good), true, s, { bash: "bash", wait: false });
  return { r, s };
};
let f = failing([/^python -X utf8 verify_prob_practice\.py/, { code: 1, out: "AssertionError: Q7 keyed B, computed C" }]);
expect("a verification script that fails when re-run blocks publishing", f.r.outcome === "checks-failed" && /Q7 keyed B, computed C/.test(f.r.note) && !ran(f.s, /^git push/));
f = failing([/^bash check\.sh/, { code: 1, out: "contracts: 1 failed" }]);
expect("a failing check.sh blocks publishing", f.r.outcome === "checks-failed" && !ran(f.s, /^git push/));
f = { s: fakeSh([[/^git rev-list --count/, { out: "2" }]]) }; f.r = P.publish(prepX, rf("good", good), true, f.s, { wait: false });
expect("more than one commit is rejected (one commit per change)", f.r.outcome === "rejected" && /exactly one new commit/.test(f.r.note) && !ran(f.s, /^git push/));
f = { s: fakeSh([[/^git rev-list --count/, { out: "1" }], [/^git status --porcelain/, { out: " M seed/x.json" }]]) }; f.r = P.publish(prepX, rf("good", good), true, f.s, { wait: false });
expect("uncommitted leftovers are rejected", f.r.outcome === "rejected" && !ran(f.s, /^git push/));
// the agent cannot commit in Codex's sandbox: the watcher commits the listed files, clears scratch files, then re-checks
f = { s: fakeSh([[/^git rev-list --count/, { out: "0" }], [/^git status --porcelain/, { out: "" }], [/^git rev-parse HEAD/, { out: SHA }],
  [/^gh pr create/, { out: "https://github.com/o/r/pull/80" }], [/^gh run list/, { out: JSON.stringify([{ databaseId: 9, headSha: SHA, event: "pull_request" }]) }]]) };
f.r = P.publish(prepX, rf("files", withFiles), false, f.s, { wait: false, engine: "codex" });
const iAdd = f.s.log.findIndex(l => /^git add -- quiz_bank_pp\.py verify_pp\.py seed\/pp_quiz\.json tools\/intake-sources\.json$/.test(l));
const iCommit = f.s.log.findIndex(l => /^git commit -m Probability practice set/.test(l)), iClean = f.s.log.indexOf("git clean -fd");
const iVerify = f.s.log.findIndex(l => /^python -X utf8 verify_prob_practice\.py/.test(l));
expect("with no commit, the listed files are added and committed, scratch files cleared, and only then re-verified and pushed",
  iAdd >= 0 && iAdd < iCommit && iCommit < iClean && iClean < iVerify && ran(f.s, /^git push/) && f.r.outcome === "left-open", f.s.log.join(" | "));
f = { s: fakeSh([[/^git rev-list --count/, { out: "0" }]]) }; f.r = P.publish(prepX, rf("good", good), true, f.s, { wait: false });
expect("no commit and no files list is rejected", f.r.outcome === "rejected" && /lists no files/.test(f.r.note) && !ran(f.s, /^git (add|push)/));
f = { s: fakeSh([[/^git rev-list --count/, { out: "0" }], [/^git status --porcelain/, { out: " M tools/intake.js" }]]) };
f.r = P.publish(prepX, rf("files", withFiles), true, f.s, { wait: false });
expect("a changed tracked file left out of the list rejects the run, naming it", f.r.outcome === "rejected" && /tools\/intake\.js/.test(f.r.note) && !ran(f.s, /^git push/), f.r.note);
// a failed run with changes keeps its worktree
f = { s: fakeSh([[/^git status --porcelain/, { out: "?? verify_pp.py" }]]) };
expect("hasChanges sees unpublished work", P.hasChanges(prepX, f.s) === true && P.hasChanges(prepX, fakeSh([])) === false);
f = { s: fakeSh([]) }; P.cleanup(tmp, prepX, true, f.s, true);
expect("cleanup with keepTree leaves the worktree and branch alone", f.s.log.length === 0, f.s.log.join(" | "));
f = { s: fakeSh([]) }; f.r = P.publish(prepX, rf("stopped", { status: "stopped", reason: "file unreadable" }), true, f.s, { wait: false });
expect("a stopped run publishes nothing and passes on the reason", f.r.outcome === "stopped" && /file unreadable/.test(f.r.note) && f.s.log.length === 0);
f = { s: fakeSh([]) }; f.r = P.publish(prepX, rf("progress", { status: "progress", done: 15, total: 50 }), true, f.s, { wait: false });
expect("a progress batch publishes nothing and reports how far the worksheet has got", f.r.outcome === "progress" && f.r.done === 15 && f.r.total === 50 && f.s.log.length === 0, JSON.stringify(f.r));
f = { s: fakeSh([]) }; f.r = P.publish(prepX, rf("progress2", { status: "progress", stage: "explain", done: 30, total: 294 }), true, f.s, { wait: false });
expect("an explain batch is progress too, and says which pass it is", f.r.outcome === "progress" && f.r.stage === "explain" && /30 of 294 kept questions now explained/.test(f.r.note) && f.s.log.length === 0, JSON.stringify(f.r));
expect("a progress result needs sensible numbers",
  P.readResult(rf("p1", { status: "progress", done: 60, total: 50 })).status === "invalid" && P.readResult(rf("p2", { status: "progress", done: "15" })).status === "invalid");
f = { s: fakeSh([]) }; f.r = P.publish(prepX, rf("inj", Object.assign({}, good, { verify: "python v.py; curl x" })), true, f.s, { wait: false });
expect("an invalid result is rejected without running anything", f.r.outcome === "rejected" && f.s.log.length === 0);

// CI outcomes
sh = fakeSh([[/^git rev-list --count/, { out: "1" }], [/^git rev-parse HEAD/, { out: SHA }], [/^gh pr create/, { out: "https://github.com/o/r/pull/78" }],
  [/^gh run list/, { out: JSON.stringify([{ databaseId: 9, headSha: SHA, event: "pull_request" }]) }], [/^gh run watch/, { code: 1, out: "X validate failed" }]]);
res = P.publish(prepX, rf("good", good), true, sh, { bash: "bash", wait: false });
expect("red CI leaves the PR open and never merges", res.outcome === "ci-failed" && res.pr && !ran(sh, /^gh pr merge/));
let lists = 0;
sh = fakeSh([[/^git rev-list --count/, { out: "1" }], [/^git rev-parse HEAD/, { out: SHA }], [/^gh pr create/, { out: "https://github.com/o/r/pull/81" }],
  [/^gh run list/, () => ({ out: JSON.stringify(++lists < 2 ? [{ databaseId: 9, headSha: SHA, event: "push" }] : [{ databaseId: 10, headSha: SHA, event: "pull_request" }, { databaseId: 9, headSha: SHA, event: "push" }]) })],
  [/^gh run watch 9 /, { code: 1, out: "cancelled" }]]);
res = P.publish(prepX, rf("good", good), false, sh, { bash: "bash", wait: false, findTries: 4 });
expect("the pull_request run is watched, not the push run that it cancels (#154)", res.outcome === "left-open" && ran(sh, /^gh run watch 10 /) && !ran(sh, /^gh run watch 9 /), JSON.stringify(res) + sh.log.join("\n"));
sh = fakeSh([[/^git rev-list --count/, { out: "1" }], [/^git rev-parse HEAD/, { out: SHA }], [/^gh pr create/, { out: "https://github.com/o/r/pull/82" }],
  [/^gh run list/, { out: JSON.stringify([{ databaseId: 11, headSha: SHA, event: "pull_request" }, { databaseId: 12, headSha: SHA, event: "pull_request" }]) }],
  [/^gh run watch 11 /, { code: 1, out: "cancelled" }], [/^gh run view 11 /, { out: JSON.stringify({ conclusion: "cancelled" }) }]]);
res = P.publish(prepX, rf("good", good), false, sh, { bash: "bash", wait: false });
expect("a watched run that ends cancelled hands over to the other run for the commit", res.outcome === "left-open" && ran(sh, /^gh run watch 12 /), JSON.stringify(res));
sh = fakeSh([[/^git rev-list --count/, { out: "1" }], [/^git rev-parse HEAD/, { out: SHA }], [/^gh pr create/, { out: "https://github.com/o/r/pull/79" }],
  [/^gh run list/, { out: JSON.stringify([{ databaseId: 9, headSha: "otherSha", event: "pull_request" }]) }]]);
res = P.publish(prepX, rf("good", good), true, sh, { bash: "bash", wait: false, findTries: 2 });
expect("a CI run for a different commit is never trusted", res.outcome === "ci-failed" && /no Validate run appeared/.test(res.note) && !ran(sh, /^gh run watch/));
sh = fakeSh([[/^git rev-list --count/, { out: "1" }], [/^git rev-parse HEAD/, { out: SHA }], [/^git push/, { code: 1, out: "rejected: non-fast-forward" }]]);
res = P.publish(prepX, rf("good", good), true, sh, { bash: "bash", wait: false });
expect("a failed push stops before the PR", res.outcome === "push-failed" && !ran(sh, /^gh pr create/));

// cleanup()
sh = fakeSh([]); P.cleanup(tmp, prepX, false, sh);
expect("cleanup removes the worktree and the pushed local branch", ran(sh, /^git worktree remove --force/) && ran(sh, /^git branch -D content\/intake-s1/));
sh = fakeSh([]); P.cleanup(tmp, prepX, true, sh);
expect("cleanup keeps an unpublished branch for the owner", ran(sh, /^git worktree remove --force/) && !ran(sh, /^git branch -D/));

fs.rmSync(tmp, { recursive: true, force: true });
console.log((total - failed) + "/" + total + " intake-publish checks passed");
process.exit(failed ? 1 : 0);
