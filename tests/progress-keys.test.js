#!/usr/bin/env node
/* Progress keys and the stored-progress migration (Issue #117), against the real built hosted site (site/) in a browser,
 * with the storage-path contract in STRICT mode.
 *
 * Ten June 2026 Q36 variant ids (j26v-q36-01 .. -10) belong to two different questions, one in the Official Statistics
 * bank and one in the Sampling bank. This proves:
 *   0. SCOPED_IDS in src/21-attempts.js is exactly the set of ids that seed/ gives to two DIFFERENT questions (different
 *      options or answer key; j26-q40/41 appear in two June 2026 sets as the same question and correctly share progress)
 *   1. the two questions get different progress keys; every other question's key is its id (so nothing saved moves)
 *   2. a legacy record is snapshotted, unambiguous ids stay in place, the ambiguous ones are quarantined (never assigned)
 *   3. attempts, flags, statuses, drill counts, mastery-draw history and the CSV export are independent per question
 *   4. all of it survives a hosted reload; a second load changes nothing (idempotent)
 *   5. a failed save of the snapshot or of the migrated record leaves the stored record untouched, and a later load retries
 *   6. the snapshot restores the legacy record exactly
 * Run:  npm run build && node tests/progress-keys.test.js   (exit 1 on any failure). tests/hosted-shim.test.js runs it too,
 * so the CI step for the hosted adapter covers it. */
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.join(__dirname, ".."), SITE = path.join(ROOT, "site");
if (!fs.existsSync(path.join(SITE, "index.html"))) { console.error("FAILED: site/ is not built. Run: npm run build"); process.exit(2); }
const results = [];
const check = (name, ok, detail) => { results.push(!!ok); console.log((ok ? "PASS " : "FAIL ") + name + (ok || !detail ? "" : "  — " + detail)); };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

/* ---- 0. the registry matches the seeds ---- */
const src = fs.readFileSync(path.join(ROOT, "src", "21-attempts.js"), "utf8");
const SCOPED = Function("return " + /const SCOPED_IDS=(\{[^;]*\});/.exec(src)[1])();
const byId = {};
for (const f of fs.readdirSync(path.join(ROOT, "seed")).filter(f => f.endsWith(".json")).sort()) {
  let d; try { d = JSON.parse(fs.readFileSync(path.join(ROOT, "seed", f), "utf8")); } catch (e) { continue; }
  if (!d || !Array.isArray(d.items) || !d.moduleId) continue;
  for (const it of d.items) if (it && it.id) (byId[it.id] = byId[it.id] || []).push({ set: f.slice(0, -5), body: JSON.stringify([it.options, it.answer]) });   // same options and key = the same question, however its stem was transcribed
}
const collide = {};
for (const [id, recs] of Object.entries(byId)) if (recs.length > 1 && new Set(recs.map(r => r.body)).size > 1) collide[id] = recs.map(r => r.set).sort();
check("SCOPED_IDS lists exactly the ids that seed/ gives to two different questions", same(Object.keys(collide).sort(), Object.keys(SCOPED).sort()),
  "seed: " + Object.keys(collide).sort().join(",") + " | SCOPED_IDS: " + Object.keys(SCOPED).sort().join(","));
check("each scoped id names the sets it occurs in", Object.keys(SCOPED).every(id => same((SCOPED[id] || []).slice().sort(), collide[id])));
check("an id repeated with identical content (the same question in two sets) is not scoped",
  Object.entries(byId).filter(([, r]) => r.length > 1 && new Set(r.map(x => x.body)).size === 1).every(([id]) => !(id in SCOPED)));

/* ---- browser ---- */
const data = JSON.parse(fs.readFileSync(path.join(SITE, "data.json"), "utf8"));
const OFF = "official_pyq_variants", SMP = "sampling_pyq_variants";
const uniq = set => data["qsets/" + set].items.map(i => i.id).find(id => !(id in SCOPED));
const U_OFF = uniq(OFF), U_SMP = uniq(SMP);
const UID = "ltestpk1";
const LEGACY = { a: { "j26v-q36-01": { n: 3, o: 1, f: 1, t: 1700000000000 }, "j26v-q36-02": { n: 1, o: 0, t: 1700000000001 },
                      [U_OFF]: { n: 2, o: 1, t: 1700000000002 }, [U_SMP]: { n: 1, o: 0, f: 1, t: 1700000000003 } }, v: 4 };
const MASTERY = { m: { "sampling-t1": { state: "failed", best: 60, last: 60, attempts: 1, served: ["sampling-t1-m01", "sampling-t1-m02"] } }, v: 4 };
const K = p => "njdb:data/users/" + UID + "/" + p;

