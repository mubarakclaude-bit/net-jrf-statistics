from verify_timeseries_common import close, finish
from math import pi, cos

def far1(phi,sig2,w):
    return sig2/(2*pi*(1-2*phi*cos(w)+phi*phi))
def fma1(theta,sig2,w):
    return sig2*(1+theta*theta-2*theta*cos(w))/(2*pi)

def simpson(f,a,b,n=20000):
    h=(b-a)/n
    total=f(a)+f(b)
    for i in range(1,n): total+=(4 if i%2 else 2)*f(a+i*h)
    return total*h/3

def main():
    n=0
    close(far1(0.8,1,0),3.9788735772973833)
    close(far1(0.8,1,pi),0.04908738521234052); n+=2
    close(simpson(lambda w:far1(0.8,1,w),-pi,pi),1/(1-0.8**2),1e-9); n+=1
    close(far1(0.5,1,0),0.6366197723675814)
    close(far1(0.5,1,pi),0.0707355302630646); n+=2
    close(simpson(lambda w:far1(0.5,1,w),-pi,pi),1/(1-0.5**2),1e-9); n+=1
    close(fma1(0.7,1,0),0.09/(2*pi))
    close(fma1(0.7,1,pi),2.89/(2*pi)); n+=2
    close(simpson(lambda w:fma1(0.7,1,w),-pi,pi),1+0.7**2,1e-9); n+=1
    close(1/(2*pi)*2*pi,1.0); n+=1
    # If variance of a smoothed ordinate scales as 1/m, halving its SD needs m x4.
    close((1/2)**0.5,1/(4**0.5)); n+=1
    finish(7,7,n)
if __name__ == "__main__": main()
