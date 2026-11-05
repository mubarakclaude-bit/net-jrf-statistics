#!/usr/bin/env python3
# Rewrite the content-factory prompts and validators in src/62-gen.js so that
# anything authored from any chat carries every feature added since the first
# lessons: foundation drills for a returning candidate, flow diagrams, real-world
# scenarios, memory aids for the right rail, weightage, difficulty bands and
# twenty-item mastery pools.
import io, re, sys

P = "src/62-gen.js"
s = io.open(P, encoding="utf-8").read()
orig = s

def cut(start, end):
    """Return the span from the line beginning with start up to the line beginning with end."""
    a = s.index(start)
    b = s.index(end, a)
    return s[a:b]

# ---------------------------------------------------------------- audience note
AUD = '''const AUDIENCE = [
  "WHO THIS IS FOR. Most candidates return to NET preparation after a break of two or three years:",
  "a job, a teaching post, a family. The statistics was learnt once, properly, and has gone quiet —",
  "they have not written a likelihood since their MSc. So pitch from the base upward:",
  "- Open every idea in plain words and a concrete case before any symbol appears.",
  "- Name the second-year tool you are about to use, the first time you use it ('the factorisation",
  "  theorem — splitting the joint density into a θ-part and a data-part').",
  "- Never write 'clearly', 'obviously', 'recall that' or 'as we know'. If a step needs recalling,",
  "  spend the line and recall it for them.",
  "- Carry every algebraic step. The gap, not the difficulty, is what makes a derivation unreadable.",
  "- Write prose a tired adult reads at five in the morning: short sentences, no filler, no cheer."
].join("\\n");
'''

# ------------------------------------------------------------------- validators
VPLAN = '''function vLessonPlan(p){
  const e=[];
  if(!p||typeof p!=="object")return["The plan was not an object."];
  ["title","objectives","prereq","refs","revision","traps","scenePlan"].forEach(k=>{
    if(!p[k])e.push("plan is missing "+k)});
  if(p.objectives&&p.objectives.length<4)e.push("fewer than 4 objectives");
  if((p.prereq||[]).length<3)e.push("fewer than 3 prerequisites — the foundation drill is built from these");
  const sp=p.scenePlan||[];
  if(sp.length<11||sp.length>16)e.push("scene plan has "+sp.length+" scenes, wanted 11-16");
  const kinds=sp.map(s=>s.kind);
  if(kinds[0]!=="foundation")e.push("the first scene must be the foundation drill");
  ["foundation","intuition","theory","worked","guided","trapcheck","summary","quiz"].forEach(k=>{
    if(kinds.indexOf(k)<0)e.push("no "+k+" scene in the plan")});
  if(kinds.filter(k=>k==="guided").length<2)e.push("needs at least two guided scenes, the last one a transfer case");
  if(!sp.filter(s=>s.flow).length)e.push("no scene carries a flow diagram — at least one must");
  if(sp.filter(s=>s.scenario).length<2)e.push("fewer than 2 scenes carry a real-world scenario");
  sp.forEach((s,i)=>{if(!s.kind||!s.title)e.push("scene "+(i+1)+" has no kind or title");
    if(s.kind==="explore"&&s.viz&&VIZ_OK.indexOf(s.viz.type||s.viz)<0)
      e.push("scene "+(i+1)+" asks for a visual this app does not have: "+(s.viz.type||s.viz))});
  if(p.revision){
    if((p.revision.sheet||[]).length<8)e.push("revision sheet has fewer than 8 lines");
    if((p.revision.cards||[]).length<6)e.push("fewer than 6 flashcards");
    if((p.revision.tricks||[]).length<3)e.push("fewer than 3 mnemonics for the memory-aids rail");
    if((p.revision.shortcuts||[]).length<3)e.push("fewer than 3 shortcuts for the memory-aids rail");
    if((p.revision.remember||[]).length<2)e.push("fewer than 2 'if you remember nothing else' lines");
    (p.revision.cards||[]).forEach((c,i)=>{if(!Array.isArray(c)||c.length!==2)
      e.push("flashcard "+(i+1)+" is not a [front, back] pair")});
  }
  return e;
}
'''

