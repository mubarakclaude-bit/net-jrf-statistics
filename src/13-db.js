/* ===================== db layer ===================== */
async function boot(){
  if(typeof claude==="undefined"||!claude||typeof claude.use!=="function"){
    S.dbMsg="no-runtime";S.ready=true;render();return}
  S.boot="Asking this view for the database…";render();
  // every capability in parallel: a slow or unanswered grant must not hold the page hostage
  const use=n=>{try{return Promise.resolve(claude.use(n)).catch(()=>null)}catch(e){return Promise.resolve(null)}};
  const pDb=use("db"),pUser=use("user"),pSample=use("sample"),pDl=use("downloads"),pPerm=use("permissions");
  pSample.then(v=>{S.sampleFn=v;if(S.ready)render()});
  pDl.then(v=>{S.dl=v;if(S.ready)render()});
  pPerm.then(v=>{S.perm=v;probePerms()});
  const late=new Promise(r=>setTimeout(()=>r("late"),12000));
  const got=await Promise.race([Promise.all([pDb,pUser]),late]);
  if(got==="late"){
    S.dbMsg="slow";S.ready=true;render();
    Promise.all([pDb,pUser]).then(([d,u])=>{S.db=d;S.user=u;S.dbMsg=d?"":"not-available";
      if(d)afterDb();else render()});
    return;
  }
  S.db=got[0];S.user=got[1];
  if(!S.db){S.dbMsg="not-available";S.ready=true;render();return}
  await afterDb();
}
async function probePerms(){
  if(!S.perm||!S.perm.state)return;
  try{S.permState=await S.perm.state();if(S.ready)render()}catch(e){}
}
async function afterDb(){
  S.boot="Reading the syllabus and lessons…";if(S.ready)render();
  try{if(S.user&&S.user.id)S.uid=await S.user.id()}catch(e){}
  const rd=async p=>{try{const s=await S.db.doc(p).get();return s.exists?s.data():null}
    catch(e){S.readErr=(e&&e.code)||"error";return null}};
  try{
    const [cat,idx,app,les,per,syl]=await Promise.all(
      ["meta/catalog","meta/index","meta/app","meta/lessons","meta/personal","meta/syllabus"].map(rd));
    S.catalog=cat;S.index=idx;S.app=app;S.lessonIdx=les;S.personal=per;S.syl=syl;
    if(syl&&syl.order&&S.catalog&&S.catalog.modules)
      S.catalog.modules.forEach(m=>{if(syl.order[m.id]!=null)m.sylOrder=syl.order[m.id]});
  }catch(e){S.dbMsg="read-failed: "+((e&&e.code)||e)}
  await loadUsers();
  try{if(S.user&&S.user.me){const me=await S.user.me();S.ownerName=(me&&me.name)||""}}catch(e){}
  // Who is looking. Only the artifact's own owner gets Admin; everyone the artifact is
  // shared with is a learner, whatever level the share menu gave them.
  try{S.isAdmin=!!(S.user&&S.user.isOwner&&S.user.isOwner())}catch(e){S.isAdmin=false}
  // a remembered profile skips the front door; anything else stops there
  const want=recallProfile();
  if(want==="me"){S.profile="me";S.authed=true}
  else if(want&&(S.users||[]).some(u=>u.id===want)){S.profile=want;S.authed=true}
  if(S.authed){await loadProfileData();await loadFeedback();migrateFeedback()}
  S.boot="";S.ready=true;render();
  // live: content written from another chat appears without a reload
  try{
    S.db.doc("meta/catalog").onSnapshot(s=>{if(s.exists){S.catalog=s.data();if(S.ready)render()}},()=>{});
    S.db.doc("meta/index").onSnapshot(s=>{if(s.exists){S.index=s.data();if(S.ready)render()}},()=>{});
    S.db.doc("meta/lessons").onSnapshot(s=>{if(s.exists){S.lessonIdx=s.data();if(S.ready)render()}},()=>{});
  }catch(e){}
  if(S.catalog&&!S.index)rescan(true);
}
const PEND={};
function save(name,body){
  if(!S.db||!S.uid)return;
  const path="data/users/"+S.uid+"/"+upath(name);
  PEND[name]=body;
  if(save["t_"+name])clearTimeout(save["t_"+name]);
  save["t_"+name]=setTimeout(async()=>{
    const b=PEND[name];delete PEND[name];
    try{await S.db.doc(path).set(b)}catch(e){
      if(e&&e.code==="invalid_argument")toast("This view cannot save progress");
      else{try{await S.db.doc(path).set(b)}catch(e2){toast("Could not save progress")}}
    }
  },700);
}
function upath(name){
  // profile "me" keeps the original paths, so nothing already saved has to move
  return S.profile&&S.profile!=="me"
    ? "p/"+S.profile+"/"+name
    : name;
}
async function loadProfileData(){
  if(!S.db||!S.uid){S.att={};S.mocks=[];S.topics={};S.errs=[];S.mastery={};S.reqs=[];S.notes={};S.asks=[];return}
  const P="data/users/"+S.uid+"/";
  const rd=async p=>{try{const s=await S.db.doc(p).get();return s.exists?s.data():null}catch(e){return null}};
  const [a,m,t,er,c,ms,rq,nt,ak]=await Promise.all(["attempts","mocks","topics","errors","config","mastery","requests","notes","asks"]
    .map(n=>rd(P+upath(n))));
  S.att=(a&&a.a)||{};S.mocks=(m&&m.list)||[];S.topics=(t&&t.t)||{};
  S.errs=(er&&er.list)||[];S.cfg=c||{};S.mastery=(ms&&ms.m)||{};S.reqs=(rq&&rq.list)||[];S.notes=(nt&&nt.n)||{};S.asks=(ak&&ak.list)||[];
  if(S.cfg.mode&&MODES[S.cfg.mode])S.mode=S.cfg.mode;
  if(S.cfg.paper===1||S.cfg.paper===2||S.cfg.paper==="all")S.paper=S.cfg.paper;
  S.bank=S.bank||{};
}
const saveAtt=()=>save("attempts",{a:S.att,v:SCHEMA});
const saveMocks=()=>save("mocks",{list:S.mocks.slice(-60)});
const saveTopics=()=>save("topics",{t:S.topics});
const saveErrs=()=>save("errors",{list:S.errs.slice(-400)});
const saveCfg=()=>save("config",S.cfg);
const saveMastery=()=>save("mastery",{m:S.mastery,v:SCHEMA});
const saveReqs=()=>save("requests",{list:S.reqs.slice(-300)});
const saveNotes=()=>save("notes",{n:S.notes});
const saveAsks=()=>save("asks",{list:(S.asks||[]).slice(-400)});

