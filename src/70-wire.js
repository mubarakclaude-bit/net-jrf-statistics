/* ===================== events ===================== */
function go(tab){
  // Admin is the owner's surface. Guard the route as well as the tab, so a learner
  // cannot reach it by typing the hash or by a route remembered from another session.
  if(tab==="admin"&&!S.isAdmin)tab="home";
  S.route=tab;location.hash=tab;render();window.scrollTo(0,0)}
function captureText(){
  const L=S.learn,les=L.topicId&&S.lessons[L.topicId];
  if(!les||L.i<0)return;
  const sc=les.scenes[L.i];if(!sc)return;
  const a=document.querySelector("#sayBox")||document.querySelector("#gBox");
  if(a){L.said=L.said||{};L.said[sc.id]=a.value}
  const q=document.querySelector("#qFree");
  if(q&&L.quiz)L.quiz.free[L.quiz.i]=q.value;
}
function markSeen(id){
  const L=S.learn,tid=L.topicId;if(!tid||!id)return;
  L.seen=L.seen||{};L.seen[id]=1;
  S.topics=S.topics||{};
  const st=S.topics[tid]||(S.topics[tid]={s:0,seen:[]});
  st.seen=st.seen||[];
  if(st.seen.indexOf(id)<0)st.seen.push(id);
  const les=S.lessons[tid];
  // Optional "JRF extension" scenes must not hold a topic open: completion counts the
  // required scenes only, so skipping an extension still finishes the lesson.
  let done=false;
  if(les){
    const req=les.scenes.filter(x=>!x.ext);
    done=req.every(x=>st.seen.indexOf(x.id)>=0);
  }
  st.s=done?2:Math.max(st.s||0,1);
  st.t=now();saveTopics();
}
function gotoScene(i){
  const L=S.learn,les=S.lessons[L.topicId];
  // A falsy lesson used to make this function return in silence, which turned every
  // "Start the lesson" button into a dead control with no message. Recover instead:
  // retry the fetch, say so, and re-render either way.
  if(!les){
    if(L.topicId){
      S.learn.pendScene=i;
      if(les===false)delete S.lessons[L.topicId];        // let a failed fetch be retried
      toast(les===false?"Reloading the lesson…":"Still fetching the lesson…");
      loadLesson(L.topicId).then(got=>{
        if(S.route!=="learn"||S.learn.topicId!==L.topicId)return;
        const want=S.learn.pendScene;delete S.learn.pendScene;
        if(got&&want!=null)gotoScene(want);else render();
      }).catch(()=>{delete S.learn.pendScene;toast("Could not load the lesson");render()});
    }
    render();return;
  }
  captureText();
  if(i===-99){L.i=-1}
  else{
    L.i=cl(i,0,les.scenes.length-1);
    // Recording progress must never be able to block the navigation itself. If this throws,
    // note it and carry on: a lesson you can read without a progress tick beats a dead button.
    try{markSeen(les.scenes[L.i].id)}
    catch(err){S.seenErr=(err&&err.message)||"error";try{console.error("markSeen failed",err)}catch(_){}}
  }
  if(narrow())S.navOpen=false;   // the contents panel is full-screen here — jumping to a scene should show it
  render();window.scrollTo(0,0);
  // keep the current step visible in the rail without disturbing the rail's own scroll otherwise
  const cur=document.querySelector(".wsnav .steprow.cur");
  if(cur&&cur.scrollIntoView)cur.scrollIntoView({block:"nearest"});
}
function openTopic(tid){
  captureText();resetLearn(tid);
  if(narrow()){S.navOpen=false;S.aideOpen=false}   // the drawer is full-screen here — get out of the way
  if(S.lessons[tid]===undefined)loadLesson(tid).then(()=>{if(S.route==="learn")render()});
  go("learn");
}
/* Draw a paper from the topic's pool: hold the difficulty mix the policy asks for,
   prefer items this profile has not met, and pull back anything recently got wrong. */
function drawPaper(pool,pol,prev){
  const want=pol.draw||pol.minQ||10;
  const mix=pol.diffMix||null;
  const seenBefore=id=>!!(S.att[id]&&S.att[id].n);
  const gotWrong=id=>!!(S.att[id]&&S.att[id].n&&!S.att[id].o);
  const lastTime=id=>(prev&&prev.indexOf(id)>=0)?1:0;   // served on the immediately previous attempt
  // fresh material first: not served last time, then never seen, then least recently seen
  const rank=(a,b)=>(lastTime(a.id)-lastTime(b.id))
                 || ((seenBefore(a.id)?1:0)-(seenBefore(b.id)?1:0))
                 || (((S.att[a.id]||{}).t||0)-((S.att[b.id]||{}).t||0))
                 || (Math.random()-0.5);
  // ...but each band reserves about a third of its slots for items previously got wrong,
  // so a retake re-tests the weak spots instead of only rotating in new questions.
  const take=(band,n)=>{
    if(n<=0)return[];
    const keep=Math.min(Math.floor(n/3),band.filter(q=>gotWrong(q.id)).length);
    const missed=band.filter(q=>gotWrong(q.id)).sort(rank).slice(0,keep);
    const got={};missed.forEach(q=>{got[q.id]=1});
    return missed.concat(band.filter(q=>!got[q.id]).sort(rank).slice(0,n-missed.length));
  };
  const out=[];
  if(mix){
    Object.keys(mix).forEach(d=>{
      out.push.apply(out,take(pool.filter(q=>(q.diff||"moderate")===d),mix[d]));
    });
  }
  // top up from whatever is left if a band was short, or if no mix is set
  if(out.length<want){
    const have={};out.forEach(q=>{have[q.id]=1});
    out.push.apply(out,pool.filter(q=>!have[q.id]).sort(rank).slice(0,want-out.length));
  }
  // present them interleaved rather than easy-block then hard-block
  return spreadKeys(out.slice(0,want),pool).sort(()=>Math.random()-0.5);
}
/* The pools are keyed evenly, but a random draw of ten can still hand a third of its
   answers to one letter, and a candidate who guesses that letter throughout scores on it.
   Swap the surplus for same-band reserves whose key is under-represented. */
