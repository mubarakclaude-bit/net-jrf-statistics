const { chromium } = require('playwright');
const txt = async p => (await p.innerText('.wscanvas')).trim().replace(/\n+/g,' / ');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(()=>chromium.launch());
  const p = await b.newPage({ viewport:{width:393,height:852}, isMobile:true, hasTouch:true });
  const errs=[]; p.on('pageerror', e=>errs.push(e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1400);
  // the front door now stands in front of the app
  if (await p.locator('[data-login="me"]').count()) { await p.click('[data-login="me"]'); await p.waitForTimeout(700); }
  await p.click('[data-tab="learn"]'); await p.waitForTimeout(500);

  console.log('A. Learn opens, drawer closed=' + (await p.evaluate(()=>!S.navOpen)));
  console.log('   canvas: ' + (await txt(p)).slice(0,64));

  // route 1 — the ready-to-learn list in the canvas
  await p.evaluate(() => { const b=document.querySelectorAll('.wscanvas [data-topic]')[0]; b.click(); });
  await p.waitForTimeout(1000);
  console.log('B. tapped a ready-to-learn button → ' + (await txt(p)).slice(0,72));
  let start = await p.evaluate(() => Array.from(document.querySelectorAll('.wscanvas button'))
    .filter(x=>/Start the lesson|Resume at scene/.test(x.textContent)).length);
  console.log('   start button present: ' + (start>0));

  // route 2 — via the drawer, exactly what the screenshot showed
  // inside a lesson the rail carries that lesson's sections, so step back to the topic tree first
  await p.evaluate(() => { S.navOpen=true; S.open.inference=true; resetLearn(null); render(); }); await p.waitForTimeout(500);
  console.log('C. drawer reopened, close button in it: ' +
    await p.evaluate(()=>!!document.querySelector('.navtop [data-nav-toggle]')));
  await p.evaluate(() => { document.querySelector('.navt[data-topic="inference-t1"]').click(); });
  await p.waitForTimeout(1000);
  console.log('   tapped the topic inside the drawer → drawer closed=' + (await p.evaluate(()=>!S.navOpen)));
  console.log('   canvas now: ' + (await txt(p)).slice(0,72));

  // can we actually reach and press start
  const pressed = await p.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('.wscanvas button'))
      .find(x=>/Start the lesson|Resume at scene/.test(x.textContent));
    if (!btn) return 'NO BUTTON';
    btn.click(); return btn.textContent.trim();
  });
  await p.waitForTimeout(700);
  console.log('D. pressed "' + pressed + '" → scene ' + await p.evaluate(()=>S.learn.i+1) +
              ': ' + (await txt(p)).slice(0,60));

  // walk a few scenes incl. a visualisation, checking nothing overflows
  for (const i of [1,5,7,8]) {
    await p.evaluate(k=>gotoScene(k), i); await p.waitForTimeout(450);
    const r = await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
      viz:!!document.querySelector('.viz'), sliders:document.querySelectorAll('[data-vz]').length}));
    console.log('E. scene '+(i+1)+(r.viz?' (viz, '+r.sliders+' sliders)':'')+': '+(r.sw>r.cw+1?'OVERFLOW '+r.sw:'fits'));
  }
  await p.evaluate(()=>gotoScene(1)); await p.waitForTimeout(500);
  await p.screenshot({ path:'/tmp/claude-0/phone-scene.png', fullPage:false });
  await p.evaluate(()=>gotoScene(-99)); await p.waitForTimeout(500);
  await p.screenshot({ path:'/tmp/claude-0/phone-overview.png', fullPage:false });
  console.log(errs.length?'ERRORS: '+errs.join(' | '):'no runtime errors');
  await b.close();
})();