/* ---- shared feedback, so the owner can see across learners ----
   Each viewer's asks and requests also go to feedback/<their id>, a SHARED path. The
   per-viewer data/users/<id>/ subtree is private even from the owner, so anything kept
   only there can never inform the content. The db rules make feedback readable by
   everyone and writable only by its own author (or the owner). */
function fbPath(){return S.uid?("feedback/"+S.uid):null}
const saveFb=()=>{
  const p=fbPath();if(!p||!S.db)return;
  if(saveFb.t)clearTimeout(saveFb.t);
  saveFb.t=setTimeout(async()=>{
    try{
      await S.db.doc(p).set({uid:S.uid,name:S.ownerName||"",label:S.profile||"me",
        asks:(S.asks||[]).slice(-200),reqs:(S.reqs||[]).slice(-200),updated:now()});
    }catch(e){S.fbErr=(e&&e.code)||"error"}
  },900);
};
/* The owner reads every learner's doc; a learner needs only their own. */
async function loadFeedback(){
  if(!S.db)return;
  try{
    if(S.isAdmin){
      const q=await S.db.collection("feedback").get();
      S.fb=q.docs.map(d=>Object.assign({id:d.id},d.data()||{}));
    }else{
      const p=fbPath();if(!p)return;
      const s=await S.db.doc(p).get();
      S.fb=s.exists?[Object.assign({id:S.uid},s.data()||{})]:[];
    }
  }catch(e){S.fbErr=(e&&e.code)||"error";S.fb=S.fb||[]}
}
/* One-time lift of anything already kept privately, so no history is lost. */
async function migrateFeedback(){
  if(!S.db||!S.uid)return;
  if(!((S.asks||[]).length||(S.reqs||[]).length))return;
  try{
    const s=await S.db.doc(fbPath()).get();
    const cur=s.exists?(s.data()||{}):null;
    if(cur&&((cur.asks||[]).length||(cur.reqs||[]).length))return;   // already lifted
    saveFb();
  }catch(e){}
}

