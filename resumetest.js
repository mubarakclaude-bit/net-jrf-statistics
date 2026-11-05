// Regression: the lesson overview must always offer a way INTO the teaching content.
// A fully-read lesson used to leave "Resume at scene 13" as the only start button,
// which landed on the mastery test — the lesson looked broken.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1440, height: 980 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1300);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }
  const tids = await p.evaluate(() => Object.keys(S.lessonIdx.topics));
  const states = [
    ['nothing read',     'none'],
    ['part read',        'part'],
    ['read with a gap',  'gap'],
    ['every scene read', 'all'],
    ['marked done',      'done'],
    ['stale scene ids',  'stale'],
  ];
  let bad = 0;
  for (const tid of tids) {
    for (const [label, mode] of states) {
      await p.evaluate(() => { S.topics = {}; resetLearn(null); render() }); await p.waitForTimeout(120);
      await p.evaluate(t => openTopic(t), tid); await p.waitForTimeout(700);
      await p.evaluate(([t, m]) => {
        const l = S.lessons[t], ids = l.scenes.map(x => x.id);
        const st = m === 'none' ? { s: 0, seen: [] }
                 : m === 'part' ? { s: 1, seen: ids.slice(0, 3) }
                 : m === 'gap' ? { s: 1, seen: [ids[0], ids[1], ids[4]] }
                 : m === 'all' ? { s: 2, seen: ids }
                 : m === 'done' ? { s: 2, done: 1, seen: ids }
                 : { s: 2, seen: ids.map((_, i) => 'gone' + i) };
        S.topics[t] = st; resetLearn(t); render();
      }, [tid, mode]); await p.waitForTimeout(300);
      // there must be at least one button that opens a TEACHING scene
      const r = await p.evaluate(t => {
        const les = S.lessons[t], qz = les.scenes.length - 1;
        const btns = [...document.querySelectorAll('.wscanvas .btn')].filter(x => x.dataset.sc !== undefined);
        const teach = btns.filter(x => +x.dataset.sc >= 0 && +x.dataset.sc !== qz);
        return { any: teach.length, labels: teach.map(x => x.textContent.trim()),
                 primary: (btns.filter(x => x.classList.contains('p'))[0] || {}).dataset };
      }, tid);
      if (!r.any) { bad++; console.log('  NO WAY INTO THE LESSON: ' + tid + ' / ' + label); }
    }
  }
  console.log('every lesson × every progress state offers a teaching entry point: ' + (bad === 0 ? 'yes' : bad + ' FAILURES'));
  // and resume must pick the first UNREAD scene, not a count
  const g = await p.evaluate(() => {
    const t = 'inference-t1', l = S.lessons[t], ids = l.scenes.map(x => x.id);
    S.topics[t] = { s: 1, seen: [ids[0], ids[1], ids[4]] }; resetLearn(t); render();
    const b = [...document.querySelectorAll('.wscanvas .btn.p')].filter(x => x.dataset.sc !== undefined)[0];
    return { label: b.textContent.trim(), sc: +b.dataset.sc };
  });
  console.log('read 1, 2 and 5 -> "' + g.label + '" (scene index ' + g.sc + ', expect 2 = the first unread)');
  console.log(errs.length ? '--- ' + errs.join('\n') : 'no runtime errors');
  await b.close();
})();