VSCENE = '''function vScene(s,i){
  const e=[],at="scene "+(i+1)+" ("+(s&&s.kind||"?")+")";
  if(!s||!s.kind)return [at+" has no kind"];
  if(!s.title)e.push(at+" has no title");
  const need={foundation:["body","items"],intuition:["body"],explore:["body","viz"],theory:["blocks"],
    worked:["problem","steps"],recall:["intro","items"],completion:["problem","steps"],
    guided:["problem","hints","solution","answer"],trapcheck:["intro","items"],summary:["body"],quiz:["setId"]}[s.kind];
  if(!need)return [at+" is not a kind this app renders"];
  need.forEach(f=>{if(!s[f])e.push(at+" is missing "+f)});
  if(s.kind==="explore"&&s.viz&&VIZ_OK.indexOf(s.viz.type)<0)
    e.push(at+" uses an unknown visual: "+s.viz.type);
  if(s.kind==="foundation"){
    const it=s.items||[];
    if(it.length<3||it.length>5)e.push(at+" has "+it.length+" prerequisite checks, wanted 3-5");
    it.forEach((x,k)=>{
      if(!x.ask)e.push(at+" check "+(k+1)+" has no question");
      if(!x.recall)e.push(at+" check "+(k+1)+" has no one-line answer");
      if(!x.refresh)e.push(at+" check "+(k+1)+" has no rebuild for a learner who marks it shaky");
      if(x.refresh&&(Array.isArray(x.refresh)?x.refresh:[x.refresh]).join(" ").length<200)
        e.push(at+" check "+(k+1)+" has a rebuild too thin to teach from")});
  }
  if(s.kind==="guided"&&(s.hints||[]).length!==3)
    e.push(at+" has "+(s.hints||[]).length+" hints, the ladder is exactly 3");
  if(s.kind==="worked"&&(s.steps||[]).some(x=>!x.say||!x.math||!x.why))
    e.push(at+" has a step missing say, math or why");
  if(s.kind==="completion"){
    const bl=(s.steps||[]).filter(x=>x.blank);
    if(!bl.length)e.push(at+" has no blanks to fill");
    bl.forEach(x=>{if(!x.blank.answer||!x.blank.prompt)e.push(at+" has a blank with no prompt or answer");
      if(!x.blank.hint)e.push(at+" has a blank with no hint")});
  }
  if(s.kind==="trapcheck"&&(s.items||[]).some(x=>typeof x.tf!=="boolean"||!x.why))
    e.push(at+" has an item with no true/false verdict or no reason");
  if(s.kind==="recall"&&(s.items||[]).some(x=>!x.q||!x.a))e.push(at+" has an incomplete recall item");
  if(s.flow){
    const n=(s.flow.nodes||[]),ed=(s.flow.edges||[]),ids={};
    if(n.length<3)e.push(at+" has a flow diagram with fewer than 3 nodes");
    n.forEach((x,k)=>{if(!x.id||x.r==null||x.c==null)e.push(at+" flow node "+(k+1)+" needs id, r and c");
      if(ids[x.id])e.push(at+" flow has two nodes called "+x.id);ids[x.id]=1;
      if(!x.label)e.push(at+" flow node "+x.id+" has no label")});
    if(!ed.length)e.push(at+" has a flow diagram with no edges");
    ed.forEach(x=>{if(!ids[x.from]||!ids[x.to])e.push(at+" flow edge "+x.from+"->"+x.to+" names a node that does not exist")});
  }
  if(s.scenario){
    const sn=s.scenario;
    if(!sn.teaser)e.push(at+" scenario has no teaser for the closed state");
    if(!sn.title)e.push(at+" scenario has no title");
    if((sn.body||[]).join(" ").length<400)e.push(at+" scenario is too thin to be worth opening");
  }
  return e;
}
'''

