/* ===================== learn workspace ===================== */
const MODES={
  syllabus:{n:"Syllabus",d:"The official unit sequence. Complete coverage, no reordering.",tag:"Universal"},
  pyq:{n:"Exam weightage",d:"Heaviest in the June 2026 paper first. Marks at stake decide the order.",tag:"Exam-focused"},
  personal:{n:"Personal",d:"An order imported for you from an analysis of your own answer sheet.",tag:"Adaptive"}
};
const MSTATE={
  notStarted:{n:"Not started",c:"dim"},learning:{n:"Learning",c:"ac"},practising:{n:"Practising",c:"ac"},
  ready:{n:"Ready to test",c:"mid"},mastered:{n:"Mastered",c:"ok"},revisionDue:{n:"Revision due",c:"mid"},
  failed:{n:"Retest needed",c:"bad"}};
const SCENEKIND={
  foundation:{n:"What you need first",i:"⌂"},
  intuition:{n:"The idea in plain words",i:"◍"},explore:{n:"Try it yourself",i:"◈"},theory:{n:"Theory",i:"▤"},
  worked:{n:"Worked example",i:"✎"},completion:{n:"Your turn",i:"◫"},guided:{n:"Problem with help",i:"◎"},
  recall:{n:"Quick recap",i:"↻"},trapcheck:{n:"Common mistakes",i:"⚑"},summary:{n:"Summary",i:"▣"},quiz:{n:"Mastery test",i:"★"}};

/* ---- path ordering ----
   The two papers are different exams with different syllabi, so they are never
   interleaved: a scope picks which paper is on the path, and "both" lists Paper 2
   first and Paper 1 after it, each ordered by the current mode. */
const PAPERS=[2,1];
function paperScope(){return S.paper===1||S.paper===2?S.paper:"all"}
function sortPaper(ms){
  if(S.mode==="syllabus"){
    const hasSyl=ms.some(m=>m.sylOrder!=null);
    return hasSyl?ms.slice().sort((a,b)=>(a.sylOrder==null?99:a.sylOrder)-(b.sylOrder==null?99:b.sylOrder)):ms.slice();
  }
  if(S.mode==="personal"&&S.personal&&S.personal.entries){
    const pr={};S.personal.entries.forEach((e,i)=>{if(pr[e.moduleId]===undefined)pr[e.moduleId]=i});
    return ms.slice().sort((a,b)=>(pr[a.id]===undefined?999:pr[a.id])-(pr[b.id]===undefined?999:pr[b.id]));
  }
  return ms.slice().sort((a,b)=>(b.marks||0)-(a.marks||0));
}
function pathPapers(){const sc=paperScope();return sc==="all"?PAPERS:[sc]}
function pathOrder(){
  let out=[];
  pathPapers().forEach(p=>{out=out.concat(sortPaper(mods(p)))});
  return out;
}
const PAPERN={2:"Paper 2 · Statistics",1:"Paper 1 · General paper"};
/* The scope control. Paper 2 is the default because that is the subject paper. */
function paperPills(){
  const sc=paperScope();
  return '<div class="pills" style="margin-bottom:10px">'+
    [[2,"Paper 2"],[1,"Paper 1"],["all","Both"]].map(x=>
      '<button class="tog" data-paper="'+x[0]+'" aria-pressed="'+(String(sc)===String(x[0]))+'">'+x[1]+
      '<span class="note" style="margin-left:6px">'+
        (x[0]==="all"?300:mods(x[0]).reduce((a,m)=>a+(m.marks||0),0))+'m</span></button>').join("")+
    '</div>';
}
function topicOrder(m){
  if(S.mode==="personal"&&S.personal&&S.personal.entries){
    const pr={};S.personal.entries.forEach((e,i)=>{pr[e.topicId]=i});
    return m.topics.slice().sort((a,b)=>(pr[a.id]===undefined?999:pr[a.id])-(pr[b.id]===undefined?999:pr[b.id]));
  }
  return m.topics;
}
function personalNote(t){
  if(S.mode!=="personal"||!S.personal||!S.personal.entries)return"";
  const e=S.personal.entries.find(x=>x.topicId===t.id);
  return e&&e.reason?e.reason:"";
}
function lessonFor(tid){const ix=(S.lessonIdx&&S.lessonIdx.topics)||{};return ix[tid]||null}
function mrec(tid){
  const r=S.mastery[tid];
  if(!r)return{state:"notStarted"};
  // a pass that is past its retention date is not a current pass
  if(r.state==="mastered"&&r.retestDue&&r.retestDue<now())
    return Object.assign({},r,{state:"revisionDue"});
  return r;
}
function selfPct(tid){
  const L=S.lessons[tid];const st=S.topics[tid]||{};
  if(st.done||st.s===2)return 100;
  if(!L||!L.scenes)return st.s===1?25:0;
  const seen=(st.seen||[]).length;return pc(seen,L.scenes.length);
}
/* "Done" is the user's own mark, separate from the verified mastery record. */
function isDone(tid){const st=S.topics[tid]||{};return !!st.done}
function topicOf(tid){let f=null;mods().forEach(m=>m.topics.forEach(t=>{if(t.id===tid)f=t}));return f}
function impOf(tid){const t=topicOf(tid);return IMP[(t&&t.imp)||2]}
function setDone(tid,on){
  const st=S.topics[tid]||(S.topics[tid]={s:0,seen:[]});
  if(on){st.done=1;st.doneT=now();st.s=2;
    const les=S.lessons[tid];
    if(les&&les.scenes){st.seen=les.scenes.map(x=>x.id);
      // only touch the live session's map when it is this topic that is open
      if(S.learn.topicId===tid){S.learn.seen={};st.seen.forEach(id=>{S.learn.seen[id]=1})}}}
  else{delete st.done;delete st.doneT;st.s=(st.seen||[]).length?1:0}
  st.t=now();saveTopics();render();
}
function resetTopic(tid){
  const st=S.topics[tid]||(S.topics[tid]={});
  st.seen=[];st.s=0;delete st.done;delete st.doneT;st.t=now();
  if(S.learn.topicId===tid)S.learn.seen={};
  saveTopics();render();
  toast("Reading progress cleared. The mastery record is kept — reset it separately if you mean to.");
}
function toggleSeen(tid,sid){
  const st=S.topics[tid]||(S.topics[tid]={s:0,seen:[]});
  st.seen=st.seen||[];
  const i=st.seen.indexOf(sid);
  if(i<0){st.seen.push(sid);S.learn.seen[sid]=1}
  else{st.seen.splice(i,1);delete S.learn.seen[sid];delete st.done;delete st.doneT}
  const les=S.lessons[tid];
  st.s=st.done?2:(les&&st.seen.length>=les.scenes.length?2:(st.seen.length?1:0));
  st.t=now();saveTopics();render();
}

/* ---- the workspace ---- */
function vLearn(){
  const g=gate();if(g)return g;
  const L=S.learn;
  let centre;
  if(!L.topicId)centre=welcomePane();
  else{
    const les=S.lessons[L.topicId];
    if(les===undefined){kickLoad(L.topicId);centre=loadingPane()}
    else if(les===null)centre=loadingPane();          // read in flight — not "absent"
    else if(!les)centre=noLessonPane(L.topicId);
    else centre=L.quiz?quizPane():scenePane();
  }
  const les=L.topicId&&S.lessons[L.topicId];
  const inLesson=!!(les&&les.scenes);
  const sty='--navw:'+S.navW+'px;--aidew:'+S.aideW+'px';
  return '<div class="ws'+(S.navOpen?"":" navhid")+(S.aideOpen?"":" aidehid")+'" style="'+sty+'">'+
    '<aside class="wsnav">'+(inLesson?stepperHTML(les):treeHTML())+'</aside>'+
    '<div class="grip gl" data-grip="nav" title="Drag to resize · double-click to collapse"></div>'+
    '<div class="wscanvas">'+centre+'</div>'+
    '<div class="grip gr" data-grip="aide" title="Drag to resize · double-click to collapse"></div>'+
    '<aside class="wsaide">'+aideHTML()+'</aside>'+
    (S.navOpen?"":'<button class="edge el" data-nav-toggle="1" title="Show the contents panel">›</button>')+
    (S.aideOpen?"":'<button class="edge er" data-aide="1" title="Show the aids panel">‹</button>')+
  '</div>';
}
/* The rail turns into the lesson's own contents once a lesson is open: every scene
   is reachable directly, instead of only by pressing continue. */
