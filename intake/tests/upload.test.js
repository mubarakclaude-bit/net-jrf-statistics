import assert from "node:assert/strict";
import worker from "../src/index.js";

const state={job:null,events:[],objects:new Map()};
const db={prepare(sql){return {bind(...args){return {first:async()=>{
 if(sql.startsWith("SELECT id,status FROM intake_jobs WHERE source_sha256"))return state.job?{id:state.job.id,status:state.job.status}:null;
 return null;
},run:async()=>{
 if(sql.startsWith("INSERT INTO intake_jobs")){const [id,name,hash,key,size,mime,status,stage,created,updated]=args;state.job={id,source_name:name,source_sha256:hash,object_key:key,source_size:size,mime_type:mime,status,stage,created_at:created,updated_at:updated};return {meta:{changes:1}};}
 if(sql.startsWith("INSERT INTO intake_events")){state.events.push(args);return {meta:{changes:1}};}
 if(sql.includes("SET status='blocked_infrastructure'")){const [updated,id]=args;if(state.job?.id===id){state.job.status="blocked_infrastructure";state.job.stage="intake";state.job.updated_at=updated;state.job.error_code="intake_enqueue_failed";return {meta:{changes:1}};}}
 return {meta:{changes:0}};
}};}}};
const bucket={put:async(key,bytes)=>state.objects.set(key,bytes),delete:async key=>state.objects.delete(key)};
const queue={send:async()=>{throw new Error("simulated queue unavailable")}};
const env={INTAKE_TOKEN:"secret",JOBS_DB:db,SOURCE_BUCKET:bucket,PROCESSING_QUEUE:queue};
const form=new FormData();form.append("file",new Blob(["safe test text"],{type:"text/plain"}),"source.txt");
const response=await worker.fetch(new Request("https://intake/upload",{method:"POST",headers:{authorization:"Bearer secret"},body:form}),env);
const body=await response.json();
assert.equal(response.status,503);
assert.equal(body.owner_action_required,true);
assert.equal(state.job.status,"blocked_infrastructure");
assert.equal(state.objects.has(state.job.object_key),true,"source object must remain available for recovery");
assert.ok(state.events.some(e=>e[1]==="intake_enqueue_blocked"));
console.log("upload acceptance recovery tests passed");
