// Every lesson must open with a foundation drill that actually works:
// items render, both verdicts record, "shaky" opens a rebuild, and the
// closing summary only appears once every item is answered.
const { chromium } = require('playwright');
const TOPICS = ['inference-t1','inference-t2','inference-t3','inference-t4','inference-t5','inference-t6','inference-t7','inference-t8','inference-t9','official-t1','official-t2','official-t3','official-t4','official-t5'];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  p.on('console', m => { if (m.type()==='error' && !/ERR_TUNNEL|fonts\.g/.test(m.text())) errs.push('CONSOLE: '+m.text()); });
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1300);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }
  await p.click('[data-tab="learn"]'); await p.waitForTimeout(300);
  let fails = 0;
  const bad = m => { fails++; console.log('   FAIL ' + m); };

  for (const tid of TOPICS) {
    await p.evaluate(t => { S.open.inference = true; openTopic(t) }, tid); await p.waitForTimeout(900);
    const first = await p.evaluate(t => { const L = S.lessons[t]; return L ? { k: L.scenes[0].kind, n: (L.scenes[0].items||[]).length, est: L.estMin, v: L.version } : null; }, tid);
    if (!first) { bad(tid + ': lesson did not load'); continue; }
    console.log(tid + '  scene1=' + first.k + ' items=' + first.n + ' est=' + first.est + 'min v' + first.v);
    if (first.k !== 'foundation') { bad(tid + ': first scene is ' + first.k); continue; }
    if (first.n !== 4) bad(tid + ': ' + first.n + ' items, expected 4');

    await p.evaluate(() => gotoScene(0)); await p.waitForTimeout(300);
    const cards = await p.locator('.found').count();
    const txt0 = (await p.innerText('.wscanvas')).trim().length;
    if (cards !== first.n) bad(tid + ': ' + cards + ' cards rendered for ' + first.n + ' items');
    if (txt0 < 900) bad(tid + ': foundation scene text only ' + txt0 + ' chars');

    // answer the first solid, the second shaky, leaving two unanswered
    await p.locator('.found').nth(0).locator('[data-found]').first().click(); await p.waitForTimeout(180);
    await p.locator('.found').nth(1).locator('[data-found]').nth(1).click(); await p.waitForTimeout(180);
    const mid = await p.evaluate(() => ({
      recalls: document.querySelectorAll('.fa').length,
      refresh: document.querySelectorAll('.frefresh').length,
      summary: document.querySelectorAll('.wscanvas .expl.ok, .wscanvas .expl.och').length,
      note: (document.querySelector('.wscanvas .note') || {}).textContent || '' }));
    if (mid.recalls !== 2) bad(tid + ': ' + mid.recalls + ' recall answers shown after 2 verdicts');
    if (mid.refresh !== 1) bad(tid + ': shaky did not open a rebuild (' + mid.refresh + ')');
    if (!/2 of 4/.test(mid.note)) bad(tid + ': progress note reads "' + mid.note.slice(0, 50) + '"');

    // finish the rest; the closing summary must then appear and name the shaky count
    for (let k = 2; k < first.n; k++) { await p.locator('.found').nth(k).locator('[data-found]').first().click(); await p.waitForTimeout(140); }
    const end = await p.evaluate(() => {
      const s = document.querySelector('.wscanvas .expl.och, .wscanvas .expl.ok');
      return { has: !!s, head: s ? s.querySelector('h4').textContent : '',
               recalls: document.querySelectorAll('.fa').length,
               refresh: document.querySelectorAll('.frefresh').length }; });
    if (!end.has) bad(tid + ': no closing summary after all items answered');
    if (!/1 of 4/.test(end.head)) bad(tid + ': summary head reads "' + end.head + '"');
    if (end.recalls !== first.n) bad(tid + ': ' + end.recalls + ' recalls at the end');
    if (end.refresh !== 1) bad(tid + ': ' + end.refresh + ' rebuilds open at the end');
    console.log('   ' + end.head + '  ·  recalls=' + end.recalls + ' rebuild=' + end.refresh + ' text=' + txt0);

    // the drill must not be a dead end: the stepper still reaches scene 2
    await p.evaluate(() => gotoScene(1)); await p.waitForTimeout(260);
    const k2 = await p.evaluate(t => S.lessons[t].scenes[S.learn.i].kind, tid);
    if (k2 === 'foundation') bad(tid + ': could not advance past the drill');
  }
  console.log('\nerrors: ' + (errs.length ? errs.join(' | ') : 'none'));
  console.log(fails ? 'FAILURES: ' + fails : 'all foundation drills pass');
  await b.close();
  process.exit(fails || errs.length ? 1 : 0);
})();