function stepperHTML(les){
  const L=S.learn,tot=les.scenes.length;
  const seen=les.scenes.filter(x=>L.seen[x.id]).length;
  const r=mrec(les.topicId),tid=les.topicId,done=isDone(tid),imp=impOf(tid),tp=topicOf(tid);
  const cur=L.quiz?tot-1:L.i;
  return '<div class="raill">'+
    '<div class="railhd">'+
      '<button class="btn sm gh" data-alltopics="1" title="Back to every topic">‹ All topics</button>'+
      '<button class="btn sm gh" data-nav-toggle="1" title="Hide the panel">✕</button>'+
    '</div>'+
    '<div class="railttl">'+
      '<b>'+nTag(topNo(les.topicId),"h")+esc(les.title)+'</b>'+
      '<div class="railmeta">'+
        '<span class="chip '+imp.c+'" title="'+esc(imp.d)+'">'+imp.s+' '+imp.n+'</span>'+
        (tp&&tp.qs?'<span class="chip dim num" title="Expected questions on this topic in one paper">~'+tp.qs+' q · '+tp.marks+' marks</span>':"")+
      '</div>'+
      '<div class="railmeta">'+
        '<span class="chip '+(done?"ok":MSTATE[r.state].c)+'">'+(done?"✓ Marked done":MSTATE[r.state].n)+'</span>'+
        '<span class="note num">'+seen+'/'+tot+'</span>'+
        (notesForTopic(tid)?'<span class="chip ac">✎ '+notesForTopic(tid)+' notes</span>':"")+'</div>'+
      '<div class="rbar"><i style="width:'+pc(seen,tot)+'%"></i></div>'+
      '<div class="railacts">'+
        '<button class="btn sm'+(done?" g":"")+'" data-done="'+tid+'" data-on="'+(done?0:1)+'">'+
          (done?"Unmark":"Mark lesson done")+'</button>'+
        '<button class="btn sm gh" data-resettopic="'+tid+'" title="Clear every tick on this lesson">Reset</button>'+
      '</div>'+
    '</div>'+
    '<div class="railsteps">'+
    '<div class="steprow'+(cur<0?" cur":"")+'"><span class="snode ov">◇</span>'+
      '<button class="step" data-sc="-99"><span class="stx"><b>Lesson overview</b>'+
      '<span class="note">objectives, route, sources</span></span></button></div>'+
    les.scenes.map((x,k)=>{
      const on=k===cur,sdone=!!L.seen[x.id];
      return '<div class="steprow'+(on?" cur":"")+(sdone?" done":"")+(x.kind==="quiz"?" test":"")+'">'+
        '<button class="snode" data-seen="'+tid+'|'+x.id+'" '+
          'title="'+(sdone?"Mark this section unread":"Mark this section read")+'" '+
          'aria-pressed="'+sdone+'">'+(sdone?"✓":(x.kind==="quiz"?"★":(k+1)))+'</button>'+
        '<button class="step" data-sc="'+k+'" aria-current="'+(on?"step":"false")+'">'+
          '<span class="stx"><b>'+esc(x.title)+(noteOf(tid,x.id)?' <span class="noteflag" title="You have a note here">✎</span>':'')+'</b>'+
            '<span class="note">'+esc(SCENEKIND[x.kind].n)+(x.mins?' · '+x.mins+' min':'')+
            (x.ext?' · <b class="extw">✦ optional</b>':'')+
            (x.exam?' · <b class="xw">'+IMP[x.exam].s+'</b>':'')+'</span>'+
          '</span></button></div>'}).join("")+'</div>'+
    (r.best!=null?'<p class="railfoot">Best mastery score '+r.best+'%. Needs '+les.mastery.pass+'% to turn green.</p>'
                 :'<p class="railfoot">The mastery test at the end is what turns this topic green.</p>')+
  '</div>';
}
function treeHTML(){
  const order=pathOrder();
  const m=MODES[S.mode];
  return '<div class="navtop">'+
    '<div class="row tight" style="justify-content:space-between"><span class="lbl">Learning path</span>'+
      '<button class="btn sm" data-nav-toggle="1">close ✕</button></div>'+
    paperPills()+
    '<div class="pills" style="margin:8px 0 4px">'+Object.keys(MODES).map(k=>
      '<button class="tog" data-mode="'+k+'" aria-pressed="'+(S.mode===k)+'">'+MODES[k].n+'</button>').join("")+'</div>'+
    '<p class="note">'+esc(m.d)+'</p>'+
    '<p class="note" style="margin-top:4px">Numbers follow the '+numSrc()+
      ' and stay with a topic whichever order you study in.</p>'+
    (S.mode==="syllabus"&&!mods().some(x=>x.sylOrder!=null)?
      '<p class="note" style="color:var(--ochre)">The official unit order has not been imported, so this falls back to the catalog order. Admin → Content factory has the prompt that loads it.</p>':"")+
    (S.mode==="personal"&&!S.personal?
      '<p class="note" style="color:var(--ochre)">No personal order imported yet. Admin → Personal order takes the analysis file.</p>':"")+
  '</div>'+
  '<div class="navlist">'+order.map((mo,oi)=>{
    const head=(paperScope()==="all"&&(oi===0||order[oi-1].paper!==mo.paper))
      ? '<div class="paperhd">'+PAPERN[mo.paper]+'</div>' : "";
    const open=!!S.open[mo.id],ts=topicOrder(mo);
    const done=ts.filter(t=>mrec(t.id).state==="mastered").length;
    const withL=ts.filter(t=>lessonFor(t.id)).length;
    return head+'<div class="navmod">'+
      '<button class="navmh" data-mod="'+mo.id+'" aria-expanded="'+open+'">'+
        '<span class="caret">▶</span>'+nTag(modNo(mo.id),"mn")+'<span class="nm">'+esc(mo.name)+'</span>'+
        '<span class="chip '+(done?"ok":"dim")+' num" title="'+(unitOf(mo.id)?'Unit '+unitOf(mo.id).no+' — '+esc(unitOf(mo.id).title):'')+'">'+done+'/'+ts.length+'</span></button>'+
      (open?'<div class="navtp">'+ts.map(t=>{
        const r=mrec(t.id),has=lessonFor(t.id),sp=selfPct(t.id);
        const imp=IMP[t.imp||2],done=isDone(t.id);
        return '<button class="navt'+(S.learn.topicId===t.id?" cur":"")+(done?" done":"")+'" data-topic="'+t.id+'">'+
          '<span class="tdot '+(done?"ok":MSTATE[r.state].c)+'">'+(done?"✓":"")+'</span>'+
          '<span class="tn">'+nTag(topNo(t.id))+esc(t.name)+
            '<span class="trow2"><span class="chip '+imp.c+'" title="'+esc(imp.n+" — "+imp.d)+'">'+imp.s+'</span>'+
            (t.qs?'<span class="note num" title="Expected questions on this topic in one paper">~'+t.qs+' q</span>':"")+
            '<span class="chip '+EXT[t.extent].c+'">'+t.extent+'</span>'+
            (has?"":'<span class="chip dim">no lesson</span>')+
            (sp?'<span class="note num">'+sp+'%</span>':"")+
            (notesForTopic(t.id)?'<span class="chip ac">✎ '+notesForTopic(t.id)+'</span>':"")+'</span></span></button>'}).join("")+
        (withL?"":'<p class="note" style="padding:4px 8px 8px">No lessons loaded for this module yet.</p>')+
      '</div>':"")+
    '</div>'}).join("")+'</div>';
}
function aideHTML(){
  const L=S.learn,les=L.topicId&&S.lessons[L.topicId];
  if(!les)return aideStub();
  const sc=les.scenes[L.i],used=L.hints[sc&&sc.id]||0;
  return '<div class="aidein">'+
    '<div class="aidehd"><span class="lbl">Formula sheet</span>'+
      '<button class="btn sm gh" data-aide="0" title="Hide this panel">✕</button></div>'+
    '<div class="drawer">'+les.revision.sheet.slice(0,7).map(x=>'<div class="dr">'+richText(x)+'</div>').join("")+'</div>'+
    notePane(les,sc)+
    tricksHTML(les,sc)+
    (used?'<div class="sep"></div><p class="note"><b>'+used+' hint'+(used>1?"s":"")+'</b> opened on this scene. The mastery test records that practice was assisted.</p>':"")+
    '<div class="sep"></div>'+
    askBox("ask-aide","Ask about this scene",
      "You are tutoring a UGC NET Statistics candidate at JRF level, inside a lesson on "+les.title+". "+
      "The scene in front of them is: "+(sc?sc.title:"")+". Their learning objective here is: "+(sc&&sc.objective||les.objectives[0])+".\n\n"+
      "They have asked for help. Do NOT give a full worked solution. Give the smallest nudge that would let them continue by themselves: name the quantity to identify, or the condition to check, or the one line of algebra that unlocks it. Under 90 words, plain text.","quick")+
    '<div class="sep"></div>'+
    '<div class="lbl">Sources for this topic</div>'+
    les.refs.map(r=>r.url
      ?'<a class="refl" href="'+esc(r.url)+'" target="_blank" rel="noopener">'+esc(r.site)+' — '+esc(r.where)+'</a>'
      :'<span class="refl book">'+esc(r.site)+' — '+esc(r.where)+'</span>').join("")+
  '</div>';
}
/* Memory aids. A lesson may carry its own; otherwise the panel offers to make them. */
function tricksHTML(les,sc){
  const rv=les.revision||{},tr=rv.tricks||[],sh=rv.shortcuts||[],rem=rv.remember||[];
  const any=tr.length||sh.length||rem.length;
  return '<div class="sep"></div><div class="lbl">Things that help you remember</div>'+
    (tr.length?'<div class="aidsec"><span class="asl">Ways to remember</span>'+
      tr.map(x=>'<div class="trick"><b>'+richText(x.hook||x.n||"")+'</b><span>'+richText(x.why||x.d||"")+'</span></div>').join("")+'</div>':"")+
    (sh.length?'<div class="aidsec"><span class="asl">Shortcuts</span>'+
      sh.map(x=>'<div class="dr sc">'+richText(typeof x==="string"?x:(x.n||""))+'</div>').join("")+'</div>':"")+
    (rem.length?'<div class="aidsec"><span class="asl">Must remember</span>'+
      rem.map(x=>'<div class="dr key">'+richText(x)+'</div>').join("")+'</div>':"")+
    (any?"":'<p class="note">No memory tricks written for this topic yet.</p>')+
    askBox("ask-tricks","Make me a memory hook for this section",
      "You are helping a UGC NET Statistics (JRF) candidate memorise material in a lesson on "+les.title+". "+
      "The section in front of them is \""+(sc?sc.title:les.title)+"\"."+
      (sc&&sc.objective?" Its objective: "+sc.objective:"")+"\n\n"+
      "Give at most three memory aids for THIS section only: a mnemonic or acronym, a one-line rule of thumb, "+
      "and a 'if you remember nothing else' line. Each under 20 words. Do not restate the theory. Plain text, no preamble.","quick")+
    '<div class="sep"></div>'+reqBox(les,sc);
}
/* The request modal: what it is for, said plainly, with attachments. */
function reqModal(){
  const m=S.reqModal;if(!m)return"";
  const les=S.lessons[S.learn.topicId];
  const sc=les&&S.learn.i>=0?les.scenes[S.learn.i]:null;
  const where=les?(esc(les.title)+(sc?" \u2014 "+esc(sc.title):" \u2014 whole lesson")):"General";
  const files=m.files||[];
  return '<div class="modalwrap" data-reqclose="1">'+
   '<div class="modal" role="dialog" aria-modal="true" aria-label="Ask for more on this section">'+
    '<div class="modalhd"><b>Ask for more on this section</b>'+
      '<button class="btn sm gh" data-reqclose="1" title="Close">\u2715</button></div>'+
    '<div class="modalbody">'+
      '<p class="modalwhy">This does not change the app now. It writes down exactly what you asked for, '+
        'against the section you were reading, and files it under <b>Admin \u2192 Requests</b>. '+
        'When content is next authored \u2014 in this chat or another one \u2014 that list is the brief: '+
        'it is copied in wholesale so nothing you asked for is forgotten. Attach a question paper, '+
        'an assignment or a photo of a page and it is logged with the request.</p>'+
      '<div class="kv" style="margin:10px 0 4px"><span>Section</span><b>'+where+'</b></div>'+
      '<label class="fl" style="margin-top:10px">What kind of thing do you want?</label>'+
      '<div class="row tight" style="margin-bottom:10px">'+
        REQKIND.map(k=>'<button class="tog" data-reqkind="'+k[0]+'" aria-pressed="'+((m.kind||"detail")===k[0])+'">'+k[1]+'</button>').join("")+'</div>'+
      '<label class="fl">Say what is missing, or what would help</label>'+
      '<textarea id="reqText" placeholder="For example: I cannot follow the step where the indicator moves into g \u2014 can you show it on a second family? Or: here is last year\u2019s assignment, please build practice from Q3 and Q7.">'+esc(m.text||"")+'</textarea>'+
      '<label class="fl" style="margin-top:12px">Attach anything that explains it (optional)</label>'+
      '<input type="file" id="reqFiles" multiple accept="image/*,.pdf,.txt,.md,.csv,.docx">'+
      (files.length?'<div class="filelist">'+files.map((f,i)=>
        '<div class="filerow"><span class="fn2">'+esc(f.name)+'</span>'+
          '<span class="note num">'+Math.round(f.size/1024)+' KB</span>'+
          (f.kept?'<span class="chip ok">stored</span>':'<span class="chip dim" title="Too large to keep inside the app; the name and size are logged">logged only</span>')+
          '<button class="btn sm gh" data-reqfiledel="'+i+'">\u2715</button></div>').join("")+'</div>':"")+
      '<p class="note" style="margin-top:8px">Files under 400 KB are stored with the request so they can be read back later. Anything larger is recorded by name and size only \u2014 keep the original.</p>'+
    '</div>'+
    '<div class="modalft">'+
      '<button class="btn" data-reqclose="1">Cancel</button><span class="sp"></span>'+
      '<button class="btn p" id="reqSend">Send the request</button></div>'+
   '</div></div>';
}
/* Ask for more material on any section. Requests are stored for later review. */
function reqBox(les,sc){
  const n=(S.reqs||[]).length;
  return '<div class="reqbox">'+
    '<div class="lbl">Ask for more on this section</div>'+
    '<p class="note" style="margin:5px 0 8px">Tell me what is missing and attach anything that explains it. '+
      'It is filed against this exact section for the next content update.</p>'+
    '<button class="btn p sm" data-reqopen="1">Open the request form</button>'+
    (n?'<p class="note" style="margin-top:7px">'+n+' request'+(n>1?"s":"")+' already filed \u00b7 Admin \u2192 Requests</p>':"")+
  '</div>';
}
function reqBoxOld(les,sc){
  const key=(les?les.topicId:"general")+"|"+(sc?sc.id:"overview");
  const st=(S.reqUI||{})[key]||{};
  return '<div class="reqbox">'+
    '<div class="lbl">Ask for more on this section</div>'+
    (st.sent?'<p class="note" style="color:var(--ok)">Request saved. It appears under Admin → Requests for review, and can be built into the next content update.</p>'+
      '<button class="btn sm" data-reqnew="'+esc(key)+'">Ask for something else</button>'
     :'<div class="row tight" style="margin:7px 0">'+
        REQKIND.map(k=>'<button class="tog" data-reqk="'+esc(key)+'|'+k[0]+'" aria-pressed="'+((st.kind||"detail")===k[0])+'">'+k[1]+'</button>').join("")+
      '</div>'+
      '<textarea id="reqText" placeholder="What is missing, or what would help? A screenshot description works too."></textarea>'+
      '<div class="row tight" style="margin-top:7px">'+
        '<button class="btn p sm" data-reqsend="'+esc(key)+'">Send the request</button>'+
        '<span class="note">Stored in your workspace, not sent anywhere.</span></div>')+
  '</div>';
}
function aideStub(){
  return '<div class="aidein"><div class="lbl">Assistance</div>'+
    '<p class="note">Open a topic and this panel carries its formula drawer, the tutor and the sources.</p></div>';
}
/* The landing page carries the whole module map itself, so it still works with the
   side panels closed — the rail is a convenience, never the only way to navigate. */
