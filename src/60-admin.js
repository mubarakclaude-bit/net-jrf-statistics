/* ---------- admin: content factory ---------- */
/* ---- feedback across every learner ----
   The owner sees all of it; a learner only ever has their own. Each row is tagged with
   who sent it, so a question asked by three different people reads as three. */
function fbRows(key){
  const out=[];
  const mine=(key==="asks"?(S.asks||[]):(S.reqs||[]));
  // Other learners come from the shared store; the current viewer's own rows come from
  // memory, so something just asked shows up without waiting for the debounced write.
  if(S.isAdmin&&Array.isArray(S.fb)){
    S.fb.forEach(d=>{
      const id=d.id||d.uid||"";
      // supersede the stored copy only when there IS a live one; otherwise a viewer
      // whose memory has not loaded would lose their own history from the view
      if(id&&S.uid&&id===S.uid&&mine.length)return;
      (d[key]||[]).forEach(r=>out.push(Object.assign({},r,
        {_uid:id,_who:d.name||d.label||"learner"})));
    });
  }
  mine.forEach(r=>out.push(Object.assign({},r,{_uid:S.uid||"",_who:S.ownerName||"you"})));
  return out;
}
function fbWho(r){
  const who=r._who||"learner";
  const id=String(r._uid||"").replace(/^u_/,"").slice(0,6);
  return who+(id?" \u00b7 "+id:"");
}
function fbLearners(key){
  const m={};fbRows(key).forEach(r=>{m[r._uid||"?"]=r._who||"learner"});
  return Object.keys(m).length;
}

const STAGES=[
 ["blueprint","Module blueprint","Plan the lessons for a whole module: which topics get one, in what order, with objectives and prerequisites.","complex"],
 ["lesson","Lesson","The full teaching document for ONE topic — scenes, theory, worked examples, visuals, revision sheet, references.","complex"],
 ["practice","Practice questions","A linked practice set for one topic, browsable in the bank.","complex"],
 ["mastery","Mastery test","An unseen set, held out of the bank and out of mocks, used only for the pass/fail test.","complex"],
 ["validation","Validation pass","Check an existing lesson and its keys: formulas, answers, notation, coverage, source claims.","complex"]];

