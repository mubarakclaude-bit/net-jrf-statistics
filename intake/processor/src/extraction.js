export function validateExtractionPages(pages,{maxPages=1000,maxPageText=200000,maxTotalText=8000000}={}){
 if(!Array.isArray(pages)||pages.length>maxPages)return {valid:false,error:"invalid_extraction_payload"};
 let totalTextChars=0;
 for(const page of pages){
  if(!page||typeof page!=="object"||!Number.isInteger(page.page)||page.page<1||page.page>100000||typeof page.text!=="string"||page.text.length>maxPageText)return {valid:false,error:"invalid_extraction_payload"};
  totalTextChars+=page.text.length;if(totalTextChars>maxTotalText)return {valid:false,error:"extraction_text_limit"};
 }
 return {valid:true,totalTextChars};
}
