import {canTransition,retryDisposition} from "./lifecycle.js";
const PORTAL = `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Private Document Intake</title><style>body{font:16px system-ui;max-width:720px;margin:40px auto;padding:0 16px;color:#17202a}input,button{font:inherit;padding:10px;margin:8px 0;width:100%;box-sizing:border-box}button{cursor:pointer}pre{white-space:pre-wrap;word-break:break-word;background:#f3f4f6;padding:12px;border-radius:8px}</style><h1>Source document intake</h1><p>Upload a supported document to the private processing service. Files are not added to the Git repository. Protect this portal with owner-only access (such as Cloudflare Access) before accepting sensitive files.</p><label>Intake token<input id="token" type="password" autocomplete="off"></label><label>Source document<input id="file" type="file" accept=".pdf,.txt,.md,.docx,.pptx,.xlsx,.csv,.html,.rtf,image/*"></label><button id="upload">Upload document</button><label>Job ID (for status)<input id="job" placeholder="Job ID"></label><button id="status">Check status</button><button id="retry">Retry blocked job</button><pre id="out">Ready.</pre><script>const out=document.getElementById('out'),token=()=>document.getElementById('token').value;document.getElementById('upload').onclick=async()=>{const f=document.getElementById('file').files[0];if(!f){out.textContent='Select a document first.';return}out.textContent='Uploading…';const d=new FormData();d.append('file',f);try{const r=await fetch('/upload',{method:'POST',headers:{Authorization:'Bearer '+token()},body:d});const j=await r.json();out.textContent=JSON.stringify(j,null,2);if(j.job_id)document.getElementById('job').value=j.job_id}catch(e){out.textContent='Upload failed: '+e}};document.getElementById('status').onclick=async()=>{const id=document.getElementById('job').value.trim();if(!id){out.textContent='Enter a job ID';return}try{const r=await fetch('/jobs/'+encodeURIComponent(id),{headers:{Authorization:'Bearer '+token()}});out.textContent=JSON.stringify(await r.json(),null,2)}catch(e){out.textContent='Status failed: '+e}};document.getElementById('retry').onclick=async()=>{const id=document.getElementById('job').value.trim();if(!id){out.textContent='Enter a job ID';return}out.textContent='Retrying after integrity checks…';try{const r=await fetch('/jobs/'+encodeURIComponent(id)+'/retry',{method:'POST',headers:{Authorization:'Bearer '+token()}});out.textContent=JSON.stringify(await r.json(),null,2)}catch(e){out.textContent='Retry failed: '+e}};</script></html>`;