function welcomePane(){
  const order=pathOrder();
  /* The suggestion has to agree with the path on screen. In syllabus or personal mode
     that is the first unfinished topic in the order being shown — including one with no
     lesson yet, because silently jumping to the first topic that happens to have content
     makes the path look as though it starts at Unit IV. Weightage mode is the one that
     ranks by marks, and there only an authored topic can be suggested. */
  const all=[];order.forEach(m=>topicOrder(m).forEach(t=>all.push([m,t])));
  const left=all.filter(([m,t])=>mrec(t.id).state!=="mastered"&&!isDone(t.id));
  const authored=left.filter(([m,t])=>lessonFor(t.id));
  const nextUp=(S.mode==="pyq"
    ? authored.slice().sort((a,b)=>((b[1].imp||2)-(a[1].imp||2)))[0]
    : left[0]) || authored[0];
  const nextHas=nextUp?!!lessonFor(nextUp[1].id):false;
  // when the next topic in order has no lesson, name the first one that does
  const firstAuthored=(!nextHas&&authored.length)?authored[0]:null;
  return '<div class="pane">'+
    paperPills()+
    '<div class="pills" style="margin-bottom:14px">'+
      '<span class="chip ac">'+esc(MODES[S.mode].tag)+'</span>'+
      Object.keys(MODES).map(k=>'<button class="tog" data-mode="'+k+'" aria-pressed="'+(S.mode===k)+'">'+MODES[k].n+'</button>').join("")+
    '</div>'+
    '<h1>Learning workspace</h1>'+
    '<p class="lead">'+esc(MODES[S.mode].d)+'</p>'+
    (nextUp?'<div class="nextup"><div>'+
       '<div class="lbl">Next in this path · '+(S.mode==="syllabus"?"first unfinished in unit order"
         :S.mode==="personal"?"first unfinished in your order":"heaviest topic left")+'</div>'+
       '<b>'+nTag(topNo(nextUp[1].id),"h")+esc(nextUp[1].name)+'</b>'+
       '<div class="note">'+esc(nextUp[0].name)+' · '+IMP[nextUp[1].imp||2].s+' '+IMP[nextUp[1].imp||2].n+
         (nextUp[1].qs?' · ~'+nextUp[1].qs+' questions a paper':'')+'</div>'+
       (nextHas?"":'<div class="note" style="margin-top:6px;color:var(--ochre)">'+
          'No lesson authored for this topic yet'+
          (firstAuthored?' — the first one with a lesson is '+topNo(firstAuthored[1].id)+' '+esc(firstAuthored[1].name):'')+
        '</div>')+'</div>'+
       (nextHas
         ?'<button class="btn p" data-topic="'+nextUp[1].id+'">Start learning ›</button>'
         :(firstAuthored?'<button class="btn p" data-topic="'+firstAuthored[1].id+'">Start '+topNo(firstAuthored[1].id)+' instead ›</button>':""))+
     '</div>':"")+
    '<div class="sep"></div>'+
    '<div class="row tight" style="justify-content:space-between;margin-bottom:10px">'+
      '<span class="lbl">'+(paperScope()==="all"?"Both papers"
          :(paperScope()===2?"Paper 2 — Statistics":"Paper 1 — general paper"))+
        ', '+(S.mode==="syllabus"?"in syllabus order":S.mode==="personal"?"in your order":"heaviest first")+'</span>'+
      '<span class="note num">'+all.filter(([m,t])=>lessonFor(t.id)).length+' of '+
        order.reduce((n,m)=>n+m.topics.length,0)+' topics have a lesson</span></div>'+
    '<div class="modgrid">'+order.map((m,oi)=>
      ((paperScope()==="all"&&(oi===0||order[oi-1].paper!==m.paper))
        ? '<div class="paperhd">'+PAPERN[m.paper]+'</div>' : "")+modCard(m)).join("")+'</div>'+
  '</div>';
}
function modCard(m){
  const ts=topicOrder(m);
  const withL=ts.filter(t=>lessonFor(t.id));
  const done=ts.filter(t=>mrec(t.id).state==="mastered").length;
  const read=ts.filter(t=>isDone(t.id)).length;
  const open=!!S.open[m.id];
  return '<div class="modcard'+(open?" open":"")+'">'+
    '<button class="modhd" data-mod="'+m.id+'" aria-expanded="'+open+'">'+
      '<span class="caret">▶</span>'+
      '<span class="mh"><b>'+nTag(modNo(m.id),"mn")+esc(m.name)+'</b>'+
        '<span class="note">'+(unitOf(m.id)?'Unit '+unitOf(m.id).no+' · ':'')+'Paper '+m.paper+' · '+m.marks+' marks · '+ts.length+' topics · '+withL.length+' with a lesson</span></span>'+
      '<span class="modstat"><span class="chip '+(done?"ok":"dim")+' num">'+done+'/'+ts.length+'</span></span>'+
    '</button>'+
    '<div class="rbar" style="margin:0 13px 11px"><i style="width:'+pc(done,ts.length)+'%"></i></div>'+
    (open?'<div class="modtopics">'+ts.map(t=>{
      const has=lessonFor(t.id),r=mrec(t.id),imp=IMP[t.imp||2],fin=isDone(t.id);
      return '<button class="mtrow'+(has?"":" nolesson")+'" '+(has?'data-topic="'+t.id+'"':'disabled')+'>'+
        '<span class="mtick'+(fin?" on":"")+'">'+(fin?"✓":"")+'</span>'+
        '<span class="mtn"><b>'+nTag(topNo(t.id))+esc(t.name)+'</b>'+
          '<span class="note">'+imp.s+' '+imp.n+(t.qs?' · ~'+t.qs+' q · '+t.marks+' marks':'')+' · '+t.extent+'</span></span>'+
        '<span class="mtend">'+(has?'<span class="chip '+MSTATE[r.state].c+'">'+MSTATE[r.state].n+'</span>'
                                   :'<span class="chip dim">no lesson</span>')+'</span>'+
      '</button>'}).join("")+'</div>':"")+
  '</div>';
}
const KICKED={};
function kickLoad(tid){
  if(KICKED[tid])return;KICKED[tid]=1;
  setTimeout(()=>{loadLesson(tid).then(()=>{delete KICKED[tid];if(S.route==="learn")render()})},0);
}
function loadingPane(){
  return '<div class="pane"><div class="sk" style="width:50%;height:22px"></div>'+
    '<div class="sk" style="margin-top:12px"></div><div class="sk" style="margin-top:8px;width:80%"></div>'+
    '<p class="note" style="margin-top:14px">Fetching the lesson from the store…</p></div>';
}
function noLessonPane(tid){
  let topic=null,mod=null;
  mods().forEach(m=>m.topics.forEach(t=>{if(t.id===tid){topic=t;mod=m}}));
  if(!topic)return '<div class="pane"><div class="empty"><h3>Topic not found</h3></div></div>';
  return '<div class="pane">'+
    '<button class="btn sm" data-nav-toggle="1" style="margin-bottom:10px">'+(S.navOpen?"‹ hide path":"☰ path")+'</button>'+
    '<h1>'+esc(topic.name)+'</h1>'+
    '<p class="lead">'+esc(mod.name)+' · depth required: <b>'+topic.extent+'</b> — '+esc(EXT[topic.extent].d)+'.</p>'+
    diagBanner(tid)+
    '<div class="row"><button class="btn p" data-jump="admin" data-mid="'+mod.id+'">Get the authoring prompt</button>'+
      '<button class="btn" data-drillmod="'+mod.id+'">Practise this module instead</button></div>'+
    '<div class="sep"></div><div class="lbl">Self-marked progress</div>'+
    '<p class="note">Until a lesson exists you can still record your own reading against this topic.</p>'+
    '<div class="st3" style="margin-top:6px"><button data-tp="'+topic.id+'" data-s="0" aria-pressed="'+(((S.topics[topic.id]||{}).s||0)===0)+'">not started</button>'+
      '<button data-tp="'+topic.id+'" data-s="1" aria-pressed="'+(((S.topics[topic.id]||{}).s||0)===1)+'">learning</button>'+
      '<button class="d" data-tp="'+topic.id+'" data-s="2" aria-pressed="'+(((S.topics[topic.id]||{}).s||0)===2)+'">read it</button></div>'+
  '</div>';
}

