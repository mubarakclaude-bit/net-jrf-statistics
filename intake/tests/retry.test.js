import assert from "node:assert/strict";
import worker from "../src/index.js";

const id="12345678-1234-1234-1234-123456789abc",text="verified source for retry",bytes=new TextEncoder().encode(text);
const sha=async b=>{const d=await crypto.subtle.digest("SHA-256",b);return [...new Uint8Array(d)].map(x=>x.toString(16).padStart(2,"0")).join("");};
const hash=await sha(bytes);
function makeDb(status="blocked_infrastructure"){
 const state={job:{id,status,source_sha256:hash,object_key:"incoming/source",source_size:bytes.byteLength},events:[]};
 const db={state,prepare(sql){return {bind(...args){return {first:async()=>state.job,run:async()=>{
 let changes=0;
 if(sql.startsWith("UPDATE intake_jobs SET status='queued'")){const [updated,idArg,statusArg]=args;if(idArg===state.job.id&&statusArg===state.job.status){state.job.status="queued";state.job.updated_at=updated;changes=1;}}
 else if(sql.startsWith("UPDATE intake_jobs SET status='blocked_infrastructure'")){const [updated,idArg]=args;if(idArg===state.job.id&&state.job.status==="queued"){state.job.status="blocked_infrastructure";state.job.updated_at=updated;changes=1;}}
 else if(sql.startsWith("INSERT INTO intake_events")){state.events.push(args);changes=1;}
 return {meta:{changes}};
}};}}};return db;
}
const bucketFor=(data)=>({get:async key=>key==="incoming/source"?{arrayBuffer:async()=>data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength)}:null});
const queueOk={send:async message=>{assert.equal(message.job_id,id);}};
const env={INTAKE_TOKEN:"secret",JOBS_DB:makeDb().state};
const db=makeDb();const envOk={INTAKE_TOKEN:"secret",JOBS_DB:db,SOURCE_BUCKET:bucketFor(bytes),PROCESSING_QUEUE:queueOk};
const res=await worker.fetch(new Request(`https://intake/jobs/${id}/retry`,{method:"POST",headers:{authorization:"Bearer secret"}}),envOk);
assert.equal(res.status,202);assert.equal(db.state.job.status,"queued");assert.ok(db.state.events.some(e=>e[1]==="manual_retry_requested"));

const badDb=makeDb();const badEnv={INTAKE_TOKEN:"secret",JOBS_DB:badDb,SOURCE_BUCKET:bucketFor(new TextEncoder().encode("tampered")),PROCESSING_QUEUE:queueOk};
const bad=await worker.fetch(new Request(`https://intake/jobs/${id}/retry`,{method:"POST",headers:{authorization:"Bearer secret"}}),badEnv);
assert.equal(bad.status,422);assert.equal(badDb.state.job.status,"blocked_infrastructure");

const failDb=makeDb("failed_retryable");const failEnv={INTAKE_TOKEN:"secret",JOBS_DB:failDb,SOURCE_BUCKET:bucketFor(bytes),PROCESSING_QUEUE:{send:async()=>{throw new Error("offline");}}};
const fail=await worker.fetch(new Request(`https://intake/jobs/${id}/retry`,{method:"POST",headers:{authorization:"Bearer secret"}}),failEnv);
assert.equal(fail.status,503);assert.equal(failDb.state.job.status,"blocked_infrastructure");assert.ok(failDb.state.events.some(e=>e[1]==="retry_enqueue_failed"));
console.log("manual retry recovery tests passed");
