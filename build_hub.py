#!/usr/bin/env python3
"""Generate the Point Estimation Drill artifact page."""
import json

bank   = json.load(open('/home/claude/w1/bank.json', encoding='utf-8'))
tables = json.load(open('/home/claude/w1/tables.json', encoding='utf-8'))

CARRY = [
    ["Sufficient", "the conditional distribution of the sample given T is free of θ"],
    ["Minimal sufficient", "a function of every other sufficient statistic"],
    ["Complete", "E[g(T)] = 0 for all θ forces g ≡ 0"],
    ["Ancillary", "distribution free of θ"],
    ["Factorisation", "f(x;θ) = g(T;θ)·h(x), h free of θ including its support"],
    ["Rao–Blackwell needs", "sufficiency → unbiased, variance no larger"],
    ["Lehmann–Scheffé needs", "sufficiency AND completeness → unique UMVUE"],
    ["Basu", "complete sufficient ⫫ ancillary"],
    ["MLE holds", "function of sufficient statistic, invariant, consistent, asymptotically normal and efficient"],
    ["MLE fails", "unbiasedness, uniqueness, existence"],
    ["The three corrections", "σ²: n−1 · exponential rate: n−1 · uniform: n+1"],
    ["CRLB", "Var(T) ≥ [τ′(θ)]²/(nI(θ)), I(θ) = −E[∂²/∂θ² log f], I_n = nI"],
    ["CRLB attained", "⟹ UMVUE. Not attained does NOT mean not UMVUE"],
    ["CRLB fails", "whenever the support depends on θ"],
    ["The counterexample", "U(θ, θ+1): sufficient, not complete — the range is ancillary with mean (n−1)/(n+1)"],
    ["Outlaws", "uniform and Cauchy — not exponential family, no CRLB"],
    ["Convex cups upward", "E[g(X)] ≥ g(EX); 1/x, x², eˣ convex, log and √ concave"],
    ["Double it, double the df", "2θΣX ~ χ²₂ₙ"],
    ["Rank over n plus one", "E(X₍ᵣ₎) = r/(n+1) for the uniform"],
]

ERROR_TYPES = [
    "Reported the wrong quantity",
    "Squared or rooted wrongly",
    "Missed a term",
    "Degrees of freedom",
    "Sign",
    "Pure recall gap",
    "Missed a condition",
    "Ran out of time",
]

DATA = dict(bank=bank, master=tables['master'], fisher=tables['fisher'],
            carry=CARRY, errorTypes=ERROR_TYPES)
payload = json.dumps(DATA, ensure_ascii=False).replace('</', '<\\/')