/* ---- the scene engine ---- */
function scenePane(){
  const L=S.learn,les=S.lessons[L.topicId];
  if(L.i<0)return overviewPane(les);
  const sc=les.scenes[L.i];
  const body={foundation:scFoundation,intuition:scIntuition,explore:scExplore,theory:scTheory,worked:scWorked,recall:scRecall,
    completion:scCompletion,guided:scGuided,trapcheck:scTrapcheck,summary:scSummary,quiz:scQuizIntro}[sc.kind];
  const tot=les.scenes.length,nxt=les.scenes[L.i+1];
  return '<div class="pane">'+
    '<div class="scbar">'+
      '<button class="btn sm gh" data-nav-toggle="1" title="'+(S.navOpen?"Hide the contents":"Show the contents")+'">'+
        '☰<span class="hidenarrow">'+(S.navOpen?'':' Contents')+'</span></button>'+
      '<span class="crumb">'+nTag(topNo(L.topicId))+esc(les.title)+'</span>'+
      '<span class="sp"></span>'+
      '<span class="scount num">'+(L.i+1)+' / '+tot+'</span>'+
      '<button class="btn sm gh" data-askopen="1" title="Ask Claude about this section (Ctrl/Cmd-K)">✦ Ask Claude</button>'+
      '<button class="btn sm gh" data-reqopen="1" title="Request more written content on this section">+ Request</button>'+
      (S.aideOpen?"":'<button class="btn sm gh" data-aide="1" title="Show the assistance panel">✦</button>')+
      '<button class="btn sm gh" data-sc="-99" title="Leave the lesson">✕</button>'+
      '<i class="scprog" style="width:'+pc(L.i+1,tot)+'%"></i>'+
    '</div>'+
    '<div class="schead"><span class="chip och">'+SCENEKIND[sc.kind].i+' '+SCENEKIND[sc.kind].n+'</span>'+
      (sc.mins?'<span class="chip dim">'+sc.mins+' min</span>':"")+
      (sc.ext?'<span class="chip ext">✦ JRF extension · optional</span>':"")+'</div>'+
    '<h1>'+esc(sc.title)+'</h1>'+
    (sc.objective?'<p class="lead">'+richText(sc.objective)+'</p>':"")+
    (sc.ext?'<div class="expl och"><h4>Optional — come back to this</h4>'+
       'This section is beyond what a pass requires. It is here because JRF is decided by the '+
       'harder theory questions. Skipping it still completes the topic, and the lesson will not '+
       'count it against you.</div>':"")+
    body(sc,les)+
    (sc.table?tableHTML(sc.table):"")+
    askPane(sc)+
    suggestAskHTML(sc)+
    scenarioHTML(sc)+
    '<div class="scnav">'+
      (L.i>0?'<button class="btn" data-sc="'+(L.i-1)+'">‹ Back</button>':'<button class="btn" data-sc="-99">‹ Overview</button>')+
      '<span class="sp"></span>'+
      (nxt?'<button class="btn p" data-sc="'+(L.i+1)+'"><span class="cnx">Next · '+esc(nxt.title)+'</span><span class="cnb">Continue</span> ›</button>'
        :'<button class="btn p" data-sc="-99">Finish ›</button>')+
    '</div>'+
  '</div>';
}
function overviewPane(les){
  const tid=les.topicId,r=mrec(tid),st=S.topics[tid]||{};
  const seen=(st.seen||[]).length,tot=les.scenes.length;
  const pol=les.mastery;
  return '<div class="pane">'+
    '<div class="row tight" style="margin-bottom:10px">'+
      '<button class="btn sm" data-nav-toggle="1">'+(S.navOpen?"‹ hide path":"☰ path")+'</button>'+
      unitTag(les.moduleId)+'<span class="chip dim">'+esc(les.breadcrumb)+'</span>'+
      '<span class="chip '+MSTATE[r.state].c+'">'+MSTATE[r.state].n+'</span>'+
      '<span class="sp"></span>'+
      '<button class="btn sm" data-askopen="1" title="Ask Claude about this topic">✦ Ask Claude</button>'+
      '<button class="btn sm" data-reqopen="1" title="Request more written content">+ Ask for more</button></div>'+
    '<h1>'+nTag(topNo(tid),"h")+esc(les.title)+'</h1>'+
    '<p class="lead">'+tot+' sections, about '+les.estMin+' minutes. '+esc(les.engineName)+'.</p>'+
    extNote(les)+
    (les.howto?'<div class="expl"><h4>How to use this lesson</h4>'+esc(les.howto)+'</div>':"")+
    // the start action sits above everything else on the page — it is what the page is for
    startBlock(les,tid,seen,tot)+
    '<div class="grid g2" style="margin:14px 0">'+
      '<div class="card flat"><div class="lbl">Progress A — self-marked</div>'+
        '<div class="kv" style="margin-top:4px"><span>sections read</span><b>'+seen+' / '+tot+'</b></div>'+bar(pc(seen,tot),isDone(tid)?"ok":"och",true)+
        '<p class="note" style="margin-top:6px">What you have been through. Useful for planning, and no evidence of anything.</p>'+
        '</div>'+
      '<div class="card flat"><div class="lbl">Progress B — verified</div>'+
        '<div class="kv" style="margin-top:4px"><span>best mastery score</span><b>'+(r.best!=null?r.best+"%":"—")+'</b></div>'+
        bar(r.best||0,(r.best||0)>=pol.pass?"ok":"bad",true)+
        '<p class="note" style="margin-top:6px">Unseen questions, no hints. This is the number that counts.</p></div>'+
    '</div>'+
    weightCard(tid)+
    '<div class="card" style="margin-bottom:12px"><div class="lbl">What you will be able to do</div>'+
      '<ol class="obj">'+les.objectives.map(o=>'<li>'+richText(o)+'</li>').join("")+'</ol></div>'+
    '<div class="grid g2" style="margin-bottom:12px">'+
      '<div class="card"><div class="lbl">Before you start</div>'+
        les.prereq.map(p=>'<div class="trow"><div class="tn"><b>'+esc(p.name)+'</b><div class="note">'+richText(p.why)+'</div></div></div>').join("")+
        '<p class="note" style="margin-top:8px">If any of these is shaky the lesson will be twice as slow. Scene 1 does not assume them, but scene 7 does.</p></div>'+
      '<div class="card"><div class="lbl">Passing this topic</div>'+
        '<div class="trow"><div class="tn">'+pol.minQ+' unseen questions, '+pol.pass+'% overall</div></div>'+
        Object.keys(pol.fmtMin).map(f=>'<div class="trow"><div class="tn">'+esc(FMT[f]?FMT[f].n:f)+' at least '+pol.fmtMin[f]+'%</div></div>').join("")+
        '<div class="trow"><div class="tn">No hints during the test</div></div>'+
        '<div class="trow"><div class="tn">Retention retest after '+pol.retestDays+' days</div></div>'+
        '<p class="note" style="margin-top:8px">'+esc(pol.note)+'</p></div>'+
    '</div>'+
    '<div class="card" style="margin-bottom:12px"><div class="lbl">The route through</div>'+
      '<div class="scenelist">'+les.scenes.map((x,k)=>
        '<div class="scrow'+(L_seen(x.id)?" seen":"")+'">'+
          '<button class="sctick" data-seen="'+tid+'|'+x.id+'" aria-pressed="'+!!L_seen(x.id)+'" '+
            'title="'+(L_seen(x.id)?"Mark unread":"Mark read")+'">'+(L_seen(x.id)?"✓":(k+1))+'</button>'+
          '<button class="scopen" data-sc="'+k+'">'+
            '<span class="sck">'+SCENEKIND[x.kind].i+'</span>'+
            '<span class="sct"><b>'+esc(x.title)+(x.ext?' <span class="chip ext sm2">✦ optional</span>':'')+'</b>'+
              '<span class="note">'+SCENEKIND[x.kind].n+(x.mins?" · "+x.mins+" min":"")+
              (x.exam?' · <b class="xw">'+IMP[x.exam].s+'</b>':'')+'</span></span></button>'+
        '</div>').join("")+'</div></div>'+
    '<div class="row" style="margin-bottom:14px">'+
      '<button class="btn" data-revsheet="1">Revision sheet</button>'+
      '<button class="btn gh" data-resettopic="'+tid+'">Reset my ticks</button></div>'+
    (S.learn.showRev?revSheetHTML(les):"")+
    '<div class="card"><div class="lbl">Verified sources for this topic</div>'+
      les.refs.map(r=>'<div class="refrow">'+
        (r.url?'<a href="'+esc(r.url)+'" target="_blank" rel="noopener"><b>'+esc(r.title)+'</b></a>'
             :'<b>'+esc(r.title)+'</b>')+
        '<div class="note">'+esc(r.site)+' · '+esc(r.where)+' · '+esc(r.type)+(r.free?" · free":"")+
          (r.url?' · link checked '+esc(r.checked):(r.isbn?' · ISBN '+esc(r.isbn):''))+'</div>'+
        '<div class="note" style="color:var(--fg2)">'+esc(r.why)+'</div></div>').join("")+
      '<p class="note" style="margin-top:8px">'+richText(les.provenance)+'</p></div>'+
  '</div>';
}
function L_seen(id){return (S.learn.seen||{})[id]}
/* The core path, stated before the learner commits to the whole thing. A topic counts as
   finished without its extensions, and saying so up front is the point of marking them. */
