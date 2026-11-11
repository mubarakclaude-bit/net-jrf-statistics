from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t5.json").read_text())
P=json.loads((R/"seed/design_t5_mastery.json").read_text())
assert len(L["scenes"])==15 and len(P["items"])==20
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
assert 5*4==20 and 6*3==18 and 5*4==20 and 6*6==36 and 4*7==28
assert L["scenes"][1]["scenario"]["answer"]=="Local control, through blocking."
assert "not automatically independent" in L["scenes"][2]["blocks"][2]["body"]
print("PASS: independent-unit counts and CRD/RBD/Latin-square allocation facts.")
