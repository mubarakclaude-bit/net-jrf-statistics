const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  p.on('console', m => { if (m.type()==='error' && !/ERR_TUNNEL|fonts\.g/.test(m.text())) errs.push('CONSOLE: '+m.text()); });
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1300);
  // the front door now stands in front of the app
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }
  console.log('lessons indexed: ' + await p.evaluate(() => Object.keys(S.lessonIdx.topics).join(', ')));
  await p.evaluate(()=>{if(S.learn&&S.learn.topicId){S.learn.quiz=null;gotoScene(-99)}}).catch(()=>{}); await p.click('[data-tab="learn"]'); await p.waitForTimeout(300);
  await p.evaluate(() => { S.open.inference = true; render(); }); await p.waitForTimeout(250);
  console.log('tree shows lesson chips: ' + await p.locator('.navt .chip.ac').count() + ' (expect 2)');
  await p.click('[data-topic="inference-t9"]'); await p.waitForTimeout(900);
  const ov = await p.innerText('.wscanvas');
  console.log('overview: ' + ov.split('\n').filter(x=>x.trim()).slice(1,4).join(' | ').slice(0,110));
  console.log('  objectives=' + await p.locator('.obj li').count() + ' sceneRows=' + await p.locator('.scrow').count() + ' refs=' + await p.locator('.refrow').count());
  const total = await p.evaluate(() => S.lessons['inference-t9'].scenes.length);
  for (let i = 0; i < total; i++) {
    await p.evaluate(k => gotoScene(k), i); await p.waitForTimeout(240);
    const info = await p.evaluate(() => {
      const sc = S.lessons['inference-t9'].scenes[S.learn.i], c = document.querySelector('.wscanvas');
      return { k: sc.kind, len: c.innerHTML.length, txt: c.innerText.trim().length,
               viz: !!document.querySelector('.viz'), sl: document.querySelectorAll('[data-vz]').length,
               blanks: document.querySelectorAll('[data-bchk]').length,
               hints: document.querySelectorAll('[data-hint]').length };
    });
    console.log('  ' + String(i+1).padStart(2) + ' ' + info.k.padEnd(11) + ' text=' + String(info.txt).padStart(5) +
      (info.viz ? ' viz('+info.sl+')' : '') + (info.blanks ? ' blanks('+info.blanks+')' : '') +
      (info.hints ? ' hintable' : '') + (info.txt < 200 ? '  <-- THIN' : ''));
  }
  // every completion blank must accept its own stated answer
  const compScenes = await p.evaluate(() =>
    S.lessons['inference-t9'].scenes.map((s,i)=>({i:i,kind:s.kind})).filter(x=>x.kind==='completion').map(x=>x.i));
  for (const si of compScenes) {
    await p.evaluate(k => gotoScene(k), si); await p.waitForTimeout(350);
    const answers = await p.evaluate(k => S.lessons['inference-t9'].scenes[k].steps
      .filter(s=>s.blank).map(s=>s.blank.answer), si);
    for (const a of answers) {
      const inp = p.locator('.bi').first();
      if (!await inp.count()) break;
      await inp.fill(a);
      await p.locator('[data-bchk]').first().click(); await p.waitForTimeout(280);
    }
    const ok = await p.evaluate(k => { const id = S.lessons['inference-t9'].scenes[k].id;
      const b = S.learn.blanks[id] || {}; return Object.keys(b).filter(x=>b[x].ok).length; }, si);
    console.log('completion scene ' + (si+1) + ': blanks accepting their own answer = ' + ok + ' / ' + answers.length);
  }
  // hint ladders
  for (const i of [8, 10]) {
    await p.evaluate(k => gotoScene(k), i); await p.waitForTimeout(260);
    for (let k = 0; k < 3; k++) { const h = p.locator('[data-hint]'); if (await h.count()) { await h.click(); await p.waitForTimeout(150); } }
    console.log('scene ' + (i+1) + ' hint ladder: ' + await p.locator('.hint').count() + ' rungs, solution hidden=' + (await p.locator('[data-sol]').count() > 0));
  }
  // mastery test
  await p.evaluate(() => gotoScene(S.lessons[S.learn.topicId].scenes.findIndex(x=>x.kind==='quiz'))); await p.waitForTimeout(300);
  await p.click('[data-startquiz]'); await p.waitForTimeout(800);
  console.log('mastery: ' + await p.evaluate(() => S.learn.quiz ? S.learn.quiz.list.length + ' questions, all MCQ=' + S.learn.quiz.list.every(q => (q.options||[]).length === 4) : 'FAILED TO START'));
  await p.evaluate(() => { const Q = S.learn.quiz; Q.list.forEach((q,k) => { Q.ans[k] = q.answer; Q.conf[k] = 2; }); render(); });
  await p.waitForTimeout(200); await p.click('#quizSubmit'); await p.waitForTimeout(600);
  console.log('all-correct: ' + await p.evaluate(() => { const Q = S.learn.quiz;
    return Q.pct + '% pass=' + Q.pass + ' byFmt=' + JSON.stringify(Q.byFmt) + ' state=' + S.mastery['inference-t9'].state; }));
  // mastery items must stay out of the bank
  await p.evaluate(()=>{if(S.learn&&S.learn.topicId){S.learn.quiz=null;gotoScene(-99)}}).catch(()=>{}); await p.click('[data-tab="bank"]'); await p.waitForTimeout(900);
  console.log('mastery leaked into bank: ' + await p.evaluate(() => allQ().filter(q => /inf-t9-m-/.test(q.id)).length) + ' (expect 0)');
  // phone width
  await p.setViewportSize({ width: 390, height: 844 });
  await p.evaluate(()=>{if(S.learn&&S.learn.topicId){S.learn.quiz=null;gotoScene(-99)}}).catch(()=>{}); await p.click('[data-tab="learn"]'); await p.waitForTimeout(300);
  await p.evaluate(() => { S.navOpen = false; openTopic('inference-t9'); }); await p.waitForTimeout(700);
  for (const i of [1, 7]) { await p.evaluate(k => gotoScene(k), i); await p.waitForTimeout(350);
    const r = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    console.log('390px scene ' + (i+1) + ': ' + (r.sw > r.cw + 1 ? 'OVERFLOW ' + r.sw : 'ok')); }
  console.log(errs.length ? 'ERRORS:\n' + errs.join('\n') : 'no runtime errors');
  await b.close();
})();
