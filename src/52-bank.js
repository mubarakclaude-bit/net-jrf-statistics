/* ---------- bank ---------- */
function vBank(){
  const g=gate();if(g)return g;
  if(S.drill)return drillHTML();
  const f=S.filt;
  const ms=mods();
  const needed=f.mod?[f.mod]:ms.map(m=>m.id);
  const missing=needed.filter(id=>!S.bank[id]&&loadedCount(id)>0);
  if(missing.length){
    setTimeout(()=>{ensure(missing).then(()=>{if(S.route==="bank")render()})},0);
    return '<div class="hd"><h1>Question bank</h1></div>'+
    '<div class="card"><div class="kv"><span>Loading '+missing.length+' module'+(missing.length>1?"s":"")+' from the store…</span><span class="note">'+esc(missing.map(id=>shortName(modById(id)||{id:id})).join(", "))+'</span></div>'+bar(25,"ac")+
    '<p class="note" style="margin-top:8px">Questions are fetched one module at a time, so the page opens fast however big the bank gets.</p></div>';
  }
  let list=f.mod?(S.bank[f.mod]||[]):allQ();
  if(f.paper)list=list.filter(q=>{const m=modById(q.moduleId);return m&&String(m.paper)===f.paper});
  if(f.fmt==="free")list=list.filter(isFree);else if(f.fmt)list=list.filter(q=>q.format===f.fmt&&!isFree(q));
  if(f.src)list=list.filter(q=>q.source===f.src);
  if(f.st)list=list.filter(q=>f.st==="flag"?((S.att[q.id]||{}).f):statusOf(q.id)===f.st);
  const tot=S.index?Object.keys(S.index.modules||{}).reduce((s,k)=>s+S.index.modules[k].total,0):0;
  const counts={unseen:0,correct:0,wrong:0,flag:0};
  allQ().forEach(q=>{counts[statusOf(q.id)]++;if((S.att[q.id]||{}).f)counts.flag++});
  const sel=(id,cur,opts)=>'<select id="'+id+'">'+opts.map(o=>'<option value="'+esc(o[0])+'"'+(cur===o[0]?" selected":"")+'>'+esc(o[1])+'</option>').join("")+'</select>';
  return '<div class="hd"><h1>Question bank</h1><p>'+tot+' loaded · previous-year questions and their variants, side by side.</p>'+
    '<div class="sp row tight">'+(list.length?'<button class="btn p sm" id="drillAll">Drill these '+list.length+'</button>':'')+'</div></div>'+
  '<div class="card flat" style="margin-bottom:12px"><div class="grid g4">'+
    '<div><label class="fl">Module</label><select id="fMod">'+
      '<option value=""'+(f.mod?"":" selected")+'>All modules</option>'+
      [2,1].map(p=>{const l=ms.filter(m=>m.paper===p);if(!l.length)return"";
        return '<optgroup label="Paper '+p+(p===2?" · Statistics":" · General paper")+'">'+
          l.map(m=>'<option value="'+m.id+'"'+(f.mod===m.id?" selected":"")+'>'+
            modNo(m.id)+" · "+esc(m.name)+" ("+loadedCount(m.id)+")"+'</option>').join("")+'</optgroup>'}).join("")+
      '</select></div>'+
    '<div><label class="fl">Format</label>'+sel("fFmt",f.fmt,[["","All formats"]].concat(FORDER.map(k=>[k,FMT[k].n+" · "+FMT[k].mix+"% of paper"])).concat([["free","Write-in · nothing to guess from"]]))+'</div>'+
    '<div><label class="fl">Source</label>'+sel("fSrc",f.src,[["","Everything"],["pyq","Previous year only"],["variant","Variants only"]])+'</div>'+
    '<div><label class="fl">My result</label>'+sel("fSt",f.st,[["","Any"],["unseen","Unseen ("+counts.unseen+")"],["wrong","Wrong ("+counts.wrong+")"],["correct","Correct ("+counts.correct+")"],["flag","Flagged ("+counts.flag+")"]])+'</div>'+
  '</div></div>'+
  (list.length?list.slice(0,220).map(qrow).join("")+(list.length>220?'<p class="note" style="text-align:center">Showing the first 220. Narrow the filters, or hit “Drill these” to walk the whole set.</p>':"")
    :'<div class="empty"><h3>Nothing matches</h3><p>'+(tot?"Loosen a filter.":"No questions in the store yet — the Content tab has the prompt that loads a module.")+'</p></div>');
}
function qrow(q){
  const st=statusOf(q.id),a=S.att[q.id]||{};
  const c={correct:"ok",wrong:"bad",unseen:"dim"}[st];
  const m=modById(q.moduleId);
  return '<button class="qrow" data-q="'+esc(q.id)+'">'+
    '<span class="chip '+c+'" style="flex:0 0 auto">'+(st==="correct"?"✓":st==="wrong"?"✗":"·")+'</span>'+
    '<span class="qs">'+esc(String(q.stem||"").replace(/\s+/g," "))+'</span>'+
    '<span class="qm"><span class="chip dim">'+esc(isFree(q)?"Write-in":(FMT[q.format]||{s:q.format}).s)+'</span>'+
      (q.source==="pyq"?'<span class="chip och">PYQ'+(q.year?" "+esc(String(q.year)):"")+'</span>':'<span class="chip ac">variant</span>')+
      (a.f?'<span class="chip mid">flag</span>':'')+
      (q.needsReview?'<span class="chip bad" title="The options did not survive extraction from the PDF \u2014 check them against the paper">options need repair</span>':'')+
      '<span class="note">'+esc(m?shortName(m):q.moduleId)+'</span></span>'+
  '</button>';
}