function extNote(les){
  const ex=les.scenes.filter(x=>x.ext);
  if(!ex.length)return"";
  const core=les.scenes.filter(x=>!x.ext),
        cmin=core.reduce((a,x)=>a+(x.mins||0),0),
        xmin=ex.reduce((a,x)=>a+(x.mins||0),0);
  return '<div class="expl och" style="margin-bottom:10px"><h4>A core path, and '+ex.length+
    ' optional section'+(ex.length>1?'s':'')+'</h4>'+
    'The core is '+core.length+' sections, about '+cmin+' minutes, and finishing it completes the '+
    'topic. '+ex.length+' section'+(ex.length>1?'s are':' is')+' marked ✦ JRF extension ('+xmin+
    ' minutes): harder theory that a pass does not need and a JRF rank often does. Do the core '+
    'first and come back.</div>';
}
/* --- the learner's own notes, per section --- */
function noteKey(tid,sid){return tid+"|"+(sid||"_topic")}
function noteOf(tid,sid){return (S.notes||{})[noteKey(tid,sid)]}
function notesForTopic(tid){
  const p=tid+"|";let n=0;
  Object.keys(S.notes||{}).forEach(k=>{if(k.indexOf(p)===0&&(S.notes[k]||{}).text)n++});
  return n;
}
function saveNote(tid,sid,text){
  const k=noteKey(tid,sid);
  S.notes=S.notes||{};
  if(text&&text.trim())S.notes[k]={text:text.trim().slice(0,4000),ts:now()};
  else delete S.notes[k];
  saveNotes();render();
}
function notePane(les,sc){
  const tid=les.topicId,sid=sc?sc.id:null;
  const n=noteOf(tid,sid)||{},open=(S.noteUI||{})[noteKey(tid,sid)];
  const where=sc?esc(sc.title):"this lesson";
  return '<div class="sep"></div>'+
    '<div class="row tight" style="justify-content:space-between"><span class="lbl">My notes</span>'+
      '<span class="chip '+(notesForTopic(tid)?"ac":"dim")+' num">'+notesForTopic(tid)+' in this lesson</span></div>'+
    (open||n.text
      ? '<textarea id="noteBox" class="notebox" placeholder="Your own words on '+where+'. Saved to your profile only.">'+esc(n.text||"")+'</textarea>'+
        '<div class="row tight" style="margin-top:6px">'+
          '<button class="btn p sm" data-notesave="'+esc(noteKey(tid,sid))+'">Save note</button>'+
          (n.text?'<button class="btn sm gh" data-notedel="'+esc(noteKey(tid,sid))+'">Delete</button>':"")+
          (n.ts?'<span class="note num">saved '+dayStr(n.ts)+'</span>':"")+'</div>'
      : '<button class="btn sm" data-noteopen="'+esc(noteKey(tid,sid))+'" style="margin-top:7px">+ Add a note on this section</button>');
}
/* The one thing this page is for. Always the first block, always a way in. */
function startBlock(les,tid,seen,tot){
  const teach=les.scenes.map((x,k)=>({x:x,k:k})).filter(o=>o.x.kind!=="quiz");
  const next=teach.filter(o=>!L_seen(o.x.id))[0];
  const qz=les.scenes.length-1,done=isDone(tid),r=mrec(tid);
  const first=!seen;
  const primary=first?{sc:0,t:"Start the lesson",s:"Begin at section 1 — "+les.scenes[0].title}
    :next?{sc:next.k,t:"Resume at section "+(next.k+1),s:esc(next.x.title)}
    :{sc:qz,t:"Take the mastery test",s:"You have read every section. "+(r.best!=null?"Your best is "+r.best+"%.":"Ten unseen questions.")};
  return '<div class="startblk">'+
    '<div class="sbmain">'+
      '<button class="btn p lg" data-sc="'+primary.sc+'">'+primary.t+' ›</button>'+
      '<span class="sbnote">'+primary.s+'</span>'+
    '</div>'+
    '<div class="sbrow">'+
      (first?"":'<button class="btn sm" data-sc="0">Start from section 1</button>')+
      (next?'<button class="btn sm" data-sc="'+qz+'">Skip to the mastery test</button>':"")+
      '<span class="sp"></span>'+
      '<button class="btn sm'+(done?" g":"")+'" data-done="'+tid+'" data-on="'+(done?0:1)+'">'+
        (done?"✓ Marked done":"Mark done")+'</button>'+
    '</div>'+
  '</div>';
}
function weightCard(tid){
  const t=topicOf(tid);if(!t)return"";
  const m=mods().filter(x=>x.topics.some(y=>y.id===tid))[0]||{};
  const imp=IMP[t.imp||2];
  return '<div class="card" style="margin-bottom:12px"><div class="lbl">Weight in the exam</div>'+
    '<div class="row tight" style="margin:6px 0 8px">'+
      '<span class="chip '+imp.c+'">'+imp.s+' '+imp.n+'</span>'+
      (t.qs?'<span class="chip dim num">~'+t.qs+' questions</span><span class="chip dim num">~'+t.marks+' marks</span>':"")+
      '<span class="chip dim">'+esc(m.name||"")+': '+(m.marks||0)+' marks</span></div>'+
    '<p class="note">'+esc(imp.d)+'. '+
      (m.wReviewed
        ? esc(m.wBasis||"")+' The module total is the real paper structure; the split across topics inside it is an editorial judgement and the admin can revise it.'
        : 'This module has not been reviewed topic by topic yet, so its '+(m.marks||0)+' marks are split evenly across its '+((m.topics||[]).length)+' topics. Treat the per-topic figure as a placeholder.')+
    '</p></div>';
}
function mixBar(counts,total){
  const o=["easy","moderate","hard"];
  return '<div class="mixbar">'+o.map(d=>counts[d]?'<i class="'+d+'" style="width:'+pc(counts[d],total)+'%"></i>':"").join("")+'</div>'+
    '<div class="mixkey">'+o.map(d=>'<span><i class="'+d+'"></i>'+DIFF[d].n+' '+(counts[d]||0)+'</span>').join("")+'</div>';
}
function revSheetHTML(les){
  return '<div class="card" style="margin-bottom:14px"><div class="row tight" style="justify-content:space-between">'+
    '<span class="lbl">One-page revision sheet</span>'+(S.dl?'<button class="btn sm" data-dlrev="1">Save it</button>':"")+'</div>'+
    '<ul class="revl">'+les.revision.sheet.map(x=>'<li>'+richText(x)+'</li>').join("")+'</ul>'+
    '<div class="lbl" style="margin-top:12px">Flashcards</div>'+
    '<div class="cards">'+les.revision.cards.map((c,k)=>
      '<button class="fcard'+(S.learn.flip&&S.learn.flip[k]?" on":"")+'" data-flip="'+k+'">'+
      '<span class="ff">'+richText(c[0])+'</span><span class="fb">'+richText(c[1])+'</span></button>').join("")+'</div></div>';
}

/* ---- scene renderers ---- */
function paras(a){return (a||[]).map(x=>'<p>'+richText(x)+'</p>').join("")}
function askPane(sc){
  // An ask carrying only a pre-written Claude prompt (the legacy {label, prompt, tier}
  // shape, still in 4.5 and 4.9) has no question to put in the box. Without this guard
  // the scene showed "Try this before you go on" above an empty prompt and a Check button.
  if(!sc.ask||!sc.ask.q)return"";
  const v=(S.learn.said||{})[sc.id]||"";
  return '<div class="think"><div class="lbl">Try this before you go on</div>'+
    '<p class="tq">'+richText(sc.ask.q)+'</p>'+
    '<textarea id="sayBox" placeholder="One or two sentences is plenty. Writing it down is what makes it stick.">'+esc(v)+'</textarea>'+
    '<div class="row" style="margin-top:8px"><button class="btn p sm" id="checkSay">Check my answer</button>'+
      '<button class="btn sm" data-nudge="'+sc.id+'">Give me a hint</button></div>'+
    ((S.learn.nudge||{})[sc.id]?'<p class="note" style="margin-top:8px;color:var(--ochre)">'+richText(sc.ask.nudge)+'</p>':"")+
    '<div class="out" id="sayOut" hidden></div></div>';
}
/* For someone coming back after a gap: check the handful of things this lesson
   assumes, and rebuild any that are shaky before the lesson proper starts. */