VQSET = '''function vQset(q,want){
  const e=[];
  if(!q||!Array.isArray(q.items))return["No items array came back."];
  if(q.items.length<Math.min(8,want))e.push("only "+q.items.length+" questions, asked for "+want);
  const ids={},keys={},diffs={};
  q.items.forEach((it,i)=>{
    const at="q"+(i+1);
    if(!it.id)e.push(at+" has no id"); else if(ids[it.id])e.push("duplicate id "+it.id); else ids[it.id]=1;
    if(!it.stem)e.push(at+" has no stem");
    if(!it.explanation||String(it.explanation).length<40)e.push(at+" has no real explanation");
    if(["easy","moderate","hard"].indexOf(it.diff)<0)
      e.push(at+' has diff '+JSON.stringify(it.diff)+', needs "easy", "moderate" or "hard"');
    else diffs[it.diff]=(diffs[it.diff]||0)+1;
    const free=!((it.options||[]).length);
    if(q.source==="mastery"&&free)e.push(at+" is write-in; a mastery test has to be machine-scored");
    if(!free){
      if(it.options.length!==4)e.push(at+" has "+it.options.length+" options, needs 4");
      if("ABCD".indexOf(it.answer)<0)e.push(at+" answer is "+JSON.stringify(it.answer)+", needs A-D");
      else keys[it.answer]=(keys[it.answer]||0)+1;
      if((it.options||[]).some(o=>/^[A-D][).]\\s/.test(String(o))))e.push(at+" options carry their own letters");
    }
    if(it.format==="multi"){
      if((it.statements||[]).length!==4)e.push(at+" needs 4 statements");
      const v=it.verdicts||{};
      if(["A","B","C","D"].some(L=>!v[L]||typeof v[L].tf!=="boolean"||!v[L].why))
        e.push(at+" needs a true/false verdict and a reason for all four statements");
    }
    if(it.format==="numeric"&&!it.check)e.push(at+" is numerical with no terminal-check line");
    if(it.format==="match"&&(it.pairs||[]).length!==4)e.push(at+" needs 4 List I/List II pairs");
    if(it.format==="order"&&(it.items||[]).length!==4)e.push(at+" needs 4 steps to order");
  });
  const fm={};q.items.forEach(i=>fm[i.format]=(fm[i.format]||0)+1);
  // a pool whose keys pile onto one letter rewards a guesser, so check the spread
  const n=q.items.length,cap=Math.ceil(n*0.4);
  Object.keys(keys).forEach(L=>{if(keys[L]>cap)
    e.push(keys[L]+" of "+n+" answers are "+L+" — spread the keys across A to D")});
  if(q.source==="mastery"){
    if(n<20)e.push("a mastery pool is 20 items so that each retake can draw a fresh ten; got "+n);
    if((fm.numeric||0)<4)e.push("only "+(fm.numeric||0)+" numerical items; the 70% floor needs at least 4");
    if((fm.multi||0)<2)e.push("only "+(fm.multi||0)+" multi-statement items; the floor needs at least 2");
    // every draw holds 3 easy / 5 moderate / 2 hard, so the pool needs double of each
    [["easy",6],["moderate",10],["hard",4]].forEach(([d,k])=>{
      if((diffs[d]||0)<k)e.push("only "+(diffs[d]||0)+" "+d+" items; a 3/5/2 draw from 20 needs at least "+k)});
  }
  return e;
}
'''

