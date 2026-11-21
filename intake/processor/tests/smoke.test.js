import assert from "node:assert/strict";
const worker=(await import("../src/index.js")).default;
const response=await worker.fetch(new Request("https://processor/health"),{});
assert.equal(response.status,200);assert.deepEqual(await response.json(),{ok:true,service:"processor"});
const unauthorized=await worker.fetch(new Request("https://processor/process",{method:"POST",headers:{"content-type":"application/json"},body:"{}"}),{PROCESSOR_TOKEN:"x"});
assert.equal(unauthorized.status,401);
const malformed=await worker.fetch(new Request("https://processor/process",{method:"POST",headers:{"content-type":"application/json","authorization":"Bearer x"},body:"{}"}),{PROCESSOR_TOKEN:"x"});
assert.equal(malformed.status,400);
const {auditSource}=await import("../src/audit.js");
const aud=auditSource({pages:[{page:1,text:"Question 1. Find the unbiased estimator of variance based on independent normal observations."}]});
assert.equal(aud.segments.length,1);assert.equal(aud.segments[0].page,1);assert.ok(aud.segments[0].labels.includes("question_or_prompt"));
const multi=auditSource({pages:[{page:1,text:"Question 1. Explain probability theory and its applications in detail. Question 2. Calculate the expected value of a random variable given the following conditions and data."}]});
assert.ok(multi.segments.length>=2);
const {mapText}=await import("../src/mapper.js");
const mapped=mapText("Explain matrix eigenvalue properties.",{items:[{id:"topic-a",name:"Matrix eigenvalues",keywords:["eigenvalue"]}]});
assert.equal(mapped.candidates[0].id,"topic-a");
const {buildCoverageReport}=await import("../src/coverage.js");
const coverage=buildCoverageReport([{segment_id:"s1",page:1,text:"matrix eigenvalues and vectors"}],[{id:"r1",name:"Matrix eigenvalues"}]);
assert.equal(coverage.entries[0].coverage_status,"potentially-covered");
console.log("processor smoke and heuristic tests passed");

const {verifyOutputs}=await import("../src/verify.js");
const verified=verifyOutputs([{type:"lesson",content:"Example",source_segment_ids:["segment-1"]}],aud.segments);
assert.equal(verified.failed,0);
const bad=verifyOutputs([{type:"lesson",content:"Untraceable",source_segment_ids:["missing"]}],aud.segments);
assert.ok(bad.failed>0);

const dup=verifyOutputs([{type:"lesson",content:"duplicate refs",source_segment_ids:["segment-1","segment-1"]}],aud.segments);
assert.ok(dup.failed>0);
const noType=verifyOutputs([{content:"missing type",source_segment_ids:["segment-1"]}],aud.segments);
assert.ok(noType.failed>0);

// Audit edge cases: empty input, stable IDs, source text bounds and conservative review flags.
const emptyAudit=auditSource({pages:[]});
assert.equal(emptyAudit.segments_detected,0);
const bounded=auditSource({pages:[{page:7,text:"A".repeat(13000)}]});
assert.equal(bounded.segments[0].page,7);
assert.equal(bounded.segments[0].segment_id,"segment-1");
assert.equal(bounded.segments[0].text.length,12000);
assert.equal(bounded.review_required,true);
const stable=auditSource({pages:[{page:2,text:"Explain a general concept and discuss its practical implications in detail."}]});
assert.equal(stable.segments[0].segment_id,"segment-1");

// Processor contract must reject malformed identity and non-job-scoped source keys.
const validJob="12345678-1234-1234-1234-123456789abc";
const validHash="a".repeat(64);
const basePayload={schema_version:1,job_id:validJob,active_attempt_id:"12345678-1234-1234-1234-123456789abc",source_sha256:validHash,object_key:"incoming/"+validJob+"/"+validHash+"/source.txt",source_name:"source.txt",source_size:12};
const invalidKeyPayload={...basePayload,object_key:"incoming/other/"+validHash+"/source.txt"};
const invalidKey=await worker.fetch(new Request("https://processor/process",{method:"POST",headers:{"content-type":"application/json","authorization":"Bearer x"},body:JSON.stringify(invalidKeyPayload)}),{PROCESSOR_TOKEN:"x"});
assert.equal(invalidKey.status,400,"processor rejects source keys outside the job namespace before storage access");
const malformedId=await worker.fetch(new Request("https://processor/process",{method:"POST",headers:{"content-type":"application/json","authorization":"Bearer x"},body:JSON.stringify({...basePayload,job_id:"../bad"})}),{PROCESSOR_TOKEN:"x"});
assert.equal(malformedId.status,400,"processor rejects malformed job IDs");

assert.throws(()=>verifyOutputs("not-array",aud.segments));
assert.throws(()=>verifyOutputs([],Array.from({length:1001},(_,i)=>({segment_id:"s"+i}))));
const malformedRefs=verifyOutputs([{type:"x",content:"ok",source_segment_ids:[null]}],aud.segments);assert.ok(malformedRefs.failed>0);
const tooLongType=verifyOutputs([{type:"x".repeat(129),content:"ok",source_segment_ids:["segment-1"]}],aud.segments);assert.ok(tooLongType.failed>0);
