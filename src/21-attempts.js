/* ===================== attempts ===================== */
/* ---- progress keys (Issue #117) ----
   A learner's attempts and flags are stored under a PROGRESS KEY, never read straight off q.id. For every question whose id
   is unique across all question sets the progress key IS the id, so nothing already saved moves. Ten June 2026 Q36 variant
   ids were given to two different questions in two banks (Official Statistics and Sampling). For an id listed in SCOPED_IDS
   the key is scoped by the question set the item came from, "<setId>::<id>", so each question keeps its own result.
   The question id itself never changes: provenance, error logs, exports and the id-history check keep using it.
   tests/progress-keys.test.js recomputes the collisions from seed/ and fails if this list is out of date. */
const SCOPED_IDS={
  "j26v-q36-01":["official_pyq_variants","sampling_pyq_variants"],"j26v-q36-02":["official_pyq_variants","sampling_pyq_variants"],
  "j26v-q36-03":["official_pyq_variants","sampling_pyq_variants"],"j26v-q36-04":["official_pyq_variants","sampling_pyq_variants"],
  "j26v-q36-05":["official_pyq_variants","sampling_pyq_variants"],"j26v-q36-06":["official_pyq_variants","sampling_pyq_variants"],
  "j26v-q36-07":["official_pyq_variants","sampling_pyq_variants"],"j26v-q36-08":["official_pyq_variants","sampling_pyq_variants"],
  "j26v-q36-09":["official_pyq_variants","sampling_pyq_variants"],"j26v-q36-10":["official_pyq_variants","sampling_pyq_variants"]};
const PK_VERSION=2;                          // attempts record format: 2 = keys are progress keys, ambiguous legacy ids quarantined
const PK_SNAPSHOT="premigrate-pk2";          // contracts/storage-paths.json "snapshot"
const isScopedId=id=>Object.prototype.hasOwnProperty.call(SCOPED_IDS,String(id));
/* The ONE way to find where a question's progress lives. */
function progressKeyOf(q){
  if(q==null)return "";
  if(typeof q==="string")return q;           // already a key (features and old call sites pass one)
  if(!q.id)return "";
  return isScopedId(q.id)?(q.setId||"unscoped")+"::"+q.id:String(q.id);
}
function attOf(q){return S.att[progressKeyOf(q)]}

function record(q,ok){
  const k=progressKeyOf(q);if(!k)return;
  const a=S.att[k]||{n:0};
  a.o=ok?1:0;a.n=(a.n||0)+1;a.t=now();S.att[k]=a;saveAtt();
}
function flagQ(q){const k=progressKeyOf(q);if(!k)return 0;const a=S.att[k]||{n:0};a.f=a.f?0:1;S.att[k]=a;saveAtt();return a.f}
function isFlagged(q){return !!(attOf(q)||{}).f}
function logErr(q,type){
  S.errs.push({qid:q.id,pk:progressKeyOf(q),mid:q.moduleId,fmt:q.format,type:type,ts:now(),stem:String(q.stem||"").slice(0,120)});
  saveErrs();toast("Logged: "+(ERRT.find(e=>e[0]===type)||["",type])[1]);
}
function statusOf(q){const a=attOf(q);if(!a||!a.n)return"unseen";return a.o?"correct":"wrong"}
function isFree(q){return !((q.options||[]).length)} // write-in: no options, you mark yourself

/* ---- migration of a stored attempts record to progress keys ----
   planPkMigration is pure: it never touches S or the store.
   - a key that is not a scoped id is already its own progress key: it stays exactly as it is (that is the migration of an
     unambiguous id; no move is needed and none is made)
   - a key that IS a scoped id was shared by two different questions, so it cannot be attributed: it goes to "quarantine",
     with the sets it could belong to. It is never given to either question and never deleted.
   - a key already scoped ("<set>::<id>") was written by this version and is kept.
   Running it on an already migrated record returns it unchanged. */
