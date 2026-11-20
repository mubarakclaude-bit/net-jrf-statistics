const PORTAL = `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Private Document Intake</title><style>body{font:16px system-ui;max-width:720px;margin:40px auto;padding:0 16px;color:#17202a}input,button{font:inherit;padding:10px;margin:8px 0;width:100%;box-sizing:border-box}button{cursor:pointer}pre{white-space:pre-wrap;word-break:break-word;background:#f3f4f6;padding:12px;border-radius:8px}</style><h1>Source document intake</h1><p>Upload a supported document to the private processing service. Files are not added to the Git repository. Protect this portal with owner-only access (such as Cloudflare Access) before accepting sensitive files.</p><label>Intake token<input id="token" type="password" autocomplete="off"></label><label>Source document<input id="file" type="file" accept=".pdf,.txt,.md,.docx,.pptx,.xlsx,.csv,.html,.rtf,image/*"></label><button id="upload">Upload document</button><label>Job ID (for status)<input id="job" placeholder="Job ID"></label><button id="status">Check status</button><pre id="out">Ready.</pre><script>const out=document.getElementById('out'),token=()=>document.getElementById('token').value;document.getElementById('upload').onclick=async()=>{const f=document.getElementById('file').files[0];if(!f){out.textContent='Select a document first.';return}out.textContent='Uploading…';const d=new FormData();d.append('file',f);try{const r=await fetch('/upload',{method:'POST',headers:{Authorization:'Bearer '+token()},body:d});const j=await r.json();out.textContent=JSON.stringify(j,null,2);if(j.job_id)document.getElementById('job').value=j.job_id}catch(e){out.textContent='Upload failed: '+e}};document.getElementById('status').onclick=async()=>{const id=document.getElementById('job').value.trim();if(!id){out.textContent='Enter a job ID';return}try{const r=await fetch('/jobs/'+encodeURIComponent(id),{headers:{Authorization:'Bearer '+token()}});out.textContent=JSON.stringify(await r.json(),null,2)}catch(e){out.textContent='Status failed: '+e}};</script></html>`;

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
    if(request.method==="POST"&&url.pathname==="/internal/processor-result"){if(!env.PROCESSOR_CALLBACK_TOKEN||request.headers.get("authorization")!==`Bearer ${env.PROCESSOR_CALLBACK_TOKEN}`)return json({error:"unauthorized"},401);let payload;try{payload=await request.json()}catch{return json({error:"invalid_json"},400)}if(!payload.job_id||payload.status!=="completed"||payload.stage!=="analysis"||!Array.isArray(payload.artifact_keys))return json({error:"invalid_contract"},400);const existing=await env.JOBS_DB.prepare("SELECT id FROM intake_jobs WHERE id=?").bind(payload.job_id).first();if(!existing)return json({error:"not_found"},404);const time=now();const details=JSON.stringify({summary:payload.summary||null,artifact_keys:Array.isArray(payload.artifact_keys)?payload.artifact_keys.slice(0,20):[]});await env.JOBS_DB.prepare("UPDATE intake_jobs SET status=?,stage=?,updated_at=?,error_code=?,error_message=? WHERE id=?").bind(payload.status,payload.stage,time,payload.error_code||null,payload.error_message||null,payload.job_id).run();await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(payload.job_id,"processor_result",payload.stage,details,time).run();return json({accepted:true});}
    if (!auth(request, env)) return json({error:"unauthorized"},401);
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
      // Concurrent duplicate requests may win the UNIQUE checksum constraint.
      const raced = await env.JOBS_DB.prepare("SELECT id,status FROM intake_jobs WHERE source_sha256=? LIMIT 1").bind(hash).first();
      await env.SOURCE_BUCKET.delete(key);
      if (raced) return json({job_id:raced.id,status:raced.status,duplicate:true},200);
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
      if (!env.PROCESSOR_URL || !env.PROCESSOR_TOKEN) {
        const time=now();
        await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='blocked_infrastructure',stage='dispatch',updated_at=? WHERE id=?").bind(time,job_id).run();
        await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(job_id,"blocked","dispatch",JSON.stringify({code:"processor_not_configured"}),time).run();
        message.ack(); continue;
      }
      try {
        const resp=await fetch(env.PROCESSOR_URL,{method:"POST",headers:{"content-type":"application/json","authorization":"Bearer "+env.PROCESSOR_TOKEN},body:JSON.stringify({schema_version:1,job_id,source_sha256:job.source_sha256,object_key:job.object_key,source_name:job.source_name,source_size:job.source_size,mime_type:job.mime_type,resume_stage:"extract"})});
        if (!resp.ok) throw new Error("processor_http_"+resp.status);
        const time=now();
        await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='processing',stage='extract',updated_at=? WHERE id=?").bind(time,job_id).run();
        await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(job_id,"dispatched","extract",JSON.stringify({processor_status:resp.status}),time).run();
        message.ack();
      } catch (e) {
        const time=now();
        await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='failed_retryable',stage='dispatch',attempts=attempts+1,updated_at=?,error_code='processor_dispatch_failed',error_message=? WHERE id=?").bind(time,"Dispatch failed; retry scheduled.",job_id).run();
        await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)").bind(job_id,"dispatch_failed","dispatch",JSON.stringify({code:"processor_dispatch_failed"}),time).run();
        message.retry();
      }
    }
  }
};
