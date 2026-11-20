// Generic document taxonomy mapper. No domain/module assumptions.
// Taxonomy may be provided per workspace/job by an authorized configuration.
export function mapText(text,taxonomy){
 const t=String(text||"").toLowerCase(),items=(taxonomy?.items||taxonomy?.topics||[]);
 const candidates=items.map(item=>{const labels=[item.name,item.label,item.description,...(item.keywords||[])].filter(Boolean).map(x=>String(x).toLowerCase());const hits=labels.filter(x=>x.length>2&&t.includes(x));return {id:item.id||null,name:item.name||item.label||null,score:hits.length,matched_terms:hits,parents:item.parent_ids||item.parent_id||null};}).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,5);
 return {candidates,confidence:candidates.length?"low":"none",review_required:true,warning:"Lexical matching only; confirm mappings against the source and selected taxonomy."};
}
