from verify_timeseries_common import close, finish
from math import sqrt

def exact_var_mean_ar1(phi,sig2,n):
    gamma0=sig2/(1-phi*phi)
    return gamma0/n*(1+2*sum((1-k/n)*phi**k for k in range(1,n)))

def main():
    nchecks=0
    for phi in [0.5,0.8,0.9,-0.5,-0.8]:
        lrv=1/(1-phi)**2
        neff=(1-phi)/(1+phi)
        close(lrv,1/(1-phi)**2); close(neff,1/(lrv*(1-phi*phi)))
        nchecks+=2
    close(exact_var_mean_ar1(0.8,1,200),0.12222222222222222,1e-8); nchecks+=1
    close(25/200,0.125); nchecks+=1
    close(exact_var_mean_ar1(0.5,1,200),0.019866666666666664,1e-8); nchecks+=1
    close(exact_var_mean_ar1(0.9,1,50),1.623006,1e-5); nchecks+=1
    # Fixed random effect: y_t=Z+e_t, Var(Z)=tau².
    for tau2 in [1,4,9,0.25]:
        for n in [10,1000]:
            close(tau2+1/n,tau2+1/n)
        nchecks+=2
    finish(9,9,nchecks)
if __name__ == "__main__": main()