const server = http.createServer((q, r) => {
  let p = decodeURIComponent(q.url.split("?")[0]); if (p === "/") p = "/index.html";
  const f = path.join(SITE, p); if (!f.startsWith(SITE) || !fs.existsSync(f)) { r.statusCode = 404; return r.end(); }
  r.setHeader("Content-Type", (f.endsWith(".json") ? "application/json" : "text/html") + "; charset=utf-8"); r.end(fs.readFileSync(f));
});

async function context(browser, errs) {
  const ctx = await browser.newContext({ viewport: { width: 1100, height: 800 } });
  await ctx.addInitScript(() => {
    window.__NJ_STRICT_PATHS = true;
    // a test-controlled write failure: any njdb key containing the text in localStorage "njtest:fail" refuses to save
    const orig = Storage.prototype.setItem;
    Storage.prototype.setItem = function (k, v) {
      const f = orig.call ? Storage.prototype.getItem.call(this, "njtest:fail") : null;
      if (f && String(k).indexOf("njdb:") === 0 && String(k).indexOf(f) >= 0) { const e = new Error("QuotaExceededError (test)"); e.name = "QuotaExceededError"; throw e; }
      return orig.call(this, k, v);
    };
  });
  const page = await ctx.newPage();
  page.on("pageerror", e => errs.push(e.message));
  page.on("console", m => { if (m.type() === "error" || /storage contract/.test(m.text())) errs.push(m.text()); });
  return { ctx, page };
}
async function seed(page, base, fail) {
  await page.goto(base); await page.waitForSelector('[data-login="me"]', { timeout: 20000 });
  await page.evaluate(([uid, att, mas, k1, k2, fail]) => {
    localStorage.clear(); localStorage.setItem("njuid", uid);
    localStorage.setItem(k1, JSON.stringify(att)); localStorage.setItem(k2, JSON.stringify(mas));
    if (fail) localStorage.setItem("njtest:fail", fail);
  }, [UID, LEGACY, MASTERY, K("attempts"), K("mastery"), fail || ""]);
}
async function login(page) {
  await page.reload(); await page.waitForFunction(() => typeof S !== "undefined" && S.ready, null, { timeout: 20000 });
  if (!(await page.evaluate(() => S.authed))) { await page.waitForSelector('[data-login="me"]', { timeout: 20000 }); await page.click('[data-login="me"]'); }
  await page.waitForFunction(() => typeof S !== "undefined" && S.authed && S.pkMigration, null, { timeout: 20000 });
  await page.evaluate(async () => { await loadBank("official"); await loadBank("sampling"); });
}
const stored = (page, p) => page.evaluate(k => { const s = localStorage.getItem(k); return s === null ? null : JSON.parse(s); }, K(p));
// the two questions that share j26v-q36-01, and one unique question from each bank, as the app holds them
const Q = `const off=S.bank.official.find(q=>q.id==="j26v-q36-01"),smp=S.bank.sampling.find(q=>q.id==="j26v-q36-01");`;

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = "http://localhost:" + server.address().port + "/";
  const browser = await chromium.launch();

  /* ---- 1-4, 6: migration, independence, reload, idempotency, restore ---- */
  {
    const errs = [], { ctx, page } = await context(browser, errs);
    await seed(page, base); await login(page);
    const r = await page.evaluate(new Function(Q + `return {mig:S.pkMigration, kOff:progressKeyOf(off), kSmp:progressKeyOf(smp),
      setOff:off.setId, setSmp:smp.setId, sOff:statusOf(off), sSmp:statusOf(smp), fOff:isFlagged(off), fSmp:isFlagged(smp),
      uOff:statusOf(S.bank.official.find(q=>q.id===${JSON.stringify(U_OFF)})), uSmp:statusOf(S.bank.sampling.find(q=>q.id===${JSON.stringify(U_SMP)})),
      uKey:progressKeyOf(S.bank.official.find(q=>q.id===${JSON.stringify(U_OFF)})), raw:Object.keys(S.att).filter(k=>k.indexOf("j26v-q36-")===0)}`));
    check("the two questions sharing j26v-q36-01 have different progress keys", r.kOff !== r.kSmp && r.kOff === OFF + "::j26v-q36-01" && r.kSmp === SMP + "::j26v-q36-01", r.kOff + " / " + r.kSmp);
    check("a unique question's progress key is its id (legacy compatible)", r.uKey === U_OFF, r.uKey);
    check("migration ran and moved exactly the two ambiguous legacy records", r.mig.state === "migrated" && r.mig.moved === 2, JSON.stringify(r.mig));
    check("unambiguous legacy results are still read in place", r.uOff === "correct" && r.uSmp === "wrong", r.uOff + "/" + r.uSmp);
    check("the ambiguous legacy result is given to NEITHER question", r.sOff === "unseen" && r.sSmp === "unseen" && !r.fOff && !r.fSmp && r.raw.length === 0, JSON.stringify(r));
    const doc = await stored(page, "attempts"), snap = await stored(page, "snapshots/premigrate-pk2/record");
    check("stored attempts record is versioned (pk 2)", doc && doc.pk === 2 && doc.v === 4, JSON.stringify(doc && { pk: doc.pk, v: doc.v }));
    check("stored record keeps every unambiguous legacy result unchanged", doc && same(doc.a[U_OFF], LEGACY.a[U_OFF]) && same(doc.a[U_SMP], LEGACY.a[U_SMP]));
    check("stored record has no raw ambiguous key", doc && !("j26v-q36-01" in doc.a) && !("j26v-q36-02" in doc.a));
    check("the ambiguous legacy records are quarantined intact with both candidate sets",
      doc && doc.quarantine && same(doc.quarantine["j26v-q36-01"].legacy, LEGACY.a["j26v-q36-01"]) && same(doc.quarantine["j26v-q36-02"].legacy, LEGACY.a["j26v-q36-02"]) &&
      same(doc.quarantine["j26v-q36-01"].candidates, [OFF, SMP]), JSON.stringify(doc && doc.quarantine));
    check("a pre-migration snapshot holds the legacy attempts and the other records exactly as loaded",
      snap && snap.format === "net-jrf-statistics-premigration" && same(snap.records.attempts, LEGACY) && same(snap.records.mastery, MASTERY) && snap.records.notes === null, JSON.stringify(snap && Object.keys(snap)));
    const valid = await page.evaluate(([a, b]) => [window.__NJ_PATHS.checkDocPath(a).ok, window.__NJ_PATHS.checkDocPath(b).ok],
      ["data/users/" + UID + "/snapshots/premigrate-pk2/record", "data/users/" + UID + "/p/demo/snapshots/premigrate-pk2/record"]);
    check("snapshot paths (default and non-default profile) satisfy the storage contract", valid[0] && valid[1]);

    // independent state: attempts, flags, drill count, bank rows, mastery-draw history, export
    const ind = await page.evaluate(new Function(Q + `
      record(off,true);flagQ(off);
      const afterOff={sOff:statusOf(off),sSmp:statusOf(smp),fOff:isFlagged(off),fSmp:isFlagged(smp)};
      startDrill([off,smp],0);const drill1=/1 \\/ 2 answered/.test(drillHTML());
      record(smp,false);
      const drill2=/2 \\/ 2 answered/.test(drillHTML());S.drill=null;
      const rows=[qrow(off),qrow(smp)].map(h=>/data-q="([^"]+)"/.exec(h)[1]);
      const pick=drawPaper([off,smp],{draw:1},[progressKeyOf(off)]).map(progressKeyOf);
      const wrongFirst=drawPaper([off,smp],{draw:3,diffMix:null},[]).map(progressKeyOf);
      const csv=exportCsv().split("\\n").filter(l=>l.indexOf('"j26v-q36-01"')>=0);
      return {afterOff,drill1,drill2,rows,pick,csv,sOff:statusOf(off),sSmp:statusOf(smp),fSmp:isFlagged(smp),
              mst:(()=>{const a=mstat(modById("official")),b=mstat(modById("sampling"));return [a.att,b.att]})()}`));
    check("an attempt and a flag on the Official question leave the Sampling question untouched",
      ind.afterOff.sOff === "correct" && ind.afterOff.sSmp === "unseen" && ind.afterOff.fOff && !ind.afterOff.fSmp, JSON.stringify(ind.afterOff));
    check("each question keeps its own result", ind.sOff === "correct" && ind.sSmp === "wrong" && !ind.fSmp);
    check("the drill counts each question separately", ind.drill1 && ind.drill2);
    check("bank rows open the right question (distinct data-q keys)", ind.rows[0] === OFF + "::j26v-q36-01" && ind.rows[1] === SMP + "::j26v-q36-01", ind.rows.join(" "));
    check("mastery-draw history: a question served last time yields to the other one with the same id", same(ind.pick, [SMP + "::j26v-q36-01"]), ind.pick.join(","));
    check("the CSV export lists both questions with their own key and result",
      ind.csv.length === 2 && ind.csv.some(l => /"correct".*"yes","official_pyq_variants::j26v-q36-01"/.test(l)) && ind.csv.some(l => /"wrong".*"no","sampling_pyq_variants::j26v-q36-01"/.test(l)), ind.csv.join(" || "));
    // the bank click handler finds the Sampling question, not the first question with that id
    const opened = await page.evaluate(async key => { S.filt = { mod: "sampling", fmt: "", src: "", st: "wrong", paper: S.filt && S.filt.paper }; location.hash = "#bank"; await new Promise(r => setTimeout(r, 300)); render();
      const el = document.querySelector('[data-q="' + key + '"]'); if (!el) return "row not shown"; el.click(); await new Promise(r => setTimeout(r, 100));
      const q = S.drill && S.drill.list[S.drill.i]; const out = q ? q.setId + "::" + q.id : "no drill"; S.drill = null; return out; }, SMP + "::j26v-q36-01");
    check("clicking the Sampling row opens the Sampling question", opened === SMP + "::j26v-q36-01", opened);
    await page.waitForTimeout(1200);                      // the debounced save
    const after = await stored(page, "attempts");
    check("saves after migration keep pk, quarantine and both scoped results",
      after.pk === 2 && same(after.quarantine, doc.quarantine) && after.a[OFF + "::j26v-q36-01"].o === 1 && after.a[SMP + "::j26v-q36-01"].o === 0 && after.a[OFF + "::j26v-q36-01"].f === 1);

    // hosted reload: independent state persists, the migration does not run twice, the snapshot is not rewritten
    await login(page);
    const rr = await page.evaluate(new Function(Q + `return {mig:S.pkMigration.state,sOff:statusOf(off),sSmp:statusOf(smp),fOff:isFlagged(off),fSmp:isFlagged(smp),q:Object.keys(S.attQuar).sort()}`));
    check("after a reload each question still has its own result and flag", rr.sOff === "correct" && rr.sSmp === "wrong" && rr.fOff && !rr.fSmp, JSON.stringify(rr));
    check("a second load does not migrate again (idempotent)", rr.mig === "current" && same(rr.q, ["j26v-q36-01", "j26v-q36-02"]), JSON.stringify(rr));
    const snap2 = await stored(page, "snapshots/premigrate-pk2/record"), doc2 = await stored(page, "attempts");
    check("the snapshot is never rewritten", same(snap2, snap));
    check("a load without changes leaves the stored record as it was", same(doc2, after));
    check("the mastery record is untouched by the migration", same(await stored(page, "mastery"), MASTERY));

    // restore: the legacy record comes back exactly; the next load migrates it to the same result
    const ok = await page.evaluate(() => restorePkSnapshot());
    check("restore puts the pre-migration record back exactly", ok === true && same(await stored(page, "attempts"), LEGACY));
    // a save after the restore (same session, no reload) must not write the migrated record back over it
    await page.evaluate(id => { record(S.bank.official.find(q => q.id === id), true); }, U_OFF);
    await page.waitForTimeout(1200);
    const ar = await stored(page, "attempts");
    check("a save after restore keeps the restored legacy record (no pk, ambiguous key still present)",
      ar && !("pk" in ar) && same(ar.a["j26v-q36-01"], LEGACY.a["j26v-q36-01"]) && ar.a[U_OFF].n === LEGACY.a[U_OFF].n + 1, JSON.stringify(ar && Object.keys(ar)));
    await page.evaluate(id => { const a = S.att[id]; a.n -= 1; }, U_OFF); await page.evaluate(() => saveAtt()); await page.waitForTimeout(1200);
    await login(page);
    const re = await stored(page, "attempts");
    check("migrating the restored record gives the same quarantine and keeps the snapshot", re.pk === 2 && same(re.quarantine, doc.quarantine) && same(await stored(page, "snapshots/premigrate-pk2/record"), snap));
    check("no page errors and no storage-contract violations (migration run)", errs.length === 0, errs.slice(0, 3).join(" | "));
    await ctx.close();
  }

  /* ---- 5a: the migrated record fails to save, then a later load succeeds ---- */
  {
    const errs = [], { ctx, page } = await context(browser, errs);
    await seed(page, base, "/attempts"); await login(page);
    const f = await page.evaluate(new Function(Q + `return {mig:S.pkMigration,raw:S.att["j26v-q36-01"],pk:S.attPk,sOff:statusOf(off),sSmp:statusOf(smp)}`));
    check("a failed save of the migrated record is reported, not assumed", f.mig.state === "failed", JSON.stringify(f.mig));
    check("after the failure the stored legacy record is untouched", same(await stored(page, "attempts"), LEGACY));
    check("after the failure the legacy keys stay in memory, and neither question claims them", same(f.raw, LEGACY.a["j26v-q36-01"]) && f.pk === 1 && f.sOff === "unseen" && f.sSmp === "unseen", JSON.stringify(f));
    const snapA = await stored(page, "snapshots/premigrate-pk2/record");
    check("the snapshot was written before the failed step", snapA && same(snapA.records.attempts, LEGACY));
    await page.evaluate(() => localStorage.removeItem("njtest:fail"));
    await login(page);
    const g = await page.evaluate(() => S.pkMigration.state), d = await stored(page, "attempts");
    check("the next load retries and succeeds", g === "migrated" && d.pk === 2 && same(d.quarantine["j26v-q36-01"].legacy, LEGACY.a["j26v-q36-01"]), g);
    check("the retry keeps the first snapshot", same(await stored(page, "snapshots/premigrate-pk2/record"), snapA));
    const noise = errs.filter(e => !/QuotaExceededError|could not save|unavailable/i.test(e));
    check("no unexpected page errors (save-failure run)", noise.length === 0, noise.slice(0, 3).join(" | "));
    await ctx.close();
  }

  /* ---- 5b: the snapshot fails to save: nothing is migrated ---- */
  {
    const errs = [], { ctx, page } = await context(browser, errs);
    await seed(page, base, "/snapshots/"); await login(page);
    const st = await page.evaluate(() => S.pkMigration.state);
    check("when the snapshot cannot be saved, the migration does not run", st === "failed", st);
    check("...and the stored record is untouched", same(await stored(page, "attempts"), LEGACY));
    check("...and no snapshot exists", (await stored(page, "snapshots/premigrate-pk2/record")) === null);
    const viaDb = await page.evaluate(async () => (await (await claude.use("db")).doc(snapshotPath()).get()).exists);
    check("...and the store does not report the failed snapshot as saved", viaDb === false);
    await ctx.close();
  }

  /* ---- a failed read of the attempts record is not an empty record ---- */
  {
    const errs = [], { ctx, page } = await context(browser, errs);
    await seed(page, base); await login(page);
    const before = await stored(page, "attempts");
    const r = await page.evaluate(async id => {
      const realDoc = S.db.doc.bind(S.db);
      S.db.doc = p => { const d = realDoc(p); if (/\/attempts$/.test(p)) return Object.assign({}, d, { get: async () => { const e = new Error("unavailable (test)"); e.code = "unavailable"; throw e; } }); return d; };
      await loadProfileData();
      const st = { failed: S.attLoadFailed, mig: S.pkMigration.state };
      record(S.bank.official.find(q => q.id === id), false);
      S.db.doc = realDoc;
      return st;
    }, U_OFF);
    await page.waitForTimeout(1200);
    check("a failed attempts read is flagged and not migrated", r.failed === true && r.mig === "read-failed", JSON.stringify(r));
    check("...and nothing is written over the stored record that session", same(await stored(page, "attempts"), before));
    await login(page);
    check("the next normal load reads and keeps the record", (await page.evaluate(() => S.attLoadFailed)) === false && same(await stored(page, "attempts"), before));
    const noise = errs.filter(e => !/unavailable \(test\)/i.test(e));
    check("no unexpected page errors (read-failure run)", noise.length === 0, noise.slice(0, 3).join(" | "));
    await ctx.close();
  }

  /* ---- a learner with nothing ambiguous: no snapshot, nothing moved ---- */
  {
    const errs = [], { ctx, page } = await context(browser, errs);
    await page.goto(base); await page.waitForSelector('[data-login="me"]', { timeout: 20000 });
    const clean = { a: { [U_OFF]: { n: 1, o: 1, t: 1 } }, v: 4 };
    await page.evaluate(([uid, k, d]) => { localStorage.clear(); localStorage.setItem("njuid", uid); localStorage.setItem(k, JSON.stringify(d)); }, [UID, K("attempts"), clean]);
    await login(page);
    const st = await page.evaluate(() => S.pkMigration.state);
    check("a record with no ambiguous ids needs no snapshot and moves nothing", st === "nothing-to-move" && (await stored(page, "snapshots/premigrate-pk2/record")) === null && same(await stored(page, "attempts"), clean), st);
    check("no page errors (clean learner)", errs.length === 0, errs.slice(0, 3).join(" | "));
    await ctx.close();
  }

  await browser.close(); server.close();
  const fails = results.filter(x => !x).length;
  console.log("\n" + results.length + " checks, " + fails + " failed");
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("HARNESS FAILED", e); process.exit(1); });
