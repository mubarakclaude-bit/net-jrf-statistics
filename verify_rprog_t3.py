#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_rprog_t3.json").read_text())
P=json.loads((R/"seed/rprog_t3_mastery.json").read_text())
assert L["id"]=="rprogt3" and L["topicId"]=="rprog-t3" and L["moduleId"]=="rprog"
assert len(L["scenes"])==13 and L["scenes"][-1]["setId"]=="rprog_t3_mastery"
assert L["anchors"]==[] and len(L["prereq"])>=3 and len(L["refs"])>=3
assert L["estMin"]==sum(s["mins"] for s in L["scenes"] if not s.get("ext"))==90
assert sum(s["kind"]=="guided" for s in L["scenes"])>=2
assert sum("scenario" in s for s in L["scenes"])>=2
assert len(P["items"])==P["count"]==20
assert Counter(x["diff"] for x in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for x in P["items"]:
 assert len(x["options"])==4 and len(x["explanation"])>=40
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi": assert len(x["statements"])==4 and set(x["verdicts"])==set("ABCD")
assert any("flow" in s for s in L["scenes"])
# A small explicit environment-chain model: lexical lookup uses the enclosing
# environment, not the caller; local assignment masks but does not overwrite it.
global_env={"x":3}
function_env={"x":5}
def lexical_lookup(name,local,parent):
 return local[name] if name in local else parent[name]
assert lexical_lookup("x",function_env,global_env)==5
assert global_env["x"]==3
# Superassignment walks parent environments and updates the first existing binding.
def superassign(name,value,environments):
 for env in environments[1:]:
  if name in env:
   env[name]=value
   return
 environments[-1][name]=value
inner={"z":1}; enclosing={"x":3}; global_env2={}
superassign("x",9,[inner,enclosing,global_env2])
assert enclosing["x"]==9 and "x" not in global_env2
superassign("new",7,[inner,{},global_env2])
assert global_env2["new"]==7
print("PASS: lexical lookup, local masking and parent-chain superassignment examples.")
print("PASS: 20 mastery items; difficulty 6/10/4; formats 12/5/3; answer keys balanced.")
