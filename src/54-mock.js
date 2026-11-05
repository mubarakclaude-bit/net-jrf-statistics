/* ---------- mock ---------- */
function vMock(){
  const g=gate();if(g)return g;
  if(S.mock)return S.mock.done?mockResult():mockRun();
  const o2=overall(2),o1=overall(1);
  const gaps=o2.ms.concat(o1.ms).filter(x=>x.loaded===0);
  const hist=S.mocks.slice().reverse().slice(0,12);
  return '<div class="hd"><h1>Mock tests</h1><p>Sampled by marks and by the format mix of the real paper — '+FORDER.map(k=>FMT[k].mix+"% "+FMT[k].s.toLowerCase()).join(", ")+'.</p></div>'+
  (gaps.length?'<div class="banner"><div><b>'+gaps.length+' module'+(gaps.length>1?"s have":" has")+' no content yet</b> ('+esc(gaps.map(x=>shortName(x.m)).join(", "))+'). A mock will quietly redistribute those questions, so it tests less than the full syllabus until they are loaded.</div></div>':"")+
  '<div class="card" style="margin-bottom:12px"><h3 style="margin-bottom:10px">Sit a paper</h3>'+
    '<div class="grid g4" style="margin-bottom:12px">'+
      '<div><label class="fl">Time I have</label><select id="mkMins">'+
        [[10,"10 minutes"],[20,"20 minutes"],[30,"half an hour"],[45,"45 minutes"],[60,"an hour"],
         [90,"90 minutes"],[120,"2 hours · full paper"],[0,"no limit — set the count myself"]]
         .map(x=>'<option value="'+x[0]+'"'+(x[0]===30?" selected":"")+'>'+x[1]+
           (x[0]?' · '+Math.max(5,Math.round(x[0]*60/PACE))+' questions':'')+'</option>').join("")+'</select></div>'+
      '<div><label class="fl">Questions</label><select id="mkN"><option value="25">25 · quick</option><option value="50">50 · half paper</option><option value="100">100 · full Paper 2</option><option value="150">150 · both papers</option></select>'+
        '<p class="note num" id="mkCount" style="margin-top:4px"></p></div>'+
      '<div><label class="fl">Scope</label><select id="mkScope"><option value="2">Paper 2 only</option><option value="all">Paper 1 + Paper 2</option><option value="weak">My weak modules</option><option value="wrong">Only questions I got wrong</option></select></div>'+
      '<div><label class="fl">Timer</label><select id="mkTimer"><option value="1" selected>Exam pace ('+PACE+'s a question)</option><option value="0">Untimed</option></select></div>'+
      '<div><label class="fl">Pass mark</label><select id="mkPass"><option value="80" selected>80% · turns modules green</option><option value="60">60% · qualifying feel</option></select></div>'+
    '</div>'+
    '<button class="btn p" id="mkStart">Start mock</button>'+
    '<p class="note" style="margin-top:8px">Pick the time you have and the question count follows at exam pace ('+PACE+'s each); choose \u201cno limit\u201d to set the count yourself. Answers stay hidden until you submit. Each question you answer also counts toward its module in the bank, so a mock is never wasted practice. Write-in numericals are left out of mocks — they cannot be scored at pace — so drill those from the bank.</p>'+
  '</div>'+
  (hist.length?'<div class="card"><h3 style="margin-bottom:8px">History</h3><div class="scroll"><table class="tbl"><thead><tr><th>Date</th><th>Scope</th><th>Score</th><th>%</th><th>Pace</th><th>Modules at pass</th></tr></thead><tbody>'+
    hist.map(k=>'<tr><td class="mono">'+esc(dayStr(k.ts))+'</td><td>'+esc(k.scope||"P2")+'</td><td class="num">'+k.c+'/'+k.n+'</td>'+
      '<td><span class="chip '+(pc(k.c,k.n)>=(k.pass||80)?"ok":pc(k.c,k.n)>=60?"mid":"bad")+' num">'+pc(k.c,k.n)+'%</span></td>'+
      '<td class="num">'+(k.secs?Math.round(k.secs/Math.max(1,k.n))+"s":"—")+'</td>'+
      '<td class="num">'+Object.keys(k.byModule||{}).filter(id=>k.byModule[id].n>=4&&pc(k.byModule[id].c,k.byModule[id].n)>=(k.pass||80)).length+'</td></tr>').join("")+
    '</tbody></table></div>'+(S.mocks.length>1?mockSpark():"")+'</div>':
   '<div class="empty"><h3>No mocks yet</h3><p>One mock at 80% is what turns a module green. Accuracy in the bank alone will not do it.</p></div>');
}
function mockSpark(){
  const d=S.mocks.slice(-16).map(k=>pc(k.c,k.n));
  const w=260,h=48,n=d.length;
  const pts=d.map((v,i)=>[(n===1?0:i*(w-8)/(n-1))+4,h-4-(h-12)*v/100]);
  const path=pts.map((p,i)=>(i?"L":"M")+p[0].toFixed(1)+" "+p[1].toFixed(1)).join(" ");
  return '<div style="margin-top:10px"><div class="lbl">Mock scores, oldest to newest</div>'+
   '<svg viewBox="0 0 '+w+' '+h+'" style="width:100%;max-width:320px;height:48px" aria-hidden="true">'+
   '<line x1="4" y1="'+(h-4-(h-12)*0.8).toFixed(1)+'" x2="'+(w-4)+'" y2="'+(h-4-(h-12)*0.8).toFixed(1)+'" stroke="var(--ok)" stroke-width="1" stroke-dasharray="3 3"/>'+
   '<path d="'+path+'" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round"/>'+
   pts.map(p=>'<circle cx="'+p[0].toFixed(1)+'" cy="'+p[1].toFixed(1)+'" r="2.5" fill="var(--accent)"/>').join("")+
   '</svg><div class="note">dashed line = 80%</div></div>';
}
function buildMock(n,scope,pass){
  const paper=scope==="all"?null:2;
  let ms=mods(paper).map(mstat);
  if(scope==="weak")ms=ms.filter(x=>x.loaded>0&&(x.att===0||x.acc<0.8));
  const pool={};let avail=0;
  ms.forEach(x=>{let l=(S.bank[x.m.id]||[]).filter(q=>!isFree(q)&&!q.needsReview);
    // a timed mock needs scorable options, and an item flagged for repair has none
    if(scope==="wrong")l=l.filter(q=>statusOf(q.id)==="wrong");
    pool[x.m.id]=l.slice();avail+=l.length});
  if(!avail)return null;
  const live=ms.filter(x=>pool[x.m.id].length);
  const tm=live.reduce((s,x)=>s+(x.m.marks||0),0)||1;
  // marks-proportional allocation, largest remainder, capped by what exists
  const alloc={},rem=[];let used=0;
  live.forEach(x=>{const raw=n*(x.m.marks||0)/tm;const f=Math.min(pool[x.m.id].length,Math.floor(raw));alloc[x.m.id]=f;used+=f;rem.push([x.m.id,raw-Math.floor(raw)])});
  rem.sort((a,b)=>b[1]-a[1]);
  let gi=0;
  while(used<Math.min(n,avail)&&gi<rem.length*40){const id=rem[gi%rem.length][0];if(alloc[id]<pool[id].length){alloc[id]++;used++}gi++}
  // format mix targets
  const want={};FORDER.forEach(k=>want[k]=Math.round(n*FMT[k].mix/100));
  const out=[];
  Object.keys(alloc).forEach(id=>{
    const k=alloc[id];if(!k)return;
    const byF={};pool[id].forEach(q=>(byF[q.format]||(byF[q.format]=[])).push(q));
    Object.keys(byF).forEach(f=>byF[f].sort((a,b)=>score(b)-score(a)));
    const taken=[];
    // first pass: respect the remaining format quota
    FORDER.forEach(f=>{
      const list=byF[f]||[];
      while(taken.length<k&&want[f]>0&&list.length){taken.push(list.shift());want[f]--}
    });
    // second pass: fill whatever is left
    const rest=[].concat.apply([],FORDER.map(f=>byF[f]||[])).sort((a,b)=>score(b)-score(a));
    while(taken.length<k&&rest.length){const q=rest.shift();if(taken.indexOf(q)<0)taken.push(q)}
    out.push.apply(out,taken);
  });
  function score(q){const a=S.att[q.id]||{};if(!a.n)return 3;if(!a.o)return 2;return 1-Math.min(.9,(now()-(a.t||0))/(1000*86400*30))}
  for(let i=out.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const t=out[i];out[i]=out[j];out[j]=t}
  return out.slice(0,n);
}
function mockRun(){
  const M=S.mock,q=M.list[M.i],total=M.list.length;
  const left=M.timed?(M.budget-(now()-M.t0)/1000):null;
  const m=modById(q.moduleId),F=FMT[q.format]||FMT.single;
  const pairs=(q.pairs||[]).length?'<div class="scroll"><table class="tbl"><thead><tr><th>List I</th><th>List II</th></tr></thead><tbody>'+
    q.pairs.map(p=>'<tr><td>'+esc(p[0]!=null?p[0]:p.i)+'</td><td>'+esc(p[1]!=null?p[1]:p.ii)+'</td></tr>').join("")+'</tbody></table></div>':"";
  const seq=(q.items||[]).length?'<div class="row tight" style="margin-bottom:10px">'+q.items.map((it,k)=>'<span class="chip dim">'+String.fromCharCode(65+k)+'. '+esc(it)+'</span>').join("")+'</div>':"";
  return '<div class="hd"><h1 style="font-size:1.15rem">Mock · '+total+' questions</h1>'+
    '<div class="sp row tight">'+(M.timed?'<span class="clock'+(left<0?" over":"")+'" id="mkClock">'+(left<0?"+":"")+hhmm(Math.abs(left))+'</span>':'<span class="chip dim">untimed</span>')+
    '<button class="btn sm" id="mkSubmit">Submit</button></div></div>'+
  '<div class="card flat" style="margin-bottom:10px"><div class="kv"><span>'+Object.keys(M.ans).length+' of '+total+' answered</span><span class="note">'+esc(m?shortName(m):"")+' · '+esc(F.s)+'</span></div>'+
    bar(pc(Object.keys(M.ans).length,total),"ac",true)+'</div>'+
  '<div class="card"><div class="stem">'+(M.i+1)+'. '+richText(q.stem)+'</div>'+pairs+seq+
    ((q.statements||[]).length?'<div style="margin-bottom:12px">'+q.statements.map((s,k)=>'<div class="stmt"><span class="sl">'+String.fromCharCode(65+k)+'</span><span class="sb">'+esc(s)+'</span></div>').join("")+'</div>':"")+
    (q.options||[]).map((o,k)=>{const L=String.fromCharCode(65+k);
      return '<button class="opt" data-mopt="'+L+'" aria-pressed="'+(M.ans[M.i]===L)+'"><span class="ol">'+L+'</span><span>'+richText(o)+'</span></button>'}).join("")+
    '<div class="row" style="margin-top:12px">'+
      (M.i>0?'<button class="btn sm" data-mnav="-1">‹ prev</button>':"")+
      '<button class="btn sm" data-mclear="1">clear</button>'+
      '<button class="btn sm gh" data-askopen="1" title="Ask Claude about a term in this question">✦ Ask</button>'+
      '<span class="sp"></span>'+
      (M.i<total-1?'<button class="btn p sm" data-mnav="1">next ›</button>':'<button class="btn p sm" id="mkSubmit2">Submit paper</button>')+
    '</div></div>'+
  '<div class="card" style="margin-top:12px"><div class="lbl" style="margin-bottom:6px">Question palette</div><div class="pal">'+
    M.list.map((_,k)=>'<button data-mgo="'+k+'" class="'+(M.ans[k]?"done":"")+(k===M.i?" cur":"")+'">'+(k+1)+'</button>').join("")+'</div></div>';
}
function submitMock(){
  const M=S.mock;let c=0;const byModule={};
  M.list.forEach((q,k)=>{
    const picked=M.ans[k];const ok=picked===q.answer;
    if(picked){record(q,ok);if(ok)c++}
    const b=byModule[q.moduleId]||(byModule[q.moduleId]={n:0,c:0});b.n++;if(ok)b.c++;
  });
  M.done=true;M.c=c;M.n=M.list.length;M.secs=Math.round((now()-M.t0)/1000);M.byModule=byModule;
  S.mocks.push({ts:now(),n:M.n,c:c,pass:M.pass,scope:M.scope==="all"?"P1+P2":M.scope==="weak"?"weak":M.scope==="wrong"?"redo":"P2",secs:M.secs,byModule:byModule});
  saveMocks();if(M.tick)clearInterval(M.tick);render();window.scrollTo(0,0);
}
function mockResult(){
  const M=S.mock,p=pc(M.c,M.n),pass=p>=M.pass;
  const rows=Object.keys(M.byModule).map(id=>{const b=M.byModule[id],m=modById(id);
    return{id:id,name:m?m.name:id,marks:m?m.marks:0,n:b.n,c:b.c,p:pc(b.c,b.n)}}).sort((a,b)=>b.marks-a.marks);
  const newGreen=rows.filter(r=>r.n>=4&&r.p>=M.pass);
  const byF={};M.list.forEach((q,k)=>{const f=byF[q.format]||(byF[q.format]={n:0,c:0});f.n++;if(M.ans[k]===q.answer)f.c++});
  return '<div class="hd"><h1>Mock result</h1><p>'+M.n+' questions in '+hhmm(M.secs)+' · '+Math.round(M.secs/M.n)+'s a question (exam pace is '+PACE+'s)</p>'+
    '<div class="sp"><button class="btn sm" id="mkExit">Done</button></div></div>'+
  '<div class="card" style="margin-bottom:12px"><div class="row" style="align-items:flex-end;gap:20px">'+
    '<div><div class="lbl">Score</div><div class="big">'+M.c+'<small>/'+M.n+'</small></div></div>'+
    '<div><div class="lbl">Percent</div><div class="big" style="color:var(--'+(pass?"ok":p>=60?"mid":"bad")+')">'+p+'<small>%</small></div></div>'+
    '<div><div class="lbl">Pass mark</div><div class="big" style="font-size:1.4rem;color:var(--fg3)">'+M.pass+'<small>%</small></div></div>'+
    '<div style="margin-left:auto"><span class="chip '+(pass?"ok":"bad")+'">'+(pass?"passed":"below pass")+'</span></div></div>'+
    bar(p,pass?"ok":p>=60?"mid":"bad")+
    (newGreen.length?'<p class="note" style="margin-top:8px"><b>'+newGreen.length+' module'+(newGreen.length>1?"s":"")+'</b> cleared '+M.pass+'% here ('+esc(newGreen.map(r=>r.name).join(", "))+'). They go green once their bank accuracy also holds.</p>':
      '<p class="note" style="margin-top:8px">No module cleared '+M.pass+'% on at least 4 questions, so nothing turns green from this paper.</p>')+
  '</div>'+
  '<div class="grid g2" style="margin-bottom:12px">'+
    '<div class="card"><h3 style="margin-bottom:8px">By module</h3><div class="scroll"><table class="tbl"><thead><tr><th>Module</th><th>Marks</th><th>Score</th><th>%</th></tr></thead><tbody>'+
      rows.map(r=>'<tr><td>'+esc(r.name)+'</td><td class="num">'+r.marks+'</td><td class="num">'+r.c+'/'+r.n+'</td><td><span class="chip '+(r.p>=M.pass?"ok":r.p>=60?"mid":"bad")+' num">'+r.p+'%</span></td></tr>').join("")+
      '</tbody></table></div></div>'+
    '<div class="card"><h3 style="margin-bottom:8px">By format</h3>'+FORDER.filter(f=>byF[f]).map(f=>{const b=byF[f];
      return '<div style="margin-bottom:8px"><div class="kv"><span>'+esc(FMT[f].n)+' <span class="note">(June: '+FMT[f].base[0]+'/'+FMT[f].base[1]+')</span></span><b>'+b.c+'/'+b.n+'</b></div>'+
        bar(pc(b.c,b.n),pc(b.c,b.n)>=M.pass?"ok":pc(b.c,b.n)>=60?"mid":"bad",true)+'</div>'}).join("")+'</div>'+
  '</div>'+
  '<div class="card"><h3 style="margin-bottom:8px">Review every question</h3>'+
    M.list.map((q,k)=>{const picked=M.ans[k],ok=picked===q.answer;
      return '<details class="sp"><summary><span class="chip '+(ok?"ok":picked?"bad":"dim")+'">'+(ok?"✓":picked?"✗":"—")+'</span><span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:400">'+(k+1)+'. '+esc(String(q.stem).replace(/\s+/g," "))+'</span></summary>'+
      '<div><div class="stem" style="font-size:.92rem">'+richText(q.stem)+'</div>'+
      (q.options||[]).map((o,j)=>{const L=String.fromCharCode(65+j);
        return '<div class="opt'+(L===q.answer?" right":L===picked?" wrong":"")+'" style="pointer-events:none"><span class="ol">'+L+'</span><span>'+richText(o)+'</span></div>'}).join("")+
      '<div class="expl"><h4>Why '+esc(q.answer)+'</h4>'+esc(q.explanation||"No explanation loaded.")+'</div>'+
      '<button class="btn sm" data-q="'+esc(q.id)+'">Open in the bank</button></div></details>'}).join("")+
  '</div>'+
  askBox("ask-mock","Ask Claude what this result says about my preparation",
    "A UGC NET Statistics candidate preparing for JRF just sat a mock. Score "+M.c+"/"+M.n+" ("+p+"%). By module: "+rows.map(r=>r.name+" "+r.c+"/"+r.n).join("; ")+
    ". By question format: "+FORDER.filter(f=>byF[f]).map(f=>FMT[f].n+" "+byF[f].c+"/"+byF[f].n).join("; ")+
    ". Pace: "+Math.round(M.secs/M.n)+" seconds a question against an exam pace of "+PACE+"s. In the real June 2026 paper they scored 31/100 questions in Paper 2, strong on match-the-list and time series, very weak on numerical work (4/21) and multi-statement items (2/19)."+
    "\n\nSay what this mock changes about that picture, name the single biggest leak, and give three specific actions for the next two weeks. Be blunt and concrete, under 220 words, plain text. Do not restate the numbers back.","complex");
}