function scFoundation(sc,les){
  const L=S.learn,st=(L.found||{})[sc.id]||{};
  const items=sc.items||[];
  const marked=items.filter((x,k)=>st[k]).length;
  const shaky=items.filter((x,k)=>st[k]==="shaky");
  return '<div class="prose">'+paras(sc.body||[sc.intro||""])+'</div>'+
    '<div class="foundgrid">'+items.map((it,k)=>{
      const v=st[k];
      return '<div class="found'+(v?" "+v:"")+'">'+
        '<div class="fq"><span class="fn3">'+(k+1)+'</span><b>'+richText(it.ask)+'</b></div>'+
        (v?'<div class="fa">'+richText(it.recall)+'</div>'+
           (v==="shaky"&&it.refresh?'<div class="frefresh"><span class="asl">Rebuild it in a minute</span>'+
              paras(Array.isArray(it.refresh)?it.refresh:[it.refresh])+'</div>':"")
          :'<div class="row tight" style="margin-top:8px">'+
             '<button class="btn sm" data-found="'+sc.id+'|'+k+'|solid">I know this</button>'+
             '<button class="btn sm" data-found="'+sc.id+'|'+k+'|shaky">Shaky — show me</button></div>')+
      '</div>'}).join("")+'</div>'+
    (marked>=items.length&&items.length
      ? '<div class="expl '+(shaky.length?"och":"ok")+'" style="margin-top:14px"><h4>'+
          (shaky.length?shaky.length+' of '+items.length+' to shore up':'All '+items.length+' solid')+'</h4>'+
          (shaky.length
            ? 'Those refreshers are enough to follow this lesson — go on. Nothing here is a gate, and a lesson built to the house standard rebuilds its own ground as it goes. If you would rather shore things up first, the prerequisite topics are listed on the overview.'
            : 'Nothing here will be assumed without warning. Go on to the lesson proper.')+
        '</div>'
      : '<p class="note" style="margin-top:12px">'+marked+' of '+items.length+' answered. Be honest — marking something shaky costs you one minute now and saves twenty later.</p>');
}
function scIntuition(sc){
  return '<div class="prose">'+paras(sc.body)+'</div>'+
    (sc.flow?flowBlock(sc.flow):"")+
    (sc.aside?'<div class="expl och"><h4>'+esc(sc.aside.h)+'</h4>'+richText(sc.aside.body)+'</div>':"");
}
/* The legacy ask shape: a question worth putting to Claude, authored with the scene.
   Rendered as a button that opens the Ask panel already carrying the prompt. */
function suggestAskHTML(sc){
  const a=sc.ask;
  if(!a||a.q||!a.prompt)return"";
  return '<div class="expl"><h4>'+esc(a.label||"A question worth asking")+'</h4>'+
    '<p class="note" style="margin:0 0 8px">'+richText(a.prompt)+'</p>'+
    '<button class="btn sm" data-askopen="1" data-intent="free" data-sel="'+esc(a.prompt)+'">'+
      '✦ Ask Claude this</button></div>';
}
/* A small reference table. Added for the family→statistic grids: the information was
   already in the prose and the revision sheet, but a grid is the form people read. */
function tableHTML(t){
  const head=t.head||[],rows=t.rows||[];
  return '<div class="tblwrap"><table class="lt">'+
    (t.caption?'<caption class="note">'+richText(t.caption)+'</caption>':"")+
    (head.length?'<thead><tr>'+head.map(h=>'<th scope="col">'+richText(h)+'</th>').join("")+'</tr></thead>':"")+
    '<tbody>'+rows.map(r=>'<tr>'+r.map((c,i)=>
      i?'<td>'+richText(c)+'</td>':'<th scope="row">'+richText(c)+'</th>').join("")+'</tr>').join("")+
    '</tbody></table></div>';
}
/* A real-world use of the idea, opened on demand and closed again without losing your place. */
function scenarioHTML(sc){
  const sn=sc.scenario;if(!sn)return"";
  const open=(S.learn.scen||{})[sc.id];
  if(!open)return '<button class="scenbtn" data-scen="'+sc.id+'">'+
    '<span class="si">◉</span><span class="sb2"><b>Where this shows up in the real world</b>'+
    '<span>'+esc(sn.teaser||sn.title||"A worked case from practice")+'</span></span>'+
    '<span class="note">open ›</span></button>';
  return '<div class="scenwrap"><div class="scenhd"><span class="si">◉</span>'+
      '<b>'+esc(sn.title||"In the real world")+'</b>'+
      '<button class="btn sm" data-scen="'+sc.id+'">‹ Back to the lesson</button></div>'+
    '<div class="scenbody">'+paras(sn.body)+
      (sn.flow?flowBlock(sn.flow):"")+
      (sn.q?'<div class="scenq"><b>Have a go at this:</b> '+richText(sn.q)+'</div>':"")+
      (sn.answer?'<div class="expl ok"><h4>What the statistics tells us</h4>'+richText(sn.answer)+'</div>':"")+
      (sn.link?'<p class="note">'+esc(sn.link)+'</p>':"")+
      '<div class="row" style="margin-top:12px"><button class="btn" data-scen="'+sc.id+'">‹ Back to the lesson</button></div>'+
    '</div></div>';
}
function scExplore(sc){
  const st=vizState(sc);
  const C=VIZ[sc.viz.type];
  if(!C)return '<div class="prose">'+paras(sc.body)+'</div><p class="note">This visualisation is not available in this build.</p>';
  const out=C.draw(st);
  return '<div class="prose">'+paras(sc.body)+'</div>'+
    '<div class="vizbox" id="vizbox"><div class="vizhead">'+richText(C.title)+'</div>'+
      '<div class="vizsvg">'+out.svg+'</div>'+
      '<div class="vizctl">'+C.controls(st).map(c=>
        '<label class="vc"><span>'+richText(c.label)+' <b class="num" data-vo="'+c.k+'">'+c.fmt(c.val)+'</b></span>'+
        '<input type="range" data-vz="'+c.k+'" min="'+c.min+'" max="'+c.max+'" step="'+c.step+'" value="'+c.val+'"></label>').join("")+'</div>'+
      '<div class="vizread">'+out.read.map(r=>'<div class="vr"><span>'+richText(r[0])+'</span><b class="num">'+richText(r[1])+'</b></div>').join("")+'</div>'+
      '<p class="vnote">'+richText(out.note)+'</p>'+
    '</div>';
}
function vizState(sc){
  const L=S.learn;
  if(!L.viz[sc.id])L.viz[sc.id]=VIZ[sc.viz.type]?VIZ[sc.viz.type].init(sc.viz):{};
  return L.viz[sc.id];
}
const BT={def:["Definition","ac"],formula:["",""],step:["",""],assume:["Condition","mid"],note:["Note","dim"],trap:["Trap","bad"]};
function scTheory(sc){
  return (sc.flow?flowBlock(sc.flow):"")+sc.blocks.map(b=>{
    if(b.t==="formula"||b.t==="step")
      return '<div class="fblock"><div class="fh">'+esc(b.h)+'</div>'+
        '<div class="fbody">'+richText(b.body)+'</div></div>';
    return '<div class="expl '+(b.t==="trap"?"bad":b.t==="assume"?"och":b.t==="def"?"":"dim")+'">'+
      '<h4>'+esc(b.h)+'</h4>'+richText(b.body)+'</div>'}).join("");
}
function scWorked(sc){
  const L=S.learn,shown=(L.steps||{})[sc.id]||1;
  return '<div class="prob">'+richText(sc.problem)+'</div>'+
    sc.steps.slice(0,shown).map((s,k)=>
      '<div class="wstep"><div class="wn">'+(k+1)+'</div><div class="wb">'+
        '<div class="ws1">'+richText(s.say)+'</div>'+
        formulaHTML(s.math)+
        '<div class="wy">'+esc(s.why)+'</div></div></div>').join("")+
    (shown<sc.steps.length
      ?'<button class="btn p" data-step="'+sc.id+'">Next step ('+shown+' of '+sc.steps.length+')</button>'
      :(sc.after?'<div class="expl ok"><h4>What to take from it</h4>'+richText(sc.after)+'</div>':""));
}
function scRecall(sc){
  const L=S.learn,rv=(L.reveal||{})[sc.id]||{};
  return '<p class="lead">'+esc(sc.intro)+'</p>'+
    sc.items.map((it,k)=>'<div class="rcard">'+
      '<div class="rq">'+richText(it.q)+'</div>'+
      (rv[k]?'<div class="ra">'+richText(it.a)+'</div>'
            :'<button class="btn sm" data-rev="'+sc.id+'|'+k+'">Reveal</button>')+
      '</div>').join("");
}
function scCompletion(sc){
  const L=S.learn,bl=(L.blanks||{})[sc.id]||{};
  return '<div class="prob">'+richText(sc.problem)+'</div>'+
    sc.steps.map((s,k)=>{
      const b=s.blank,v=bl[k]||{};
      return '<div class="wstep"><div class="wn">'+(k+1)+'</div><div class="wb">'+
        '<div class="ws1">'+richText(s.say)+'</div>'+
        (b?(v.ok===undefined
            ?'<div class="blank"><label class="fl">'+richText(b.prompt)+'</label>'+
              '<input type="text" class="bi" data-bk="'+sc.id+'|'+k+'" value="'+esc(v.val||"")+'" placeholder="type it, then check">'+
              '<div class="row tight" style="margin-top:6px"><button class="btn p sm" data-bchk="'+sc.id+'|'+k+'">Check</button>'+
              '<button class="btn sm" data-bhint="'+sc.id+'|'+k+'">Hint</button>'+
              '<button class="btn sm" data-bshow="'+sc.id+'|'+k+'">Show me</button></div>'+
              (v.hint?'<p class="note" style="margin-top:6px;color:var(--ochre)">'+esc(b.hint)+'</p>':"")+
              (v.wrong?'<p class="note" style="margin-top:6px;color:var(--bad)">Not a match. Check the signs and the brackets, then try once more — or take the hint.</p>':"")+
              '</div>'
            :'<div class="fm'+(v.ok?" ok":"")+'">'+esc(b.answer)+'</div>'+
             '<div class="note">'+(v.ok?"✓ you had it":"shown — count this as assisted")+'</div>')
          :formulaHTML(s.math))+
        ((b&&v.ok===undefined)?"":'<div class="wy">'+richText(s.why)+'</div>')+
      '</div></div>'}).join("")+
    (sc.after?'<div class="expl ok"><h4>What to take from it</h4>'+richText(sc.after)+'</div>':"");
}
function scGuided(sc){
  const L=S.learn,h=(L.hints||{})[sc.id]||0,sol=(L.solShown||{})[sc.id];
  return '<div class="prob">'+richText(sc.problem)+'</div>'+
    '<div class="hintlad">'+
      sc.hints.slice(0,h).map((x,k)=>'<div class="hint"><span class="hn">Hint '+(k+1)+'</span>'+richText(x)+'</div>').join("")+
      (h<sc.hints.length&&!sol?'<button class="btn" data-hint="'+sc.id+'">'+(h?"Another hint ("+(h+1)+" of "+sc.hints.length+")":"I need a hint")+'</button>':"")+
    '</div>'+
    '<div class="think" style="margin-top:12px"><div class="lbl">Your answer</div>'+
      '<textarea id="gBox" placeholder="Work it out on paper, then write your final answer here.">'+esc((L.said||{})[sc.id]||"")+'</textarea>'+
      '<div class="row" style="margin-top:8px">'+
        (sol?"":'<button class="btn p sm" data-sol="'+sc.id+'">Show the solution</button>')+
        '<button class="btn sm" id="gradeMe">Ask Claude to check my working</button></div>'+
      '<div class="out" id="sayOut" hidden></div></div>'+
    (sol?'<div class="sep"></div>'+
      sc.solution.map((s,k)=>'<div class="wstep"><div class="wn">'+(k+1)+'</div><div class="wb">'+
        '<div class="ws1">'+richText(s.say)+'</div>'+formulaHTML(s.math)+'</div></div>').join("")+
      '<div class="expl ok"><h4>Answer</h4>'+richText(sc.answer)+'</div>'+
      (sc.check?'<div class="expl och"><h4>Terminal check</h4>'+richText(sc.check)+'</div>':"")+
      (h?'<p class="note">You used '+h+' hint'+(h>1?"s":"")+' here. That is recorded — the mastery test is hint-free, and this is how the two stay distinguishable.</p>':"")
    :"");
}
function scTrapcheck(sc){
  const L=S.learn,v=(L.verd||{})[sc.id]||{},all=Object.keys(v).length>=sc.items.length;
  return '<p class="lead">'+esc(sc.intro)+'</p>'+
    sc.items.map((it,k)=>{
      const got=v[k],truth=it.tf?"T":"F",right=got===truth;
      return '<div class="stmt'+(all?(right?" v-t":" v-f"):(got?" v-sel":""))+'">'+
        '<span class="sl">'+String.fromCharCode(65+k)+'</span>'+
        '<span class="sb">'+esc(it.claim)+
          (all?'<div class="note" style="margin-top:5px"><b>'+(it.tf?"TRUE":"FALSE")+'</b> — '+richText(it.why)+
               (right?' <b style="color:var(--ok)">✓ you had it</b>':' <b style="color:var(--bad)">✗ you said '+(got==="T"?"true":"false")+'</b>')+'</div>':"")+
        '</span>'+
        (all?"":'<span class="sv"><button class="vb t" data-tv="'+sc.id+'|'+k+'|T" aria-pressed="'+(got==="T")+'">T</button>'+
          '<button class="vb f" data-tv="'+sc.id+'|'+k+'|F" aria-pressed="'+(got==="F")+'">F</button></span>')+
      '</div>'}).join("")+
    (all?'<div class="expl ok"><h4>Score on this set</h4>'+
        sc.items.filter((it,k)=>v[k]===(it.tf?"T":"F")).length+' of '+sc.items.length+
        ' correct. In the real paper these six would have been one question, scored all or nothing.</div>'
      :'<p class="note" style="color:var(--ochre)">'+Object.keys(v).length+' of '+sc.items.length+' answered. The reasons stay hidden until every statement has a verdict.</p>');
}
function scSummary(sc,les){
  return '<ul class="revl">'+sc.body.map(x=>'<li>'+richText(x)+'</li>').join("")+'</ul>'+
    '<div class="sep"></div>'+revSheetHTML(les);
}
function scQuizIntro(sc,les){
  const r=mrec(les.topicId),pol=les.mastery;
  const set=S.sets[sc.setId]||[],poolN=set.filter(q=>!isFree(q)).length;
  const mix=pol.diffMix||{},drawN=pol.draw||pol.minQ||10,attempts=r.attempts||0;
  if(!set.length&&sc.setId&&S.db)loadSet(sc.setId).then(()=>{if(S.route==="learn")render()});
  return '<div class="prose"><p>'+drawN+' questions drawn from a pool of '+(poolN||"—")+
      ', kept out of the practice bank and out of mocks. No hints, no second attempt within a question.</p>'+
    (attempts?'<p>You have taken this '+attempts+' time'+(attempts>1?"s":"")+
      '. The draw favours questions you have not met and pulls back anything you got wrong, so a retake is a different paper with deliberate overlap on your weak items.</p>':"")+
    '<p>You will be asked how confident you are before each answer is locked. That is not decoration: answering correctly with low confidence, or wrongly with high confidence, means different things and the result page separates them.</p></div>'+
    '<div class="card" style="margin:14px 0"><div class="lbl">To pass</div>'+
      '<div class="trow"><div class="tn">'+pol.pass+'% overall</div></div>'+
      Object.keys(pol.fmtMin).map(f=>'<div class="trow"><div class="tn">'+esc(FMT[f]?FMT[f].n:f)+' at least '+pol.fmtMin[f]+'%</div></div>').join("")+
      (r.best!=null?'<div class="trow"><div class="tn">Your best so far: <b>'+r.best+'%</b>'+(r.attempts>1?" over "+r.attempts+" attempts":"")+'</div></div>':"")+
      (Object.keys(mix).length?'<div class="sep"></div><div class="lbl">Difficulty of this paper</div>'+
        mixBar(mix,drawN)+
        '<p class="note" style="margin-top:6px">Every paper is drawn to this mix, so two attempts are comparable. '+
        'NTA publishes no official difficulty split — this models a NET-style paper, and it is an admin setting.</p>':"")+
    '</div>'+
    '<button class="btn p" data-startquiz="'+les.id+'">Start the mastery test</button>';
}

