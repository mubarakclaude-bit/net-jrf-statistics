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
    if (!auth(request, env)) return json({error:"unauthorized"},401);
    if (request.method === "GET" && url.pathname.startsWith("/jobs/")) {
      const id = url.pathname.slice("/jobs/".length);
      if (!id || id.includes("/")) return json({error:"invalid_job_id"},400);
      const job = await env.JOBS_DB.prepare("SELECT id,source_name,source_size,status,stage,attempts,created_at,updated_at,error_code,error_message FROM intake_jobs WHERE id=?").bind(id).first();
      if (!job) return json({error:"not_found"},404);
      const events = await env.JOBS_DB.prepare("SELECT event,stage,details_json,created_at FROM intake_events WHERE job_id=? ORDER BY id DESC LIMIT 30").bind(id).all();
      return json({job,events:events.results||[]});
    }
    if (request.method !== "POST" || url.pathname !== "/upload") return json({error:"not_found"},404);
    const form = await request.formData().catch(()=>null);
    if (!form) return json({error:"invalid_multipart"},400);
    const file = form.get("file");
    if (!(file instanceof File)) return json({error:"missing_file"},400);
    const limit = Number(env.MAX_UPLOAD_BYTES)||MAX_UPLOAD_BYTES;
    if (file.size <= 0 || file.size > limit) return json({error:"file_size_limit"},413);
    const name = file.name || "source.pdf";
    if (!name.toLowerCase().endsWith(".pdf") || file.type !== "application/pdf") return json({error:"pdf_only"},415);
    const bytes = await file.arrayBuffer();
    const signature = new Uint8Array(bytes).slice(0,5);
    if (signature[0]!==37 || signature[1]!==80 || signature[2]!==68 || signature[3]!==70 || signature[4]!==45) return json({error:"invalid_pdf_signature"},415);
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
      const job = await env.JOBS_DB.prepare("SELECT status,stage FROM intake_jobs WHERE id=?").bind(job_id).first();
      if (!job || job.status === "completed") { message.ack(); continue; }
      const time = now();
      // Scaffold checkpoint: full extraction/authoring/review pipeline is not yet connected.
      await env.JOBS_DB.prepare("UPDATE intake_jobs SET status='needs_worker',stage='worker_scaffold',attempts=attempts+1,updated_at=? WHERE id=?").bind(time,job_id).run();
      await env.JOBS_DB.prepare("INSERT INTO intake_events (job_id,event,stage,details_json,created_at) VALUES (?,?,?,?,?)")
        .bind(job_id,"checkpoint","worker_scaffold",JSON.stringify({note:"Extraction and content pipeline not yet connected"}),time).run();
      message.ack();
    }
  }
};
