import assert from "node:assert/strict";
import {validateExtractionPages} from "../src/extraction.js";
assert.deepEqual(validateExtractionPages([{page:1,text:"ok"}]),{valid:true,totalTextChars:2});
assert.equal(validateExtractionPages(null).valid,false);
assert.equal(validateExtractionPages([{page:0,text:"invalid page"}]).valid,false);
assert.equal(validateExtractionPages([{page:1,text:"x".repeat(200001)}]).valid,false);
assert.equal(validateExtractionPages(Array.from({length:41},(_,i)=>({page:i+1,text:"x".repeat(200000)}))).error,"extraction_text_limit");
assert.equal(validateExtractionPages(Array.from({length:1001},(_,i)=>({page:i+1,text:""}))).valid,false);
assert.equal(validateExtractionPages([{page:1,text:"x",ocr:true},{page:2,text:"y",ocr:false}]).valid,true);
console.log("extraction bounds tests passed");

assert.equal(validateExtractionPages([{page:1,text:"a"},{page:1,text:"b"}]).error,"duplicate_extraction_page");
assert.equal(validateExtractionPages([{page:1,text:"ok",confidence:1.2}]).valid,false);
assert.equal(validateExtractionPages([{page:1,text:"ok",confidence:0.5,ocr:"yes"}]).valid,false);
assert.equal(validateExtractionPages([{page:2,text:"ok",confidence:0,ocr:true}]).valid,true);
