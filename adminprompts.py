#!/usr/bin/env python3
# The Admin tab's copy-out prompt packs are how content gets authored from another
# chat. Bring them up to what the app now renders: a returning candidate's foundation
# drill, flow diagrams, real-world scenarios, memory aids in the right rail, exam
# weightage, difficulty bands, and 20-item mastery pools.
import io, sys

P = "src/60-admin.js"
s = io.open(P, encoding="utf-8").read()
orig = s

def span(start, end):
    a = s.index(start); b = s.index(end, a)
    return s[a:b]

AUDIENCE = r"""const PACK_AUDIENCE = [
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

"""

SCHEMA_LESSON = r"""const SCHEMA_LESSON = [
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
'   "viz":{"type":"exp-likelihood"|"mle-sampling"|"unif-likelihood", ...params},"ask":{"q","nudge"}}',
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
'Only those three "viz" types exist in the app today. Do not invent a fourth — a scene',
'referencing an unknown type renders its text and says the visual is unavailable.'
].join("\n");
"""

SCHEMA_Q = r"""const SCHEMA_Q = [
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
"""

LESSON_STAGE = r"""  if(stage==="lesson")return [head,tctx,"",
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

"""

PRACTICE_STAGE = r"""  if(stage==="practice")return [head,tctx,"",
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

"""

MASTERY_STAGE = r"""  if(stage==="mastery")return [head,tctx,"",
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

"""

VALIDATION_EXTRA = r"""  " 10. The foundation drill: does every later scene stay inside what it checked or taught?",
  " 11. Flow diagrams: every edge between nodes that exist, no node off the grid, labels short.",
  " 12. Scenarios: any figure presented as fact — confirm it or have it rewritten qualitatively.",
  " 13. Difficulty tags: is every item tagged, and does the pool hold 6 easy / 10 moderate / 4 hard?",
  " 14. Key spread: no letter holding more than 40% of a set.",
  "",
"""

s = s.replace("const SCHEMA_LESSON = [", AUDIENCE + "const SCHEMA_LESSON = [", 1)
s = s.replace(span("const SCHEMA_LESSON = [", "const SCHEMA_Q = ["), SCHEMA_LESSON + "\n")
s = s.replace(span("const SCHEMA_Q = [", "function stagePrompt("), SCHEMA_Q + "\n")
s = s.replace(span('  if(stage==="lesson")return [head,tctx,"",', '  if(stage==="practice")return'), LESSON_STAGE)
s = s.replace(span('  if(stage==="practice")return [head,tctx,"",', '  if(stage==="mastery")return'), PRACTICE_STAGE)
s = s.replace(span('  if(stage==="mastery")return [head,tctx,"",', "  // validation"), MASTERY_STAGE)
s = s.replace('  "Then apply only the fixes I approve. Report first, write second.",',
              VALIDATION_EXTRA + '  "Then apply only the fixes I approve. Report first, write second.",')

# the topic context block should carry the exam weight, since weight decides depth
s = s.replace('''  const tctx=t?["Topic: "+t.id+" — "+t.name,
    "Required depth: "+t.extent+" — "+EXT[t.extent].d+".",''',
'''  const tctx=t?["Topic: "+t.id+" — "+t.name,
    "Required depth: "+t.extent+" — "+EXT[t.extent].d+".",
    t.imp?("Exam weight: "+IMP[t.imp].s+" "+IMP[t.imp].n+" — "+IMP[t.imp].d+
      (t.qs?(". About "+t.qs+" question"+(t.qs>1?"s":"")+" a paper, "+(t.marks||t.qs*2)+" marks.")
           :"")+" Weight decides how many worked examples and transfer cases it earns, not the tone."):"",''')

if s == orig:
    sys.exit("nothing changed — anchors did not match")
io.open(P, "w", encoding="utf-8").write(s)
print("60-admin.js rewritten: %d -> %d bytes" % (len(orig), len(s)))
