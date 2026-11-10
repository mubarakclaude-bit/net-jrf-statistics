#!/usr/bin/env python3
"""Exact checks for the T6 simple random walk and gambler's ruin lesson."""
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from math import comb

ROOT=Path(__file__).resolve().parent
lesson=json.loads((ROOT/"seed/lesson_stochastic_t6.json").read_text())
pool=json.loads((ROOT/"seed/stochastic_t6_mastery.json").read_text())
assert lesson["topicId"]=="stochastic-t6"
assert len(lesson["scenes"])==12
assert sum(bool(s.get("scenario")) for s in lesson["scenes"])==2
assert len(pool["items"])==20

# Binomial position: S4=2 iff exactly three upward moves.
assert comb(4,3)*F(1,2)**4==F(1,4)
# Fair four-step return to zero: two up and two down.
assert comb(4,2)*F(1,2)**4==F(3,8)

# Fair gambler's ruin u_i=i/N satisfies the recurrence and boundaries.
for N in range(2,12):
    for i in range(1,N):
        u=lambda j:F(j,N)
        assert u(i)==F(1,2)*u(i+1)+F(1,2)*u(i-1)
    assert F(0,N)==0 and F(N,N)==1

# Biased worked example p=2/3, q=1/3, N=3, i=1.
p=F(2,3); q=F(1,3); N=3
u=lambda i:(1-(q/p)**i)/(1-(q/p)**N)
assert u(0)==0 and u(N)==1
assert u(1)==F(4,7)
assert 1-u(1)==F(3,7)

# Expected absorption time recurrence: fair m_i=i(N-i).
for N in range(2,10):
    m=lambda i:i*(N-i)
    for i in range(1,N):
        assert m(i)==1+F(1,2)*m(i+1)+F(1,2)*m(i-1)
    assert m(0)==0 and m(N)==0

# Biased expected duration formula agrees with first-step recurrence.
p=F(2,3); q=F(1,3); N=3
u=lambda i:(1-(q/p)**i)/(1-(q/p)**N)
m=lambda i:(F(i)-N*u(i))/(q-p)
assert m(0)==0 and m(N)==0
for i in range(1,N):
    assert m(i)==1+p*m(i+1)+q*m(i-1)
assert m(1)==F(15,7)

items=pool["items"]
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in items)=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in items)=={"A":5,"B":5,"C":5,"D":5}
assert all(x["topic"]=="stochastic-t6" for x in items)
assert all(len(x.get("statements",[]))==4 and set(x.get("verdicts",{}))=={"A","B","C","D"} for x in items if x["format"]=="multi")
assert all(len(x.get("statements",[]))==4 and set(x.get("verdicts",{}))=={"A","B","C","D"} for x in items if x["format"]=="multi")
print("T6 random walk, gambler's ruin and expected-time checks: PASS")
