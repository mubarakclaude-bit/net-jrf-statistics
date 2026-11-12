#!/usr/bin/env python3
from fractions import Fraction as F
p=[F(1,6),F(1,3),F(1,2)]
y=[F(10),F(30),F(30)]
z=[yi/pi for yi,pi in zip(y,p)]
assert z==[60,90,60]
mean=sum(pi*zi for pi,zi in zip(p,z))
second=sum(pi*zi*zi for pi,zi in zip(p,z))
var=second-mean*mean
assert mean==70 and second==5100 and var==200
assert var/4==50
# Completion example with size measures 2,3,5.
sizes=[2,3,5]; total=sum(sizes)
prob=[F(x,total) for x in sizes]
assert prob==[F(1,5),F(3,10),F(1,2)]
assert F(12)/prob[0]==60 and F(20)/prob[2]==40
assert (F(12)/prob[0]+F(20)/prob[2])/2==50
print("PASS HH contributions",z,"expectation",mean,"single-draw variance",var)
print("PASS HH mean-estimator variance for n=4:",var/4)