HTML = r'''<title>Point Estimation Drill</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: one column, max 940px; sticky tab rail; question cards; diagrams inside the column */
:root{
  --paper:#f6f7f9; --card:#ffffff; --ink:#14181e; --muted:#5a646f; --line:#dce2ea;
  --accent:#2f4b8f; --accent-soft:#e9edf7; --ok:#1d7a4d; --bad:#a93226; --warn:#9a6511;
  --ok-soft:#e6f3ec; --bad-soft:#fae9e7; --warn-soft:#fbf1e0;
  --serif:"IBM Plex Serif",Georgia,serif;
  --sans:"IBM Plex Sans",system-ui,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#11141a; --card:#191e26; --ink:#e6eaf1; --muted:#98a3b0; --line:#2a313b;
  --accent:#8ea8e6; --accent-soft:#1e2636; --ok:#5ec48f; --bad:#e5867e; --warn:#d9a85c;
  --ok-soft:#16281f; --bad-soft:#2c1b19; --warn-soft:#2a2216; color-scheme:dark;}}
:root[data-theme="dark"]{
  --paper:#11141a; --card:#191e26; --ink:#e6eaf1; --muted:#98a3b0; --line:#2a313b;
  --accent:#8ea8e6; --accent-soft:#1e2636; --ok:#5ec48f; --bad:#e5867e; --warn:#d9a85c;
  --ok-soft:#16281f; --bad-soft:#2c1b19; --warn-soft:#2a2216; color-scheme:dark;}

body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.5;}
.wrap{max-width:940px;margin:0 auto;padding-inline:16px;padding-block:0 48px;}
h1,h2,h3{font-family:var(--serif);text-wrap:balance;margin:0;}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums;}

header.top{padding-block:22px 14px;border-bottom:1px solid var(--line);}
header.top h1{font-size:1.5rem;font-weight:600;letter-spacing:-.01em;}
header.top p{margin:4px 0 0;color:var(--muted);font-size:.86rem;}

nav.tabs{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--paper);
  display:flex;gap:4px;overflow-x:auto;padding-block:8px;border-bottom:1px solid var(--line);margin-bottom:20px;}
nav.tabs button{flex:0 0 auto;font:500 .82rem/1 var(--sans);letter-spacing:.02em;color:var(--muted);
  background:none;border:1px solid transparent;border-radius:999px;padding:8px 13px;cursor:pointer;}
nav.tabs button:hover{color:var(--ink);}
nav.tabs button[aria-selected="true"]{background:var(--accent-soft);color:var(--accent);border-color:var(--line);}
nav.tabs button:focus-visible,.btn:focus-visible,.cell:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}

.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px;margin-bottom:14px;}
.lede{color:var(--muted);font-size:.9rem;margin-bottom:14px;}
.btn{font:500 .84rem var(--sans);border:1px solid var(--line);background:var(--card);color:var(--ink);
  border-radius:7px;padding:8px 13px;cursor:pointer;}
.btn:hover{border-color:var(--accent);}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff;}
.btn.primary:hover{opacity:.9;}
.btn[disabled]{opacity:.42;cursor:not-allowed;}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;}
.spread{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;justify-content:space-between;}
.eyebrow{font:600 .7rem/1 var(--sans);letter-spacing:.09em;text-transform:uppercase;color:var(--muted);}
.stat{font-family:var(--mono);font-variant-numeric:tabular-nums;}

/* question card */
.qstem{font-size:1.02rem;margin-bottom:12px;}
.sts{display:grid;gap:8px;margin-bottom:14px;}
.st{display:grid;grid-template-columns:22px 1fr auto;gap:10px;align-items:start;
  border:1px solid var(--line);border-radius:8px;padding:10px 11px;min-width:0;}
.st .lab{font-family:var(--mono);font-weight:500;color:var(--accent);}
.st .txt{min-width:0;font-size:.94rem;}
.tf{display:flex;gap:5px;}
.tf button{font:500 .74rem var(--sans);border:1px solid var(--line);background:var(--card);
  color:var(--muted);border-radius:6px;padding:5px 9px;cursor:pointer;}
.tf button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff;}
.st.right{border-color:var(--ok);background:var(--ok-soft);}
.st.wrong{border-color:var(--bad);background:var(--bad-soft);}
.why{grid-column:2/-1;font-size:.85rem;color:var(--muted);margin-top:2px;}
.opts{display:grid;gap:7px;}
.opt{text-align:left;font:400 .93rem/1.45 var(--sans);border:1px solid var(--line);background:var(--card);
  color:var(--ink);border-radius:8px;padding:10px 12px;cursor:pointer;min-width:0;}
.opt:hover{border-color:var(--accent);}
.opt .k{font-family:var(--mono);font-weight:500;color:var(--accent);margin-right:8px;}
.opt.correct{border-color:var(--ok);background:var(--ok-soft);}
.opt.chosen-wrong{border-color:var(--bad);background:var(--bad-soft);}
.gate{font-size:.85rem;color:var(--warn);background:var(--warn-soft);border:1px solid var(--line);
  border-radius:8px;padding:9px 11px;margin-bottom:12px;}
.ans{border-top:1px solid var(--line);margin-top:14px;padding-top:12px;font-size:.93rem;}
.ans .val{font-family:var(--mono);font-weight:500;font-size:1.05rem;color:var(--accent);}
.chk{background:var(--warn-soft);border-left:3px solid var(--warn);padding:8px 11px;border-radius:0 7px 7px 0;
  margin-top:10px;font-size:.88rem;}
.pill{display:inline-block;font:500 .7rem/1 var(--sans);letter-spacing:.04em;padding:5px 9px;
  border-radius:999px;background:var(--accent-soft);color:var(--accent);}

/* tables */
.tblwrap{overflow-x:auto;}
table{border-collapse:collapse;width:100%;font-size:.86rem;}
th{text-align:left;font:600 .72rem/1 var(--sans);letter-spacing:.06em;text-transform:uppercase;
  color:var(--muted);padding:9px 10px;border-bottom:1px solid var(--line);white-space:nowrap;}
td{padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top;}
td.dist{font-weight:500;}
.cell{font-family:var(--mono);font-size:.84rem;background:var(--accent-soft);color:transparent;
  border:1px dashed var(--line);border-radius:5px;padding:4px 9px;cursor:pointer;min-width:62px;display:inline-block;}
.cell.shown{background:none;color:var(--ink);border-color:transparent;border-style:solid;}

/* log */
.logitem{border:1px solid var(--line);border-radius:8px;padding:11px 12px;margin-bottom:8px;}
.logitem .meta{font-size:.76rem;color:var(--muted);display:flex;gap:10px;flex-wrap:wrap;margin-top:5px;}
.due{border-color:var(--warn);background:var(--warn-soft);}
input[type=text],select,textarea{font:400 .9rem var(--sans);color:var(--ink);background:var(--card);
  border:1px solid var(--line);border-radius:7px;padding:9px 10px;width:100%;min-width:0;}
label.fld{display:block;margin-bottom:10px;}
label.fld span{display:block;font:600 .72rem/1 var(--sans);letter-spacing:.06em;text-transform:uppercase;
  color:var(--muted);margin-bottom:5px;}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;}
.note{font-size:.84rem;color:var(--muted);}
svg{max-width:100%;height:auto;display:block;}
.pick{display:flex;gap:9px;align-items:flex-start;border:1px solid var(--line);border-radius:8px;
  padding:10px 12px;margin-bottom:7px;cursor:pointer;}
.pick input{margin-top:3px;flex:0 0 auto;}
.toast{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(18px + env(safe-area-inset-bottom,0px));
  background:var(--ink);color:var(--paper);font-size:.84rem;padding:10px 16px;border-radius:999px;z-index:20;}
input[type=range]{width:100%;accent-color:var(--accent);}
</style>

<div class="wrap">
  <header class="top">
    <h1>Point Estimation Drill</h1>
    <p>Week 1 · UGC NET Statistics (107) · the parts of the module that work better on a screen than on paper</p>
  </header>

  <nav class="tabs" role="tablist">
    <button role="tab" data-tab="multi" aria-selected="true">Multi-statement</button>
    <button role="tab" data-tab="numeric" aria-selected="false">Numerical</button>
    <button role="tab" data-tab="concept" aria-selected="false">Conceptual</button>
    <button role="tab" data-tab="recall" aria-selected="false">Recall</button>
    <button role="tab" data-tab="diagrams" aria-selected="false">Diagrams</button>
    <button role="tab" data-tab="log" aria-selected="false">Error log</button>
    <button role="tab" data-tab="offline" aria-selected="false">Take offline</button>
  </nav>

  <section id="p-multi"></section>
  <section id="p-numeric" hidden></section>
  <section id="p-concept" hidden></section>
  <section id="p-recall" hidden></section>
  <section id="p-diagrams" hidden></section>
  <section id="p-log" hidden></section>
  <section id="p-offline" hidden></section>
</div>

<script>
const D = __DATA__;
const $ = (s,r=document)=>r.querySelector(s);
const el = (t,c,h)=>{const e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e;};
const esc = s => String(s).replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]));
const LET = ['A','B','C','D'];
const today = () => new Date().toISOString().slice(0,10);

/* ---------- small persistent store: db when available, else localStorage ---------- */
let db=null, uid=null, store='local';
function lsGet(k,f){ try{ const v=localStorage.getItem(k); return v?JSON.parse(v):f; }catch(e){ return f; } }
function lsSet(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} }

const Log = {
  items: lsGet('pe.log',[]),
  async load(){
    if(!db) return;
    try{
      const snap = await db.collection('errors').orderBy('ts','desc').limit(200).get();
      this.items = snap.docs.map(d=>Object.assign({id:d.id}, d.data()));
    }catch(e){}
  },
  async add(it){
    it.id = 'e'+Date.now().toString(36);
    this.items.unshift(it);
    lsSet('pe.log', this.items.slice(0,200));
    if(db){ try{ await db.collection('errors').doc(it.id).set(it); }catch(e){} }
  },
  async mark(id, field){
    const it = this.items.find(x=>x.id===id); if(!it) return;
    it[field] = today();
    lsSet('pe.log', this.items.slice(0,200));
    if(db){ try{ await db.collection('errors').doc(id).update({[field]: it[field]}); }catch(e){} }
  },
  async remove(id){
    this.items = this.items.filter(x=>x.id!==id);
    lsSet('pe.log', this.items);
    if(db){ try{ await db.collection('errors').doc(id).delete(); }catch(e){} }
  }
};
const Drill = {
  v: lsGet('pe.drill',{}),
  bump(kind){ const d=today(); this.v[d]=this.v[d]||{multi:0,numeric:0,concept:0};
    this.v[d][kind]=(this.v[d][kind]||0)+1; lsSet('pe.drill',this.v); },
  todayCount(kind){ return (this.v[today()]||{})[kind]||0; }
};

/* ---------- tabs ---------- */
const PANELS = ['multi','numeric','concept','recall','diagrams','log','offline'];
function show(tab){
  PANELS.forEach(p=>{ $('#p-'+p).hidden = (p!==tab); });
  document.querySelectorAll('nav.tabs button').forEach(b=>b.setAttribute('aria-selected', String(b.dataset.tab===tab)));
  lsSet('pe.tab', tab);
  if(tab==='log') renderLog();
  if(tab==='diagrams') renderDiagrams();
  window.scrollTo({top:0,behavior:'instant'});
}
document.querySelectorAll('nav.tabs button').forEach(b=>b.onclick=()=>show(b.dataset.tab));

/* ---------- multi-statement ---------- */
let mIdx = 0, mVerdicts = {}, mDone = false, mScore = lsGet('pe.mscore',{n:0,opt:0,st:0});
function renderMulti(){
  const q = D.bank.multi[mIdx];
  const host = $('#p-multi'); host.innerHTML='';
  const head = el('div','spread');
  head.appendChild(el('div','', `<span class="eyebrow">${esc(q.day)}</span>
     <div class="note" style="margin-top:4px">Question ${q.n} of ${D.bank.multi.length} · five a day</div>`));
  head.appendChild(el('div','', `<span class="pill">today ${Drill.todayCount('multi')}/5</span>`));
  const card = el('div','card');
  card.appendChild(head);
  card.appendChild(el('div','qstem', esc(q.stem)));

  const wrapS = el('div','sts');
  q.sts.forEach((s,i)=>{
    const L = LET[i];
    const row = el('div','st'); row.dataset.l = L;
    row.appendChild(el('div','lab', L));
    row.appendChild(el('div','txt', esc(s)));
    const tf = el('div','tf');
    ['True','False'].forEach(w=>{
      const b = el('button',null,w);
      b.setAttribute('aria-pressed','false');
      b.onclick = ()=>{
        if(mDone) return;
        mVerdicts[L] = (w==='True');
        tf.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed', String(x.textContent===w)));
        maybeOpen();
      };
      tf.appendChild(b);
    });
    row.appendChild(tf);
    wrapS.appendChild(row);
  });
  card.appendChild(wrapS);

  const gate = el('div','gate','Judge all four statements before the options appear. That order is the whole point of the drill.');
  card.appendChild(gate);
  const optBox = el('div','opts'); optBox.hidden = true;
  q.opts.forEach((o,i)=>{
    const b = el('button','opt', `<span class="k">${LET[i]}</span>${esc(o)}`);
    b.onclick = ()=>pickMulti(LET[i]);
    optBox.appendChild(b);
  });
  card.appendChild(optBox);
  const ansBox = el('div','ans'); ansBox.hidden = true; ansBox.id='m-ans';
  card.appendChild(ansBox);

  const nav = el('div','row'); nav.style.marginTop='14px';
  const prev = el('button','btn','Previous'); prev.disabled = mIdx===0;
  prev.onclick = ()=>{ mIdx--; mVerdicts={}; mDone=false; renderMulti(); };
  const next = el('button','btn primary','Next question');
  next.onclick = ()=>{ mIdx=(mIdx+1)%D.bank.multi.length; mVerdicts={}; mDone=false; renderMulti(); };
  const logb = el('button','btn','Log an error');
  logb.onclick = ()=>{ prefillLog('Multi-statement Q'+q.n); show('log'); };
  nav.append(prev,next,logb);
  card.appendChild(nav);
  host.appendChild(card);

  const sc = el('div','card');
  sc.innerHTML = `<span class="eyebrow">Running accuracy</span>
    <div class="row" style="margin-top:8px;gap:20px">
      <div><div class="stat" style="font-size:1.35rem">${mScore.n?Math.round(100*mScore.opt/mScore.n):0}%</div>
           <div class="note">option correct · ${mScore.opt}/${mScore.n}</div></div>
      <div><div class="stat" style="font-size:1.35rem">${mScore.n?Math.round(100*mScore.st/(4*mScore.n)):0}%</div>
           <div class="note">statements judged right · ${mScore.st}/${4*mScore.n}</div></div>
    </div>
    <p class="note" style="margin-top:10px">The second number is the one that matters. In June you scored 11% on this
    format; getting the option right while misjudging two statements is a near miss, not a skill.</p>`;
  host.appendChild(sc);

  function maybeOpen(){
    if(Object.keys(mVerdicts).length===4){ gate.hidden=true; optBox.hidden=false; }
  }
}
function pickMulti(choice){
  if(mDone) return;
  mDone = true;
  const q = D.bank.multi[mIdx];
  const host = $('#p-multi');
  host.querySelectorAll('.opt').forEach((b,i)=>{
    if(LET[i]===q.ans) b.classList.add('correct');
    else if(LET[i]===choice) b.classList.add('chosen-wrong');
  });
  let right = 0;
  host.querySelectorAll('.st').forEach(row=>{
    const L = row.dataset.l, v = q.v[L];
    const mine = mVerdicts[L];
    const ok = (mine === v.tf);
    if(ok) right++;
    row.classList.add(ok?'right':'wrong');
    row.appendChild(el('div','why',
      `<strong>${v.tf?'True':'False'}</strong> — ${esc(v.why)}${ok?'':' · you said '+(mine?'true':'false')}`));
  });
  mScore = {n:mScore.n+1, opt:mScore.opt+(choice===q.ans?1:0), st:mScore.st+right};
  lsSet('pe.mscore', mScore);
  Drill.bump('multi');
  const a = $('#m-ans'); a.hidden=false;
  a.innerHTML = `Correct option <span class="val">(${q.ans})</span> — ${esc(q.opts[LET.indexOf(q.ans)])}.
    You judged <strong>${right} of 4</strong> statements correctly.`;
}

/* ---------- numerical ---------- */
let nIdx = 0, nWritten=false, nChecked=false;
function renderNum(){
  const q = D.bank.numerical[nIdx];
  const host = $('#p-numeric'); host.innerHTML='';
  const card = el('div','card');
  card.appendChild(el('div','spread',
    `<span class="eyebrow">Problem ${q.n} of ${D.bank.numerical.length}</span>
     <span class="pill">today ${Drill.todayCount('numeric')}</span>`));
  card.appendChild(el('div','qstem', esc(q.stem)));
  const gate = el('div','gate','Work it on paper first. The answer unlocks only after both boxes below are ticked — an unchecked answer is what produced 4/21 in June.');
  card.appendChild(gate);
  const row = el('div','row');
  const b1 = el('button','btn','① I wrote my answer');
  const b2 = el('button','btn','② I ran the check');
  const reveal = el('button','btn primary','Reveal'); reveal.disabled = true;
  b1.onclick = ()=>{ nWritten=!nWritten; b1.classList.toggle('primary',nWritten); gateCheck(); };
  b2.onclick = ()=>{ nChecked=!nChecked; b2.classList.toggle('primary',nChecked); gateCheck(); };
  function gateCheck(){ reveal.disabled = !(nWritten && nChecked); }
  const ansBox = el('div','ans'); ansBox.hidden=true;
  reveal.onclick = ()=>{
    ansBox.hidden=false; gate.hidden=true;
    ansBox.innerHTML = `<div><span class="val">${esc(q.ans)}</span></div>` +
      (q.work?`<div style="margin-top:6px">${esc(q.work)}</div>`:'') +
      (q.check?`<div class="chk"><strong>Check</strong> — ${esc(q.check)}</div>`:'');
    Drill.bump('numeric');
  };
  row.append(b1,b2,reveal);
  card.appendChild(row);
  card.appendChild(ansBox);
  const nav = el('div','row'); nav.style.marginTop='14px';
  const prev = el('button','btn','Previous'); prev.disabled = nIdx===0;
  prev.onclick=()=>{ nIdx--; nWritten=nChecked=false; renderNum(); };
  const next = el('button','btn','Next problem');
  next.onclick=()=>{ nIdx=(nIdx+1)%D.bank.numerical.length; nWritten=nChecked=false; renderNum(); };
  const lg = el('button','btn','Log an error');
  lg.onclick=()=>{ prefillLog('Numerical Q'+q.n); show('log'); };
  nav.append(prev,next,lg);
  card.appendChild(nav);
  host.appendChild(card);
}

/* ---------- conceptual ---------- */
let cIdx = 0, cDone=false;
function renderConc(){
  const q = D.bank.conceptual[cIdx];
  const host = $('#p-concept'); host.innerHTML='';
  const card = el('div','card');
  card.appendChild(el('div','spread',
    `<span class="eyebrow">Question ${q.n} of ${D.bank.conceptual.length}</span>
     <span class="note">recognition — your strongest tier, so keep it short</span>`));
  card.appendChild(el('div','qstem', esc(q.stem)));
  const box = el('div','opts');
  q.opts.forEach((o,i)=>{
    const b = el('button','opt', `<span class="k">${LET[i]}</span>${esc(o)}`);
    b.onclick = ()=>{
      if(cDone) return; cDone = true;
      box.querySelectorAll('.opt').forEach((x,j)=>{
        if(LET[j]===q.ans) x.classList.add('correct');
        else if(j===i) x.classList.add('chosen-wrong');
      });
      ans.hidden=false; ans.innerHTML = esc(q.expl);
      Drill.bump('concept');
    };
    box.appendChild(b);
  });
  card.appendChild(box);
  const ans = el('div','ans'); ans.hidden=true; card.appendChild(ans);
  const nav = el('div','row'); nav.style.marginTop='14px';
  const next = el('button','btn primary','Next');
  next.onclick=()=>{ cIdx=(cIdx+1)%D.bank.conceptual.length; cDone=false; renderConc(); };
  const lg = el('button','btn','Log an error');
  lg.onclick=()=>{ prefillLog('Conceptual Q'+q.n); show('log'); };
  nav.append(next,lg);
  card.appendChild(nav);
  host.appendChild(card);
}

/* ---------- recall ---------- */
function renderRecall(){
  const host = $('#p-recall'); host.innerHTML='';
  const c1 = el('div','card');
  c1.innerHTML = `<div class="spread"><h2 style="font-size:1.1rem">The master table</h2>
    <button class="btn" id="revall">Reveal all</button></div>
    <p class="lede">Tap a cell to check yourself. Sunday's Part A is reproducing this on blank paper, so use this to find the gaps, not to read.</p>`;
  const tw = el('div','tblwrap');
  const tb = el('table');
  tb.innerHTML = '<thead><tr><th>Distribution</th><th>Complete sufficient statistic</th><th>MLE</th><th>UMVUE</th><th>Note</th></tr></thead>';
  const body = el('tbody');
  D.master.forEach(r=>{
    const tr = el('tr');
    tr.appendChild(el('td','dist', esc(r[0])));
    [1,2,3].forEach(i=>{
      const td = el('td');
      const b = el('button','cell', esc(r[i]||'—'));
      b.onclick = ()=>b.classList.toggle('shown');
      td.appendChild(b); tr.appendChild(td);
    });
    tr.appendChild(el('td','note', esc(r[4]||'')));
    body.appendChild(tr);
  });
  tb.appendChild(body); tw.appendChild(tb); c1.appendChild(tw);
  host.appendChild(c1);
  $('#revall').onclick = ()=>{
    const cells = host.querySelectorAll('.cell');
    const anyHidden = [...cells].some(c=>!c.classList.contains('shown'));
    cells.forEach(c=>c.classList.toggle('shown', anyHidden));
    $('#revall').textContent = anyHidden ? 'Hide all' : 'Reveal all';
  };

  const c2 = el('div','card');
  c2.innerHTML = `<h2 style="font-size:1.1rem">Fisher information</h2>`;
  const tw2 = el('div','tblwrap'); const t2 = el('table');
  t2.innerHTML = '<thead><tr><th>Distribution</th><th>I(θ)</th></tr></thead>';
  const b2 = el('tbody');
  D.fisher.forEach(r=>{
    const tr = el('tr');
    tr.appendChild(el('td','dist', esc(r[0])));
    const td = el('td'); const btn = el('button','cell', esc(r[1]));
    btn.onclick=()=>btn.classList.toggle('shown'); td.appendChild(btn); tr.appendChild(td);
    b2.appendChild(tr);
  });
  t2.appendChild(b2); tw2.appendChild(t2); c2.appendChild(tw2);
  host.appendChild(c2);

  const c3 = el('div','card');
  c3.innerHTML = `<h2 style="font-size:1.1rem">Carry sheet</h2>
    <p class="lede">The deciding line for each idea. Handwrite your own version — copying this one does not stick the same way.</p>`;
  const tw3 = el('div','tblwrap'); const t3 = el('table');
  const b3 = el('tbody');
  D.carry.forEach(r=>{
    const tr = el('tr');
    tr.appendChild(el('td','dist', esc(r[0])));
    const td = el('td'); const btn = el('button','cell', esc(r[1]));
    btn.style.whiteSpace='normal'; btn.style.textAlign='left';
    btn.onclick=()=>btn.classList.toggle('shown'); td.appendChild(btn); tr.appendChild(td);
    b3.appendChild(tr);
  });
  t3.appendChild(b3); tw3.appendChild(t3); c3.appendChild(tw3);
  host.appendChild(c3);
}

/* ---------- diagrams ---------- */
function renderDiagrams(){
  const host = $('#p-diagrams');
  if(host.dataset.built) { drawFisher(); return; }
  host.dataset.built = '1';
  host.innerHTML = `
  <div class="card">
    <h2 style="font-size:1.1rem">How the week fits together</h2>
    <p class="lede">Every theorem in week 1 exists to feed the one to its right. Read it once and the section order stops being arbitrary.</p>
    <div class="tblwrap">${CONCEPT_SVG}</div>
  </div>
  <div class="card">
    <h2 style="font-size:1.1rem">Finding a UMVUE — the algorithm</h2>
    <p class="lede">Run this under time pressure instead of recalling the theory.</p>
    <div class="tblwrap">${FLOW_SVG}</div>
  </div>
  <div class="card">
    <h2 style="font-size:1.1rem">Why the uniform MLE sits on a boundary</h2>
    <p class="lede">The likelihood for U(0, θ): zero below the sample maximum, then falling as 1/θⁿ. Nothing to differentiate — the maximum is at the left edge.</p>
    <div class="tblwrap">${UNIF_SVG}</div>
  </div>
  <div class="card">
    <h2 style="font-size:1.1rem">Fisher information for a proportion</h2>
    <p class="lede">I(p) = 1/[p(1−p)]. Information explodes near 0 and 1 and is smallest at p = 0.5 — which is why extreme proportions are the easiest to estimate and p near a half the hardest.</p>
    <div class="tblwrap"><svg id="fsvg" viewBox="0 0 640 300" role="img" aria-label="Fisher information curve"></svg></div>
    <label class="fld" style="margin-top:10px"><span>p = <span class="stat" id="plab">0.25</span></span>
      <input type="range" id="pslider" min="2" max="98" value="25"></label>
    <p class="note" id="fnote"></p>
  </div>`;
  $('#pslider').oninput = drawFisher;
  drawFisher();
}
function drawFisher(){
  const sl = $('#pslider'); if(!sl) return;
  const p = (+sl.value)/100;
  const W=640,H=300,L=56,R=20,T=18,B=42;
  const xs = v => L + v*(W-L-R);
  const maxI = 40;
  const ys = v => H-B - Math.min(v,maxI)/maxI*(H-T-B);
  let path='';
  for(let i=1;i<=199;i++){ const v=i/200, I=1/(v*(1-v)); if(I>maxI) continue;
    path += (path?'L':'M')+xs(v).toFixed(1)+' '+ys(I).toFixed(1); }
  const I = 1/(p*(1-p));
  const ticks=[0,0.25,0.5,0.75,1].map(v=>`<line x1="${xs(v)}" y1="${H-B}" x2="${xs(v)}" y2="${H-B+5}" stroke="var(--line)"/>
     <text x="${xs(v)}" y="${H-B+20}" text-anchor="middle" font-size="11" fill="var(--muted)" font-family="var(--mono)">${v}</text>`).join('');
  const yt=[4,10,20,40].map(v=>`<line x1="${L-5}" y1="${ys(v)}" x2="${W-R}" y2="${ys(v)}" stroke="var(--line)" stroke-dasharray="2 4"/>
     <text x="${L-9}" y="${ys(v)+4}" text-anchor="end" font-size="11" fill="var(--muted)" font-family="var(--mono)">${v}</text>`).join('');
  $('#fsvg').innerHTML = `${yt}
    <line x1="${L}" y1="${T}" x2="${L}" y2="${H-B}" stroke="var(--line)"/>
    <line x1="${L}" y1="${H-B}" x2="${W-R}" y2="${H-B}" stroke="var(--line)"/>
    ${ticks}
    <path d="${path}" fill="none" stroke="var(--accent)" stroke-width="2.2"/>
    <line x1="${xs(p)}" y1="${T}" x2="${xs(p)}" y2="${H-B}" stroke="var(--warn)" stroke-dasharray="4 3"/>
    <circle cx="${xs(p)}" cy="${ys(I)}" r="5" fill="var(--warn)"/>
    <text x="${W-R}" y="${T+12}" text-anchor="end" font-size="12" fill="var(--muted)" font-family="var(--mono)">I(p)</text>
    <text x="${(L+W-R)/2}" y="${H-6}" text-anchor="middle" font-size="11" fill="var(--muted)">p</text>`;
  $('#plab').textContent = p.toFixed(2);
  $('#fnote').innerHTML = `At p = ${p.toFixed(2)}: I(p) = <span class="stat">${I.toFixed(2)}</span>. ` +
    `With n = 20 the Cramér–Rao bound for unbiased estimators of p is p(1−p)/n = <span class="stat">${(p*(1-p)/20).toFixed(5)}</span>, ` +
    `and Var(X̄) equals it exactly — so X̄ is efficient at every p.`;
}

/* ---------- error log ---------- */
let logPrefill = '';
function prefillLog(ref){ logPrefill = ref; }
function dueState(it){
  const days = d => Math.floor((Date.now()-Date.parse(d))/86400000);
  if(!it.r1 && days(it.ts) >= 7) return 'first repair due';
  if(it.r1 && !it.r2 && days(it.ts) >= 14) return 'second repair due';
  return '';
}
function renderLog(){
  const host = $('#p-log'); host.innerHTML='';
  const form = el('div','card');
  form.innerHTML = `<h2 style="font-size:1.1rem">Log an error</h2>
    <p class="lede">Record the <em>type</em>, not the question. ${store==='db'
      ? 'Saved to this artifact, so it follows you between phone and laptop.'
      : 'Saved in this browser only — sign in to sync across devices.'}</p>
    <div class="grid2">
      <label class="fld"><span>Type</span><select id="etype">${D.errorTypes.map(t=>`<option>${esc(t)}</option>`).join('')}</select></label>
      <label class="fld"><span>Question</span><input type="text" id="eref" value="${esc(logPrefill)}" placeholder="Multi-statement Q14"></label>
    </div>
    <label class="fld"><span>The fix, in one line</span><input type="text" id="efix" placeholder="Rao–Blackwell keeps the estimand — read E(h) first"></label>
    <button class="btn primary" id="esave">Save entry</button>`;
  host.appendChild(form);
  $('#esave').onclick = async ()=>{
    const fix = $('#efix').value.trim();
    if(!fix){ $('#efix').focus(); return; }
    await Log.add({type:$('#etype').value, ref:$('#eref').value.trim(), fix, ts:new Date().toISOString(), r1:'', r2:''});
    logPrefill=''; toast('Entry saved'); renderLog();
  };

  const counts = {};
  Log.items.forEach(i=>counts[i.type]=(counts[i.type]||0)+1);
  const top = Object.entries(counts).sort((a,b)=>b[1]-a[1]);
  const sum = el('div','card');
  sum.innerHTML = `<h2 style="font-size:1.1rem">By type</h2>` + (top.length
    ? `<div class="tblwrap"><table><tbody>${top.map(([t,c])=>
        `<tr><td class="dist">${esc(t)}</td><td class="stat" style="text-align:right">${c}</td>
         <td class="note">${c>=3?'three or more — this is next week\'s first target':''}</td></tr>`).join('')}</tbody></table></div>`
    : `<p class="note">Nothing logged yet. The log is the part of the plan that decides what you study next, so it only works if you feed it.</p>`);
  host.appendChild(sum);

  const due = Log.items.filter(i=>dueState(i));
  const dueCard = el('div','card');
  dueCard.innerHTML = `<h2 style="font-size:1.1rem">Spaced repair queue</h2>
    <p class="lede">Every error gets redone twice — once after a week, once a fortnight on. From blank paper, never by rereading the fix.</p>`;
  if(!due.length) dueCard.appendChild(el('p','note','Nothing due. Entries appear here seven days after you log them.'));
  due.forEach(it=>{
    const d = el('div','logitem due');
    d.innerHTML = `<strong>${esc(it.type)}</strong>${it.ref?' · '+esc(it.ref):''}
      <div style="margin-top:5px">${esc(it.fix)}</div>
      <div class="meta"><span>${esc(dueState(it))}</span><span>logged ${esc((it.ts||'').slice(0,10))}</span></div>`;
    const b = el('button','btn','Redone from blank paper');
    b.style.marginTop='9px';
    b.onclick = async ()=>{ await Log.mark(it.id, it.r1?'r2':'r1'); renderLog(); };
    d.appendChild(b);
    dueCard.appendChild(d);
  });
  host.appendChild(dueCard);

  const all = el('div','card');
  all.innerHTML = `<h2 style="font-size:1.1rem">All entries</h2>`;
  if(!Log.items.length) all.appendChild(el('p','note','Empty.'));
  Log.items.forEach(it=>{
    const d = el('div','logitem');
    d.innerHTML = `<strong>${esc(it.type)}</strong>${it.ref?' · '+esc(it.ref):''}
      <div style="margin-top:5px">${esc(it.fix)}</div>
      <div class="meta"><span>logged ${esc((it.ts||'').slice(0,10))}</span>
        <span>${it.r1?'repaired '+esc(it.r1):'not yet repaired'}</span>
        <span>${it.r2?'second repair '+esc(it.r2):''}</span></div>`;
    const x = el('button','btn','Delete'); x.style.marginTop='9px';
    x.onclick = async ()=>{ await Log.remove(it.id); renderLog(); };
    d.appendChild(x);
    all.appendChild(d);
  });
  host.appendChild(all);
}
function toast(msg){
  const t = el('div','toast', esc(msg)); document.body.appendChild(t);
  setTimeout(()=>t.remove(), 2200);
}

/* ---------- take offline ---------- */
const SECTIONS = [
  ['master','The master table'],
  ['fisher','Fisher information table'],
  ['carry','Carry sheet'],
  ['multi','Multi-statement set — 35 questions with per-statement verdicts'],
  ['numeric','Numerical set — 25 problems with answers and checks'],
  ['concept','Conceptual set — 40 questions'],
  ['log','Your error log'],
];
function renderOffline(){
  const host = $('#p-offline'); host.innerHTML='';
  const c = el('div','card');
  c.innerHTML = `<h2 style="font-size:1.1rem">Take selected parts offline</h2>
    <p class="lede">Tick what you need, download one HTML file, and print it from your own browser. Printing is blocked inside this frame, so the file is the way out.</p>`;
  SECTIONS.forEach(([k,label])=>{
    const l = el('label','pick');
    l.innerHTML = `<input type="checkbox" value="${k}" checked><span>${esc(label)}</span>`;
    c.appendChild(l);
  });
  const row = el('div','row'); row.style.marginTop='12px';
  const dl = el('button','btn primary','Download HTML');
  dl.onclick = ()=>doDownload('html');
  const anki = el('button','btn','Download Anki CSV');
  anki.onclick = ()=>doDownload('csv');
  row.append(dl,anki);
  c.appendChild(row);
  c.appendChild(el('p','note','The CSV holds the carry sheet and the master table as question-and-answer pairs — import it into Anki for the spaced-recall half.'));
  host.appendChild(c);
}
function selected(){ return [...$('#p-offline').querySelectorAll('input:checked')].map(i=>i.value); }
function buildHTML(keys){
  const css = `body{font:12pt/1.35 "IBM Plex Sans",system-ui,sans-serif;color:#15181d;max-width:960px;margin:0 auto;padding:18px;}
  h1{font-size:19pt}h2{font-size:14pt;border-bottom:2px solid #0f2a4a;padding-bottom:4px;margin-top:26px}
  table{border-collapse:collapse;width:100%;font-size:10pt;margin:8px 0}
  th{background:#e7eef6;text-align:left;padding:5px 7px;border:.5pt solid #b6c4d4}
  td{padding:4px 7px;border:.5pt solid #ccd6e2;vertical-align:top}
  .q{margin:10px 0;page-break-inside:avoid}.a{color:#19456f}
  @media print{@page{size:A4;margin:14mm}body{padding:0}}`;
  let h = `<!doctype html><html><head><meta charset="utf-8"><title>Week 1 — selected</title><style>${css}</style></head><body>`;
  h += `<h1>Week 1 — Point estimation</h1><p>Selected sections · UGC NET Statistics (107)</p>`;
  const tbl = (head, rows) => `<table><thead><tr>${head.map(x=>`<th>${esc(x)}</th>`).join('')}</tr></thead><tbody>${
    rows.map(r=>`<tr>${r.map(c=>`<td>${esc(c??'')}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
  if(keys.includes('master')) h += `<h2>The master table</h2>` +
    tbl(['Distribution','Complete sufficient statistic','MLE','UMVUE','Note'], D.master);
  if(keys.includes('fisher')) h += `<h2>Fisher information</h2>` + tbl(['Distribution','I(θ)'], D.fisher);
  if(keys.includes('carry')) h += `<h2>Carry sheet</h2>` + tbl(['Idea','The deciding line'], D.carry);
  if(keys.includes('multi')){ h += `<h2>Multi-statement set</h2>`;
    D.bank.multi.forEach(q=>{ h += `<div class="q"><strong>${q.n}.</strong> ${esc(q.stem)}<br>` +
      q.sts.map((s,i)=>`${LET[i]}. ${esc(s)}`).join(' ') + `<br>` +
      q.opts.map((o,i)=>`(${LET[i]}) ${esc(o)}`).join(' ') +
      `<br><span class="a">→ (${q.ans}). ` + LET.map(L=>`${L} ${q.v[L].tf?'✓':'✗'} ${esc(q.v[L].why)}`).join('. ') +
      `</span></div>`; }); }
  if(keys.includes('numeric')){ h += `<h2>Numerical set</h2>`;
    D.bank.numerical.forEach(q=>{ h += `<div class="q"><strong>${q.n}.</strong> ${esc(q.stem)}<br>` +
      `<span class="a">→ ${esc(q.ans)}. ${esc(q.work)}${q.check?' <em>Check: '+esc(q.check)+'</em>':''}</span></div>`; }); }
  if(keys.includes('concept')){ h += `<h2>Conceptual set</h2>`;
    D.bank.conceptual.forEach(q=>{ h += `<div class="q"><strong>${q.n}.</strong> ${esc(q.stem)}<br>` +
      q.opts.map((o,i)=>`(${LET[i]}) ${esc(o)}`).join(' ') +
      `<br><span class="a">→ (${q.ans}). ${esc(q.expl)}</span></div>`; }); }
  if(keys.includes('log') && Log.items.length) h += `<h2>Error log</h2>` +
    tbl(['Type','Question','Fix','Logged'], Log.items.map(i=>[i.type,i.ref,i.fix,(i.ts||'').slice(0,10)]));
  return h + `</body></html>`;
}
function buildCSV(){
  const q = s => '"'+String(s).replace(/"/g,'""')+'"';
  const rows = [];
  D.carry.forEach(r=>rows.push([q(r[0]), q(r[1]), q('week1 carry')]));
  D.master.forEach(r=>{
    rows.push([q('Complete sufficient statistic for '+r[0]), q(r[1]), q('week1 master')]);
    if(r[2]) rows.push([q('MLE for '+r[0]), q(r[2]), q('week1 master')]);
    if(r[3]) rows.push([q('UMVUE for '+r[0]), q(r[3]), q('week1 master')]);
  });
  D.fisher.forEach(r=>rows.push([q('Fisher information for '+r[0]), q(r[1]), q('week1 fisher')]));
  return rows.map(r=>r.join(',')).join('\n');
}
async function doDownload(kind){
  const keys = selected();
  if(kind==='html' && !keys.length){ toast('Tick at least one section'); return; }
  const data = kind==='html' ? buildHTML(keys) : buildCSV();
  const filename = kind==='html' ? 'week1-point-estimation-selected.html' : 'week1-anki.csv';
  const dl = window.claude?.use ? await window.claude.use('downloads').catch(()=>null) : null;
  if(!dl){ toast('Downloads are not available in this view'); return; }
  try{ await dl.save({filename, data}); toast('Saved'); }
  catch(e){ toast(e && e.code==='declined' ? 'Download cancelled' : 'Could not save the file'); }
}

/* ---------- boot ---------- */
renderMulti(); renderNum(); renderConc(); renderRecall(); renderOffline();
show(lsGet('pe.tab','multi'));
(async ()=>{
  if(!window.claude?.use) return;
  try{
    const u = await window.claude.use('user');
    db = await window.claude.use('db');
    if(db){ store='db'; uid = u ? await u.id() : null; await Log.load(); if(!$('#p-log').hidden) renderLog(); }
  }catch(e){}
})();
</script>'''

