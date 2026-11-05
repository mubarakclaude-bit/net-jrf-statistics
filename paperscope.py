#!/usr/bin/env python3
# Two changes to the learning path:
#   1. Paper 1 and Paper 2 are never interleaved. Exam-weightage and personal order
#      sort within a paper, not across the two, which previously dropped a Paper 1
#      module into the middle of the Paper 2 run.
#   2. A paper scope on the path — Paper 2 by default, since that is what is being
#      targeted — with Paper 1 and Both a click away. The choice is saved with the
#      rest of the config, so it survives a reload.
import io, sys

def patch(path, pairs):
    s = io.open(path, encoding="utf-8").read()
    before = s
    for a, b in pairs:
        if a not in s: sys.exit("anchor not found in %s:\n%s" % (path, a[:140]))
        s = s.replace(a, b, 1)
    io.open(path, "w", encoding="utf-8").write(s)
    return s != before

# ---- state: the scope, defaulting to Paper 2
patch("src/11-state.js", [
 ('  mode:"pyq",navW:286,aideW:300,',
  '  mode:"pyq",paper:2,navW:286,aideW:300,'),
])
patch("src/13-db.js", [
 ("  if(S.cfg.mode&&MODES[S.cfg.mode])S.mode=S.cfg.mode;",
  "  if(S.cfg.mode&&MODES[S.cfg.mode])S.mode=S.cfg.mode;\n"
  "  if(S.cfg.paper===1||S.cfg.paper===2||S.cfg.paper===\"all\")S.paper=S.cfg.paper;"),
])

# ---- ordering: scope first, then never mix the two papers
patch("src/45-learn.js", [
 ("""/* ---- path ordering ---- */
function pathOrder(){
  const ms=mods(2).concat(mods(1));
  if(S.mode==="syllabus"){
    const hasSyl=ms.some(m=>m.sylOrder!=null);
    return hasSyl?ms.slice().sort((a,b)=>(a.sylOrder==null?99:a.sylOrder)-(b.sylOrder==null?99:b.sylOrder)):ms;
  }
  if(S.mode==="personal"&&S.personal&&S.personal.entries){
    const pr={};S.personal.entries.forEach((e,i)=>{if(pr[e.moduleId]===undefined)pr[e.moduleId]=i});
    return ms.slice().sort((a,b)=>(pr[a.id]===undefined?999:pr[a.id])-(pr[b.id]===undefined?999:pr[b.id]));
  }
  return ms.slice().sort((a,b)=>(b.marks||0)-(a.marks||0));
}""",
  """/* ---- path ordering ----
   The two papers are different exams with different syllabi, so they are never
   interleaved: a scope picks which paper is on the path, and "both" lists Paper 2
   first and Paper 1 after it, each ordered by the current mode. */
const PAPERS=[2,1];
function paperScope(){return S.paper===1||S.paper===2?S.paper:"all"}
function sortPaper(ms){
  if(S.mode==="syllabus"){
    const hasSyl=ms.some(m=>m.sylOrder!=null);
    return hasSyl?ms.slice().sort((a,b)=>(a.sylOrder==null?99:a.sylOrder)-(b.sylOrder==null?99:b.sylOrder)):ms.slice();
  }
  if(S.mode==="personal"&&S.personal&&S.personal.entries){
    const pr={};S.personal.entries.forEach((e,i)=>{if(pr[e.moduleId]===undefined)pr[e.moduleId]=i});
    return ms.slice().sort((a,b)=>(pr[a.id]===undefined?999:pr[a.id])-(pr[b.id]===undefined?999:pr[b.id]));
  }
  return ms.slice().sort((a,b)=>(b.marks||0)-(a.marks||0));
}
function pathPapers(){const sc=paperScope();return sc==="all"?PAPERS:[sc]}
function pathOrder(){
  let out=[];
  pathPapers().forEach(p=>{out=out.concat(sortPaper(mods(p)))});
  return out;
}
const PAPERN={2:"Paper 2 · Statistics",1:"Paper 1 · General paper"};
/* The scope control. Paper 2 is the default because that is the subject paper. */
function paperPills(){
  const sc=paperScope();
  return '<div class="pills" style="margin-bottom:10px">'+
    [[2,"Paper 2"],[1,"Paper 1"],["all","Both"]].map(x=>
      '<button class="tog" data-paper="'+x[0]+'" aria-pressed="'+(String(sc)===String(x[0]))+'">'+x[1]+
      '<span class="note" style="margin-left:6px">'+
        (x[0]==="all"?300:mods(x[0]).reduce((a,m)=>a+(m.marks||0),0))+'m</span></button>').join("")+
    '</div>';
}"""),
])