function vAdmin(){
  const url=(S.app&&S.app.url)||"";
  const ms=S.catalog?mods():[];
  const idx=S.index||{modules:{}};
  const lix=(S.lessonIdx&&S.lessonIdx.topics)||{};
  const rows=ms.map(m=>{const x=idx.modules[m.id]||{total:0,pyq:0,variant:0,mastery:0,sets:[]};
    const les=m.topics.filter(t=>lix[t.id]).length;
    return{m:m,t:x.total,pyq:x.pyq||0,va:x.variant||0,mas:x.mastery||0,sets:x.sets||[],les:les}});
  const tot=rows.reduce((s,r)=>s+r.t,0),tgt=rows.reduce((s,r)=>s+(r.m.targetQ||0),0);
  const lesTot=rows.reduce((s,r)=>s+r.les,0),topTot=ms.reduce((s,m)=>s+m.topics.length,0);
  const pm=modById(S.pickMod)||(rows.filter(r=>r.t<r.m.targetQ).sort((a,b)=>b.m.marks-a.m.marks)[0]||rows[0]||{}).m||null;
  const pt=pm?(pm.topics.find(t=>t.id===S.pickTopic)||pm.topics[0]):null;
  return '<div class="hd"><h1>Admin · content factory</h1><p>This page holds no content. Every lesson, question set and syllabus row lives in the artifact\'s database, so a separate chat can author a topic without the app being rebuilt.</p>'+
    '<div class="sp row tight"><button class="btn sm" id="rescan">Rescan store</button>'+(S.dl?'<button class="btn sm" id="exportAll">Export everything</button>':"")+'</div></div>'+
  (!S.catalog?'<div class="banner ac"><div><b>Seed the catalog first.</b> Paste into a new chat: <span class="mono">Write the 21-module NET Statistics catalog to meta/catalog in artifact '+(url||"&lt;this artifact\'s URL&gt;")+'</span></div></div>':"")+
  '<div class="grid g2" style="margin-bottom:12px">'+
    '<div class="card flat"><div class="kv"><span class="lbl">Lessons authored</span><b>'+lesTot+' of '+topTot+' topics</b></div>'+bar(pc(lesTot,topTot),"ac")+
      '<p class="note" style="margin-top:6px">A topic without a lesson can still be drilled from the bank — it just has nothing to teach from.</p></div>'+
    '<div class="card flat"><div class="kv"><span class="lbl">Question bank fill</span><b>'+tot+' of '+tgt+'</b></div>'+bar(pc(tot,tgt),"och")+
      '<p class="note" style="margin-top:6px">Five per mark. Index rebuilt '+esc(idx.updated?idx.updated.slice(0,16).replace("T"," "):"never")+'.</p></div>'+
  '</div>'+
  factoryCard(pm,pt,url,idx,lix)+
  '<div class="card" style="margin-bottom:12px"><h3 style="margin-bottom:8px">Per module</h3><div class="scroll"><table class="tbl"><thead><tr>'+
    '<th>Module</th><th>Marks</th><th>Lessons</th><th>Bank</th><th>PYQ</th><th>Mastery</th><th>Target</th><th>Fill</th><th></th></tr></thead><tbody>'+
    rows.map(r=>'<tr><td>'+esc(r.m.name)+'</td><td class="num">'+r.m.marks+'</td>'+
      '<td class="num">'+r.les+'/'+r.m.topics.length+'</td><td class="num"><b>'+r.t+'</b></td><td class="num">'+r.pyq+'</td>'+
      '<td class="num">'+r.mas+'</td><td class="num">'+r.m.targetQ+'</td>'+
      '<td style="min-width:80px">'+bar(pc(r.t,r.m.targetQ),r.t>=r.m.targetQ?"ok":r.t?"och":"dim",true)+'</td>'+
      '<td><button class="btn sm" data-prompt="'+r.m.id+'">open</button></td></tr>').join("")+
    '</tbody></table></div></div>'+
  usersCard()+
  importCard(url)+
  schemaCard()+
  diagCard()+
  offlineCard(ms);
}
function factoryCard(pm,pt,url,idx,lix){
  if(!pm)return"";
  const stage=S.stage||"lesson";
  const has=pt?!!lix[pt.id]:false;
  const txt=stagePrompt(stage,pm,pt,url,idx,lix);
  return '<div class="card" style="margin-bottom:12px">'+
    '<h3 style="margin-bottom:4px">Generate a prompt pack</h3>'+
    '<p class="note" style="margin-bottom:10px">Pick what to author, copy the prompt into a new chat, and the result is written straight into this artifact\'s store. Come back and press <b>Rescan store</b>.</p>'+
    '<div class="grid g3" style="margin-bottom:10px">'+
      '<div><label class="fl">Module</label><select id="fMod2">'+mods().map(m=>'<option value="'+m.id+'"'+(m.id===pm.id?" selected":"")+'>'+modNo(m.id)+' · '+esc(m.name)+'</option>').join("")+'</select></div>'+
      '<div><label class="fl">Topic</label><select id="fTop">'+pm.topics.map(t=>'<option value="'+t.id+'"'+(pt&&t.id===pt.id?" selected":"")+'>'+topNo(t.id)+' · '+esc(t.name)+(lix[t.id]?"  ✓ lesson":"")+'</option>').join("")+'</select></div>'+
      '<div><label class="fl">Stage</label><select id="fStage">'+STAGES.map(s=>'<option value="'+s[0]+'"'+(stage===s[0]?" selected":"")+'>'+esc(s[1])+'</option>').join("")+'</select></div>'+
    '</div>'+
    '<p class="note" style="margin-bottom:8px">'+esc((STAGES.find(s=>s[0]===stage)||[])[2]||"")+
      (has&&stage==="lesson"?' <b style="color:var(--ochre)">A lesson already exists for this topic — writing it again replaces it. Use the validation stage instead to check it.</b>':"")+'</p>'+
    '<textarea id="pBox" style="min-height:320px" readonly>'+esc(txt)+'</textarea>'+
    '<div class="row" style="margin-top:8px">'+
      (S.sampleFn&&stage!=="blueprint"&&stage!=="validation"
        ? '<button class="btn p sm" id="genRun">✦ Author it here</button>' : '')+
      '<button class="btn sm" id="pCopy">Copy prompt for a chat</button>'+
      (S.dl?'<button class="btn sm" id="pSave">Save as a file</button>':"")+
      '<span class="note">'+txt.split("\n").length+' lines</span></div>'+
    (S.sampleFn&&(stage==="blueprint"||stage==="validation")
      ?'<p class="note" style="margin-top:6px">This stage has no in-app run: a blueprint is for you to read and decide on, and a validation pass needs to fetch the reference URLs, which this page cannot do. Both belong in a chat.</p>':"")+
    genPanel()+
  '</div>'+
  askPanel()+
  reqPanel();
}
/* Everything the learner asked for, newest first, ready to hand to an authoring chat. */
function reqPanel(){
  const rs=fbRows("reqs").sort((a,b)=>(b.ts||0)-(a.ts||0));
  const K={};REQKIND.forEach(k=>{K[k[0]]=k[1]});
  return '<div class="card" style="margin-bottom:12px">'+
    '<div class="row tight" style="justify-content:space-between;margin-bottom:8px">'+
      '<h3 style="margin:0">Requests from '+(S.isAdmin?"learners":"you")+'</h3>'+
      '<span class="chip '+(rs.length?"ac":"dim")+' num">'+rs.length+'</span>'+
      (S.isAdmin?'<span class="chip och num">'+fbLearners("reqs")+' learner'+
        (fbLearners("reqs")===1?"":"s")+'</span>':"")+'</div>'+
    (rs.length
      ? '<div class="reqlist">'+rs.slice(0,60).map((r,i)=>
          '<div class="reqrow">'+
            '<span class="chip '+(r.kind==="bug"?"bad":"och")+'">'+esc(K[r.kind]||r.kind)+'</span>'+
            '<div class="rqb"><b>'+esc(r.topic||"")+' · '+esc(r.scene||"")+'</b>'+
              '<div class="note">'+esc(r.text||"")+'</div>'+
              '<div class="note num">'+(S.isAdmin?esc(fbWho(r))+' \u00b7 ':"")+
                new Date(r.ts||0).toISOString().slice(0,16).replace("T"," ")+
                (r.profile&&r.profile!=="me"?" · "+esc(r.profile):"")+'</div></div>'+
            '<button class="btn sm gh" data-reqdel="'+i+'" title="Remove this request">\u2715</button>'+
          '</div>').join("")+'</div>'+
        '<div class="row" style="margin-top:10px">'+
          '<button class="btn sm" id="reqCopy">Copy them as an authoring brief</button>'+
          (S.dl?'<button class="btn sm" id="reqSave">Save as a file</button>':"")+'</div>'
      : '<p class="note">Nothing requested yet. Inside any lesson, the right-hand panel has \u201cAsk for more on this section\u201d \u2014 what you send lands here with the section reference attached.</p>')+
  '</div>';
}
function reqBrief(){
  const rs=(S.reqs||[]).slice().sort((a,b)=>(a.ts||0)-(b.ts||0));
  const K={};REQKIND.forEach(k=>{K[k[0]]=k[1]});
  return "# Content requests from the learner\n\n"+
    "Artifact: "+((S.app&&S.app.url)||"(url not set)")+"\n"+
    "Generated "+new Date().toISOString().slice(0,16).replace("T"," ")+"\n\n"+
    rs.map(r=>"## "+(K[r.kind]||r.kind)+" \u2014 "+(r.topic||"")+"\n"+
      "- topic id: `"+(r.topicId||"")+"`  section: `"+(r.sceneId||"")+"` ("+(r.scene||"")+")\n"+
      "- asked: "+new Date(r.ts||0).toISOString().slice(0,16).replace("T"," ")+"\n\n"+
      (r.text||"")+"\n").join("\n");
}

const PACK_AUDIENCE = [
'WHO THIS IS FOR',
'Most NET candidates come back to preparation after two or three years away — a job, a',
'teaching post, a family. The statistics was learnt once, properly, and has gone quiet.',
'So the content starts from the base and climbs:',
'  - Open every idea in plain words and one concrete case before a symbol appears.',
'  - Name the second-year tool the first time you use it, in a clause, not a footnote.',
'  - Never write "clearly", "obviously", "recall that" or "as we know". If a step needs',
'    recalling, spend the line and recall it.',
'  - Carry every algebraic step. The gap, not the difficulty, is what makes a derivation',
'    unreadable to someone out of practice.',
'  - Short sentences. No cheerleading. Write for a tired adult at five in the morning.',
'  - Where a prerequisite is genuinely needed, do not explain it inline — put it in the',
'    opening foundation drill, which exists for exactly this.'
].join("\n");

