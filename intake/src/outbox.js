// Durable outbox dispatcher. Creation of job+outbox is intentionally left to a D1 batch
// transaction at the intake boundary; this module only claims and delivers existing rows.
const iso=()=>new Date().toISOString();
export async function claimOutbox(db,{limit=10,leaseMs=30000}={}){
 const bounded=Math.max(1,Math.min(50,Number.isSafeInteger(limit)?limit:10));
 const time=iso(),until=new Date(Date.now()+Math.max(1000,Math.min(120000,leaseMs))).toISOString();
 const rows=await db.prepare("SELECT id,job_id,payload_json FROM intake_outbox WHERE state='pending' OR (state='claimed' AND claim_until<?) ORDER BY created_at LIMIT ?").bind(time,bounded).all();
 const claimed=[];
 for(const row of rows.results||[]){const token=crypto.randomUUID();const r=await db.prepare("UPDATE intake_outbox SET state='claimed',claim_token=?,claim_until=?,attempts=attempts+1,updated_at=? WHERE id=? AND (state='pending' OR (state='claimed' AND claim_until<?))").bind(token,until,time,row.id,time).run();if(r.meta?.changes)claimed.push({...row,claim_token:token,claim_until:until});}
 return claimed;
}
export async function deliverOutbox(db,queue,{limit=10}={}){
 const claims=await claimOutbox(db,{limit});let sent=0,failed=0;
 for(const row of claims){let payload;try{payload=JSON.parse(row.payload_json);}catch{payload=null;}
  if(!payload||payload.job_id!==row.job_id){await db.prepare("UPDATE intake_outbox SET state='blocked',last_error='invalid_payload',claim_token=NULL,claim_until=NULL,updated_at=? WHERE id=? AND claim_token=?").bind(iso(),row.id,row.claim_token).run();failed++;continue;}
  try{await queue.send(payload);const t=iso();const r=await db.prepare("UPDATE intake_outbox SET state='sent',sent_at=?,claim_token=NULL,claim_until=NULL,last_error=NULL,updated_at=? WHERE id=? AND state='claimed' AND claim_token=?").bind(t,t,row.id,row.claim_token).run();if(r.meta?.changes)sent++;}
  catch(e){const t=iso();await db.prepare("UPDATE intake_outbox SET state='pending',claim_token=NULL,claim_until=NULL,last_error=?,updated_at=? WHERE id=? AND state='claimed' AND claim_token=?").bind(String(e?.message||'queue_send_failed').slice(0,500),t,row.id,row.claim_token).run();failed++;}
 }
 return {claimed:claims.length,sent,failed};
}
