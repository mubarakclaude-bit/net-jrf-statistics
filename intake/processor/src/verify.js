// Independent deterministic checks on configured generated outputs; does not assess factual correctness.
export function verifyOutputs(outputs,segments){
 const ids=new Set((segments||[]).map(s=>s.segment_id)),checks=[];
 (outputs||[]).forEach((o,i)=>{
  const refs=o?.source_segment_ids||[];
  checks.push({output_index:i,check:"provenance_references",passed:Array.isArray(refs)&&refs.length>0&&refs.every(id=>ids.has(id)),referenced_segments:refs});
  checks.push({output_index:i,check:"nonempty_content",passed:typeof o?.content==="string"&&o.content.trim().length>0});
  checks.push({output_index:i,check:"bounded_content",passed:typeof o?.content==="string"&&o.content.length<=100000});
  checks.push({output_index:i,check:"output_type",passed:typeof o?.type==="string"&&o.type.trim().length>0});
  checks.push({output_index:i,check:"unique_source_refs",passed:Array.isArray(refs)&&new Set(refs).size===refs.length});
 });
 return {schema_version:1,checks,passed:checks.filter(x=>x.passed).length,failed:checks.filter(x=>!x.passed).length,review_required:true,warning:"Deterministic structural checks only; no independent semantic, factual or domain validation."};
}
