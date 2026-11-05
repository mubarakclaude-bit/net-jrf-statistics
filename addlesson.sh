#!/usr/bin/env bash
# One call for the mechanical half of adding a lesson, replacing four separate steps.
#   ./addlesson.sh <authoring.py> <seed-stem> <topicId> <storeDocId> <masterySetStem>
# Generates, validates, checks every formula through the renderer, wires the test harness,
# and updates both copies of the lesson index. Prints only what changed or what failed.
set -e
# pipefail matters: `python3 "$PY" | tail -2` otherwise reports tail's exit code, so a syntax
# error in the authoring script was swallowed and the run continued on a STALE seed file.
set -o pipefail
PY=$1; STEM=$2; TID=$3; DOC=$4; SET=$5
python3 "$PY" | tail -2
node vcheck.js "seed/$STEM.json" 2>&1 | grep -vE '^seed/' | head -12
python3 -I - "$STEM" "$TID" "$DOC" "$SET" <<'PYEOF'
import io,json,sys,datetime,subprocess
stem,tid,doc,sset=sys.argv[1:5]
L=json.load(io.open('seed/%s.json'%stem,encoding='utf-8'))
# every formula through the layout engine: a refusal means the lesson would render as source
out=[]
def walk(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='math' and isinstance(v,str): out.extend(x for x in v.split('\n') if x.strip())
            elif k=='body' and isinstance(v,str) and o.get('t') in('formula','step','def'):
                out.extend(x for x in v.split('\n') if x.strip())
            else: walk(v)
    elif isinstance(o,list):
        for x in o: walk(x)
walk(L)
io.open('/tmp/claude-0/_m.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False))
subprocess.run(['node','mathrender.js','/tmp/claude-0/_m.json','/tmp/claude-0/_mo.json'],
               capture_output=True)
r=json.load(io.open('/tmp/claude-0/_mo.json',encoding='utf-8'))
bad=[k for k,v in r.items() if not v['ok']]
print('formulas %d, stacked %d, refusals %d'%(len(r),sum(1 for v in r.values() if 'pfrac' in v['print']),len(bad)))
for k in bad[:4]: print('  REFUSED:',k[:88])
# No pool item may cite its OWN answer as a wrong option. The key-spread relabel rewrites
# "option X" references, and a plural list ("options B and C") once slipped through and left a
# check line ruling out the correct answer.
import re
P=json.load(io.open('seed/%s.json'%sset,encoding='utf-8'))
selfcite=[]
for it in P.get('items',[]):
    ans=it.get('answer')
    for fld in ('explanation','check'):
        t=it.get(fld) or ''
        if 'option' not in t.lower(): continue
        cited=set()
        for m in re.finditer(r'[Oo]ptions?\s+([ABCD](?:\s*(?:,|and|or)\s*[ABCD])*)',t):
            cited|=set(re.findall(r'[ABCD]',m.group(1)))
        if ans in cited: selfcite.append((it['id'],fld,ans))
if selfcite:
    for x in selfcite: print('  SELF-CITED ANSWER: %s %s cites its own answer %s'%x)
    raise SystemExit('pool cites its own answer as an option — fix before pushing')
print('option references consistent with the keys')
# wire the test harness, idempotently
s=io.open('test.js',encoding='utf-8').read()
# Match the EXACT wiring line, not a substring: 'probabilityt1' is a substring of
# 'probabilityt13', which once made this report "already wired" and silently skip a lesson.
docline="docs['lessons/%s'] = J("%doc
setline="'%s',"%sset
if docline not in s:
    anchor="  docs['meta/lessons'] = J('meta_lessons');"
    assert s.count(anchor)==1
    s=s.replace(anchor,"  docs['lessons/%s'] = J('%s');\n%s"%(doc,stem,anchor),1)
    a="'official_t5_mastery',"; assert s.count(a)==1
    s=s.replace(a,a+" %s"%setline,1)
    io.open('test.js','w',encoding='utf-8').write(s)
    print('harness wired')
else: print('harness already wired')
# Never leave this to chance again: assert both halves really are present.
s=io.open('test.js',encoding='utf-8').read()
assert docline in s, 'HARNESS NOT WIRED: missing %s'%docline
assert setline in s, 'HARNESS NOT WIRED: missing mastery set %s'%setline
ent={'id':L['id'],'title':L['title'],'moduleId':L['moduleId'],'estMin':L['estMin'],
     'scenes':len(L['scenes']),'status':L['status'],'version':L['version']}
for path in ('seed/meta_lessons.json','/tmp/claude-0/store/lessons_merged.json'):
    d=json.load(io.open(path,encoding='utf-8'))
    d['topics'][tid]=ent; d['count']=len(d['topics'])
    d['updated']=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    json.dump(d,io.open(path,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('indexed %s: %d min, %d scenes | store doc lessons/%s, qset %s'%(tid,ent['estMin'],ent['scenes'],doc,sset))
PYEOF
