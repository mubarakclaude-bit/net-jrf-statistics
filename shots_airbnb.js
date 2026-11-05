const { chromium } = require('playwright');
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome'}).catch(()=>chromium.launch());
const shots=[];
async function go(name,w,hh,theme,fn){
  const p=await b.newPage({viewport:{width:w,height:hh}});
  await p.goto('file:///tmp/claude-0/harness.html');await p.waitForTimeout(1400);
  if(await p.locator('[data-login="me"]').count()){await p.click('[data-login="me"]');await p.waitForTimeout(800)}
  await p.evaluate(t=>document.documentElement.setAttribute('data-theme',t),theme);
  if(fn)await fn(p);
  await p.waitForTimeout(500);
  const f='/tmp/claude-0/shots/'+name+'.png';
  await p.screenshot({path:f});shots.push(f);await p.close();
}
await go('01-home-light',1280,900,'light');
await go('02-learn-light',1280,900,'light',async p=>{await p.click('[data-tab="learn"]');await p.waitForTimeout(400);
  await p.evaluate(()=>{S.open.inference=true;render()})});
await go('03-lesson-found',1280,900,'light',async p=>{await p.click('[data-tab="learn"]');await p.waitForTimeout(300);
  await p.evaluate(()=>openTopic('inference-t1'));await p.waitForTimeout(900);
  await p.evaluate(()=>gotoScene(0));await p.waitForTimeout(400)});
await go('04-drill-light',1280,900,'light',async p=>{await p.click('[data-tab="bank"]');await p.waitForTimeout(900);
  await p.evaluate(()=>{const r=document.querySelector('.qrow');if(r)r.click()});await p.waitForTimeout(600)});
await go('05-mock-light',1280,900,'light',async p=>{await p.click('[data-tab="mock"]');await p.waitForTimeout(500)});
await go('06-home-dark',1280,900,'dark');
await go('07-lesson-dark',1280,900,'dark',async p=>{await p.click('[data-tab="learn"]');await p.waitForTimeout(300);
  await p.evaluate(()=>openTopic('inference-t6'));await p.waitForTimeout(900);
  await p.evaluate(()=>gotoScene(3));await p.waitForTimeout(400)});
await go('08-phone-learn',390,844,'light',async p=>{await p.click('[data-tab="learn"]');await p.waitForTimeout(400);
  await p.evaluate(()=>{S.open.inference=true;render()})});
await go('09-phone-sheet',390,844,'light',async p=>{await p.click('[data-tab="learn"]');await p.waitForTimeout(300);
  await p.evaluate(()=>openTopic('inference-t1'));await p.waitForTimeout(900);
  await p.evaluate(()=>gotoScene(1));await p.waitForTimeout(300);
  await p.evaluate(()=>{const r=document.querySelector('.scbar [data-reqopen]');if(r)r.click()});await p.waitForTimeout(500)});
console.log(shots.join('\n'));
await b.close()})();