CONCEPT_SVG = r'''<svg viewBox="0 0 700 430" role="img" aria-label="How the week fits together" style="min-width:560px">
<defs><marker id="ar" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
<polygon points="0 0, 9 3.5, 0 7" fill="var(--muted)"/></marker></defs>
<style>
.bx{fill:var(--card);stroke:var(--line);stroke-width:1.2}
.bk{fill:var(--accent-soft);stroke:var(--accent);stroke-width:1.4}
.tl{font:600 12.5px var(--sans);fill:var(--ink)}
.sb{font:11px var(--sans);fill:var(--muted)}
.ln{stroke:var(--muted);stroke-width:1.2;fill:none;marker-end:url(#ar)}
.lb{font:10.5px var(--sans);fill:var(--muted)}
</style>
<rect class="bx" x="12" y="20" width="150" height="46" rx="7"/>
<text class="tl" x="24" y="42">Factorisation</text><text class="sb" x="24" y="57">f = g(T;θ)·h(x)</text>

<rect class="bk" x="222" y="20" width="150" height="46" rx="7"/>
<text class="tl" x="234" y="42">Sufficiency</text><text class="sb" x="234" y="57">T keeps everything</text>

<rect class="bx" x="12" y="104" width="150" height="46" rx="7"/>
<text class="tl" x="24" y="126">Exponential family</text><text class="sb" x="24" y="141">h·c(θ)·exp[w(θ)t(x)]</text>

<rect class="bk" x="222" y="104" width="150" height="46" rx="7"/>
<text class="tl" x="234" y="126">Completeness</text><text class="sb" x="234" y="141">E[g(T)]=0 ⟹ g≡0</text>

<rect class="bx" x="432" y="20" width="150" height="46" rx="7"/>
<text class="tl" x="444" y="42">Rao–Blackwell</text><text class="sb" x="444" y="57">variance no larger</text>

<rect class="bk" x="432" y="104" width="150" height="46" rx="7"/>
<text class="tl" x="444" y="126">Lehmann–Scheffé</text><text class="sb" x="444" y="141">unique UMVUE</text>

<rect class="bx" x="12" y="188" width="150" height="46" rx="7"/>
<text class="tl" x="24" y="210">Ancillarity</text><text class="sb" x="24" y="225">distribution free of θ</text>

<rect class="bx" x="222" y="188" width="150" height="46" rx="7"/>
<text class="tl" x="234" y="210">Basu</text><text class="sb" x="234" y="225">the two are independent</text>

<rect class="bx" x="12" y="282" width="150" height="46" rx="7"/>
<text class="tl" x="24" y="304">Regularity</text><text class="sb" x="24" y="319">support free of θ</text>

<rect class="bx" x="222" y="282" width="150" height="46" rx="7"/>
<text class="tl" x="234" y="304">Fisher information</text><text class="sb" x="234" y="319">I(θ) = −E[∂²log f/∂θ²]</text>

<rect class="bx" x="432" y="282" width="150" height="46" rx="7"/>
<text class="tl" x="444" y="304">Cramér–Rao</text><text class="sb" x="444" y="319">a floor on variance</text>

<rect class="bx" x="222" y="366" width="150" height="46" rx="7"/>
<text class="tl" x="234" y="388">MLE and moments</text><text class="sb" x="234" y="403">routes that ignore all this</text>

<path class="ln" d="M162 43 H 218"/>
<path class="ln" d="M372 43 H 428"/>
<path class="ln" d="M162 127 H 218"/>
<path class="ln" d="M372 127 H 428"/>
<path class="ln" d="M297 66 V 100"/>
<path class="ln" d="M507 66 V 100"/>
<path class="ln" d="M297 150 V 184"/>
<path class="ln" d="M162 211 H 218"/>
<path class="ln" d="M162 305 H 218"/>
<path class="ln" d="M372 305 H 428"/>
<path class="ln" d="M297 328 V 362"/>
<text class="lb" x="378" y="38">one S</text>
<text class="lb" x="378" y="122">two S</text>
<text class="lb" x="302" y="88">adds</text>
<text class="lb" x="512" y="88">plus completeness</text>
<text class="lb" x="302" y="172">meets no information</text>
<text class="lb" x="302" y="352">if they fail</text>
</svg>'''

