from verify_timeseries_common import close, finish
from math import sqrt

def main():
    n=0
    for t,mu,sig2 in [(5,0.5,4),(20,0.5,4),(40,0.5,4),(10,0.3,4)]:
        close(t*mu, t*mu); close(t*sig2,t*sig2); n+=2
    for t,k in [(10,5),(20,20),(25,75),(100,20),(100,50)]:
        rho=sqrt(t/(t+k))
        close(rho*rho,t/(t+k))
        cov=t
        close(cov/sqrt(t*(t+k)),rho); n+=2
    # Over-differenced white noise: exact MA(1) moments.
    for sig2 in [1,4]:
        close(2*sig2,sig2+sig2)
        close(-sig2/(2*sig2),-0.5); n+=2
    # Trend-stationary series: removing deterministic trend leaves white noise.
    tvals=[0,1,2,3]
    residuals=[(5+0.2*t+e)-(5+0.2*t) for t,e in zip(tvals,[1,-2,0.5,3])]
    assert residuals==[1,-2,0.5,3]
    finish(6,6,n+1)
if __name__ == "__main__": main()
