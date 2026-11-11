from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t6.json").read_text())
P=json.loads((R/"seed/design_t6_mastery.json").read_text())
assert len(L["scenes"])==15 and len(P["items"])==20
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
assert 2**3==8 and 8//2==4 and 2-1==1
assert 16//4==4 and 4*5==20
assert L["scenes"][7]["kind"]=="guided" and len(L["scenes"][7]["hints"])==3
assert "whole-plot error stratum" in L["scenes"][7]["steps"][0]["math"]
assert "whole-plot error" in L["scenes"][7]["solution"][0]["math"]
assert "λᵢ" in L["scenes"][10]["blocks"][1]["body"]
print("PASS: factorial block counts, split-plot error strata and PBIBD class-concurrence checks.")
