#!/usr/bin/env bash
# One call for the mechanical half of adding a lesson, replacing four separate steps.
#   ./addlesson.sh <authoring.py> <seed-stem> <topicId> <storeDocId> <masterySetStem>
# Generates, validates, checks every formula through the renderer and asserts the lesson is wired.
# It edits NO shared file: the lesson index and the test harness are generated from seed/ by
# tools/seed-docs.js. Prints only what changed or what failed.
set -e
# pipefail matters: `"$PYBIN" "$PY" | tail -2` otherwise reports tail's exit code, so a syntax
# error in the authoring script was swallowed and the run continued on a STALE seed file.
set -o pipefail
# Windows installs Python as `python`, and `python3` there is often a Microsoft Store alias
# that is not a working interpreter. Pick a real one rather than assuming the name.
PYBIN=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys;sys.exit(0 if sys.version_info[0]==3 else 1)" >/dev/null 2>&1; then
    PYBIN="$c"; break
  fi
done
[ -n "$PYBIN" ] || { echo "FAILED: no working Python 3 found (tried python3, python)"; exit 1; }
PY=$1; STEM=$2; TID=$3; DOC=$4; SET=$5
mkdir -p .cache
START=$(date +%s)
"$PYBIN" "$PY" | tail -2
# The authoring script hardcodes its own output path, so a <seed-stem> that does not match it
# sends the validator to the wrong file. If a file happens to sit at that path from an earlier
# run, everything downstream validates a STALE seed and passes. Refuse both cases loudly.
mtime() { stat -c %Y "$1" 2>/dev/null || stat -f %m "$1"; }
if [ ! -f "seed/$STEM.json" ]; then
  echo "FAILED: $PY did not write seed/$STEM.json"
  echo "  The <seed-stem> argument must match the OUT constant in the script."
  echo "  $PY has: $(grep -m1 '^OUT' "$PY" || echo '(no OUT line found)')"
  exit 1
fi
if [ "$(mtime "seed/$STEM.json")" -lt "$START" ]; then
  echo "FAILED: seed/$STEM.json is STALE — this run did not write it."
  echo "  The <seed-stem> argument does not match the OUT constant in $PY."
  echo "  $PY has: $(grep -m1 '^OUT' "$PY" || echo '(no OUT line found)')"
  exit 1
fi
node vcheck.js "seed/$STEM.json" 2>&1 | grep -vE '^seed/' | head -12
"$PYBIN" -I - "$STEM" "$TID" "$DOC" "$SET" <<'PYEOF'
import io,json,sys,os,datetime,subprocess
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
io.open('.cache/_m.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False))
subprocess.run(['node','mathrender.js','.cache/_m.json','.cache/_mo.json'],
               capture_output=True)
r=json.load(io.open('.cache/_mo.json',encoding='utf-8'))
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
PYEOF
# The lesson index and the test harness are GENERATED from seed/ by tools/seed-docs.js, so this script
# no longer edits test.js or seed/meta_lessons.json (the two files every parallel author used to collide
# in). It only asserts that the lesson is wired the way you said: topic id, store doc id, quiz set, 20 items.
node tools/gen-index.js --expect "$TID" "$DOC" "$SET"
