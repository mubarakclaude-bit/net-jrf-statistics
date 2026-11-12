#!/usr/bin/env python3
"""Exact and structural checks for T7 birth–death and M/M/1 lesson."""
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
ROOT=Path(__file__).resolve().parent
lesson=json.loads((ROOT/"seed/lesson_stochastic_t7.json").read_text())
pool=json.loads((ROOT/"seed/stochastic_t7_mastery.json").read_text())
assert lesson["topicId"]=="stochastic-t7" and len(lesson["scenes"])==15
assert sum(bool(s.get("scenario")) for s in lesson["scenes"])==2
assert len(pool["items"])==20
# Finite birth-death chain in worked example: unnormalised weights 1,1,1/4.
weights=[F(1),F(1),F(1,4)]
total=sum(weights)
pi=[w/total for w in weights]
assert pi==[F(4,9),F(4,9),F(1,9)] and sum(pi)==1
# General local balance across adjacent states.
lam=[F(2),F(1)]; mu=[F(0),F(2),F(4)]
for n in range(2):
    assert pi[n]*lam[n]==pi[n+1]*mu[n+1]
# M/M/1 exact identities for lambda=2, mu=3.
lam,mu=F(2),F(3); rho=lam/mu
assert rho==F(2,3) and rho<1
p0=1-rho
p2=p0*rho**2
L=rho/(1-rho); Lq=rho**2/(1-rho)
W=1/(mu-lam); Wq=rho/(mu-lam)
assert p0==F(1,3) and p2==F(4,27)
assert L==2 and Lq==F(4,3)
assert W==1 and Wq==F(2,3)
assert L==lam*W and Lq==lam*Wq and L-Lq==rho and W-Wq==1/mu
# Stability boundary must not be treated as stationary.
assert not (F(4,4)<1)
items=pool["items"]
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in items)=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in items)=={"A":5,"B":5,"C":5,"D":5}
assert all(x["topic"]=="stochastic-t7" for x in items)
assert all(len(x.get("statements",[]))==4 and set(x.get("verdicts",{}))=={"A","B","C","D"} for x in items if x["format"]=="multi")
# Ensure multi-statement assessment metadata is specific to its displayed stem.
assert all("stated incorrect" not in s.lower() for q in pool["items"] for s in q.get("statements", []))
assert all(len(v.get("why", "")) >= 20 for q in pool["items"] if q["format"] == "multi" for v in q["verdicts"].values())
print("T7 birth–death, M/M/1 and mastery checks: PASS")