const SCHEMA_LESSON = [
'LESSON DOCUMENT — write to  lessons/<lessonId>   (lessonId: lowercase, e.g. "mle")',
'{',
'  "id","moduleId","topicId","title","breadcrumb","engine","engineName","estMin",',
'  "version":"1.0","status":"approved","provenance":"<who authored what>",',
'  "objectives":[ 4-6 strings, each something the learner can DO ],',
'  "prereq":[ {"id","name","why"} x3-4 — the opening foundation drill is built from these ],',
'  "mastery":{"minQ":10,"pass":80,"draw":10,"fmtMin":{"numeric":70,"multi":70},',
'             "diffMix":{"easy":3,"moderate":5,"hard":2},"noHints":true,',
'             "retestDays":7,"note":"<say these are platform settings, not NTA rules>"},',
'  "refs":[ {"title","where","site","url","type","free":true,"checked":"YYYY-MM-DD","why"} ],',
'  "revision":{"sheet":[ 8-12 one-line facts ], "cards":[ [front,back] x8 ],',
'              "tricks":[ {"hook","why"} x3-4 ], "shortcuts":[ 3-4 strings ],',
'              "remember":[ 2-3 strings ], "traps":[ 3-5 strings ]},',
'  "traps":[ 5-8 strings ],',
'  "scenes":[ ... see below ... ]',
'}',
'',
'revision.tricks, .shortcuts and .remember are what the right-hand rail shows as Memory aids',
'beside every scene: a mnemonic with the reason it works, a rule of thumb, and the one line to',
'keep if everything else goes. Without them that panel says nothing has been authored.',
'',
'SCENE KINDS — the lesson OPENS with foundation, then runs intuition to quiz:',
'  {"id","kind":"foundation","title","mins","objective","body":[2-3 paragraphs on why this',
'   check exists],"items":[{"ask":"<the prerequisite, as a question>",',
'   "recall":"<the one-line answer>","refresh":[2-3 paragraphs that rebuild it from the base,',
'   with one small worked instance]} x3-5]}',
'  {"id","kind":"intuition","title","mins","objective","body":[paragraphs],',
'   "aside":{"h","body"},"ask":{"q","nudge"}}',
'  {"id","kind":"explore","title","mins","objective","body":[paragraphs],',
'   "viz":{"type":"exp-likelihood"|"mle-sampling"|"unif-likelihood"|"np-power", ...params},"ask":{"q","nudge"}}',
'  {"id","kind":"theory","title","mins","objective",',
'   "blocks":[{"t":"def"|"formula"|"step"|"assume"|"note"|"trap","h","body"}]}',
'  {"id","kind":"worked","title","mins","objective","problem",',
'   "steps":[{"say","math","why"}],"after":"<what to take from it>"}',
'  {"id","kind":"recall","title","mins","objective","intro","items":[{"q","a"}]}',
'  {"id","kind":"completion","title","mins","objective","problem",',
'   "steps":[{"say","math","why"} or {"say","blank":{"prompt","answer","accept":[...],"hint"},"why"}],"after"}',
'  {"id","kind":"guided","title","mins","objective","problem","hints":[direction,method,next-step],',
'   "solution":[{"say","math"}],"answer","check"}',
'  {"id","kind":"trapcheck","title","mins","objective","intro","items":[{"claim","tf":true|false,"why"}]}',
'  {"id","kind":"summary","title","mins","objective","body":[strings]}',
'  {"id","kind":"quiz","title","mins","objective","setId":"<the mastery set id>"}',
'',
'FLOW DIAGRAMS — any scene may carry one, and at least one scene in the lesson must.',
'The app draws it with no library, from the grid you give, so the layout is yours:',
'  "flow":{"caption","nodes":[{"id","r":row from 0,"c":column from 0,"w":columns wide (optional),',
'          "label","kind":"start"|"step"|"decision"|"end"|"note"}],',
'          "edges":[{"from","to","label":"<short, optional>","side":"l"|"r" (optional)}]}',
'  4-8 nodes, at most 4 columns. Place nodes so edges run down or across, never diagonally.',
'  Draw the things worth drawing: a decision procedure ("is the support free of theta?"), the',
'  route through a derivation, or a classification with its boundaries.',
'',
'REAL-WORLD SCENARIOS — at least two scenes carry one. It sits collapsed under the scene and',
'opens in place, so the learner can drill into it and come straight back:',
'  "scenario":{"teaser":"<one line naming the situation>","title","body":[3-5 paragraphs],',
'              "flow":{...} (optional),"close":"<what the idea bought them, in one sentence>"}',
'  Use real practice — reliability testing, crop trials, clinical monitoring, insurance claims,',
'  official surveys. Never present invented numbers as historical fact: if you do not know the',
'  real figures, describe the situation qualitatively instead.',
'',
'Only those four "viz" types exist in the app today — the likelihood of an exponential sample,',
'the sampling distribution of n/SigmaX, the U(0,theta) likelihood cliff, and a one-sided normal',
'test\'s critical value and power. Do not invent a fifth: a scene referencing an unknown type',
'renders its text and says the visual is unavailable.'
].join("\n");

const SCHEMA_Q = [
'QUESTION ITEM — one of five shapes, "format" decides which:',
'  single : {"id","format":"single","topic","diff","stem","options":[4],"answer":"A".."D","explanation"}',
'  numeric: {"id","format":"numeric","topic","diff","stem","options":[4],"answer","explanation","check"}',
'           (for a write-in numerical, pass "options":[] and put the full answer in "answer")',
'  multi  : {"id","format":"multi","topic","diff","stem","statements":[4],"options":[4],"answer",',
'            "verdicts":{"A":{"tf":true,"why"},"B":{...},"C":{...},"D":{...}},"explanation"}',
'  match  : {"id","format":"match","topic","diff","stem","pairs":[[ListI,ListII] x4],"options":[4],"answer","explanation"}',
'  order  : {"id","format":"order","topic","diff","stem","items":[4 steps],"options":[4],"answer","explanation"}',
'',
'  - "diff" is required on every item: "easy" | "moderate" | "hard".',
'      easy     one definition or one step, answerable from recall in under a minute',
'      moderate two or three steps, or one step plus a verification',
'      hard     a transfer case, a boundary condition, or an answer needing a trap avoided',
'    The app draws every test as 3 easy / 5 moderate / 2 hard, to model a NET-style paper, and',
'    a retake draws again from the same pool — so a pool short of a band cannot be drawn evenly.',
'  - spread the keys across A, B, C and D. A pool keyed mostly to one letter hands marks to a',
'    candidate who guesses that letter throughout; no letter should hold more than 40% of a set.',
'  - options are four plain strings with no "A)" prefix — the app adds the letters.',
'  - every numeric item needs "check": the quantity actually asked, and the one verification',
'    that catches the usual slip.',
'  - every multi item needs a verdict AND a reason for all four statements.',
'  - an explanation is written for someone returning after years away: name the result it rests',
'    on, and say why each distractor is wrong. An explanation that restates the key has failed.'
].join("\n");