function spreadKeys(list,pool){
  const keyOf=q=>{const o=q.options||[];const k=o.indexOf(q.answer);return k>=0?"ABCD"[k]:String(q.answer)};
  const cap=Math.max(2,Math.ceil(list.length/4)+1);          // ten questions -> at most 4 of any letter
  const have={};list.forEach(q=>{have[q.id]=1});
  for(let guard=0;guard<12;guard++){
    const tally={};list.forEach(q=>{const k=keyOf(q);tally[k]=(tally[k]||0)+1});
    const over=Object.keys(tally).filter(k=>tally[k]>cap).sort((a,b)=>tally[b]-tally[a])[0];
    if(!over)break;
    const k=list.findIndex(q=>keyOf(q)===over);
    const band=(list[k].diff||"moderate");
    const alt=pool.filter(q=>!have[q.id]&&(q.diff||"moderate")===band&&(tally[keyOf(q)]||0)<cap);
    if(!alt.length)break;
    const pick=alt[Math.floor(Math.random()*alt.length)];
    delete have[list[k].id];have[pick.id]=1;list[k]=pick;
  }
  return list;
}
async function startQuiz(les){
  const sc=les.scenes.filter(s=>s.kind==="quiz")[0];
  if(!sc||!sc.setId){toast("This lesson has no mastery set attached");return}
  let pool=await loadSet(sc.setId);
  const dropped=pool.filter(isFree).length;
  pool=pool.filter(q=>!isFree(q));
  if(!pool.length){toast("The mastery set for this topic has not been authored yet");return}
  const pol=les.mastery,r=S.mastery[les.topicId]||{};
  const list=drawPaper(pool,pol,r.served||[]);
  if(list.length<pol.minQ)toast("Only "+list.length+" scorable questions — the policy wants "+pol.minQ);
  if(dropped)toast(dropped+" write-in item"+(dropped>1?"s":"")+" left out: a pass/fail test has to be machine-scored");
  S.learn.quiz={list:list,i:0,ans:{},conf:{},free:{},self:{},done:false,t0:now(),
                pool:pool.length,repeat:list.filter(q=>(r.served||[]).indexOf(q.id)>=0).length};
  render();window.scrollTo(0,0);
}
function redrawViz(){
  const L=S.learn,les=S.lessons[L.topicId];if(!les||L.i<0)return;
  const sc=les.scenes[L.i];if(!sc||sc.kind!=="explore")return;
  const C=VIZ[sc.viz.type];if(!C)return;
  const st=vizState(sc),out=C.draw(st),box=document.querySelector("#vizbox");if(!box)return;
  box.querySelector(".vizsvg").innerHTML=out.svg;
  box.querySelector(".vizread").innerHTML=out.read.map(r=>'<div class="vr"><span>'+esc(r[0])+'</span><b class="num">'+esc(r[1])+'</b></div>').join("");
  box.querySelector(".vnote").textContent=out.note;
  C.controls(st).forEach(c=>{const o=box.querySelector('[data-vo="'+c.k+'"]');if(o)o.textContent=c.fmt(c.val)});
}

