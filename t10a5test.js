// Walk 10A.5 end to end: every scene renders with real content, the drill works,
// the blanks accept their answers, the diagrams are well formed, and the mastery
// test grades.
const { chromium } = require('playwright');
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium/chrome-linux/chrome'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1400,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push('PAGEERROR '+e.message));
p.on('console',m=>{if(m.type()==='error'&&!/ERR_TUNNEL|fonts\.g/.test(m.text()))errs.push('CONSOLE '+m.text())});
await p.goto('file:///tmp/claude-0/harness.html');await p.waitForTimeout(1500);
if(await p.locator('[data-login="me"]').count()){await p.click('[data-login="me"]');await p.waitForTimeout(800)}
let fails=0;const bad=m=>{fails++;console.log('   FAIL '+m)};
await p.evaluate(()=>openTopic('official-t5'));await p.waitForTimeout(1000);
const les=await p.evaluate(()=>{const L=S.lessons['official-t5'];return L?{n:L.scenes.length,est:L.estMin,
  v:L.version,title:L.title,obj:L.objectives.length,refs:L.refs.length,
  flow:L.scenes.filter(s=>s.flow).length,scen:L.scenes.filter(s=>s.scenario).length,
  tricks:(L.revision.tricks||[]).length,no:topNo('official-t5')}:null});
if(!les) { console.log('lesson did not load'); process.exit(1); }
console.log(les.no+' '+les.title+'  v'+les.v+'  '+les.n+' scenes, '+les.est+' min');
console.log('   objectives '+les.obj+' · refs '+les.refs+' · flow '+les.flow+' · scenarios '+les.scen+' · mnemonics '+les.tricks);
if(les.flow<1) bad('no flow diagram');
if(les.scen<2) bad('fewer than two scenarios');
// every scene renders with real text
for(let i=0;i<les.n;i++){
  await p.evaluate(k=>gotoScene(k),i);await p.waitForTimeout(220);
  const info=await p.evaluate(()=>{const sc=S.lessons['official-t5'].scenes[S.learn.i],c=document.querySelector('.wscanvas');
    return {k:sc.kind,txt:c.innerText.trim().length,flow:!!c.querySelector('.flowbox svg'),
            blanks:c.querySelectorAll('[data-bchk]').length,hints:c.querySelectorAll('[data-hint]').length,
            found:c.querySelectorAll('.found').length};});
  console.log('   '+String(i+1).padStart(2)+' '+info.k.padEnd(11)+' text='+String(info.txt).padStart(5)+
    (info.flow?' flow':'')+(info.blanks?' blanks('+info.blanks+')':'')+(info.hints?' hintable':'')+
    (info.found?' checks('+info.found+')':'')+(info.txt<250?'   <-- THIN':''));
  if(info.txt<250) bad('scene '+(i+1)+' ('+info.k+') is thin: '+info.txt+' chars');
}
// the completion blanks must accept what the lesson taught
const ci=await p.evaluate(()=>S.lessons['official-t5'].scenes.findIndex(s=>s.kind==='completion'));
await p.evaluate(k=>gotoScene(k),ci);await p.waitForTimeout(300);
const answers=['due 2021, now 2027, postponed by the pandemic','Registration of Births and Deaths Act 1969, amended 2023','pilot 1964-65, full scale 1969-70','CBR 18.4, CDR 6.4','93 per 1,00,000 live births for 2019-21'];
for(let n=0;n<answers.length;n++){
  const inp=p.locator('.bi').first();
  if(!await inp.count())break;
  await inp.fill(answers[n]);await p.locator('[data-bchk]').first().click();
  // wait for this blank to be graded rather than guessing at a delay
  await p.waitForFunction(k=>Object.keys(S.learn.blanks['s5']||{}).length>k,n,{timeout:4000}).catch(()=>{});
}
const okc=await p.evaluate(()=>{const b=S.learn.blanks['s5']||{};return Object.keys(b).filter(k=>b[k].ok).length});
console.log('   completion: '+okc+' / 5 blanks accepted');
if(okc<5) bad('only '+okc+' of 5 blanks accepted their intended answer');
// mastery test
const qi=await p.evaluate(()=>S.lessons['official-t5'].scenes.findIndex(s=>s.kind==='quiz'));
await p.evaluate(k=>gotoScene(k),qi);await p.waitForTimeout(300);
await p.click('[data-startquiz]');await p.waitForTimeout(900);
const quiz=await p.evaluate(()=>S.learn.quiz?{n:S.learn.quiz.list.length,
  four:S.learn.quiz.list.every(q=>(q.options||[]).length===4),
  mix:S.learn.quiz.list.reduce((a,q)=>(a[q.diff]=(a[q.diff]||0)+1,a),{}),
  keys:S.learn.quiz.list.reduce((a,q)=>(a[q.answer]=(a[q.answer]||0)+1,a),{})}:null);
console.log('   mastery draw: '+JSON.stringify(quiz));
if(!quiz) bad('the mastery test did not start');
else{
  if(quiz.n!==10) bad('drew '+quiz.n+' questions, policy wants 10');
  if(!quiz.four) bad('an item does not have four options');
  if(JSON.stringify(quiz.mix)!==JSON.stringify({easy:3,moderate:5,hard:2})&&
     (quiz.mix.easy!==3||quiz.mix.moderate!==5||quiz.mix.hard!==2)) bad('mix is '+JSON.stringify(quiz.mix)+', wanted 3/5/2');
  if(Math.max(...Object.values(quiz.keys))>4) bad('key spread in the draw: '+JSON.stringify(quiz.keys));
}
await p.evaluate(()=>{const Q=S.learn.quiz;Q.list.forEach((q,k)=>{Q.ans[k]=q.answer;Q.conf[k]=2});render()});
await p.waitForTimeout(200);await p.click('#quizSubmit');await p.waitForTimeout(700);
const res=await p.evaluate(()=>({pct:S.learn.quiz.pct,pass:S.learn.quiz.pass,st:S.mastery['official-t5'].state}));
console.log('   all-correct run: '+res.pct+'% pass='+res.pass+' state='+res.st);
if(res.pct!==100||!res.pass) bad('a fully correct run did not pass');
// an all-A guesser must not pass
await p.evaluate(()=>{S.mastery={};S.learn.quiz=null;render()});
await p.evaluate(()=>gotoScene(S.lessons['official-t5'].scenes.findIndex(s=>s.kind==='quiz')));await p.waitForTimeout(250);
await p.click('[data-startquiz]');await p.waitForTimeout(800);
await p.evaluate(()=>{const Q=S.learn.quiz;Q.list.forEach((q,k)=>{Q.ans[k]='A';Q.conf[k]=1});render()});
await p.waitForTimeout(200);await p.click('#quizSubmit');await p.waitForTimeout(700);
const guess=await p.evaluate(()=>({pct:S.learn.quiz.pct,pass:S.learn.quiz.pass}));
console.log('   all-A guess: '+guess.pct+'% pass='+guess.pass);
if(guess.pass) bad('guessing A throughout passed the test');
console.log('\nerrors: '+(errs.join(' | ')||'none'));
console.log(fails?'FAILURES: '+fails:'10A.5 is complete and works end to end');
await b.close();process.exit(fails||errs.length?1:0);})();
