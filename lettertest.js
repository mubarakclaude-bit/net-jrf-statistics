// The self-lettered-options check must catch a genuinely lettered set and leave
// Indian initials alone.
const { chromium } = require('playwright');
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1200,height:900}});
await p.goto('file:///tmp/claude-0/harness.html');await p.waitForTimeout(1400);
if(await p.locator('[data-login="me"]').count()){await p.click('[data-login="me"]');await p.waitForTimeout(800)}
const r=await p.evaluate(()=>{
  const mk=o=>({source:'variant',items:[{id:'x',format:'single',topic:'t',diff:'easy',stem:'s',options:o,answer:'A',
    explanation:'a long enough explanation to clear the length check in the validator'}]});
  const lettered=mk(['A) one','B) two','C) three','D) four']);
  const initials=mk(['V. K. R. V. Rao','D. R. Gadgil','C. R. Rao','P. C. Mahalanobis']);
  const one=mk(['D. R. Gadgil and V. K. R. V. Rao','Something else','A third option','A fourth option']);
  const f=x=>vQset(x,1).filter(e=>/own letters/.test(e)).length;
  return {lettered:f(lettered),initials:f(initials),one:f(one)};});
console.log('lettered options flagged: '+r.lettered+' (expect 1)');
console.log('four Indian initials flagged: '+r.initials+' (expect 0)');
console.log('one option starting with an initial flagged: '+r.one+' (expect 0)');
const ok=r.lettered===1&&r.initials===0&&r.one===0;
console.log(ok?'the lettered-options check is precise':'FAILURE');
await b.close();process.exit(ok?0:1);})();
