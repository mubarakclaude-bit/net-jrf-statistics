/* ===================== Ask Claude, anywhere =====================
   A learner reading a lesson, sitting in the bank, or part-way through a mock should
   never have to leave the page to ask what a term means. This module gives one surface
   that works from every route: select any text and a chip appears, or press the Ask
   button in the scene bar, the bank row, or the quiz. Every exchange is kept and shown
   in Admin, because the questions people ask are the clearest signal of where the
   written content is too thin.

   One deliberate restriction: during an unsubmitted mastery test the assistant is told
   to define terms and refuse the answer. The mastery score is the only verified number
   in this app, and an assistant that answers the paper for you destroys it.
*/
const ASKINTENT=[
  ["define",   "Define the term",      "a tight definition, then one sentence on why it is defined that way"],
  ["elaborate","Explain further",      "a fuller explanation than the page gives, with the reasoning spelled out"],
  ["basics",   "Drill to the basics",  "assume almost nothing and build up from the simplest idea that makes this make sense"],
  ["example",  "Give me an example",   "a concrete worked example with real numbers, carried through to the answer"],
  ["exam",     "Why it matters in the exam", "how this is actually asked in UGC NET Statistics, and the usual trap"],
  ["free",     "Ask something else",   "answer exactly what is asked"]];

/* Where the learner is, in enough detail for a useful answer. */
function askCtx(){
  const c={route:S.route,topicId:null,topic:null,sceneId:null,scene:null,qId:null,qText:null,locked:false};
  if(S.route==="learn"&&S.learn&&S.learn.topicId){
    const les=S.lessons[S.learn.topicId];
    c.topicId=S.learn.topicId;
    c.topic=(les&&les.title)||topicName(S.learn.topicId)||S.learn.topicId;
    const Q=S.learn.quiz;
    if(Q&&Q.list&&Q.list[Q.i]!==undefined){
      const q=Q.list[Q.i];
      c.qId=q.id;c.qText=q.stem;c.sceneId="quiz";c.scene="Mastery test";
      c.locked=!Q.done;                      // unsubmitted: no answers, no hints
    }else if(les&&S.learn.i>=0&&les.scenes[S.learn.i]){
      const sc=les.scenes[S.learn.i];c.sceneId=sc.id;c.scene=sc.title;
    }else{c.sceneId="overview";c.scene="Lesson overview"}
  }
  else{
    const q=currentAskQuestion();
    if(q){c.qId=q.id;c.qText=q.stem;c.topicId=q.topic||null;
      c.topic=c.topicId?(topicName(c.topicId)||c.topicId):(q.moduleId||"Question bank");
      c.scene=S.route==="mock"?"Mock test":S.route==="drill"?"Drill":"Question bank";
      // Hold the answer back until they have committed to one: in a mock until it is
      // submitted, in a drill until they have checked their own.
      c.locked=S.route==="mock"?!(S.mock&&S.mock.done):(S.route==="drill"?!(S.drill&&S.drill.checked):false);
    }
  }
  return c;
}
/* The question on screen, whichever surface is showing one. */
function currentAskQuestion(){
  try{
    if(S.route==="drill"&&S.drill&&S.drill.list)return S.drill.list[S.drill.i]||null;
    if(S.route==="mock"&&S.mock&&S.mock.list)return S.mock.list[S.mock.i]||null;
  }catch(e){}
  return null;
}
function topicName(tid){
  let n=null;(S.catalog?S.catalog.modules:[]).forEach(m=>(m.topics||[]).forEach(t=>{if(t.id===tid)n=t.name}));
  return n;
}

/* Build the prompt. Context first so the answer lands at the right level, then the
   restriction if one applies, then the actual request. */
