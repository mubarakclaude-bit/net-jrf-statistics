/* ---------- export ---------- */
function exportMd(mid,what){
  let list=mid?(S.bank[mid]||[]):allQ();
  if(what==="wrong")list=list.filter(q=>statusOf(q.id)==="wrong");
  if(what==="flag")list=list.filter(q=>(S.att[q.id]||{}).f);
  if(what==="unseen")list=list.filter(q=>statusOf(q.id)==="unseen");
  if(!list.length)return null;
  const L=["# NET JRF Statistics — "+(mid?(modById(mid)||{}).name:"all modules"),"",
    "*"+list.length+" questions · "+({wrong:"answered wrongly",flag:"flagged",unseen:"not yet attempted",all:"everything loaded"}[what])+" · exported "+dayStr(now())+"*",""];
  const byM={};list.forEach(q=>(byM[q.moduleId]||(byM[q.moduleId]=[])).push(q));
  Object.keys(byM).forEach(id=>{
    const m=modById(id);L.push("## "+(m?m.name+" — "+m.marks+" marks":id),"");
    byM[id].forEach((q,k)=>{
      L.push("**"+(k+1)+". "+String(q.stem).replace(/\s+/g," ")+"**","");
      (q.statements||[]).forEach((s,j)=>L.push("- ("+String.fromCharCode(65+j)+") "+s));
      if((q.pairs||[]).length){L.push("");L.push("| List I | List II |");L.push("|---|---|");
        q.pairs.forEach(p=>L.push("| "+(p[0]!=null?p[0]:p.i)+" | "+(p[1]!=null?p[1]:p.ii)+" |"))}
      if((q.items||[]).length)L.push("",q.items.map((it,j)=>String.fromCharCode(65+j)+". "+it).join("  "));
      L.push("");
      if(isFree(q))L.push("*Write in your answer — nothing to guess from.*");
      else (q.options||[]).forEach((o,j)=>L.push(String.fromCharCode(65+j)+". "+o));
      L.push("","> **Answer"+(isFree(q)?": ":" ")+q.answer+(isFree(q)?"":".")+"** "+String(q.explanation||"").replace(/\s+/g," "));
      if(q.check)L.push(">","> *Check:* "+q.check);
      if(q.verdicts)Object.keys(q.verdicts).sort().forEach(Ltr=>{const v=q.verdicts[Ltr];
        L.push(">","> ("+Ltr+") "+((v.tf===true||v.tf==="T")?"TRUE":"FALSE")+" — "+(v.why||""))});
      L.push("","---","");
    });
  });
  return L.join("\n");
}
function exportCsv(){
  const rows=[["module","qid","format","source","topic","answered","last_result","attempts","flagged"]];
  mods().forEach(m=>(S.bank[m.id]||[]).forEach(q=>{const a=S.att[q.id]||{};
    rows.push([m.name,q.id,q.format,q.source,q.topic||"",a.n?"yes":"no",a.n?(a.o?"correct":"wrong"):"",a.n||0,a.f?"yes":"no"])}));
  return rows.map(r=>r.map(c=>'"'+String(c).replace(/"/g,'""')+'"').join(",")).join("\n");
}
async function saveFile(name,data){
  if(!S.dl){toast("Saving files is not available here");return}
  try{await S.dl.save({filename:name,data:data});toast("Saved")}
  catch(e){const c=e&&e.code;toast(c==="declined"?"Save cancelled":"Could not save"+(c?" ("+c+")":""))}
}

