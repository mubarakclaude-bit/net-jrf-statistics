// Durable D1 fencing helpers. All ownership changes are conditional SQL updates.
const nowIso=()=>new Date().toISOString();
export async function claimExecution(db,jobId,sourceHash,token,leaseMs=60000){
 if(!db||!token||!/^([a-f0-9]{64})$/i.test(sourceHash)||!jobId)return null;
 const now=nowIso(),until=new Date(Date.now()+leaseMs).toISOString();
 await db.prepare("INSERT INTO processor_execution_claims (job_id,source_sha256,fencing_token,claim_token,lease_until,state,updated_at) VALUES (?, ?, 0, NULL, NULL, 'idle', ?) ON CONFLICT(job_id) DO NOTHING").bind(jobId,sourceHash,now).run();
 const res=await db.prepare("UPDATE processor_execution_claims SET source_sha256=?,fencing_token=fencing_token+1,claim_token=?,lease_until=?,state='claimed',updated_at=? WHERE job_id=? AND source_sha256=? AND (state!='claimed' OR lease_until IS NULL OR lease_until < ?) AND state!='completed'").bind(sourceHash,token,until,now,jobId,sourceHash,now).run();
 if(!res.meta?.changes)return null;
 return await db.prepare("SELECT job_id,source_sha256,fencing_token,claim_token,lease_until,state FROM processor_execution_claims WHERE job_id=? AND claim_token=? AND state='claimed'").bind(jobId,token).first();
}
export async function renewExecution(db,claim,leaseMs=60000){
 if(!claim?.job_id||!claim.claim_token||!Number.isSafeInteger(claim.fencing_token))return false;
 const now=nowIso(),until=new Date(Date.now()+leaseMs).toISOString();
 const r=await db.prepare("UPDATE processor_execution_claims SET lease_until=?,updated_at=? WHERE job_id=? AND source_sha256=? AND fencing_token=? AND claim_token=? AND state='claimed' AND lease_until>=?").bind(until,now,claim.job_id,claim.source_sha256,claim.fencing_token,claim.claim_token,now).run();return !!r.meta?.changes;
}
export async function fenceCheckpoint(db,claim,state='claimed'){
 if(!claim?.job_id||!claim.claim_token||!Number.isSafeInteger(claim.fencing_token))return false;
 const now=nowIso();const r=await db.prepare("UPDATE processor_execution_claims SET updated_at=? WHERE job_id=? AND source_sha256=? AND fencing_token=? AND claim_token=? AND state=? AND lease_until>=?").bind(now,claim.job_id,claim.source_sha256,claim.fencing_token,claim.claim_token,state,now).run();return !!r.meta?.changes;
}
export async function settleExecution(db,claim,state){
 if(!['completed','failed'].includes(state)||!claim?.job_id||!claim.claim_token)return false;
 const now=nowIso();const r=await db.prepare("UPDATE processor_execution_claims SET state=?,lease_until=NULL,updated_at=? WHERE job_id=? AND source_sha256=? AND fencing_token=? AND claim_token=? AND state='claimed' AND lease_until>=?").bind(state,now,claim.job_id,claim.source_sha256,claim.fencing_token,claim.claim_token,now).run();return !!r.meta?.changes;
}