# ------------------------------------------------------------------ the prompts
PROMPTS = '''/* ---- prompts ---- */
function genCtx(m,t){
  return ["Module: "+m.id+" — "+m.name+" ("+m.marks+" of "+(m.paper===2?200:100)+" marks, Paper "+m.paper+")",
   "The candidate scored "+m.baseline+" on this module in June 2026. Their marks are lost on verification,",
   "not on method: right working reported as the wrong quantity, dropped terms, wrong degrees of freedom.",
   t?("Topic: "+t.id+" — "+t.name):"",
   t?("Required depth: "+t.extent+" — "+EXT[t.extent].d+"."):"",
   t&&t.imp?("Exam weight: "+IMP[t.imp].s+" "+IMP[t.imp].n+" — "+IMP[t.imp].d+
             (t.qs?(". About "+t.qs+" question"+(t.qs>1?"s":"")+" a paper, "+(t.marks||t.qs*2)+" marks."):"")):"",
   "","Weight decides depth, not tone: a two-star topic still gets a full lesson, but the heavy ones",
   "earn more worked examples and more transfer practice.","",AUDIENCE].filter(Boolean).join("\\n");
}
function pPlan(m,t){
  return ["You are authoring a lesson for a UGC NET Statistics JRF learning app. Return JSON ONLY — no prose, no code fence.",
  "",genCtx(m,t),"",
  "Produce the PLAN for the lesson, not its content. JSON shape:",
  '{"title","breadcrumb","estMin",',
  ' "objectives":[4-6 strings, each something the learner can DO],',
  ' "prereq":[{"id","name","why"} x3-4 — these become the opening foundation drill],',
  ' "refs":[{"title","where","site","url","type","free":true,"why"}],',
  ' "revision":{"sheet":[8-12 one-line facts],"cards":[[front,back] x8],',
  '   "tricks":[{"hook","why"} x3-4],"shortcuts":[3-4 strings],"remember":[2-3 strings],"traps":[3-5 strings]},',
  ' "traps":[5-8 strings],',
  ' "scenePlan":[{"id":"s1","kind","title","objective","mins",',
  '    "viz":{"type",...} only on explore, "flow":true where a diagram is planned, "scenario":true where one is]}',
  "",
  "scenePlan must be 11-16 scenes and must OPEN with the foundation drill:",
  "  foundation → intuition → explore → theory → worked → recall → completion → theory → explore",
  "  → guided → trapcheck → guided (TRANSFER: a case the lesson has not shown) → summary → quiz",
  "The foundation scene is the returning candidate's way in: it checks the 3-4 prereq items above,",
  "and nothing later in the lesson may assume anything that is not either checked there or taught here.",
  "",
  "Mark \\"flow\\":true on at least one scene — a decision procedure, a derivation route or a",
  "classification worth drawing rather than describing. Mark \\"scenario\\":true on at least two:",
  "a real use of the idea, from industry, government statistics, medicine or research practice.",
  "",
  "Use an explore scene only where one of these three visuals genuinely fits the maths:",
  '  "exp-likelihood" (likelihood of an exponential sample; shows the data entering only through n and Σx)',
  '  "mle-sampling"   (exact sampling distribution of n/ΣX; shows bias dying as n grows)',
  '  "unif-likelihood"(likelihood for U(0,θ); a cliff at the sample maximum, derivative never zero)',
  "If none of the three fits this topic, use fewer explore scenes rather than forcing one.",
  "The quiz scene carries \\"setId\\":\\""+m.id+"_"+(t?t.id.split("-").pop():"tN")+"_mastery\\".",
  "",
  "REFERENCES: only cite pages you are confident exist at a stable URL, naming the exact lesson,",
  "chapter or lecture number. Two or three. If you are unsure a URL resolves, leave it out —",
  "they will be shown to the learner marked as unverified, because this page cannot check them."].join("\\n");
}
function pScenes(m,t,plan,batch){
  return ["You are writing scenes for a UGC NET Statistics JRF lesson. Return JSON ONLY — no prose, no code fence.",
  "",genCtx(m,t),"",
  "Lesson title: "+plan.title,
  "Objectives: "+(plan.objectives||[]).join(" | "),
  "Prerequisites the foundation drill checks: "+(plan.prereq||[]).map(p=>p.name).join(" | "),
  "Full scene plan, for consistency of notation and so you do not repeat yourself:",
  (plan.scenePlan||[]).map((s,i)=>"  "+(i+1)+". ["+s.kind+"] "+s.title+" — "+(s.objective||"")).join("\\n"),
  "",
  "WRITE ONLY these scenes, in full: "+batch.map(b=>b.i+1).join(", "),
  "Return {\\"scenes\\":[ ... ]} with one object per scene, in that order, each carrying its \\"id\\".",
  "",
  "Shapes:",
  ' foundation {"id","kind","title","mins","objective","body":[2-3 paragraphs saying why this check exists],',
  '             "items":[{"ask","recall","refresh":[2-3 paragraphs]} x3-5]}',
  ' intuition  {"id","kind","title","mins","objective","body":[paragraphs],"aside":{"h","body"},"ask":{"q","nudge"}}',
  ' explore    {"id","kind","title","mins","objective","body":[paragraphs],"viz":{...from the plan},"ask":{"q","nudge"}}',
  ' theory     {"id","kind","title","mins","objective","blocks":[{"t":"def"|"formula"|"step"|"assume"|"note"|"trap","h","body"}]}',
  ' worked     {"id","kind","title","mins","objective","problem","steps":[{"say","math","why"}],"after"}',
  ' recall     {"id","kind","title","mins","objective","intro","items":[{"q","a"}]}',
  ' completion {"id","kind","title","mins","objective","problem","steps":[{"say","math","why"} or',
  '             {"say","blank":{"prompt","answer","accept":[3-5 spellings a learner might type],"hint"},"why"}],"after"}',
  ' guided     {"id","kind","title","mins","objective","problem","hints":[direction,method,next-step],',
  '             "solution":[{"say","math"}],"answer","check"}',
  ' trapcheck  {"id","kind","title","mins","objective","intro","items":[{"claim","tf":true|false,"why"}]}',
  ' summary    {"id","kind","title","mins","objective","body":[strings]}',
  ' quiz       {"id","kind","title","mins","objective","setId"}',
  "",
  "Any scene the plan marked \\"flow\\":true also carries a diagram, laid out on an explicit grid:",
  '  "flow":{"caption","nodes":[{"id","r":row from 0,"c":column from 0,"w":columns wide (optional),',
  '          "label","kind":"start"|"step"|"decision"|"end"|"note"}],',
  '          "edges":[{"from","to","label" (optional, short),"side":"l"|"r" (optional)}]}',
  "  Keep it to 4-8 nodes, at most 4 columns, every edge between nodes that exist. No library is used:",
  "  the grid you give is the layout, so place nodes so that edges run down or across, not diagonally.",
  "",
  "Any scene the plan marked \\"scenario\\":true also carries a real-world case, collapsed until opened:",
  '  "scenario":{"teaser":"one line naming the situation","title","body":[3-5 paragraphs],',
  '              "flow":{...} (optional),"close":"what the idea bought them, in one sentence"}',
  "  Use a real setting with real quantities — reliability testing, crop trials, clinical monitoring,",
  "  insurance claims, official surveys. No invented statistics presented as historical fact: if you",
  "  do not know the real figures, describe the situation qualitatively instead.",
  "",
  "Rules that matter:",
  "- A foundation item is a prerequisite CHECK, not a lesson: ask names the tool, recall is the",
  "  one-line answer, refresh rebuilds it from the base with one small worked instance.",
  "- Every worked step needs all three of say, math and why. The why is the teaching.",
  "- A hint ladder is exactly three rungs and never gives the answer away.",
  "- A completion blank needs a hint and several accepted spellings, because the learner types it.",
  "- A trapcheck item needs a boolean tf and a reason.",
  "- Plain text for maths (Σxᵢ, θ̂, ∂ℓ/∂θ). No LaTeX, no markdown, no backslashes.",
  "- Check every number you write. A wrong critical value or a dropped factor of 2 teaches the error."].join("\\n");
}
function pQuestions(m,t,kind,n,avoid){
  const mastery=kind==="mastery";
  return ["You are writing questions for a UGC NET Statistics JRF app. Return JSON ONLY — no prose, no code fence.",
  "",genCtx(m,t),"",
  "Write "+n+" questions. Return {\\"items\\":[ ... ]}.",
  mastery?("These are a HELD-OUT MASTERY POOL of "+n+": unseen, decisive, machine-scored. Every item MUST be "+
    "multiple choice with exactly 4 options — no write-in. They must TRANSFER: change the distribution, "+
    "parameterisation or framing so that memorising worked examples does not pass. At least 4 numerical "+
    "and at least 2 multi-statement.")
         :("These are PRACTICE, browsable in the question bank. Match the real paper's mix: "+FORDER.map(k=>FMT[k].mix+"% "+FMT[k].n.toLowerCase()).join(", ")+". Include 2 write-in numericals with \\"options\\":[] so there is nothing to back-solve from."),
  "",
  'DIFFICULTY. Every item carries "diff":"easy"|"moderate"|"hard", on the real paper\\'s own scale:',
  "  easy     — one definition or one step, answerable from recall in under a minute.",
  "  moderate — two or three steps, or one step plus a verification.",
  "  hard     — a transfer case, a boundary condition, or an answer that needs a trap avoided.",
  mastery?("The app draws each test as 3 easy, 5 moderate, 2 hard, and a retake draws again from this pool, "+
           "so write "+Math.round(n*0.3)+" easy, "+Math.round(n*0.5)+" moderate and "+Math.round(n*0.2)+" hard.")
         :"Aim for roughly 3 easy to 5 moderate to 2 hard.",
  "Spread the correct answers evenly across A, B, C and D. A pool keyed mostly to one letter",
  "hands marks to a candidate who guesses that letter throughout.",
  "",
  "Item shapes — \\"format\\" decides which:",
  ' single  {"id","format":"single","topic","diff","stem","options":[4],"answer":"A".."D","explanation"}',
  ' numeric {"id","format":"numeric","topic","diff","stem","options":[4],"answer","explanation","check"}',
  ' multi   {"id","format":"multi","topic","diff","stem","statements":[4],"options":[4],"answer",',
  '          "verdicts":{"A":{"tf":true,"why"},"B":{...},"C":{...},"D":{...}},"explanation"}',
  ' match   {"id","format":"match","topic","diff","stem","pairs":[[ListI,ListII] x4],"options":[4],"answer","explanation"}',
  ' order   {"id","format":"order","topic","diff","stem","items":[4 steps],"options":[4],"answer","explanation"}',
  "",
  'ids: "'+m.id+"-"+(t?t.id.split("-").pop():"tN")+"-"+(mastery?"m":"p")+'-01", -02, …',
  'topic: "'+(t?t.id:"")+'"',
  "- options are four plain strings with NO \\"A)\\" prefix; the app adds the letters.",
  "- every numerical item needs \\"check\\": the quantity actually asked, and the one verification that catches the usual slip.",
  "- every multi item needs a verdict AND a reason for all four statements, and the keyed option must agree with them.",
  "- an explanation that merely restates the answer is a failed question. Say why the distractors are wrong.",
  "- an explanation is written for someone returning after years away: name the result it rests on.",
  "- work every number out before you key it. An item with a wrong key is worse than no item.",
  avoid?("- Do NOT reuse these stems: "+avoid):""].filter(Boolean).join("\\n");
}
'''

