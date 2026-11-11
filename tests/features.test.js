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
    // A feature normally lives at #f-<id>; one that "replaces" a built-in view lives at that view's own route.
    const route = manifest.replaces || "f-" + id;
    const t = { id, page, expect, open: async () => {
      await page.evaluate(r => { location.hash = "#" + r; }, route);
      await page.waitForSelector("#v-" + route + ".on", { timeout: 10000 });
      await page.waitForTimeout(250);
    } };
    try {
      await page.goto(base); await page.waitForSelector('[data-login="me"]', { timeout: 20000 });
      await page.click('[data-login="me"]'); await page.waitForFunction(() => typeof S !== "undefined" && S.authed, null, { timeout: 20000 });
      expect("registered with the app", await page.evaluate(i => typeof FEATURES !== "undefined" && !!FEATURES[i], id));
      expect("has a section in the page", await page.evaluate(r => !!document.getElementById("v-" + r), route));
      expect(manifest.replaces ? "its built-in tab '" + route + "' is still in the navigation bar, exactly once" : "navigation shows it exactly when its manifest says tab:" + manifest.tab,
        (await page.locator('#nav [data-tab="' + route + '"]').count()) === (manifest.replaces || manifest.tab ? 1 : 0));
      if (id === ids[0]) {          // the host interface (ctx.app, version 2) is checked once per run, whichever feature runs first
        const h = await page.evaluate(() => {
          const a = FEATURES[Object.keys(FEATURES)[0]].ctx.app, out = {}, cfg0 = a.settings.get();
          out.version = a.version;
          const ls = a.lessons(); out.lessons = ls.length; out.expectLessons = Object.keys(S.lessonIdx.topics).length;
          out.shape = ls.length > 0 && ls.every(l => l.topicId && l.title && l.moduleId);
          const t0 = ls[0].title; ls[0].title = "changed by a feature"; out.lessonsCopy = a.lessons()[0].title === t0 && S.lessonIdx.topics[ls[0].topicId].title === t0;
          const lp = a.learnProgress(); out.lp = lp.withLesson === out.expectLessons; lp.withLesson = -1; out.lpCopy = a.learnProgress().withLesson === out.expectLessons;
          const g = a.settings.get(); g.exam = "mutated"; out.getCopy = a.settings.get().exam === cfg0.exam;
          try { a.navigate("no-such-route"); out.navBad = "accepted"; } catch (e) { out.navBad = String(e.message); }
          a.navigate("learn"); out.navOk = location.hash === "#learn";
          return out;
        });
        await page.waitForFunction(() => S.route === "learn", null, { timeout: 5000 }).catch(() => {});
        expect("host interface v2: version is 2", h.version === 2, h.version);
        expect("host interface v2: lessons() lists every lesson with topicId, title and moduleId", h.lessons > 0 && h.lessons === h.expectLessons && h.shape, JSON.stringify(h));
        expect("host interface v2: lessons(), learnProgress() and settings.get() return copies a feature cannot corrupt", h.lessonsCopy && h.lpCopy && h.getCopy && h.lp, JSON.stringify(h));
        expect("host interface v2: navigate() goes to a known route and refuses an unknown one, naming the known routes", h.navOk && /not a route/.test(h.navBad) && /learn/.test(h.navBad), h.navBad);
        expect("host interface v2: the route actually changed", await page.evaluate(() => S.route === "learn"));
      }
      await t.open();
      expect("is visible at #" + route, await page.evaluate(r => document.getElementById("v-" + r).classList.contains("on"), route));
      expect("did not fall back to the error card", (await page.locator("#v-" + route).textContent()).indexOf("failed to display") < 0);
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
