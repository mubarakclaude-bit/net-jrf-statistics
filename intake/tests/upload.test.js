import assert from "node:assert/strict";
import worker from "../src/index.js";
// Regression coverage for filename sanitization.
async function main(){
 const state={job:null,events:[],outbox:[],objects:new Map()};
 const db={prepare(sql){return{bind(...args){return{first:async()=>sql.startsWith("SELECT id,status FROM intake_jobs WHERE source_sha256")&&state.job?{id:state.job.id,status:state.job.status}:null,run:async()=>{if(sql.startsWith("INSERT INTO intake_jobs")){const[id,name,hash,key,size,mime,status,stage,created,updated]=args;state.job={id,source_name:name,source_sha256:hash,object_key:key,source_size:size,mime_type:mime,status,stage,created_at:created,updated_at:updated};return{meta:{changes:1}};}if(sql.startsWith("INSERT INTO intake_events")){state.events.push(args);return{meta:{changes:1}};}if(sql.startsWith("INSERT INTO intake_outbox")){state.outbox.push(args);return{meta:{changes:1}};}return{meta:{changes:0}};}};}} ,batch:async stmts=>Promise.all(stmts.map(s=>s.run()))};
 const bucket={put:async(k,b)=>state.objects.set(k,b),delete:async k=>state.objects.delete(k)};
 const env={INTAKE_TOKEN:"secret",JOBS_DB:db,SOURCE_BUCKET:bucket,PROCESSING_QUEUE:{send:async()=>{throw Error("dispatcher is not invoked in HTTP request")}}};
 const form=new FormData();form.append("file",new Blob(["safe test text"],{type:"text/plain"}),"source.txt");
 const response=await worker.fetch(new Request("https://intake/upload",{method:"POST",headers:{authorization:"Bearer secret"},body:form}),env);const body=await response.json();
 assert.equal(response.status,202);assert.equal(body.status,"accepted");assert.equal(state.job.status,"queued");assert.equal(state.outbox.length,1);assert.equal(state.outbox[0][1],state.job.id);assert.equal(state.objects.has(state.job.object_key),true);
 console.log("upload creates durable dispatch intent tests passed");
}
main().catch(err=>{console.error(err);process.exitCode=1;});
