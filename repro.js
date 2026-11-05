const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const seen = [];
  p.on('pageerror', e => console.log('PAGEERROR: ' + e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1400);
  // the front door now stands in front of the app
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }
  await p.click('[data-tab="learn"]'); await p.waitForTimeout(300);
  console.log('welcome pane says: ' + (await p.innerText('.wscanvas')).split('\n').slice(0,6).join(' / '));
  await p.evaluate(() => { S.open.inference = true; render(); }); await p.waitForTimeout(200);
  // click exactly as a person would, then sample the canvas every 120ms
  await p.click('[data-topic="inference-t4"]');
  for (let i = 0; i < 16; i++) {
    const t = (await p.innerText('.wscanvas')).trim().slice(0, 70).replace(/\s+/g, ' ');
    seen.push((i*120) + 'ms: ' + t);
    await p.waitForTimeout(120);
  }
  console.log(seen.join('\n'));
  console.log('final lesson state: ' + await p.evaluate(() => {
    const v = S.lessons['inference-t4'];
    return v === undefined ? 'undefined' : v === null ? 'null (in flight)' : v === false ? 'false (absent)' : 'loaded';
  }));
  await b.close();
})();
