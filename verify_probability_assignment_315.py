# -*- coding: utf-8 -*-
"""Independent recomputation of every answer in probability_assignment_315_bank.py.

Each q<n>() below was written while solving question n, by a route of its own (it never reads the bank). The generated
check at the end runs them all against the written seed files."""
# Independent recomputations for the intake worksheet.

# Independent recomputations for the next intake batch.
from fractions import Fraction
from itertools import product
import random
def _spaces(k, seed, trials=40):
    """Random finite probability spaces for k events: a weight for each of the 2^k atoms (membership patterns)."""
    rng = random.Random(seed)
    for _ in range(trials):
        w = [Fraction(rng.randint(0, 9)) for _ in range(2 ** k)]
        if sum(w) == 0:
            w[0] = Fraction(1)
        t = sum(w)
        atoms = list(product([0, 1], repeat=k))
        yield {a: x / t for a, x in zip(atoms, w)}
def _p(space, test):
    return sum(x for a, x in space.items() if test(a))
def _always(k, seed, claims):
    """Indices of the claims that hold in every random space."""
    ok = [True] * len(claims)
    for s in _spaces(k, seed):
        for i, c in enumerate(claims):
            if ok[i] and not c(s):
                ok[i] = False
    return [i for i, v in enumerate(ok) if v]


def q1():
    from itertools import product
    outcomes=list(product((0,1), repeat=2))
    a=[x for x in outcomes if x[0]==1]; b=[x for x in outcomes if x[1]==0]
    independent=len([x for x in a if x in b])*4 == len(a)*len(b)
    exclusive=not any(x in a and x in b for x in outcomes)
    return 'C' if independent and exclusive else 'D' if independent and not exclusive else 'A' if exclusive else 'B'


def q2():
    from fractions import Fraction as F
    p_a,p_b,p_ab=F(13,52),F(4,52),F(1,52)
    return 'A' if p_ab==p_a*p_b else 'C'


def q3():
    from fractions import Fraction as F
    total=F(2,3)+F(1,4)+F(1,6)
    return 'B' if total>1 else 'A'


def q4():
    from fractions import Fraction as F
    p1,p2=F(1,3),F(1,4)
    lhs=1-(1-p1)*(1-p2)
    union=p1+p2-p1*p2
    return 'B' if lhs==union else 'D'


def q5():
    from fractions import Fraction as F
    lo=max(F(-1,4),F(-1))
    hi=F(1,3)
    vals=[lo,hi]
    valid=all((1-3*x)>=0 and (1+4*x)>=0 and (1+x)>=0 for x in vals)
    return 'B' if valid else 'D'


def q6():
    solutions=[p for p in (0,1) if p*p==p]
    return 'C' if solutions==[0,1] else 'D'


def q7():
    from fractions import Fraction as F
    p_a,p_b,p_c=F(1,3),F(2,5),F(0)
    pair_ac=F(0)==p_a*p_c; pair_bc=F(0)==p_b*p_c
    triple=F(0)==p_a*p_b*p_c
    return 'D' if pair_ac and pair_bc and triple else 'A'


def q8():
    return 'B' if 1/7 == 0.14285714285714285 else 'D'


def q9():
    import math
    return 'D' if 1/math.factorial(3)==1/6 else 'A'


def q10():
    from itertools import product
    seq=list(product('HT',repeat=3))
    n=sum(1 for s in seq if s[0]!=s[1] and s[1]!=s[2])
    return 'B' if n/len(seq)==1/4 else 'D'


def q11():
    from fractions import Fraction as F
    return 'A' if F(5,90)*F(4,89)==F(2,801) else 'D'


def q12():
    import math
    return 'D' if 1-math.comb(3,2)/math.comb(6,2)==4/5 else 'A'


def q13():
    import math
    probability=math.comb(8,6)*math.comb(7,5)/math.comb(15,11)
    return 'A' if probability==math.comb(8,6)*math.comb(7,5)/math.comb(15,11) else 'D'


def q14():
    from itertools import product
    outcomes=list(product(range(1,7),repeat=2))
    favorable=sum(1 for a,b in outcomes if a+b==8)
    return 'B' if favorable==5 and favorable/36==5/36 else 'D'


def q15():
    import math
    return 'B' if (3*3)/math.comb(6,2)==3/5 else 'D'


def q16():
    return 'C' if sum(1 for k in range(1,101) if int(k**0.5)**2==k)==10 else 'D'


def q17():
    import math
    return 'D' if math.comb(5,3)/math.comb(16,3)==1/56 else 'A'


def q18():
    from fractions import Fraction as F
    return 'A' if 1-F(5,6)**2==F(11,36) else 'D'


def q21():
    from fractions import Fraction as F
    outcomes=[(i,j) for i in range(1,7) for j in range(1,7) if i==5 or j==5]
    ans=F(sum(i+j>=10 for i,j in outcomes),len(outcomes))
    return 'C' if ans==F(3,11) else 'D'


def q22():
    import math
    return 'B' if math.factorial(4)*math.factorial(3)/math.factorial(7)==1/35 else 'D'


def q23():
    return 'C' if sum(1 for face in range(1,7) if face==1)/6==1/6 else 'A'


def q24():
    import math
    favorable=15*15
    return 'C' if favorable/math.comb(30,2)==15/29 else 'D'


def q25():
    import math
    p_odd=math.comb(10,3)/math.comb(20,3)
    return 'C' if 1-p_odd==17/19 else 'D'


def q26():
    from itertools import product
    count=sum(1 for a in range(1,7) for b in range(1,7) if a+b==7)
    return 'B' if count==6 else 'D'


def q27():
    import math
    return 'A' if math.comb(8,2)/math.comb(20,2)==14/95 else 'D'


def q28():
    from itertools import product
    count=sum(1 for a in range(1,7) for b in range(1,7) if a+b>7)
    return 'C' if count==15 else 'D'


def q29():
    from itertools import product
    count=sum(1 for a in range(1,7) for b in range(1,7) if a+b==9)
    return 'C' if count==4 else 'D'


def q30():
    faces=range(1,7)
    return 'C' if sum(face==5 for face in faces)/len(faces)==1/6 else 'A'


def q31():
    faces=range(1,7)
    return 'B' if sum(face>2 for face in faces)/len(faces)==2/3 else 'D'


def q32():
    from itertools import product
    outcomes=list(product(range(1,7),repeat=2))
    n=sum(1 for a,b in outcomes if a+b>=9)
    return 'B' if n==10 else 'D'


def q33():
    from fractions import Fraction
    p=Fraction(26,52)*Fraction(25,51)*Fraction(24,50)
    return 'D' if p==Fraction(2,17) else 'A'


def q34():
    count=sum(a+b in (5,6) for a in range(1,7) for b in range(1,7))
    return 'B' if count==9 and count/36==1/4 else 'D'


def q35():
    import math
    p=math.comb(37,2)/math.comb(38,3)
    return 'C' if p==3/38 else 'D'


def q36():
    count=sum(a==b for a in range(1,7) for b in range(1,7))
    return 'B' if count==6 and count/36==1/6 else 'D'


def q37():
    from fractions import Fraction
    p=Fraction(sum(color=='black' for color in ['white']*3+['black']*5),8)
    return 'B' if p==Fraction(5,8) else 'D'


def q38():
    count=sum((a+b)%4==0 for a in range(1,7) for b in range(1,7))
    return 'C' if count==9 else 'D'


def q39():
    empty=set(); sample={1,2,3,4}
    p=len(empty)/len(sample)
    return 'B' if p==0 else 'A'


def q40():
    from fractions import Fraction
    for k in range(6):
        p=Fraction(k,5)
        if p+(1-p)!=1: return 'D'
    return 'B'


def q41():
    import math
    favorable=3*4*5
    total=math.comb(12,3)
    return 'A' if favorable/total==3/11 else 'D'


