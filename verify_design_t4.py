from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t4.json").read_text())
P=json.loads((R/"seed/design_t4_mastery.json").read_text())
assert len(L["scenes"])==15 and len(P["items"])==20
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
N=[[1,1,1,0,0,0],[1,0,0,1,1,0],[0,1,0,1,0,1],[0,0,1,0,1,1]]
v,b=4,6
assert [sum(row) for row in N]==[3]*4
assert [sum(N[i][j] for i in range(v)) for j in range(b)]==[2]*6
NN=[[sum(N[i][j]*N[k][j] for j in range(b)) for k in range(v)] for i in range(v)]
assert NN==[[3,1,1,1],[1,3,1,1],[1,1,3,1],[1,1,1,3]]
r,k,lam=3,2,1
assert b*k==v*r==12 and lam*(v-1)==r*(k-1)==3
for vv,rr,kk in [(7,6,3),(6,5,3),(5,4,2),(9,4,3),(8,7,4)]:
 assert (rr*(kk-1))%(vv-1)==0 and (vv*rr)%kk==0
print("PASS: incidence matrix row/column sums and NN' identity.")
print("PASS: BIBD parameter identities and worked calculations.")