const REPO = "https://github.com/mubarakclaude-bit/net-jrf-statistics";
function stagePrompt(stage,m,t,url,idx,lix){
  const U=url||"<paste the artifact URL here>";
  const x=(idx.modules||{})[m.id]||{total:0,mastery:0,sets:[]};
  const head=[
  "Author study content for my UGC NET Statistics JRF app and write it into the artifact's database.",
  "",
  "Artifact: "+U,
  "Module: "+m.id+" — "+m.name+"  ("+m.marks+" of "+(m.paper===2?200:100)+" marks, Paper "+m.paper+")",
  "My June 2026 score on this module: "+m.baseline+" questions correct.",
  ].join("\n");
  const tctx=t?["Topic: "+topNo(t.id)+" "+t.id+" — "+t.name,
    "Required depth: "+t.extent+" — "+EXT[t.extent].d+".",
    t.imp?("Exam weight: "+IMP[t.imp].s+" "+IMP[t.imp].n+" — "+IMP[t.imp].d+
      (t.qs?(". About "+t.qs+" question"+(t.qs>1?"s":"")+" a paper, "+(t.marks||t.qs*2)+" marks.")
           :"")+" Weight decides how many worked examples and transfer cases it earns, not the tone."):"",
    "Lesson already present: "+(lix[t.id]?("yes, "+lix[t.id].scenes+" scenes, version "+lix[t.id].version):"no")].join("\n"):"";
  const tail=[
  "",
  "START HERE — THE PIPELINE IS IN A REPO, DO NOT REBUILD IT",
  "  "+REPO,
  "Clone it, then read SPEC.md before writing anything. It carries the house standard, the",
  "pool rules, the registered visualisation names and the store layout, and the repo holds the",
  "validators that enforce them. An authoring script written without reading SPEC.md will fail",
  "validation on the first run.",
  "",
  "Work the way the repo does:",
  "  1. Read SPEC.md, then lessons/EXAMPLE.py as the pattern to follow.",
  "  2. Check seed/*_pyq_variants.json for this topic. Where a previous-year question and its",
  "     variants exist, THOSE ARE THE SPECIFICATION — each variant stem earns a section or a",
  "     pool item. Read the full stem, never a one-line label: two questions in this bank are",
  "     filed under the wrong module and one was nearly built as the wrong topic entirely.",
  "  3. VERIFY EVERY NUMBER by computing it — one script at the end, not checks interleaved.",
  "     Simulate, integrate, enumerate. Roughly half the lessons so far had a figure of mine",
  "     that was wrong until a script caught it. State in the provenance what you verified and how.",
  "  4. Write the authoring script, then run:",
  "       ./addlesson.sh <script.py> <seed-stem> <topicId> <storeDocId> <masterySetStem>",
  "     It generates the seed, runs both validators, renders every formula, audits the pool for",
  "     self-cited answers, wires the test harness and updates the index. Fix what it reports",
  "     and re-run until it passes clean. Do not push a lesson it has not passed.",
  "  5. Push with the ArtifactData tool, action \"set\", url "+U+", using file_path so a large",
  "     document never passes through the conversation. Batch the lesson, its question set and",
  "     meta/lessons into ONE batch call, pinning meta/lessons with if_version.",
  "  6. Run node test.js, then node clicktest.js. Both must pass.",
  "",
  "Never edit a store document you did not just write — add a new one instead, so two chats",
  "cannot overwrite each other.",
  "",
  "WHEN YOU ARE DONE",
  "Tell me the document path you wrote and the item count, commit and push the authoring script",
  "to the repo, and remind me to press \"Rescan store\" on the Admin tab so the counters and the",
  "learning tree pick it up."].join("\n");

  if(stage==="blueprint")return [head,"",
  "TASK — module blueprint.",
  "The module has these topics already in the catalog:",
  m.topics.map(z=>"  "+z.id+"  ["+z.extent+"]  "+z.name).join("\n"),
  "",
  "Produce a plan, not content: for each topic give the learning objectives, the prerequisite",
  "topics (by id where they are in this module, by name otherwise), an estimated lesson length,",
  "which of the registered visualisations could carry it (SPEC.md lists them; there are 18, and a",
  "name outside that list is rejected by the validator), and the order I should learn them in",
  "given that I scored "+m.baseline+" on this module in June 2026.",
  "Flag any topic in the official syllabus that these rows do not cover.",
  "",
  "Return it as a table in the chat. Do NOT write anything to the database for this stage —",
  "I want to read the plan and decide before any content is authored.",
  ].join("\n");

  if(stage==="lesson")return [head,tctx,"",
  "TASK — write the complete lesson for this ONE topic.",
  "",
  PACK_AUDIENCE,
  "",
  "This candidate can follow a derivation but cannot yet reproduce it alone, and loses marks on",
  "verification rather than method. Build the intuition before any algebra. Every scene has one",
  "objective and one thing to do. No walls of text.",
  "",
  "Required shape: 11-16 scenes, OPENING with the foundation drill —",
  "  foundation → intuition → explore → theory → worked → recall → completion → theory → explore",
  "  → guided → trapcheck → guided (transfer, unfamiliar framing) → summary → quiz",
  "",
  "THE FOUNDATION DRILL is the returning candidate's way in, and it is not optional. Take the",
  "3-4 prerequisites above and turn each into one check: the question, the one-line answer, and",
  "a rebuild from the base for anyone who marks it shaky. The learner answers \"I know this\" or",
  "\"Shaky — show me\" on each, and the rebuild opens in place. After that scene, nothing in the",
  "lesson may assume anything that is neither checked there nor taught here.",
  "",
  "Worked examples must FADE: the first shows every step, the completion scene hides steps and",
  "asks for them, the guided scenes give only a hint ladder. The last guided scene must be a",
  "case the lesson has not shown, so it tests method selection and not recall.",
  "",
  "The hint ladder is three rungs and never gives the answer:",
  "  1 direction — what to identify first.  2 method — which theorem or formula applies.",
  "  3 next step — the one operation to perform.",
  "",
  "ALSO REQUIRED, because the app renders them and an empty panel reads as a gap:",
  "  - at least one flow diagram, on whichever scene has something worth drawing;",
  "  - at least two real-world scenarios, collapsed under their scene;",
  "  - revision.tricks, .shortcuts and .remember for the Memory aids rail.",
  "",
  "REFERENCES: two or three, each pointing at the exact chapter, lesson or lecture number that",
  "covers this topic. Verify every URL resolves before you write it, and say in \"why\" what that",
  "source is for and at which scene to reach for it. If you cannot verify a link, leave it out.",
  "Never invent a citation.",
  "",
  "VERIFY EVERY NUMBER before you write it — critical values, variances, bounds, probabilities.",
  "Compute them rather than recalling them. A wrong figure in a lesson teaches the error.",
  "",
  SCHEMA_LESSON,"",
  "Write it to  lessons/"+(t?t.id.replace(/[^a-z0-9]/gi,"")+"":"<lessonId>")+"  with topicId \""+(t?t.id:"")+"\" and moduleId \""+m.id+"\".",
  "Set the quiz scene's setId to \""+m.id+"_"+(t?t.id.split("-").pop():"tN")+"_mastery\" — then run the mastery stage to create it.",
  tail].join("\n");

  if(stage==="practice")return [head,tctx,"",
  "TASK — a practice set of 15 questions for this topic, browsable in the question bank.",
  "",
  PACK_AUDIENCE,
  "",
  "Match the format mix of the real paper: "+FORDER.map(k=>FMT[k].mix+"% "+FMT[k].n.toLowerCase()).join(", ")+".",
  "Include at least two write-in numericals (options: []) — the exam is multiple choice, but",
  "back-solving from options hides exactly the weakness I need to fix.",
  "Mix the difficulty roughly 3 easy to 5 moderate to 2 hard, and tag every item with \"diff\".",
  "Every explanation must teach, not confirm. A one-line explanation is a failed question.",
  "",
  SCHEMA_Q,"",
  "Write to  qsets/"+m.id+"_"+(t?t.id.split("-").pop():"tN")+"_practice  with body:",
  '{ "moduleId":"'+m.id+'", "source":"variant", "topicId":"'+(t?t.id:"")+'",',
  '  "label":"'+(t?t.name:"")+' — practice", "count":15, "items":[...] }',
  'ids must be globally unique: "'+m.id+'-'+(t?t.id.split("-").pop():"tN")+'-p-01", -02, …',
  tail].join("\n");

  if(stage==="mastery")return [head,tctx,"",
  "TASK — a mastery POOL of 20 UNSEEN questions for this topic.",
  "",
  PACK_AUDIENCE,
  "",
  "These are held out: the app keeps source \"mastery\" out of the question bank and out of mock",
  "papers, so they stay genuinely unseen until the test. They decide pass or fail, so they must",
  "be clean — no ambiguity, no two defensible answers, no trick wording.",
  "",
  "Why twenty and not ten. Each test draws ten from the pool at 3 easy / 5 moderate / 2 hard, and",
  "a retake draws again — fresh items where it can, with about a third of each band reserved for",
  "questions previously got wrong. Twenty items, tagged 6 easy / 10 moderate / 4 hard, is the",
  "smallest pool that lets a retake be mostly new while still re-testing the weak spots.",
  "",
  "They must TRANSFER rather than repeat: change the distribution, the parameterisation or the",
  "framing from whatever the lesson and the practice set used. A learner who memorised the",
  "worked examples should not pass.",
  "At least 4 numerical and at least 2 multi-statement, to clear the format floors.",
  "Spread the keys evenly across A, B, C and D — five of each across the twenty.",
  "",
  "Work every answer out in full before keying it, and state the working in the explanation.",
  "A mastery item with a wrong key does more damage than a missing topic.",
  "",
  SCHEMA_Q,"",
  "Write to  qsets/"+m.id+"_"+(t?t.id.split("-").pop():"tN")+"_mastery  with body:",
  '{ "moduleId":"'+m.id+'", "source":"mastery", "topicId":"'+(t?t.id:"")+'",',
  '  "label":"'+(t?t.name:"")+' — mastery test (unseen)", "count":20, "items":[...] }',
  'ids: "'+m.id+'-'+(t?t.id.split("-").pop():"tN")+'-m-01", -02, …',
  "The lesson's quiz scene must carry this same setId.",
  tail].join("\n");

  // validation
  return [head,tctx,"",
  "TASK — validation pass. Do not author new content.",
  "",
  "Read these documents from the artifact with the ArtifactData tool:",
  "  lessons/"+(t&&lix[t.id]?lix[t.id].id:"<lessonId>"),
  "  qsets/"+m.id+"_"+(t?t.id.split("-").pop():"tN")+"_practice",
  "  qsets/"+m.id+"_"+(t?t.id.split("-").pop():"tN")+"_mastery",
  "",
  "Check and report, as a list of findings with the document and field for each:",
  "  1. Every formula. Re-derive each one independently; do not trust the text.",
  "  2. Every answer key against its own explanation — flag any that disagree.",
  "  3. Numerical answers, recomputed from the numbers given in the stem.",
  "  4. Multi-statement items: does the keyed option match the four verdicts?",
  "  5. Notation consistency across the lesson, practice and mastery sets.",
  "  6. Ambiguity: any item where a second option is defensible.",
  "  7. Coverage: anything in the topic's required depth ("+(t?t.extent:"")+") the lesson never teaches.",
  "  8. Every reference URL — fetch it and confirm it says what the \"why\" claims.",
  "  9. Any mastery item that merely repeats a practice item rather than transferring.",
  "",
  " 10. The foundation drill: does every later scene stay inside what it checked or taught?",
  " 11. Flow diagrams: every edge between nodes that exist, no node off the grid, labels short.",
  " 12. Scenarios: any figure presented as fact — confirm it or have it rewritten qualitatively.",
  " 13. Difficulty tags: is every item tagged, and does the pool hold 6 easy / 10 moderate / 4 hard?",
  " 14. Key spread: no letter holding more than 40% of a set.",
  "",
  "Then apply only the fixes I approve. Report first, write second.",
  "A numerically correct answer can still rest on a wrong theorem condition — say so when you see it."].join("\n");
}

