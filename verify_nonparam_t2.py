#!/usr/bin/env python3
"""Independent checks for the sign and Wilcoxon signed-rank lesson."""
from fractions import Fraction
from math import comb
d=[4,-1,3,-2,5,-6]
assert sum(x>0 for x in d)==3 and sum(x<0 for x in d)==3
r={1:1,2:2,3:3,4:4,5:5,6:6}
wp=sum(r[abs(x)] for x in d if x>0); wm=sum(r[abs(x)] for x in d if x<0)
assert (wp,wm)==(12,9) and wp+wm==len(d)*(len(d)+1)//2==21
d2=[2,0,-1,3,0,4,-2,1]; nz=[x for x in d2 if x]
assert len(nz)==6 and sum(x>0 for x in nz)==4 and sum(x<0 for x in nz)==2
assert Fraction(sum(x>0 for x in nz),len(nz))==Fraction(2,3)
d3=[2,-1,4,0,-3,5,-2]; vals=sorted(abs(x) for x in d3 if x); ranks={}; i=0
while i<len(vals):
    j=i+1
    while j<len(vals) and vals[j]==vals[i]: j+=1
    ranks[vals[i]]=Fraction((i+1)+j,2); i=j
wp3=sum(ranks[abs(x)] for x in d3 if x>0); wm3=sum(ranks[abs(x)] for x in d3 if x<0)
assert (wp3,wm3)==(Fraction(27,2),Fraction(15,2)) and wp3+wm3==21
m=6
assert Fraction(m,2)==3 and Fraction(m,4)==Fraction(3,2)
assert Fraction(m*(m+1),4)==Fraction(21,2)
assert Fraction(m*(m+1)*(2*m+1),24)==Fraction(91,4)
p=min(1, 2*sum(comb(m,k) for k in range(0, min(3,m-3)+1))/(2**m))
assert p==1
print("PASS worked example: 3 positive, 3 negative; W+=12, W-=9; total=21")
print("PASS zero exclusion: m=6, positive proportion=2/3")
print("PASS tied absolute ranks: W+=13.5, W-=7.5; total=21")
print("PASS sign and signed-rank null moments and exact binomial tail")
