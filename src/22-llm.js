/* ===================== LLM helper ===================== */
function askBox(id,label,prompt,tier){
  return '<div class="ask" id="'+id+'"><button class="btn sm" data-ask="'+id+'" data-tier="'+(tier||"default")+'">✦ '+esc(label)+'</button>'+
    '<textarea hidden data-p="'+id+'">'+esc(prompt)+'</textarea><div class="out" hidden></div></div>';
}
async function runAsk(box){
  const ta=box.querySelector("textarea[data-p]"),out=box.querySelector(".out"),btn=box.querySelector("button[data-ask]");
  if(!S.sampleFn){out.hidden=false;out.textContent="Claude is not available in this view.";return}
  btn.disabled=true;out.hidden=false;out.textContent="Thinking…";
  try{
    const r=await S.sampleFn(ta.value,{modelTier:btn.dataset.tier,onText:({text})=>{out.textContent=text}});
    out.textContent=r.text||out.textContent;
  }catch(e){
    const c=e&&e.code;
    out.textContent=c==="not_granted"?"Permission for Claude was declined for this page.":
      c==="rate_limited"?"Too many requests just now — try again in a minute.":
      "Could not reach Claude"+(c?" ("+c+")":"")+".";
  }
  btn.disabled=false;
}

