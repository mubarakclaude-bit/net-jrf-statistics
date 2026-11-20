export function validateExtractionPages(pages,{maxPages=1000,maxPageText=200000,maxTotalText=8000000}={}) {
 if(!Array.isArray(pages)||pages.length>maxPages)return {valid:false,error:"invalid_extraction_payload"};
 let totalTextChars=0;const seenPages=new Set();
 for(const page of pages){
  if(!page||typeof page!=="object"||!Number.isInteger(page.page)||page.page<1||page.page>100000||typeof page.text!=="string"||page.text.length>maxPageText)return {valid:false,error:"invalid_extraction_payload"};
  if(seenPages.has(page.page))return {valid:false,error:"duplicate_extraction_page"};seenPages.add(page.page);
  if(page.confidence!==undefined&&page.confidence!==null&&(!Number.isFinite(page.confidence)||page.confidence<0||page.confidence>1))return {valid:false,error:"invalid_extraction_payload"};
  if(page.ocr!==undefined&&typeof page.ocr!=="boolean")return {valid:false,error:"invalid_extraction_payload"};
  totalTextChars+=page.text.length;if(totalTextChars>maxTotalText)return {valid:false,error:"extraction_text_limit"};
 }
 return {valid:true,totalTextChars};
}
