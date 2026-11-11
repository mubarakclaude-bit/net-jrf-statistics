// The Progress screen, moved out of the core bundle (was src/55-progress.js, vProgress). It draws exactly what the
// built-in view drew, through ctx.app, and serves the built-in route #progress in the same place in the navigation bar.

function render(ctx) {
  const app = ctx.app, esc = ctx.esc;
  const { bar, pc, fmtPct, nTag, modNo, askBox } = app.ui, { FORDER, FMT, ERRT } = app.data;
  const errs = app.errors();

  const g=app.gate();if(g)return g;
  const o2=app.overall(2),o1=app.overall(1);
  const F=app.formatStats();
  const et={};errs.forEach(e=>et[e.type]=(et[e.type]||0)+1);
  const emax=Math.max(1,...Object.values(et));
  const loadedAny=app.bankLoaded();
  return '<div class="hd"><h1>Progress</h1><p>The diagnostic view: marks at stake against marks you can currently defend.</p>'+
    '<div class="sp"><button class="btn sm" id="loadAllBtn">Load every module</button></div></div>'+
  '<div class="grid g2" style="margin-bottom:12px">'+
    '<div class="card"><h3 style="margin-bottom:10px">Paper 2 · '+Math.round(o2.proj)+' of 200 projected</h3>'+
      o2.ms.map(x=>'<div style="margin-bottom:9px"><div class="kv"><span>'+esc(x.m.name)+' <span class="note">'+x.m.marks+'m</span></span><b>'+Math.round(x.proj)+'<span class="note"> / '+x.m.marks+'</span></b></div>'+
        bar(pc(x.proj,x.m.marks),x.st==="ok"?"ok":x.st==="bad"?"bad":x.st==="empty"?"dim":"mid",true)+'</div>').join("")+'</div>'+
    '<div class="card"><h3 style="margin-bottom:10px">Paper 1 · '+Math.round(o1.proj)+' of 100 projected</h3>'+
      o1.ms.map(x=>'<div style="margin-bottom:9px"><div class="kv"><span>'+esc(x.m.name)+' <span class="note">'+x.m.marks+'m</span></span><b>'+Math.round(x.proj)+'<span class="note"> / '+x.m.marks+'</span></b></div>'+
        bar(pc(x.proj,x.m.marks),x.st==="ok"?"ok":x.st==="bad"?"bad":x.st==="empty"?"dim":"mid",true)+'</div>').join("")+'</div>'+
  '</div>'+
  '<div class="grid g2" style="margin-bottom:12px">'+
    '<div class="card"><h3 style="margin-bottom:4px">Accuracy by question format</h3>'+
      '<p class="note" style="margin-bottom:10px">The June 2026 paper broke down 50 single-concept, 21 numerical, 19 multi-statement, 7 match, 3 order. Your score fell by <b>demand level</b>, not by topic — that is the thing to fix.</p>'+
      (loadedAny?FORDER.map(f=>{const b=F[f],base=FMT[f].base;
        const p=b.att?pc(b.cor,b.att):0;
        return '<div style="margin-bottom:10px"><div class="kv"><span>'+esc(FMT[f].n)+'</span><b>'+(b.att?p+"%":"—")+' <span class="note">now · June '+pc(base[0],base[1])+'%</span></b></div>'+
          bar(p,b.att?(p>=80?"ok":p>=60?"mid":"bad"):"dim",true)+
          '<div class="bar sm" style="margin-top:2px"><i class="och" style="width:'+pc(base[0],base[1])+'%;opacity:.5"></i></div>'+
          '<div class="note">'+b.cor+' of '+b.att+' answered here · '+base[0]+' of '+base[1]+' in the real paper</div></div>'}).join("")
        :'<p class="note">Hit “Load every module” to compute this across the whole bank.</p>')+'</div>'+
    '<div class="card"><h3 style="margin-bottom:4px">Error profile</h3><p class="note" style="margin-bottom:10px">'+errs.length+' logged. Most of your June misses were verification failures, not method failures — this table is how you prove that is changing.</p>'+
      (errs.length?ERRT.filter(e=>et[e[0]]).sort((a,b)=>et[b[0]]-et[a[0]]).map(e=>
        '<div style="margin-bottom:8px"><div class="kv"><span>'+esc(e[1])+'</span><b>'+et[e[0]]+'</b></div>'+bar(100*et[e[0]]/emax,"och",true)+'</div>').join("")+
        '<button class="btn sm" id="errClear" style="margin-top:6px">Clear the log</button>'
        :'<p class="note">Nothing logged yet. After a wrong answer in the bank, tag what actually went wrong — one tap.</p>')+
      (errs.length>=6?askBox("ask-err","Ask Claude what my errors have in common",
        "A UGC NET Statistics (JRF) candidate logged these errors while drilling. Counts by type: "+ERRT.filter(e=>et[e[0]]).map(e=>e[1]+" × "+et[e[0]]).join("; ")+
        ". Recent items: "+errs.slice(-18).map(e=>"["+e.fmt+"/"+e.type+"] "+e.stem).join(" | ")+
        "\n\nFind the pattern underneath these, not a restatement of the counts. Name the single habit that would remove the most of them, and give one concrete drill, five minutes long, to build that habit. Under 180 words, plain text.","complex"):"")+
    '</div>'+
  '</div>'+
  '<div class="card"><h3 style="margin-bottom:8px">Every module, one table</h3><div class="scroll"><table class="tbl"><thead><tr>'+
    '<th>Module</th><th>P</th><th>Marks</th><th>June</th><th>Bank</th><th>Answered</th><th>Accuracy</th><th>Mock</th><th>Projected</th><th>Status</th></tr></thead><tbody>'+
    o2.ms.concat(o1.ms).map(x=>'<tr><td>'+nTag(modNo(x.m.id))+esc(x.m.name)+'</td><td class="num">'+x.m.paper+'</td><td class="num">'+x.m.marks+'</td>'+
      '<td class="mono">'+esc(x.m.baseline)+'</td><td class="num">'+x.loaded+' / '+x.target+'</td><td class="num">'+x.att+'</td>'+
      '<td class="num">'+(x.att?fmtPct(x.acc):"—")+'</td><td class="num">'+(x.mock===null?"—":x.mock+"%")+'</td>'+
      '<td class="num">'+Math.round(x.proj)+'</td>'+
      '<td><span class="chip '+({ok:"ok",mid:"mid",bad:"bad",new:"ac",empty:"dim"}[x.st])+'">'+({ok:"green",mid:"working",bad:"weak",new:"untouched",empty:"empty"}[x.st])+'</span></td></tr>').join("")+
    '</tbody></table></div></div>';
}

function wire(ctx, el) {
  const app = ctx.app;
  const la = el.querySelector("#loadAllBtn");
  if (la) la.onclick = async () => {
    la.disabled = true;
    await app.loadAll((i, n) => { la.textContent = "Loading " + i + "/" + n; });
    la.textContent = "Loaded"; ctx.rerender();
  };
  const ec = el.querySelector("#errClear");
  if (ec) ec.onclick = () => {
    if (ec.dataset.c) { app.clearErrors(); ctx.rerender(); }
    else { ec.dataset.c = "1"; ec.textContent = "Press again to clear " + app.errors().length; }
  };
}

return { render, wire };