function importCard(url){
  return '<div class="grid g2" style="margin-bottom:12px">'+
  '<div class="card"><h3 style="margin-bottom:4px">Personal order</h3>'+
    '<p class="note" style="margin-bottom:8px">Mode C. Analyse an answer sheet outside the app, then paste the result here. It reorders the learning path without touching any content. Versioned by exam cycle; importing again replaces it.</p>'+
    '<textarea id="persBox" placeholder=\'{"cycle":"2026-06","entries":[{"moduleId":"inference","topicId":"inference-t4","priority":1,"reason":"2/17 on this module and every miss was a numerical"}]}\'>'+
      esc(S.personal?JSON.stringify(S.personal,null,1):"")+'</textarea>'+
    '<div class="row" style="margin-top:8px"><button class="btn p sm" id="persSave">Import</button>'+
      (S.personal?'<span class="chip ok">'+(S.personal.entries||[]).length+' entries · cycle '+esc(S.personal.cycle||"—")+'</span>':'<span class="chip dim">none imported</span>')+'</div></div>'+
  '<div class="card"><h3 style="margin-bottom:4px">Official syllabus order</h3>'+
    '<p class="note" style="margin-bottom:8px">Mode A. A map from module id to its unit number in the official syllabus. Until this is set, syllabus mode falls back to the catalog order and says so.</p>'+
    '<textarea id="sylBox" placeholder=\'{"cycle":"2026","order":{"maths":1,"probability":2,"inference":3}}\'>'+
      esc(S.syl?JSON.stringify(S.syl,null,1):"")+'</textarea>'+
    '<div class="row" style="margin-top:8px"><button class="btn p sm" id="sylSave">Import</button>'+
      (S.syl?'<span class="chip ok">loaded</span>':'<span class="chip dim">not set</span>')+'</div></div>'+
  '</div>';
}
function schemaCard(){
  return '<div class="card" style="margin-bottom:12px"><h3 style="margin-bottom:8px">How the store is laid out</h3>'+
    '<div class="scroll"><table class="tbl"><thead><tr><th>Path</th><th>What it holds</th><th>Written by</th></tr></thead><tbody>'+
    [["meta/catalog","modules, marks, baselines, topics and required depth","a chat, once"],
     ["meta/index","question counts per module","this page, or a chat"],
     ["meta/lessons","which topics have a lesson","this page, on rescan"],
     ["meta/app","this artifact's URL and schema version","a chat, after publishing"],
     ["meta/syllabus","official unit order (mode A)","this page, from an import"],
     ["meta/personal","your personalised order (mode C)","this page, from an import"],
     ["lessons/&lt;id&gt;","one topic's whole teaching document","a chat"],
     ["qsets/&lt;id&gt;","one batch: {moduleId, source, label, count, items[]}","a chat, append-only"],
     ["data/users/&lt;you&gt;/attempts","every question you answered","this page"],
     ["data/users/&lt;you&gt;/mastery","verified mastery per topic, with retest dates","this page"],
     ["data/users/&lt;you&gt;/topics","self-marked scenes read","this page"],
     ["data/users/&lt;you&gt;/mocks","mock results per module","this page"],
     ["data/users/&lt;you&gt;/errors","your error log","this page"],
     ["data/users/&lt;you&gt;/config","exam date, target, path mode","this page"]].map(r=>
      '<tr><td class="mono">'+r[0]+'</td><td>'+r[1]+'</td><td class="note">'+r[2]+'</td></tr>').join("")+
    '</tbody></table></div>'+
    '<p class="note" style="margin-top:8px"><b>Sharing.</b> Everything under <span class="mono">data/users/&lt;you&gt;/</span> is private per person — another viewer, and the owner too, cannot read it. So sharing this artifact shares the lessons, the question bank and the syllabus, and shares nobody\'s scores. Give someone access from the artifact\'s own Share menu; this page cannot do it.</p>'+
    '<p class="note"><b>Not built here.</b> Aggregate analytics across learners, retrieval-augmented answering over the library, and automatic symbolic checking of formulas all need a server. The validation stage above puts those checks in a chat instead, which is slower and needs you to approve the findings.</p></div>';
}
function offlineCard(ms){
  return '<div class="card"><h3 style="margin-bottom:8px">Download it</h3>'+
    '<p class="note" style="margin-bottom:8px">Export what you need as a file to print or read on paper — the page cannot open a print dialog itself.</p>'+
    (S.dl?'<div class="row"><select id="exMod"><option value="">Every module</option>'+ms.map(m=>'<option value="'+m.id+'">'+esc(m.name)+'</option>').join("")+'</select>'+
      '<select id="exWhat"><option value="wrong">Only my wrong ones</option><option value="flag">Only flagged</option><option value="unseen">Only unseen</option><option value="all">Everything</option></select>'+
      '<button class="btn p sm" id="exGo">Export as markdown</button><button class="btn sm" id="exCsv">Export as CSV</button></div>'
      :'<p class="note">Saving files is not available in this view.</p>')+'</div>';
}

