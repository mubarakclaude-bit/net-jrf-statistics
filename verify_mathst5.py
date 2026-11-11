#!/usr/bin/env python3
"""Exact theorem anchors for Mathematics T5."""
import json
from collections import Counter
# |x| is continuous at 0, but one-sided derivatives are -1 and +1.
assert abs(0-0)==0 and (-1)!=1
# Piecewise continuity: 2a+1=4 gives a=3/2.
assert 2*(3/2)+1==4
# f=x^2 on [1,3]: average slope 4; derivative 2c=4 gives c=2.
assert (3**2-1**2)/(3-1)==4 and 2*2==4 and 1<2<3
# f=x^2-1 on [-1,1]: equal endpoints and derivative zero at c=0.
assert (-1)**2-1==1**2-1==0 and 2*0==0
# f=x^2 on [0,2]: MVT point c=1.
assert (2**2-0**2)/2==2 and 2*1==2
with open("seed/maths_t5_mastery.json",encoding="utf-8") as f: pool=json.load(f)
items=pool["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert sum(x["format"]=="numeric" for x in items)>=4
assert sum(x["format"]=="multi" for x in items)>=2
assert max(Counter(x["answer"] for x in items).values())<=8
print("Mathematics T5 exact theorem anchors and mastery-pool structure: PASS")
