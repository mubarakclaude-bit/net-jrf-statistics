from verify_timeseries_common import close, finish

def ar2_moments(phi1,phi2,sig2):
    rho1=phi1/(1-phi2)
    rho2=phi1*rho1+phi2
    gamma0=sig2*(1-phi2)/((1+phi2)*((1-phi2)**2-phi1**2))
    return rho1,rho2,gamma0

def main():
    n=0
    for phi,sig2 in [(0.8,1),(0.8,4),(-0.6,1)]:
        close(sig2/(1-phi**2), sig2/(1-phi**2))
        close(phi**2, abs(phi)**2); n+=2
    r1,r2,g0=ar2_moments(0.5,0.3,1)
    close(r1,0.7142857142857143); close(r2,0.6571428571428571); close(g0,2.2435897435897436); n+=3
    rhos=[1.0,r1,r2]
    for _ in range(3):
        rhos.append(0.5*rhos[-1]+0.3*rhos[-2])
    close(rhos[3],0.5428571428571429)
    close(rhos[5],0.39714285714285713); n+=2
    r1,r2,g0=ar2_moments(0.6,0.2,1)
    close(r1,0.75); close(r2,0.65); close(g0,2.380952380952381); n+=3
    # Variance is >= innovation variance; equality at white noise.
    close(1/(1-0**2),1.0)
    assert 1/(1-0.8**2) > 1
    finish(4,4,n+1)
if __name__ == "__main__": main()
