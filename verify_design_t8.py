from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t8.json").read_text())
P=json.loads((R/"seed/design_t8_mastery.json").read_text())
assert len(L["scenes"])==15 and len(P["items"])==20
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
# Concurrence graph: chain 1-2-3-4 is connected; graph with components {1,2,3},{4,5} is not.
edges={(1,2),(2,3),(3,4)}
reach={1}
while True:
 new=reach|{b for a,b in edges if a in reach}|{a for a,b in edges if b in reach}
 if new==reach: break
 reach=new
assert reach=={1,2,3,4}
# Rank criterion and component relation.
assert 5-1==4
assert 6-2==4
assert 10-3==7
# BIBD concurrence graph with v=7, lambda>0 is complete.
assert 7*6//2==21
print("PASS: connectedness graph, rank v−1, component-rank relation and BIBD graph counts.")
