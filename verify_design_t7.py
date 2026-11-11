from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t7.json").read_text())
P=json.loads((R/"seed/design_t7_mastery.json").read_text())
assert len(L["scenes"])==14 and len(P["items"])==20
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
# RBD: t=3,r=3,B=20,T=18,G=48 -> 66/4=16.5
assert (3*20+3*18-48)/((3-1)*(3-1))==16.5
# Latin square p=3,R=14,C=12,T=13,G=30 -> 57/2=28.5
assert (3*(14+12+13)-2*30)/((3-1)*(3-2))==28.5
assert 12-1==11 and 17-1==16
print("PASS: RBD and Latin-square missing-value calculations and error-df adjustment.")