function planPkMigration(doc){
  const a=(doc&&doc.a)||{},quarantine=Object.assign({},(doc&&doc.quarantine)||{}),att={};
  let moved=0;
  Object.keys(a).forEach(k=>{
    if(isScopedId(k)){
      if(!quarantine[k])quarantine[k]={legacy:a[k],candidates:SCOPED_IDS[k].slice(),reason:"legacy id shared by two different questions"};
      moved++;
    }else att[k]=a[k];
  });
  return{doc:{a:att,v:SCHEMA,pk:PK_VERSION,quarantine:quarantine},moved:moved};
}
/* JSON with object keys sorted, so a store that returns keys in another order still compares equal. */
function canon(v){return v&&typeof v==="object"?(Array.isArray(v)?"["+v.map(canon).join(",")+"]":
  "{"+Object.keys(v).sort().map(k=>JSON.stringify(k)+":"+canon(v[k])).join(",")+"}"):JSON.stringify(v===undefined?null:v)}
function snapshotPath(){return "data/users/"+S.uid+"/"+upath("snapshots/"+PK_SNAPSHOT+"/record")}
/* Called by loadProfileData with the attempts record as stored and every record as loaded (for the snapshot).
   Order: snapshot (written and read back; an existing one is kept, it is the earliest state) -> migrated attempts written
   -> only then the in-memory state switches. If any write fails, the stored record is untouched, the in-memory state keeps
   the legacy keys (so a later save writes them back unchanged) and the next load tries again. */
async function migrateProgressKeys(stored,records){
  S.attPk=stored&&stored.pk>=PK_VERSION?stored.pk:1;
  S.attQuar=(stored&&stored.quarantine)||{};
  S.pkMigration={state:"current"};
  if(S.attPk>=PK_VERSION)return S.pkMigration;
  const plan=planPkMigration(stored);
  if(!plan.moved){S.attPk=PK_VERSION;S.attQuar=plan.doc.quarantine;return S.pkMigration={state:"nothing-to-move"}}
  if(!S.db||!S.uid)return S.pkMigration={state:"no-store"};
  try{
    const sref=S.db.doc(snapshotPath());
    const prev=await sref.get();
    if(!prev.exists){
      await sref.set({format:"net-jrf-statistics-premigration",version:1,createdAt:new Date().toISOString(),
        learnerId:String(S.uid),profileId:S.profile||"me",reason:"progress keys v"+PK_VERSION+" (Issue #117)",records:records});
      const back=await sref.get();
      if(!back.exists||canon((back.data().records||{}).attempts)!==canon(records.attempts))
        throw new Error("snapshot did not read back");
    }
    await S.db.doc("data/users/"+S.uid+"/"+upath("attempts")).set(plan.doc);
  }catch(e){
    // nothing stored changed; keep legacy keys in memory so no later save can lose them
    return S.pkMigration={state:"failed",error:String((e&&e.code)||(e&&e.message)||e)};
  }
  S.att=plan.doc.a;S.attPk=PK_VERSION;S.attQuar=plan.doc.quarantine;
  S.pkMigration={state:"migrated",moved:plan.moved};
  toast(plan.moved+" old result"+(plan.moved>1?"s":"")+" on June 2026 Q36 variant ids shared by two banks could not be matched to one question. They are kept aside, not counted.");
  return S.pkMigration;
}
/* Put the pre-migration attempts record back exactly as it was saved. The next load migrates it again (same result). */
async function restorePkSnapshot(){
  if(!S.db||!S.uid)return false;
  const s=await S.db.doc(snapshotPath()).get();
  if(!s.exists)return false;
  const att=(s.data().records||{}).attempts;
  if(!att)return false;
  await S.db.doc("data/users/"+S.uid+"/"+upath("attempts")).set(att);
  // the in-memory state must match what was restored, or the next save would write the migrated record back over it
  S.att=Object.assign({},att.a||{});S.attPk=att.pk>=PK_VERSION?att.pk:1;S.attQuar=att.quarantine||{};S.attLoadFailed=false;
  S.pkMigration={state:"restored"};
  return true;
}