function wire(){try{wireAll()}catch(e){
  // a half-wired page looks like buttons that do nothing; say so rather than sit there
  console.error("wire failed",e);
  S.wireErr=(e&&e.message)||String(e);
  const bar=document.querySelector("#wireErr");
  if(bar){bar.hidden=false;bar.textContent="Some controls failed to bind ("+S.wireErr+"). Reload the page \u2014 if it persists, Admin \u2192 Diagnostics has the detail."}
}}
function wireAll(){
  if(typeof askSelectionWatch==="function")askSelectionWatch();
  document.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>{S.drill=null;go(b.dataset.tab)});
  const V=$("#v-"+S.route);if(!V)return;
  const on=(sel,fn)=>V.querySelectorAll(sel).forEach(e=>e.onclick=ev=>fn(e,ev));
  const one=(id,fn)=>{const e=V.querySelector(id);if(e)e.onclick=fn};

  /* --- front door --- */
  document.querySelectorAll("#hdProfile").forEach(e=>e.onclick=()=>signOut());
  on("[data-login]",e=>{const id=e.dataset.login;
    if(id==="me"){doLogin("me");return}
    const u=(S.users||[]).find(x=>x.id===id);
    if(u&&!u.pass){doLogin(id);return}
    S.askPass=S.askPass===id?"":id;S.passVal="";S.authErr="";render();
    setTimeout(()=>{const b=document.querySelector("#passBox");b&&b.focus()},40)});
  const pb=V.querySelector("#passBox");
  if(pb){pb.oninput=()=>{S.passVal=pb.value};
    pb.onkeydown=ev=>{if(ev.key==="Enter")doLogin(S.askPass,pb.value)}}
  one("#passGo",()=>{const i=V.querySelector("#passBox");doLogin(S.askPass,i?i.value:"")});

  /* --- gate recovery --- */
  one("#permOpen",async()=>{try{await S.perm.manage();await probePerms();if(!S.db)location.reload()}catch(e){toast("The permissions panel did not open — use the artifact's own menu")}});
  one("#permAsk",async()=>{try{await S.perm.request(["db","user"]);location.reload()}catch(e){toast("That request was not granted")}});
  one("#permReload",()=>location.reload());

  /* --- shared --- */
  on("[data-ask]",e=>runAsk(e.closest(".ask")));
  on("[data-go]",e=>{const id=e.dataset.go;S.open[id]=true;go("learn")});
  on("[data-jump]",e=>{const t=e.dataset.jump,mid=e.dataset.mid;
    if(t==="learn"&&mid){openTopic(mid);return}
    if(mid&&t==="bank"){S.filt.mod=mid;ensure([mid])}
    if(mid&&t==="admin"){S.pickMod=mid;S.pickTopic=""}
    go(t)});
  on("[data-tp]",e=>{const id=e.dataset.tp,s=+e.dataset.s;
    const st=S.topics[id]||(S.topics[id]={});st.s=s;st.t=now();saveTopics();render()});
  on("[data-drillmod]",async e=>{const id=e.dataset.drillmod;await ensure([id]);startDrill((S.bank[id]||[]).slice())});

  /* --- learn workspace --- */
  on("[data-mode]",e=>{S.mode=e.dataset.mode;S.cfg.mode=S.mode;saveCfg();render()});
  on("[data-paper]",e=>{const v=e.dataset.paper;
    S.paper=(v==="all")?"all":+v;S.cfg.paper=S.paper;saveCfg();render()});
  on("[data-mod]",e=>{const id=e.dataset.mod;S.open[id]=!S.open[id];render()});
  on("[data-topic]",e=>openTopic(e.dataset.topic));
  on("[data-nav-toggle]",()=>{S.navOpen=!S.navOpen;savePanels();render()});
  on("[data-alltopics]",()=>{resetLearn(null);S.route="learn";
    if(!narrow())S.navOpen=true;        // never land on a page with no way to navigate
    render();window.scrollTo(0,0)});
  on("[data-done]",e=>setDone(e.dataset.done,e.dataset.on==="1"));
  on("[data-resettopic]",e=>resetTopic(e.dataset.resettopic));
  on("[data-seen]",e=>{const p=e.dataset.seen.split("|");toggleSeen(p[0],p[1])});
  on("[data-reqk]",e=>{const i=e.dataset.reqk.lastIndexOf("|");
    const key=e.dataset.reqk.slice(0,i),k=e.dataset.reqk.slice(i+1);
    const box=V.querySelector("#reqText"),txt=box?box.value:"";
    S.reqUI[key]=Object.assign({},S.reqUI[key],{kind:k,txt:txt});render();
    const b2=V.querySelector("#reqText");if(b2){b2.value=txt;b2.focus()}});
  on("[data-found]",e=>{const p=e.dataset.found.split("|");
    S.learn.found=S.learn.found||{};
    const bag=S.learn.found[p[0]]=S.learn.found[p[0]]||{};
    bag[p[1]]=p[2];render()});
  on("[data-scen]",e=>{const id=e.dataset.scen;S.learn.scen=S.learn.scen||{};
    S.learn.scen[id]=!S.learn.scen[id];render();
    if(S.learn.scen[id]){const el=document.querySelector(".scenwrap");if(el)el.scrollIntoView({block:"nearest"})}});
  on("[data-noteopen]",e=>{S.noteUI=S.noteUI||{};S.noteUI[e.dataset.noteopen]=1;render();
    setTimeout(()=>{const b=document.querySelector("#noteBox");if(b)b.focus()},40)});
  on("[data-notesave]",e=>{const k=e.dataset.notesave.split("|");
    const box=V.querySelector("#noteBox");
    saveNote(k[0],k[1]==="_topic"?null:k[1],box?box.value:"");toast("Note saved")});
  on("[data-notedel]",e=>{const k=e.dataset.notedel.split("|");
    saveNote(k[0],k[1]==="_topic"?null:k[1],"");toast("Note deleted")});
  /* ---- Ask Claude, from anywhere ---- */
  on("[data-askopen]",e=>{askOpen(e.dataset.sel||"",e.dataset.intent||"")});
  on("[data-askchip]",()=>{const c=S.askChip;askOpen((c&&c.text)||"","define")});
  // on(sel,fn) calls fn(element, event) — the element is first. Comparing e.target to
  // e.currentTarget on the element compares two undefineds, which closed the panel on
  // every click inside it. Use the event, and only close on the backdrop itself.
  on("[data-askclose]",(el,ev)=>{
    if(el.dataset.askclose==="bg"&&ev&&ev.target!==el)return;
    askClose()});
  on("[data-askintent]",e=>{if(!S.ask)return;
    const t=V.querySelector("#askFree");if(t)S.ask.free=t.value;
    S.ask.intent=e.dataset.askintent;render();
    const t2=V.querySelector("#askFree");if(t2){t2.focus();t2.selectionStart=t2.value.length}});
  on("[data-asksend]",()=>{if(!S.ask)return;
    const t=V.querySelector("#askFree");if(t)S.ask.free=t.value;
    askRun()});
  on("[data-askhelp]",e=>{const A=S.ask;if(!A)return;
    const good=e.dataset.askhelp==="1";
    const last=(S.asks||[])[S.asks.length-1];
    if(last)last.helpful=good;
    saveAsks();
    toast(good?"Noted — thank you":"Noted. This section is flagged for rewriting.");
    render()});
  on("[data-askdel]",e=>{const i=+e.dataset.askdel;
    const rs=(S.asks||[]).slice().sort((a,b)=>(b.ts||0)-(a.ts||0));
    const t=rs[i];if(!t)return;S.asks=S.asks.filter(x=>x!==t);saveAsks();render()});

  on("[data-reqopen]",()=>{S.reqModal={kind:"detail",text:"",files:[]};render();
    setTimeout(()=>{const b=document.querySelector("#reqText");if(b)b.focus()},50)});
  on("[data-reqclose]",(e,ev)=>{if(e.classList.contains("modalwrap")&&ev.target!==e)return;
    const b=V.querySelector("#reqText");if(b&&S.reqModal)S.reqModal.text=b.value;
    S.reqModal=null;render()});
  on("[data-reqkind]",e=>{const b=V.querySelector("#reqText");
    if(b&&S.reqModal)S.reqModal.text=b.value;
    S.reqModal.kind=e.dataset.reqkind;render()});
  on("[data-reqfiledel]",e=>{const b=V.querySelector("#reqText");
    if(b&&S.reqModal)S.reqModal.text=b.value;
    S.reqModal.files.splice(+e.dataset.reqfiledel,1);render()});
  const rf=V.querySelector("#reqFiles");
  if(rf)rf.onchange=async()=>{
    const box=V.querySelector("#reqText");if(box&&S.reqModal)S.reqModal.text=box.value;
    const LIM=400*1024;
    for(const f of Array.from(rf.files||[]).slice(0,6)){
      const rec={name:f.name,size:f.size,type:f.type||"",kept:false};
      if(f.size<=LIM){
        try{rec.data=await new Promise((res,rej)=>{const r=new FileReader();
          r.onload=()=>res(r.result);r.onerror=rej;r.readAsDataURL(f)});rec.kept=true}
        catch(e){}
      }
      S.reqModal.files.push(rec);
    }
    render();
  };
  const rs3=V.querySelector("#reqSend");
  if(rs3)rs3.onclick=()=>{
    const box=V.querySelector("#reqText"),txt=(box&&box.value||"").trim();
    if(!txt){toast("Say what you need \u2014 it is saved with the section reference");return}
    const les=S.lessons[S.learn.topicId];
    const sc=les&&S.learn.i>=0?les.scenes[S.learn.i]:null;
    S.reqs.push({ts:now(),topicId:S.learn.topicId||"general",sceneId:sc?sc.id:"overview",
      topic:les?les.title:"General",scene:sc?sc.title:"Whole lesson",
      kind:S.reqModal.kind||"detail",text:txt.slice(0,2000),profile:S.profile,
      files:(S.reqModal.files||[]).map(f=>({name:f.name,size:f.size,type:f.type,kept:!!f.kept,data:f.data}))});
    saveReqs();saveFb();S.reqModal=null;render();
    toast("Request filed \u2014 Admin \u2192 Requests has it");
  };
  on("[data-reqnew]",e=>{delete S.reqUI[e.dataset.reqnew];render()});
  on("[data-reqdel]",e=>{const rs=(S.reqs||[]).slice().sort((a,b)=>(b.ts||0)-(a.ts||0));
    const t=rs[+e.dataset.reqdel];if(!t)return;
    S.reqs=S.reqs.filter(x=>x!==t);saveReqs();saveFb();render()});
  const ac=V.querySelector("#askCopy");
  if(ac)ac.onclick=()=>copy(askBrief());
  const as2=V.querySelector("#askSave");
  if(as2)as2.onclick=()=>saveFile("content-gaps-from-questions.md",askBrief());
  const rc=V.querySelector("#reqCopy");
  if(rc)rc.onclick=()=>copy(reqBrief());
  const rs2=V.querySelector("#reqSave");
  if(rs2)rs2.onclick=()=>saveFile("content-requests.md",reqBrief());
  on("[data-reqsend]",e=>{
    const key=e.dataset.reqsend,box=V.querySelector("#reqText");
    const txt=(box&&box.value||"").trim();
    if(!txt){toast("Say what you need and it will be saved with the section reference");return}
    const parts=key.split("|"),les=S.lessons[S.learn.topicId];
    S.reqs.push({ts:now(),topicId:parts[0],sceneId:parts[1],
      topic:les?les.title:parts[0],
      scene:(les&&(les.scenes.filter(x=>x.id===parts[1])[0]||{}).title)||parts[1],
      kind:(S.reqUI[key]||{}).kind||"detail",text:txt.slice(0,1200),profile:S.profile});
    saveReqs();saveFb();S.reqUI[key]={sent:1};render();
    toast("Request saved — Admin → Requests lists them all")});
  on("[data-aide]",e=>{S.aideOpen=e.dataset.aide==="1";savePanels();render()});
  // drag the grips to resize; double-click one to collapse that side
  V.querySelectorAll("[data-grip]").forEach(g=>{
    const side=g.dataset.grip;
    g.ondblclick=()=>{if(side==="nav")S.navOpen=false;else S.aideOpen=false;savePanels();render()};
    g.onpointerdown=ev=>{
      ev.preventDefault();g.setPointerCapture(ev.pointerId);g.classList.add("on");
      const ws=g.closest(".ws"),box=ws.getBoundingClientRect();
      const move=e=>{
        const w=side==="nav"?(e.clientX-box.left):(box.right-e.clientX);
        const v=cl(Math.round(w),200,Math.min(520,Math.round(box.width*0.42)));
        if(side==="nav"){S.navW=v;ws.style.setProperty("--navw",v+"px")}
        else{S.aideW=v;ws.style.setProperty("--aidew",v+"px")}
      };
      const up=()=>{g.classList.remove("on");g.releasePointerCapture(ev.pointerId);
        window.removeEventListener("pointermove",move);window.removeEventListener("pointerup",up);
        savePanels();redrawViz()};
      window.addEventListener("pointermove",move);window.addEventListener("pointerup",up);
    };
  });
  // Navigation must never fail in silence. If anything inside throws, the click used to
  // leave the page untouched with no message, which is indistinguishable from a dead button.
  on("[data-sc]",e=>{
    const i=+e.dataset.sc;
    try{gotoScene(i)}
    catch(err){
      const L=S.learn,les=L&&S.lessons[L.topicId];
      // Put the whole diagnosis on the page. A toast disappears and most people will not
      // open a console, so a failure that cannot be reproduced locally stays invisible.
      const info=["section "+(i+1)+"  topic "+((L&&L.topicId)||"?"),
        "lesson: "+(les===undefined?"undefined":les===null?"null":les===false?"false":
          ("object, "+((les.scenes||[]).length)+" scenes")),
        "scene id: "+(((les&&les.scenes||[])[i]||{}).id||"?")+
          "   kind: "+(((les&&les.scenes||[])[i]||{}).kind||"?"),
        "", String((err&&err.message)||err),
        String((err&&err.stack)||"").split("\n").slice(1,5).join("\n")].join("\n");
      try{console.error("gotoScene("+i+") failed",err,info)}catch(_){}
      try{
        let box=document.getElementById("navErrBox");
        if(!box){box=document.createElement("div");box.id="navErrBox";
          box.setAttribute("style","position:fixed;left:12px;right:12px;bottom:12px;z-index:99999;"+
            "background:#2a0d12;color:#ffd9e0;border:1px solid #ff7a96;border-radius:12px;"+
            "padding:12px 14px;font:12px/1.45 ui-monospace,Menlo,Consolas,monospace;"+
            "white-space:pre-wrap;max-height:46vh;overflow:auto;box-shadow:0 8px 30px rgba(0,0,0,.5)");
          document.body.appendChild(box);}
        box.textContent="Navigation failed — please screenshot this\n\n"+info;
      }catch(_){toast("Could not open section "+(i+1)+": "+((err&&err.message)||"error"))}
    }
  });
  on("[data-revsheet]",()=>{S.learn.showRev=!S.learn.showRev;render()});
  on("[data-flip]",e=>{const k=+e.dataset.flip;S.learn.flip=S.learn.flip||{};
    S.learn.flip[k]=!S.learn.flip[k];render()});
  on("[data-step]",e=>{const id=e.dataset.step;S.learn.steps=S.learn.steps||{};
    S.learn.steps[id]=(S.learn.steps[id]||1)+1;render()});
  on("[data-rev]",e=>{const p=e.dataset.rev.split("|");S.learn.reveal=S.learn.reveal||{};
    (S.learn.reveal[p[0]]=S.learn.reveal[p[0]]||{})[p[1]]=1;render()});
  on("[data-tv]",e=>{const p=e.dataset.tv.split("|");S.learn.verd=S.learn.verd||{};
    (S.learn.verd[p[0]]=S.learn.verd[p[0]]||{})[p[1]]=p[2];render()});
  on("[data-hint]",e=>{const id=e.dataset.hint;S.learn.hints=S.learn.hints||{};
    S.learn.hints[id]=(S.learn.hints[id]||0)+1;captureText();render()});
  on("[data-sol]",e=>{captureText();S.learn.solShown=S.learn.solShown||{};S.learn.solShown[e.dataset.sol]=1;render()});
  on("[data-nudge]",e=>{captureText();S.learn.nudge=S.learn.nudge||{};S.learn.nudge[e.dataset.nudge]=1;render()});
  on("[data-startquiz]",()=>{const les=S.lessons[S.learn.topicId];if(les)startQuiz(les)});
  // completion blanks
  on("[data-bchk]",e=>{const p=e.dataset.bchk.split("|"),les=S.lessons[S.learn.topicId];
    const sc=les.scenes.filter(x=>x.id===p[0])[0],b=sc.steps[+p[1]].blank;
    const inp=V.querySelector('[data-bk="'+e.dataset.bchk+'"]');
    const norm=s=>String(s||"").toLowerCase().replace(/[\s,]/g,"").replace(/[−–—]/g,"-").replace(/\*/g,"");
    const got=norm(inp.value);
    // a shorter form may match as a substring, but only if it agrees on the leading sign:
    // "x/λ²" must not be accepted for "−x/λ²".
    const sign=s=>s.charAt(0)==="-"?"-":"+";
    const ok=got.length>0&&[b.answer].concat(b.accept||[]).some(a=>{const A=norm(a);
      return A===got||(got.length>3&&A.indexOf(got)>=0&&sign(A)===sign(got))});
    S.learn.blanks=S.learn.blanks||{};const bag=S.learn.blanks[p[0]]=S.learn.blanks[p[0]]||{};
    const cur=bag[p[1]]||{};
    if(ok)bag[p[1]]={ok:true,val:inp.value};
    else bag[p[1]]={val:inp.value,wrong:true,hint:cur.hint,tries:(cur.tries||0)+1};
    render()});
  on("[data-bhint]",e=>{const p=e.dataset.bhint.split("|");S.learn.blanks=S.learn.blanks||{};
    const bag=S.learn.blanks[p[0]]=S.learn.blanks[p[0]]||{};
    const inp=V.querySelector('[data-bk="'+e.dataset.bhint+'"]');
    bag[p[1]]=Object.assign({},bag[p[1]],{hint:1,val:inp?inp.value:""});
    S.learn.hints[p[0]]=(S.learn.hints[p[0]]||0)+1;render()});
  on("[data-bshow]",e=>{const p=e.dataset.bshow.split("|");S.learn.blanks=S.learn.blanks||{};
    (S.learn.blanks[p[0]]=S.learn.blanks[p[0]]||{})[p[1]]={ok:false};
    S.learn.hints[p[0]]=(S.learn.hints[p[0]]||0)+3;render()});
  V.querySelectorAll("[data-vz]").forEach(inp=>{inp.oninput=()=>{
    const les=S.lessons[S.learn.topicId],sc=les.scenes[S.learn.i];
    const st=vizState(sc);st[inp.dataset.vz]=+inp.value;redrawViz()}});
  const dlrev=V.querySelector("[data-dlrev]");
  if(dlrev)dlrev.onclick=()=>{const les=S.lessons[S.learn.topicId];
    saveFile("revision-"+les.id+".md","# "+les.title+" — revision sheet\n\n"+
      les.revision.sheet.map(x=>"- "+x).join("\n")+"\n\n## Flashcards\n\n"+
      les.revision.cards.map(c=>"**"+c[0]+"**\n: "+c[1]).join("\n\n")+"\n\n## Traps\n\n"+
      les.traps.map(x=>"- "+x).join("\n"))};
  // socratic check
  one("#checkSay",async()=>{
    captureText();
    const les=S.lessons[S.learn.topicId],sc=les.scenes[S.learn.i];
    const said=(S.learn.said||{})[sc.id]||"";
    const out=V.querySelector("#sayOut");out.hidden=false;
    if(!said.trim()){out.textContent="Write something first — even a wrong sentence is worth more than a blank box.";return}
    if(!S.sampleFn){out.textContent="Claude is not available in this view.";return}
    out.textContent="Thinking…";
    try{const r=await S.sampleFn(
      "A UGC NET Statistics candidate is working through a lesson on "+les.title+". The scene asked them: \""+sc.ask.q+"\"\n"+
      "They answered: \""+said+"\"\n\nJudge their reasoning. Say what is right in it first. If something is wrong or missing, name it precisely — but do NOT supply the full answer; ask them one question that would lead them to it. If they have it, say so plainly and add the one refinement that would make it exam-proof. Under 110 words, plain text.",
      {modelTier:"default",onText:({text})=>{out.textContent=text}});
      out.textContent=r.text||out.textContent}
    catch(e){out.textContent="Could not reach Claude"+(e&&e.code?" ("+e.code+")":"")+"."}});
  one("#gradeMe",async()=>{
    captureText();
    const les=S.lessons[S.learn.topicId],sc=les.scenes[S.learn.i];
    const said=(S.learn.said||{})[sc.id]||"";
    const out=V.querySelector("#sayOut");out.hidden=false;
    if(!said.trim()){out.textContent="Write your working or your final answer first.";return}
    if(!S.sampleFn){out.textContent="Claude is not available in this view.";return}
    out.textContent="Checking…";
    try{const r=await S.sampleFn(
      "Problem: "+sc.problem+"\nThe correct answer is: "+sc.answer+"\n"+
      "A UGC NET Statistics candidate wrote: \""+said+"\"\n\n"+
      "Mark it. If it is right, say so in one line and state the single check that would have confirmed it in the exam. If it is wrong, find the FIRST step that goes wrong and name only that — do not rewrite the whole solution, and do not give the next step away. If they reported the wrong quantity rather than making a maths error, say that explicitly, because that is their recurring failure. Under 120 words, plain text.",
      {modelTier:"complex",onText:({text})=>{out.textContent=text}});
      out.textContent=r.text||out.textContent}
    catch(e){out.textContent="Could not reach Claude"+(e&&e.code?" ("+e.code+")":"")+"."}});
  /* --- mastery quiz --- */
  const Q=S.learn.quiz;
  if(Q&&!Q.done){
    on("[data-qopt]",e=>{Q.ans[Q.i]=e.dataset.qopt;render()});
    on("[data-conf]",e=>{Q.conf[Q.i]=+e.dataset.conf;render()});
    on("[data-qgo]",e=>{captureText();Q.i=cl(+e.dataset.qgo,0,Q.list.length-1);render();window.scrollTo(0,0)});
    const qsub=()=>{captureText();
      const miss=Q.list.length-Object.keys(Q.ans).length;
      if(miss>0&&!Q.confirmed){Q.confirmed=true;toast(miss+" unanswered — press Submit again to finish");return}
      gradeQuiz();render();window.scrollTo(0,0)};
    one("#quizSubmit",qsub);one("#quizSubmit2",qsub);
  }

  /* --- bank --- */
  ["fMod","fFmt","fSrc","fSt"].forEach(id=>{const el=V.querySelector("#"+id);if(!el)return;
    el.onchange=async()=>{S.filt={mod:V.querySelector("#fMod").value,fmt:V.querySelector("#fFmt").value,
      src:V.querySelector("#fSrc").value,st:V.querySelector("#fSt").value,paper:S.filt.paper};
      if(S.filt.mod)await ensure([S.filt.mod]);else await ensure(mods().map(m=>m.id).filter(id=>loadedCount(id)));
      render()}});
  on("[data-q]",e=>{const id=e.dataset.q,all=allQ(),i=all.findIndex(q=>q.id===id);
    if(i<0){toast("Load that module first");return}S.mock=null;startDrill(all,i)});
  one("#drillAll",()=>{const f=S.filt;let list=f.mod?(S.bank[f.mod]||[]):allQ();
    if(f.paper)list=list.filter(q=>{const m=modById(q.moduleId);return m&&String(m.paper)===f.paper});
    if(f.fmt==="free")list=list.filter(isFree);else if(f.fmt)list=list.filter(q=>q.format===f.fmt&&!isFree(q));
    if(f.src)list=list.filter(q=>q.source===f.src);
    if(f.st)list=list.filter(q=>f.st==="flag"?((S.att[q.id]||{}).f):statusOf(q.id)===f.st);
    startDrill(list)});

  /* --- drill --- */
  if(S.drill){const D=S.drill,q=D.list[D.i];
    on("[data-exit]",()=>{S.drill=null;render()});
    on("[data-nav]",e=>{const t=V.querySelector("#freeAns");if(t)D.free=t.value;
      D.i=cl(D.i+ +e.dataset.nav,0,D.list.length-1);D.pick=null;D.verd={};D.wrote=false;D.checked=false;
      D.matched=false;D.shown=false;D.err=null;D.self=null;D.free="";render();window.scrollTo(0,0)});
    on("[data-opt]",e=>{if(D.shown)return;D.pick=e.dataset.opt;render()});
    on("[data-v]",e=>{if(D.shown)return;const p=e.dataset.v.split("|");D.verd[p[0]]=p[1];render()});
    on("[data-w]",()=>{D.wrote=!D.wrote;render()});
    on("[data-c]",()=>{D.checked=!D.checked;render()});
    on("[data-mt]",()=>{D.matched=!D.matched;render()});
    on("[data-flag]",e=>{flagQ(e.dataset.flag);render()});
    on("[data-err]",e=>{if(D.err===e.dataset.err)return;D.err=e.dataset.err;logErr(q,e.dataset.err);render()});
    on("[data-self]",e=>{D.self=e.dataset.self==="1";record(q,D.self);render()});
    const fa=V.querySelector("#freeAns");if(fa)fa.oninput=()=>{D.free=fa.value};
    one("#reveal",()=>{if(fa)D.free=fa.value;D.shown=true;
      if(!isFree(q))record(q,D.pick===q.answer);render()});
  }

  /* --- mock --- */
  const mkM=V.querySelector("#mkMins"),mkNsel=V.querySelector("#mkN");
  if(mkM&&mkNsel){
    const lab=V.querySelector("#mkCount");
    const sync=()=>{const m=+mkM.value;mkNsel.disabled=!!m;
      const want=m?Math.max(5,Math.round(m*60/PACE)):+mkNsel.value;
      if(lab)lab.textContent=m?("this paper: "+want+" questions, "+m+" minutes at exam pace")
                              :("about "+Math.round(want*PACE/60)+" minutes at exam pace");};
    mkNsel.onchange=sync;
    mkM.onchange=sync;sync();
  }
  const mkS=V.querySelector("#mkStart");if(mkS)mkS.onclick=async()=>{
    const mins=+((V.querySelector("#mkMins")||{}).value||0);
    // the time you have decides the length, unless you asked to set it yourself
    const n=mins?Math.max(5,Math.round(mins*60/PACE)):+V.querySelector("#mkN").value;
    const scope=V.querySelector("#mkScope").value,
      timed=V.querySelector("#mkTimer").value==="1",pass=+V.querySelector("#mkPass").value;
    mkS.disabled=true;mkS.textContent="Loading questions…";
    await ensure(mods(scope==="all"?null:2).map(m=>m.id).filter(id=>loadedCount(id)));
    const list=buildMock(n,scope,pass);
    if(!list||!list.length){mkS.disabled=false;mkS.textContent="Start mock";toast("Not enough questions in the bank for that scope");return}
    S.mock={list:list,i:0,ans:{},t0:now(),timed:timed,budget:list.length*PACE,pass:pass,scope:scope,done:false};
    if(timed)S.mock.tick=setInterval(()=>{const c=$("#mkClock");if(!c||!S.mock||S.mock.done)return;
      const l=S.mock.budget-(now()-S.mock.t0)/1000;c.textContent=(l<0?"+":"")+hhmm(Math.abs(l));c.classList.toggle("over",l<0)},1000);
    render();window.scrollTo(0,0)};
  if(S.mock&&!S.mock.done){const M=S.mock;
    on("[data-mopt]",e=>{M.ans[M.i]=e.dataset.mopt;if(M.i<M.list.length-1)M.i++;render()});
    on("[data-mnav]",e=>{M.i=cl(M.i+ +e.dataset.mnav,0,M.list.length-1);render()});
    on("[data-mclear]",()=>{delete M.ans[M.i];render()});
    on("[data-mgo]",e=>{M.i=+e.dataset.mgo;render();window.scrollTo(0,0)});
    const sub=()=>{if(Object.keys(M.ans).length<M.list.length&&!M.confirmed){M.confirmed=true;
      toast(M.list.length-Object.keys(M.ans).length+" unanswered — press Submit again to finish");return}submitMock()};
    one("#mkSubmit",sub);one("#mkSubmit2",sub);
  }
  one("#mkExit",()=>{S.mock=null;render()});

  /* --- progress --- */
  const progressRecords=["attempts","mocks","topics","errors","config","mastery","requests","notes","asks"];
  const progressPath=n=>"data/users/"+S.uid+"/"+upath(n);
  const plainObject=x=>!!x&&typeof x==="object"&&!Array.isArray(x)&&(Object.getPrototypeOf(x)===Object.prototype||Object.getPrototypeOf(x)===null);
  function jsonSafe(x,depth){
    if(depth>12)return false;
    if(x===null||typeof x==="string"||typeof x==="boolean")return true;
    if(typeof x==="number")return Number.isFinite(x);
    if(Array.isArray(x))return x.length<=10000&&x.every(v=>jsonSafe(v,depth+1));
    if(!plainObject(x))return false;
    return Object.keys(x).length<=20000&&Object.keys(x).every(k=>
      k!=="__proto__"&&k!=="constructor"&&k!=="prototype"&&jsonSafe(x[k],depth+1));
  }
  const objectMap=x=>plainObject(x)&&Object.keys(x).every(k=>plainObject(x[k]));
  const objectList=x=>Array.isArray(x)&&x.length<=10000&&x.every(plainObject);
  function validateProgressRecord(n,v){
    if(v===null)return true;
    if(!plainObject(v)||!jsonSafe(v,0))return false;
    if((n==="attempts"||n==="mastery")&&v.v!=null&&v.v!==SCHEMA)return false;
    if(n==="attempts")return Object.keys(v).every(k=>["a","v"].includes(k))&&plainObject(v.a)&&objectMap(v.a);
    if(n==="mocks"||n==="errors"||n==="requests"||n==="asks")
      return Object.keys(v).every(k=>k==="list")&&objectList(v.list);
    if(n==="topics")return Object.keys(v).every(k=>k==="t")&&objectMap(v.t);
    if(n==="mastery")return Object.keys(v).every(k=>["m","v"].includes(k))&&plainObject(v.m)&&objectMap(v.m);
    if(n==="notes")return Object.keys(v).every(k=>k==="n")&&plainObject(v.n)&&jsonSafe(v.n,0);
    if(n==="config"){
      if(v.exam!=null&&typeof v.exam!=="string")return false;
      if(v.target!=null&&(!Number.isFinite(v.target)||v.target<60||v.target>200))return false;
      if(v.mode!=null&&!Object.prototype.hasOwnProperty.call(MODES,v.mode))return false;
      if(v.paper!=null&&![1,2,"all"].includes(v.paper))return false;
      return true;
    }
    return false;
  }
  function emptyProgressRecord(n,v){
    if(v===null)return true;
    if(n==="attempts")return Object.keys(v.a||{}).length===0;
    if(n==="topics")return Object.keys(v.t||{}).length===0;
    if(n==="mastery")return Object.keys(v.m||{}).length===0;
    if(n==="notes")return Object.keys(v.n||{}).length===0;
    if(n==="config")return Object.keys(v).filter(k=>k!=="v").length===0;
    return !((v.list||[]).length);
  }
  function sameJson(a,b){return JSON.stringify(a)===JSON.stringify(b)}
  async function readProgressRecord(n){
    const snap=await S.db.doc(progressPath(n)).get();
    return snap.exists?snap.data():null;
  }
  async function verifyProgressWrite(path,value){
    const snap=await S.db.doc(path).get();
    const actual=snap.exists?snap.data():null;
    if(!sameJson(actual,value))throw new Error("Read-back verification failed for "+path.split("/").pop());
    // The hosted static adapter can fall back to in-memory storage when localStorage is
    // unavailable or full. A database read-back alone would then give a false success.
    try{
      if(localStorage.getItem("njuid")!==null){
        const raw=localStorage.getItem("njdb:"+path);
        if(value===null){if(raw!==null)throw new Error("Durability check failed for "+path.split("/").pop())}
        else if(raw===null||!sameJson(JSON.parse(raw),value))throw new Error("Durability check failed for "+path.split("/").pop());
      }
    }catch(e){if(e&&/Durability check/.test(e.message))throw e;
      throw new Error("Could not verify browser storage durability")}
  }
  async function flushProgressPending(){
    for(const n of progressRecords){
      if(!Object.prototype.hasOwnProperty.call(PEND,n))continue;
      if(save["t_"+n]){clearTimeout(save["t_"+n]);delete save["t_"+n]}
      const body=PEND[n];delete PEND[n];
      await S.db.doc(progressPath(n)).set(body);
      await verifyProgressWrite(progressPath(n),body);
    }
  }
  const progressExport=V.querySelector("#progressExport");
  if(progressExport)progressExport.onclick=async()=>{
    if(!S.db||!S.uid){toast("Learner progress is not available");return}
    progressExport.disabled=true;
    try{
      await flushProgressPending();
      const records={};
      for(const n of progressRecords)records[n]=await readProgressRecord(n);
      const backup={format:"net-jrf-statistics-progress",version:1,schemaVersion:SCHEMA,
        exportedAt:new Date().toISOString(),sourceUserId:S.uid,records};
      const blob=new Blob([JSON.stringify(backup,null,2)],{type:"application/json"});
      const url=URL.createObjectURL(blob),a=document.createElement("a");
      a.href=url;a.download="net-jrf-progress-"+dayStr(now())+".json";
      document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
      toast("Progress backup downloaded");
    }catch(e){toast("Backup failed: "+((e&&e.message)||"unknown error"))}
    finally{progressExport.disabled=false}
  };
  const progressImportBtn=V.querySelector("#progressImportBtn"),progressImportFile=V.querySelector("#progressImportFile");
  if(progressImportBtn&&progressImportFile){
    progressImportBtn.onclick=()=>progressImportFile.click();
    progressImportFile.onchange=async()=>{
      const file=progressImportFile.files&&progressImportFile.files[0];if(!file)return;
      let progressImported=false;
      try{
        const backup=JSON.parse(await file.text()),names=progressRecords;
        if(!plainObject(backup)||backup.format!=="net-jrf-statistics-progress"||backup.version!==1||
           backup.schemaVersion!==SCHEMA||!plainObject(backup.records)||
           names.some(n=>!Object.prototype.hasOwnProperty.call(backup.records,n))||
           Object.keys(backup.records).some(n=>names.indexOf(n)<0)){
          toast("Unsupported backup format or schema version");return;
        }
        for(const n of names)if(!validateProgressRecord(n,backup.records[n])){
          toast("Backup validation failed: "+n+" has an invalid structure");return;
        }
        if(names.every(n=>emptyProgressRecord(n,backup.records[n]))){
          toast("This backup contains no learner progress; nothing was imported");return;
        }
        if(!confirm("Import "+file.name+"? Current progress will first be snapshotted, then replaced. Continue?"))return;
        await flushProgressPending();
        const previous={};
        for(const n of names)previous[n]=await readProgressRecord(n);
        const snapshotId="preimport-"+Date.now().toString(36);
        const snapshotPath="data/users/"+S.uid+"/progress-snapshots/"+snapshotId;
        const snapshot={format:"net-jrf-statistics-preimport",version:1,createdAt:new Date().toISOString(),
          learnerId:S.uid,profile:S.profile||"me",records:previous};
        await S.db.doc(snapshotPath).set(snapshot);
        await verifyProgressWrite(snapshotPath,snapshot);
        for(const n of names){if(save["t_"+n]){clearTimeout(save["t_"+n]);delete save["t_"+n]}delete PEND[n]}
        const written=[];
        try{
          for(const n of names){
            const path=progressPath(n),ref=S.db.doc(path),value=backup.records[n];
            if(value===null)await ref.delete();else await ref.set(value);
            await verifyProgressWrite(path,value);
            written.push(n);
          }
        }catch(writeErr){
          const rollbackFailed=[];
          for(const n of names.slice().reverse()){
            try{
              const ref=S.db.doc(progressPath(n));
              if(previous[n]===null)await ref.delete();else await ref.set(previous[n]);
              await verifyProgressWrite(progressPath(n),previous[n]);
            }catch(rollbackErr){rollbackFailed.push(n)}
          }
          const detail=rollbackFailed.length
            ? " Rollback could not restore: "+rollbackFailed.join(", ")+". Pre-import snapshot: "+snapshotId+"."
            : " Previous records were restored. Pre-import snapshot: "+snapshotId+".";
          throw new Error((writeErr&&writeErr.message||"write failed")+"."+detail);
        }
        await loadProfileData();progressImported=true;
        let feedbackOk=true;
        try{
          if(saveFb.t){clearTimeout(saveFb.t);delete saveFb.t}
          const feedback={uid:S.uid,name:S.ownerName||"",label:S.profile||"me",
            asks:(S.asks||[]).slice(-200),reqs:(S.reqs||[]).slice(-200),updated:now()};
          await S.db.doc(fbPath()).set(feedback);
          const fbSnap=await S.db.doc(fbPath()).get();
          feedbackOk=!!(fbSnap.exists&&sameJson(fbSnap.data(),feedback));
        }catch(feedbackErr){feedbackOk=false}
        render();toast("Progress imported and verified. "+(feedbackOk?"Shared feedback refreshed. ":"Shared feedback refresh needs attention. ")+"Pre-import snapshot: "+snapshotId);
      }catch(e){toast((progressImported?"Progress imported; follow-up issue: ":"Import failed: ")+((e&&e.message)||"invalid backup"))}
      finally{progressImportFile.value=""}
    };
  }
  const la=V.querySelector("#loadAllBtn");if(la)la.onclick=async()=>{la.disabled=true;
    await loadAll((i,n)=>{la.textContent="Loading "+i+"/"+n});la.textContent="Loaded";render()};
  const ec=V.querySelector("#errClear");if(ec)ec.onclick=()=>{
    if(ec.dataset.c){S.errs=[];saveErrs();render()}else{ec.dataset.c="1";ec.textContent="Press again to clear "+S.errs.length}};
  /* --- admin --- */
  const rs=V.querySelector("#rescan");if(rs)rs.onclick=()=>{rs.disabled=true;rs.textContent="Scanning…";rescan()};
  one("#diagRun",e=>{const b=V.querySelector("#diagRun");b.disabled=true;b.textContent="Checking…";runDiag()});
  one("#diagCopy",()=>{const d=S.diag;if(!d)return;
    copy(d.rows.map(r=>(r[2]?"OK   ":"FAIL ")+r[0]+"  "+r[1]+"  "+(r[3]!==undefined?r[3]:"")).join("\n"))});
  on("[data-prompt]",e=>{S.pickMod=e.dataset.prompt;S.pickTopic="";render();
    setTimeout(()=>{const t=$("#pBox");t&&t.scrollIntoView({block:"center",behavior:"smooth"})},60)});
  const fm2=V.querySelector("#fMod2");if(fm2)fm2.onchange=()=>{S.pickMod=fm2.value;S.pickTopic="";render()};
  const ft=V.querySelector("#fTop");if(ft)ft.onchange=()=>{S.pickTopic=ft.value;render()};
  const fs=V.querySelector("#fStage");if(fs)fs.onchange=()=>{S.stage=fs.value;render()};
  one("#pCopy",()=>copy(V.querySelector("#pBox").value));
  one("#genRun",()=>{const m=modById(S.pickMod)||mods()[0];
    const t=m.topics.find(x=>x.id===S.pickTopic)||m.topics[0];
    if(!S.sampleFn){toast("Claude is not available in this view");return}
    runGen(S.stage||"lesson",m,t)});
  one("#genSave",()=>commitGen());
  one("#genPreview",()=>{S.gen.showJson=!S.gen.showJson;render()});
  one("#genDrop",()=>{S.gen=null;render()});
  const psv=V.querySelector("#pSave");if(psv)psv.onclick=()=>saveFile("prompt-"+(S.stage||"lesson")+"-"+(S.pickTopic||S.pickMod||"module")+".md",V.querySelector("#pBox").value);
  one("#usersSave",async()=>{
    await importMeta("users",V.querySelector("#usersBox").value,b=>{S.users=b.users||[]})});
  one("#persSave",async()=>{await importMeta("personal",V.querySelector("#persBox").value,b=>{S.personal=b})});
  one("#sylSave",async()=>{await importMeta("syllabus",V.querySelector("#sylBox").value,b=>{S.syl=b;
    if(b.order&&S.catalog)S.catalog.modules.forEach(m=>{if(b.order[m.id]!=null)m.sylOrder=b.order[m.id]})})});
  const ea=V.querySelector("#exportAll");if(ea)ea.onclick=async()=>{ea.disabled=true;await loadAll();
    saveFile("net-jrf-backup-"+dayStr(now())+".json",JSON.stringify({catalog:S.catalog,index:S.index,
      lessons:S.lessonIdx,bank:S.bank,attempts:S.att,mastery:S.mastery,mocks:S.mocks,topics:S.topics,
      errors:S.errs,config:S.cfg},null,1));ea.disabled=false};
  const eg=V.querySelector("#exGo");if(eg)eg.onclick=async()=>{const mid=V.querySelector("#exMod").value;
    eg.disabled=true;await ensure(mid?[mid]:mods().map(m=>m.id).filter(id=>loadedCount(id)));
    const md=exportMd(mid,V.querySelector("#exWhat").value);eg.disabled=false;
    if(!md){toast("Nothing matches that selection");return}
    saveFile("net-jrf-"+(mid||"all")+"-"+V.querySelector("#exWhat").value+".md",md)};
  const ecsv=V.querySelector("#exCsv");if(ecsv)ecsv.onclick=async()=>{ecsv.disabled=true;await loadAll();ecsv.disabled=false;saveFile("net-jrf-questions.csv",exportCsv())};

  /* --- settings --- */
  one("#cfgSave",()=>{S.cfg.exam=V.querySelector("#cfgExam").value||"";
    S.cfg.target=cl(+V.querySelector("#cfgTarget").value||150,60,200);
    saveCfg();toast("Saved");render()});
}
async function importMeta(doc,txt,after){
  if(!S.db){toast("No database in this view");return}
  let body;try{body=JSON.parse(txt)}catch(e){toast("That is not valid JSON");return}
  if(typeof body!=="object"||!body||Array.isArray(body)){toast("The top level must be an object");return}
  body.importedAt=new Date().toISOString();
  try{await S.db.doc("meta/"+doc).set(body);after&&after(body);toast("Imported");render()}
  catch(e){toast("Could not write ("+(e&&e.code||"error")+")")}
}
async function ensure(ids){
  const need=ids.filter(id=>!S.bank[id]&&loadedCount(id)>0);
  if(!need.length)return;
  for(const id of need)await loadBank(id);
}
