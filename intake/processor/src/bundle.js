// Generic JSON bundle builder. Caller supplies artifact objects and verified metadata.
export function buildBundle({job_id,source_sha256,artifacts,review_required=true}){
 if(!job_id||!source_sha256||!Array.isArray(artifacts))throw new Error("invalid_bundle_input");
 const entries=artifacts.map((a,i)=>{
  if(!a||typeof a.key!=="string"||typeof a.content!=="string")throw new Error("invalid_artifact");
  return {ordinal:i+1,key:a.key,content_type:a.content_type||"application/json",content:a.content};
 });
 return {schema_version:1,bundle_type:"generic-source-processing",job_id,source_sha256,created_at:new Date().toISOString(),review_required,artifact_count:entries.length,artifacts:entries,limitations:["Bundle preserves supplied artifacts; it does not certify their accuracy or completeness."]};
}
