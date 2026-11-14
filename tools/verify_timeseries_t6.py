from verify_timeseries_common import close, finish
from math import sqrt

def main():
    n=0
    for t,mu,sig2,expected_mean,expected_var in [(5,0.5,4,2.5,20),(20,0.5,4,10,80),(40,0.5,4,20,160),(10,0.3,4,3,40)]:
        close(t*mu, expected_mean); close(t*sig2,expected_var); n+=2
    for t,k,expected in [(10,5,0.816496580927726),(20,20,0.7071067811865476),(25,75,0.5),(100,20,0.9128709291752769),(100,50,0.816496580927726)]:
        rho=sqrt(t/(t+k))
        close(rho,expected)
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
