/* ===================== utils ===================== */
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const pc=(a,b)=>b?Math.round(100*a/b):0;
const cl=(v,a,b)=>Math.max(a,Math.min(b,v));
const now=()=>Date.now();
const narrow=()=>((typeof window!=="undefined"&&window.innerWidth)||1200)<=980;
const fmtPct=v=>(v*100).toFixed(0)+"%";
function toast(m,ms){const t=document.createElement("div");t.id="toast";t.textContent=m;$("#toast")&&$("#toast").remove();document.body.appendChild(t);setTimeout(()=>t.remove(),ms||2200)}
function hhmm(s){s=Math.max(0,Math.round(s));const m=Math.floor(s/60);return String(m).padStart(2,"0")+":"+String(s%60).padStart(2,"0")}
function dayStr(ts){const d=new Date(ts);return d.toISOString().slice(0,10)}
function bar(p,c,sm){return '<div class="bar'+(sm?" sm":"")+'"><i class="'+(c||"")+'" style="width:'+cl(p,0,100)+'%"></i></div>'}
function ring(p,c){const r=20,C=2*Math.PI*r,o=C*(1-cl(p,0,100)/100);
  return '<svg class="ring" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="'+r+'" fill="none" stroke="var(--surface3)" stroke-width="5"/>'+
  '<circle cx="24" cy="24" r="'+r+'" fill="none" stroke="var(--'+(c||"accent")+')" stroke-width="5" stroke-linecap="round" stroke-dasharray="'+C.toFixed(1)+'" stroke-dashoffset="'+o.toFixed(1)+'" transform="rotate(-90 24 24)"/>'+
  '<text x="24" y="28" text-anchor="middle">'+Math.round(p)+'</text></svg>'}
function copy(txt,btn){
  try{navigator.clipboard.writeText(txt).then(()=>toast("Copied"),()=>sel())}catch(e){sel()}
  function sel(){const t=document.createElement("textarea");t.value=txt;t.style.position="fixed";t.style.opacity="0";document.body.appendChild(t);t.select();
    try{document.execCommand("copy");toast("Copied")}catch(e2){toast("Select the text and copy manually")}t.remove()}
}

/* panel geometry is a per-device convenience, so it lives in browser storage */
function savePanels(){
  try{localStorage.setItem("njpanels",JSON.stringify(
    {navW:S.navW,aideW:S.aideW,navOpen:S.navOpen,aideOpen:S.aideOpen}))}catch(e){}
}
function loadPanels(){
  try{const p=JSON.parse(localStorage.getItem("njpanels")||"null");if(!p)return;
    if(p.navW)S.navW=cl(+p.navW,200,520);
    if(p.aideW)S.aideW=cl(+p.aideW,200,520);
    if(!narrow()){if(typeof p.navOpen==="boolean")S.navOpen=p.navOpen;
                  if(typeof p.aideOpen==="boolean")S.aideOpen=p.aideOpen}
  }catch(e){}
}