async function loadBank(mid){
  if(S.bank[mid]||S.loading[mid]||!S.db)return S.bank[mid]||[];
  S.loading[mid]=true;
  try{
    const q=await S.db.collection("qsets").where("moduleId","==",mid).get();
    const items=[];const seen={};
    q.docs.forEach(d=>{const b=d.data()||{};
      if(b.source==="mastery")return;           // kept unseen for mastery tests
      (b.items||[]).forEach(it=>{
        if(!it||!it.id||seen[it.id])return;seen[it.id]=1;
        items.push(Object.assign({},it,{moduleId:mid,source:b.source||"variant",setId:d.id,setLabel:b.label||d.id}));
      })});
    S.bank[mid]=items;
  }catch(e){S.bank[mid]=[];toast("Could not load "+mid+" ("+(e&&e.code||"error")+")")}
  delete S.loading[mid];return S.bank[mid];
}
async function loadSet(setId){
  if(S.sets[setId]||!S.db)return S.sets[setId]||[];
  try{const s=await S.db.doc("qsets/"+setId).get();
    const b=s.exists?s.data():null;
    S.sets[setId]=b?(b.items||[]).map(it=>Object.assign({},it,{moduleId:b.moduleId,source:b.source||"mastery"})):[];
  }catch(e){S.sets[setId]=[]}
  return S.sets[setId];
}
async function loadLesson(tid){
  if(S.lessons[tid]!==undefined||!S.db)return S.lessons[tid];
  const ent=lessonFor(tid);
  if(!ent){S.lessons[tid]=false;return false}
  S.lessons[tid]=null;
  try{const s=await S.db.doc("lessons/"+ent.id).get();
    S.lessons[tid]=s.exists?s.data():false;
  }catch(e){
    // keep the failure visible and retryable rather than caching it for the session
    S.lessons[tid]=false;S.lessonErr=(S.lessonErr||{});S.lessonErr[tid]=(e&&e.code)||"error";
  }
  return S.lessons[tid];
}
async function loadAll(onp){
  const ms=mods();for(let i=0;i<ms.length;i++){if(!S.bank[ms[i].id])await loadBank(ms[i].id);onp&&onp(i+1,ms.length)}
}
async function rescan(quiet){
  if(!S.db)return;
  try{
    const q=await S.db.collection("qsets").get();
    const out={};
    q.docs.forEach(d=>{const b=d.data()||{};const mid=b.moduleId;if(!mid)return;
      const o=out[mid]||(out[mid]={total:0,pyq:0,variant:0,mastery:0,fmt:{},sets:[]});
      const items=b.items||[],src=b.source||"variant";
      if(src!=="mastery"){o.total+=items.length;o[src==="pyq"?"pyq":"variant"]+=items.length;
        items.forEach(it=>{const f=it&&it.format||"single";o.fmt[f]=(o.fmt[f]||0)+1})}
      else o.mastery+=items.length;
      o.sets.push({id:d.id,label:b.label||d.id,source:src,count:items.length});
    });
    const idx={modules:out,updated:new Date().toISOString(),docs:q.size,v:SCHEMA};
    await S.db.doc("meta/index").set(idx);S.index=idx;S.bank={};
    // index the lessons too, so the tree knows which topics have one
    const ls=await S.db.collection("lessons").get();
    const topics={};
    ls.docs.forEach(d=>{const b=d.data()||{};if(!b.topicId)return;
      topics[b.topicId]={id:d.id,title:b.title||d.id,moduleId:b.moduleId,estMin:b.estMin||20,
        scenes:(b.scenes||[]).length,status:b.status||"draft",version:b.version||"1.0"}});
    const li={topics:topics,updated:new Date().toISOString(),count:ls.size,v:SCHEMA};
    await S.db.doc("meta/lessons").set(li);S.lessonIdx=li;S.lessons={};
    if(!quiet)toast("Rescanned: "+q.size+" question sets, "+ls.size+" lessons");
    render();
  }catch(e){if(!quiet)toast("Rescan failed ("+(e&&e.code||"error")+")")}
}
