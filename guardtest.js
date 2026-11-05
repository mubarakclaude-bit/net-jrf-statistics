// Regressions for two scoring defects: a blank that accepted a sign-dropped answer,
// and mastery sets whose key was "A" every time (so an all-A guesser was marked mastered).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1300);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }

  // --- 1. sign discipline on completion blanks ---------------------------------
  // For every blank in every lesson whose answer starts with a minus, typing the
  // same expression WITHOUT the minus must be rejected.
  await p.click('[data-tab="learn"]'); await p.waitForTimeout(300);
  const tids = await p.evaluate(() => Object.keys(S.lessonIdx.topics));
  let tried = 0, wrongly = 0;
  for (const tid of tids) {
    await p.evaluate(t => openTopic(t), tid); await p.waitForTimeout(700);
    const idxs = await p.evaluate(t => (S.lessons[t] ? S.lessons[t].scenes : [])
      .map((s, i) => ({ i, k: s.kind })).filter(x => x.k === 'completion').map(x => x.i), tid);
    for (const k of idxs) {
      await p.evaluate(j => gotoScene(j), k); await p.waitForTimeout(220);
      const signed = await p.evaluate(([t, j]) => S.lessons[t].scenes[j].steps
        .map((s, n) => ({ n, a: s.blank && s.blank.answer }))
        .filter(x => x.a && /^[−\-–—]/.test(x.a)), [tid, k]);
      for (const { n, a } of signed) {
        const stripped = a.replace(/^[−\-–—]\s*/, '');
        const accepted = await p.evaluate(([t, j, n, v]) => {
          const sc = S.lessons[t].scenes[j], sel = '[data-bk="' + sc.id + '|' + n + '"]';
          const inp = document.querySelector(sel); if (!inp) return 'no input';
          inp.value = v;
          document.querySelector('[data-bchk="' + sc.id + '|' + n + '"]').click();
          const bag = (S.learn.blanks || {})[sc.id] || {};
          return !!(bag[n] && bag[n].ok);
        }, [tid, k, n, stripped]);
        tried++; if (accepted === true) { wrongly++; console.log('  ACCEPTED sign-dropped ' + tid + ' scene' + (k+1) + ' blank' + n + ': ' + JSON.stringify(stripped) + ' for ' + JSON.stringify(a)); }
        await p.evaluate(() => { S.learn.blanks = {}; render(); }); await p.waitForTimeout(120);
      }
    }
  }
  console.log('sign-dropped blanks tested: ' + tried + ', wrongly accepted: ' + wrongly + ' (expect 0)');

  // --- 2. an all-A guesser must not pass any mastery test ----------------------
  for (const tid of tids) {
    const r = await p.evaluate(async t => {
      S.learn.topicId = t; await loadLesson(t);
      const les = S.lessons[t]; if (!les) return null;
      await startQuiz(les);
      const Q = S.learn.quiz; if (!Q) return null;
      Q.list.forEach((_, k) => { Q.ans[k] = 'A'; Q.conf[k] = 2; });
      gradeQuiz();
      const keys = {}; Q.list.forEach(q => { keys[q.answer] = (keys[q.answer] || 0) + 1; });
      const out = { t, pct: Q.pct, pass: Q.pass, keys, n: Q.list.length };
      S.learn.quiz = null; delete S.mastery[t];
      return out;
    }, tid);
    if (r) console.log('  ' + r.t + ': all-A guess scores ' + r.pct + '% pass=' + r.pass +
      '  key spread ' + JSON.stringify(r.keys) + ' over ' + r.n);
  }
  console.log(errs.length ? '--- errors:\n' + errs.join('\n') : 'no runtime errors');
  await b.close();
})();
