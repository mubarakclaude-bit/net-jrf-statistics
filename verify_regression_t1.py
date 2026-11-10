#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_regression_t1.json').read_text())
P=json.loads((R/'seed/regression_t1_mastery.json').read_text())
assert L['topicId']=='regression-t1' and len(L['scenes'])==15
assert len(L['objectives'])>=5 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert sum('scenario' in s for s in L['scenes'])>=1
assert len([s for s in L['scenes'] if s['kind']=='worked'])>=2
# Exact symbolic identities are checked through small full-rank designs.
import numpy as np
X=np.array([[1,0],[1,1],[1,2]],dtype=object)
H=X@np.linalg.inv(np.array(X.T@X,dtype=float))@X.T
M=np.eye(3)-H
assert np.allclose(H.T,H) and np.allclose(H@H,H)
assert np.allclose(M.T,M) and np.allclose(M@M,M)
assert np.allclose(H@M,0) and np.allclose(X.T@M,0)
assert abs(np.trace(H)-2)<1e-9 and abs(np.trace(M)-1)<1e-9
Q=P['items']
assert len(Q)==20
assert Counter(x['diff'] for x in Q)=={'easy':6,'moderate':10,'hard':4}
assert Counter(x['format'] for x in Q)=={'single':12,'numeric':5,'multi':3}
assert Counter(x['answer'] for x in Q)=={'A':5,'B':5,'C':5,'D':5}
assert all(x.get('check') for x in Q if x['format']=='numeric')
assert all(len(x.get('statements',[]))==4 and set(x.get('verdicts',{}))=={'A','B','C','D'} for x in Q if x['format']=='multi')
print('Regression T1 hat-matrix identities and mastery checks: PASS')
