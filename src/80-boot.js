/* ===================== theme + routing ===================== */
(function(){
  const r=document.documentElement;
  let t=null;try{t=localStorage.getItem("njt")}catch(e){}
  if(t)r.setAttribute("data-theme",t);
  $("#themeBtn").onclick=()=>{
    const cur=r.getAttribute("data-theme");
    const dark=cur?cur==="dark":window.matchMedia("(prefers-color-scheme: dark)").matches;
    const nx=dark?"light":"dark";r.setAttribute("data-theme",nx);
    try{localStorage.setItem("njt",nx)}catch(e){}};
})();
window.addEventListener("hashchange",()=>{
  const h=(location.hash||"").replace("#","");
  if(TABS.some(([k])=>k===h)&&h!==S.route){S.route=h;S.drill=null;render()}});
(function(){const h=(location.hash||"").replace("#","");if(TABS.some(([k])=>k===h))S.route=h})();
loadPanels();
render();
boot();
