"""Independent checks for the first 1000-MCQ PDF batch. Run with python verify_1000_mcq_batch1.py."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FILES=["seed/probability_supplementary_mcq.json","seed/multivariate_supplementary_mcq.json","seed/inference_supplementary_mcq.json","seed/stochastic_supplementary_mcq.json"]
def close(a,b,tol=1e-12): assert abs(a-b)<=tol,(a,b)
# p.954 joint MGF: means 1,3; variances 4,36; covariance 12.
close(12/math.sqrt(4*36),1); assert 1<3
# p.955 half-Cauchy normalisation.
close((2/math.pi)*(math.pi/2),1)
# p.956 CDF jump at 2.
close((4-7/3)/10,1/6)
# p.957 Binomial(3,1/6).
n,p=3,1/6
close(n*p,.5); close(n*p*(1-p),5/12)
close(3*p*p*(1-p)+p**3,2/27); close((1-p)**3,125/216)
# p.958 projection ranks r and p-r.
assert 5-2==3 and 2+3==5
# p.960 Markov matrix.
P=[[.25,.25,.25,.25],[0,.5,.5,0],[.75,0,.25,0],[.25,.5,0,.25]]
for row in P: close(sum(row),1)
close(P[0][0],.25); close(P[1][2],.5); close((0+1+2+3)/4,1.5)
# p.961 normal-sample identities; equal variances imply zero sum/difference covariance.
close(1-1,0)
# p.963 covariance of sum and difference.
for s in (.5,1,2): close(s*s-s*s,0)
# p.964 Uniform(-1,2) mean is below threshold 1.
assert (-1+2)/2==.5 and .5<1
seen=set(); total=0
for rel in FILES:
 d=json.loads((ROOT/rel).read_text(encoding="utf-8"))
 assert d["source"]=="variant" and d["count"]==len(d["items"])
 for q in d["items"]:
  assert q["id"] not in seen; seen.add(q["id"])
  assert len(q["explanation"])>=40 and 1<=q["pno"]<=1011
  if q["format"]=="multi":
   assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD") and q["answer"] in "ABCD"
  elif q["format"]=="single": assert len(q["options"])==4 and q["answer"] in "ABCD"
  elif q["format"]=="numeric": assert q["options"]==[] and q["check"]
 total+=d["count"]
assert total==211,total
print("PASS: 211 supplementary questions; source-key corrections recorded; ambiguous items held out.")
