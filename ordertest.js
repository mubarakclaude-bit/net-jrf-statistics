// Outside the learning path every list ascends in syllabus order, so the numbers on
// screen read 1, 2, 3A, 3B, 4 … rather than jumping 4, 1, 6, 9.
const { chromium } = require('playwright');
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1400,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/claude-0/harness.html');await p.waitForTimeout(1500);
if(await p.locator('[data-login="me"]').count()){await p.click('[data-login="me"]');await p.waitForTimeout(800)}
let fails=0;const bad=m=>{fails++;console.log('   FAIL '+m)};
const key=n=>{const m=/^(\d+)([AB]?)$/.exec(n);return m?+m[1]*10+(m[2]==='B'?1:0):999};
const asc=(l,where)=>{const k=l.map(key);
  if(k.join()!==k.slice().sort((a,b)=>a-b).join()) bad(where+' is not in syllabus order: '+l.join(', '));
  else console.log('   '+where.padEnd(22)+l.join(' '));};

asc(await p.evaluate(()=>mods(2).map(m=>modNo(m.id))),'mods(2)');
// bank filter
await p.click('[data-tab="bank"]');await p.waitForSelector('#fMod',{timeout:15000});
asc(await p.evaluate(()=>{
  const g=document.querySelectorAll('#fMod optgroup')[0];
  return g?[...g.querySelectorAll('option')].map(o=>o.textContent.split(' · ')[0]):[];
}),'bank filter');
// progress table
await p.click('[data-tab="progress"]');await p.waitForTimeout(800);
const rows=await p.evaluate(()=>[...document.querySelectorAll('.tbl tbody tr td:first-child .nnum')].map(x=>x.textContent.trim()));
asc(rows.filter(x=>/^\d/.test(x)),'progress table');
// admin picker
await p.click('[data-tab="admin"]');await p.waitForTimeout(700);
asc(await p.evaluate(()=>[...document.querySelectorAll('#fMod2 option')].map(o=>o.text.split(' · ')[0]).filter(x=>/^\d/.test(x))),'admin module picker');
// the home strip is a marks chart, so it ranks by marks and must stay that way
const strip=await p.evaluate(()=>{go('home');render();
  return [...document.querySelectorAll('.strip button')].map(b=>+(b.title.match(/— (\d+) marks/)||[])[1])});
console.log('   home strip marks     '+strip.join(' '));
if(strip.join()!==strip.slice().sort((a,b)=>b-a).join()) bad('the weightage strip is no longer ranked by marks');
// the learning path still honours its own mode
const pyq=await p.evaluate(()=>{S.mode='pyq';render();return pathOrder().map(m=>modNo(m.id))});
console.log('   learn path (weightage) '+pyq.join(' '));
if(pyq[0]!=='4') bad('weightage mode no longer leads with the heaviest module');
console.log('\nerrors: '+(errs.join(' | ')||'none'));
console.log(fails?'FAILURES: '+fails:'every list ascends, and the two deliberate orderings survive');
await b.close();process.exit(fails||errs.length?1:0);})();
