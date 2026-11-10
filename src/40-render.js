/* ===================== render ===================== */
function render(){
  if(S.ready&&!S.authed){
    document.body.classList.add("gated");
    const nv=$("#nav");nv.innerHTML="";nv.dataset.h="";measureTop();
    allRoutes().forEach(k=>{const n=$("#v-"+k);if(n)n.classList.remove("on")});
    const h=$("#v-home");h.classList.add("on");h.innerHTML=vAuth();
    wire();return;
  }
  document.body.classList.remove("gated");
  document.body.classList.toggle("focus",
    S.focus!==false && S.route==="learn" && !!S.learn.topicId &&
    (S.learn.i>=0 || !!S.learn.quiz) && !!S.lessons[S.learn.topicId]);
  renderNav();
  measureTop();
  const o=S.ready&&S.catalog?overall(2):null;
  $("#hdScore").textContent=o?("projected "+Math.round(o.proj)+"/200 · P2"):"—";
  const d=examDays(),hd=$("#hdDays");
  if(d===null){hd.textContent="set exam date";hd.className="chip dim"}
  else{hd.textContent=d>=0?d+" days to exam":"exam date passed";hd.className="chip "+(d<=21?"bad":d<=60?"mid":"ac")}
  const bst=$("#hdBuild");if(bst)bst.textContent="build "+BUILD.slice(5,16);
  const pc2=$("#hdProfile");
  if(pc2){pc2.textContent=profileName();pc2.className="chip "+(S.profile==="me"?"dim":"och");pc2.hidden=!S.ready}
  allRoutes().forEach(k=>{const s=$("#v-"+k);if(s)s.classList.toggle("on",S.route===k)});
  document.body.classList.toggle("wide",S.route==="learn");
  const f={home:vHome,learn:vLearn,bank:vBank,mock:vMock,progress:vProgress,admin:vAdmin}[S.route]||featureView(S.route);
  if(f)$("#v-"+S.route).innerHTML=f()+(typeof reqModal==="function"?reqModal():"")
    +(typeof askPanelHTML==="function"?askPanelHTML():"")
    +(typeof askChipHTML==="function"?askChipHTML():"");
  wire();
  featureAfterRender();
}
function measureTop(){
  const t=$("#top");if(!t)return;
  const h=document.body.classList.contains("focus")?0:Math.round(t.getBoundingClientRect().height);
  if(h!==S.topH){S.topH=h;document.documentElement.style.setProperty("--toph",h+"px")}
}
function renderNav(){
  const o=S.ready&&S.catalog?overall():null;
  const lp=o?learnProgress():null;
  const html=TABS.concat(featureTabs()).filter(([k])=>k!=="admin"||S.isAdmin).map(([k,n])=>{
    let b="";
    if(k==="learn"&&lp)b=' <span class="chip '+(lp.mastered?"ok":"dim")+' num">'+lp.mastered+'/'+lp.withLesson+'</span>';
    if(k==="bank"&&o)b=' <span class="chip dim num">'+o.loaded+'</span>';
    if(k==="mock"&&S.mocks.length)b=' <span class="chip dim num">'+S.mocks.length+'</span>';
    return '<button data-tab="'+k+'" aria-current="'+(S.route===k)+'">'+n+b+'</button>'}).join("");
  const nav=$("#nav");
  if(nav.dataset.h===html)return;          // nothing changed — leave the scroll position alone
  const keep=nav.scrollLeft;
  nav.innerHTML=html;nav.dataset.h=html;
  nav.scrollLeft=keep;
  const cur=nav.querySelector('[aria-current="true"]');
  if(cur&&cur.offsetLeft<keep)nav.scrollLeft=Math.max(0,cur.offsetLeft-12);
  else if(cur&&cur.offsetLeft+cur.offsetWidth>keep+nav.clientWidth)
    nav.scrollLeft=cur.offsetLeft+cur.offsetWidth-nav.clientWidth+12;
}
function gate(){
  if(!S.ready)return '<div class="card" style="margin-bottom:12px"><div class="row tight">'+
      '<span class="chip ac">starting up</span><span class="note">'+esc(S.boot||"Connecting…")+'</span></div>'+
      bar(S.boot?60:25,"ac")+
      '<p class="note" style="margin-top:8px">If this does not clear within about fifteen seconds, this view has not granted the page its database. The message that replaces this will say what to do.</p></div>'+
    '<div class="grid g2">'+Array(2).fill('<div class="card"><div class="sk" style="width:40%"></div><div class="sk" style="height:26px;margin-top:10px"></div></div>').join("")+'</div>';
  if(!S.db)return permBanner();
  if(!S.catalog)return '<div class="banner ac"><div><b>The database is reachable but the syllabus is not in it.</b> '+
    (S.readErr?'The last read failed with <span class="mono">'+esc(S.readErr)+'</span>, which usually means this view may not read shared data. ':'Nothing has been written to <span class="mono">meta/catalog</span> yet. ')+
    'Open <b>Admin → Diagnostics</b> and run the checks — it reads every path the app needs and reports what came back.</div></div>';
  return null;
}
function permBanner(){
  const ps=S.permState||{};
  const dbState=ps.db||ps["db"]||null;
  const known=S.permState?Object.keys(ps).map(k=>k+": "+ps[k]).join(" · "):"";
  return '<div class="banner bad"><div><b>This view has not given the page its database.</b>'+
    '<p style="margin:6px 0 0">Every lesson, question and score lives in the artifact\'s own store, so without it there is nothing to show. '+
    (S.dbMsg==="slow"?'The grant did not answer within twelve seconds. ':'')+
    (dbState?'Permission state for the database: <b>'+esc(String(dbState))+'</b>. ':'')+
    'This usually means the page was opened signed out, in a preview, or the permission was declined.</p>'+
    (known?'<p class="note" style="margin-top:6px">'+esc(known)+'</p>':'')+
    '<div class="row tight" style="margin-top:9px">'+
      (S.perm&&S.perm.manage?'<button class="btn p sm" id="permOpen">Open permissions</button>':'')+
      (S.perm&&S.perm.request?'<button class="btn sm" id="permAsk">Ask again</button>':'')+
      '<button class="btn sm" id="permReload">Reload the page</button>'+
    '</div></div></div>';
}

