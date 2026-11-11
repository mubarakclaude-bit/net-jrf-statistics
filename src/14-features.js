/* ===================== features =====================
   The plug-in point, added once so that no feature ever has to edit shared wiring again.

   A feature is a folder, src/features/<id>/ : feature.json (manifest), index.js (the feature), test.js (its own browser
   test). tools/build-features.js scans that folder at build time, wraps each index.js in a private scope (so two features
   can never collide on a name) and appends one registerFeature(manifest, {render, wire}) call per feature just before
   boot. Nothing else lists features.

   What a feature may rely on is the ctx it receives:
     ctx.id, ctx.version            from its manifest
     ctx.profile, ctx.uid           the selected profile ("me" is the default) and the learner id
     ctx.esc(s)                     HTML-escape
     ctx.toast(message)             a short message
     ctx.rerender()                 draw the feature again
     ctx.route                      the route it is shown at: "f-<id>", or the built-in route it replaces (see below)
     ctx.app                        the host interface (version 2), see appApi() below: gate, overall, formatStats, errors,
                                    loadAll, clearErrors, settings.get/set (exam date, target), lessons(), learnProgress(),
                                    navigate(route), ui helpers and data tables. A feature never touches the app's internal
                                    state S or its global helpers directly.
     ctx.store.get/set/remove(key)  learner data. ONLY the keys declared in feature.json "storage"; each is stored at
                                    data/users/<uid>/features/<id>/<key> (under p/<profile>/ for a non-default profile),
                                    a path the storage contract allows. Any other key throws.
   A feature that throws while drawing shows an error card; it can never blank the rest of the app.

   A manifest may say "replaces": "<built-in route>" (tab must then be false). The feature is shown at that built-in route,
   in that route's place in the navigation bar, and the app no longer draws the built-in view. This is how a built-in view
   becomes a feature module without changing its address, its position or what the learner sees. */
const FEATURES={};

function makeFeatureStore(f){
  const declared=new Set(f.manifest.storage);
  const pathFor=key=>{
    if(!declared.has(key))throw new Error("feature '"+f.manifest.id+"': storage key '"+key+"' is not declared in its feature.json");
    return "data/users/"+S.uid+"/"+upath("features/"+f.manifest.id+"/"+key);
  };
  const need=()=>{if(!S.db||!S.uid)throw new Error("Learner storage is not available (not signed in)")};
  return{
    async get(key){const p=pathFor(key);if(!S.db||!S.uid)return null;
      const s=await S.db.doc(p).get();return s.exists?((s.data()||{}).value===undefined?null:s.data().value):null},
    async set(key,value){const p=pathFor(key);need();
      if(value===undefined)throw new Error("feature '"+f.manifest.id+"': cannot store undefined");
      await S.db.doc(p).set({v:1,value:value})},
    async remove(key){const p=pathFor(key);need();await S.db.doc(p).delete()}
  };
}

/* The host interface a feature may call (ctx.app). Small, read-mostly, and defined once here so that a view moved out of
   the core bundle reaches the app's logic through a named, documented surface and not through globals. Everything is looked
   up at call time. Adding to it is a core change (AGENTS.md, section C). */
function appApi(){
  return Object.freeze({
    gate:()=>gate(),                          /* "" when the app is ready, else the view to show instead */
    overall:paper=>overall(paper),            /* marks, projection and per-module status for paper 1 or 2 */
    formatStats:()=>fmtStats(),               /* accuracy by question format across the loaded bank */
    errors:()=>S.errs.slice(),                /* the learner's logged errors (a copy) */
    bankLoaded:()=>Object.keys(S.bank).length>0,
    loadAll:onProgress=>loadAll(onProgress),  /* load every module's questions */
    clearErrors:()=>{S.errs=[];saveErrs()},
    /* v2 */
    version:2,
    settings:Object.freeze({
      /* the learner's own settings, the same ones the app's Settings page edits: { exam: "YYYY-MM-DD" or "", target: 60..200 } */
      get:()=>({exam:S.cfg.exam||"",target:S.cfg.target||150}),
      /* change some of them; written at once with the learner's config (not after the usual short delay), and the header and
         every view redraw. Bad values throw. Returns a promise that settles when the setting is saved. */
      set:patch=>{
        if(!patch||typeof patch!=="object")throw new Error("settings.set needs an object, for example {exam:\"2026-12-01\"}");
        const keys=Object.keys(patch),known=["exam","target"],odd=keys.filter(k=>known.indexOf(k)<0);
        if(odd.length)throw new Error("settings.set: unknown setting '"+odd[0]+"' (known: "+known.join(", ")+")");
        if("exam" in patch){const v=patch.exam;
          if(v!==""&&!(typeof v==="string"&&/^\d{4}-\d{2}-\d{2}$/.test(v)&&!isNaN(new Date(v+"T00:00:00"))))throw new Error("settings.set: exam must be \"\" or a date like 2026-12-01")}
        if("target" in patch){const v=patch.target;if(typeof v!=="number"||!isFinite(v))throw new Error("settings.set: target must be a number from 60 to 200")}
        if("exam" in patch)S.cfg.exam=patch.exam;
        if("target" in patch)S.cfg.target=cl(patch.target,60,200);
        saveCfg();const done=flushSave("config");render();
        return done||Promise.resolve();   /* settles when the setting is written */
      }
    }),
    lessons:()=>{const ix=(S.lessonIdx&&S.lessonIdx.topics)||{};   /* every lesson, as copies: topicId, id, title, moduleId, estMin, scenes, status, version */
      return Object.keys(ix).sort().map(t=>Object.assign({topicId:t},ix[t]))},
    learnProgress:()=>Object.assign({},learnProgress()),
    navigate:route=>{if(!routeKnown(route))throw new Error("navigate: '"+route+"' is not a route (known: "+allRoutes().join(", ")+")");location.hash="#"+route},
    ui:Object.freeze({bar:bar,pc:pc,fmtPct:fmtPct,nTag:nTag,modNo:modNo,askBox:askBox}),
    data:Object.freeze({FORDER:FORDER,FMT:FMT,ERRT:ERRT})
  });
}
let APP_API=null;

