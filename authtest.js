const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome' }).catch(()=>chromium.launch());
  const ctx = await b.newContext({ viewport:{width:1200,height:900} });
  const p = await ctx.newPage();
  const errs=[]; p.on('pageerror', e=>errs.push(e.message));
  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1500);

  console.log('1. front door shown: ' + (await p.locator('.gatecard').count()>0));
  console.log('   owner row: "' + (await p.locator('.plogin.owner .pt b').textContent()).trim() + '"');
  console.log('   test profiles: ' + await p.locator('.plogin:not(.owner)').count() +
              ', tabs hidden: ' + (await p.locator('#nav button').count()===0));

  await p.click('[data-login="demo"]'); await p.waitForTimeout(350);
  await p.fill('#passBox','9999'); await p.click('#passGo'); await p.waitForTimeout(450);
  console.log('2. wrong passcode rejected: ' + /does not match/.test(await p.innerText('.gatecard')) +
              ', still gated: ' + (await p.locator('.gatecard').count()>0));
  await p.fill('#passBox','1234'); await p.click('#passGo'); await p.waitForTimeout(900);
  console.log('3. correct passcode → in: ' + (await p.locator('.gatecard').count()===0) +
              ', chip "' + (await p.textContent('#hdProfile')).trim() + '"');

  await p.click('[data-tab="learn"]'); await p.waitForTimeout(400);
  await p.evaluate(()=>openTopic('inference-t1')); await p.waitForTimeout(900);
  await p.evaluate(()=>gotoScene(3)); await p.waitForTimeout(900);
  const w=[...new Set(await p.evaluate(()=>window.__writes.map(x=>x[1]).filter(x=>/data\/users/.test(x))))];
  console.log('4. demo writes to: ' + JSON.stringify(w));
  console.log('   demo scenes read: ' + await p.evaluate(()=>((S.topics['inference-t1']||{}).seen||[]).length) +
              ', demo attempts: ' + await p.evaluate(()=>Object.keys(S.att).length));

  // a scene runs in focus mode with the app header hidden, so leave the lesson first
  await p.click('.scbar [data-sc="-99"]'); await p.waitForTimeout(400);
  await p.click('[data-alltopics]'); await p.waitForTimeout(400);
  console.log('   left the lesson, app header back: ' + await p.locator('#hdProfile').isVisible());
  await p.click('#hdProfile'); await p.waitForTimeout(600);
  console.log('5. signed out → gate: ' + (await p.locator('.gatecard').count()>0));
  await p.click('[data-login="me"]'); await p.waitForTimeout(900);
  console.log('   as owner: chip "' + (await p.textContent('#hdProfile')).trim() +
    '", scenes read on t1: ' + await p.evaluate(()=>((S.topics['inference-t1']||{}).seen||[]).length) + ' (owner had none)' +
    ', attempts: ' + await p.evaluate(()=>Object.keys(S.att).length));

  await p.goto('file:///tmp/claude-0/harness.html'); await p.waitForTimeout(1600);
  console.log('6. reload remembers profile, no gate: ' + (await p.locator('.gatecard').count()===0) +
    ', chip "' + (await p.textContent('#hdProfile')).trim() + '"');

  await p.setViewportSize({width:393,height:852});
  await p.evaluate(()=>{try{localStorage.removeItem('njprof')}catch(e){}});
  await p.reload(); await p.waitForTimeout(1600);
  const r = await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
    card:Math.round(document.querySelector('.gatecard').getBoundingClientRect().width), toph:getComputedStyle(document.documentElement).getPropertyValue('--toph')}));
  console.log('7. phone gate: card=' + r.card + 'px overflow=' + (r.sw-r.cw) + ' headerVar=' + r.toph.trim());
  await p.screenshot({path:'/tmp/claude-0/gate-phone.png'});
  // drawer must not cover the tab bar
  await p.click('[data-login="me"]'); await p.waitForTimeout(800);
  await p.click('[data-tab="learn"]'); await p.waitForTimeout(400);
  await p.evaluate(()=>{S.navOpen=true;render()}); await p.waitForTimeout(400);
  const hit = await p.evaluate(()=>{
    const t=document.querySelector('[data-tab="bank"]').getBoundingClientRect();
    const el=document.elementFromPoint(t.x+t.width/2, t.y+t.height/2);
    return el?el.className+'|'+el.tagName:'none';});
  console.log('8. with the drawer open, the tab bar is reachable: ' + /data-tab|button/i.test(hit) + '  (hit: ' + hit + ')');
  await p.setViewportSize({width:1200,height:900}); await p.waitForTimeout(300);
  await p.evaluate(()=>{try{localStorage.removeItem('njprof')}catch(e){}}); await p.reload(); await p.waitForTimeout(1600);
  await p.screenshot({path:'/tmp/claude-0/gate-desktop.png'});
  console.log(errs.length?'ERRORS: '+errs.join(' | '):'no runtime errors');
  await b.close();
})();
