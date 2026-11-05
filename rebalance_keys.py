import json,glob,os,re,hashlib,collections,sys,shutil
SEED=sys.argv[1]
L="ABCD"
# "Option C" / "option C" -> remappable. Parenthesised or ordinal refs -> too ambiguous, skip item.
REF=re.compile(r'(?i)\b(option|options|choice|alternative)s?(\s+)([A-D])\b')
AMBIG=re.compile(r'(?i)(the (first|second|third|fourth|last) (option|choice|answer|alternative)|\([A-D]\)|\b[A-D]\)\s)')
report=[]
for p in sorted(glob.glob(os.path.join(SEED,"*.json"))):
    d=json.load(open(p))
    its=d.get("items")
    if not isinstance(its,list) or not its or not isinstance(its[0],dict) or "answer" not in its[0]: continue
    if d.get("source")=="pyq":
        report.append((os.path.basename(p),"SKIPPED (pyq: option order is historical)",None,None)); continue
    before=collections.Counter(q.get("answer") for q in its if (q.get("options") or []))
    # round-robin target position, so each file comes out near-even
    tgt=0; changed=0; skipped=[]
    for q in its:
        opts=q.get("options") or []
        if len(opts)!=4: continue
        txt=(q.get("explanation") or "")+" "+(q.get("check") or "")
        if AMBIG.search(txt):
            skipped.append(q.get("id")); tgt=(tgt+1)%4; continue
        old=q["answer"]
        if old not in L: continue
        oi=L.index(old)
        want=tgt%4; tgt+=1
        # deterministic permutation of the three distractors, seeded on the item id
        h=int(hashlib.sha256(("key:"+str(q.get("id"))).encode()).hexdigest(),16)
        others=[i for i in range(4) if i!=oi]
        # pick one of the 6 orderings of the three distractors
        import itertools
        perms=list(itertools.permutations(others))
        order=list(perms[h%len(perms)])
        # new position j holds old index src[j]
        src=[None]*4; src[want]=oi
        k=0
        for j in range(4):
            if src[j] is None: src[j]=order[k]; k+=1
        q["options"]=[opts[src[j]] for j in range(4)]
        q["answer"]=L[want]
        # old letter -> new letter map, for "Option X" references
        newof={src[j]:j for j in range(4)}
        def remap(m):
            o=L.index(m.group(3).upper())
            return m.group(1)+m.group(2)+L[newof[o]]
        for f in ("explanation","check"):
            if q.get(f): q[f]=REF.sub(remap,q[f])
        changed+=1
    after=collections.Counter(q.get("answer") for q in its if (q.get("options") or []))
    json.dump(d,open(p,"w"),ensure_ascii=False,indent=1)
    report.append((os.path.basename(p),"%d reordered"%changed+(", %d left alone (%s)"%(len(skipped),",".join(skipped)) if skipped else ""),dict(sorted(before.items())),dict(sorted(after.items()))))
for n,msg,b,a in report:
    print("%-34s %s"%(n,msg))
    if b is not None: print("%-34s   %s  ->  %s"%("",b,a))
