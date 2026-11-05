// The two papers are separate exams: the path never interleaves them, the scope
// defaults to Paper 2, and syllabus mode runs in official unit order.
const { chromium } = require('playwright');
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1400,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/claude-0/harness.html');await p.waitForTimeout(1400);
if(await p.locator('[data-login="me"]').count()){await p.click('[data-login="me"]');await p.waitForTimeout(800)}
let fails=0;const bad=m=>{fails++;console.log('   FAIL '+m)};

console.log('default scope: '+await p.evaluate(()=>paperScope()));
if(await p.evaluate(()=>paperScope())!==2) bad('the path does not open on Paper 2');

for(const mode of ['syllabus','pyq','personal']){
  for(const sc of [2,1,'all']){
    const o=await p.evaluate(a=>{S.mode=a[0];S.paper=a[1];render();
      return pathOrder().map(m=>({n:modNo(m.id),p:m.paper,s:m.sylOrder}))},[mode,sc]);
    const papers=o.map(x=>x.p);
    const runs=papers.filter((x,i)=>i===0||papers[i-1]!==x).length;   // 1 per paper if grouped
    const want=sc==='all'?2:1;
    const line=mode.padEnd(9)+' scope '+String(sc).padEnd(4)+' -> '+o.length+' modules, '+runs+' block(s), first '+o[0].n;
    console.log('  '+line);
    if(runs!==want) bad(mode+'/'+sc+': papers interleave ('+runs+' blocks)');
    if(sc!=='all'&&papers.some(x=>x!==sc)) bad(mode+'/'+sc+': scope leaked another paper');
    if(sc==='all'&&papers[0]!==2) bad(mode+': Paper 1 came before Paper 2');
    if(mode==='syllabus'){
      const sy=o.filter(x=>x.s!=null).map(x=>x.s);
      if(sy.join()!==sy.slice().sort((a,b)=>a-b).join()) bad('syllabus mode is not in syllabus order');
    }
  }
}
// the control is on the rail and the landing, and headings appear only in "both"
await p.evaluate(()=>{S.mode='pyq';S.paper=2;resetLearn(null);render()});await p.click('[data-tab="learn"]');await p.waitForTimeout(400);
const two=await p.evaluate(()=>({pills:document.querySelectorAll('[data-paper]').length,
  heads:document.querySelectorAll('.paperhd').length,cards:document.querySelectorAll('.modcard').length}));
console.log('Paper 2 only: '+JSON.stringify(two));
if(two.pills<3) bad('scope control missing');
if(two.heads) bad('paper headings shown when only one paper is in scope');
if(two.cards!==12) bad('expected 12 Paper 2 modules, got '+two.cards);
await p.evaluate(()=>{const b=document.querySelector('[data-paper="all"]');b.click()});await p.waitForTimeout(500);
const all=await p.evaluate(()=>({heads:[...document.querySelectorAll('.modgrid > .paperhd')].map(x=>x.textContent),
  railHeads:document.querySelectorAll('.navlist > .paperhd').length,
  cards:document.querySelectorAll('.modcard').length}));
console.log('Both: '+JSON.stringify(all));
if(all.heads.length!==2) bad('expected one heading per paper on the landing, got '+all.heads.length);
if(all.railHeads!==2) bad('expected one heading per paper in the rail, got '+all.railHeads);
if(all.cards!==21) bad('expected 21 modules, got '+all.cards);
// the choice is saved
const saved=await p.evaluate(()=>S.cfg.paper);
console.log('saved to config: '+JSON.stringify(saved));
if(saved!=='all') bad('scope not written to config');
// the bank filter groups by paper
await p.click('[data-tab="bank"]');
await p.waitForSelector('#fMod',{timeout:15000});   // the bank streams its modules in
const g=await p.evaluate(()=>[...document.querySelectorAll('#fMod optgroup')].map(o=>o.label+':'+o.children.length));
console.log('bank filter groups: '+JSON.stringify(g));
if(g.length!==2) bad('bank filter is not grouped by paper');
console.log('\nerrors: '+(errs.join(' | ')||'none'));
console.log(fails?'FAILURES: '+fails:'papers stay separate and syllabus mode is in unit order');
await b.close();process.exit(fails||errs.length?1:0);})();