# ------------------------------------------------------------------- splice it in
s = s.replace(cut("function vLessonPlan(p){", "function vScene(s,i){"), VPLAN)
s = s.replace(cut("function vScene(s,i){", "function vQset(q,want){"), VSCENE)
s = s.replace(cut("function vQset(q,want){", "/* ---- prompts ---- */"), VQSET)
s = s.replace(cut("/* ---- prompts ---- */", "/* ---- the job runner ---- */"), PROMPTS)

# the audience block sits above the validators, next to VIZ_OK
s = s.replace('const VIZ_OK = ["exp-likelihood","mle-sampling","unif-likelihood"];',
               'const VIZ_OK = ["exp-likelihood","mle-sampling","unif-likelihood"];\n' + AUD)

# a mastery pool is twenty items now, and the saved lesson carries the draw policy
s = s.replace('  const n=stage==="mastery"?10:15;', '  const n=stage==="mastery"?20:15;')
s = s.replace('''    mastery:{minQ:10,pass:80,fmtMin:{numeric:70,multi:70},noHints:true,retestDays:7,
      note:"Platform settings, not an NTA rule."},''',
'''    mastery:{minQ:10,pass:80,draw:10,fmtMin:{numeric:70,multi:70},
      diffMix:{easy:3,moderate:5,hard:2},noHints:true,retestDays:7,
      note:"Platform settings, not an NTA rule. Ten drawn from the pool at 3 easy / 5 moderate / 2 hard; "+
           "a retake draws again, holding the mix and pulling back items previously got wrong."},''')

if s == orig:
    sys.exit("nothing changed — the anchors did not match")
io.open(P, "w", encoding="utf-8").write(s)
print("62-gen.js rewritten: %d -> %d bytes" % (len(orig), len(s)))
