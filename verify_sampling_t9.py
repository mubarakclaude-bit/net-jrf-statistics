#!/usr/bin/env python3
from fractions import Fraction as F
# SYG coefficient examples.
c1=(F(2,5)*F(1,2)-F(3,20))/F(3,20)
delta=F(3,10)*F(2,5)-F(1,10)
assert c1==F(1,3) and delta==F(1,50)
# Des Raj n=2 exact worked example.
p1,p2=F(1,5),F(3,10)
y1,y2=F(10),F(12)
z1,z2=y1/p1,y2/p2
desraj=(z1*(1+p1)+z2*(1-p1))/2
v_desraj=F(1,4)*(1-p1)**2*(z1-z2)**2
assert (z1,z2)==(50,40)
assert desraj==46 and v_desraj==16
# Murthy unordered n=2 estimate and variance.
murthy=((1-p2)*z1+(1-p1)*z2)/(2-p1-p2)
v_murthy=((1-p1)*(1-p2)*(1-p1-p2)/(2-p1-p2)**2)*(z1-z2)**2
assert murthy==F(134,3)
assert v_murthy==F(112,9)
# Symmetry: swapping the pair leaves Murthy unchanged.
murthy_swapped=((1-p1)*z2+(1-p2)*z1)/(2-p1-p2)
assert murthy_swapped==murthy
print("PASS SYG coefficients",c1,delta)
print("PASS Des Raj estimate/variance",desraj,v_desraj)
print("PASS Murthy estimate/variance",murthy,v_murthy)
