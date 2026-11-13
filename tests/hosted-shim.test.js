/* Conformance test for the HOSTED storage adapter (web/shim.js), run against the real built site (site/) in a real
 * browser, with the storage-path contract in STRICT mode. It proves four things about the adapter:
 *   1. the whole app runs on contract-valid paths only (no invalid_argument, no page errors)
 *   2. an invalid path is rejected exactly as the Claude artifact store would reject it
 *   3. only per-learner data is persisted; content documents never are (so new deploys always reach returning visitors)
 *   4. a learner's progress, in the default and in a non-default profile, survives a reload
 * Run:  node build_site.js && node tests/hosted-shim.test.js   (exit 1 on any failure) */
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const SITE = path.join(__dirname, "..", "site");
if (!fs.existsSync(path.join(SITE, "index.html"))) { console.error("FAILED: site/ is not built. Run: ./build.sh && node build_site.js"); process.exit(2); }
const results = [];
const check = (name, ok, detail) => { results.push(ok); console.log((ok ? "PASS " : "FAIL ") + name + (detail ? "  — " + detail : "")); };
const server = http.createServer((q, r) => {
  let p = decodeURIComponent(q.url.split("?")[0]); if (p === "/") p = "/index.html";
  const f = path.join(SITE, p); if (!f.startsWith(SITE) || !fs.existsSync(f)) { r.statusCode = 404; return r.end(); }
  r.setHeader("Content-Type", (f.endsWith(".json") ? "application/json" : "text/html") + "; charset=utf-8"); r.end(fs.readFileSync(f));
});
(async () => {
  await new Promise(r => server.listen(0, r));
  const base = "http://localhost:" + server.address().port + "/";
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1100, height: 800 } });
  await ctx.addInitScript(() => { window.__NJ_STRICT_PATHS = true; });
  const page = await ctx.newPage(); const errs = [];
  page.on("pageerror", e => errs.push(e.message)); page.on("console", m => { if (m.type() === "error" || /storage contract/.test(m.text())) errs.push(m.text()); });
  await page.goto(base); await page.waitForSelector('[data-login="me"]', { timeout: 20000 });
  // stale content copies saved by an older build must be cleared on load
  await page.evaluate(() => { localStorage.setItem("njdb:meta/lessons", JSON.stringify({ topics: { stale: 1 } })); localStorage.setItem("njdb:lessons/regressiont5", JSON.stringify({ title: "STALE" })); });
  await page.reload(); await page.waitForSelector('[data-login="me"]', { timeout: 20000 });
  await page.click('[data-login="me"]'); await page.waitForFunction(() => typeof S !== "undefined" && S.authed, null, { timeout: 20000 });
  for (const tab of ["learn", "bank", "mock", "progress", "admin", "home"]) { await page.evaluate(t => { location.hash = "#" + t; }, tab); await page.waitForTimeout(350); }
  const r = await page.evaluate(async () => {
    const db = await claude.use("db"), out = {};
    const tryDoc = p => { try { db.doc(p); return "accepted"; } catch (e) { return e.code; } };
    out.bad = tryDoc("data/users/u1/progress-snapshots/preimport-x"); out.good = tryDoc("data/users/u1/snapshots/preimport-x/record");
    const idx = (await db.doc("meta/lessons").get()).data(), l5 = (await db.doc("lessons/regressiont5").get()).data();
    out.indexCount = Object.keys(idx.topics).length; out.lessonTitle = l5 && l5.title;
    await db.doc("meta/lessons").set({ topics: { y: 1 } });                                  // the app's own rescan-style write
    out.contentWritePersisted = Object.keys(localStorage).some(k => /^njdb:(meta|lessons|qsets)\//.test(k));
    const uid = localStorage.getItem("njuid");
    await db.doc("data/users/" + uid + "/mastery").set({ m: { a: 1 }, v: 4 });
    await db.doc("data/users/" + uid + "/p/demo/attempts").set({ a: { q: { n: 1 } }, v: 4 });
    return out;
  });
  check("invalid path is rejected like the artifact store", r.bad === "invalid_argument", String(r.bad));
  check("contract path is accepted", r.good === "accepted");
  check("stale content copies from older builds were cleared (index is the deployed one)", r.indexCount >= 48 && /Multicollinearity/.test(r.lessonTitle || ""), "topics=" + r.indexCount + " lesson=" + r.lessonTitle);
  check("content documents are never persisted in the browser", r.contentWritePersisted === false);
  await page.reload(); await page.waitForSelector("#v-home, [data-login=\"me\"]", { timeout: 20000 });
  const kept = await page.evaluate(() => { const u = localStorage.getItem("njuid"); return { m: !!localStorage.getItem("njdb:data/users/" + u + "/mastery"), p: !!localStorage.getItem("njdb:data/users/" + u + "/p/demo/attempts"), c: Object.keys(localStorage).some(k => /^njdb:(meta|lessons|qsets)\//.test(k)) }; });
  check("learner progress (default profile) survives a reload", kept.m);
  check("learner progress (non-default profile) survives a reload", kept.p);
  check("no content copies after reload", kept.c === false);
  check("the app ran every tab on contract-valid paths with no errors", errs.length === 0, errs.slice(0, 3).join(" | "));
  await browser.close(); server.close();
  const fails = results.filter(x => !x).length;
  console.log("\n" + results.length + " checks, " + fails + " failed");
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("HARNESS FAILED", e); process.exit(1); });
