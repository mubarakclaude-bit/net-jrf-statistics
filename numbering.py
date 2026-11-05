#!/usr/bin/env python3
# Give every module a number and every topic a decimal number (1, 1.1, 1.2 …) so the
# syllabus can be talked about by position. The numbers are identities, not positions
# in the current view: they come from the official syllabus order when that has been
# imported and from the catalog order otherwise, so 1.3 means the same topic whether
# the learner is in syllabus, exam-weightage or personal mode.
import io, sys

def patch(path, pairs, must=True):
    s = io.open(path, encoding="utf-8").read()
    before = s
    for a, b in pairs:
        if a not in s:
            if must: sys.exit("anchor not found in %s:\n%s" % (path, a[:160]))
            continue
        s = s.replace(a, b, 1)
    if s != before:
        io.open(path, "w", encoding="utf-8").write(s)
    return s != before

# ---------------------------------------------------------------- the numbering
NUM = '''
/* ---- syllabus numbering ----
   A module's number and a topic's decimal number are identities, not positions in
   the current view. They follow the official syllabus order once that has been
   imported, and the catalog order until then, so "1.3" means the same topic in
   every study mode. The map is cached and rebuilt only when the catalog changes. */
let NUMMAP=null,NUMSIG="";
function numSig(){
  const l=(S.catalog&&S.catalog.modules)||[];
  return l.map(m=>m.id+":"+(m.sylOrder==null?"-":m.sylOrder)+":"+((m.topics||[]).length)).join("|");
}
function numMap(){
  const sig=numSig();
  if(NUMMAP&&NUMSIG===sig)return NUMMAP;
  const l=((S.catalog&&S.catalog.modules)||[]).slice();
  const hasSyl=l.some(m=>m.sylOrder!=null);
  l.sort(hasSyl
    ?(a,b)=>(a.sylOrder==null?999:a.sylOrder)-(b.sylOrder==null?999:b.sylOrder)
    :(a,b)=>(a.order||0)-(b.order||0));
  const mod={},top={};
  l.forEach((m,i)=>{
    mod[m.id]=String(i+1);
    (m.topics||[]).forEach((t,j)=>{top[t.id]=(i+1)+"."+(j+1)});
  });
  NUMMAP={mod:mod,top:top,src:hasSyl?"official syllabus order":"catalog order"};
  NUMSIG=sig;
  return NUMMAP;
}
function modNo(id){return numMap().mod[id]||""}
function topNo(tid){return numMap().top[tid]||""}
function numSrc(){return numMap().src}
/* The number as a small label. Mono and tabular so a column of them lines up. */
function nTag(n,cls){return n?'<span class="nnum'+(cls?" "+cls:"")+'">'+n+'</span>':""}
'''
s = io.open("src/20-metrics.js", encoding="utf-8").read()
if "function numMap()" not in s:
    s = s.replace('function modById(id){return mods().find(m=>m.id===id)}',
                  'function modById(id){return mods().find(m=>m.id===id)}\n' + NUM.strip() + "\n")
    io.open("src/20-metrics.js", "w", encoding="utf-8").write(s)

# ------------------------------------------------------------------ learn rail
patch("src/45-learn.js", [
 # module header in the rail
 ("""        '<span class="caret">▶</span><span class="nm">'+esc(mo.name)+'</span>'+""",
  """        '<span class="caret">▶</span>'+nTag(modNo(mo.id),"mn")+'<span class="nm">'+esc(mo.name)+'</span>'+"""),
 # topic row in the rail
 ("""          '<span class="tn">'+esc(t.name)+""",
  """          '<span class="tn">'+nTag(topNo(t.id))+esc(t.name)+"""),
 # module card on the landing
 ("""      '<span class="mh"><b>'+esc(m.name)+'</b>'+""",
  """      '<span class="mh"><b>'+nTag(modNo(m.id),"mn")+esc(m.name)+'</b>'+"""),
 # topic row inside a module card
 ("""        '<span class="mtn"><b>'+esc(t.name)+'</b>'+""",
  """        '<span class="mtn"><b>'+nTag(topNo(t.id))+esc(t.name)+'</b>'+"""),
 # the lesson overview heading and the scene bar's crumb
 ("""    '<h1>'+esc(les.title)+'</h1>'+
    '<p class="lead">'+tot+' sections, about '+les.estMin+' minutes. '+esc(les.engineName)+'.</p>'+""",
  """    '<h1>'+nTag(topNo(tid),"h")+esc(les.title)+'</h1>'+
    '<p class="lead">'+tot+' sections, about '+les.estMin+' minutes. '+esc(les.engineName)+'.</p>'+"""),
 ("""      '<span class="crumb">'+esc(les.title)+'</span>'+""",
  """      '<span class="crumb">'+nTag(topNo(L.topicId))+esc(les.title)+'</span>'+"""),
])

