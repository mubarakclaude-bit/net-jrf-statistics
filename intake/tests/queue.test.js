import assert from "node:assert/strict";
import worker from "../src/index.js";

class DB {
  constructor() {
    this.job={id:"12345678-1234-1234-1234-123456789abc",status:"accepted",source_sha256:"hash",manifest_key:null,object_key:"incoming/key",source_name:"source.txt",source_size:12,mime_type:"text/plain",attempts:0,dispatch_lease_until:null,dispatch_lease_token:null};
    this.events=[];
  }
  prepare(sql) {
    const db=this;
    return {
      bind(...args) {
        return {
          first:async()=>{
            if(sql.startsWith("SELECT id,status,source_sha256"))return {...db.job};
            if(sql.startsWith("SELECT id,status FROM intake_jobs"))return {id:db.job.id,status:db.job.status,source_sha256:db.job.source_sha256};
            if(sql.startsWith("SELECT status,attempts"))return {status:db.job.status,attempts:db.job.attempts};
            return null;
          },
          run:async()=>{
            let changes=0;
            if(sql.includes("SET dispatch_lease_until=?")) {
              const [until,token,updated,id]=args;
              if(id===db.job.id&&(!db.job.dispatch_lease_until||db.job.dispatch_lease_until<args[4])) {
                db.job.dispatch_lease_until=until;db.job.dispatch_lease_token=token;db.job.updated_at=updated;changes=1;
              }
            } else if(sql.includes("SET status='processing',stage='extract'")) {
              const [updated,id,token,status]=args;
              if(id===db.job.id&&token===db.job.dispatch_lease_token&&status===db.job.status) {
                db.job.status="processing";db.job.stage="extract";db.job.updated_at=updated;changes=1;
              }
            } else if(sql.includes("SET status='completed'")) {
              const [manifestKey,updated,id]=args;
              if(id===db.job.id&&db.job.status==="processing") {
                db.job.status="completed";db.job.stage="analysis";db.job.manifest_key=manifestKey;db.job.updated_at=updated;db.job.dispatch_lease_token=null;db.job.dispatch_lease_until=null;changes=1;
              }
            } else if(sql.includes("SET stage='extract',updated_at=?")) {
              const [updated,id,token]=args;
              if(id===db.job.id&&token===db.job.dispatch_lease_token&&db.job.status==="processing") {
                db.job.updated_at=updated;db.job.dispatch_lease_token=null;db.job.dispatch_lease_until=null;changes=1;
              }
            } else if(sql.includes("SET status=?,stage='dispatch',attempts=?")) {
              const [status,attempts,updated,message,id,token]=args;
              if(id===db.job.id&&token===db.job.dispatch_lease_token) {
                db.job.status=status;db.job.attempts=attempts;db.job.updated_at=updated;db.job.error_code="processor_dispatch_failed";db.job.error_message=message;db.job.dispatch_lease_token=null;db.job.dispatch_lease_until=null;changes=1;
              }
            } else if(sql.includes("SET status='blocked_infrastructure'")) {
              const [updated,id,token]=args;
              if(id===db.job.id&&token===db.job.dispatch_lease_token) {
                db.job.status="blocked_infrastructure";db.job.updated_at=updated;db.job.dispatch_lease_token=null;db.job.dispatch_lease_until=null;changes=1;
              }
            } else if(sql.startsWith("UPDATE intake_jobs SET dispatch_lease_until=NULL")) {
              const [id,token]=args;
              if(id===db.job.id&&token===db.job.dispatch_lease_token) {
                db.job.dispatch_lease_token=null;db.job.dispatch_lease_until=null;changes=1;
              }
            } else if(sql.startsWith("INSERT INTO intake_events")) {
              db.events.push(args);changes=1;
            }
            return {meta:{changes}};
          }
        };
      }
    };
  }
}

