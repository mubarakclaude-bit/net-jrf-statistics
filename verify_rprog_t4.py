#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_rprog_t4.json').read_text())
P=json.loads((R/'seed/rprog_t4_mastery.json').read_text())
assert L['id']=='rprogt4' and L['topicId']=='rprog-t4' and L['moduleId']=='rprog'
assert len(L['scenes'])==14 and L['scenes'][-1]['setId']=='rprog_t4_mastery'
assert len(P['items'])==P['count']==20
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
fmt=Counter(q['format'] for q in P['items'])
assert fmt.get('numeric',0)>=4 and fmt.get('multi',0)>=2
for q in P['items']:
 assert len(q['options'])==4 and len(q['explanation'])>=30
 if q['format']=='numeric': assert q.get('check')
 if q['format']=='multi': assert len(q['statements'])==4 and all(isinstance(q['verdicts'][k]['tf'],bool) and q['verdicts'][k]['why'] for k in 'ABCD')
assert sum(s['kind']=='guided' for s in L['scenes'])>=2 and any(s.get('flow') for s in L['scenes'])
assert 2*2-1*3==1
A=(3,2); B=(2,4); assert A[1]==B[0] and (A[0],B[1])==(3,4)
A=[[1,2],[3,4]]; B=[[2,0],[1,2]]
elem=[[A[i][j]*B[i][j] for j in range(2)] for i in range(2)]
prod=[[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
assert elem==[[2,0],[3,8]] and prod==[[4,4],[10,8]]
print('PASS: R T4 structure and mastery contract; determinant and product-dimension arithmetic.')
