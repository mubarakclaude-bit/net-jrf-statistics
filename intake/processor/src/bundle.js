// Generic JSON bundle builder. Caller supplies artifact objects and verified metadata.
const UUID=/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const HASH=/^[a-f0-9]{64}$/i;
export function buildBundle({job_id,source_sha256,artifacts,review_required=true}){
 if(!UUID.test(job_id||"")||!HASH.test(source_sha256||"")||!Array.isArray(artifacts)||artifacts.length>20||typeof review_required!=="boolean")throw new Error("invalid_bundle_input");
 const seen=new Set();let total=0;
 const entries=artifacts.map((a,i)=>{
  if(!a||typeof a.key!=="string"||!a.key.startsWith(`jobs/${job_id}/`)||a.key.length>512||typeof a.content!=="string"||a.content.length>8*1024*1024||typeof (a.content_type||"application/json")!=="string")throw new Error("invalid_artifact");
  if(seen.has(a.key))throw new Error("duplicate_artifact_key");seen.add(a.key);total+=a.content.length;if(total>8*1024*1024)throw new Error("bundle_content_limit");
  return {ordinal:i+1,key:a.key,content_type:a.content_type||"application/json",content:a.content};
 });
 return {schema_version:1,bundle_type:"generic-source-processing",job_id,source_sha256,created_at:new Date().toISOString(),review_required,artifact_count:entries.length,artifacts:entries,limitations:["Bundle preserves supplied artifacts; it does not certify their accuracy or completeness."]};
}