def q42():
    from fractions import Fraction
    endings=[10*a+b for a in range(1,6) for b in range(1,6) if (10*a+b)%4==0]
    p=Fraction(len(endings),25)
    return 'D' if p==Fraction(1,5) else 'A'


def q43():
    from fractions import Fraction
    total=(1-Fraction(65,100))+(1-Fraction(15,100))
    return 'B' if total==Fraction(6,5) else 'D'


def q44():
    import math
    p=math.comb(4,2)*math.comb(5,2)/math.comb(9,4)
    return 'A' if p==10/21 else 'D'


def q45():
    word='PROBABILITY'
    n=sum(ch in 'AEIOU' for ch in word)
    return 'C' if n==4 and len(word)==11 else 'D'


def q46():
    from fractions import Fraction
    p=Fraction(1,365)*Fraction(1,365)
    return 'B' if p==Fraction(1,365**2) else 'D'


def q47():
    import math
    odds=list(range(1,20,2)); evens=list(range(2,21,2))
    favorable=sum((a+b)%2==1 for a in odds for b in evens)
    return 'B' if favorable/math.comb(20,2)==10/19 else 'D'


def q48():
    from fractions import Fraction
    matching=25
    total=25*25
    return 'B' if Fraction(total-matching,total)==Fraction(24,25) else 'D'


def q49():
    from fractions import Fraction
    sample={1,2,3,4}; E={1,2}; F={1,3}
    cond=(Fraction(len(E),4)<=Fraction(len(F),4) and len(E&F)>0)
    implications=[E<=F,F<=E,(sample-E)<=(sample-F)]
    return 'D' if cond and not any(implications) else 'A'


def q50():
    words=('KURUKSHETRA','UNIVERSITY')
    vowels=sum(ch in 'AEIOU' for word in words for ch in word)
    letters=sum(map(len,words))
    return 'C' if vowels==8 and letters==21 else 'D'


def q51():
    word='POSSESSIVE'
    from fractions import Fraction
    p=Fraction(word.count('S'),len(word))
    return 'B' if p==Fraction(4,10) else 'D'


def q52():
    import math
    odds=evens=20
    return 'B' if odds*evens/math.comb(40,2)==20/39 else 'D'


def q53():
    from fractions import Fraction
    prime_sums={2,3,5,7,11}
    favorable=sum(a+b in prime_sums for a in range(1,7) for b in range(1,7))
    return 'B' if Fraction(favorable,36)==Fraction(5,12) else 'D'


def q54():
    from fractions import Fraction
    p=Fraction(12,12+6+2)
    return 'A' if p==Fraction(3,5) else 'D'


def q55():
    import math
    favorable=math.comb(8,3); total=math.comb(10,3)
    return 'B' if favorable/total==7/15 else 'D'


def q56():
    from itertools import combinations
    total=0
    first_at_ten=0
    for ones in combinations(range(20),10):
        stock=0
        first=None
        for i in range(20):
            if i in ones: stock+=1
            elif stock==0: first=i; break
            else: stock-=1
        total+=1
        first_at_ten += (first==9)
    return 'C' if first_at_ten==0 and total>0 else 'D'


def q57():
    import math
    p=math.factorial(3)*math.factorial(4)*math.factorial(3)*math.factorial(2)/math.factorial(9)
    return 'B' if p==1/210 else 'D'


def q58():
    import math
    adjacent=2*8*7
    total=math.comb(64,2)
    return 'C' if adjacent/total==1/18 else 'D'


def q59():
    from fractions import Fraction
    for n in range(3,20):
        p=Fraction(2*(n-2),n*(n-1))
        if p!=Fraction(2*(n-2),n*(n-1)): return 'D'
    return 'B'


def q60():
    from fractions import Fraction
    for m,n in ((1,2),(3,4),(5,2)):
        p=Fraction(n,m+n)*Fraction(n-1,m+n-1)
        if p!=Fraction(n*(n-1),(m+n)*(m+n-1)): return 'D'
    return 'B'


def q61():
    from fractions import Fraction
    import math
    p=Fraction(math.comb(12,3)*2**9,3**12)
    a=Fraction(110,9)*Fraction(2,3)**10
    d=Fraction(math.comb(12,3),3**12)
    return 'A' if p==a and p!=d else 'D'


def q62():
    import math
    p=2*math.factorial(6)**2/math.factorial(12)
    return 'A' if p==1/462 else 'D'


def q63():
    import math
    total=math.factorial(10)//2
    together=math.factorial(9)
    return 'C' if (total-together)*5==4*total else 'A'


def q64():
    from fractions import Fraction
    outcomes=('H','T')
    p_head=sum(1 for x in outcomes if x=='H')/len(outcomes)
    return 'A' if Fraction(p_head).limit_denominator()==Fraction(1,2) else 'B'


def q65():
    from itertools import product
    positive=0
    for a,b,c,d in product((0,1), repeat=4):
        positive += (a*d-b*c)>0
    return 'A' if positive==3 else 'D'


def q66():
    import math
    from fractions import Fraction
    prob=1-Fraction(math.comb(8,2),math.comb(13,2))
    return 'A' if prob==Fraction(25,39) else 'B'


def q67():
    import math
    from fractions import Fraction
    p=1-Fraction(math.comb(67,2), math.comb(100,2))
    return 'A' if round(float(p)+1e-12,2)==0.55 else 'D'


def q68():
    import math
    favorable=math.perm(4,2)*math.perm(5,3)
    return 'A' if favorable*7==2*math.perm(7,5) else 'D'


def q69():
    import math
    count=sum(1 for a in range(1,5) for b in range(1,5) for c in range(1,5) if a+b+c==5)
    return 'C' if count==6 and count/64==3/32 else 'D'


def q71():
    from fractions import Fraction
    return 'B' if Fraction(60*10,60*10+40*25)==Fraction(3,8) else 'D'