/* ---- mastery test ---- */
function quizPane(){
  const Q=S.learn.quiz,les=S.lessons[S.learn.topicId];
  if(Q.done)return quizResult(Q,les);
  const q=Q.list[Q.i],free=isFree(q);
  return '<div class="pane"><div class="scbar">'+
    '<button class="btn sm" data-sc="-99" title="Leave the test">✕</button>'+
    '<span class="chip bad">test · hints off</span>'+
    '<div class="scdots">'+Q.list.map((_,k)=>'<button class="scd'+(k===Q.i?" cur":"")+(Q.ans[k]?" seen":"")+'" data-qgo="'+k+'"></button>').join("")+'</div>'+
    '<span class="chip dim">'+Object.keys(Q.ans).length+'/'+Q.list.length+' answered</span>'+
    '<button class="btn sm gh" data-askopen="1" title="Ask Claude what a word means — it will not tell you the answer">✦ Ask</button>'+
    '<button class="btn sm" id="quizSubmit">Submit</button></div>'+
    '<div class="schead"><span class="chip dim">'+esc(isFree(q)?"Write-in":(FMT[q.format]||{n:q.format}).n)+'</span></div>'+
    '<div class="stem">'+richText(q.stem)+'</div>'+
    ((q.statements||[]).length?'<div style="margin-bottom:12px">'+q.statements.map((s,k)=>
      '<div class="stmt"><span class="sl">'+String.fromCharCode(65+k)+'</span><span class="sb">'+esc(s)+'</span></div>').join("")+'</div>':"")+
    ((q.pairs||[]).length?'<div class="scroll"><table class="tbl"><thead><tr><th>List I</th><th>List II</th></tr></thead><tbody>'+
      q.pairs.map(p=>'<tr><td>'+esc(p[0])+'</td><td>'+esc(p[1])+'</td></tr>').join("")+'</tbody></table></div>':"")+
    ((q.items||[]).length?'<div class="row tight" style="margin-bottom:10px">'+q.items.map(it=>'<span class="chip dim">'+esc(it)+'</span>').join("")+'</div>':"")+
    (free?'<textarea id="qFree" placeholder="Write your answer out.">'+esc(Q.free[Q.i]||"")+'</textarea>'
         :(q.options||[]).map((o,k)=>{const Lt=String.fromCharCode(65+k);
            return '<button class="opt" data-qopt="'+Lt+'" aria-pressed="'+(Q.ans[Q.i]===Lt)+'"><span class="ol">'+Lt+'</span><span>'+richText(o)+'</span></button>'}).join(""))+
    '<div class="conf"><span class="lbl">How sure are you?</span><div class="row tight">'+
      [["1","guessing"],["2","fairly sure"],["3","certain"]].map(c=>
        '<button class="tog" data-conf="'+c[0]+'" aria-pressed="'+(String(Q.conf[Q.i])===c[0])+'">'+c[1]+'</button>').join("")+'</div></div>'+
    '<div class="scnav">'+
      (Q.i>0?'<button class="btn" data-qgo="'+(Q.i-1)+'">‹ back</button>':"")+'<span class="sp"></span>'+
      (Q.i<Q.list.length-1?'<button class="btn p" data-qgo="'+(Q.i+1)+'">next ›</button>'
        :'<button class="btn p" id="quizSubmit2">Submit the test</button>')+
    '</div></div>';
}
function gradeQuiz(){
  const Q=S.learn.quiz,les=S.lessons[S.learn.topicId],pol=les.mastery;
  let c=0;const byFmt={},rows=[];
  Q.list.forEach((q,k)=>{
    const free=isFree(q);
    const ok=free?(Q.self[k]===true):(Q.ans[k]===q.answer);
    if(ok)c++;
    const f=free?"numeric":q.format;
    const b=byFmt[f]||(byFmt[f]={n:0,c:0});b.n++;if(ok)b.c++;
    rows.push({q:q,ok:ok,picked:free?(Q.free[k]||""):Q.ans[k],conf:Q.conf[k]||0});
    record(q,ok);
  });
  const pct=pc(c,Q.list.length);
  const fails=Object.keys(pol.fmtMin).filter(f=>byFmt[f]&&pc(byFmt[f].c,byFmt[f].n)<pol.fmtMin[f]);
  const pass=pct>=pol.pass&&!fails.length&&Q.list.length>=pol.minQ;
  const byDiff={};
  rows.forEach(row=>{const d=row.q.diff||"moderate";
    const bd=byDiff[d]||(byDiff[d]={n:0,c:0});bd.n++;if(row.ok)bd.c++});
  Q.byDiff=byDiff;
  const r=mrec(les.topicId),everPassed=!!r.passedOnce||r.state==="mastered";
  const rec={state:pass?"mastered":(everPassed?"revisionDue":"failed"),
    best:Math.max(r.best||0,pct),last:pct,passedOnce:everPassed||pass,
    byFmt:byFmt,byDiff:byDiff,ts:now(),attempts:(r.attempts||0)+1,
    served:Q.list.map(q=>q.id),
    retestDue:pass?now()+pol.retestDays*86400000:null,independent:true};
  S.mastery[les.topicId]=rec;saveMastery();
  Q.done=true;Q.c=c;Q.pct=pct;Q.byFmt=byFmt;Q.rows=rows;Q.pass=pass;Q.fails=fails;
}
function quizResult(Q,les){
  const pol=les.mastery;
  const cal=[[0,0],[0,0],[0,0]];
  Q.rows.forEach(r=>{const i=cl((r.conf||1)-1,0,2);cal[i][1]++;if(r.ok)cal[i][0]++});
  const over=Q.rows.filter(r=>r.conf===3&&!r.ok).length;
  const under=Q.rows.filter(r=>r.conf===1&&r.ok).length;
  const missed=Q.rows.filter(r=>!r.ok);
  return '<div class="pane">'+
    '<div class="row tight" style="margin-bottom:12px"><button class="btn sm" data-sc="-99">‹ topic</button>'+
      '<span class="chip '+(Q.pass?"ok":"bad")+'">'+(Q.pass?"MASTERED":"not yet")+'</span></div>'+
    '<h1>'+Q.c+' of '+Q.list.length+' — '+Q.pct+'%</h1>'+
    bar(Q.pct,Q.pass?"ok":"bad")+
    '<div class="grid g2" style="margin:14px 0">'+
      '<div class="card"><div class="lbl">Against the policy</div>'+
        '<div class="trow"><span class="chip '+(Q.pct>=pol.pass?"ok":"bad")+'">'+(Q.pct>=pol.pass?"✓":"✗")+'</span><div class="tn">'+Q.pct+'% overall, need '+pol.pass+'%</div></div>'+
        Object.keys(pol.fmtMin).map(f=>{const b=Q.byFmt[f];if(!b)return"";
          const p=pc(b.c,b.n);
          return '<div class="trow"><span class="chip '+(p>=pol.fmtMin[f]?"ok":"bad")+'">'+(p>=pol.fmtMin[f]?"✓":"✗")+'</span>'+
            '<div class="tn">'+esc(FMT[f]?FMT[f].n:f)+' '+b.c+'/'+b.n+' = '+p+'%, need '+pol.fmtMin[f]+'%</div></div>'}).join("")+
        '<div class="trow"><span class="chip ok">✓</span><div class="tn">Answered without hints</div></div>'+
        (Q.byDiff?'<div class="sep"></div><div class="lbl">By difficulty</div>'+
          ["easy","moderate","hard"].map(d=>{const bd=Q.byDiff[d];if(!bd)return"";
            return '<div class="trow"><span class="chip '+(pc(bd.c,bd.n)>=60?"ok":"bad")+'">'+bd.c+'/'+bd.n+'</span>'+
              '<div class="tn">'+DIFF[d].n+' — '+pc(bd.c,bd.n)+'%</div></div>'}).join("")+
          (Q.repeat!==undefined?'<p class="note" style="margin-top:6px">'+
            (Q.repeat?Q.repeat+' of these appeared on your last attempt; the other '+(Q.list.length-Q.repeat)+' were new.'
                     :'Every question here was new since your last attempt.')+'</p>':""):"")+
        (Q.pass?'<p class="note" style="margin-top:8px">Marked mastered. A retention retest falls due in '+pol.retestDays+' days — passing once is not the same as still knowing it next week.</p>'
               :'<p class="note" style="margin-top:8px">'+(Q.fails.length?"The overall score is not the problem — a format floor is.":"Below the overall threshold.")+' The scenes below cover what you missed.</p>')+
      '</div>'+
      '<div class="card"><div class="lbl">Confidence against correctness</div>'+
        [["certain",2],["fairly sure",1],["guessing",0]].map(([n,i])=>cal[i][1]?
          '<div style="margin-bottom:8px"><div class="kv"><span>'+n+'</span><b>'+cal[i][0]+'/'+cal[i][1]+'</b></div>'+
          bar(pc(cal[i][0],cal[i][1]),pc(cal[i][0],cal[i][1])>=80?"ok":"bad",true)+'</div>':"").join("")+
        (over?'<p class="note" style="color:var(--bad)">'+over+' answered with certainty and wrong. That is a misconception, not a slip — it will not fix itself with more practice on the same material.</p>':"")+
        (under?'<p class="note">'+under+' guessed and right. Treat those as unknown, not known.</p>':"")+
        (!over&&!under?'<p class="note">Your confidence tracked your accuracy. That is worth as much as the score.</p>':"")+
      '</div>'+
    '</div>'+
    (missed.length?'<div class="card" style="margin-bottom:12px"><div class="lbl">Go back to these</div>'+
      remediation(missed,les)+'</div>':"")+
    '<div class="card" style="margin-bottom:12px"><div class="lbl">Every question</div>'+
      Q.rows.map((r,k)=>'<details class="sp"><summary><span class="chip '+(r.ok?"ok":"bad")+'">'+(r.ok?"✓":"✗")+'</span>'+
        '<span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:400">'+(k+1)+'. '+esc(String(r.q.stem).replace(/\s+/g," "))+'</span></summary>'+
        '<div><div class="stem" style="font-size:.92rem">'+esc(r.q.stem)+'</div>'+
        ((r.q.statements||[]).length?r.q.statements.map((s,j)=>'<div class="stmt"><span class="sl">'+String.fromCharCode(65+j)+'</span><span class="sb">'+esc(s)+'</span></div>').join(""):"")+
        (isFree(r.q)?'<div class="expl"><h4>Answer</h4><b>'+esc(r.q.answer)+'</b><br>'+esc(r.q.explanation)+'</div>'
          :(r.q.options||[]).map((o,j)=>{const Lt=String.fromCharCode(65+j);
             return '<div class="opt'+(Lt===r.q.answer?" right":Lt===r.picked?" wrong":"")+'" style="pointer-events:none"><span class="ol">'+Lt+'</span><span>'+richText(o)+'</span></div>'}).join("")+
            '<div class="expl"><h4>Why '+esc(r.q.answer)+'</h4>'+esc(r.q.explanation)+'</div>')+
        (r.q.check?'<div class="expl och"><h4>Terminal check</h4>'+esc(r.q.check)+'</div>':"")+
        (r.q.verdicts?'<div class="vlist">'+Object.keys(r.q.verdicts).sort().map(Lt=>{const v=r.q.verdicts[Lt];
          const tf=(v.tf===true||v.tf==="T")?"T":"F";
          return '<div class="vitem"><b>'+Lt+'</b><span class="tf '+tf+'">'+tf+'</span><span>'+esc(v.why)+'</span></div>'}).join("")+'</div>':"")+
        '</div></details>').join("")+'</div>'+
    '<div class="row">'+(Q.pass?'<button class="btn p" data-sc="-99">Back to the topic</button>'
      :'<button class="btn p" data-startquiz="'+les.id+'">Retake the test</button><button class="btn" data-sc="0">Restart the lesson</button>')+
      '</div>'+
    askBox("ask-quizres","Ask Claude what to do about this result",
      "A UGC NET Statistics (JRF) candidate just took a mastery test on "+les.title+" and scored "+Q.pct+"%"+(Q.pass?" (passed)":" (did not pass)")+
      ". By format: "+Object.keys(Q.byFmt).map(f=>f+" "+Q.byFmt[f].c+"/"+Q.byFmt[f].n).join("; ")+
      ". They answered "+over+" questions wrongly while reporting full certainty, and got "+under+" right while guessing."+
      (missed.length?" The questions they missed were about: "+missed.map(r=>String(r.q.stem).slice(0,90)).join(" | "):"")+
      "\n\nSay what the pattern is — misconception, method selection, or execution — and give two specific things to do before retaking. Do not restate the score. Under 170 words, plain text.","complex")+
  '</div>';
}
function remediation(missed,les){
  // map a missed question to the scenes whose objective covers it, by keyword overlap
  const words=t=>String(t||"").toLowerCase().match(/[a-zα-ω̂]{4,}/g)||[];
  const scored=les.scenes.map((sc,k)=>{
    const bag=words(sc.title+" "+(sc.objective||"")+" "+JSON.stringify(sc.blocks||sc.body||sc.items||""));
    let s=0;missed.forEach(r=>{const w=words(r.q.stem+" "+r.q.explanation);
      w.forEach(x=>{if(bag.indexOf(x)>=0)s++})});
    return {k:k,sc:sc,s:s}}).filter(x=>x.sc.kind!=="quiz").sort((a,b)=>b.s-a.s).slice(0,3);
  return scored.map(x=>'<button class="scrow" data-sc="'+x.k+'">'+
    '<span class="scn">'+(x.k+1)+'</span><span class="sck">'+SCENEKIND[x.sc.kind].i+'</span>'+
    '<span class="sct"><b>'+esc(x.sc.title)+'</b><span class="note">'+esc(x.sc.objective||SCENEKIND[x.sc.kind].n)+'</span></span></button>').join("")+
    '<p class="note" style="margin-top:8px">Chosen by overlap between what you missed and what each scene teaches — a keyword match, not a diagnosis. Trust your own reading of the explanations above it.</p>';
}