const db=new DB();
const extractBytes=new TextEncoder().encode("test artifact");
const digest=await crypto.subtle.digest("SHA-256",extractBytes);
const extractHash=[...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,"0")).join("");
const attemptId="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa";
const manifestKey=`jobs/${db.job.id}/attempts/1-${attemptId}/manifest.json`;
const extractKey=`jobs/${db.job.id}/attempts/1-${attemptId}/extract.json`;
const manifest={schema_version:1,job_id:db.job.id,attempt_id:attemptId,fencing_token:1,source_sha256:db.job.source_sha256,artifacts:[{key:extractKey,sha256:extractHash,size:extractBytes.byteLength}]};
const artifacts=new Map([[manifestKey,JSON.stringify(manifest)],[extractKey,extractBytes]]);
const artifactBucket={get:async key=>{const v=artifacts.get(key);if(!v)return null;if(typeof v==="string")return {text:async()=>v};return {arrayBuffer:async()=>v.buffer.slice(v.byteOffset,v.byteOffset+v.byteLength)};}};
const env={JOBS_DB:db,ARTIFACT_BUCKET:artifactBucket,PROCESSOR_URL:"https://processor/process",PROCESSOR_TOKEN:"secret",PROCESSOR_CALLBACK_TOKEN:"callback"};
const workerFetch=globalThis.fetch;let callbackResult;
globalThis.fetch=async()=>{
  // Simulate a completion callback arriving while the dispatch request is still in flight.
  const callbackPayload={job_id:db.job.id,status:"completed",stage:"analysis",attempt_id:"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",fencing_token:1,manifest_key:"jobs/12345678-1234-1234-1234-123456789abc/attempts/1-aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/manifest.json",summary:{pages:1,segments:2,production_created:false},artifact_keys:["jobs/12345678-1234-1234-1234-123456789abc/attempts/1-aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/extract.json","jobs/12345678-1234-1234-1234-123456789abc/attempts/1-aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/manifest.json"]};
  callbackResult=await worker.fetch(new Request("https://intake/internal/processor-result",{method:"POST",headers:{authorization:"Bearer callback","content-type":"application/json"},body:JSON.stringify(callbackPayload)}),env);
  return new Response("ok",{status:200});
};
let ack=0,retry=0;
try{await worker.queue({messages:[{body:{job_id:db.job.id},ack(){ack++},retry(){retry++}}]},env);}finally{globalThis.fetch=workerFetch;}
assert.equal(callbackResult.status,200,"completion callback should succeed during dispatch");
assert.equal(db.job.status,"completed","fast callback must not be rejected or overwritten");
assert.equal(ack,1,"queue message should be acknowledged after dispatch");
assert.equal(retry,0);
assert.ok(db.events.some(e=>e[1]==="processing_started"));
assert.ok(db.events.some(e=>e[1]==="processor_result"));

const invalid=await worker.fetch(new Request("https://intake/internal/processor-result",{method:"POST",headers:{authorization:"Bearer callback","content-type":"application/json"},body:JSON.stringify({job_id:db.job.id,status:"completed",stage:"analysis",attempt_id:"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",fencing_token:1,manifest_key:"jobs/12345678-1234-1234-1234-123456789abc/attempts/1-aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/manifest.json",artifact_keys:["outside-prefix"]})}),env);
assert.equal(invalid.status,400,"callback must reject artifact keys outside the job namespace");

const failedDb=new DB();let failRetry=0,failAck=0;
const failEnv={JOBS_DB:failedDb,PROCESSOR_URL:"https://processor/process",PROCESSOR_TOKEN:"secret"};
const fetchFail=globalThis.fetch;globalThis.fetch=async()=>new Response("down",{status:502});
try{await worker.queue({messages:[{body:{job_id:failedDb.job.id},ack(){failAck++},retry(){failRetry++}}]},failEnv);}finally{globalThis.fetch=fetchFail;}
assert.equal(failedDb.job.status,"failed_retryable");
assert.equal(failedDb.job.attempts,1);
assert.equal(failedDb.job.dispatch_lease_token,null);
assert.equal(failRetry,1);assert.equal(failAck,0);

const blockedDb=new DB();const blockedEnv={JOBS_DB:blockedDb};let blockedAck=0,blockedRetry=0;
await worker.queue({messages:[{body:{job_id:blockedDb.job.id},ack(){blockedAck++},retry(){blockedRetry++}}]},blockedEnv);
assert.equal(blockedDb.job.status,"blocked_infrastructure");
assert.equal(blockedAck,1);assert.equal(blockedRetry,0);
console.log("queue callback-race, retry and blocker tests passed");

const duplicatePayload={job_id:db.job.id,status:"completed",stage:"analysis",attempt_id:"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",fencing_token:1,manifest_key:manifestKey,artifact_keys:[extractKey,manifestKey]};
const duplicateCallback=await worker.fetch(new Request("https://intake/internal/processor-result",{method:"POST",headers:{authorization:"Bearer callback","content-type":"application/json"},body:JSON.stringify(duplicatePayload)}),env);
assert.equal(duplicateCallback.status,200,"repeated completion callback should be accepted idempotently");
assert.equal((await duplicateCallback.json()).duplicate,true,"duplicate callback should be marked as duplicate");

const corruptedArtifacts=new Map([[manifestKey,JSON.stringify(manifest)],[extractKey,new TextEncoder().encode("tampered artifact")]]);
const corruptEnv={...env,ARTIFACT_BUCKET:{get:async key=>{const v=corruptedArtifacts.get(key);if(!v)return null;if(typeof v==="string")return {text:async()=>v};return {arrayBuffer:async()=>v.buffer.slice(v.byteOffset,v.byteOffset+v.byteLength)};}}};
const integrityPayload={...duplicatePayload,job_id:"12345678-1234-1234-1234-123456789abc"};
// The ledger is already completed in the fixture, so duplicate behavior takes precedence;
// use a separate state fixture in the integrity test to exercise hash verification.
const integrityDb=new DB();integrityDb.job.status="processing";
const integrityEnv={...corruptEnv,JOBS_DB:integrityDb};
const integrity=await worker.fetch(new Request("https://intake/internal/processor-result",{method:"POST",headers:{authorization:"Bearer callback","content-type":"application/json"},body:JSON.stringify({...duplicatePayload,job_id:integrityDb.job.id})}),integrityEnv);
assert.equal(integrity.status,422,"tampered artifact bytes must fail manifest integrity validation");
assert.equal(integrityDb.job.status,"processing","integrity failure must not complete the ledger");
