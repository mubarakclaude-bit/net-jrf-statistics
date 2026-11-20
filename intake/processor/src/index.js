const json=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{"content-type":"application/json","cache-control":"no-store"}});
const safe=(v,n=200)=>String(v||"").replace(/[\\x00-\\x1f\\x7f]/g,"").slice(0,n);
async function sha256(buf){const d=await crypto.subtle.digest("SHA-256",buf);return [...new Uint8Array(d)].map(x=>x.toString(16).padStart(2,"0")).join("")}
export default {async fetch(req,env){
 const u=new URL(req.url);if(req.method==="GET"&&u.pathname==="/health")return json({ok:true,service:"processor"});
 if(req.method!=="POST"||u.pathname!=="/process")return json({error:"not_found"},404);
 if(!env.PROCESSOR_TOKEN||req.headers.get("authorization")!==`Bearer ${env.PROCESSOR_TOKEN}`)return json({error:"unauthorized"},401);
 let p;try{p=await req.json()}catch{return json({error:"invalid_json"},400)}
 if(p.schema_version!==1||!p.job_id||!p.source_sha256||!p.object_key||!p.source_name)return json({error:"invalid_contract"},400);
 if(!env.SOURCE_BUCKET||!env.ARTIFACT_BUCKET||!env.EXTRACTOR_URL||!env.EXTRACTOR_TOKEN)return json({error:"blocked_infrastructure",missing:"required bindings or secrets"},503);
 const obj=await env.SOURCE_BUCKET.get(p.object_key);if(!obj)return json({error:"source_not_found"},404);
 const bytes=await obj.arrayBuffer();if(await sha256(bytes)!==p.source_sha256)return json({error:"source_hash_mismatch"},422);
 if(bytes.byteLength>20*1024*1024)return json({error:"source_size_limit"},413);
 const raw=new Uint8Array(bytes);let binary="";for(let i=0;i<raw.length;i+=32768)binary+=String.fromCharCode(...raw.subarray(i,i+32768));const b64=btoa(binary);
 let ext;try{const res=await fetch(env.EXTRACTOR_URL,{method:"POST",headers:{"authorization":`Bearer ${env.EXTRACTOR_TOKEN}`,"content-type":"application/json"},body:JSON.stringify({job_id:p.job_id,source_sha256:p.source_sha256,source_name:safe(p.source_name),pdf_base64:b64})});if(!res.ok)return json({error:"extractor_failed",status:res.status},502);ext=await res.json()}catch{return json({error:"extractor_unavailable"},502)}
 if(!Array.isArray(ext.pages)||ext.pages.length>1000||ext.pages.some((x,i)=>!Number.isInteger(x.page)||typeof x.text!=="string"||x.text.length>200000))return json({error:"invalid_extraction_payload"},422);
 const pages=ext.pages.map(x=>({page:x.page,text:x.text,confidence:Number.isFinite(x.confidence)?x.confidence:null,ocr:!!x.ocr})).sort((a,b)=>a.page-b.page);
 const artifact={schema_version:1,job_id:p.job_id,source_sha256:p.source_sha256,source_name:safe(p.source_name),extracted_at:new Date().toISOString(),pages,page_count:pages.length,stage:"extract",next_stage:"source-audit",warning:"Extraction only. Source audit, syllabus mapping, coverage audit, lesson drafting, verification and PR packaging have not been run."};
 const key=`jobs/${p.job_id}/extract.json`;await env.ARTIFACT_BUCKET.put(key,JSON.stringify(artifact),{httpMetadata:{contentType:"application/json"}});
 return json({accepted:true,job_id:p.job_id,stage:"extract",artifact_key:key,page_count:pages.length,next_stage:"source-audit",pipeline_status:"blocked_next_stage_not_implemented"});
}};
