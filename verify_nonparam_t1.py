#!/usr/bin/env python3
"""Independent exact-rank checks for the Mann–Whitney U lesson."""
from fractions import Fraction
ES=[65,57,74,43,39,88,62,69,70,72,59,60,80,83,50]
LC=[85,87,92,98,90,88,75,72,60,93,88,89,96,73,62]
def ranks(groups):
    tagged=sorted((v,g,i) for g,vals in enumerate(groups) for i,v in enumerate(vals))
    out={}; i=0
    while i<len(tagged):
        j=i+1
        while j<len(tagged) and tagged[j][0]==tagged[i][0]: j+=1
        rank=Fraction((i+1)+j,2)
        for _,g,k in tagged[i:j]: out[g,k]=rank
        i=j
    return out
r=ranks([ES,LC]); n1,n2=len(ES),len(LC); N=n1+n2
R1=sum(r[0,i] for i in range(n1)); R2=sum(r[1,i] for i in range(n2))
U1=R1-Fraction(n1*(n1+1),2); U2=R2-Fraction(n2*(n2+1),2)
assert (R1,R2)==(Fraction(305,2),Fraction(625,2))
assert (U1,U2)==(Fraction(65,2),Fraction(385,2))
assert R1+R2==Fraction(N*(N+1),2)==465
assert U1+U2==n1*n2==225 and min(U1,U2)==Fraction(65,2)
small=ranks([[4,8,10],[5,8,12]])
assert [small[0,i] for i in range(3)]==[1,Fraction(7,2),5]
assert [small[1,i] for i in range(3)]==[2,Fraction(7,2),6]
assert sum(small.values())==21
assert Fraction(n1*n2,2)==Fraction(225,2)
assert Fraction(n1*n2*(N+1),12)==Fraction(6975,12)
def tie_factor(N,ts):
    return Fraction(N**3-N-sum(t**3-t for t in ts),N**3-N)
assert tie_factor(6,[2])==Fraction(34,35)
print("PASS Q42: R_ES=152.5, R_LC=312.5; U_ES=32.5, U_LC=192.5; min U=32.5")
print("PASS rank total=465; U sum=225; average-rank tie example")
print("PASS null mean, no-tie variance and tie-correction identity")
