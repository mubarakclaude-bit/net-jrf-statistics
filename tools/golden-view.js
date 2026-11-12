#!/usr/bin/env node
/* Captures what a built-in view renders, in fixed states, so a refactor can be proved to change nothing.
 *
 *   node tools/golden-view.js <site-dir> <out.json> [route]        (route defaults to "progress")
 *
 * Serves the built site in <site-dir>, signs in, and records the view's exact HTML in three states: straight after
 * start-up, after "Load every module", and after attempts and an error log are added. Run it on the build BEFORE a change
 * and on the build AFTER, then compare the two files; they must be identical. Uses only the repository's own tooling. */
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const [dir, out, route = "progress"] = process.argv.slice(2);
if (!dir || !out) { console.error("usage: node tools/golden-view.js <site-dir> <out.json> [route]"); process.exit(2); }
const SITE = path.resolve(dir);

const server = http.createServer((q, r) => {
  let p = decodeURIComponent(q.url.split("?")[0]); if (p === "/") p = "/index.html";
  const f = path.join(SITE, p); if (!f.startsWith(SITE) || !fs.existsSync(f)) { r.statusCode = 404; return r.end(); }
  r.setHeader("Content-Type", (f.endsWith(".json") ? "application/json" : "text/html") + "; charset=utf-8"); r.end(fs.readFileSync(f));
});

(async () => {
  await new Promise(r => server.listen(0, r));
  const browser = await chromium.launch(), page = await browser.newPage({ viewport: { width: 1300, height: 900 } });
  const errs = []; page.on("pageerror", e => errs.push(e.message));
  await page.goto("http://localhost:" + server.address().port + "/");
  await page.waitForSelector('[data-login="me"]', { timeout: 20000 }); await page.click('[data-login="me"]');
  await page.waitForFunction(() => typeof S !== "undefined" && S.ready, null, { timeout: 30000 });
  const html = () => page.evaluate(r => document.getElementById("v-" + r).innerHTML, route);
  const go = async () => { await page.evaluate(r => { location.hash = "#" + r; }, route); await page.waitForSelector("#v-" + route + ".on"); await page.waitForTimeout(400); };
  const result = {};
  await go(); result.fresh = await html();
  const load = page.locator("#loadAllBtn");
  if (await load.count()) { await load.click(); await page.waitForFunction(() => document.querySelector("#loadAllBtn") && /Loaded/.test(document.querySelector("#loadAllBtn").textContent), null, { timeout: 120000 }).catch(() => {}); await page.waitForTimeout(800); }
  result.loaded = await html();
  await page.evaluate(() => {
    const ids = []; Object.keys(S.bank).sort().forEach(m => S.bank[m].slice(0, 6).forEach(q => ids.push(q.id)));
    ids.forEach((id, i) => { S.att[id] = { n: 1 + (i % 3), o: i % 3 ? 1 : 0 }; });
    const kinds = ERRT.map(e => e[0]);
    S.errs = Array.from({ length: 9 }, (_, i) => ({ type: kinds[i % kinds.length], fmt: FORDER[i % FORDER.length], stem: "golden stem " + i }));
    render();
  });
  await page.waitForTimeout(500);
  result.withData = await html();
  result.errors = errs;
  fs.writeFileSync(out, JSON.stringify(result, null, 1));
  console.log("captured " + route + ": " + Object.keys(result).filter(k => k !== "errors").map(k => k + "=" + result[k].length + " chars").join(", ") + (errs.length ? "  PAGE ERRORS: " + errs.join(" | ") : ""));
  await browser.close(); server.close(); process.exit(errs.length ? 1 : 0);
})().catch(e => { console.error("FAILED", e); process.exit(1); });
