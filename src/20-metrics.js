/* ===================== metrics ===================== */
/* Every list in the app runs in syllabus order once the official units are loaded, so
   the numbers on screen ascend. The learning path overrides this per study mode, and
   the home strip sorts itself by marks, because that is what it is showing. */
function mods(paper){
  const l=(S.catalog&&S.catalog.modules)||[];
  const out=(paper?l.filter(m=>m.paper===paper):l).slice();
  const hasSyl=out.some(m=>m.sylOrder!=null);
  return out.sort(hasSyl
    ?(a,b)=>((a.paper===b.paper?0:(b.paper||0)-(a.paper||0))||
             (a.sylOrder==null?999:a.sylOrder)-(b.sylOrder==null?999:b.sylOrder))
    :(a,b)=>(a.order||0)-(b.order||0));
}
function modById(id){return mods().find(m=>m.id===id)}
/* ---- syllabus numbering ----
   A module's number and a topic's decimal number are identities, not positions in
   the current view. They follow the official syllabus order once that has been
   imported, and the catalog order until then, so "1.3" means the same topic in
   every study mode. The map is cached and rebuilt only when the catalog changes. */
let NUMMAP=null,NUMSIG="";
function numSig(){
  const l=(S.catalog&&S.catalog.modules)||[];
  return l.map(m=>m.id+":"+(m.sylOrder==null?"-":m.sylOrder)+":"+((m.topics||[]).length)).join("|");
}
function numMap(){
  const sig=numSig();
  if(NUMMAP&&NUMSIG===sig)return NUMMAP;
  const l=((S.catalog&&S.catalog.modules)||[]).slice();
  const hasSyl=l.some(m=>m.sylOrder!=null);
  l.sort(hasSyl
    ?(a,b)=>(a.sylOrder==null?999:a.sylOrder)-(b.sylOrder==null?999:b.sylOrder)
    :(a,b)=>(a.order||0)-(b.order||0));
  const mod={},top={},U=(S.syl&&S.syl.units)||{};
  l.forEach((m,i)=>{
    // the official unit number when the syllabus has been imported, else the position
    const lab=(U[m.id]&&U[m.id].label)||String(i+1);
    mod[m.id]=lab;
    (m.topics||[]).forEach((t,j)=>{top[t.id]=lab+"."+(j+1)});
  });
  NUMMAP={mod:mod,top:top,src:hasSyl?"official syllabus units":"catalog order"};
  NUMSIG=sig;
  return NUMMAP;
}
function modNo(id){return numMap().mod[id]||""}
/* The official syllabus unit a module sits in, once the order has been imported.
   Two modules can share a unit — the catalog splits Unit III and Unit X. */
function unitOf(id){const u=(S.syl&&S.syl.units)||{};return u[id]||null}
function unitTag(id){const u=unitOf(id);
  return u?'<span class="chip dim" title="'+esc(u.title)+'">Unit '+esc(u.no)+'</span>':""}
function topNo(tid){return numMap().top[tid]||""}
function numSrc(){return numMap().src}
/* The number as a small label. Mono and tabular so a column of them lines up. */
function nTag(n,cls){return n?'<span class="nnum'+(cls?" "+cls:"")+'">'+n+'</span> ':""}

function baseAcc(m){const p=String(m.baseline||"0/1").split("/");const a=+p[0]||0,b=+p[1]||1;return b?a/b:0}
function loadedCount(id){const x=S.index&&S.index.modules&&S.index.modules[id];return x?x.total:0}
function minSample(m){return Math.max(10,Math.round((m.targetQ||50)*0.2))}
function mockPctFor(id){ // best module score across stored mocks with at least 4 questions from it
  let best=null;S.mocks.forEach(k=>{const b=k.byModule&&k.byModule[id];if(b&&b.n>=4){const p=pc(b.c,b.n);if(best===null||p>best)best=p}});return best}
function mstat(m){
  const ids=S.bank[m.id];
  let att=0,cor=0;
  const scan=(qid)=>{const a=S.att[qid];if(a&&a.n){att++;if(a.o)cor++}};
  if(ids)ids.forEach(q=>scan(q.id));
  else Object.keys(S.att).forEach(qid=>{if(qid.indexOf(m.id+"-")===0)scan(qid)});
  const loaded=loadedCount(m.id),target=m.targetQ||50;
  const acc=att?cor/att:0;
  const ba=baseAcc(m);
  const shrunk=(cor+SHRINK*ba)/(att+SHRINK);
  const need=minSample(m),mk=mockPctFor(m.id),pass=(m.passPct||80);
  const gAcc=att>=need&&acc*100>=pass, gMock=mk!==null&&mk>=pass;
  let st="empty";
  if(loaded===0)st="empty";
  else if(att===0)st="new";
  else if(gAcc&&gMock)st="ok";
  else if(acc*100>=pass)st="mid";
  else if(acc*100>=60)st="mid";
  else st="bad";
  return{m:m,att:att,cor:cor,acc:acc,shrunk:shrunk,base:ba,loaded:loaded,target:target,
    cov:pc(Math.min(att,target),target),fill:pc(Math.min(loaded,target),target),
    need:need,mock:mk,gAcc:gAcc,gMock:gMock,st:st,
    proj:(m.marks||0)*shrunk,baseMarks:(m.marks||0)*ba};
}
function overall(paper){
  const ms=mods(paper).map(mstat);
  const marks=ms.reduce((s,x)=>s+(x.m.marks||0),0);
  const proj=ms.reduce((s,x)=>s+x.proj,0);
  const base=ms.reduce((s,x)=>s+x.baseMarks,0);
  const att=ms.reduce((s,x)=>s+x.att,0),cor=ms.reduce((s,x)=>s+x.cor,0);
  const loaded=ms.reduce((s,x)=>s+x.loaded,0),target=ms.reduce((s,x)=>s+x.target,0);
  const readiness=marks?ms.reduce((s,x)=>{
    const a=Math.min(1,x.acc/((x.m.passPct||80)/100)),n=Math.min(1,x.att/x.need);
    return s+(x.m.marks||0)*a*n},0)/marks:0;
  return{ms:ms,marks:marks,proj:proj,base:base,att:att,cor:cor,loaded:loaded,target:target,
    green:ms.filter(x=>x.st==="ok").length,readiness:readiness,acc:att?cor/att:0};
}
function fmtStats(){ // accuracy by question format across everything loaded
  const o={};FORDER.forEach(f=>o[f]={att:0,cor:0});
  Object.keys(S.bank).forEach(mid=>S.bank[mid].forEach(q=>{
    const a=S.att[q.id];if(!a||!a.n)return;const f=o[q.format]||o.single;f.att++;if(a.o)f.cor++}));
  return o;
}
function target(){return S.cfg.target||150}
function examDays(){if(!S.cfg.exam)return null;const d=new Date(S.cfg.exam+"T00:00:00");return Math.ceil((d-new Date())/86400000)}
function allQ(){const out=[];Object.keys(S.bank).forEach(mid=>out.push.apply(out,S.bank[mid]));return out}

