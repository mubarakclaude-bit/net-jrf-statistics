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
# Exact rational projection identities for X = [[1,0],[1,1],[1,2]].
from fractions import Fraction as F
H=[[F(5,6),F(1,3),F(-1,6)],[F(1,3),F(1,3),F(1,3)],[F(-1,6),F(1,3),F(5,6)]]
M=[[F(1,6),F(-1,3),F(1,6)],[F(-1,3),F(2,3),F(-1,3)],[F(1,6),F(-1,3),F(1,6)]]
def tr(A): return sum(A[i][i] for i in range(len(A)))
def mul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def transpose(A): return [list(x) for x in zip(*A)]
I=[[F(int(i==j)) for j in range(3)] for i in range(3)]
X=[[F(1),F(0)],[F(1),F(1)],[F(1),F(2)]]
assert transpose(H)==H and mul(H,H)==H
assert transpose(M)==M and mul(M,M)==M
assert mul(H,M)==[[F(0)]*3 for _ in range(3)]
assert mul(transpose(X),M)==[[F(0)]*3 for _ in range(2)]
assert tr(H)==2 and tr(M)==1
Q=P['items']
assert len(Q)==20
assert Counter(x['diff'] for x in Q)=={'easy':6,'moderate':10,'hard':4}
assert Counter(x['format'] for x in Q)=={'single':12,'numeric':5,'multi':3}
assert Counter(x['answer'] for x in Q)=={'A':5,'B':5,'C':5,'D':5}
assert all(x.get('check') for x in Q if x['format']=='numeric')
assert all(len(x.get('statements',[]))==4 and set(x.get('verdicts',{}))=={'A','B','C','D'} for x in Q if x['format']=='multi')
print('Regression T1 hat-matrix identities and mastery checks: PASS')
