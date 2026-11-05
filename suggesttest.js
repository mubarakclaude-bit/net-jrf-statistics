// The suggestion card must agree with the path on screen, and must say so when the
// next topic in that order has no lesson yet.
const { chromium } = require('playwright');
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1400,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/claude-0/harness.html');await p.waitForTimeout(1400);
if(await p.locator('[data-login="me"]').count()){await p.click('[data-login="me"]');await p.waitForTimeout(800)}
let fails=0;const bad=m=>{fails++;console.log('   FAIL '+m)};
await p.click('[data-tab="learn"]');await p.waitForTimeout(400);
for(const mode of ['syllabus','pyq']){
  const r=await p.evaluate(m=>{S.mode=m;resetLearn(null);render();
    const c=document.querySelector('.nextup');
    const first=pathOrder()[0];
    const firstTopic=topicOrder(first)[0];
    return {card:c?c.innerText.replace(/\n+/g,' | '):'none',
            pathFirst:modNo(first.id)+' '+first.name, firstTopicNo:topNo(firstTopic.id)};},mode);
  console.log(mode+':');
  console.log('   path starts at   '+r.pathFirst);
  console.log('   card says        '+r.card.slice(0,150));
  if(mode==='syllabus'){
    if(!/^1 /.test(r.pathFirst)) bad('syllabus path does not start at unit 1: '+r.pathFirst);
    if(r.card.indexOf(r.firstTopicNo)<0) bad('syllabus card does not name the first topic in order ('+r.firstTopicNo+')');
    if(!/No lesson authored/.test(r.card)) bad('card does not say the topic has no lesson yet');
    if(!/Start 4\.1 instead/.test(r.card)) bad('card offers no authored alternative');
  } else {
    if(!/4\.1/.test(r.card)) bad('weightage card should still lead with the heaviest authored topic');
    if(/No lesson authored/.test(r.card)) bad('weightage card suggested an unauthored topic');
  }
}
console.log('\nerrors: '+(errs.join(' | ')||'none'));
console.log(fails?'FAILURES: '+fails:'the suggestion follows the path in every mode');
await b.close();process.exit(fails||errs.length?1:0);})();
