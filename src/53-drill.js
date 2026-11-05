/* ---------- drill ---------- */
function startDrill(list,i){
  if(!list.length){toast("No questions in that set yet");return}
  S.drill={list:list,i:i||0,pick:null,verd:{},wrote:false,checked:false,matched:false,shown:false,self:null,free:"",err:null};
  S.route="bank";location.hash="bank";render();window.scrollTo(0,0);
}
function drillHTML(){
  const D=S.drill,q=D.list[D.i];
  if(!q)return '<div class="empty"><h3>Set finished</h3><button class="btn p" data-exit="1">Back to the bank</button></div>';
  const m=modById(q.moduleId),F=FMT[q.format]||FMT.single;
  const a=S.att[q.id]||{};
  const free=isFree(q);
  const total=D.list.length;
  const done=D.list.filter(x=>(S.att[x.id]||{}).n).length;
  let gated=false,gateMsg="";
  if(q.format==="multi"){const n=Object.keys(D.verd).length;gated=n<(q.statements||[]).length;gateMsg="Give every statement a verdict first — "+n+" of "+(q.statements||[]).length+" done."}
  if(q.format==="numeric"){gated=!(D.wrote&&D.checked);gateMsg="Work it on paper, then confirm both boxes."}
  if(q.format==="match"||q.format==="order"){gated=!D.matched;gateMsg="Do the matching yourself before the options."}
  const opts=free?"":(q.options||[]).map((o,k)=>{
    const L=String.fromCharCode(65+k);
    let cls="";
    if(D.shown){if(L===q.answer)cls=" right";else if(L===D.pick)cls=" wrong"}
    return '<button class="opt'+cls+'" data-opt="'+L+'" aria-pressed="'+(D.pick===L)+'"'+(D.shown?" disabled":"")+'><span class="ol">'+L+'</span><span>'+richText(o)+'</span></button>'}).join("");
  const stmts=(q.statements||[]).map((s,k)=>{
    const L=String.fromCharCode(65+k),v=D.verd[L];
    return '<div class="stmt'+(v==="T"?" v-t":v==="F"?" v-f":"")+'"><span class="sl">'+L+'</span><span class="sb">'+esc(s)+'</span>'+
      '<span class="sv"><button class="vb t" data-v="'+L+'|T" aria-pressed="'+(v==="T")+'"'+(D.shown?" disabled":"")+'>T</button>'+
      '<button class="vb f" data-v="'+L+'|F" aria-pressed="'+(v==="F")+'"'+(D.shown?" disabled":"")+'>F</button></span></div>'}).join("");
  const pairs=(q.pairs||[]).length?'<div class="scroll"><table class="tbl"><thead><tr><th>List I</th><th>List II</th></tr></thead><tbody>'+
    q.pairs.map(p=>'<tr><td>'+esc(p[0]!=null?p[0]:p.i)+'</td><td>'+esc(p[1]!=null?p[1]:p.ii)+'</td></tr>').join("")+'</tbody></table></div>':"";
  const seq=(q.items||[]).length?'<div class="row tight" style="margin-bottom:10px">'+q.items.map((it,k)=>'<span class="chip dim">'+String.fromCharCode(65+k)+'. '+esc(it)+'</span>').join("")+'</div>':"";
  let verd="";
  if(D.shown&&q.verdicts){
    verd='<div class="vlist">'+Object.keys(q.verdicts).sort().map(L=>{const v=q.verdicts[L];
      const got=D.verd[L],tf=(v.tf===true||v.tf==="T")?"T":"F";
      return '<div class="vitem"><b>'+L+'</b><span class="tf '+tf+'">'+tf+'</span><span>'+esc(v.why||"")+
        (got&&got!==tf?' <b style="color:var(--bad)">— you said '+got+'</b>':got===tf?' <b style="color:var(--ok)">✓</b>':"")+'</span></div>'}).join("")+'</div>';
  }
  const ok=D.shown&&(free?D.self===true:D.pick===q.answer);
  const wrong=D.shown&&(free?D.self===false:D.pick!==q.answer);
  const writeIn=free?'<label class="fl">Your answer — write it down before you look at the solution</label>'+
    '<textarea id="freeAns" placeholder="θ̂ = … , and the quantity asked is …" style="min-height:76px"'+(D.shown?" readonly":"")+'>'+esc(D.free||"")+'</textarea>':"";
  return '<div class="hd"><button class="btn sm" data-exit="1">‹ Bank</button>'+
    '<p>'+esc(m?m.name:q.moduleId)+' · '+esc(F.n)+(q.source==="pyq"?" · previous year"+(q.year?" "+esc(String(q.year)):""):"")+(q.pno?" · Q"+esc(String(q.pno)):"")+'</p>'+
    '<div class="sp row tight"><span class="chip dim num">'+(D.i+1)+' / '+total+'</span>'+
      '<button class="btn sm" data-flag="'+esc(q.id)+'">'+(a.f?"★ flagged":"☆ flag")+'</button></div></div>'+
  '<div class="card flat" style="margin-bottom:10px"><div class="kv"><span class="lbl">this set</span><b>'+done+' / '+total+' answered</b></div>'+bar(pc(done,total),"ac",true)+'</div>'+
  '<div class="card">'+
    '<p class="note" style="margin-bottom:8px">'+esc(F.hint)+'</p>'+
    '<div class="stem">'+richText(q.stem)+'</div>'+
    (q.needsReview?'<div class="expl bad"><h4>Options need repair</h4>'+esc(q.reviewNote||'')+'</div>':"")+
    pairs+seq+
    (stmts?'<div style="margin-bottom:12px">'+stmts+'</div>':"")+
    (q.format==="numeric"?'<div class="row tight" style="margin:0 0 12px">'+
      '<button class="tog" data-w="1" aria-pressed="'+D.wrote+'"'+(D.shown?" disabled":"")+'>I wrote the working out</button>'+
      '<button class="tog" data-c="1" aria-pressed="'+D.checked+'"'+(D.shown?" disabled":"")+'>I checked which quantity was asked</button></div>':"")+
    ((q.format==="match"||q.format==="order")?'<div class="row tight" style="margin:0 0 12px">'+
      '<button class="tog" data-mt="1" aria-pressed="'+D.matched+'"'+(D.shown?" disabled":"")+'>I worked out '+(q.format==="order"?"the order":"every row")+' myself</button></div>':"")+
    '<div'+(gated&&!D.shown?' class="locked"':"")+'>'+(free?writeIn:opts)+'</div>'+
    (gated&&!D.shown?'<p class="note" style="color:var(--ochre)">'+esc(gateMsg)+'</p>':"")+
    '<div class="row" style="margin-top:12px">'+
      '<button class="btn sm gh" data-askopen="1" title="Ask Claude about a term in this question">✦ Ask Claude</button>'+
      (D.shown?'':'<button class="btn p" id="reveal"'+((gated||(!free&&!D.pick))?" disabled":"")+'>'+(free?"Reveal the answer":"Check answer")+'</button>')+
      (D.shown&&!free?'<span class="chip '+(ok?"ok":"bad")+'">'+(ok?"correct":"wrong — answer "+esc(q.answer))+'</span>':"")+
      (D.shown&&free&&D.self==null?'<span class="chip och">mark yourself</span><button class="btn g sm" data-self="1">I had this</button><button class="btn sm" data-self="0">I missed it</button>':"")+
      (D.shown&&free&&D.self!=null?'<span class="chip '+(ok?"ok":"bad")+'">'+(ok?"you marked it right":"you marked it wrong")+'</span>':"")+
      '<span class="sp"></span>'+
      (D.i>0?'<button class="btn sm" data-nav="-1">‹ prev</button>':"")+
      (D.i<total-1?'<button class="btn sm" data-nav="1">next ›</button>':'<button class="btn sm" data-exit="1">finish</button>')+
    '</div>'+
    (D.shown?
      (q.check?'<div class="expl och"><h4>Check your arithmetic</h4>'+richText(q.check)+'</div>':"")+
      '<div class="expl'+(ok?" ok":"")+'"><h4>'+(free?"Answer":"Why "+esc(q.answer))+'</h4>'+
        (free?'<b>'+esc(q.answer)+'</b><br>':"")+esc(q.explanation||"No explanation loaded for this question yet.")+'</div>'+verd+
      (wrong?'<div style="margin-top:10px"><div class="lbl" style="margin-bottom:5px">Log what went wrong — this builds your error profile</div><div class="row tight">'+
        ERRT.map(e=>'<button class="tog" data-err="'+e[0]+'" aria-pressed="'+(D.err===e[0])+'" title="'+esc(e[1])+'">'+esc(e[1])+'</button>').join("")+'</div></div>':"")+
      askBox("ask-q","Explain it another way",
        "A UGC NET Statistics (JRF) candidate got this question "+(ok?"right but wants it firmer":"wrong")+". Question: "+String(q.stem)+
        ((q.statements||[]).length?"\nStatements: "+q.statements.map((s,k)=>String.fromCharCode(65+k)+") "+s).join(" "):"")+
        (free?"":"\nOptions: "+(q.options||[]).map((o,k)=>String.fromCharCode(65+k)+") "+o).join(" "))+
        "\nCorrect answer: "+q.answer+(!free&&D.pick?"\nThey chose: "+D.pick:"")+(free&&D.free?"\nThey wrote: "+D.free:"")+
        "\n\nExplain it a second way, different from a textbook proof: give the intuition in two sentences, then the one line of algebra or the one counterexample that settles it, then the single thing to remember so this never costs a mark again. Under 150 words, plain text.","default")+
      askBox("ask-q2","Give me three more like this",
        "Write three fresh questions at UGC NET Statistics (JRF) level on exactly the concept this question tests, in the same format ("+(free?"numerical, write-in answer, no options":(FMT[q.format]||FMT.single).n)+"). Source question: "+String(q.stem)+" (answer "+q.answer+"). For each new question give the stem, "+(free?"the answer, and the one verification that catches the usual slip":"four options labelled A-D, the correct letter, and one line of why")+". Vary the distribution or the parameter so they are not restatements. Plain text.","complex")
      :"")+
  '</div>';
}

