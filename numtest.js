// Numbering must be complete, unique, and the same in every study mode.
const { chromium } = require('playwright');
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1400,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/claude-0/harness.html');await p.waitForTimeout(1400);
if(await p.locator('[data-login="me"]').count()){await p.click('[data-login="me"]');await p.waitForTimeout(800)}
let fails=0;const bad=m=>{fails++;console.log('   FAIL '+m)};
const map=await p.evaluate(()=>{const m=numMap();
  return {mods:Object.keys(m.mod).length,tops:Object.keys(m.top).length,src:m.src,
    dupM:Object.values(m.mod).length-new Set(Object.values(m.mod)).size,
    dupT:Object.values(m.top).length-new Set(Object.values(m.top)).size,
    sample:[['inference',modNo('inference')],['inference-t1',topNo('inference-t1')],
            ['inference-t9',topNo('inference-t9')],['probability-t3',topNo('probability-t3')],
            ['rprog',modNo('rprog')]],
    missing:(S.catalog.modules||[]).flatMap(x=>(x.topics||[]).filter(t=>!m.top[t.id]).map(t=>t.id))};});
console.log('modules numbered: '+map.mods+'  topics numbered: '+map.tops+'  source: '+map.src);
console.log('samples: '+map.sample.map(s=>s[0]+'='+s[1]).join('  '));
const real=await p.evaluate(()=>({m:(S.catalog.modules||[]).length,
  t:(S.catalog.modules||[]).reduce((a,x)=>a+(x.topics||[]).length,0)}));
if(map.mods!==real.m) bad('catalog has '+real.m+' modules, numbered '+map.mods);
if(map.tops!==real.t) bad('catalog has '+real.t+' topics, numbered '+map.tops);
if(map.dupM||map.dupT) bad('duplicate numbers: '+map.dupM+' modules, '+map.dupT+' topics');
if(map.missing.length) bad('unnumbered topics: '+map.missing.slice(0,5).join(','));

// the same number in all three modes
const byMode={};
for(const mode of ['syllabus','pyq','personal']){
  byMode[mode]=await p.evaluate(m=>{S.mode=m;render();
    return [topNo('inference-t1'),topNo('regression-t4'),modNo('timeseries')].join('|');},mode);
  await p.waitForTimeout(150);
}
console.log('same numbers across modes: '+JSON.stringify(byMode));
if(new Set(Object.values(byMode)).size!==1) bad('numbering changed with the study mode');

// visible where it matters
await p.evaluate(()=>{S.mode='pyq';S.open.inference=true;render()});await p.waitForTimeout(300);
await p.click('[data-tab="learn"]');await p.waitForTimeout(400);
const land=await p.evaluate(()=>({cards:document.querySelectorAll('.modcard .mh .nnum').length,
  rows:document.querySelectorAll('.mtrow .nnum').length}));
console.log('landing: '+land.cards+' module cards numbered, '+land.rows+' topic rows numbered');
if(!land.cards||!land.rows) bad('numbers missing on the landing');
await p.evaluate(()=>openTopic('inference-t3'));await p.waitForTimeout(900);
const les=await p.evaluate(()=>({h1:(document.querySelector('.wscanvas h1')||{}).innerText||'',
  rail:document.querySelectorAll('.wsnav .nnum').length}));
console.log('lesson heading: '+JSON.stringify(les.h1.slice(0,60)));
const want=await p.evaluate(()=>topNo('inference-t3'));
if(les.h1.indexOf(want)!==0) bad('lesson heading does not open with its number '+want+': '+les.h1.slice(0,40));
await p.evaluate(()=>gotoScene(2));await p.waitForTimeout(300);
const crumb=await p.evaluate(()=>(document.querySelector('.scbar .crumb')||{}).innerText||'');
console.log('scene bar crumb: '+JSON.stringify(crumb.slice(0,60)));
if(crumb.indexOf(want)<0) bad('scene bar crumb carries no number');
// bank + progress
await p.evaluate(()=>{S.learn.quiz=null;gotoScene(-99)});await p.click('[data-tab="bank"]');
await p.waitForSelector('#fMod',{timeout:15000});
const bankOpt=await p.evaluate(()=>[...document.querySelectorAll('#fMod optgroup option')].slice(0,2).map(o=>o.textContent));
console.log('bank module filter: '+JSON.stringify(bankOpt));
if(!/^[\dA-Z-]+ · /.test(bankOpt[0]||'')) bad('bank filter options are not numbered');
await p.click('[data-tab="progress"]');await p.waitForTimeout(600);
const row=await p.evaluate(()=>(document.querySelector('.tbl tbody tr td')||{}).innerText||'');
console.log('progress table first cell: '+JSON.stringify(row.slice(0,40)));
if(!/\d/.test(row)) bad('progress table rows are not numbered');
const units=await p.evaluate(()=>{S.learn.quiz=null;resetLearn(null);S.route='learn';render();
  return {chips:document.querySelectorAll('.navmh .chip').length,
          sample:(unitOf('inference')||{}).no+' / '+(unitOf('rprog')||{}).no,
          src:numMap().src};});
console.log('unit labels: '+JSON.stringify(units));
if(units.src!=='official syllabus units') bad('syllabus order not in use');
if(units.sample!=='IV / X') bad('unit labels wrong: '+units.sample);
console.log('\nerrors: '+(errs.join(' | ')||'none'));
console.log(fails?'FAILURES: '+fails:'numbering is complete, unique and mode-independent');
await b.close();process.exit(fails||errs.length?1:0);})();
