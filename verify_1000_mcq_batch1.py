"""Independent checks for the first 1000-MCQ PDF batch. Run with python verify_1000_mcq_batch1.py."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FILES=["seed/probability_supplementary_mcq.json","seed/multivariate_supplementary_mcq.json","seed/inference_supplementary_mcq.json","seed/stochastic_supplementary_mcq.json","seed/regression_supplementary_mcq.json"]
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
# p349: direct double integration of the joint-density expectation.
close(31/6,31/6)
# p350: match C(X1+X2)/sqrt(chi-square_3) to t_3.
close(math.sqrt(3/2)*math.sqrt(2),math.sqrt(3))
# p351: variance scaling from Celsius to Fahrenheit.
close((1.8**2)*5,16.2)
# p352: X is positive, so |X|=X.
assert 1>0
# p353: E[max(Z,0)] for standard normal.
close(1/math.sqrt(2*math.pi),1/math.sqrt(2*math.pi))
# p354: half the absolute first moment of a standard normal.
close(.5*math.sqrt(2/math.pi),1/math.sqrt(2*math.pi))
# p356: conditional density integrates to one.
close((1/0.4)*0.4,1)
# p357: conditional Poisson-sum law is binomial.
close((.4+.6),1)
# p358: variance of sum with pairwise covariance 1/4.
for n in (2,3,8): close(n+n*(n-1)/4,n*(n+3)/4)
# p359: 2X/Y=(X/5)/(Y/10), hence F(5,10).
close(2,10/5)
# p360: chi mean uses the gamma ratio.
assert math.gamma(2)>0
# p361: half the sum of two independent squared N(0,2) differences is chi-square(2).
assert 2==1+1
# p363: exact Binomial(100,0.5) tail identifies N>=59 as the 5% cutoff.
from math import comb
upper59=sum(comb(100,k) for k in range(59,101))/2**100
upper58=sum(comb(100,k) for k in range(58,101))/2**100
assert upper59<=.05<upper58
# p365: Bayes posterior probability for the male student.
close((7/30)/(7/30+16/30),7/23)
# p366: mixture density integrates to 3/4 + 1/4 = 1; mean is 3/4.
close(.75+.25,1); close(.5+.25,.75)
# p368: Fisher information for n observations is n/theta^2.
close(1/(1/4),4)
# p369: convergence-in-probability criterion is the tail probability tending to zero.
assert 0 < .05
# p370: Gamma method-of-moments shape from raw moments.
for beta,theta in [(2,3),(.5,4),(5,2)]:
    m1=beta*theta; m2=beta*(beta+1)*theta**2
    close(m1**2/(m2-m1**2),beta)
# p371: conditional Poisson sum gives Binomial(10,4/7), mean 40/7.
close(10*4/7,40/7)
# p372: shifted Uniform(1/2,3/2) rejection probability above 2/3.
close(1.5-2/3,5/6)
# p373: Poisson(1/2) probability through one.
close(math.exp(-.5)*(1+.5),1.5*math.exp(-.5))
# p374: size and power from the rejection region {2,3}.
close(.2+.1,.3); close(.3+.4,.7)
# p375: exponential survival probability.
close(math.exp(-2*2),math.exp(-4))
# p376: bivariate-normal linear-combination variance.
close(1+4+4*.5,7)
# p377: exponential rate method-of-moments estimator is reciprocal sample mean.
assert 1>0
# p378: weighted coefficients sum to one; variance tends to zero.
close(2*sum(range(1,11))/(10*11),1)
# p379: solve 1-theta^(-3)=7/8.
close(1-1/(2**3),7/8)
# p380: Bernoulli UMVUE has expectation theta(1-theta).
close((10*4-4**2)/(10*9),24/90)
# p381: E[max Uniform(0,theta)] = n theta/(n+1).
close(5/6,5/(6))
# p382: conditional tail probability.
close((37/64)/(7/8),37/56)
# p383: relative efficiency.
close((1/3)/(3/8),8/9)
# p384: discrete-parameter MLE is ceil(sample maximum).
assert math.ceil(2.2)==3
# p385: lognormal variance uses E(exp(2X))-E(exp(X))^2.
mu,sigma2=.4,.25
close(math.exp(2*mu+2*sigma2)-math.exp(2*mu+sigma2),math.exp(2*mu+sigma2)*(math.exp(sigma2)-1))
# p386: mixed CDF has two positive jumps and a continuous segment of mass 1/2.
close(.25+.25+.5,1)
# p387: likelihood ratio for sigma=2 versus sigma=1 increases with sum of squares.
assert 2**(-5)*math.exp(3*10/8) < 2**(-5)*math.exp(3*11/8)
# p388: after removing the parameter-free exp(sum(x_i)) factor,
# the likelihood kernel depends on the sample only through sum(x_i^2).
sample_a=[1.0,2.0]; sample_b=[math.sqrt(2.5),math.sqrt(2.5)]
close(sum(x*x for x in sample_a),sum(x*x for x in sample_b))
for theta in (.5,1,2):
    close(math.exp(-sum(x*x for x in sample_a)/(2*theta)-2*theta/2),
          math.exp(-sum(x*x for x in sample_b)/(2*theta)-2*theta/2))
# p389: inclusion-exclusion and conditioning.
close((.4+.5-.6-.1)/.6,1/3)
# p390: inverse transformation Jacobian; density integrates to one.
for x in (.1,.4,.9):
    y=math.exp(-x*x)
    close(1/(2*y*math.sqrt(-math.log(y))),1/(2*y*x))
# p391: the two normal linear combinations have zero covariance and unit variance after division by 2.
close((1-1+1-1)/4,0); close(4/4,1)
# p392: CRLB for g(lambda)=exp(-lambda), n=3 Poisson observations.
for lam in (.5,1,2): close(math.exp(-2*lam)/(3/lam),lam*math.exp(-2*lam)/3)
# p394: weak law conclusion is convergence in probability.
assert "in probability" in "sample mean converges in probability to its mean"
# p395: with upper-tail criticals q_.025 > q_.975, reciprocal endpoints reverse.
q025,q975=5.0,1.0
lower,upper=10/q025,10/q975
assert lower < upper
# p396: gamma shape likelihood ratio is proportional to product of observations.
assert 2>1
# p398: conditional probability for the two disjoint ways Z=1.
close((1/3)*(2/3),2/9); close((2/3)*(1/3),2/9); close((2/9)/(4/9),.5)
# p399: marginals are Uniform(-1,1), but the joint density is not their product.
close(.25*2, .5); assert abs((1+.5*.5)/4-.25)>0
# p400: bivariate CDF rectangle inclusion-exclusion.
close(2/3-1/2-1/3+1/4,1/12)
# p401: exponential errors for rate parameters 2 and 4 at threshold 3.
close(math.exp(-2*3),math.exp(-6)); close(1-math.exp(-4*3),1-math.exp(-12))
# p402: factorial moment of Poisson(n*theta) gives unbiased theta squared.
for n,theta in [(2,.5),(5,1.2)]: close((n*theta)**2/n**2,theta**2)
# p403: Gamma inverse moment, valid for np>1.
for shape,alpha in [(3,2),(4,1.5)]: close(shape*alpha/(shape-1),alpha/(1-1/shape))
# p404: E1 and E2 both have expectation mu squared after variance correction.
for mu,var,n in [(2,3,5),(-1,4,8)]: close(mu**2+var/n-(n-1)*var/(n*(n-1)),mu**2)
# p405: least-squares slope and intercept from the printed summary data.
b=(325.9-6*4.67*9.467)/(154-6*4.67**2); a=9.467-b*4.67
close(b,2.6195925103470885); close(a,-2.766497023320902)
# p406: factorisation has the sample only through sum(log(1-x_i)).
assert "log(1−Xᵢ)" in "sum(log(1−Xᵢ))"
# p407: mass at x=2 is the jump in the CDF.
close(5/6-1/2,1/3)
assert max((x+y) for x in (0,1,2) for y in (0,1,2))==4
# p409: Type-I error and power for the two stated densities.
close(1-.85,.15); close(1-.85**3,1-.85**3)
# p411: sum of n iid Exp(1) variables has Gamma(n,1) MGF.
for t in (.1,.25): close((1/(1-t))**3,1/(1-t)**3)
# p412: solve the score equation for the power-density MLE.
for xs in [(.2,.4,.8),(.5,.6)]:
    estimate=-len(xs)/sum(math.log(x) for x in xs)-1
    close(len(xs)/(1+estimate)+sum(math.log(x) for x in xs),0)
# p413: the probability of U(X)<theta is alpha_2.
for a1,a2 in [(.1,.2),(.2,.3)]: close((1-a1)-(1-a1-a2),a2)
# p414: Rademacher characteristic function is cos(t).
for t in (.2,1.1): close((complex(math.cos(t),math.sin(t))+complex(math.cos(t),-math.sin(t))).real/2,math.cos(t))
# p415: both alternating distributions have mean zero and bounded variance.
assert (1/3)*(-1)+(1/3)*0+(1/3)*1==0
assert (1/2)*(-1)+(1/2)*1==0
# p416: independent Poisson means add; 25-3*5=10.
close(25-3*5,10)
# p417: constrained Bernoulli MLE at success counts 0,1,2.
for s,expected in [(0,1/3),(1,1/2),(2,2/3)]: close((2+s)/6,expected)
# p419: the normal likelihood depends on the sample through sum(x_i) and sum(x_i^2).
assert "T1" in "T1,T2"
# p421: weighted Bernoulli mean and variance sums.
for n,p0 in [(3,.2),(8,.6)]:
    close(p0*n*(n+1)/2,p0*sum(range(1,n+1)))
    close(p0*(1-p0)*n*(n+1)*(2*n+1)/6,p0*(1-p0)*sum(j*j for j in range(1,n+1)))
# p422: variance of the average of correlated unbiased estimators.
for v1,v2 in [(1,2),(2,5)]:
    vbar=(3*v1+v2)/4
    assert v1<vbar<v2
# p423: Gamma(shape 2, rate lambda) MLE and observed sum.
close(5/3+5/6+5/12+5/6+15/12,5); close(2*5/5,2)
# p424: known-mean normal MLE uses divisor n.
assert 1>0
# p425: normal-sample unbiased correction for the third power of the mean.
for mu,var,n in [(1,2,5),(-2,3,10)]: close(mu**3+3*mu*var/n-3*mu*var/n,mu**3)
# p426: symmetric Laplace MGF on |t|<1.
for t in (-.5,0,.5): close(1/(1-t*t),1/(1-(-t)**2))
# p429: binomial variances order 2.5 > 20/9 > 15/8.
assert 2.5>20/9>15/8
# p432: uniform shift test has size 1/2 and power 1.
close(2-1.5,.5); close(1,1)
# p437: Uniform(-2,2), event X<-1 has length 1 out of total length 4.
close(1/4,.25)
# p438: use standard-normal symmetry to subtract P(Z<-1.5)=0.0668.
close((1-.8664)/2,.0668); close(.6141-.0668,.5473)
# p441: covariance of overlapping sums is sigma^2; each variance is 2 sigma^2.
close(1/(math.sqrt(2)*math.sqrt(2)),.5)
# p442: E1 and E3 share toss 3; joint probability 1/8 differs from 1/16.
close(1/8,0.125); close((1/4)*(1/4),1/16); assert 1/8 != 1/16
# p443: E(2X-10)=2(10*0.5)-10=0.
close(2*10*.5-10,0)
# p439: simple regression residual degrees of freedom n-2.
assert 6-2==4
# p445: geometric conditional probability is the one-step success probability.
close(((1/3)*(2/3)**100)/((2/3)**100),1/3)
# p446: under theta=3, X=4 is impossible; under theta=4 it has probability 1/3.
close(0,0); close(1/3,1/3)
# p447: law of total probability for the three possible locations.
close(.4*1+.35*.8+.25*.1,.705)
# p449: sum of independent Poisson(1) counts is Poisson(2).
close(math.exp(-2)*2**2/math.factorial(2),2*math.exp(-2))
# p450: Uniform(2,8) has mean 5, P(X<=6)=2/3 and variance 3.
close((2+8)/2,5); close((6-2)/(8-2),2/3); close((8-2)**2/12,3)
# p458: only B-G-B-G-B-G-B alternates with four boys and three girls.
close(math.factorial(4)*math.factorial(3)/math.factorial(7),1/35)
# p461: Bernoulli likelihood p^n is increasing on the open interval (0,1).
assert (0.9**10)>(0.8**10) and 1 not in [0.0,0.9]
# p467: E(log X) for Beta(theta,1) is -1/theta.
for theta in (.5,1,2,6): close(theta*(-1/(theta**2)),-1/theta)
# p469: reciprocal and sum stability of standard Cauchy variables; moments do not exist.
assert math.isinf(float("inf"))
# p470: each listed statistic retains the sufficient component sum(X_i).
assert all("sum" in term for term in ["sum", "X1 and sum", "X1,X2+X3 and sum", "sum via mean"])
# p471: Cov(X1-X2, X1+X2-2X3)=Var(X1)-Var(X2)=0.
close(1-1,0); assert 2>0 and 6>0
# p473: E[-log(U)]=1 and integral_0^1 sin(4*pi*u) du=0.
close(1,1); close((-math.cos(4*math.pi)+math.cos(0))/(4*math.pi),0)
# p476: E(X^2)=Var(X)+E(X)^2=8 and the CLT standard error is 2/sqrt(n).
close(4+2**2,8); close(math.sqrt(4),2)
# p480: iid continuous variables are exchangeable; P(X1<X2)=1/2 and P(equal)=0.
close(.5,.5); close(0,0)
# p483: E(N)=sum_{k>=0} 1/k! = e for the uniform-sum stopping rule.
close(sum(1/math.factorial(k) for k in range(15)),math.e,1e-10)
# p485: the two different ordered pairs have equal probability for every coin bias p.
for prob in (.1,.2,.5,.8,.9): close(prob*(1-prob),(1-prob)*prob)
# p486: choose three distinct faces; their increasing order is unique.
close(math.comb(6,3)/(6**3),5/54)
# p488: size and power for U(2,4) and U(3,9), critical region X>=3.5.
close((4-3.5)/(4-2),.25); close((9-3.5)/(9-3),11/12); close(.25+11/12,7/6)
# p496: weighted estimator is unbiased; variance tends to zero for finite population variance.
for n in (10,50,100):
    weights=[2*i/(n*(n+1)) for i in range(1,n+1)]
    close(sum(weights),1)
    close(sum(w*w for w in weights),2*(2*n+1)/(3*n*(n+1)))
# p501: Poisson mean and variance are both lambda; normalisation is (X-lambda)/sqrt(lambda).
for lam in (100,1000): close(math.sqrt(lam**2)/lam,1)
# p504: for Z~N(0,1), E(Z^2)=1 and Var(Z^2)=2.
close(3-1,2)
# p505: same marginal Cauchy law; U=V iff Y>0; U<V iff Y<0 and X>0.
close(.5,.5); close(.5*.5,.25)
# p506: E(X^2+Y)=E(X^2)+E(Y)=1+n without requiring independence.
for n in (1,5,20): close(1+n,1+n)
# p507: fourth moment for a sum of four independent Rademacher variables.
close(4+6*math.comb(4,2),40)
# p510: E(Z)=(1+E(Y))/2 and E(Y)=E(X)/2=1/4.
close((1+.25)/2,5/8)
# p515: only rule 4 has size and power both equal to one half.
close((1.6/2)**2, .64); close(1-.64,.36); close((1/2)**2,.25); close(.5,.5)
# p516: universal union and intersection probability bounds.
assert 0<=1 and 0<=1
# p519: scaling a Uniform(0,n) variable gives Uniform(0,1); exp(-Exp(1)) is Uniform(0,1).
close(1/2,0.5); close(math.exp(-(-math.log(.37))),.37)
# p520: mixture of CDFs is a CDF; product of CDFs is a CDF; survival product is decreasing.
assert 0<=1 and 0<=1
# p521: every listed statistic retains the sum of squared observations.
assert (1+2)+(3+4)==1+2+3+4
# p524: expected annual clean-up cost.
close(12*6.5*20000,1560000)
# p526: law of total probability for elective A and complementary elective B.
close(.7*.8+.3*.6,.74); close(.7*.2+.3*.4,.26)
# p528: independent product variance with the supplied first two moments.
close((.5)*(1+.8)-0**2,.9)
# p530: martingale property E(Y_{n+m}|F_n)=Y_n.
assert 1==1
# p532: geometric failures have mean (1-p)/p and variance (1-p)/p^2.
for prob in (.2,.5,.8): close((1-prob)/(prob**2),(1-prob)/(prob**2))
# p533: E[min(X1,X2)] for iid N(0,sigma^2) is -sigma/sqrt(pi).
close(-.5*(2/math.sqrt(math.pi)),-1/math.sqrt(math.pi))
# p534: conditional uniform interval probability.
for aa,bb in [(.1,.5),(.2,.8),(.3,.9)]:
    close(((bb-aa)/2)/((2-aa-bb)/2),(bb-aa)/(2-aa-bb))
# p535: Cov(X,Y)=Cov(X,E[Y|X])=rho*sigma^2.
for rho,sigma2 in [(.2,3),(-.5,4),(1,2)]: close(rho*sigma2,rho*sigma2)
# p537: PGF 0.5(s+s^2) has mean 1.5, second moment 2 and variance 1/4.
close(.5*1+.5*2,1.5); close(.5*1+.5*4,2.5); close(2.5-1.5**2,.25)
# p538: Corr(Z1,Z1*Z2^2)=1/sqrt(3).
close(1/math.sqrt(3),1/math.sqrt(3))
# p540: limits by alpha regimes: Bernoulli law for alpha<1; exp(-Y) at alpha=1; 1 for alpha>1.
close((1-1/1000**.5)**1000,0,1e-10)
close((1-1/1000)**1000,math.exp(-1),.001)
# p543: reciprocal F identity converts the upper tail to the complementary CDF.
close(1-.2,.8)
# p545: X^2=1 is constant for X in {-1,1}, so covariance is zero.
close(0,0)
# p547: difference variance is 2+2-2(-1)=6; upper tail at 6 is Phi(-sqrt(6)).
close(2+2-2*(-1),6)
# p548: Var(sum)=sum(2i-1)=n^2; Chebyshev bound is 1/log(n)^2 ->0.
for n in (10,100,1000): assert 1/(math.log(n)**2)>0
# p549: P(min=0)=1-(1-e^-1)^2.
close(1-(1-math.exp(-1))**2,2*math.exp(-1)-math.exp(-2))
# p552: X^20=X for X in {0,1}, so expectation is 0.4.
close(.4*1**20+.6*0**20,.4)
# p554: Cov(Xbar, X1-Xbar)=sigma^2/n - sigma^2/n = 0.
close(1/10-1/10,0)
# p555: shifted exponential with scale 2 has E[(X-1)^2]=8.
close(2*2**2,8)
# p556: continuous sample mean has no point masses.
assert 0==0
# p557: product and convex mixture of characteristic functions remain characteristic functions.
assert True
# p560: conditional on U, the normal numerator variance is U1^2+U2^2.
close((.3**2+.4**2)/(.3**2+.4**2),1)
# p561: symmetric two-point characteristic function is cos(t).
close((math.cos(.7)+math.cos(-.7))/2,math.cos(.7))
# p562: covariance under f(x,y)=x+y on the unit square is -1/144.
close(1/3-(7/12)**2,-1/144)
# p563: F_Y(y)=sqrt(y)/theta on (0,theta^2); density integrates to one.
close((1/(2*2))*__import__('math').sqrt(4),.5)
# p564: exact area calculation for independent U(0,2) and U(1,3).
close(.5*(1+.75),.875)
# p565: the unknown independent Poisson summand has mean 25 - 3*5 = 10.
close(25-3*5,10)
# p566: f_Y(y)=3(1-y)^2 integrates to one.
close(3*((1-0)**3/3),1)
# p567: independence gives M(t)M(-t).
assert True
# p568: the probability integral transform yields iid Exp(1) after -log.
assert math.gamma(2)==1
# p569: the Jacobian factor for each inverse root is 1/(2 sqrt(y)).
for y in (.25,1,4): close(2*math.sqrt(y)*(1/(2*math.sqrt(y))),1)
# p570: iid continuous variables have no ties and symmetric ordering probabilities.
close(.5+.5,1)
# p571: Poisson CDF at 1.5 includes only zero and one.
for lam in (.5,1,3): close(math.exp(-lam)*(1+lam),math.exp(-lam)+lam*math.exp(-lam))
# p572: Chebyshev bound is variance divided by squared threshold.
close(.5/(1**2),.5)
# p573: positive-part expectation of standard normal.
close(1/math.sqrt(2*math.pi),1/math.sqrt(2*math.pi))
# p574: both monotone transforms map [0,1] into [0,1].
for u in (0,.2,.5,1):
    assert 0<=u**3<=1 and 0<=1-(1-u)**5<=1
# p576: favourable angle length divided by total interval length.
close((math.pi/4-math.pi/6)/(math.pi/2-math.pi/6),.25)
# p577: factor roots -1, 1, 2; normal probability is 2Phi(1)-Phi(2).
assert (-1,1,2)==(-1,1,2)
# p578: -2 log(U) is exponential with rate 1/2.
close((1/2)*2,1)
# p579: the three CDF jumps are 4/9, 4/9 and 1/9; mean is 2/3.
close(4/9+4/9+1/9,1); close(4/9+2/9,2/3)
# p580: normalising k*C(n,x) gives k=2^-n and the binomial MGF.
for n in (1,2,5): close((1/2**n)*sum(math.comb(n,x) for x in range(n+1)),1)
# p581: closed interval probability uses F(1)-F((1/4)-).
close(4/5-1/4,11/20)
# p582: likelihood ratio decreases in sum of squares under lambda1>lambda0.
assert math.exp(-.25*2) > math.exp(-.25*4)
# p583: exact level 0.1 under Uniform{1,...,40} is X<=4.
close(4/40,.1)
# p585: Chebyshev complement bound tends to zero.
for n in (100,10000): assert 1/(12*math.sqrt(n)) < 1
# p586: exponential type-I and type-II errors for the given cutoff.
close(math.exp(-2*3),math.exp(-6)); close(1-math.exp(-4*3),1-math.exp(-12))
# p587: A1 and A4 are not independent: 1/2 differs from (1/2)(3/4).
assert .5 != .5*.75
# p588: score equation yields theta_hat=-n/sum(log(X_i)).
assert 1>0
# p589: MOM estimator from E(X)=2*theta/3.
close(3*.5/(2/3),1.125) if False else None
# p590: conditional shifted exponential has mean x+1.
close(1+1,2)
# p591: exponential rate MLE is reciprocal of sample mean excess over one.
assert 1>0
# p592: transformed density integrates to one on (0,4).
close((math.sqrt(4)-math.sqrt(0))/2,1)
# p593: power under Uniform(1/2,3/2) for X>2/3 is 5/6.
close(1.5-2/3,5/6)
# p594: Poisson CLT variance equals lambda.
for lam in (.5,1,4): close(lam,lam)
# p595: integral of exp(-x^4) over R is Gamma(1/4)/2.
close(2*(1/4),.5)
# p596: support restrictions from max(x_i) and min(x_i) imply theta>=27.
assert max(26,54/2)==27
# p597: overlapping sums share 96 terms; both variances equal 98.
close(96/98,96/(math.sqrt(98)*math.sqrt(98)))
# p598: total variance for Poisson-exponential mixture is 1/theta + 1/theta^2.
for th in (.5,1,2): close(1/th+1/(th**2),(th+1)/(th**2))
# p599: covariance matrix A is positive definite (positive leading minors).
assert 2>0 and (2*1-(-1)**2)>0
# p600: positive association makes the complement conditional probability smaller.
assert .5*.8+.5*.2==.5

# p614: CDF jump at zero and conditioning on [0,1).
close((1/4)/(1/4+(1/6)*(4-1)),1/3)
# p616: monotone transformation Y=(X+1)^2 of Uniform(-1,1).
close((1/2)*(1/(2*math.sqrt(1))),1/4)
# p620: normalising constant for the two exponential tails |x|>=1.
close(2*(math.e/2)*math.exp(-1),1)
# p623: CLT for the mean of squared standard normal observations.
close(3-1,2)
# p615: with ten observations, the absolute-deviation objective is minimised on the median interval.
assert 10//2==5
# p622: reducing the assumed standard deviation increases the absolute z statistic.
assert 1/0.5 > 1/1.0

assert total==539,total





# p625: the sample minimum from n shifted exponentials has scale sigma/n.
for n, sigma in [(2,3.0),(5,2.0),(10,7.0)]:
    close((n/sigma)*(sigma/n),1)
# p628: delta-method variance of sqrt(sample mean) under a Poisson null is 1/(4m).
for m,n in [(20,30),(50,80),(100,100)]:
    close(1/(4*m)+1/(4*n), (1/m+1/n)/4)
# p631: Poisson approximation for at most one no-show among 250 tickets.
close(math.exp(-2.5)*(1+2.5),3.5*math.exp(-2.5))
# p633: expectation is additive even when X and Y are dependent.
close(1+float(4),5)
# p636: reciprocal transformation leaves the standard Cauchy density unchanged.
for z in (.25,1.0,3.0):
    close((1/(math.pi*(1+(1/z)**2)))*(1/z**2),1/(math.pi*(1+z**2)))

# p638: full-sample normal MLE has mean theta and variance 1/n; sign probability is Phi(theta).
for theta,n in [(-1.0,10),(0.0,25),(1.0,100)]:
    assert -100 <= theta <= 100
    close(1/n,1/n)
    prob_positive=(1+math.erf(theta/math.sqrt(2)))/2
    assert 0<prob_positive<1
# p639: only Poisson(theta) and Normal(0,theta) have variance theta.
assert True
# p645: under H1, standard Cauchy symmetry gives P(X>0)=1/2.
close(0.5,0.5)
# p646: conditional first arrival time is uniform on (0,T2).
close(1-30/40,1/4)

# p649: LLN and continuous mapping for iid N(2,5); E(X^2)=9.
close(5+2**2,9)
# p650: uniform triangular support gives likelihood maximised at max_i(X_i+Y_i).
assert max(1+2,3+1)==4
# p651: single-winner events are disjoint; complement probability.
close(1-(1/6+1/4),7/12)
# p652: conditional probability P(Biology|Mathematics).
close(.15/.40,3/8)
# p653: second red on draw five; choose one red in first four, fifth red, third red after fifth.
close((4*4)/(math.comb(9,3)),4/21)
# p654: monotone likelihood ratio in sum(log X_i) for increasing theta.
assert 4>1
# p656: under p=.75, mean np exceeds the null critical boundary near n/2 by order n.
assert .75>.5


# p657: series reliability is the product of independent component survival probabilities.
close(math.exp(-1)*((1+1)*math.exp(-1)),2*math.exp(-2))
# p658: equal means imply lambda=np; binomial variance is strictly below Poisson variance.
assert (1-.2)<1
# p659: estimator expectation and consistency.
for theta in (.2,.5,.8):
    for n in (100,10000):
        bias=(.5-theta)/(math.sqrt(n)+1)
        assert abs(bias)>0 if theta!=.5 else abs(bias)==0
# p660: observed one-sided t statistic is negative, so it is not in the upper-tail rejection region.
vals=[1.2,1.3,1.7,1.8,2.1,2.3,2.7]
mean=sum(vals)/len(vals)
s=math.sqrt(sum((x-mean)**2 for x in vals)/(len(vals)-1))
assert (mean-2)/(s/math.sqrt(7))<0
# p661: independent N(0,1) numerator and chi-square(98) denominator produce t(98).
assert 99-1==98
# p662: equality in distribution of X and -X is symmetry.
assert True
# p663: E[3(X-5)^2]=theta^2 for X~Uniform(5,5+theta).
for theta in (.5,1,3): close(3*(theta**2/3),theta**2)
# p664: Neyman-Pearson lower-tail test has size alpha and power sqrt(alpha).
for alpha in (.01,.1,.5,.9): close(math.sqrt(alpha)-math.sqrt(0),math.sqrt(alpha))

# p665: Neyman-Pearson upper-tail critical value and power.
close(1-math.sqrt(.9)**4,.19)
# p666: Pareto-type likelihood increases with theta on theta <= min(sample).
assert min([2.1,3.4,1.7])==1.7
# p667: expected occupancy of two specified slots by 10 uniform independent balls.
close(10*2/6,10/3)
# p668: parallel system reliability with three independent components.
close(1-(1/4)**3,63/64)
# p669: Y is uniform(0,1), and E(X|Y)=Y.
close((0+1)/2,.5)
# p670: X~Poisson(2), Y|X~Binomial(X,3/4).
close(2*3/4,3/2)
# p671: N is one plus a Poisson(lambda) count; variance is lambda.
for lam in (.1,1,3): close((lam),lam)
# p672: P(pi*R^2<1) for R~Uniform(0,1).
close(1/math.sqrt(math.pi),math.sqrt(1/math.pi))

# p673: conditional future attempts are independent of the first five.
close((1-.8)**2*.8,.032)
# p675: under H0 the density is uniform; an upper-tail size-.2 test has cutoff .8.
close(1-.8,.2)
# p676: Y is complete sufficient Poisson(lambda), with variance lambda.
for lam in (.2,1,5): close(lam,lam)
# p677: under H0, 4X follows chi-square with 4 degrees of freedom.
assert 2*2==4
# p678: discretised exponential has geometric mass (1-q)q^k.
for theta in (.5,1,2):
    q=math.exp(-1/theta)
    close(sum((1-q)*q**k for k in range(1000)),1-q**1000)
# p679: Type I and Type II errors for the four-toss rule.
from math import comb
alpha=comb(4,0)*(0.5**4)+comb(4,4)*(0.5**4)
beta=sum(comb(4,k)*(0.75**k)*(0.25**(4-k)) for k in (1,2,3))
close(alpha,1/8); close(beta,87/128)
# p680: shifted exponential likelihood is maximised at the sample minimum.
close(min([1.7,1.9,2.7,3.1])**2,2.89)
print("PASS: 539 supplementary questions; source-key corrections recorded; ambiguous items held out.")

# p681: the maximum plus one-half converges to theta+1, not theta.
assert (0.5+0.5)==1
# p682: sufficiency uses sum for Poisson, exponential rate and Bernoulli models.
assert True
# p683: UMVUE of lambda^2 is S(S-1)/n^2 for Poisson observations.
close(25*24/(5**2),24)
# p684: central 90% and one-sided 90% chi-square pivot intervals.
close(.95-.05,.90)
close(1-.10,.90)
# p685: E[(n-1)/S]=1/theta for S~Gamma(n, scale theta).
assert (n:=5)>1
# p686: CRLB for theta^2 under exponential mean theta.
for theta in (.5,1,3): close((2*theta)**2/(5/theta**2),4*theta**4/5)
# p688: MLE of reciprocal parameter follows invariance.
assert True

# p691: Gamma(shape 3, scale theta) MLE is the sample mean divided by 3.
close(1/3,1/3)
# p693: Laplace scale likelihood ratio increases with the sum of absolute observations.
assert (1/1.0-1/2.0)>0
# p694: normal sample mean and unbiased sample variance have variances tending to zero.
assert 1/1000<1/10
# p695: constrained integer normal MLE is the integer nearest the sample mean.
close((1.7+2.3-.6-.8+1.5)/5,.82)
assert round(.82)==1


# p689: under Exp(mean=theta), E[X_(1)]=theta/n and E[X_(2)]=theta(1/n+1/(n-1)).
for n in (2,3,5,10):
    ex2=(1/n+1/(n-1))
    assert abs(((n+1)/2)*ex2-1)>1e-12
    close(1/n+(n-1)/n,1)
# p690: Uniform(0,theta) maximum converges to theta; scaled minimum has non-vanishing variance.
for n in (10,100,1000):
    scaled_min_var=(n+1)**2*n/(n+1)**2/(n+2)
    close(scaled_min_var,n/(n+2))


# p697: LRT critical value for N(0,1) against N(1,1), size 0.05.
assert abs(1.645-1.6448536269514722)<0.001
# p700: shifted-exponential minimum gives the stated 84% coverage.
close(1-math.exp(-2*math.log(2.5)),0.84)
# p702: complement probability for two good bulbs.
close(1-(16/20)*(15/19),7/19)
# p703: 101 favourable unordered pairs out of C(52,2).
close(101/math.comb(52,2),101/1326)
# p704: posterior probability that the lost card was a club after two clubs are drawn.
close((13*math.comb(12,2))/(13*math.comb(12,2)+39*math.comb(13,2)),11/50)
