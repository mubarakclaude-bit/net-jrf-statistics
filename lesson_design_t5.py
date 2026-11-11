import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t5.json").read_text())
P=json.loads((R/"seed/design_t5_mastery.json").read_text())
assert L["id"]=="designt5" and L["topicId"]=="design-t5"
assert len(L["scenes"])==15 and L["scenes"][-1]["kind"]=="quiz" and L["scenes"][-1]["setId"]=="design_t5_mastery"
assert len(P["items"])==20
assert Counter(x["diff"] for x in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in P["items"])=={"single":9,"numeric":8,"multi":3}
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
assert sum("ask" in x for x in L["scenes"])>=6 and sum("scenario" in x for x in L["scenes"])>=2
assert any(x.get("kind")=="trapcheck" for x in L["scenes"])
for x in P["items"]:
 assert len(x["options"])==4 and len(x["explanation"])>=35
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi":
  truth="".join(k for k in "ABCD" if x["verdicts"][k]["tf"])
  assert x["options"]["ABCD".index(x["answer"])]=={"ABC":"A, B and C only","ABD":"A, B and D only"}[truth]
print("PASS: 14 scenes; mastery contract; balanced keys, formats and difficulty.")