function genPanel(){
  const g=S.gen;if(!g)return"";
  const done=!g.running&&g.out;
  return '<div class="genbox">'+
    '<div class="row tight" style="justify-content:space-between;margin-bottom:8px">'+
      '<span class="lbl">'+esc(g.phase||"Authoring")+'</span>'+
      (g.running?'<span class="chip ac">working…</span>':g.saved?'<span class="chip ok">saved</span>':
        g.out?'<span class="chip mid">review before saving</span>':'<span class="chip bad">stopped</span>')+'</div>'+
    bar(g.pct||0,g.saved?"ok":g.running?"ac":"och")+
    '<div class="genlog">'+g.log.map(l=>'<div class="gl '+l.state+'">'+
      '<span class="gi">'+(l.state==="bad"?"✗":l.state==="warn"?"!":"✓")+'</span>'+esc(l.msg)+'</div>').join("")+'</div>'+
    (done?
      '<div class="sep"></div>'+
      '<div class="kv"><span class="lbl">Will be written to</span><b class="mono">'+esc(g.out.path)+'</b></div>'+
      '<p class="note">'+esc(g.out.summary)+'</p>'+
      (g.errs&&g.errs.length?
        '<div class="expl bad" style="margin:10px 0"><h4>'+g.errs.length+' thing'+(g.errs.length>1?"s":"")+' to look at</h4>'+
        '<ul style="margin:4px 0 0;padding-left:18px">'+g.errs.slice(0,8).map(e=>'<li>'+esc(e)+'</li>').join("")+
        (g.errs.length>8?'<li>…and '+(g.errs.length-8)+' more</li>':"")+'</ul></div>'
        :'<p class="note" style="color:var(--ok)">Passed every schema check.</p>')+
      (g.out.kind==="lesson"?'<p class="note" style="color:var(--ochre);margin-top:6px">References were not link-checked — this page cannot fetch them. Open each one before you trust it, or run the validation stage in a chat.</p>':"")+
      '<div class="row" style="margin-top:10px">'+
        (g.saved?'<button class="btn" data-jump="learn" data-mid="'+esc(g.topic)+'">Open it in Learn</button>'
          :'<button class="btn p sm" id="genSave"'+(g.saving?" disabled":"")+'>'+(g.saving?"Saving…":"Save to the store")+'</button>')+
        '<button class="btn sm" id="genPreview">'+(g.showJson?"Hide":"Show")+' the JSON</button>'+
        '<button class="btn sm" id="genDrop">Discard</button>'+
      '</div>'+
      (g.showJson?'<textarea readonly style="min-height:200px;margin-top:8px">'+esc(JSON.stringify(g.out.body,null,1))+'</textarea>':"")
      :"")+
  '</div>';
}
function usersCard(){
  const us=S.users||[];
  return '<div class="card" style="margin-bottom:12px"><h3 style="margin-bottom:4px">Test profiles</h3>'+
    '<p class="note" style="margin-bottom:8px">Each profile keeps its own answers, scores and mastery, under your private area of the store. '+
    'Lessons and the question bank are shared by all of them. Use one to hand someone the app without mixing their answers into yours — '+
    'and note the passcode is a convenience, not a lock: it is stored alongside the app, so anyone who can open this link can open any profile.</p>'+
    (us.length?'<div class="scroll"><table class="tbl"><thead><tr><th>Name</th><th>id</th><th>Passcode</th><th>Shown as</th></tr></thead><tbody>'+
      us.map(u=>'<tr><td>'+esc(u.name||u.id)+'</td><td class="mono">'+esc(u.id)+'</td>'+
        '<td class="mono">'+esc(u.pass?String(u.pass):"none")+'</td><td class="note">'+esc(u.note||"")+'</td></tr>').join("")+
      '</tbody></table></div>':'<p class="note">None yet.</p>')+
    '<label class="fl" style="margin-top:10px">Profiles, as JSON</label>'+
    '<textarea id="usersBox" style="min-height:120px">'+esc(JSON.stringify({users:us.length?us:[
      {id:"demo",name:"Test learner",pass:"1234",note:"A clean slate for trying the app",hint:"four ones... no, 1234"}]},null,1))+'</textarea>'+
    '<div class="row" style="margin-top:8px"><button class="btn p sm" id="usersSave">Save profiles</button>'+
      '<span class="note">Writes <span class="mono">meta/users</span>.</span></div></div>';
}

