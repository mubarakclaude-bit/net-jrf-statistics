from verify_timeseries_common import close, finish
from math import sqrt

def ar1_variance(phi,sig2,k):
    return sig2*(1-phi**(2*k))/(1-phi**2)

def main():
    n=0
    phi,y,sig2=0.7,2,1
    for k,forecast,var in [(1,1.4,1),(2,0.98,1.49),(10,0.0564950498,1.9592197594843606)]:
        close(phi**k*y,forecast,1e-6); close(ar1_variance(phi,sig2,k),var,1e-6); n+=2
    close(sig2/(1-phi**2),1.9607843137254901); n+=1
    # AR(2) recursion with actual values available at first step.
    y_t,y_tm1=2,1
    f1=0.5*y_t+0.3*y_tm1
    f2=0.5*f1+0.3*y_t
    close(f1,1.3); close(f2,1.25); n+=2
    # MA(2) forecast-error variance reaches gamma0 at k=q+1.
    psi=[1,-0.4,0.2]
    close(sum(x*x for x in psi[:1]),1)
    close(sum(x*x for x in psi[:2]),1.16)
    close(sum(x*x for x in psi),1.20); n+=3
    # MA(1) minus convention: one-step forecast and variance.
    theta,eps=0.6,1.5
    close(-theta*eps,-0.9); close(1+theta**2,1.36); n+=2
    # The best linear forecast is not automatically the full conditional mean
    # under merely uncorrelated (not independent/Gaussian) Wold innovations.
    finish(11,11,n)
if __name__ == "__main__": main()
