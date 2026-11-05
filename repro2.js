const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  p.on('pageerror', e => console.log('PAGEERROR: ' + e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1400);
  // the front door now stands in front of the app
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }
  await p.click('[data-tab="learn"]'); await p.waitForTimeout(250);
  await p.evaluate(() => { S.open.inference = true; render(); }); await p.waitForTimeout(200);
  await p.click('[data-topic="inference-t4"]');
  const seen = [];
  for (let i = 0; i < 8; i++) { seen.push((i*90)+'ms: '+(await p.innerText('.wscanvas')).trim().slice(0,56).replace(/\s+/g,' ')); await p.waitForTimeout(90); }
  console.log('no-lesson flash gone:\n' + seen.join('\n'));
  // diagnostics
  await p.click('[data-tab="admin"]'); await p.waitForTimeout(400);
  await p.click('#diagRun'); await p.waitForTimeout(2500);
  console.log('\n--- diagnostics table ---');
  console.log(await p.evaluate(() => S.diag.rows.map(r => (r[2]?'OK   ':'FAIL ') + String(r[0]).padEnd(11) + ' ' + String(r[1]).padEnd(34) + ' ' + (r[3]!==undefined?r[3]:'')).join('\n')));
  // now simulate the failure the user may be hitting: index names a lesson that is gone
  await p.evaluate(() => { delete window.__docs['lessons/mle']; S.lessons = {}; });
  await p.click('[data-tab="learn"]'); await p.waitForTimeout(250);
  await p.evaluate(() => openTopic('inference-t4')); await p.waitForTimeout(900);
  console.log('\nmissing-document message: ' + (await p.innerText('.wscanvas')).split('\n').slice(2,4).join(' | ').slice(0,180));
  // and the case where the index itself never loaded
  await p.evaluate(() => { S.lessonIdx = null; S.lessons = {}; openTopic('inference-t4'); }); await p.waitForTimeout(900);
  console.log('no-index message: ' + (await p.innerText('.wscanvas')).split('\n').slice(2,4).join(' | ').slice(0,180));
  await b.close();
})();
