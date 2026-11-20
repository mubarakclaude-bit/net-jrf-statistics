import assert from "node:assert/strict";
import {buildBundle} from "../src/bundle.js";
const b=buildBundle({job_id:"job-1",source_sha256:"abc",artifacts:[{key:"a.json",content:"{}"}]});
assert.equal(b.bundle_type,"generic-source-processing");assert.equal(b.artifact_count,1);assert.equal(b.review_required,true);
assert.throws(()=>buildBundle({job_id:"",source_sha256:"x",artifacts:[]}));
assert.throws(()=>buildBundle({job_id:"j",source_sha256:"x",artifacts:[{}]}));
console.log("bundle tests passed");