/* ---------- diagnostics ---------- */
async function runDiag(){
  const out=[],t0=Date.now();
  const cap=(n)=>{try{return !!({db:S.db,user:S.user,sample:S.sampleFn,downloads:S.dl}[n])}catch(e){return false}};
  out.push(["runtime","claude.use available",typeof claude!=="undefined"&&!!(claude&&claude.use)]);
  ["db","user","sample","downloads"].forEach(n=>out.push(["capability",n,cap(n)]));
  out.push(["identity","your private id",!!S.uid,S.uid?"present":"absent — per-person progress cannot be saved"]);
  if(!S.db){S.diag={rows:out,ms:0,at:new Date().toISOString()};render();return}
  const doc=async p=>{try{const s=await S.db.doc(p).get();
    if(!s.exists)return[false,"not found"];
    const d=s.data()||{};const n=JSON.stringify(d).length;
    return[true,n+" bytes"+(d.scenes?", "+d.scenes.length+" scenes":"")+(d.items?", "+d.items.length+" items":"")+(d.modules?", "+(d.modules.length||Object.keys(d.modules).length)+" modules":"")]}
    catch(e){return[false,"read failed: "+(e&&e.code||"error")]}};
  const coll=async p=>{try{const q=await S.db.collection(p).get();
    return[q.size>0,q.size+" document"+(q.size===1?"":"s")+(q.size?": "+q.docs.map(d=>d.id).slice(0,6).join(", ")+(q.size>6?" …":""):"")]}
    catch(e){return[false,"read failed: "+(e&&e.code||"error")]}};
  for(const p of ["meta/catalog","meta/index","meta/lessons","meta/app"]){
    const r=await doc(p);out.push(["document",p,r[0],r[1]])}
  for(const p of ["lessons","qsets"]){const r=await coll(p);out.push(["collection",p,r[0],r[1]])}
  // every lesson the index names must actually resolve
  const ix=(S.lessonIdx&&S.lessonIdx.topics)||{};
  const tids={};mods().forEach(m=>m.topics.forEach(t=>{tids[t.id]=m.name}));
  for(const tid of Object.keys(ix)){
    const r=await doc("lessons/"+ix[tid].id);
    out.push(["lesson",tid+" → lessons/"+ix[tid].id,r[0]&&!!tids[tid],
      (r[0]?r[1]:r[1])+(tids[tid]?"":" · WARNING: this topic id is not in the catalog, so the tree can never show it")]);
    const sc=S.lessons[tid];
    const setId=(r[0]&&sc&&sc.scenes?(sc.scenes.filter(x=>x.kind==="quiz")[0]||{}).setId:null);
    if(setId){const m=await doc("qsets/"+setId);
      out.push(["mastery set",setId,m[0],m[1]])}
  }
  S.diag={rows:out,ms:Date.now()-t0,at:new Date().toISOString()};render();
}
function diagCard(){
  const d=S.diag;
  return '<div class="card" style="margin-bottom:12px"><div class="row tight" style="justify-content:space-between;margin-bottom:6px">'+
    '<h3>Diagnostics</h3><button class="btn sm" id="diagRun">'+(d?"Run again":"Run checks")+'</button></div>'+
    '<p class="note" style="margin-bottom:8px">Reads every path the app depends on and reports what came back. Run this first when something is missing, and send me the result rather than a description.</p>'+
    (d?'<div class="scroll"><table class="tbl"><thead><tr><th></th><th>What</th><th>Path or name</th><th>Result</th></tr></thead><tbody>'+
      d.rows.map(r=>'<tr><td><span class="chip '+(r[2]?"ok":"bad")+'">'+(r[2]?"✓":"✗")+'</span></td>'+
        '<td class="note">'+esc(r[0])+'</td><td class="mono">'+esc(r[1])+'</td><td class="note">'+esc(r[3]!==undefined?r[3]:(r[2]?"ok":"missing"))+'</td></tr>').join("")+
      '</tbody></table></div>'+
      '<p class="note" style="margin-top:8px">'+d.rows.filter(r=>!r[2]).length+' of '+d.rows.length+' checks failed · '+d.ms+'ms · '+esc(d.at.slice(0,19).replace("T"," "))+'</p>'+
      (S.dl?'<button class="btn sm" id="diagCopy" style="margin-top:6px">Copy the result</button>':"")
     :'<p class="note">Not run yet.</p>')+
  '</div>';
}

