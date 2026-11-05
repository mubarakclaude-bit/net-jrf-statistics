// End-to-end walk of the pilot topic: tree -> every scene -> mastery test -> verified record.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/ERR_TUNNEL|fonts\.g/.test(m.text())) errs.push('CONSOLE: ' + m.text()); });
  await page.goto('file:///tmp/claude-0/harness.html');
  await page.waitForTimeout(900);
  // the front door now stands in front of the app
  if (await page.locator('[data-login="me"]').count()) { await page.click('[data-login="me"]'); await page.waitForTimeout(700); }
  const say = s => console.log(s);

  say('boot: lessons indexed=' + await page.evaluate(() => Object.keys((S.lessonIdx && S.lessonIdx.topics) || {}).length));

  // ---- learn tab + tree
  await page.evaluate(()=>{if(S.learn&&S.learn.topicId){S.learn.quiz=null;gotoScene(-99)}}).catch(()=>{}); await page.click('[data-tab="learn"]'); await page.waitForTimeout(350);
  say('workspace panes=' + await page.locator('.wsnav, .wscanvas, .wsaide').count() +
      '  modes=' + await page.locator('[data-mode]').count());
  for (const m of ['syllabus', 'personal', 'pyq']) {
    await page.click('[data-mode="' + m + '"]'); await page.waitForTimeout(200);
    const first = await page.locator('.navmh .nm').first().textContent();
    const warn = /falls back|No personal order/.test(await page.innerHTML('.wsnav'));
    say('mode ' + m.padEnd(9) + ' first module="' + first + '"  caveat shown=' + warn);
  }
  await page.click('.navmh[data-mod="inference"]'); await page.waitForTimeout(250);
  say('inference topics in tree=' + await page.locator('[data-topic]').count() +
      '  with lesson=' + await page.locator('.navt .chip.ac').count());

  // ---- open the topic -> overview
  await page.click('[data-topic="inference-t4"]'); await page.waitForTimeout(600);
  const ov = await page.innerHTML('.wscanvas');
  say('overview: objectives=' + await page.locator('.obj li').count() +
      ' prereq=' + (ov.match(/Before you start/) ? 'yes' : 'no') +
      ' sceneRows=' + await page.locator('.scrow').count() +
      ' refs=' + await page.locator('.refrow').count() +
      ' twoProgressBars=' + (/Progress A/.test(ov) && /Progress B/.test(ov)));

  // ---- walk every scene
  await page.click('.scrow'); await page.waitForTimeout(350);
  const total = await page.evaluate(() => S.lessons['inference-t4'].scenes.length);
  for (let i = 0; i < total; i++) {
    await page.evaluate(k => gotoScene(k), i);
    await page.waitForTimeout(260);
    const info = await page.evaluate(() => {
      const sc = S.lessons['inference-t4'].scenes[S.learn.i];
      const c = document.querySelector('.wscanvas');
      return { kind: sc.kind, title: sc.title, len: c.innerHTML.length,
               viz: !!document.querySelector('.viz'), ctl: document.querySelectorAll('[data-vz]').length,
               empty: c.innerText.trim().length < 80 };
    });
    say('  scene ' + String(i + 1).padStart(2) + ' ' + info.kind.padEnd(11) +
        ' html=' + String(info.len).padStart(5) + (info.viz ? ' viz(' + info.ctl + ' sliders)' : '') +
        (info.empty ? '  <-- LOOKS EMPTY' : ''));
  }
  say('scenes marked read=' + await page.evaluate(() => (S.topics['inference-t4'].seen || []).length) + '/' + total);

  // ---- visualisation maths
  await page.evaluate(() => gotoScene(2)); await page.waitForTimeout(300);
  const vz = await page.evaluate(() => {
    const sc = S.lessons['inference-t4'].scenes[2], st = vizState(sc);
    st.n = 2; st.S = 12; st.lam = 2 / 12;
    const o = VIZ['exp-likelihood'].draw(st);
    const at = {}; o.read.forEach(r => at[r[0]] = r[1]);
    return at;
  });
  say('exp-likelihood at n=2 Σx=12: λ̂=' + vz['λ̂ = n/Σxᵢ'] + ' (expect 0.1667), at-peak=' + vz['likelihood vs peak']);
  const samp = await page.evaluate(() => {
    const o = (n) => { const st = { n: n, lam: 0.5 }; const r = VIZ['mle-sampling'].draw(st); const a = {}; r.read.forEach(x => a[x[0]] = x[1]); return a; };
    return { n2: o(2), n20: o(20) };
  });
  say('mle-sampling n=2: E=' + samp.n2['E[λ̂] = nλ/(n−1)'] + ' bias%=' + samp.n2['bias as % of λ'] + ' (expect 1.0000, 100.0%)');
  say('mle-sampling n=20: E=' + samp.n20['E[λ̂] = nλ/(n−1)'] + ' bias%=' + samp.n20['bias as % of λ'] + ' (expect 0.5263, 5.3%)');
  const uni = await page.evaluate(() => { const st = { n: 5, m: 4.2, th: 3.0 }; const r = VIZ['unif-likelihood'].draw(st);
    const a = {}; r.read.forEach(x => a[x[0]] = x[1]); return { below: a['likelihood vs peak'], note: r.note }; });
  say('unif-likelihood at θ=3.0 < x(n)=4.2: likelihood=' + uni.below + ' (expect 0.0%)');
  // slider actually redraws
  await page.evaluate(() => gotoScene(8)); await page.waitForTimeout(300);
  const before = await page.locator('.vr b').first().textContent();
  await page.locator('[data-vz="n"]').fill('30'); await page.locator('[data-vz="n"]').dispatchEvent('input'); await page.waitForTimeout(250);
  const after = await page.evaluate(() => Array.from(document.querySelectorAll('.vr b')).map(b => b.textContent));
  say('slider n->30 redraws: E[λ̂]=' + after[1] + ' bias%=' + after[3] + ' (expect 0.5172, 3.4%)');

  // ---- completion blanks
  await page.evaluate(() => gotoScene(6)); await page.waitForTimeout(300);
  say('completion: blanks=' + await page.locator('[data-bchk]').count());
  await page.locator('.bi').first().fill('nonsense');
  await page.locator('[data-bchk]').first().click(); await page.waitForTimeout(250);
  say('  wrong answer -> rejected=' + /Not a match/.test(await page.innerHTML('.wscanvas')));
  await page.locator('[data-bhint]').first().click(); await page.waitForTimeout(250);
  say('  hint shown=' + /log of a product/.test(await page.innerHTML('.wscanvas')) +
      '  assistance recorded=' + await page.evaluate(() => S.learn.hints['s6'] || 0));
  await page.locator('.bi').first().fill('k log p + (n-k) log(1-p)');
  await page.locator('[data-bchk]').first().click(); await page.waitForTimeout(300);
  say('  correct answer accepted=' + await page.evaluate(() => !!(S.learn.blanks.s6 && S.learn.blanks.s6['1'] && S.learn.blanks.s6['1'].ok)));

  // ---- guided hint ladder
  await page.evaluate(() => gotoScene(10)); await page.waitForTimeout(300);
  say('guided: solution hidden at start=' + !(await page.locator('[data-sol]').count() === 0));
  for (let k = 0; k < 3; k++) { const b = page.locator('[data-hint]'); if (await b.count()) { await b.click(); await page.waitForTimeout(180); } }
  say('  hints opened=' + await page.locator('.hint').count() + '  recorded=' + await page.evaluate(() => S.learn.hints['s10']));
  await page.locator('[data-sol]').click(); await page.waitForTimeout(300);
  say('  solution steps=' + await page.locator('.wstep').count() + '  terminal check=' + /Terminal check/.test(await page.innerHTML('.wscanvas')));

  // ---- trapcheck gating
  await page.evaluate(() => gotoScene(11)); await page.waitForTimeout(300);
  say('trapcheck: reasons hidden before all verdicts=' + !/TRUE<\/b> —/.test(await page.innerHTML('.wscanvas')));
  const n = await page.locator('[data-tv$="|T"]').count();
  const scid = await page.evaluate(() => S.lessons['inference-t4'].scenes[11].id);
  for (let k = 0; k < n; k++) { await page.click('[data-tv="' + scid + '|' + k + '|T"]'); await page.waitForTimeout(120); }
  say('  after ' + n + ' verdicts: reasons shown=' + /you had it|you said/.test(await page.innerHTML('.wscanvas')) +
      '  score line=' + /Score on this set/.test(await page.innerHTML('.wscanvas')));

  // ---- mastery test
  await page.evaluate(() => gotoScene(14)); await page.waitForTimeout(300);
  say('quiz intro: policy shown=' + /80% overall/.test(await page.innerHTML('.wscanvas')));
  await page.click('[data-startquiz]'); await page.waitForTimeout(700);
  const qn = await page.evaluate(() => S.learn.quiz ? S.learn.quiz.list.length : 0);
  say('mastery test built: ' + qn + ' questions, all MCQ=' + await page.evaluate(() => S.learn.quiz.list.every(q => (q.options || []).length === 4)));
  // answer every question correctly, with varied confidence
  await page.evaluate(() => {
    const Q = S.learn.quiz;
    Q.list.forEach((q, k) => { Q.ans[k] = q.answer; Q.conf[k] = (k % 3) + 1; });
    render();
  });
  await page.waitForTimeout(250);
  await page.click('#quizSubmit'); await page.waitForTimeout(600);
  const res = await page.evaluate(() => { const Q = S.learn.quiz; return { pct: Q.pct, pass: Q.pass, byFmt: Q.byFmt, rec: S.mastery['inference-t4'] }; });
  say('all-correct run: ' + res.pct + '% pass=' + res.pass + ' byFmt=' + JSON.stringify(res.byFmt));
  say('  mastery record: state=' + res.rec.state + ' best=' + res.rec.best + ' retestDue in days=' +
      (res.rec.retestDue ? Math.round((res.rec.retestDue - Date.now()) / 86400000) : '—'));
  say('  result page: policy rows=' + await page.locator('.wscanvas .trow').count() +
      ' confidence panel=' + /Confidence against correctness/.test(await page.innerHTML('.wscanvas')) +
      ' review items=' + await page.locator('.wscanvas details.sp').count());

  // ---- a failing run drives remediation + format floors
  await page.evaluate(() => { const les = S.lessons['inference-t4']; startQuiz(les); });
  await page.waitForTimeout(600);
  await page.evaluate(() => {
    const Q = S.learn.quiz;
    Q.list.forEach((q, k) => {
      const wrong = 'ABCD'.split('').filter(L => L !== q.answer)[0];
      // get the 3 singles right, miss most numericals -> should fail the numeric floor
      Q.ans[k] = (q.format === 'numeric') ? wrong : q.answer;
      Q.conf[k] = (q.format === 'numeric') ? 3 : 2;
    });
    render();
  });
  await page.waitForTimeout(250);
  await page.click('#quizSubmit'); await page.waitForTimeout(600);
  const r2 = await page.evaluate(() => { const Q = S.learn.quiz; return { pct: Q.pct, pass: Q.pass, fails: Q.fails, byFmt: Q.byFmt, rec: S.mastery['inference-t4'] }; });
  say('numeric-fail run: ' + r2.pct + '% pass=' + r2.pass + ' floorsFailed=' + JSON.stringify(r2.fails) + ' byFmt=' + JSON.stringify(r2.byFmt));
  say('  best score retained=' + r2.rec.best + ' (state now ' + r2.rec.state + ', attempts ' + r2.rec.attempts + ')');
  say('  overconfidence flagged=' + /answered with certainty and wrong/.test(await page.innerHTML('.wscanvas')));
  say('  remediation scenes offered=' + await page.locator('.wscanvas .scrow').count());

  // ---- mastery items stay out of bank and mocks
  await page.evaluate(()=>{if(S.learn&&S.learn.topicId){S.learn.quiz=null;gotoScene(-99)}}).catch(()=>{}); await page.click('[data-tab="bank"]'); await page.waitForTimeout(900);
  const bankIds = await page.evaluate(() => allQ().map(q => q.id));
  say('bank size=' + bankIds.length + '  mastery items leaked into bank=' + bankIds.filter(i => /-m-\d/.test(i)).length + ' (expect 0)');

  // ---- admin prompt packs
  await page.evaluate(()=>{if(S.learn&&S.learn.topicId){S.learn.quiz=null;gotoScene(-99)}}).catch(()=>{}); await page.click('[data-tab="admin"]'); await page.waitForTimeout(400);
  for (const st of ['blueprint', 'lesson', 'practice', 'mastery', 'validation']) {
    await page.selectOption('#fStage', st); await page.waitForTimeout(250);
    const t = await page.inputValue('#pBox');
    say('stage ' + st.padEnd(11) + ' ' + String(t.length).padStart(5) + ' chars, names artifact=' + /artifact\/TEST/.test(t) + ', names a db path=' + /(lessons\/|qsets\/)/.test(t));
  }
  await page.selectOption('#fStage', 'lesson'); await page.waitForTimeout(200);
  // the module picker opens on whichever module is weakest, so say which one we mean
  await page.selectOption('#fMod2', 'inference'); await page.waitForTimeout(250);
  await page.selectOption('#fTop', 'inference-t4'); await page.waitForTimeout(250);
  say('existing-lesson warning on the lesson stage=' + /already exists for this topic/.test(await page.innerHTML('#v-admin')));
  // imports
  await page.fill('#persBox', '{"cycle":"2026-06","entries":[{"moduleId":"timeseries","topicId":"timeseries-t1","priority":1,"reason":"6/10 here already — protect it"}]}');
  await page.click('#persSave'); await page.waitForTimeout(500);
  say('personal import: stored=' + await page.evaluate(() => !!(S.personal && S.personal.entries)) +
      ' wrote=' + await page.evaluate(() => window.__writes.filter(w => w[1] === 'meta/personal').length));
  await page.fill('#sylBox', '{"cycle":"2026","order":{"maths":1,"probability":2,"inference":3,"timeseries":9}}');
  await page.click('#sylSave'); await page.waitForTimeout(500);
  await page.evaluate(()=>{if(S.learn&&S.learn.topicId){S.learn.quiz=null;gotoScene(-99)}}).catch(()=>{}); await page.click('[data-tab="learn"]'); await page.waitForTimeout(300);
  // the rail shows the open lesson's contents; leaving the lesson brings the topic tree back
  if (await page.locator('[data-alltopics]').count()) { await page.click('[data-alltopics]'); await page.waitForTimeout(350); }
  // the switcher now sits on the landing pane as well as the rail, so three or six
  say('left the lesson -> mode switcher back in the rail: ' + (await page.locator('.wsnav [data-mode]').count() === 3));
  await page.click('[data-mode="syllabus"]'); await page.waitForTimeout(300);
  say('syllabus order applied: first module="' + await page.locator('.navmh .nm').first().textContent() + '" (expect Mathematics)');
  await page.click('[data-mode="personal"]'); await page.waitForTimeout(300);
  say('personal order applied: first module="' + await page.locator('.navmh .nm').first().textContent() + '" (expect Time series)');

  // ---- responsive
  for (const w of [1400, 980, 390]) {
    await page.setViewportSize({ width: w, height: 900 });
    await page.evaluate(()=>{if(S.learn&&S.learn.topicId){S.learn.quiz=null;gotoScene(-99)}}).catch(()=>{}); await page.click('[data-tab="learn"]'); await page.waitForTimeout(350);
    await page.evaluate(() => { S.navOpen = w => w; });
    const r = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    say(w + 'px learn: scrollWidth=' + r.sw + ' client=' + r.cw + (r.sw > r.cw + 1 ? '  <-- OVERFLOW' : '  ok'));
    if (w === 390) {
      await page.evaluate(() => { S.navOpen = false; openTopic('inference-t4'); });
      await page.waitForTimeout(500);
      await page.evaluate(() => gotoScene(8)); await page.waitForTimeout(350);
      const r2 = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
      say('390px scene with viz: scrollWidth=' + r2.sw + ' client=' + r2.cw + (r2.sw > r2.cw + 1 ? '  <-- OVERFLOW' : '  ok'));
    }
  }
  say('--- errors: ' + (errs.length ? '\n' + errs.join('\n') : 'none'));
  await browser.close();
})().catch(e => { console.error('HARNESS FAILED', e); process.exit(1); });
