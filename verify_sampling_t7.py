#!/usr/bin/env python3
from fractions import Fraction as F
pi_psu=F(2,10); pi_cond=F(5,20); pi_unit=pi_psu*pi_cond
assert pi_psu==F(1,5) and pi_cond==F(1,4)
assert pi_unit==F(1,20) and F(12)/pi_unit==240
assert F(1,2)*F(1,3)*F(1,4)==F(1,24)
p1=F(200,1000); p2=F(50,200); poverall=p1*p2
assert poverall==F(1,20) and 1/poverall==20
assert F(1,2)*F(1,5)*F(1,10)==F(1,100)
print("PASS two-stage probability",pi_unit,"HT contribution",F(12)/pi_unit)
print("PASS three-stage probability 1/24")
print("PASS two-phase probability",poverall,"weight",1/poverall)