function registerFeature(manifest,def){
  if(!manifest||!manifest.id)throw new Error("registerFeature: manifest has no id");
  if(FEATURES[manifest.id])throw new Error("feature '"+manifest.id+"' is registered twice");
  if(!def||typeof def.render!=="function")throw new Error("feature '"+manifest.id+"' must provide render(ctx)");
  const route=manifest.replaces||"f-"+manifest.id,f={manifest:manifest,def:def,route:route};
  if(manifest.replaces){
    if(!TABS.some(t=>t[0]===manifest.replaces))throw new Error("feature '"+manifest.id+"' replaces '"+manifest.replaces+"', which is not a built-in route");
    if(featureByRoute(route))throw new Error("route '"+route+"' is already served by feature '"+featureByRoute(route).manifest.id+"'");
  }
  FEATURES[manifest.id]=f;
  if(!document.getElementById("v-"+route)){
    const home=document.getElementById("v-home"),sec=document.createElement("section");sec.id="v-"+route;
    if(home&&home.parentNode)home.parentNode.appendChild(sec);
  }
  f.ctx={id:manifest.id,version:manifest.version,route:route,
    get app(){return APP_API||(APP_API=appApi())},
    get profile(){return S.profile||"me"},get uid(){return S.uid},
    esc:esc,toast:toast,rerender:()=>render(),store:makeFeatureStore(f)};
}
const featureIds=()=>Object.keys(FEATURES).sort();
/* every route the app can show: the built-in tabs and every feature (a feature is reachable at #f-<id>) */
const allRoutes=()=>TABS.map(t=>t[0]).concat(featureIds().filter(i=>!FEATURES[i].manifest.replaces).map(i=>"f-"+i));
const routeKnown=r=>allRoutes().indexOf(r)>=0;
/* the navigation entries for features whose manifest says tab:true */
const featureTabs=()=>featureIds().filter(i=>FEATURES[i].manifest.tab&&!FEATURES[i].manifest.replaces).map(i=>["f-"+i,FEATURES[i].manifest.title]);
/* the feature shown at a route: "f-<id>", or the built-in route it replaces */
function featureByRoute(route){
  if(/^f-/.test(route)){const f=FEATURES[route.slice(2)];return f&&!f.manifest.replaces?f:null}
  const ids=featureIds();for(let i=0;i<ids.length;i++)if(FEATURES[ids[i]].manifest.replaces===route)return FEATURES[ids[i]];
  return null;
}
function featureView(route){
  const f=featureByRoute(route);if(!f)return null;
  return()=>{try{return f.def.render(f.ctx)||""}
    catch(e){console.error("feature "+f.manifest.id+" failed to render",e);
      return '<div class="card"><h3>'+esc(f.manifest.title)+'</h3><p class="note">This feature failed to display: '+esc((e&&e.message)||e)+'</p></div>'}};
}
function featureAfterRender(){
  const f=featureByRoute(S.route);if(!f||typeof f.def.wire!=="function")return;
  try{f.def.wire(f.ctx,document.getElementById("v-"+S.route))}
  catch(e){console.error("feature "+f.manifest.id+" failed to wire",e);toast("Feature error: "+((e&&e.message)||e))}
}