/* ---------- home ---------- */
function vHome(){
  const g=gate();if(g)return g;
  const o2=overall(2),o1=overall(1),oA=overall();
  const t=target(),d=examDays();
  const lp=learnProgress();
  return '<div class="hd"><h1>Where you stand</h1><p>Paper 2 marks, weighted by what the June 2026 paper actually asked.</p></div>'+
  '<div class="card" style="margin-bottom:12px">'+
    '<div class="row" style="align-items:flex-end;gap:18px">'+
      '<div><div class="lbl">Projected Paper 2</div><div class="big">'+Math.round(o2.proj)+'<small>/200</small></div></div>'+
      '<div><div class="lbl">June 2026 actual</div><div class="big" style="font-size:1.5rem;color:var(--fg3)">'+Math.round(o2.base)+'<small>/200</small></div></div>'+
      '<div><div class="lbl">Your target</div><div class="big" style="font-size:1.5rem;color:var(--ok)">'+t+'<small>/200</small></div></div>'+
      '<div style="margin-left:auto;text-align:right"><div class="lbl">Readiness</div>'+ring(o2.readiness*100,o2.readiness>=.8?"ok":o2.readiness>=.5?"mid":"bad")+'</div>'+
    '</div>'+
    '<div class="gauge"><i style="width:'+cl(pc(o2.proj,200),0,100)+'%"></i>'+
      '<span class="mk" style="left:'+pc(o2.base,200)+'%"></span><span class="mk t" style="left:'+pc(t,200)+'%"></span></div>'+
    '<div class="gmarks"><span style="left:'+pc(o2.base,200)+'%">June: '+Math.round(o2.base)+'</span><span style="left:'+pc(t,200)+'%">target '+t+'</span></div>'+
    '<p class="note" style="margin-top:6px">Projection = Σ (module marks × accuracy), with a thinly-sampled module pulled back toward its June 2026 accuracy ('+SHRINK+' pseudo-attempts). It moves when you answer questions, not when you load them.</p>'+
  '</div>'+
  '<div class="grid g2" style="margin-bottom:12px">'+
    '<div class="card"><div class="lbl">Progress A — self-marked</div>'+
      '<div class="kv" style="margin-top:6px"><span>'+lp.scenes+' of '+lp.scenesTot+' lesson scenes read</span><b>'+pc(lp.scenes,lp.scenesTot)+'%</b></div>'+
      bar(pc(lp.scenes,lp.scenesTot),"och")+
      '<p class="note" style="margin-top:8px">What you have been through. It measures effort, and it is evidence of nothing.</p></div>'+
    '<div class="card"><div class="lbl">Progress B — verified mastery</div>'+
      '<div class="kv" style="margin-top:6px"><span>'+lp.mastered+' of '+lp.withLesson+' topics passed at '+(lp.pass)+'%</span><b>'+pc(lp.mastered,lp.withLesson||1)+'%</b></div>'+
      bar(pc(lp.mastered,lp.withLesson||1),"ok")+
      '<p class="note" style="margin-top:8px">Unseen questions, hints off, format floors met. The dashboard never averages this with the bar on the left.</p></div>'+
  '</div>'+
  '<div class="grid g4" style="margin-bottom:12px">'+
    stat("Questions answered",o2.att+o1.att,"of "+oA.loaded+" in the bank")+
    stat("Accuracy so far",oA.att?fmtPct(oA.acc):"—",oA.cor+" of "+oA.att)+
    stat("Modules green",o2.green+o1.green,"of "+oA.ms.length+" · 80% + a mock")+
    stat("Mocks taken",S.mocks.length,S.mocks.length?("last "+pc(S.mocks[S.mocks.length-1].c,S.mocks[S.mocks.length-1].n)+"%"):"none yet")+
  '</div>'+
  '<div class="card" style="margin-bottom:12px"><div class="kv"><span class="lbl">Paper 2 by weightage — width is marks, colour is status</span><span class="note">click a block</span></div>'+
    stripHTML(o2.ms.slice().sort((a,b)=>(b.m.marks||0)-(a.m.marks||0)))+
    '<div class="row tight" style="margin-top:9px">'+
      '<span class="chip ok">green · 80%+ and a mock to prove it</span><span class="chip mid">in progress</span>'+
      '<span class="chip bad">under 60%</span><span class="chip ac">loaded, untouched</span><span class="chip dim">no content yet</span></div></div>'+
  '<div class="grid g2">'+
    '<div class="card"><h3 style="margin-bottom:8px">Do this next</h3>'+nextAction(o2,lp)+'</div>'+
    '<div class="card"><h3 style="margin-bottom:8px">Your two study modes</h3>'+
      '<div class="trow"><span class="chip och">Alone</span><div class="tn">College desk, or after the children are asleep. Numerical and derivation work — anything needing paper and an uninterrupted twenty minutes.</div></div>'+
      '<div class="trow"><span class="chip ac">With kids</span><div class="tn">Paper in hand while they play, or during house work. Statements, conditions, definitions, match-the-list — theory you can hold in your head and check in one glance.</div></div>'+
      '<p class="note" style="margin-top:8px">Every topic in <b>Learn</b> carries the tag for the mode that suits it, so you can pick by whichever hand you have free.</p></div>'+
  '</div>'+
  settingsCard(d);
}
function learnProgress(){
  const ix=(S.lessonIdx&&S.lessonIdx.topics)||{};
  let scenes=0,scenesTot=0,mastered=0,withLesson=0,ready=0;
  Object.keys(ix).forEach(tid=>{
    withLesson++;scenesTot+=ix[tid].scenes||1;
    scenes+=((S.topics[tid]||{}).seen||[]).length;
    const st=mrec(tid).state;
    if(st==="mastered")mastered++;
    if(st==="ready")ready++;
  });
  return {scenes:scenes,scenesTot:scenesTot||1,mastered:mastered,withLesson:withLesson,ready:ready,pass:80};
}
function stat(l,v,sub){return '<div class="card flat"><div class="lbl">'+esc(l)+'</div><div class="big" style="font-size:1.55rem;margin:3px 0">'+esc(String(v))+'</div><div class="note">'+esc(sub||"")+'</div></div>'}
function stripHTML(ms){
  const tot=ms.reduce((s,x)=>s+(x.m.marks||0),0)||1;
  return '<div class="strip">'+ms.map(x=>{
    const w=100*(x.m.marks||0)/tot;
    return '<button class="s-'+x.st+'" data-go="'+x.m.id+'" style="flex:0 0 '+w.toFixed(2)+'%" title="'+esc(x.m.name+" — "+x.m.marks+" marks")+'">'+(w>7?esc(shortName(x.m))+" "+x.m.marks:x.m.marks)+'</button>'}).join("")+'</div>';
}
function shortName(m){return{inference:"Inference",probability:"Probability",regression:"Regression",stochastic:"Stochastic",timeseries:"Time series",maths:"Maths",multivariate:"Multivariate",rprog:"R",sampling:"Sampling",design:"Design",official:"Official",nonparam:"Nonpar."}[m.id]||m.name}
function nextAction(o2,lp){
  const out=[],ix=(S.lessonIdx&&S.lessonIdx.topics)||{};
  // 1. a lesson part-read
  let resume=null,due=null,totest=null;
  Object.keys(ix).forEach(tid=>{
    const seen=((S.topics[tid]||{}).seen||[]).length,tot=ix[tid].scenes||1,r=mrec(tid);
    if(r.state==="mastered"&&r.retestDue&&r.retestDue<now()&&!due)due=[tid,ix[tid]];
    if(seen>0&&seen<tot&&r.state!=="mastered"&&!resume)resume=[tid,ix[tid],seen,tot];
    if(seen>=tot&&r.state!=="mastered"&&!totest)totest=[tid,ix[tid]];
  });
  if(due)out.push(["Retention retest: "+due[1].title,"You passed this one and the retest is due. Passing once is not the same as still knowing it.","learn",due[0]]);
  if(totest)out.push(["Sit the mastery test for "+totest[1].title,"You have read every scene. Nothing is verified until you answer unseen questions without hints.","learn",totest[0]]);
  if(resume)out.push(["Finish "+resume[1].title,"Scene "+(resume[2]+1)+" of "+resume[3]+". About "+Math.max(5,Math.round(resume[1].estMin*(1-resume[2]/resume[3])))+" minutes left.","learn",resume[0]]);
  const weak=o2.ms.filter(x=>x.loaded>0&&x.att>0&&x.acc<0.6).sort((a,b)=>b.m.marks-a.m.marks);
  const mockDue=o2.ms.filter(x=>x.gAcc&&!x.gMock).sort((a,b)=>b.m.marks-a.m.marks);
  const empty=o2.ms.filter(x=>x.loaded===0).sort((a,b)=>b.m.marks-a.m.marks);
  if(weak[0])out.push(["Drill "+weak[0].m.name,fmtPct(weak[0].acc)+" on "+weak[0].att+" questions — "+weak[0].m.marks+" marks ride on it","bank",weak[0].m.id]);
  if(mockDue[0])out.push(["Mock to turn "+mockDue[0].m.name+" green","Bank accuracy is already past "+mockDue[0].m.passPct+"%. It needs one mock at "+mockDue[0].m.passPct+"%","mock",""]);
  if(!lp.withLesson)out.push(["Author the first lesson","No topic has a lesson yet. Admin generates the prompt that writes one into the store.","admin",""]);
  else if(empty[0])out.push(["Load content for "+empty[0].m.name,empty[0].m.marks+" marks with an empty bank","admin",empty[0].m.id]);
  if(!out.length)out.push(["Take a full mock","Everything loaded has been answered. Sit a 100-question paper at exam pace.","mock",""]);
  return out.slice(0,3).map((a,i)=>'<div class="trow"><span class="chip '+(i?"dim":"och")+' num">'+(i+1)+'</span><div class="tn"><b>'+esc(a[0])+'</b><div class="note">'+esc(a[1])+'</div></div>'+
    '<button class="btn sm" data-jump="'+a[2]+'" data-mid="'+esc(a[3])+'">Go</button></div>').join("");
}
function settingsCard(d){
  return '<div class="card" style="margin-top:12px"><h3 style="margin-bottom:8px">Settings</h3><div class="row" style="gap:14px;align-items:flex-end">'+
    '<div><label class="fl">Exam date</label><input type="date" id="cfgExam" value="'+esc(S.cfg.exam||"")+'"></div>'+
    '<div><label class="fl">Paper 2 target (of 200)</label><input type="number" id="cfgTarget" min="60" max="200" step="2" value="'+target()+'" style="width:88px"></div>'+
    '<button class="btn" id="cfgSave">Save</button>'+
    '<span class="note" style="flex:1;min-width:160px">'+(d===null?"No exam date set, so the page cannot pace you.":"Everything here is per-person and private to your login. Sharing the artifact does not share your scores.")+'</span>'+
  '</div></div>';
}
