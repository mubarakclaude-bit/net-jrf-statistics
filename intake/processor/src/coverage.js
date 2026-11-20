// Generic coverage matching against configured resource index. Lexical candidates only.
const words=s=>new Set(String(s||"").toLowerCase().split(/[^a-z0-9]+/).filter(w=>w.length>=3));
const score=(a,b)=>{const x=words(a),y=words(b);if(!x.size||!y.size)return 0;let n=0;for(const w of x)if(y.has(w))n++;return n/Math.max(x.size,y.size)};
export function buildCoverageReport(sourceItems,resourceIndex){
 const resources=Array.isArray(resourceIndex)?resourceIndex:(resourceIndex?.items||resourceIndex?.resources||[]);
 const items=Array.isArray(sourceItems)?sourceItems:(sourceItems?.items||[]);
 const entries=items.map(x=>{const sourceText=x.objective||x.text||x.title||"";const explicit=x.objective_id;const matches=resources.map(r=>({id:r.id||r.resource_id||null,name:r.name||r.title||r.label||"",match_score:score(sourceText,[r.name,r.title,r.label,r.description,...(r.keywords||[])].filter(Boolean).join(" "))})).filter(r=>r.id&&(explicit? r.id===explicit:r.match_score>=0.25)).sort((a,b)=>b.match_score-a.match_score).slice(0,5);return {source_item_id:x.id||x.segment_id||x.candidate_id||null,source_page:x.page||null,objective_id:explicit||null,source_excerpt:String(sourceText).slice(0,1000),matched_resource_candidates:matches,coverage_status:matches.length?"potentially-covered":"gap-or-unmapped"};});
 return {schema_version:1,entries,counts:{items:entries.length,potentially_covered:entries.filter(x=>x.coverage_status==="potentially-covered").length,gap_or_unmapped:entries.filter(x=>x.coverage_status!=="potentially-covered").length},review_required:true,warning:"Lexical/identifier-based matching only; does not assess resource quality, depth or correctness. Thresholds are heuristic."};
}
