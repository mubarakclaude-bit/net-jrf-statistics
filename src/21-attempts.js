/* ===================== attempts ===================== */
function record(q,ok){
  const a=S.att[q.id]||{n:0};
  a.o=ok?1:0;a.n=(a.n||0)+1;a.t=now();S.att[q.id]=a;saveAtt();
}
function flagQ(id){const a=S.att[id]||{n:0};a.f=a.f?0:1;S.att[id]=a;saveAtt();return a.f}
function logErr(q,type){
  S.errs.push({qid:q.id,mid:q.moduleId,fmt:q.format,type:type,ts:now(),stem:String(q.stem||"").slice(0,120)});
  saveErrs();toast("Logged: "+(ERRT.find(e=>e[0]===type)||["",type])[1]);
}
function statusOf(id){const a=S.att[id];if(!a||!a.n)return"unseen";return a.o?"correct":"wrong"}
function isFree(q){return !((q.options||[]).length)} // write-in: no options, you mark yourself