function askPrompt(ctx,intent,sel,free){
  const it=ASKINTENT.filter(x=>x[0]===intent)[0]||ASKINTENT[0];
  const L=[];
  L.push("You are helping one candidate prepare for UGC NET Statistics (Paper 2, subject code 107), aiming for JRF.");
  L.push("They are working through a study app and have asked a question from inside it.");
  L.push("");
  L.push("WHERE THEY ARE");
  if(ctx.topic)L.push("Topic: "+ctx.topic+(ctx.topicId?" ("+ctx.topicId+")":""));
  if(ctx.scene)L.push("Section: "+ctx.scene);
  if(ctx.qText)L.push("Question on screen: "+String(ctx.qText).slice(0,400));
  L.push("");
  if(sel){L.push("WHAT THEY SELECTED ON THE PAGE");L.push('"'+String(sel).slice(0,1200)+'"');L.push("")}
  if(free){L.push("THEIR QUESTION");L.push(String(free).slice(0,800));L.push("")}
  L.push("WHAT THEY WANT");
  L.push(it[1]+" — "+it[2]+".");
  L.push("");
  if(ctx.locked){
    L.push("IMPORTANT RESTRICTION");
    L.push("They are part-way through a scored test that has not been submitted. Do NOT give the answer to the");
    L.push("question on screen, do not say which option is right, and do not hint at it by elimination.");
    L.push("You may define terms and explain general theory. If what they asked cannot be answered without");
    L.push("giving the answer away, say so in one line and offer to explain it fully once they submit.");
    L.push("");
  }
  L.push("HOW TO ANSWER");
  L.push("Plain text, no markdown headings or bullet characters. Use the notation a statistics candidate expects.");
  L.push("Be direct and specific; skip preamble. Around 120-180 words unless the question needs the arithmetic");
  L.push("shown, in which case show it. If the page's own wording is loose or wrong, say so plainly.");
  return L.join("\n");
}

function askOpen(sel,intent){
  const ctx=askCtx();
  S.ask={ctx:ctx,sel:sel||"",intent:intent||(sel?"define":"free"),free:"",out:"",busy:false,err:null,saved:false};
  S.askChip=null;
  render();
}
function askClose(){S.ask=null;render()}

async function askRun(){
  const A=S.ask;if(!A||A.busy)return;
  if(!S.sampleFn){A.err="Claude is not available in this view.";render();return}
  A.busy=true;A.err=null;A.out="";A.saved=false;render();
  const prompt=askPrompt(A.ctx,A.intent,A.sel,A.free);
  try{
    const r=await S.sampleFn(prompt,{modelTier:A.intent==="basics"||A.intent==="example"?"complex":"default",
      onText:({text})=>{if(S.ask===A){A.out=text;render()}}});
    if(S.ask!==A)return;
    A.out=(r&&r.text)||A.out;A.busy=false;
    askRecord(A);
    render();
  }catch(e){
    if(S.ask!==A)return;
    const c=e&&e.code;
    A.err=c==="not_granted"?"Permission for Claude was declined for this page."
      :c==="rate_limited"?"Too many requests just now — wait a minute and try again."
      :"Could not reach Claude"+(c?" ("+c+")":"")+".";
    A.busy=false;render();
  }
}
/* Keep the exchange. This is the record Admin reads to find thin content. */
function askRecord(A){
  if(A.saved||!A.out)return;
  S.asks=S.asks||[];
  S.asks.push({ts:now(),profile:S.profile||"me",route:A.ctx.route,
    topicId:A.ctx.topicId||"general",topic:A.ctx.topic||"",
    sceneId:A.ctx.sceneId||"",scene:A.ctx.scene||"",qId:A.ctx.qId||"",
    intent:A.intent,sel:String(A.sel||"").slice(0,400),q:String(A.free||"").slice(0,400),
    a:String(A.out||"").slice(0,1500),helpful:null});
  A.saved=true;saveAsks();if(typeof saveFb==="function")saveFb();
}

