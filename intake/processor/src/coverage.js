// Generic learning-resource coverage comparator.
// Requires source-derived objectives and an explicitly supplied resource index.
export function buildCoverageReport(sourceItems,resourceIndex){
 const resources=Array.isArray(resourceIndex)?resourceIndex:(resourceIndex?.items||resourceIndex?.resources||[]);
 const covered=new Set(resources.flatMap(x=>[x.id,x.objective_id,...(x.objective_ids||[])]).filter(Boolean));
 const items=Array.isArray(sourceItems)?sourceItems:(sourceItems?.items||[]);
 const entries=items.map(x=>({source_item_id:x.id||x.candidate_id||null,source_page:x.page||null,objective_id:x.objective_id||null,objective:x.objective||x.text||x.title||"",matched_resource_ids:x.objective_id&&covered.has(x.objective_id)?[x.objective_id]:[],coverage_status:x.objective_id?(covered.has(x.objective_id)?"potentially-covered":"gap-or-unmapped"):"unmapped"}));
 return {schema_version:1,entries,counts:{items:entries.length,potentially_covered:entries.filter(x=>x.coverage_status==="potentially-covered").length,gap_or_unmapped:entries.filter(x=>x.coverage_status!=="potentially-covered").length},review_required:true,warning:"Identifier-based comparison only; does not assess resource quality, depth or correctness."};
}
