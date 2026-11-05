// Click-driven walk: no gotoScene() calls, no evaluate() shortcuts. For every authored
// topic, click the real tree row, click the real start button, then click Continue all
// the way to the quiz. This is the test that was missing: every earlier topic test drove
// the stepper programmatically, so a dead button could not have been caught.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  p.on('console', m => { if (m.type() === 'error' && !/ERR_TUNNEL|fonts\.g/.test(m.text())) errs.push('CONSOLE ' + m.text()); });
  await p.goto('file://' + require('path').join(__dirname, '.cache', 'harness.html')); await p.waitForTimeout(1500);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(800); }
  await p.click('[data-tab="learn"]'); await p.waitForTimeout(400);

  await p.waitForFunction(() => !!(S.lessonIdx && S.lessonIdx.topics), null, { timeout: 15000 });
  const topics = await p.evaluate(() => Object.keys(S.lessonIdx.topics).sort());
  let fails = 0; const bad = m => { fails++; console.log('   FAIL ' + m); };

  for (const tid of topics) {
    // open every module so the row is clickable, then click the row itself
    // leave any open lesson and show the path tree, so the row is on screen
    await p.evaluate(() => { S.navOpen = true; S.catalog.modules.forEach(m => S.open[m.id] = true);
      resetLearn(null); render(); });
    await p.waitForTimeout(250);
    const row = p.locator('[data-topic="' + tid + '"]');
    if (!await row.count()) { bad(tid + ': no row in the tree'); continue; }
    await row.first().click();
    // wait for the overview to settle, however long the fetch takes
    await p.waitForFunction(t => !!(S.lessons[t] && S.lessons[t].scenes), tid, { timeout: 15000 })
      .catch(() => {});
    await p.waitForTimeout(400);

    const start = p.locator('.startblk .sbmain button');
    if (!await start.count()) { bad(tid + ': no start button on the overview'); continue; }
    const label = ((await start.first().textContent()) || '').trim();
    const before = await p.evaluate(() => S.learn.i);
    await start.first().click();
    await p.waitForTimeout(700);
    const after = await p.evaluate(() => S.learn.i);
    if (after === before) { bad(tid + ': "' + label + '" did not move off ' + before); continue; }

    // now click Continue/Next in the footer until the quiz, counting the hops
    let hops = 0, stuck = null;
    for (let k = 0; k < 20; k++) {
      const kind = await p.evaluate(() => { const L = S.lessons[S.learn.topicId];
        return S.learn.i >= 0 && L ? L.scenes[S.learn.i].kind : null; });
      if (kind === 'quiz') break;
      const nx = p.locator('.scnav button.p').filter({ hasText: /Next|Continue|Finish/ });
      if (!await nx.count()) { stuck = 'no footer Next at scene ' + (await p.evaluate(() => S.learn.i) + 1) + ' (' + kind + ')'; break; }
      const i0 = await p.evaluate(() => S.learn.i);
      await nx.first().click(); await p.waitForTimeout(450);
      const i1 = await p.evaluate(() => S.learn.i);
      if (i1 === i0) { stuck = 'Next did not advance from scene ' + (i0 + 1) + ' (' + kind + ')'; break; }
      hops++;
    }
    const end = await p.evaluate(() => { const L = S.lessons[S.learn.topicId];
      return { i: S.learn.i, kind: L.scenes[S.learn.i].kind, n: L.scenes.length,
               seen: ((S.topics[S.learn.topicId] || {}).seen || []).length }; });
    if (stuck) bad(tid + ': ' + stuck);
    console.log('  ' + tid.padEnd(13) + ' "' + label.slice(0, 22).padEnd(22) + '" → ' + hops +
      ' clicks → scene ' + (end.i + 1) + '/' + end.n + ' (' + end.kind + ')  seen=' + end.seen +
      (stuck ? '   <-- STUCK' : ''));
    if (end.seen === 0) bad(tid + ': nothing recorded as seen after clicking through');
  }
  console.log('\nerrors: ' + (errs.join(' | ') || 'none'));
  console.log(fails ? 'FAILURES: ' + fails : 'every authored lesson starts and advances by clicking');
  await b.close(); process.exit(fails || errs.length ? 1 : 0);
})();
