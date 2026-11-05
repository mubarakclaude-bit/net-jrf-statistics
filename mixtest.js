// The mastery paper must hold the policy's difficulty mix, and a retake must be
// a different paper. Also checks the completion controls: tick, untick, mark done, reset.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1300);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }

  const tids = await p.evaluate(() => Object.keys(S.lessonIdx.topics));
  console.log('--- difficulty mix held on every topic ---');
  for (const tid of tids) {
    const r = await p.evaluate(async t => {
      S.learn.topicId = t; await loadLesson(t);
      const les = S.lessons[t]; const sc = les.scenes.filter(s => s.kind === 'quiz')[0];
      const pool = (await loadSet(sc.setId)).filter(q => (q.options || []).length);
      const want = les.mastery.diffMix;
      const got = {}; const tally = l => l.reduce((a, q) => { a[q.diff || 'none'] = (a[q.diff || 'none'] || 0) + 1; return a }, {});
      const paper = drawPaper(pool, les.mastery, []);
      return { t, pool: pool.length, poolMix: tally(pool), want, got: tally(paper), n: paper.length };
    }, tid);
    const ok = Object.keys(r.want).every(d => (r.got[d] || 0) === r.want[d]);
    console.log('  ' + r.t.padEnd(14) + ' pool ' + r.pool + ' ' + JSON.stringify(r.poolMix) +
                ' -> paper of ' + r.n + ' ' + JSON.stringify(r.got) + (ok ? '  matches policy' : '  MIX NOT MET, wanted ' + JSON.stringify(r.want)));
  }

  console.log('--- a retake is a different paper ---');
  const rt = await p.evaluate(async () => {
    const t = 'inference-t5'; S.learn.topicId = t; await loadLesson(t);
    const les = S.lessons[t], sc = les.scenes.filter(s => s.kind === 'quiz')[0];
    const pool = (await loadSet(sc.setId)).filter(q => (q.options || []).length);
    S.att = {};
    const a = drawPaper(pool, les.mastery, []);
    // record attempt 1 the way gradeQuiz does: everything answered, half of them wrong
    a.forEach((q, i) => { S.att[q.id] = { n: 1, o: i % 2 === 0 ? 1 : 0, t: Date.now() } });
    const served = a.map(q => q.id);
    const bPaper = drawPaper(pool, les.mastery, served);
    const overlap = bPaper.filter(q => served.indexOf(q.id) >= 0);
    const wrongLast = a.filter((q, i) => i % 2 === 1).map(q => q.id);
    return { n: bPaper.length, overlap: overlap.length,
             fresh: bPaper.filter(q => served.indexOf(q.id) < 0).length,
             missedBack: bPaper.filter(q => wrongLast.indexOf(q.id) >= 0).length,
             missedTotal: wrongLast.length,
             mix: bPaper.reduce((acc, q) => { acc[q.diff] = (acc[q.diff] || 0) + 1; return acc }, {}) };
  });
  console.log('  attempt 2: ' + rt.n + ' questions, ' + rt.fresh + ' never seen, ' + rt.overlap +
              ' repeated — of which ' + rt.missedBack + ' of the ' + rt.missedTotal + ' you got wrong came back');
  console.log('  attempt 2 mix: ' + JSON.stringify(rt.mix));

  console.log('--- completion controls ---');
  await p.evaluate(() => { S.topics = {}; openTopic('inference-t5'); }); await p.waitForTimeout(800);
  await p.evaluate(() => gotoScene(0)); await p.waitForTimeout(350);
  const sid = await p.evaluate(() => S.lessons['inference-t5'].scenes[2].id);
  await p.evaluate(s => document.querySelector('[data-seen="inference-t5|' + s + '"]').click(), sid);
  await p.waitForTimeout(300);
  console.log('  ticked a section by hand: seen = ' + await p.evaluate(() => (S.topics['inference-t5'].seen || []).length));
  await p.evaluate(s => document.querySelector('[data-seen="inference-t5|' + s + '"]').click(), sid);
  await p.waitForTimeout(300);
  console.log('  unticked it again: seen = ' + await p.evaluate(() => (S.topics['inference-t5'].seen || []).length));
  await p.click('[data-done="inference-t5"]'); await p.waitForTimeout(400);
  console.log('  marked the lesson done: done=' + await p.evaluate(() => !!S.topics['inference-t5'].done) +
              ', every section ticked=' + await p.evaluate(() => (S.topics['inference-t5'].seen || []).length === S.lessons['inference-t5'].scenes.length) +
              ', self-marked progress=' + await p.evaluate(() => selfPct('inference-t5')) + '%');
  const inTree = await p.evaluate(async () => { resetLearn(null); S.open.inference = true; render();
    await new Promise(r => setTimeout(r, 250));
    const row = document.querySelector('[data-topic="inference-t5"]');
    return { green: row.className.indexOf('done') >= 0, tick: row.querySelector('.tdot').textContent.trim() }; });
  console.log('  left hierarchy shows it: class has "done"=' + inTree.green + ', marker=' + JSON.stringify(inTree.tick));
  await p.evaluate(() => { S.mastery['inference-t5'] = { state:'mastered', best:90, attempts:1, passedOnce:true };
                           openTopic('inference-t5') }); await p.waitForTimeout(700);
  await p.click('[data-resettopic="inference-t5"]'); await p.waitForTimeout(400);
  console.log('  reset: done=' + await p.evaluate(() => !!S.topics['inference-t5'].done) +
              ', seen=' + await p.evaluate(() => (S.topics['inference-t5'].seen || []).length) +
              ', mastery record kept=' + await p.evaluate(() => !!S.mastery['inference-t5']));

  console.log('--- weightage reaches the UI ---');
  const w = await p.evaluate(() => { resetLearn(null); S.open.inference = true; render();
    const rows = [...document.querySelectorAll('[data-topic^="inference-t"]')].slice(0, 3);
    return rows.map(r => r.innerText.replace(/\n+/g, ' | ').slice(0, 90)); });
  w.forEach(x => console.log('  ' + x));
  console.log(errs.length ? '--- ' + errs.join('\n') : 'no runtime errors');
  await b.close();
})();
