import assert from "node:assert/strict";
const worker=(await import("../src/index.js")).default;
const response=await worker.fetch(new Request("https://processor/health"),{});
assert.equal(response.status,200);assert.deepEqual(await response.json(),{ok:true,service:"processor"});
const unauthorized=await worker.fetch(new Request("https://processor/process",{method:"POST",headers:{"content-type":"application/json"},body:"{}"}),{PROCESSOR_TOKEN:"x"});
assert.equal(unauthorized.status,401);
const malformed=await worker.fetch(new Request("https://processor/process",{method:"POST",headers:{"content-type":"application/json","authorization":"Bearer x"},body:"{}"}),{PROCESSOR_TOKEN:"x"});
assert.equal(malformed.status,400);
console.log("processor contract smoke tests passed");
