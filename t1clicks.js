/* 4.1 driven ONLY by real clicks — the failure mode that bit this lesson twice was a
   handler that threw before render(), so programmatic gotoScene() passed while the UI
   did nothing. Nothing here calls gotoScene. */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  p.on('console', m => { if (m.type() === 'error' && !/ERR_TUNNEL|fonts\.g/.test(m.text())) errs.push('CONSOLE: ' + m.text()); });
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1300);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }

  await p.click('[data-tab="learn"]'); await p.waitForTimeout(300);
  await p.click('[data-mod="inference"]').catch(() => {});
  await p.waitForTimeout(250);
  await p.click('[data-topic="inference-t1"]'); await p.waitForTimeout(900);
  console.log('opened 4.1 by click; on overview = ' + await p.evaluate(() => S.learn.i < 0));

  // the button the user reported dead
  const start = p.locator('[data-sc="0"]').first();
  console.log('start control present: ' + (await start.count() > 0));
  await start.click(); await p.waitForTimeout(500);
  let at = await p.evaluate(() => S.learn.i);
  console.log('after clicking Start  -> scene index ' + at + (at === 0 ? '  OK' : '  <-- DEAD'));

  // walk the whole lesson forward using only the footer Next control
  const total = await p.evaluate(() => S.lessons['inference-t1'].scenes.length);
  let stalled = [];
  for (let i = 1; i < total; i++) {
    const nx = p.locator('.scnav [data-sc="' + i + '"]').first();
    if (!await nx.count()) { stalled.push(i + ' (no next control)'); break; }
    await nx.click(); await p.waitForTimeout(260);
    const now = await p.evaluate(() => S.learn.i);
    if (now !== i) stalled.push(i + ' (landed ' + now + ')');
  }
  console.log('forward walk by Next, ' + total + ' scenes: ' + (stalled.length ? 'STALLED at ' + stalled.join(', ') : 'all advanced'));

  // the contents chips — the second control the user reported dead
  // open the contents panel only if it is currently closed — clicking blind just closes it
  if (!await p.evaluate(() => !!S.navOpen)) { await p.click('[data-nav-toggle="1"]'); await p.waitForTimeout(350); }
  console.log('contents panel open: ' + await p.evaluate(() => !!S.navOpen));
  const jumps = [2, 9, 5, 14, 1];
  const bad = [];
  for (const j of jumps) {
    const chip = p.locator('.scrow [data-sc="' + j + '"], [data-sc="' + j + '"]').first();
    if (!await chip.count()) { bad.push(j + ' (missing)'); continue; }
    await chip.click(); await p.waitForTimeout(280);
    const now = await p.evaluate(() => S.learn.i);
    if (now !== j) bad.push(j + ' (landed ' + now + ')');
  }
  console.log('contents jumps ' + jumps.join(',') + ': ' + (bad.length ? 'FAILED ' + bad.join(', ') : 'all landed'));

  // the foundation self-rating buttons, since scene 1 was reframed
  const f0 = await p.evaluate(() => S.lessons['inference-t1'].scenes[0].id);
  const chip0 = p.locator('[data-sc="0"]').first(); await chip0.click(); await p.waitForTimeout(300);
  const marks = await p.locator('[data-found]').count();
  console.log('foundation: ' + marks + ' rating buttons on ' +
    await p.evaluate(() => S.lessons['inference-t1'].scenes[0].items.length) + ' checks');
  await p.locator('[data-found="' + f0 + '|1|shaky"]').click(); await p.waitForTimeout(300);
  console.log('marking check 2 shaky reveals the rebuild: ' + (await p.locator('.frefresh').count() > 0));

  // progress actually recorded (markSeen was the crash site)
  // optional JRF-extension scenes: marked in the UI, and not required for completion
  {
    const ex = await p.evaluate(() => S.lessons['inference-t1'].scenes
      .map((s, i) => ({ i, ext: !!s.ext, kind: s.kind })).filter(s => s.ext));
    console.log('extension scenes: ' + (ex.length ? ex.map(e => (e.i + 1) + ' (' + e.kind + ')').join(', ') : 'NONE'));
    if (ex.length) {
      await p.locator('[data-sc="' + ex[0].i + '"]').first().click(); await p.waitForTimeout(300);
      const chip = await p.locator('.schead .chip.ext').count();
      const banner = await p.evaluate(() => /Optional — come back/.test(document.querySelector('.wscanvas').innerText));
      console.log('  chip on the scene head: ' + (chip ? 'yes' : 'NO') + ' · opt-out banner: ' + (banner ? 'yes' : 'NO'));
      const railed = await p.evaluate(() => /optional/i.test(
        (document.querySelector('.navtp, .steprail, .wsnav') || document.body).innerText));
      console.log('  marked in the contents rail: ' + (railed ? 'yes' : 'NO'));
      // reset, walk the CORE scenes only, and the topic must still read complete
      const st = await p.evaluate(exi => {
        const les = S.lessons['inference-t1'];
        S.topics['inference-t1'] = { s: 0, seen: [] }; S.learn.seen = {};
        les.scenes.forEach((x, i) => { if (!x.ext) markSeen(x.id); });
        const r = S.topics['inference-t1'];
        return { seen: r.seen.length, of: les.scenes.length, s: r.s,
                 skipped: les.scenes.filter(x => x.ext).length };
      }, ex[0].i);
      console.log('  core only (' + st.seen + ' of ' + st.of + ' seen, ' + st.skipped +
        ' extension skipped): state=' + (st.s === 2 ? 'complete  OK' : 's=' + st.s + '  <-- BLOCKED by an optional scene'));
    }
  }
  console.log('progress recorded: ' + await p.evaluate(() => {
    const r = (S.topics && S.topics['inference-t1']) || {};
    const n = S.lessons['inference-t1'].scenes.length;
    return (r.seen || []).length + ' of ' + n + ' scenes seen, state=' + (r.s === 2 ? 'complete' : r.s === 1 ? 'in progress' : 'NOT STARTED');
  }));
  console.log(errs.length ? 'ERRORS:\n' + errs.join('\n') : 'no runtime errors');
  await b.close();
})();
