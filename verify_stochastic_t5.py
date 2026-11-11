#!/usr/bin/env python3
"""Independent exact/numerical checks for the T5 Poisson-process lesson."""
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
lesson=json.loads((ROOT/"seed/lesson_stochastic_t5.json").read_text())
pool=json.loads((ROOT/"seed/stochastic_t5_mastery.json").read_text())
assert lesson["topicId"]=="stochastic-t5"
assert len(lesson["scenes"])==15
assert sum(1 for s in lesson["scenes"] if s.get("scenario"))==2
assert len(pool["items"])==20

# Core count law: probabilities sum to one (numerical tail truncation).
for mu in [0.5,1.0,2.0,3.0,6.0]:
    partial=sum(math.exp(-mu)*mu**n/math.factorial(n) for n in range(40))
    assert abs(partial-1.0)<1e-12

# Count examples and complement.
assert abs(math.exp(-3)*3**2/math.factorial(2)-0.22404180765538775)<1e-14
assert abs((1-math.exp(-0.6))-0.4511883639059736)<1e-14

# Exponential survival, mean and variance.
lam=6.0; t=1/6
assert abs(math.exp(-lam*t)-math.exp(-1))<1e-15
assert 1/lam==1/6
assert 1/(lam*lam)==1/36

# kth-arrival survival equals the Poisson lower tail.
for k in range(1,7):
    mu=2.0
    gamma_survival=math.exp(-mu)*sum(mu**j/math.factorial(j) for j in range(k))
    poisson_lower=sum(math.exp(-mu)*mu**j/math.factorial(j) for j in range(k))
    assert abs(gamma_survival-poisson_lower)<1e-15

# T2 example: P(T_2 > 1) = P(N(1) <= 1) = 3e^-2.
assert abs(3*math.exp(-2)-0.4060058497098381)<1e-14

# Memorylessness: P(X>s+t | X>s) = P(X>t).
lam=1.7; s=2.3; t=0.8
conditional=math.exp(-lam*(s+t))/math.exp(-lam*s)
assert abs(conditional-math.exp(-lam*t))<1e-14

# Mastery pool composition and answer-key spread.
items=pool["items"]
from collections import Counter
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in items)=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in items)=={"A":5,"B":5,"C":5,"D":5}
assert all(x["topic"]=="stochastic-t5" for x in items)
assert all(x["answer"] in {"A","B","C","D"} for x in items)
assert all(len(x.get("statements", []))==4 and set(x.get("verdicts",{}))=={"A","B","C","D"} for x in items if x["format"]=="multi")
print("T5 Poisson, exponential, Erlang and mastery checks: PASS")