# ---- the scope control, on the rail and on the landing pane
patch("src/45-learn.js", [
 ("""    '<div class="pills" style="margin:8px 0 4px">'+Object.keys(MODES).map(k=>""",
  """    paperPills()+
    '<div class="pills" style="margin:8px 0 4px">'+Object.keys(MODES).map(k=>"""),
 ("""    '<div class="pills" style="margin-bottom:14px">'+
      '<span class="chip ac">'+esc(MODES[S.mode].tag)+'</span>'+""",
  """    paperPills()+
    '<div class="pills" style="margin-bottom:14px">'+
      '<span class="chip ac">'+esc(MODES[S.mode].tag)+'</span>'+"""),
])

# ---- paper headings when both are shown, in the rail and on the landing
patch("src/45-learn.js", [
 ("""  '<div class="navlist">'+order.map(mo=>{""",
  """  '<div class="navlist">'+order.map((mo,oi)=>{
    const head=(paperScope()==="all"&&(oi===0||order[oi-1].paper!==mo.paper))
      ? '<div class="paperhd">'+PAPERN[mo.paper]+'</div>' : "";"""),
 ("""    return '<div class="navmod">'+""",
  """    return head+'<div class="navmod">'+"""),
])
patch("src/45-learn.js", [
 ("""      '<div class="modgrid">'+order.map(m=>modCard(m)).join("")+'</div>'+""",
  """      '<div class="modgrid">'+order.map((m,oi)=>
        ((paperScope()==="all"&&(oi===0||order[oi-1].paper!==m.paper))
          ? '<div class="paperhd">'+PAPERN[m.paper]+'</div>' : "")+modCard(m)).join("")+'</div>'+"""),
])

# ---- wiring
patch("src/70-wire.js", [
 ("""  on("[data-mode]",e=>{S.mode=e.dataset.mode;S.cfg.mode=S.mode;saveCfg();render()});""",
  """  on("[data-mode]",e=>{S.mode=e.dataset.mode;S.cfg.mode=S.mode;saveCfg();render()});
  on("[data-paper]",e=>{const v=e.dataset.paper;
    S.paper=(v==="all")?"all":+v;S.cfg.paper=S.paper;saveCfg();render()});"""),
])

# ---- the bank's module filter should group by paper rather than list all 21 flat
patch("src/52-bank.js", [
 ("""    '<div><label class="fl">Module</label>'+sel("fMod",f.mod,[["","All modules"]].concat(ms.map(m=>[m.id,modNo(m.id)+" · "+m.name+" ("+loadedCount(m.id)+")"])))+'</div>'+""",
  """    '<div><label class="fl">Module</label><select id="fMod">'+
      '<option value=""'+(f.mod?"":" selected")+'>All modules</option>'+
      [2,1].map(p=>{const l=ms.filter(m=>m.paper===p);if(!l.length)return"";
        return '<optgroup label="Paper '+p+(p===2?" · Statistics":" · General paper")+'">'+
          l.map(m=>'<option value="'+m.id+'"'+(f.mod===m.id?" selected":"")+'>'+
            modNo(m.id)+" · "+esc(m.name)+" ("+loadedCount(m.id)+")"+'</option>').join("")+'</optgroup>'}).join("")+
      '</select></div>'+"""),
])

# ---- a heading style for the paper groups
CSS = """
/* Paper headings — the two papers are separate exams, never run together. */
.paperhd{font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:var(--fg3);padding:14px 4px 6px;border-top:1px solid var(--line);margin-top:6px}
.modgrid>.paperhd:first-child,.navlist>.paperhd:first-child{border-top:0;margin-top:0;padding-top:4px}
.navlist .paperhd{padding-inline:14px}
"""
w = io.open("src/02-ws.css", encoding="utf-8").read()
if ".paperhd{" not in w:
    io.open("src/02-ws.css", "w", encoding="utf-8").write(w + CSS)
print("paper scope added; the two papers no longer interleave")
