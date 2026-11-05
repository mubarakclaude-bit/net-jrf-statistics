// No route through the workspace may leave the learner on a page with nothing to act on.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1440, height: 980 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1400);
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(800); }
  await p.click('[data-tab="learn"]'); await p.waitForTimeout(400);

  const probe = async tag => {
    const r = await p.evaluate(() => {
      const c = document.querySelector('.wscanvas');
      const cb = c.getBoundingClientRect();   // content with no width is still a blank screen
      const acts = [...c.querySelectorAll('button,a')].filter(x => !x.disabled && x.offsetParent !== null);
      const topicWays = acts.filter(x => x.dataset.topic || x.dataset.mod || x.dataset.sc !== undefined || x.dataset.alltopics);
      return { nav: S.navOpen, aide: S.aideOpen, topic: S.learn.topicId, i: S.learn.i,
               actions: acts.length, ways: topicWays.length,
               text: (c.innerText || '').trim().length, w: Math.round(cb.width),
               edge: !!document.querySelector('.edge') };
    });
    const dead = r.ways === 0 || r.w < 300;
    console.log('  ' + tag.padEnd(36) + 'nav=' + (r.nav ? 'open' : 'shut') + ' chars=' + String(r.text).padStart(5) +
                ' actions=' + String(r.actions).padStart(3) + ' ways-in=' + String(r.ways).padStart(3) +
                ' edgeTab=' + (r.edge ? 'yes' : 'no ') + (dead ? (r.w < 300 ? '   <-- CANVAS COLLAPSED TO ' + r.w + 'px' : '   <-- DEAD END') : ''));
    return dead;
  };
  let dead = 0;
  console.log('--- landing page with the panels closed ---');
  await p.evaluate(() => { S.navOpen = false; S.aideOpen = false; resetLearn(null); render() }); await p.waitForTimeout(400);
  dead += await probe('landing, both panels shut') ? 1 : 0;
  await p.evaluate(() => { S.open.inference = true; render() }); await p.waitForTimeout(300);
  dead += await probe('landing, a module expanded') ? 1 : 0;

  console.log('--- the sequence that used to go blank ---');
  await p.evaluate(() => { S.navOpen = true; render() }); await p.waitForTimeout(300);
  await p.click('[data-topic="inference-t1"]'); await p.waitForTimeout(1100);
  dead += await probe('t1 overview') ? 1 : 0;
  await p.evaluate(() => gotoScene(0)); await p.waitForTimeout(500);
  await p.evaluate(() => { const x = document.querySelector('.wsnav [data-nav-toggle]'); if (x) x.click() }); await p.waitForTimeout(400);
  dead += await probe('in a scene, contents closed') ? 1 : 0;
  await p.evaluate(() => { const x = document.querySelector('.scbar [data-sc="-99"]'); if (x) x.click() }); await p.waitForTimeout(500);
  dead += await probe('left the lesson') ? 1 : 0;
  await p.evaluate(() => { const x = document.querySelector('[data-alltopics]'); if (x) x.click() }); await p.waitForTimeout(500);
  dead += await probe('all topics (was the blank page)') ? 1 : 0;

  console.log('--- the landing page carries the module map ---');
  const m = await p.evaluate(() => {
    resetLearn(null); S.navOpen = false; render();
    const c = document.querySelector('.wscanvas');
    return { modules: c.querySelectorAll('.modcard').length,
             stars: (c.innerText.match(/★/g) || []).length,
             paper: /Paper 2 · 34 marks/.test(c.innerText),
             nextUp: !!c.querySelector('.nextup [data-topic]') };
  });
  console.log('  module cards=' + m.modules + ', star ratings on screen=' + m.stars +
              ', module marks shown=' + m.paper + ', suggested-next action=' + m.nextUp);

  console.log('--- start action is the first thing on a lesson ---');
  await p.evaluate(() => openTopic('inference-t1')); await p.waitForTimeout(900);
  const o = await p.evaluate(() => {
    const c = document.querySelector('.wscanvas');
    const start = c.querySelector('.startblk .btn.p'), done = c.querySelector('[data-done]');
    const r1 = start.getBoundingClientRect(), r2 = done.getBoundingClientRect();
    return { start: start.textContent.trim(), startY: Math.round(r1.top), doneY: Math.round(r2.top),
             aboveFold: r1.top < 700 };
  });
  console.log('  "' + o.start + '" at y=' + o.startY + ', mark-done at y=' + o.doneY +
              ' -> start comes first: ' + (o.startY <= o.doneY) + ', above the fold: ' + o.aboveFold);

  console.log('--- panels resize and remember ---');
  const z = await p.evaluate(async () => {
    S.navOpen = true; S.aideOpen = true; render(); await new Promise(r => setTimeout(r, 200));
    const g = document.querySelector('[data-grip="nav"]'); const had = !!g;
    S.navW = 380; savePanels(); render(); await new Promise(r => setTimeout(r, 200));
    const w = document.querySelector('.wsnav').getBoundingClientRect().width;
    let stored = null; try { stored = JSON.parse(localStorage.getItem('njpanels')) } catch (e) {}
    return { grip: had, width: Math.round(w), stored: stored && stored.navW };
  });
  console.log('  grip present=' + z.grip + ', rail width after setting 380 = ' + z.width + 'px, remembered=' + z.stored);
  console.log('--- every panel combination, landing and in a lesson ---');
  for (const [nav, aide] of [[true,true],[false,true],[true,false],[false,false]]) {
    for (const t of [null, 'inference-t1']) {
      await p.evaluate(([n,a,tt]) => { S.navOpen=n; S.aideOpen=a; if(tt)openTopic(tt); else resetLearn(null); render() }, [nav,aide,t]);
      await p.waitForTimeout(t ? 650 : 300);
      dead += await probe('nav ' + (nav?'open':'shut') + ' / aide ' + (aide?'open':'shut') + ' / ' + (t||'landing')) ? 1 : 0;
    }
  }
  console.log(dead ? dead + ' FAILURES' : 'no dead ends and no collapsed canvas on any route');
  console.log(errs.length ? '--- ' + errs.join('\n') : 'no runtime errors');
  await b.close();
})();