/* What the learner asked Claude, newest first. The point of keeping these is not the
   answers — it is the pattern. A topic that generates many questions, or any question
   whose answer was marked unhelpful, is a topic whose written content is too thin. */
function askPanel(){
  const all=fbRows("asks");
  const rs=all.slice().sort((a,b)=>(b.ts||0)-(a.ts||0));
  const IN={};ASKINTENT.forEach(x=>{IN[x[0]]=x[1]});
  // rank topics by how much help they needed
  const byTopic={};
  all.forEach(r=>{const k=r.topicId||"general";
    const o=byTopic[k]||(byTopic[k]={id:k,name:r.topic||k,n:0,bad:0,basics:0});
    o.n++;if(r.helpful===false)o.bad++;if(r.intent==="basics")o.basics++});
  const hot=Object.keys(byTopic).map(k=>byTopic[k]).sort((a,b)=>(b.bad-a.bad)||(b.n-a.n)).slice(0,8);
  const flagged=all.filter(r=>r.helpful===false).length;
  return '<div class="card" style="margin-bottom:12px">'+
    '<div class="row tight" style="justify-content:space-between;margin-bottom:8px">'+
      '<h3 style="margin:0">Questions asked of Claude</h3>'+
      '<span class="chip '+(rs.length?"ac":"dim")+' num">'+rs.length+'</span>'+
      (S.isAdmin?'<span class="chip och num" title="Learners who have asked something">'+
        fbLearners("asks")+' learner'+(fbLearners("asks")===1?"":"s")+'</span>':"")+
      (flagged?'<span class="chip bad num" title="Answers marked not helpful">'+flagged+' flagged</span>':"")+
    '</div>'+
    (rs.length
      ? '<p class="note" style="margin-bottom:10px">Where the learner had to ask is where the written content did '+
          'not do its job. Topics are ranked by answers marked unhelpful first, then by how often help was needed.</p>'+
        '<div class="asktop">'+hot.map(t=>
          '<span class="chip '+(t.bad?"bad":t.basics?"och":"dim")+'" title="'+esc(t.name)+'">'+
            esc((topNo(t.id)?topNo(t.id)+" ":"")+String(t.name).slice(0,34))+' · '+t.n+
            (t.bad?" ("+t.bad+" flagged)":"")+'</span>').join("")+'</div>'+
        '<div class="asklist">'+rs.slice(0,80).map((r,i)=>
          '<div class="askrow">'+
            '<span class="chip '+(r.helpful===false?"bad":r.intent==="basics"?"och":"dim")+'">'+
              esc(IN[r.intent]||r.intent)+'</span>'+
            '<div class="akb">'+
              '<b>'+esc((topNo(r.topicId)?topNo(r.topicId)+" ":"")+(r.topic||"general"))+
                (r.scene?' · '+esc(r.scene):"")+'</b>'+
              (r.sel?'<div class="akq">selected: “'+esc(String(r.sel).slice(0,180))+'”</div>':"")+
              (r.q?'<div class="akq">asked: '+esc(String(r.q).slice(0,180))+'</div>':"")+
              (r.a?'<div class="aka">'+esc(String(r.a).slice(0,260))+'…</div>':"")+
              '<div class="note num">'+(S.isAdmin?esc(fbWho(r))+' · ':"")+
                new Date(r.ts||0).toISOString().slice(0,16).replace("T"," ")+
                (r.qId?' · '+esc(r.qId):"")+
                (r.helpful===false?' · marked not helpful':r.helpful===true?' · helpful':"")+
                (r.profile&&r.profile!=="me"?' · '+esc(r.profile):"")+'</div></div>'+
            '<button class="btn sm gh" data-askdel="'+i+'" title="Remove">\u2715</button>'+
          '</div>').join("")+'</div>'+
        '<div class="row" style="margin-top:10px">'+
          '<button class="btn sm" id="askCopy">Copy as a content brief</button>'+
          (S.dl?'<button class="btn sm" id="askSave">Save as a file</button>':"")+'</div>'
      : '<p class="note">Nothing asked yet. Select any text anywhere in the app \u2014 a lesson, a question, a mock \u2014 '+
        'and an \u201cAsk Claude\u201d chip appears; Ctrl\u2011K (Cmd\u2011K) opens the same panel without a selection. '+
        'Everything asked lands here.</p>')+
  '</div>';
}
/* A brief an authoring chat can act on: grouped by topic, worst first. */
function askBrief(){
  const all=fbRows("asks");
  if(!all.length)return "No questions asked yet.";
  const g={};
  all.forEach(r=>{const k=r.topicId||"general";(g[k]=g[k]||{name:r.topic||k,rows:[]}).rows.push(r)});
  const keys=Object.keys(g).sort((a,b)=>
    (g[b].rows.filter(r=>r.helpful===false).length-g[a].rows.filter(r=>r.helpful===false).length)||
    (g[b].rows.length-g[a].rows.length));
  const L=["Content gaps, inferred from what the learner had to ask Claude.",
    "Ranked by answers marked unhelpful, then by volume. "+all.length+" questions in total.",""];
  keys.forEach(k=>{
    const o=g[k],bad=o.rows.filter(r=>r.helpful===false).length;
    L.push("## "+(topNo(k)?topNo(k)+" ":"")+o.name+"  ("+o.rows.length+" asked"+(bad?", "+bad+" answers unhelpful":"")+")");
    o.rows.slice(0,12).forEach(r=>{
      L.push("- ["+r.intent+(r.scene?" · "+r.scene:"")+"] "+
        (r.sel?'selected "'+String(r.sel).slice(0,120)+'"':"")+
        (r.q?(r.sel?" — ":"")+String(r.q).slice(0,160):"")+
        (r.helpful===false?"   <-- answer marked unhelpful":""));
    });
    L.push("");
  });
  L.push("For each heading: decide whether the lesson should already have answered this.");
  L.push("If it should, say which scene to extend and how. If the question is outside the syllabus, say so.");
  return L.join("\n");
}