const MAX_UPLOAD_BYTES = 20 * 1024 * 1024;
const now = () => new Date().toISOString();
const json = (data, status=200) => new Response(JSON.stringify(data), {
  status, headers: { "content-type": "application/json; charset=utf-8", "cache-control":"no-store" }
});
async function sha256(buffer) {
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return [...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,"0")).join("");
}
function auth(request, env) {
  const token = env.INTAKE_TOKEN;
  if (!token) return false;
  return request.headers.get("authorization") === `Bearer ${token}`;
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/health") return json({ok:true,service:"intake"});
    if (request.method === "GET" && url.pathname === "/") return new Response(PORTAL,{headers:{"content-type":"text/html; charset=utf-8","cache-control":"no-store"}});
    if(request.method==="POST"&&url.pathname==="/internal/processor-result"){
      if(!env.PROCESSOR_CALLBACK_TOKEN||request.headers.get("authorization")!==`Bearer ${env.PROCESSOR_CALLBACK_TOKEN}`)return json({error:"unauthorized"},401);
      let payload;try{payload=await request.json()}catch{return json({error:"invalid_json"},400)}
      const uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
      if(!uuid.test(payload.job_id||"")||payload.status!=="completed"||payload.stage!=="analysis"||!payload.attempt_id||!Number.isSafeInteger(payload.fencing_token)||typeof payload.manifest_key!=="string"||!Array.isArray(payload.artifact_keys)||payload.artifact_keys.length<1||payload.artifact_keys.length>20||payload.artifact_keys.some(k=>typeof k!=="string"||k.length>512||!k.startsWith(`jobs/${payload.job_id}/attempts/`)))return json({error:"invalid_contract"},400);
      const existing=await env.JOBS_DB.prepare("SELECT id,status,source_sha256 FROM intake_jobs WHERE id=?").bind(payload.job_id).first();
      if(!existing)return json({error:"not_found"},404);
      if(existing.status==="completed")return json({accepted:true,duplicate:true});
      if(existing.status!=="processing"||!canTransition(existing.status,"completed"))return json({error:"invalid_transition"},409);
      // Independently validate the private manifest and every artifact before the
      // ledger is allowed to record completion.
      if(!env.ARTIFACT_BUCKET)return json({error:"artifact_storage_unconfigured"},503);
      const expectedPrefix=`jobs/${payload.job_id}/attempts/`;if(!payload.manifest_key.startsWith(expectedPrefix)||!payload.manifest_key.endsWith("/manifest.json"))return json({error:"invalid_manifest_key"},400);const manifestObj=await env.ARTIFACT_BUCKET.get(payload.manifest_key);
      if(!manifestObj)return json({error:"manifest_not_found"},422);
      let manifest;try{manifest=JSON.parse(await manifestObj.text())}catch{return json({error:"invalid_manifest"},422)}
      if(manifest.schema_version!==1||manifest.job_id!==payload.job_id||manifest.attempt_id!==payload.attempt_id||manifest.fencing_token!==payload.fencing_token||manifest.source_sha256!==existing.source_sha256||!Array.isArray(manifest.artifacts)||manifest.artifacts.length>20)return json({error:"manifest_invalid"},422);
      const reported=new Set(payload.artifact_keys),manifestKeys=new Set(manifest.artifacts.map(x=>x?.key));
      if(manifest.artifacts.some(x=>!x||typeof x.key!=="string"||!x.key.startsWith(expectedPrefix)||! /^[a-f0-9]{64}$/i.test(x.sha256||"")||!Number.isSafeInteger(x.size)||x.size<0)||[...manifestKeys].some(k=>!reported.has(k))||[...reported].some(k=>k!==payload.manifest_key&&!manifestKeys.has(k)))return json({error:"artifact_manifest_mismatch"},422);
      for(const entry of manifest.artifacts){const stored=await env.ARTIFACT_BUCKET.get(entry.key);if(!stored)return json({error:"artifact_missing"},422);const bytes=await stored.arrayBuffer();if(bytes.byteLength!==entry.size||await sha256(bytes)!==entry.sha256)return json({error:"artifact_integrity_mismatch"},422);}
      const summary=payload.summary&&typeof payload.summary==="object"?{pages:Number.isSafeInteger(payload.summary.pages)?payload.summary.pages:null,segments:Number.isSafeInteger(payload.summary.segments)?payload.summary.segments:null,production_created:typeof payload.summary.production_created==="boolean"?payload.summary.production_created:null}:null;
      const time=now(),details=JSON.stringify({summary,artifact_keys:payload.artifact_keys,manifest_key:payload.manifest_key,attempt_id:payload.attempt_id,fencing_token:payload.fencing_token});
      const settled=await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='completed',stage='analysis',manifest_key=?,updated_at=?,error_code=NULL,error_message=NULL,dispatch_lease_until=NULL,dispatch_lease_token=NULL WHERE id=? AND status='processing'").bind(payload.manifest_key,time,payload.job_id).run();
      if(!settled.meta?.changes)return json({error:"state_conflict"},409);
      await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(payload.job_id,"processor_result","analysis",details,time).run();
      return json({accepted:true});
    }
    if (!auth(request, env)) return json({error:"unauthorized"},401);
    if(request.method==="GET"){
      const parts=url.pathname.split("/");
      if(parts.length===5&&parts[1]==="jobs"&&parts[3]==="artifacts"){
        const id=parts[2],filename=parts[4],uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
        const allowed=new Set(["manifest.json","extract.json","source-audit.json","taxonomy-map.json","coverage-report.json","production.json","verification-report.json"]);
        if(!uuid.test(id)||!allowed.has(filename))return json({error:"not_found"},404);
        if(!env.ARTIFACT_BUCKET)return json({error:"artifact_storage_unconfigured"},503);
        const job=await env.JOBS_DB.prepare("SELECT id,status,source_sha256,manifest_key FROM intake_jobs WHERE id=?").bind(id).first();
        if(!job)return json({error:"not_found"},404);
        if(job.status!=="completed")return json({error:"job_not_completed"},409);
        const manifestObj=await env.ARTIFACT_BUCKET.get(job.manifest_key);if(!manifestObj)return json({error:"manifest_not_found"},404);
        let manifest;try{manifest=JSON.parse(await manifestObj.text())}catch{return json({error:"invalid_manifest"},422)}
        if(manifest.schema_version!==1||manifest.job_id!==id||manifest.source_sha256!==job.source_sha256||!Array.isArray(manifest.artifacts)||manifest.artifacts.length>20||manifest.artifacts.some(x=>!x||typeof x.key!=="string"||!x.key.startsWith(`jobs/${id}/attempts/`)||typeof x.sha256!=="string"||!Number.isSafeInteger(x.size)||x.size<0))return json({error:"manifest_invalid"},422);
        if(filename==="manifest.json")return new Response(JSON.stringify(manifest),{headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store","content-disposition":`attachment; filename="${filename}"`}});
        const suffix="/"+filename,entry=manifest.artifacts.find(x=>x&&x.key.endsWith(suffix)&&typeof x.sha256==="string"&&Number.isSafeInteger(x.size));const key=entry?.key;
        if(!entry)return json({error:"artifact_not_in_manifest"},404);
        const obj=await env.ARTIFACT_BUCKET.get(key);if(!obj)return json({error:"artifact_not_found"},404);
        const bytes=await obj.arrayBuffer();if(bytes.byteLength!==entry.size||await sha256(bytes)!==entry.sha256)return json({error:"artifact_integrity_mismatch"},422);
        return new Response(bytes,{headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store","content-disposition":`attachment; filename="${filename}"`}});
      }
    }
    if(request.method==="POST"&&url.pathname.startsWith("/jobs/")){
      const parts=url.pathname.split("/");
      if(parts.length===4&&parts[1]==="jobs"&&parts[3]==="retry"){
        const id=parts[2],uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
        if(!uuid.test(id))return json({error:"invalid_job_id"},400);
        const job=await env.JOBS_DB.prepare("SELECT id,status,source_sha256,object_key,source_size FROM intake_jobs WHERE id=?").bind(id).first();
        if(!job)return json({error:"not_found"},404);
        if(!["blocked_infrastructure","failed_retryable"].includes(job.status)||!canTransition(job.status,"queued"))return json({error:"retry_not_allowed"},409);
        if(!env.SOURCE_BUCKET||!env.PROCESSING_QUEUE)return json({error:"recovery_storage_unconfigured"},503);
        if(!env.PROCESSOR_URL||!env.PROCESSOR_TOKEN)return json({error:"processor_not_configured"},503);
        const source=await env.SOURCE_BUCKET.get(job.object_key);if(!source)return json({error:"source_missing"},409);
        const bytes=await source.arrayBuffer();if(bytes.byteLength!==job.source_size||await sha256(bytes)!==job.source_sha256)return json({error:"source_integrity_failed"},422);
        const time=now();
        const moved=await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='queued',stage='dispatch',updated_at=?,error_code=NULL,error_message=NULL,dispatch_lease_until=NULL,dispatch_lease_token=NULL WHERE id=? AND status=?").bind(time,id,job.status).run();
        if(!moved.meta?.changes)return json({error:"state_conflict"},409);
        await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(id,"manual_retry_requested","dispatch",JSON.stringify({source_integrity_verified:true}),time).run();
        try{await env.PROCESSING_QUEUE.send({job_id:id,stage:"extract",sha256:job.source_sha256});return json({job_id:id,status:"queued",retry_requested:true},202);}
        catch{
          const blockedTime=now();
          await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='blocked_infrastructure',stage='dispatch',updated_at=?,error_code='retry_enqueue_failed',error_message='Manual retry queueing failed.',dispatch_lease_until=NULL,dispatch_lease_token=NULL WHERE id=? AND status='queued'").bind(blockedTime,id).run();
          try{await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(id,"retry_enqueue_failed","dispatch",JSON.stringify({code:"retry_enqueue_failed"}),blockedTime).run();}catch{/* job remains owner-action blocked */}
          return json({job_id:id,status:"blocked_infrastructure",error:"retry_enqueue_failed"},503);
        }
      }
    }
    if (request.method === "GET" && url.pathname.startsWith("/jobs/")) {
      const id = url.pathname.slice("/jobs/".length);
      if (!id || id.includes("/")) return json({error:"invalid_job_id"},400);
      const job = await env.JOBS_DB.prepare("SELECT id,source_name,source_size,mime_type,status,stage,attempts,created_at,updated_at,error_code FROM intake_jobs WHERE id=?").bind(id).first();
      if (!job) return json({error:"not_found"},404);
      const events = await env.JOBS_DB.prepare("SELECT event,stage,details_json,created_at FROM intake_events WHERE job_id=? ORDER BY id DESC LIMIT 30").bind(id).all();
      return json({job,events:events.results||[]});
    }
    if (request.method !== "POST" || url.pathname !== "/upload") return json({error:"not_found"},404);
    const form = await request.formData().catch(()=>null);
    if (!form) return json({error:"invalid_multipart"},400);
    const file = form.get("file");
    if (!(file instanceof File)) return json({error:"missing_file"},400);
    const configuredLimit = Number(env.MAX_UPLOAD_BYTES);
    const limit = Number.isFinite(configuredLimit) && configuredLimit > 0 ? Math.min(configuredLimit, MAX_UPLOAD_BYTES) : MAX_UPLOAD_BYTES;
    const contentLength = Number(request.headers.get("content-length"));
    if (Number.isFinite(contentLength) && contentLength > limit + 1024 * 1024) return json({error:"file_size_limit"},413);
    if (file.size <= 0 || file.size > limit) return json({error:"file_size_limit"},413);
    const name = (file.name || "source.pdf").replace(/[\\x00-\\x1f\\x7f]/g,"").slice(0,180) || "source.pdf";
    const allowedTypes=new Set(["application/pdf","text/plain","text/markdown","text/csv","text/html","application/rtf","application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/vnd.openxmlformats-officedocument.presentationml.presentation","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]);
    const mime=(file.type||"application/octet-stream").toLowerCase();
    const allowedImages=new Set(["image/png","image/jpeg","image/webp"]);if(!allowedTypes.has(mime)&&!allowedImages.has(mime))return json({error:"unsupported_document_type"},415);
    const bytes=await file.arrayBuffer();
    const sig=new Uint8Array(bytes);if(mime==="application/pdf"&&(sig[0]!==37||sig[1]!==80||sig[2]!==68||sig[3]!==70||sig[4]!==45))return json({error:"invalid_pdf_signature"},415);if(mime==="image/png"&&(sig.length<8||[137,80,78,71,13,10,26,10].some((v,i)=>sig[i]!==v)))return json({error:"invalid_image_signature"},415);if(mime==="image/jpeg"&&(sig[0]!==255||sig[1]!==216||sig[2]!==255))return json({error:"invalid_image_signature"},415);if(mime==="image/webp"&&(String.fromCharCode(...sig.slice(0,4))!=="RIFF"||String.fromCharCode(...sig.slice(8,12))!=="WEBP"))return json({error:"invalid_image_signature"},415);
    const hash = await sha256(bytes);
    const duplicate = await env.JOBS_DB.prepare("SELECT id,status FROM intake_jobs WHERE source_sha256=? LIMIT 1").bind(hash).first();
    if (duplicate) return json({job_id:duplicate.id,status:duplicate.status,duplicate:true},200);
    const id = crypto.randomUUID();
    const key = `incoming/${id}/${hash}/${name.replace(/[^a-zA-Z0-9._-]/g,"_")}`;
    const time = now();
    await env.SOURCE_BUCKET.put(key, bytes, {httpMetadata:{contentType:mime}});
    try {
      await env.JOBS_DB.prepare("INSERT INTO intake_jobs (id,source_name,source_sha256,object_key,source_size,mime_type,status,stage,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)")
        .bind(id,name,hash,key,file.size,mime,"accepted","intake",time,time).run();
      await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)")
        .bind(id,"accepted","intake",JSON.stringify({size:file.size,sha256:hash,mime_type:mime}),time).run();
      await env.PROCESSING_QUEUE.send({job_id:id,stage:"extract",sha256:hash});
    } catch (e) {
      // A competing upload may win the checksum constraint; clean only this request's object.
      const raced = await env.JOBS_DB.prepare("SELECT id,status FROM intake_jobs WHERE source_sha256=? LIMIT 1").bind(hash).first();
      if(raced&&raced.id!==id){await env.SOURCE_BUCKET.delete(key);return json({job_id:raced.id,status:raced.status,duplicate:true},200);}
      // If our ledger row exists but queue/event acceptance failed, preserve the source
      // and make the recovery requirement explicit rather than deleting a live object.
      if(raced&&raced.id===id){
        const time=now();
        await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='blocked_infrastructure',stage='intake',updated_at=?,error_code='intake_enqueue_failed',error_message='Job acceptance requires owner recovery.',dispatch_lease_until=NULL,dispatch_lease_token=NULL WHERE id=? AND status='accepted'").bind(time,id).run();
        try{await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(id,"intake_enqueue_blocked","intake",JSON.stringify({code:"intake_enqueue_failed"}),time).run();}catch{/* ledger row remains visible for manual recovery */}
        return json({job_id:id,status:"blocked_infrastructure",error:"intake_enqueue_failed",owner_action_required:true},503);
      }
      await env.SOURCE_BUCKET.delete(key);
      throw e;
    }
    return json({job_id:id,status:"accepted",duplicate:false},202);
  },
  async queue(batch, env) {
    for (const message of batch.messages) {
      const {job_id} = message.body || {};
      if (!job_id) { message.ack(); continue; }
      const job = await env.JOBS_DB.prepare("SELECT id,status,source_sha256,object_key,source_name,source_size,mime_type FROM intake_jobs WHERE id=?").bind(job_id).first();
      if (!job || ["completed","failed_terminal","cancelled"].includes(job.status)) { message.ack(); continue; }
      const leaseToken=crypto.randomUUID(), leaseTime=now(), leaseUntil=new Date(Date.now()+30000).toISOString();
      const claim=await env.JOBS_DB.prepare("UPDATE intake_jobs SET dispatch_lease_until=?,dispatch_lease_token=?,updated_at=? WHERE id=? AND status NOT IN ('completed','failed_terminal','cancelled') AND (dispatch_lease_until IS NULL OR dispatch_lease_until < ?)").bind(leaseUntil,leaseToken,leaseTime,job_id,leaseTime).run();
      if(!claim.meta?.changes){message.retry();continue;}
      if (!env.PROCESSOR_URL || !env.PROCESSOR_TOKEN) {
        const time=now();
        if(canTransition(job.status,"blocked_infrastructure")) await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='blocked_infrastructure',stage='dispatch',updated_at=?,error_code='processor_not_configured',error_message='Processing service configuration is required.',dispatch_lease_until=NULL,dispatch_lease_token=NULL WHERE id=? AND dispatch_lease_token=?").bind(time,job_id,leaseToken).run();
        await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(job_id,"blocked","dispatch",JSON.stringify({code:"processor_not_configured"}),time).run();
        message.ack(); continue;
      }
      // Move to processing before the synchronous processor call so a fast completion
      // callback cannot race against an accepted/queued ledger state.
      if(!canTransition(job.status,"processing")){await env.JOBS_DB.prepare("UPDATE intake_jobs SET dispatch_lease_until=NULL,dispatch_lease_token=NULL WHERE id=? AND dispatch_lease_token=?").bind(job_id,leaseToken).run();message.ack();continue;}
      const started=await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='processing',stage='extract',updated_at=? WHERE id=? AND dispatch_lease_token=? AND status=?").bind(leaseTime,job_id,leaseToken,job.status).run();
      if(!started.meta?.changes){message.retry();continue;}
      await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(job_id,"processing_started","extract",JSON.stringify({lease_token_claimed:true}),leaseTime).run();
      try {
        const resp=await fetch(env.PROCESSOR_URL,{method:"POST",headers:{"content-type":"application/json","authorization":"Bearer "+env.PROCESSOR_TOKEN},body:JSON.stringify({schema_version:1,job_id,source_sha256:job.source_sha256,object_key:job.object_key,source_name:job.source_name,source_size:job.source_size,mime_type:job.mime_type,resume_stage:"extract"})});
        if (!resp.ok) throw new Error("processor_http_"+resp.status);
        const time=now();
        const settled=await env.JOBS_DB.prepare("UPDATE intake_jobs SET stage='extract',updated_at=?,dispatch_lease_until=NULL,dispatch_lease_token=NULL WHERE id=? AND dispatch_lease_token=? AND status='processing'").bind(time,job_id,leaseToken).run();
        if(!settled.meta?.changes){message.ack();continue;}
        await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(job_id,"dispatched","extract",JSON.stringify({processor_status:resp.status}),time).run();
        message.ack();
      } catch (e) {
        const time=now();
        const current=await env.JOBS_DB.prepare("SELECT status,attempts FROM intake_jobs WHERE id=?").bind(job_id).first();
        const nextAttempts=(current?.attempts||0)+1,disposition=retryDisposition("failed_retryable",nextAttempts,5);
        const nextStatus=disposition==="terminalize"?"failed_terminal":"failed_retryable";
        if(current&&canTransition(current.status,nextStatus)){
          const failedUpdate=await env.JOBS_DB.prepare("UPDATE intake_jobs SET status=?,stage='dispatch',attempts=?,updated_at=?,error_code='processor_dispatch_failed',error_message=?,dispatch_lease_until=NULL,dispatch_lease_token=NULL WHERE id=? AND dispatch_lease_token=? AND status NOT IN ('completed','failed_terminal','cancelled')").bind(nextStatus,nextAttempts,time,nextStatus==="failed_terminal"?"Dispatch failed after bounded retries.":"Dispatch failed; retry scheduled.",job_id,leaseToken).run();
          if(!failedUpdate.meta?.changes){message.ack();continue;}
          await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(job_id,nextStatus==="failed_terminal"?"dispatch_terminal":"dispatch_failed","dispatch",JSON.stringify({code:"processor_dispatch_failed",attempt:nextAttempts,limit:5}),time).run();
        }
        if(disposition==="terminalize")message.ack();else message.retry();
      }
    }
  }
};
