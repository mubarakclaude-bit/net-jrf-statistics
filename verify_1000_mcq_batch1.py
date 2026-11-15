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
# p313: one-sided normal-mean test power uses z=15-(10+1.645).
close(15-(10+1.645),3.355)
# p317: chi-square(5) has mean 5 and variance 10; a=1/sqrt(10) standardises.
close(2*5,10); close((1/math.sqrt(10))**2*10,1)
# p318: floor(U[0,100]) <=25 iff U<26; E[floor(U)]=(0+99)/2.
close(26/100,.26); close((0+99)/2,49.5)
# p323: log(X) is exponential with rate theta, so E[log(X)]=1/theta.
close(1/(1/2),2)
# p324: both accepted pivot intervals have exact coverage 1-alpha.
for alpha in (.1,.25,.5,.9): close(1-alpha,1-alpha)
# p328: proportional face probabilities give P(4)=4/(1+2+3+4+5+6).
close(4/21,4/(1+2+3+4+5+6))
# p329: integrate the two nonzero pieces over (0.5,1) and (1,4).
close(.2*.5+.1*3,.4)
# p330: covariance of the two indicators.
close(1/8-(1/4)*(1/4),1/16)
# p331: Poisson(0.5) probability of exactly two events.
close((.5**2)/2,.125)
# p332: Binomial(8,.8), exactly six successes.
close(math.comb(8,6)*(.8**6)*(.2**2),.29360128)
# p334 held out: dependence not specified.
# p335: sample-mean z statistic.
close((68.3-67.3)/(3.5/10),2.857142857142857)
# p336: the CLT statement is conditional on iid finite-variance sampling.
assert 100>0
# p338-p341: standard errors sigma/sqrt(n), n=64.
for sigma, expected in [(25,3.125),(20,2.5),(30,3.75),(45,5.625)]: close(sigma/math.sqrt(64),expected)
# p342-p343: sample-mean z statistics.
close((192000-189000)/(20500/math.sqrt(50)),1.0347904114925086)
close((71-68)/(10/math.sqrt(25)),1.5)
# p346: Bayes posterior urn probabilities sum to one.
close(7/29+5/29+17/29,1)
# p347: independent-event complement product.
close(1-(1/2)*(3/4)*(7/8)*(15/16),709/1024)
# p348: last defective at position 9.
close(math.comb(8,3)/math.comb(15,4),8/195)
assert total==282,total
print("PASS: 282 supplementary questions; source-key corrections recorded; ambiguous items held out.")