# the rail footer should say what the numbers mean, once
patch("src/45-learn.js", [
 ("""    '<p class="note">'+esc(m.d)+'</p>'+""",
  """    '<p class="note">'+esc(m.d)+'</p>'+
    '<p class="note" style="margin-top:4px">Numbers follow the '+numSrc()+
      ' and stay with a topic whichever order you study in.</p>'+"""),
])

# ------------------------------------------------------- bank, mock, progress, admin
patch("src/52-bank.js", [
 ("""ms.map(m=>[m.id,m.name+" ("+loadedCount(m.id)+")"])""",
  """ms.map(m=>[m.id,modNo(m.id)+" · "+m.name+" ("+loadedCount(m.id)+")"])"""),
])
patch("src/55-progress.js", [
 ("""    o2.ms.concat(o1.ms).map(x=>'<tr><td>'+esc(x.m.name)+'</td>""",
  """    o2.ms.concat(o1.ms).map(x=>'<tr><td>'+nTag(modNo(x.m.id))+esc(x.m.name)+'</td>"""),
])
patch("src/60-admin.js", [
 ("""mods().map(m=>'<option value="'+m.id+'"'+(m.id===pm.id?" selected":"")+'>'+esc(m.name)+'</option>')""",
  """mods().map(m=>'<option value="'+m.id+'"'+(m.id===pm.id?" selected":"")+'>'+modNo(m.id)+' · '+esc(m.name)+'</option>')"""),
 ("""pm.topics.map(t=>'<option value="'+t.id+'"'+(pt&&t.id===pt.id?" selected":"")+'>'+esc(t.name)+(lix[t.id]?"  ✓ lesson":"")+'</option>')""",
  """pm.topics.map(t=>'<option value="'+t.id+'"'+(pt&&t.id===pt.id?" selected":"")+'>'+topNo(t.id)+' · '+esc(t.name)+(lix[t.id]?"  ✓ lesson":"")+'</option>')"""),
 # the authoring packs should name the number too, so a chat knows which topic is meant
 ('''  const tctx=t?["Topic: "+t.id+" — "+t.name,''',
  '''  const tctx=t?["Topic: "+topNo(t.id)+" "+t.id+" — "+t.name,'''),
])

# ------------------------------------------------------------------------- CSS
CSS = """
/* Syllabus numbers: quiet, monospaced and tabular so a column of them lines up. */
.nnum{display:inline-block;font-family:var(--mono);font-size:.72em;font-weight:600;
  color:var(--fg3);font-variant-numeric:tabular-nums;margin-right:7px;letter-spacing:-.01em}
.nnum.mn{color:var(--fg2);background:var(--surface3);border-radius:6px;padding:1px 6px;font-size:.7em}
.nnum.h{color:var(--fg3);font-size:.6em;vertical-align:middle;margin-right:9px}
.tbl .nnum{margin-right:6px}
"""
h = io.open("src/00-head.html", encoding="utf-8").read()
if ".nnum{" not in h:
    h = h.replace("\n/* ===================== Airbnb patterns ===================== */",
                  CSS + "\n/* ===================== Airbnb patterns ===================== */")
    io.open("src/00-head.html", "w", encoding="utf-8").write(h)

print("numbering added: modules 1..N, topics N.M, from the catalog or the official syllabus order")
