import json
from pathlib import Path
L=json.loads((Path(__file__).resolve().parent/"seed/lesson_sampling_t4.json").read_text(encoding="utf-8"))
assert L["anchors"]==[{"paper":"j26","q":36}]
#!/usr/bin/env python3
from fractions import Fraction as F
M,n=20,4
totals=[20,25,30,25]
tbar=F(sum(totals),len(totals)); yhat=M*tbar
assert tbar==25 and yhat==500
N=M*5
assert N==100 and yhat/N==5
deff=1+(8-1)*F(1,4); neff=F(160)/deff
assert deff==F(11,4) and round(float(neff),2)==58.18
assert F(12)*F(15+18+21,3)==216
deff_a=1+(10-1)*F(1,10); deff_b=1+(5-1)*F(1,10)
assert deff_a==F(19,10) and deff_b==F(7,5)
assert round(float(F(200)/deff_a),2)==105.26
assert round(float(F(200)/deff_b),2)==142.86
assert F(20,4)==5 and F(160,2)==80
print("PASS cluster expansion, design effect and effective sample size")