FLOW_SVG = r'''<svg viewBox="0 0 660 400" role="img" aria-label="UMVUE decision flowchart" style="min-width:520px">
<defs><marker id="ar2" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
<polygon points="0 0, 9 3.5, 0 7" fill="var(--muted)"/></marker></defs>
<style>
.d{fill:var(--accent-soft);stroke:var(--accent);stroke-width:1.4}
.b{fill:var(--card);stroke:var(--line);stroke-width:1.2}
.g{fill:var(--ok-soft);stroke:var(--ok);stroke-width:1.4}
.t{font:600 12.5px var(--sans);fill:var(--ink)}
.s{font:11px var(--sans);fill:var(--muted)}
.l{stroke:var(--muted);stroke-width:1.2;fill:none;marker-end:url(#ar2)}
.e{font:10.5px var(--sans);fill:var(--muted)}
</style>
<rect class="d" x="170" y="14" width="300" height="52" rx="7"/>
<text class="t" x="186" y="36">Is there a complete sufficient statistic T?</text>
<text class="s" x="186" y="52">exponential family ⟹ yes. Uniform, Cauchy ⟹ check by hand</text>

<rect class="d" x="170" y="112" width="300" height="52" rx="7"/>
<text class="t" x="186" y="134">Can you see an unbiased function of T?</text>
<text class="s" x="186" y="150">does E of something built from T give τ(θ)?</text>

<rect class="g" x="20" y="212" width="250" height="56" rx="7"/>
<text class="t" x="36" y="234">Route A — that is the UMVUE</text>
<text class="s" x="36" y="250">X̄ for λ, (n−1)/ΣX for the rate,</text>
<text class="s" x="36" y="263">(n+1)/n · X₍ₙ₎ for U(0, θ)</text>

<rect class="g" x="330" y="212" width="300" height="56" rx="7"/>
<text class="t" x="346" y="234">Route B — Rao–Blackwellise</text>
<text class="s" x="346" y="250">start from an indicator on one observation,</text>
<text class="s" x="346" y="263">condition on T. The estimand never changes</text>

<rect class="b" x="170" y="320" width="300" height="52" rx="7"/>
<text class="t" x="186" y="342">No complete sufficient statistic</text>
<text class="s" x="186" y="358">a UMVUE may not exist — U(θ, θ+1) is the case</text>

<path class="l" d="M320 66 V 108"/>
<path class="l" d="M240 164 L 150 208"/>
<path class="l" d="M400 164 L 470 208"/>
<path class="l" d="M470 40 H 600 V 346 H 474"/>
<text class="e" x="330" y="90">yes</text>
<text class="e" x="176" y="190">yes</text>
<text class="e" x="438" y="190">no</text>
<text class="e" x="528" y="34">no</text>
</svg>'''

