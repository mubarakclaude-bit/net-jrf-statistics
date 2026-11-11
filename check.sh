#!/usr/bin/env bash
# Report drift between what is on disk and what the index and harness claim.
# READ-ONLY by default — it writes nothing, so it is safe to run any time.
#
# WHY. Two shared files are appended to by `addlesson.sh`:
#   seed/meta_lessons.json   the lesson index, which is what gets PUSHED to the store
#   test.js                  the harness wiring
# Parallel authoring collides there even when the lessons themselves never overlap, and a
# botched merge loses an entry silently. Run this after any merge, rebase or cherry-pick,
# and before any push to the store.
#
#   ./check.sh            report only
#   ./check.sh --fix-index   rewrite seed/meta_lessons.json entries from the seeds
#
# --fix-index is NOT automatic on purpose. The index is not purely derived: it is the local
# copy of what the store serves. If a seed was revised locally and never pushed, the seed and
# the index legitimately disagree, and overwriting the index would claim a version the app
# does not have. Resolve such a case by pushing the lesson, not by reindexing.
set -e
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
FIX=0; [ "$1" = "--fix-index" ] && FIX=1
mkdir -p .cache
FIX=$FIX "$PYBIN" -I - <<'PYEOF'
import io,json,glob,os,re,sys,datetime
fix=os.environ.get('FIX')=='1'
bad=0

seeds={}
for f in sorted(glob.glob('seed/lesson_*.json')):
    stem=os.path.basename(f)[:-5]
    try: L=json.load(io.open(f,encoding='utf-8'))
    except Exception as e:
        print('BROKEN  %s is not valid JSON (%s)'%(f,e.__class__.__name__)); bad=1; continue
    miss=[k for k in ('id','title','moduleId','estMin','scenes','status','version','topicId') if k not in L]
    if miss:
        print('BROKEN  %s missing %s'%(f,', '.join(miss))); bad=1; continue
    seeds[L['topicId']]={'stem':stem,'doc':L['id'],
        'ent':{'id':L['id'],'title':L['title'],'moduleId':L['moduleId'],'estMin':L['estMin'],
               'scenes':len(L['scenes']),'status':L['status'],'version':L['version']}}

# one topicId per seed, or the index silently loses one
byid={}
for tid,v in seeds.items(): byid.setdefault(v['doc'],[]).append(tid)
for doc,tids in byid.items():
    if len(tids)>1:
        print('DUPLICATE  store doc %s claimed by %s'%(doc,', '.join(tids))); bad=1

idx=json.load(io.open('seed/meta_lessons.json',encoding='utf-8'))
topics=idx.get('topics',{})
if idx.get('count') != len(topics):
    print('COUNT DRIFT  meta_lessons.json count=%s but topics=%d'%(idx.get('count'),len(topics))); bad=1

missing=sorted(set(seeds)-set(topics))
extra  =sorted(set(topics)-set(seeds))
drift  =[t for t in sorted(set(seeds)&set(topics)) if topics[t]!=seeds[t]['ent']]

for t in missing: print('NOT INDEXED  %s (seed %s) — run addlesson.sh or ./check.sh --fix-index'%(t,seeds[t]['stem']))
for t in extra:   print('NO SEED      %s is in the index with no seed file on disk'%t)
for t in drift:
    a,b=topics[t],seeds[t]['ent']
    d=[k for k in b if a.get(k)!=b[k]]
    print('DRIFT        %s: index has %s'%(t,', '.join('%s=%s'%(k,a.get(k)) for k in d)))
    print('                     seed has %s'%(', '.join('%s=%s'%(k,b[k]) for k in d)))
if missing or extra or drift: bad=1

# harness: every lesson wired, every wired pool present on disk
t=io.open('test.js',encoding='utf-8').read()
for tid,v in sorted(seeds.items()):
    if "docs['lessons/%s'] = J("%v['doc'] not in t:
        print('NOT WIRED    %s — test.js has no docs line for lessons/%s'%(tid,v['doc'])); bad=1
wired=set(re.findall(r"'([a-z0-9_]+_(?:mastery|practice))'",t))
for s in sorted(wired):
    if not os.path.exists('seed/%s.json'%s):
        print('WIRED, ABSENT  test.js references %s with no seed/%s.json'%(s,s)); bad=1
pools=set(os.path.basename(f)[:-5] for f in glob.glob('seed/*_mastery.json'))
for s in sorted(pools-wired):
    print('POOL NOT WIRED  seed/%s.json exists but test.js does not load it'%s); bad=1

if fix and drift+missing:
    for tid in drift+missing: topics[tid]=seeds[tid]['ent']
    idx['topics']=topics; idx['count']=len(topics)
    idx['updated']=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    json.dump(idx,io.open('seed/meta_lessons.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('\nFIXED %d index entries. The store still serves the old values until you push'%len(drift+missing))
    print('seed/meta_lessons.json AND every lesson whose version changed.')
elif not bad:
    print('clean: %d lessons, index and harness agree with the seeds on disk'%len(seeds))
sys.exit(0)
PYEOF

# Keep Probability question-bank totals and all 13 mastery pools independently verified.
if [ -f verify_probability_index.py ]; then
  python3 verify_probability_index.py
fi