function diagBanner(tid){
  const ent=lessonFor(tid);
  const nIdx=Object.keys((S.lessonIdx&&S.lessonIdx.topics)||{}).length;
  if(!S.lessonIdx)
    return '<div class="banner bad"><div><b>The lessons index has not been read.</b> The page could not load '+
      '<span class="mono">meta/lessons</span>, so it does not know which topics have a lesson. '+
      'Open <b>Admin</b> and press <b>Rescan store</b> — that rebuilds the index by scanning the lessons collection.</div></div>';
  if(!ent)
    return '<div class="banner ac"><div><b>No lesson is indexed for this topic.</b> '+
      (nIdx?('The index lists '+nIdx+' lesson'+(nIdx>1?'s':'')+', none of them for <span class="mono">'+esc(tid)+'</span>. '+
             'If one was authored since the index was built, press <b>Rescan store</b> on Admin.')
           :'The index is empty — nothing has been authored yet, or the index needs rebuilding from Admin.')+
      ' Lessons live in the database, not in this page, so a chat can write one without the app being rebuilt.</div></div>';
  return '<div class="banner bad"><div><b>The lesson document could not be read.</b> The index names '+
    '<span class="mono">lessons/'+esc(ent.id)+'</span> for this topic, but fetching it returned nothing. '+
    'That usually means the document was deleted or renamed after the index was built — '+
    '<b>Rescan store</b> on Admin will resync it.</div></div>';
}
