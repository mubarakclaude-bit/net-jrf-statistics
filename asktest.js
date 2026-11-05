// Ask Claude: the chip appears on a selection, the panel opens from every surface,
// the exchange is answered, recorded and shown in Admin — and the mastery-test lock
// genuinely reaches the prompt.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  p.on('console', m => { if (m.type()==='error' && !/ERR_TUNNEL|fonts\.g/.test(m.text())) errs.push('CONSOLE ' + m.text()); });
  let fails = 0; const bad = m => { fails++; console.log('   FAIL ' + m); };

  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1500);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(800); }
  // capture every prompt the page sends to Claude
  await p.evaluate(() => {
    window.__prompts = [];
    S.sampleFn = async (prompt, opts) => {
      window.__prompts.push({ prompt, tier: opts && opts.modelTier });
      if (opts && opts.onText) opts.onText({ text: 'A sufficient statistic is one whose' });
      return { text: 'A sufficient statistic is one whose conditional distribution leaves no parameter.' };
    };
  });

  await p.click('[data-tab="learn"]'); await p.waitForTimeout(400);
  await p.evaluate(() => { S.navOpen = true; S.open.inference = true; render(); }); await p.waitForTimeout(300);
  await p.click('[data-topic="inference-t1"]');
  await p.waitForFunction(() => !!(S.lessons['inference-t1'] && S.lessons['inference-t1'].scenes), null, { timeout: 15000 });
  await p.waitForTimeout(500);

  // 1. the Ask button on the overview
  const ov = await p.locator('[data-askopen]').count();
  if (!ov) bad('no Ask Claude button on the lesson overview');
  await p.locator('[data-askopen]').first().click(); await p.waitForTimeout(400);
  if (!await p.locator('.askmodal').count()) bad('the panel did not open from the overview button');
  console.log('overview: panel opens, intents = ' + await p.locator('[data-askintent]').count());

  // 2. an intent + an answer, recorded
  await p.locator('[data-askintent="basics"]').click(); await p.waitForTimeout(200);
  await p.locator('[data-asksend]').first().click(); await p.waitForTimeout(600);
  const out = (await p.locator('.askout').textContent().catch(() => '')) || '';
  console.log('answer rendered: ' + (out.length > 20 ? 'yes (' + out.length + ' chars)' : 'NO'));
  if (out.length < 20) bad('no answer rendered');
  const rec = await p.evaluate(() => (S.asks || []).length);
  console.log('exchanges recorded: ' + rec);
  if (!rec) bad('the exchange was not recorded');
  const tier = await p.evaluate(() => window.__prompts[0].tier);
  console.log('"drill to basics" used tier: ' + tier);

  // 3. the unhelpful flag, which is what Admin ranks by
  await p.locator('[data-askhelp="0"]').click(); await p.waitForTimeout(300);
  const flagged = await p.evaluate(() => (S.asks || []).filter(a => a.helpful === false).length);
  console.log('flagged as unhelpful: ' + flagged);
  if (!flagged) bad('the unhelpful flag was not stored');
  await p.locator('[data-askclose="1"]').click(); await p.waitForTimeout(300);

  // 4. the selection chip
  await p.evaluate(() => { gotoScene(3); });
  await p.waitForTimeout(400);
  await p.evaluate(() => {
    // a sentence-sized element, the way a learner actually selects
    const el = Array.from(document.querySelectorAll('.wscanvas p, .wscanvas .ws1, .wscanvas b'))
      .filter(x => { const t = (x.textContent || '').trim(); return t.length > 20 && t.length < 400; })[0]
      || document.querySelector('.wscanvas p');
    const r = document.createRange(); r.selectNodeContents(el);
    const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    document.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
  });
  await p.waitForTimeout(350);
  const chip = await p.locator('.askchip').count();
  console.log('selection chip appears: ' + (chip ? 'yes' : 'NO'));
  if (!chip) bad('no chip after selecting text');
  if (chip) {
    await p.locator('.askchip').click(); await p.waitForTimeout(400);
    const quoted = await p.locator('.askquote').count();
    console.log('selection carried into the panel: ' + (quoted ? 'yes' : 'NO'));
    if (!quoted) bad('the selection was not carried into the panel');
    await p.locator('[data-askclose="1"]').click(); await p.waitForTimeout(250);
  }

  // 5. THE IMPORTANT ONE: during an unsubmitted mastery test the prompt must forbid the answer
  await p.evaluate(() => gotoScene(S.lessons['inference-t1'].scenes.findIndex(s => s.kind === 'quiz')));
  await p.waitForTimeout(300);
  await p.click('[data-startquiz]'); await p.waitForTimeout(900);
  const askInQuiz = await p.locator('[data-askopen]').count();
  if (!askInQuiz) bad('no Ask button during the mastery test');
  await p.locator('[data-askopen]').first().click(); await p.waitForTimeout(400);
  const warned = await p.locator('.askmodal').textContent();
  console.log('lock warning shown to the learner: ' + (/will not give the answer/.test(warned) ? 'yes' : 'NO'));
  if (!/will not give the answer/.test(warned)) bad('no lock warning during an open test');
  await p.locator('[data-asksend]').first().click(); await p.waitForTimeout(600);
  const quizPrompt = await p.evaluate(() => window.__prompts[window.__prompts.length - 1].prompt);
  const hasLock = /IMPORTANT RESTRICTION/.test(quizPrompt) && /Do NOT give the answer/.test(quizPrompt);
  console.log('prompt carries the restriction: ' + (hasLock ? 'yes' : 'NO'));
  if (!hasLock) bad('the mastery-test restriction did not reach the prompt');
  const carriesQ = /Question on screen:/.test(quizPrompt);
  console.log('prompt carries the question context: ' + (carriesQ ? 'yes' : 'NO'));
  await p.locator('[data-askclose="1"]').click(); await p.waitForTimeout(250);

  // 6. Admin shows them, ranks them, and can export a brief
  await p.evaluate(() => { S.learn.quiz = null; gotoScene(-99); });
  await p.click('[data-tab="admin"]'); await p.waitForTimeout(700);
  const rows = await p.locator('.askrow').count();
  const chips = await p.locator('.asktop .chip').count();
  console.log('admin: ' + rows + ' exchanges listed, ' + chips + ' topic chips');
  if (!rows) bad('admin does not list the exchanges');
  const brief = await p.evaluate(() => askBrief());
  console.log('brief: ' + brief.split('\n').length + ' lines, names the flagged topic: ' +
    /answer marked unhelpful/.test(brief));
  if (!/answer marked unhelpful/.test(brief)) bad('the brief does not surface the flagged answer');

  console.log('\nerrors: ' + (errs.join(' | ') || 'none'));
  console.log(fails ? 'FAILURES: ' + fails : 'Ask Claude works on every surface, and the test lock holds');
  await b.close(); process.exit(fails || errs.length ? 1 : 0);
})();