/* ---- the panel ---- */
function askPanelHTML(){
  const A=S.ask;if(!A)return"";
  const c=A.ctx;
  const where=[c.topic&&(nTag(topNo(c.topicId))+esc(c.topic)),c.scene&&esc(c.scene)].filter(Boolean).join(" · ");
  return '<div class="modalwrap" data-askclose="bg">'+
    '<div class="modal askmodal" role="dialog" aria-label="Ask Claude">'+
      '<div class="row tight" style="justify-content:space-between;margin-bottom:8px">'+
        '<h3 style="margin:0">✦ Ask Claude</h3>'+
        '<button class="btn sm gh" data-askclose="1" aria-label="Close">✕</button></div>'+
      (where?'<p class="note" style="margin-bottom:8px">'+where+'</p>':"")+
      (c.locked?'<p class="note" style="color:var(--ochre);margin-bottom:8px">'+
        'A scored test is open, so Claude will explain terms but will not give the answer away. '+
        'Submit the test and it will go through the question in full.</p>':"")+
      (A.sel?'<div class="askquote">'+esc(A.sel.slice(0,600))+(A.sel.length>600?"…":"")+'</div>':"")+
      '<div class="askintents">'+ASKINTENT.map(x=>
        '<button class="btn sm'+(A.intent===x[0]?" p":"")+'" data-askintent="'+x[0]+'">'+esc(x[1])+'</button>').join("")+
      '</div>'+
      (A.intent==="free"||A.free
        ?'<textarea id="askFree" class="ta" rows="2" placeholder="What would you like to know?">'+esc(A.free)+'</textarea>':"")+
      '<div class="row" style="margin-top:8px">'+
        '<button class="btn p" data-asksend="1"'+(A.busy?" disabled":"")+'>'+(A.busy?"Thinking…":"Ask")+'</button>'+
        (A.out&&!A.busy?'<button class="btn sm" data-asksend="again">Ask again</button>':"")+
        '<span class="sp"></span>'+
        (A.out&&!A.busy?'<span class="note">Was this useful? </span>'+
          '<button class="btn sm" data-askhelp="1" title="Helpful">👍</button>'+
          '<button class="btn sm" data-askhelp="0" title="Not helpful — flags the section for rewriting">👎</button>':"")+
      '</div>'+
      (A.err?'<p class="note" style="color:var(--bad);margin-top:8px">'+esc(A.err)+'</p>':"")+
      (A.out?'<div class="askout">'+esc(A.out)+'</div>':"")+
      '<p class="note" style="margin-top:10px">Every question you ask is kept under Admin, so the thin parts of '+
        'the written content can be found and rewritten.</p>'+
    '</div></div>';
}
/* The chip that follows a text selection. */
function askChipHTML(){
  const c=S.askChip;if(!c)return"";
  return '<button class="askchip" data-askchip="1" style="left:'+Math.round(c.x)+'px;top:'+Math.round(c.y)+'px">'+
    '✦ Ask Claude</button>';
}

/* Watch for a text selection anywhere in the app and offer the chip. Bound once, on the
   document, so it keeps working across re-renders without being re-attached. */
function askSelectionWatch(){
  if(askSelectionWatch.on)return;askSelectionWatch.on=true;
  const place=()=>{
    try{
      if(S.ask)return;                                   // the panel is already open
      const sel=window.getSelection&&window.getSelection();
      if(!sel||sel.isCollapsed){if(S.askChip){S.askChip=null;render()}return}
      const text=String(sel.toString()||"").trim();
      // Selecting a whole paragraph to ask "elaborate on this" is a fair use, so the cap
      // here is generous; the prompt truncates what it actually sends.
      if(text.length<3||text.length>6000){if(S.askChip){S.askChip=null;render()}return}
      // ignore selections made inside the panel, inputs, or the admin prompt boxes
      const node=sel.anchorNode&&(sel.anchorNode.nodeType===1?sel.anchorNode:sel.anchorNode.parentElement);
      if(node&&node.closest&&node.closest(".askmodal,textarea,input,.modal"))return;
      const r=sel.getRangeAt(0).getBoundingClientRect();
      if(!r||(!r.width&&!r.height))return;
      const x=Math.min(Math.max(8,r.left),Math.max(8,window.innerWidth-150));
      const y=Math.max(8,r.top-40);
      const c=S.askChip;
      if(c&&c.text===text&&Math.abs(c.x-x)<2&&Math.abs(c.y-y)<2)return;
      S.askChip={text:text,x:x,y:y};render();
    }catch(e){}
  };
  document.addEventListener("mouseup",()=>setTimeout(place,10));
  document.addEventListener("keyup",e=>{if(e.shiftKey||e.key==="Escape")setTimeout(place,10)});
  document.addEventListener("keydown",e=>{
    if(e.key==="Escape"&&S.ask){askClose();return}
    // a keyboard way in, for anyone not using a mouse
    if((e.key==="k"||e.key==="K")&&(e.metaKey||e.ctrlKey)){e.preventDefault();
      const t=String((window.getSelection&&window.getSelection().toString())||"").trim();
      askOpen(t,t?"define":"free")}
  });
  document.addEventListener("scroll",()=>{if(S.askChip){S.askChip=null;render()}},true);
}
