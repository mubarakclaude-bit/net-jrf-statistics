export function buildCoverageReport(mapping,lessonIndex){
 const lessons=Array.isArray(lessonIndex)?lessonIndex:(lessonIndex?.lessons||[]);
 const covered=new Set(lessons.map(x=>x.topicId||x.topic_id).filter(Boolean));
 const entries=(mapping.candidates||[]).flatMap(q=>(q.match?.suggestions||[]).flatMap(m=>(m.topic_candidates||[]).map(t=>({candidate_id:q.candidate_id,page:q.page,module:m.module,topic_id:t.id,topic_name:t.name,lexical_score:t.score,existing_lesson:covered.has(t.id)}))));
 const counts={candidate_topics:entries.length,topics_with_lesson:entries.filter(x=>x.existing_lesson).length,topics_without_lesson:entries.filter(x=>!x.existing_lesson).length};
 return {schema_version:1,job_id:mapping.job_id,source_sha256:mapping.source_sha256,entries,counts,review_required:true,warning:"Coverage is lexical candidate matching, not proof that a lesson adequately teaches the source concept."};
}
