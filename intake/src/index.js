const MAX_UPLOAD_BYTES = 20 * 1024 * 1024;
const now = () => new Date().toISOString();
const json = (data, status=200) => new Response(JSON.stringify(data), {
  status, headers: { "content-type": "application/json; charset=utf-8" }
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
    if (request.method !== "POST" || url.pathname !== "/upload") return json({error:"not_found"},404);
    if (!auth(request, env)) return json({error:"unauthorized"},401);
    const form = await request.formData().catch(()=>null);
    if (!form) return json({error:"invalid_multipart"},400);
    const file = form.get("file");
    if (!(file instanceof File)) return json({error:"missing_file"},400);
    if (file.size <= 0 || file.size > (Number(env.MAX_UPLOAD_BYTES)||MAX_UPLOAD_BYTES)) return json({error:"file_size_limit"},413);
    const name = file.name || "source.pdf";
    if (!name.toLowerCase().endsWith(".pdf") || file.type !== "application/pdf") return json({error:"pdf_only"},415);
    const bytes = await file.arrayBuffer();
    // Lightweight magic-byte check. This is not malware scanning.
    if (new Uint8Array(bytes).slice(0,5).toString() !== new Uint8Array([37,80,68,70,45]).toString()) return json({error:"invalid_pdf_signature"},415);
    const hash = await sha256(bytes);
    const duplicate = await env.JOBS_DB.prepare("SELECT id,status FROM intake_jobs WHERE source_sha256=? LIMIT 1").bind(hash).first();
    if (duplicate) return json({job_id:duplicate.id,status:duplicate.status,duplicate:true},200);
    const id = crypto.randomUUID();
    const key = `incoming/${id}/${hash}.pdf`;
    const time = now();
    await env.SOURCE_BUCKET.put(key, bytes, {httpMetadata:{contentType:"application/pdf"}});
    try {
      await env.JOBS_DB.prepare("INSERT INTO intake_jobs (id,source_name,source_sha256,object_key,source_size,status,stage,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?)")
        .bind(id,name,hash,key,file.size,"accepted","intake",time,time).run();
      await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)")
        .bind(id,"accepted","intake",JSON.stringify({size:file.size,sha256:hash}),time).run();
      await env.PROCESSING_QUEUE.send({job_id:id,stage:"extract",sha256:hash});
    } catch (e) {
      await env.SOURCE_BUCKET.delete(key);
      throw e;
    }
    return json({job_id:id,status:"accepted",duplicate:false},202);
  },
  async queue(batch, env) {
    for (const message of batch.messages) {
      const {job_id} = message.body || {};
      if (!job_id) { message.ack(); continue; }
      const job = await env.JOBS_DB.prepare("SELECT status,stage FROM intake_jobs WHERE id=?").bind(job_id).first();
      if (!job || job.status === "completed") { message.ack(); continue; }
      // Scaffold checkpoint: processing worker is intentionally not yet wired.
      const time = now();
      await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='needs_worker',stage='worker_scaffold',attempts=attempts+1,updated_at=? WHERE id=?").bind(time,job_id).run();
      await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)")
        .bind(job_id,"checkpoint","worker_scaffold",JSON.stringify({note:"Extraction pipeline not yet connected"}),time).run();
      message.ack();
    }
  }
};
