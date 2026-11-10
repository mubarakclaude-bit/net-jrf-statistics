/* Runs every feature's own test (src/features/<id>/test.js) against the built hosted site.
 *   node build_site.js && node tests/features.test.js            all features
 *   node tests/features.test.js --only ref-counter                one feature
 *
 * Each feature gets a FRESH browser context, with the storage-path contract in strict mode (an invalid path throws), and
 * fails if its page logs any error. Generic checks run for every feature, so a contributor writes only the behaviour
 * that is specific to their feature:
 *   - its section exists and becomes visible at #f-<id>
 *   - it appears in the navigation bar exactly when its manifest says tab:true
 *   - its own test passes
 *   - no page error, no failed console call, while it ran
 * The test file exports  async function (t)  with  t = { id, page, open(), expect(name, ok, detail) }. */
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.join(__dirname, "..");
const SITE = path.join(ROOT, "site"), FEATURES = path.join(ROOT, "src", "features");
if (!fs.existsSync(path.join(SITE, "index.html"))) { console.error("FAILED: site/ is not built. Run: npm run build"); process.exit(2); }
const only = process.argv.includes("--only") ? process.argv[process.argv.indexOf("--only") + 1] : null;
const verbose = process.argv.includes("--verbose");          // also print every passing check, not only the failures
const ids = (fs.existsSync(FEATURES) ? fs.readdirSync(FEATURES, { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name).sort() : []).filter(i => !only || i === only);
if (!ids.length) { console.log(only ? "FAILED: no feature named " + only : "no features to test"); process.exit(only ? 1 : 0); }

const server = http.createServer((q, r) => {
  let p = decodeURIComponent(q.url.split("?")[0]); if (p === "/") p = "/index.html";
  const f = path.join(SITE, p); if (!f.startsWith(SITE) || !fs.existsSync(f)) { r.statusCode = 404; return r.end(); }
  r.setHeader("Content-Type", (f.endsWith(".json") ? "application/json" : "text/html") + "; charset=utf-8"); r.end(fs.readFileSync(f));
});

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = "http://localhost:" + server.address().port + "/";
  const browser = await chromium.launch();
  let failed = 0, total = 0;
  for (const id of ids) {
    const manifest = JSON.parse(fs.readFileSync(path.join(FEATURES, id, "feature.json"), "utf8"));
    // A feature's test may export contextOptions (for example { timezoneId: "Pacific/Kiritimati" }) to run in a particular
    // browser setting. Playwright can only set these when the context is created, so the test file is loaded first.
    let testFn = null, loadError = null;
    try { testFn = require(path.join(FEATURES, id, "test.js")); } catch (e) { loadError = e; }
    const ctx = await browser.newContext(Object.assign({ viewport: { width: 1100, height: 800 } }, (testFn && testFn.contextOptions) || {}));
    await ctx.addInitScript(() => { window.__NJ_STRICT_PATHS = true; });
    const page = await ctx.newPage(), errs = [], lines = [];
    page.on("pageerror", e => errs.push(e.message));
    page.on("console", m => { if (m.type() === "error" || /storage contract/.test(m.text())) errs.push(m.text()); });
    const expect = (name, ok, detail) => { lines.push({ name, ok: !!ok, detail }); };
    const t = { id, page, expect, open: async () => {
      await page.evaluate(i => { location.hash = "#f-" + i; }, id);
      await page.waitForSelector("#v-f-" + id + ".on", { timeout: 10000 });
      await page.waitForTimeout(250);
    } };
    try {
      await page.goto(base); await page.waitForSelector('[data-login="me"]', { timeout: 20000 });
      await page.click('[data-login="me"]'); await page.waitForFunction(() => typeof S !== "undefined" && S.authed, null, { timeout: 20000 });
      expect("registered with the app", await page.evaluate(i => typeof FEATURES !== "undefined" && !!FEATURES[i], id));
      expect("has a section in the page", await page.evaluate(i => !!document.getElementById("v-f-" + i), id));
      expect("navigation shows it exactly when its manifest says tab:" + manifest.tab,
        (await page.locator('#nav [data-tab="f-' + id + '"]').count()) === (manifest.tab ? 1 : 0));
      await t.open();
      expect("is visible at #f-" + id, await page.evaluate(i => document.getElementById("v-f-" + i).classList.contains("on"), id));
      expect("did not fall back to the error card", (await page.locator("#v-f-" + id).textContent()).indexOf("failed to display") < 0);
      if (loadError) throw loadError;
      await testFn(t);
    } catch (e) { expect("its test ran to the end", false, String(e && e.message || e).split("\n")[0]); }
    expect("no page error or console error while it ran", errs.length === 0, errs.slice(0, 2).join(" | "));
    const bad = lines.filter(l => !l.ok);
    console.log((bad.length ? "FAIL " : "PASS ") + "feature " + id + "  (" + (lines.length - bad.length) + "/" + lines.length + " checks)");
    if (verbose) for (const l of lines.filter(x => x.ok)) console.log("     ok " + l.name);
    for (const l of bad) console.log("     x " + l.name + (l.detail ? "  — " + String(l.detail).slice(0, 160) : ""));
    failed += bad.length; total += lines.length;
    await ctx.close();
  }
  await browser.close(); server.close();
  console.log("\n" + ids.length + " feature(s), " + total + " checks, " + failed + " failed");
  process.exit(failed ? 1 : 0);
})().catch(e => { console.error("HARNESS FAILED", e); process.exit(1); });