UNIF_SVG = r'''<svg viewBox="0 0 640 280" role="img" aria-label="Likelihood for the uniform family" style="min-width:460px">
<style>.ax{stroke:var(--line);stroke-width:1.2}.cv{stroke:var(--accent);stroke-width:2.4;fill:none}
.gd{stroke:var(--line);stroke-dasharray:3 4}.lb{font:11px var(--sans);fill:var(--muted)}
.hl{font:600 12px var(--sans);fill:var(--accent)}</style>
<line class="ax" x1="60" y1="30" x2="60" y2="230"/>
<line class="ax" x1="60" y1="230" x2="610" y2="230"/>
<line class="gd" x1="240" y1="30" x2="240" y2="230"/>
<path class="cv" d="M60 230 L 240 230"/>
<path class="cv" d="M240 230 L 240 62"/>
<path class="cv" d="M240 62 C 300 100, 380 150, 600 198"/>
<circle cx="240" cy="62" r="5.5" fill="var(--accent)"/>
<text class="hl" x="252" y="56">maximum at θ = x₍ₙ₎</text>
<text class="lb" x="246" y="248">x₍ₙ₎</text>
<text class="lb" x="120" y="214">L(θ) = 0</text>
<text class="lb" x="118" y="228" font-size="10">no θ below the data</text>
<text class="lb" x="400" y="130">L(θ) = 1/θⁿ, falling</text>
<text class="lb" x="596" y="248" text-anchor="end">θ</text>
<text class="lb" x="30" y="36">L(θ)</text>
</svg>'''

HTML = (HTML.replace('__DATA__', payload)
            .replace('${CONCEPT_SVG}', CONCEPT_SVG)
            .replace('${FLOW_SVG}', FLOW_SVG)
            .replace('${UNIF_SVG}', UNIF_SVG))

open('/home/claude/w1/hub.html', 'w', encoding='utf-8').write(HTML)
print('wrote hub.html', len(HTML), 'bytes')
