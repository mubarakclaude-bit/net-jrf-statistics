// Every lesson must carry two scenarios, each opening and closing in place
// without losing the learner's position in the lesson.
const { chromium } = require('playwright');
const T=['inference-t1','inference-t2','inference-t3','inference-t4','inference-t5','inference-t6','inference-t7','inference-t8','inference-t9','official-t1','official-t2','official-t3','official-t4','official-t5'];
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1400,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/claude-0/harness.html');await p.waitForTimeout(1400);
if(await p.locator('[data-login="me"]').count()){await p.click('[data-login="me"]');await p.waitForTimeout(800)}
let fails=0;const bad=m=>{fails++;console.log('   FAIL '+m)};
for(const t of T){
  await p.evaluate(x=>openTopic(x),t);await p.waitForTimeout(900);
  const info=await p.evaluate(x=>{const L=S.lessons[x];
    return {n:L.scenes.filter(s=>s.scenario).length, v:L.version,
      where:L.scenes.map((s,i)=>s.scenario?[i,s.kind,s.scenario.title]:null).filter(Boolean),
      thin:L.scenes.filter(s=>s.scenario&&(s.scenario.body||[]).join(' ').length<600).map(s=>s.id)};},t);
  console.log(t+'  v'+info.v+'  scenarios='+info.n);
  info.where.forEach(w=>console.log('    scene '+(w[0]+1)+' ('+w[1]+') — '+w[2]));
  if(info.n<2) bad(t+' has only '+info.n+' scenario(s)');
  if(info.thin.length) bad(t+' scenario too thin on '+info.thin.join(','));
  // open the second one and check it renders, then close it and check the scene is intact
  const idx=info.where[1][0];
  await p.evaluate(i=>gotoScene(i),idx);await p.waitForTimeout(350);
  const before=await p.evaluate(()=>document.querySelector('.wscanvas').innerText.length);
  await p.evaluate(()=>{const b=document.querySelector('.scenbtn');if(b)b.click()});await p.waitForTimeout(350);
  const open=await p.evaluate(()=>({wrap:!!document.querySelector('.scenwrap'),
     len:document.querySelector('.wscanvas').innerText.length,
     close:!!document.querySelector('.scenwrap [data-scen]')}));
  if(!open.wrap) bad(t+' second scenario did not open');
  if(open.len<=before) bad(t+' opening the scenario added no content');
  if(!open.close) bad(t+' opened scenario has no way back');
  await p.evaluate(()=>{const b=document.querySelector('.scenwrap [data-scen]');if(b)b.click()});await p.waitForTimeout(350);
  const after=await p.evaluate(()=>({wrap:!!document.querySelector('.scenwrap'),
     i:S.learn.i,len:document.querySelector('.wscanvas').innerText.length}));
  if(after.wrap) bad(t+' scenario would not close');
  if(after.i!==idx) bad(t+' closing the scenario moved the learner off the scene');
  console.log('    opened +'+(open.len-before)+' chars, closed back to scene '+(after.i+1));
}
console.log('\nerrors: '+(errs.join(' | ')||'none'));
console.log(fails?'FAILURES: '+fails:'two working scenarios in every lesson');
await b.close();process.exit(fails||errs.length?1:0);})();