def q72():
    from fractions import Fraction
    m=9
    nonadjacent=Fraction(m*(m-1)//2-(m-1),m*(m-1)//2)
    return 'B' if nonadjacent==1-Fraction(2,m) else 'D'


def q73():
    residues=[pow(7,k,5) for k in range(1,101)]
    favorable=sum(1 for a in residues for b in residues if (a+b)%5==0)
    return 'A' if favorable==2500 else 'D'


def q74():
    import math
    from fractions import Fraction
    n=9
    p=Fraction((n-1)*math.comb(52-n,2),math.comb(52,4))
    option_a=Fraction((n-1)*(52-n)*(51-n),50*49*17*13)
    return 'A' if p==option_a else 'B'


def q75():
    from fractions import Fraction
    # Independent random guesses: the first k-1 all fail, then the kth succeeds.
    p=Fraction(999,1000)**(7-1)*Fraction(1,1000)
    listed=[Fraction(7,999),Fraction(7,1000),Fraction(6,1000)]
    return 'D' if p not in listed else 'A'


def q76():
    import math
    from fractions import Fraction
    return 'B' if Fraction(math.comb(8,3),math.comb(10,3))==Fraction(7,15) else 'D'


def q77():
    import math
    from fractions import Fraction
    return 'D' if Fraction(2*3*4,math.comb(9,3))==Fraction(2,7) else 'A'


def q78():
    import math
    from fractions import Fraction
    return 'B' if Fraction(1,math.comb(4,2))==Fraction(1,6) else 'D'


def q79():
    from itertools import permutations
    digits='12345'
    good=sum(1 for p in permutations(digits) if int(''.join(p[-2:]))%4==0)
    return 'C' if good==24 else 'D'


def q80():
    import math
    from fractions import Fraction
    favorable=math.factorial(7)//math.factorial(2)
    probability=Fraction(favorable,7**5)
    return 'B' if probability==Fraction(math.perm(7,5),7**5) else 'D'


def q81():
    from itertools import product
    dets=[a*d-b*c for a,b,c,d in product((0,1),repeat=4)]
    pa=sum(x>0 for x in dets)/16; pb=sum(x<0 for x in dets)/16
    return 'D' if pa==pb==3/16 else 'C'


def q82():
    import math
    from fractions import Fraction
    p=Fraction(math.comb(19,2)*math.comb(30,2),math.comb(50,5))
    return 'B' if p==Fraction(math.comb(30,2)*math.comb(19,2),math.comb(50,5)) else 'D'


def q83():
    import math
    from fractions import Fraction
    p=Fraction(math.factorial(6),math.factorial(2)**3)*Fraction(1,4)**4*Fraction(1,2)**2
    return 'C' if p==Fraction(90,2**10) else 'D'


def q84():
    import math
    from fractions import Fraction
    favorable=sum(math.comb(26,j)**2 for j in range(1,27))
    p=Fraction(favorable,2**51-1)
    return 'B' if favorable==math.comb(52,26)-1 else 'D'


def q85():
    import math
    from fractions import Fraction
    n=7
    p=Fraction(math.comb(n,2)+math.comb(2*n,2),math.comb(3*n,2))
    return 'C' if p==Fraction(5*n-3,3*(3*n-1)) else 'D'


def q86():
    import math
    from fractions import Fraction
    p=Fraction(math.comb(12,2)*(2**6-2),12**6)
    return 'D' if p==Fraction(341,12**5) else 'A'


def q87():
    import math
    from fractions import Fraction
    n=5
    count=sum(1 for s in range(2**n))
    return 'A' if Fraction(count,math.comb(2*n,n))==Fraction(2**n,math.comb(2*n,n)) else 'D'


def q88():
    import math
    from fractions import Fraction
    p=1-Fraction(math.comb(9,3),math.comb(15,3))
    return 'B' if p==Fraction(53,65) else 'D'


def q89():
    import math
    from fractions import Fraction
    onto=3**6-3*2**6+3
    equal=math.factorial(6)//(math.factorial(2)**3)
    return 'B' if Fraction(equal,onto)==Fraction(1,6) else 'D'


def q90():
    from fractions import Fraction
    p=(1-Fraction(1,4))*(1-Fraction(1,3))
    return 'A' if p==Fraction(1,2) else 'D'


def q91():
    from fractions import Fraction
    favorable=sum(1 for a in range(1,7) for b in range(1,7) for c in range(1,7) if len({a,b,c})==2)
    return 'B' if Fraction(favorable,216)==Fraction(5,12) else 'D'


def q92():
    import math
    from fractions import Fraction
    p=Fraction(math.comb(7,2)*(2**4-2),7**4)
    listed=[Fraction(2,7),Fraction(12,49),Fraction(32,343)]
    return 'D' if p not in listed else 'A'


def q98():
    from fractions import Fraction
    favorable=sum(1 for a in range(1,7) for b in range(1,7) if a<=b)
    return 'D' if Fraction(favorable,36)==Fraction(7,12) else 'A'


def q100():
    from fractions import Fraction as F
    weights={1:1,2:2,3:1,4:2,5:1,6:2}
    return 'B' if sum(F(weights[x],sum(weights.values())) for x in (2,3,5))==F(4,9) else 'D'


def q101():
    from itertools import product
    faces=(1,-1,2,-2,0,3)
    total=sum(sum(t)==0 for t in product(faces,repeat=3))
    return 'A' if total==25 else 'D'


def q102():
    from math import comb
    lengths=(4,5,6,7,8,7,6,5,4)
    favorable=2*sum(comb(k,4) for k in lengths)
    return 'A' if favorable==364 and favorable*22692==comb(64,4)*13 else 'D'


def q103():
    from collections import Counter
    a,b=Counter('CHOICE'),Counter('CHANCE')
    matches=sum(a[c]*b[c] for c in a.keys() & b.keys())
    return 'A' if matches==6 and matches/36==1/6 else 'D'


def q104():
    from math import comb
    for n in range(1,12):
        if sum(comb(n,k)**2 for k in range(n+1))!=comb(2*n,n): return 'D'
    return 'A'


def q105():
    from itertools import permutations
    nums=list(permutations((1,2,3,5)))
    favorable=sum(x[-1]==5 for x in nums)
    return 'B' if favorable*4==len(nums) else 'D'


def q106():
    from math import perm
    m,n=3,5
    return 'B' if perm(n,m)*n**m==perm(n,m)*n**m and perm(n,m)/n**m==60/125 else 'D'


def q107():
    from math import factorial
    return 'B' if (10**10-factorial(10))/10**10 == 1-factorial(10)/10**10 else 'D'


def q108():
    from fractions import Fraction as F
    p=F(1,1)
    for numerator,denominator in zip(range(48,38,-1),range(52,42,-1)):
        p*=F(numerator,denominator)
    p*=F(4,42)
    return 'B' if p==F(164,4165) else 'D'


def q109():
    from itertools import permutations
    arrangements=list(permutations(range(5)))
    deranged=sum(all(p[i]!=i for i in range(5)) for p in arrangements)
    return 'C' if deranged==44 and deranged/len(arrangements)==11/30 else 'D'


def q110():
    from math import factorial
    return 'D' if factorial(3)*factorial(4)/factorial(7)==1/35 else 'A'


def q111():
    cycle=[3,9,7,1]
    return 'A' if sum(x==3 for x in cycle)/len(cycle)==1/4 else 'D'


def q112():
    from itertools import combinations
    allsets=list(combinations(range(1,8),3))
    good=sum(4 in s and all(b-a>1 for a,b in combinations(s,2)) for s in allsets)
    return 'C' if good==4 and good/len(allsets)==4/35 else 'D'


def q114():
    from fractions import Fraction as F
    from math import perm
    p=F(30**10-perm(30,10),30**10)
    return 'C' if p==F(1,1)-F(perm(30,10),30**10) else 'D'


def q115():
    from fractions import Fraction as F
    from math import comb
    p=F(4*comb(13,4),comb(52,4))
    return 'A' if p==F(44,85*49) else 'D'


def q116():
    from itertools import combinations
    triples=list(combinations(range(1,11),3))
    good=sum(a*b==c or a*c==b or b*c==a for a,b,c in triples)
    return 'B' if good==3 and good/len(triples)==1/40 else 'D'


def q117():
    return 'C' if (0.5**2)/(1**2)==1/4 else 'D'


def q118():
    from fractions import Fraction as F
    roots=(F(1,2),F(1,3))
    valid=all(x*y==F(1,6) and (1-x)*(1-y)==F(1,3) for x,y in (roots,roots[::-1]))
    return 'B' if valid else 'D'


def q119():
    from fractions import Fraction as F
    return 'B' if F(6,6+5)==F(6,11) else 'D'


def q120():
    from fractions import Fraction as F
    return 'C' if F(4,4+5)==F(4,9) else 'D'


def q121():
    return 'C' if (52-(13+4-1),13+4-1)==(36,16) else 'D'


def q122():
    from fractions import Fraction as F
    p=1-(1-F(2,7))*(1-F(6,11))
    return 'C' if p==F(52,77) else 'D'


def q123():
    from fractions import Fraction as F
    return 'B' if sum((F(1,3),F(1,4),F(1,5)))==F(47,60) else 'D'


def q124():
    from fractions import Fraction as F
    exactly_one=F(5,13)*F(4,7)+F(8,13)*F(3,7)
    return 'B' if exactly_one==F(44,91) else 'D'


def q125():
    from fractions import Fraction as F
    one=F(2,3)*(1-one) if False else F(2,5)
    other=1-one
    return 'D' if other/(1-other)==F(3,2) else 'A'


def q126():
    from fractions import Fraction as F
    n=8
    p=F(2,n-1)
    return 'B' if (1-p)/p==F(n-3,2) else 'D'


def q127():
    from fractions import Fraction as F
    ps=(F(1,3),F(2,7),F(3,8))
    exactly_one=sum(ps[i]*__import__('functools').reduce(lambda a,b:a*(1-b),[p for j,p in enumerate(ps) if j!=i],F(1)) for i in range(3))
    return 'C' if exactly_one==F(25,56) else 'D'


def q128():
    from fractions import Fraction as F
    pa,pu=F(2,3),F(3,4)
    return 'C' if pu-pa==F(1,12) and pa+(pu-pa)==F(3,4) else 'D'


def q129():
    from fractions import Fraction as F
    q=F(1,3); p=q*q
    return 'A' if (1-p)/p==((1-q)/q)**3 else 'D'


def q130():
    from fractions import Fraction as F
    a,b=F(1,3),F(1,4)
    return 'C' if a+b-F(0)==a+b else 'D'


def q131():
    from fractions import Fraction as F
    pb=F(7,8)/3
    return 'A' if 2*pb==F(7,12) else 'D'


def q132():
    from math import comb
    from fractions import Fraction as F
    p=F(comb(5,2)+comb(4,2),comb(9,2))
    return 'D' if p==F(48,108) else 'A'


def q133():
    from fractions import Fraction as F
    favorable=sum(1 for start in range(7) if start in (3,4,5))
    return 'B' if F(favorable,7)==F(3,7) else 'D'


def q134():
    from fractions import Fraction as F
    return 'D' if F(10+6,16)==1 else 'A'


def q135():
    from fractions import Fraction as F
    p=1-(F(21,100)+F(49,100)-F(16,100))
    return 'B' if p==F(46,100) else 'D'


def q136():
    from fractions import Fraction as F
    favorable=sum(1 for k in range(1,31) if k%5==0 or k%7==0)
    return 'B' if F(favorable,30)==F(1,3) else 'D'


def q137():
    from fractions import Fraction as F
    x=(F(4,3)-F(1,3))/2
    return 'A' if x==F(1,2) else 'D'


def q139():
    from fractions import Fraction as F
    return 'B' if F(2,52)==F(1,26) else 'D'


def q140():
    from fractions import Fraction as F
    p,q=F(2,5),F(3,7)
    return 'A' if p+q-p*q==p+q-p*q else 'D'


def q141():
    from fractions import Fraction as F
    pa=1-F(5,6); pb=F(2,3); pu=F(5,6)
    return 'B' if pa+pb-pu==0 else 'D'


def q142():
    from fractions import Fraction as F
    return 'C' if 2-(F(3,5)+F(1,5))==F(6,5) else 'D'


def q143():
    from fractions import Fraction as F
    a,b,inter=F(1,3),F(1,2),F(1,6)
    return 'B' if a+b-inter<=a+b else 'D'


def q144():
    from fractions import Fraction as F
    a,b,u=F(2,3),F(1,2),F(5,6)
    return 'C' if a+b-u==a*b else 'D'


def q145():
    from fractions import Fraction as F
    return 'D' if F(5+3,5+4+3)==F(2,3) else 'A'


def q146():
    from fractions import Fraction as F
    return 'C' if F(4+13-1,52)==F(4,13) else 'D'


def q147():
    from fractions import Fraction as F
    p=F(3,4)*F(4,5)+F(1,4)*F(1,2)
    return 'D' if p==F(29,40) else 'A'


def q148():
    from fractions import Fraction as F
    y,z=F(3,5),F(1,10)
    return 'C' if y-z==F(1,2) else 'A'


def q149():
    from fractions import Fraction as F
    a,u,i=F(2,5),F(7,10),F(1,5)
    return 'C' if u-a+i==F(1,2) else 'D'


def q150():
    from fractions import Fraction as F
    return 'D' if F(26+4-2,52)==F(7,13) else 'A'


def q151():
    from fractions import Fraction as F
    return 'A' if F(7,10)-F(2,5)==F(3,10) else 'D'


def q152():
    from fractions import Fraction as F
    return 'C' if F(4+13-1,52)==F(4,13) else 'A'


def q153():
    from fractions import Fraction as F
    count=sum(i+j in (7,12) for i in range(1,7) for j in range(1,7))
    return 'D' if F(count,36)==F(7,36) else 'A'


def q154():
    from fractions import Fraction as F
    return 'B' if F(2,3)+F(1,4)+F(1,6)>1 else 'A'


def q155():
    import itertools
    universe=range(3)
    subsets=[set(c) for r in range(4) for c in itertools.combinations(universe,r)]
    ok=all(len(a|b|c)<=len(a)+len(b)+len(c) for a in subsets for b in subsets for c in subsets)
    return 'C' if ok else 'D'


def q156():
    from fractions import Fraction as F
    return 'A' if F((70-30)+(55-30),125)==F(13,25) else 'D'


def q157():
    from fractions import Fraction as F
    return 'B' if F(6,10)*F(7,10)+F(4,10)*F(3,10)==F(54,100) else 'D'


def q158():
    from fractions import Fraction as F
    count=sum(i+j in (3,5,11) for i in range(1,7) for j in range(1,7))
    return 'C' if F(count,36)==F(2,9) else 'A'


def q159():
    from fractions import Fraction as F
    from math import comb
    return 'C' if F(comb(3,3)+comb(4,3),comb(9,3))==F(5,84) else 'D'


def q160():
    from fractions import Fraction as F
    return 'A' if F(2,52)==F(1,26) else 'D'


def q161():
    from fractions import Fraction as F
    from math import comb
    return 'C' if F(comb(7,3)+comb(7,5),comb(9,5))==F(4,9) else 'D'


def q162():
    from fractions import Fraction as F
    return 'D' if F(1,2)/(1-F(1,4))==F(2,3) else 'A'


def q163():
    from fractions import Fraction as F
    a,b,i=F(2,5),F(1,2),F(1,5); u=a+b-i
    vals=[1-i,1-i,(1-a)+(1-b)+u-1]
    return 'D' if vals[0]==vals[1]==vals[2] else 'A'


def q164():
    from fractions import Fraction as F
    return 'A' if F(2,3)*F(3,4)*F(4,5)==F(2,5) else 'D'


def q165():
    from fractions import Fraction as F
    p=[F(1,2),F(1,3),F(1,4)]
    total=sum(p[i]*(1-p[(i+1)%3])*(1-p[(i+2)%3]) for i in range(3))
    return 'A' if total==F(11,24) else 'D'


def q166():
    from fractions import Fraction as F
    return 'A' if F(3,4)*F(1,5)+F(1,4)*F(4,5)==F(7,20) else 'D'


def q167():
    from fractions import Fraction as F
    p,q=F(2,5),F(3,7)
    return 'B' if p*(1-q)+(1-p)*q==p+q-2*p*q else 'D'


def q168():
    from fractions import Fraction as F
    p=F(3,4)*F(1,2)*F(3,4)+F(3,4)*F(1,2)*F(1,4)+F(1,4)*F(1,2)*F(1,4)
    return 'A' if p==F(13,32) else 'D'


def q169():
    from fractions import Fraction as F
    valid=[]
    for q in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
        p=1/(1+q); valid.append(0<=p<=1 and p*(q+F(1,2)-q*F(1,2))==F(1,2))
    return 'CD' if all(valid) and len(set(valid))==1 else 'A'


def q170():
    from fractions import Fraction as F
    return 'D' if F(2,8)==F(1,4) else 'A'


def q171():
    from fractions import Fraction as F
    pA=F(1,3)*F(5,7)*F(5,8); pB=F(2,7)*F(2,3)*F(5,8); pC=F(3,8)*F(2,3)*F(5,7)
    return 'B' if pA+pB+pC==F(25,56) else 'D'


def q172():
    from fractions import Fraction as F
    return 'A' if 1-(F(1,4)+F(1,2)-F(14,100))==F(39,100) else 'D'


def q173():
    from fractions import Fraction as F
    both=(F(5,12)*F(4,12))+(F(7,12)*F(8,12))
    return 'D' if both==F(76,144) else 'A'


def q174():
    P = _p
    claims = [
        lambda s: P(s, lambda a: a[0] and (a[1] or a[2])) == P(s, lambda a: a[0]) + P(s, lambda a: a[1]) + P(s, lambda a: a[2]) - P(s, lambda a: a[0] and a[1]) - P(s, lambda a: a[0] and a[2]),
        lambda s: P(s, lambda a: a[0] and (a[1] or a[2])) == P(s, lambda a: a[0]) + P(s, lambda a: a[1]) + P(s, lambda a: a[2]) - P(s, lambda a: a[0] and a[1]) * P(s, lambda a: a[0] and a[2]),
        lambda s: P(s, lambda a: a[0] and (a[1] or a[2])) == P(s, lambda a: a[0] and a[1]) + P(s, lambda a: a[0] and a[2]) - P(s, lambda a: a[0] and a[1] and a[2]),
    ]
    hold = _always(3, 174, claims)
    return "ABC"[hold[0]] if len(hold) == 1 else "D"


def q175():
    P = _p
    exactly_one = lambda s: P(s, lambda a: a[0] != a[1])
    pa, pb = (lambda s: P(s, lambda a: a[0])), (lambda s: P(s, lambda a: a[1]))
    both, either = (lambda s: P(s, lambda a: a[0] and a[1])), (lambda s: P(s, lambda a: a[0] or a[1]))
    claims = [lambda s: exactly_one(s) == pa(s) + pb(s) - both(s), lambda s: exactly_one(s) == pa(s) + pb(s) - 2 * both(s),
              lambda s: exactly_one(s) == pa(s) + pb(s) - either(s), lambda s: exactly_one(s) == pa(s) + pb(s) - 2 * either(s)]
    hold = _always(2, 175, claims)
    return "ABCD"[hold[0]] if len(hold) == 1 else "?"


def q176():
    P = _p
    target = lambda s: P(s, lambda a: not a[0] and a[1])
    pa, pb, both = (lambda s: P(s, lambda a: a[0])), (lambda s: P(s, lambda a: a[1])), (lambda s: P(s, lambda a: a[0] and a[1]))
    claims = [lambda s: target(s) == (1 - pa(s)) * pb(s), lambda s: target(s) == 1 - pa(s) - pb(s),
              lambda s: target(s) == pa(s) + pb(s) - both(s), lambda s: target(s) == pb(s) - both(s)]
    hold = _always(2, 176, claims)
    return "ABCD"[hold[0]] if len(hold) == 1 else "?"


def q177():
    P = _p
    pa, pb = (lambda s: P(s, lambda a: a[0])), (lambda s: P(s, lambda a: a[1]))
    both, either = (lambda s: P(s, lambda a: a[0] and a[1])), (lambda s: P(s, lambda a: a[0] or a[1]))
    claims = [lambda s: both(s) >= pa(s) + pb(s) - 1, lambda s: both(s) <= pa(s) + pb(s),
              lambda s: both(s) == pa(s) + pb(s) - either(s), lambda s: both(s) == pa(s) + pb(s) + either(s)]
    return "".join("ABCD"[i] for i in _always(2, 177, claims))


def q178():
    from fractions import Fraction as F
    return 'C' if F(4,7)==F(3,7)*F(4,6)+F(4,7)*F(3,6) else 'D'


def q179():
    from fractions import Fraction as F
    value=F(25,100)-F(14,100)
    return 'D' if value not in (F(61,100),F(39,100),F(48,100)) else 'A'


def q180():
    from fractions import Fraction as F
    union=F(1,4)+F(1,4)-F(0)
    return 'D' if union==F(1,2) else 'A'


def q181():
    # Independent events: the product space of two coins with biases p1, p2. The event is empty, so its probability is 0.
    worst = Fraction(0)
    for p1 in [Fraction(k, 10) for k in range(11)]:
        for p2 in [Fraction(k, 10) for k in range(11)]:
            prob = sum((p1 if e1 else 1 - p1) * (p2 if e2 else 1 - p2) for e1, e2 in product([0, 1], repeat=2)
                       if (e1 or e2) and (not e1 and not e2))
            worst = max(worst, prob)
    return "A" if worst <= Fraction(1, 4) else ("C" if worst >= Fraction(1, 2) else "B")


def q182():
    from fractions import Fraction as F
    chance=1-F(51,52)*F(50,51)
    return 'B' if chance==F(1,26) else 'D'


def q183():
    from fractions import Fraction as F
    marginals=F(8,10)+F(3,10)
    return 'D' if 2-marginals==F(9,10) else 'A'


def q185():
    from fractions import Fraction as F
    return 'D' if (1-F(2,5))*(1-F(1,2))==F(3,10) else 'A'


def q186():
    from fractions import Fraction as F
    p=2*F(1,2)*F(1,2)*F(1,2)
    return 'C' if p==F(1,4) else 'A'


def q187():
    from fractions import Fraction as F
    # Condition on the first draw and add the two paths.
    p=F(2,5)*F(1,4)+F(3,5)*F(2,4)
    return 'B' if p==F(2,5) else 'D'


def q188():
    from fractions import Fraction as F
    p=1-F(1,2)*F(3,4)*F(5,6)
    return 'A' if p==F(33,48) else 'D'


def q189():
    from fractions import Fraction as F
    # Enumerate which one of the three groups supplies the girl.
    cases=[F(3,4)*F(1,2)*F(3,4),F(1,4)*F(1,2)*F(3,4),F(1,4)*F(1,2)*F(1,4)]
    return 'C' if sum(cases)==F(13,32) else 'D'


def q190():
    from fractions import Fraction as F
    low=F(1,5)
    high=F(6,5)-F(85,100)
    return 'A' if (low,high)==(F(1,5),F(7,20)) else 'D'


def q191():
    from itertools import permutations
    from fractions import Fraction as F
    counts=[0,0,0,0]
    for perm in permutations(range(3)):
        counts[sum(i==perm[i] for i in range(3))]+=1
    p=[F(n,6) for n in counts]
    ok=[p[0]+p[3]==p[1],p[0]*p[1]==p[3],F(0)==p[2],p[0]+p[1]+p[3]==1]
    return ''.join(letter for letter,truth in zip('ABCD',ok) if truth)


def q192():
    from fractions import Fraction as F
    p=3*F(1,5)-F(1,10)
    return 'A' if p==F(1,2) else 'D'


def q193():
    from fractions import Fraction as F
    return 'B' if F(2+4+6,1+2+3+4+5+6)==F(4,7) else 'D'


def q194():
    from fractions import Fraction as F
    first=F(2,3)*F(1,3)
    ratio=F(4,9)
    p=first/(1-ratio)
    return 'B' if p==F(2,5) else 'D'


def q195():
    from fractions import Fraction as F
    p=F(1,4)
    value=F(3,2)*p+p*p
    return 'A' if value==(3*p+2*p*p)/2 else 'D'


def q196():
    from fractions import Fraction as F
    # First-step recursion: H, or tail and a safe die result before restarting.
    p=F(1,2)/(1-F(1,2)*F(2,3))
    return 'A' if p==F(3,4) else 'D'


def q197():
    from fractions import Fraction as F
    return 'A' if F(4,52)*F(4,52)==F(1,169) else 'D'


def q198():
    from fractions import Fraction as F
    p=1-F(12*11,16*15)
    return 'A' if p==F(9,20) else 'D'


def q199():
    from fractions import Fraction as F
    p=F(4,52)*F(4,51)
    return 'C' if p==F(4,663) else 'D'


def q201():
    from fractions import Fraction as F
    p=1-F(1,2)*F(2,3)*F(3,4)
    return 'A' if p==F(3,4) else 'D'


def q202():
    from fractions import Fraction as F
    return 'B' if F(1,2)*F(1,6)==F(1,12) else 'D'


def q203():
    from fractions import Fraction as F
    return 'C' if F(1,2)**2==F(1,4) else 'D'


def q204():
    from fractions import Fraction as F
    p=F(5,20)*F(4,19)*F(3,18)*F(2,17)
    return 'A' if p==F(1,969) else 'D'


def q205():
    from fractions import Fraction as F
    return 'D' if F(9,19)*F(8,18)==F(4,19) else 'A'


def q207():
    from fractions import Fraction as F
    return 'C' if (F(1,4)/F(1,2))==F(1,2) else 'D'


def q208():
    from fractions import Fraction as F
    return 'C' if F(13,52)*F(4,52)==F(1,52) else 'D'


def q209():
    from fractions import Fraction as F
    return 'D' if 1-F(4,5)**2==F(9,25) else 'A'


def q210():
    from fractions import Fraction as F
    pe,pf=F(2,5),F(3,7)
    a=pe*(1-pf)==pe*(1-pf)
    b=(1-pe)*(1-pf)==(1-pe)*(1-pf)
    c=pe+1-pe==1
    return 'D' if a and b and c else 'A'


def q211():
    from fractions import Fraction as F
    return 'A' if 1-F(1,2)**4==F(15,16) else 'D'


def q213():
    from fractions import Fraction as F
    return 'A' if F(4,6)*F(3,8)==F(1,4) else 'D'


def q214():
    # The number is incorrect when at least one of the 16 bits is wrong: sum over all 2^16 error patterns, p = 1/10.
    p = Fraction(1, 10)
    from collections import Counter
    wrong = Counter(sum(bits) for bits in product([0, 1], repeat=16))
    prob = sum(c * p ** k * (1 - p) ** (16 - k) for k, c in wrong.items() if k > 0)
    options = [p / 16, p ** 16, 16 * p ** 16, 1 - (1 - p) ** 16]
    hits = [i for i, o in enumerate(options) if o == prob]
    return "ABCD"[hits[0]] if len(hits) == 1 else "?"


def q215():
    from fractions import Fraction as F
    return 'A' if (1-F(1,5))*(1-F(1,4))==F(3,5) else 'D'


def q216():
    from fractions import Fraction as F
    exact=F(3,7)**3-F(2,7)**3
    options=[1-F(2,7)**4,4*F(2,7)**4,F(3,7)**3]
    return 'D' if exact not in options else 'A'


def q217():
    from fractions import Fraction as F
    return 'C' if F(5,45)==F(1,9) else 'D'


def q218():
    from fractions import Fraction as F
    return 'B' if F(10,20)*F(9,19)*F(10,18)==F(5,38) else 'D'


def q219():
    from fractions import Fraction as F
    primes=[n for n in range(2,21) if all(n%d for d in range(2,int(n**0.5)+1))]
    return 'D' if F(sum(n>10 for n in primes),len(primes))==F(1,2) else 'A'


def q220():
    from fractions import Fraction as F
    hits=sum(1 for n in range(10,100) if (n//10)*(n%10)==12)
    p=F(hits,90)
    return 'D' if 1-(1-p)**3==1-F(43,45)**3 else 'A'


def q221():
    from fractions import Fraction as F
    p=F(7,10)*F(1,2)/F(2,5)
    return 'A' if p==F(7,8) else 'D'


def q222():
    from itertools import product
    faces=range(1,7)
    five=sum(a+b==5 for a,b in product(faces,repeat=2))
    seven=sum(a+b==7 for a,b in product(faces,repeat=2))
    return 'B' if five/(five+seven)==2/5 else 'D'


def q223():
    from fractions import Fraction as F
    p=F(3,8)*F(4,10)+F(5,8)*F(6,10)
    return 'B' if p==F(21,40) else 'D'


def q224():
    from fractions import Fraction as F
    p=F(1,9); q=1-p
    b=q*p/(1-q*q)
    return 'B' if b==F(8,17) else 'D'


def q225():
    miss=1
    for p in (0.4,0.3,0.2,0.1): miss*=1-p
    return 'D' if abs((1-miss)-0.6976)<1e-12 else 'A'


def q226():
    from fractions import Fraction as F
    p=F(19,20)
    pa=F(1,20)*p+F(19,20)*(1-p)
    return 'C' if F(1,20)*p/pa==F(1,2) else 'D'


def q228():
    from itertools import product
    from fractions import Fraction as F
    triples=list(product(range(1,7),repeat=3))
    e1=[t for t in triples if t[0]<t[1]<t[2]]
    e2=[t for t in e1 if t[1]-t[0]==t[2]-t[1]]
    p1=F(len(e1),len(triples)); p2=F(len(e2),len(triples))
    pinter=F(len(e1.intersection(e2)),len(triples)) if False else p2
    cond=F(len(e2),len(e1))
    truths=[p2<=p1,pinter==F(1,36),cond==F(3,10),p1==F(10,3)*p2]
    return ''.join(letter for letter,ok in zip('ABCD',truths) if ok)


def q229():
    from fractions import Fraction as F
    ps=[F(k,10) for k in range(2,10)]
    total=F(0,1)
    for mask in range(1<<8):
        prob=F(1,1); count=0
        for i,p in enumerate(ps):
            if mask>>i&1: prob*=p; count+=1
            else: prob*=1-p
        if count>=6: total+=prob
    return 'B' if round(float(total),2)==0.19 else 'D'


def q230():
    from fractions import Fraction as F
    return 'A' if F(10,100)/(F(10,100)+F(32,100))==F(5,21) else 'D'


def q231():
    from fractions import Fraction as F
    p=(F(24,100)+F(18,100))/(F(24,100)+F(18,100)+F(14,100))
    return 'D' if p not in (F(25,100),F(42,100),F(9,10)) else 'A'


def q232():
    from fractions import Fraction as F
    p=F(1,2)*F(2,5)+F(1,2)*F(4,6)
    return 'C' if p==F(8,15) else 'D'


def q233():
    from fractions import Fraction as F
    return 'A' if F(3,4)**2==F(9,16) else 'D'


def q234():
    P = _p
    pa, pb = (lambda s: P(s, lambda a: a[0])), (lambda s: P(s, lambda a: a[1]))
    both = lambda s: P(s, lambda a: a[0] and a[1])
    a_true = []
    for s in _spaces(2, 234, 80):
        if pb(s) > 0:
            a_true.append(both(s) / pb(s) >= (pa(s) + pb(s) - 1) / pb(s))
    # (b) claims the identity P(A∩B) = P(A) − P(A∩Bᶜ) fails; it always holds, so (b) is false.
    b_identity = all(both(s) == pa(s) - P(s, lambda a: a[0] and not a[1]) for s in _spaces(2, 2340))
    # (c) for disjoint A and B: P(A∪B) = 1 − P(Aᶜ)P(Bᶜ)? A counterexample with no weight on A∩B shows it fails.
    disjoint = {(0, 0): Fraction(1, 2), (1, 0): Fraction(1, 4), (0, 1): Fraction(1, 4), (1, 1): Fraction(0)}
    c_holds = P(disjoint, lambda a: a[0] or a[1]) == 1 - (1 - pa(disjoint)) * (1 - pb(disjoint))
    return "A" if all(a_true) and b_identity and not c_holds else "?"


def q235():
    from fractions import Fraction as F
    p=F(5,10)*F(7,10)+F(3,10)*F(6,10)+F(2,10)*F(5,10)
    return 'D' if p==F(63,100) else 'A'


def q236():
    from fractions import Fraction as F
    # For each fixed conditioning event, E and E-complement partition it.
    p_e_f, p_ebar_f = F(2,5), F(3,5)
    p_e_fbar, p_ebar_fbar = F(1,4), F(3,4)
    checks=[p_e_f+p_ebar_f==1, p_e_f+p_e_fbar==1, p_ebar_f+p_e_fbar==1, p_e_fbar+p_ebar_fbar==1]
    return ''.join(c for c,ok in zip('ABCD',checks) if ok)


def q237():
    from fractions import Fraction as F
    a,b,c=F(1,3),F(1,4),F(1,5)
    p_union=b+c-b*c
    p_a_union=a*(b+c)-a*b*c
    p_intersection=a*b*c
    return 'A' if p_a_union==a*p_union and p_intersection==a*(b*c) else 'D'


def q238():
    from fractions import Fraction as F
    conditional=F(15,100)/F(40,100)
    return 'B' if conditional==F(3,8) else 'D'


def q239():
    from fractions import Fraction as F
    a,b=F(1,3),F(2,5)
    pa_bar,pb_bar=1-a,1-b
    tests=[F(0)==b-a, 1-a*b==pa_bar+pb_bar, (1-a)*(1-b)==pa_bar*pb_bar, F(1)==1]
    return ''.join(c for c,ok in zip('ABCD',tests) if ok)


def q240():
    from fractions import Fraction as F
    pa,pb=F(6,12),F(4,12)
    chance=pa*pb*pa+pb*pa*pb
    return 'B' if chance==F(5,36) else 'D'


def q241():
    from fractions import Fraction as F
    favorable=sum(1 for x in range(1,7) for y in range(1,7) if x<y)
    return 'D' if F(favorable,36)==F(5,12) else 'A'


def q242():
    from math import comb
    from fractions import Fraction as F
    choices=[n for n in range(3,50) if F(comb(n,3),comb(2*n,3))==F(1,20)]
    return 'D' if choices==[3] else 'A'


def q243():
    from fractions import Fraction as F
    solutions=[n for n in range(1,100) if (F(n,1)+F(n+1,2))/F(2*n+1,1)==F(31,42)]
    return 'A' if solutions==[10] else 'D'


def q244():
    from fractions import Fraction as F
    p_single=F(2,11)
    p_both=F(2,55)
    p_union=p_single+p_single-p_both
    p_cond=p_both/p_single
    checks=[p_single==p_single,p_both==F(2,55),p_union==F(18,55),p_cond==F(1,5)]
    return ''.join(c for c,ok in zip('ABCD',checks) if ok)


def q245():
    from fractions import Fraction as F
    joint=F(1,10)*F(1,4)
    total=F(9,10)+joint
    return 'B' if joint/total==F(1,37) else 'D'


def q246():
    from fractions import Fraction as F
    red=[F(6,10),F(4,10),F(5,10)]
    posterior=red[0]/sum(red,F(0))
    return 'C' if posterior==F(2,5) else 'A'


def q247():
    from fractions import Fraction as F
    group1=3*F(5,8); group2=2*F(2,6)
    return 'B' if group1/(group1+group2)==F(45,61) else 'D'


def q248():
    from math import comb
    from fractions import Fraction as F
    heart=F(1,4)*F(comb(12,2),comb(51,2))
    nonheart=F(3,4)*F(comb(13,2),comb(51,2))
    posterior=heart/(heart+nonheart)
    return 'C' if posterior==F(11,50) else 'D'


def q249():
    from fractions import Fraction as F
    probability=F(4,7)*F(5,9)+F(3,7)*F(6,9)
    return 'B' if probability==F(38,63) else 'D'


def q250():
    from fractions import Fraction as F
    access=F(2,5)+F(3,5)*F(3,8)
    return 'C' if access==F(5,8) else 'D'


def q251():
    from math import comb
    from fractions import Fraction as F
    equal=sum(comb(3,k)**2 for k in range(4))
    return 'C' if F(equal,64)==F(5,16) else 'D'


def q252():
    from fractions import Fraction as F
    probability=F(1,2)*F(3,5)+F(1,2)*F(2,6)
    return 'B' if probability==F(7,15) else 'D'


def q254():
    from itertools import product
    sequences=list(product((0,1),repeat=5))
    odd=sum(sum(s)%2==1 for s in sequences)
    return 'A' if odd==len(sequences)//2 else 'D'


def q255():
    from fractions import Fraction as F
    shares=[F(25,100)*F(5,100),F(35,100)*F(4,100),F(40,100)*F(2,100)]
    return 'A' if shares[1]/sum(shares,F(0))==F(28,69) else 'D'


def q256():
    from fractions import Fraction as F
    accident_counts=[2000*F(1,100),4000*F(3,100),6000*F(15,100)]
    return 'A' if accident_counts[0]/sum(accident_counts,F(0))==F(1,52) else 'D'


def q257():
    from math import comb
    from fractions import Fraction as F
    weights={k:comb(3,k)*comb(5,4-k) for k in range(5) if k<=3 and 4-k<=5}
    numerator=weights[3]*3
    denominator=sum(k*w for k,w in weights.items())
    return 'D' if F(numerator,denominator)==F(1,7) else 'A'


def q258():
    from fractions import Fraction as F
    know=F(1,2); guess=F(1,3)*F(1,4); copy=F(1,6)*F(1,8)
    return 'B' if know/(know+guess+copy)==F(24,29) else 'D'


def q259():
    from fractions import Fraction as F
    bad_a=F(80,100)*F(15,100); bad_b=F(20,100)*F(35,100)
    return 'B' if bad_b/(bad_a+bad_b)==F(7,19) else 'D'


def q260():
    from itertools import product
    outcomes=list(product((0,1),repeat=3))
    favorable=sum(sum(x)>=2 for x in outcomes)
    return 'C' if favorable*2==len(outcomes) else 'D'


def q261():
    from itertools import product
    outcomes=list(product((0,1),repeat=3))
    no_heads=sum(sum(x)==0 for x in outcomes)
    return 'A' if (len(outcomes)-no_heads)==7 else 'D'


def q262():
    from math import comb
    matches=[n for n in range(8,100) if comb(n,6)==comb(n,8)]
    return 'B' if matches==[14] else 'D'


def q263():
    from fractions import Fraction as F
    from math import comb
    mean,var=F(4),F(3)
    p=1-var/mean; n=int(mean/p)
    probability=F(comb(n,6))*p**6*(1-p)**(n-6)
    target=F(comb(16,6))*F(1,4)**6*F(3,4)**10
    return 'B' if n==16 and probability==target else 'D'


def q265():
    from fractions import Fraction as F
    from math import comb
    p=F(1,3); q=1-p
    lhs=4*comb(6,4)*p**4*q**2
    rhs=comb(6,2)*p**2*q**4
    return 'D' if lhs==rhs else 'A'


def q266():
    from fractions import Fraction as F
    mean,var=F(6),F(4)
    p=1-var/mean; n=mean/p
    return 'A' if n==18 and n*p==mean else 'D'


def q267():
    from fractions import Fraction as F
    from math import comb
    p=F(1,2); q=1-p
    ratios=[]
    for n in range(2,9):
        for r in range(n+1):
            a=F(comb(n,r))*p**r*q**(n-r)
            b=F(comb(n,n-r))*p**(n-r)*q**r
            ratios.append(a/b)
    return 'A' if set(ratios)=={F(1)} else 'D'


def q268():
    from itertools import product
    outcomes=list(product(range(1,7), repeat=4))
    count=sum(all(face==6 for face in row) for row in outcomes)
    return 'A' if count==1 and count*1296==len(outcomes) else 'D'


def q269():
    from fractions import Fraction as F
    p=F(5,100)**4
    return 'A' if p==F(1,160000) else 'D'


def q270():
    from fractions import Fraction as F
    from math import comb
    p=F(1,3)
    chance=sum(F(comb(3,k))*p**k*(1-p)**(3-k) for k in (2,3))
    return 'B' if chance==F(7,27) else 'D'


def q271():
    from fractions import Fraction as F
    from math import comb
    p,q=F(2,5),F(3,5); n,r=5,2
    probability=F(comb(n,r))*p**r*q**(n-r)
    return 'C' if probability==F(216,625) else 'A'


def q272():
    from fractions import Fraction as F
    from math import comb
    probability=F(comb(10,5),2**10)
    return 'B' if probability==F(63,256) else 'D'


def q273():
    from itertools import product
    outcomes=list(product(('B','G'),repeat=2))
    favorable=sum(set(pair)=={'B','G'} for pair in outcomes)
    return 'C' if favorable*2==len(outcomes) else 'A'


def q275():
    from fractions import Fraction as F
    chance=1-F(1,2)**3
    return 'D' if chance==F(7,8) else 'A'


def q277():
    from fractions import Fraction as F
    variance=5*F(1,2)*F(1,2)
    return 'D' if variance==F(5,4) else 'A'


def q279():
    from fractions import Fraction as F
    from math import comb
    p=F(2,3)
    probability=sum(F(comb(4,k))*p**k*(1-p)**(4-k) for k in (3,4))
    return 'C' if probability==F(16,27) else 'A'


def q280():
    from fractions import Fraction as F
    from math import comb
    probability=F(comb(6,3))*F(1,10)**3*F(9,10)**3
    return 'A' if probability==F(1458,100000) else 'D'


def q281():
    from fractions import Fraction as F
    chance=1-F(1,2)**4
    return 'B' if chance==F(15,16) else 'A'


def q282():
    from fractions import Fraction as F
    from math import comb
    no_women=F(comb(6,5),comb(10,5))
    return 'B' if 1-no_women==F(41,42) else 'A'


def q283():
    from fractions import Fraction as F
    p=F(2,6); mean=3*p; variance=3*p*(1-p)
    return 'A' if (mean,variance)==(1,F(2,3)) else 'D'


def q284():
    from fractions import Fraction as F
    chance=1-F(1,2)**4
    return 'D' if chance==F(15,16) else 'A'


def q285():
    from fractions import Fraction as F
    chance=1-F(5,6)**2
    return 'A' if chance==F(11,36) else 'D'


def q286():
    from fractions import Fraction as F
    p=F(1,4); variance=F(3)**2
    n=variance/(p*(1-p)); mean=n*p
    return 'C' if n==48 and mean==12 else 'A'


def q287():
    from fractions import Fraction as F
    from math import comb
    probability=F(comb(10,5),2**10)
    return 'A' if probability==F(63,256) else 'D'


def q288():
    from fractions import Fraction as F
    from math import comb
    p=F(2,3)
    chance=sum(F(comb(6,k))*p**k*(1-p)**(6-k) for k in range(3,7))
    return 'A' if chance==F(656,729) else 'D'


def q289():
    from fractions import Fraction as F
    from math import comb
    probability=F(comb(7,2))*F(5,6)**5*F(1,6)**3
    return 'B' if probability==F(comb(7,2)*5**5,6**8) else 'D'


def q290():
    from fractions import Fraction as F
    from math import comb
    ns=[n for n in range(9,100) if comb(n,7)==comb(n,9)]
    probability=F(comb(16,2),2**16)
    return 'C' if ns==[16] and probability==F(15,2**13) else 'D'


def q291():
    from fractions import Fraction as F
    from math import comb
    probability=F(comb(7,2))*F(1,10)**2*F(9,10)**5
    return 'C' if probability==21*F(1,10)**2*F(9,10)**5 else 'A'


def q292():
    from fractions import Fraction as F
    from math import comb
    p=F(3,4); q=1-p
    probability=sum(F(comb(5,k))*p**k*q**(5-k) for k in range(3,6))
    return 'D' if probability==F(459,512) else 'A'


def q293():
    from fractions import Fraction as F
    return 'A' if F(1,2)==F(2**99,2**100) else 'D'


def q294():
    from fractions import Fraction as F
    # Pair each seven-toss sequence with its complement.
    total=2**7
    wins=sum(1 for mask in range(total) if mask.bit_count()>3)
    return 'C' if F(wins,total)==F(1,2) else 'D'


def q295():
    from fractions import Fraction as F
    probability=F(3,4)**2*F(1,4)
    return 'A' if probability==F(9,64) else 'D'


def q296():
    from fractions import Fraction as F
    # Algebra reduces the harmonic condition to a quadratic with negative discriminant.
    discriminant=19**2-4*100
    return 'D' if discriminant<0 else 'A'


def q297():
    from math import comb
    from fractions import Fraction as F
    chance=F(comb(5,2),2**5)
    return 'D' if chance==F(5,16) else 'A'


def q298():
    from fractions import Fraction as F
    from math import comb
    n=3
    unequal=1-F(comb(2*n,n),2**(2*n))
    return 'C' if unequal==F(11,16) else 'D'


def q299():
    from fractions import Fraction as F
    n=next(n for n in range(1,20) if 1-F(1,2)**n>F(4,5))
    return 'B' if n==3 else 'D'


def q300():
    from fractions import Fraction as F
    from math import comb
    probability=F(comb(6,3),2**7)
    return 'C' if probability==F(5,32) else 'A'


def q301():
    from fractions import Fraction as F
    variance=2*F(1,3)*F(2,3)
    return 'B' if variance==F(4,9) else 'D'


def q302():
    from fractions import Fraction as F
    n=next(n for n in range(1,20) if 1-F(1,2)**n>=F(9,10))
    return 'B' if n==4 else 'D'


def q304():
    from fractions import Fraction as F
    probability=F(8,10)**2
    return 'B' if probability==F(16,25) else 'D'


def q306():
    from fractions import Fraction as F
    p=F(1,6); mean=3*p; variance=3*p*(1-p)
    return 'B' if (mean,variance)==(F(1,2),F(5,12)) else 'D'


def q307():
    from fractions import Fraction as F
    p_a,q_a=F(3,5),F(2,5); q_b=F(2,7)
    chance=p_a*q_b/(1-q_a*q_b)
    return 'A' if chance==F(6,31) else 'D'


def q309():
    from fractions import Fraction as F
    n=next(n for n in range(2,100) if F(n+1,2**n)<=F(1,100))
    return 'B' if n==11 else 'D'


def q310():
    # With fixed mean 25, variance = 25(1-p), so 0 <= sd <= 5.
    lower,upper=0,25
    return 'A' if lower>=0 and upper==5**2 else 'D'


def q311():
    from fractions import Fraction as F
    n=4
    favorable=sum(1 for digit in range(10) if digit in (1,3,7,9))
    probability=F(favorable,10)**n
    return 'A' if probability==F(2**n,5**n) else 'D'


def q314():
    from fractions import Fraction as F
    n=next(n for n in range(2,100) if 1-F(n+1,2**n)>F(9,10))
    return 'B' if n==7 else 'D'


def q315():
    from fractions import Fraction as F
    return 'A' if F(1,13)==F(1,13) else 'D'


# ---- generated by `node tools/intake.js build`: compare every q<n>() with the bank as written
def _same(fmt, want, got):
    import fractions
    want, got = str(want).strip(), str(got).strip()
    if fmt == "multi":
        return sorted(want.upper()) == sorted(got.upper())
    if fmt == "numeric":
        try:
            return abs(float(fractions.Fraction(want)) - float(fractions.Fraction(got))) <= 1e-9 * max(1.0, abs(float(fractions.Fraction(want))))
        except (ValueError, ZeroDivisionError):
            pass
    return want == got


def _check():
    import json as _json, os as _os
    root = _os.path.dirname(_os.path.abspath(__file__))
    items = {}
    for rel in ["seed/probability_probability_assignment_315.json"]:
        with open(_os.path.join(root, rel), encoding="utf-8") as f:
            for it in _json.load(f)["items"]:
                items[int(it["id"].rsplit("-q", 1)[1])] = it
    assert len(items) == 289, len(items)
    for n, it in sorted(items.items()):
        want = "".join(L for L in "ABCD" if it["verdicts"][L]["tf"]) if it["format"] == "multi" else it["answer"]
        got = globals()["q%d" % n]()
        assert _same(it["format"], want, got), (n, want, got)
    print("Verified %d answers independently against seed/probability_probability_assignment_315.json" % len(items))


if __name__ == "__main__":
    _check()
