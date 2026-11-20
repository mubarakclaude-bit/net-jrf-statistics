// Deterministic preliminary source audit. Treat output as candidates, not verified questions.
const clean=s=>String(s||"").replace(/\s+/g," ").trim();
const splitBlocks=pages=>pages.flatMap(p=>clean(p.text).split(/(?=(?:Question\s*\d+|Q\s*\d+|\d{1,3}[.)]\s))/i).map((text,i)=>({page:p.page,block_index:i,text})).filter(x=>x.text.length>=40);
const likelyQuestion=t=>/(?:question\s*\d+|\bQ\s*\d+|\d{1,3}[.)]\s+[A-Z]|(?:which|find|calculate|determine|estimate|test|prove|show)\b)/i.test(t);
const likelyAnswerKey=t=>/(?:answer\s*key|correct\s+option|\b[1-4]\s*[.,;\s]+[1-4]\s*[.,;\s]+[1-4])/i.test(t);
export function auditSource(artifact){
 const blocks=splitBlocks(artifact.pages||[]),candidates=blocks.filter(b=>likelyQuestion(b.text));
 const keyPages=(artifact.pages||[]).filter(p=>likelyAnswerKey(p.text)).map(p=>p.page);
 return {schema_version:1,source_sha256:artifact.source_sha256,created_at:new Date().toISOString(),pages_reviewed:(artifact.pages||[]).length,blocks_detected:blocks.length,question_candidates:candidates.map((b,i)=>({candidate_id:"candidate-"+(i+1),page:b.page,text:b.text.slice(0,12000),length:b.text.length,confidence:"heuristic",flags:["not_source-verified","question-boundary-heuristic"]})),answer_key_page_candidates:keyPages,excluded_or_unclassified:blocks.length-candidates.length,review_required:true,limitations:["Heuristic segmentation can miss, merge or misclassify items.","OCR/extraction text may be incomplete.","Answer keys have not been reconciled.","This is not mathematical verification."]};
}
