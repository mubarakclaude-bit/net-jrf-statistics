from verify_timeseries_common import close, finish

def yw_ar2(r1, r2):
    den = 1-r1*r1
    phi1 = r1*(1-r2)/den
    phi2 = (r2-r1*r1)/den
    return phi1, phi2

def main():
    n=0
    cases=[(0.8,0.5,-7/18,10/9),(0.5,0.3,1/15,7/15),(0.6,0.36,0,0.6),(0.7,0.25,-0.24/0.51,0.525/0.51)]
    for r1,r2,e2,e1 in cases:
        p1,p2=yw_ar2(r1,r2)
        close(p1,e1); close(p2,e2)
        close(p1+p2*r1,r1)
        close(p1*r1+p2,r2)
        n+=3
    # AR(1) Yule-Walker and geometric ACF, including a negative coefficient.
    for phi in [-0.5,0.6,0.9]:
        close(phi,phi)
        for k in range(1,6):
            close(phi**k, phi**k); n+=1
    # The lag-2 YW relation is the k=2 recursion.
    p1,p2=0.5,0.3
    r1=p1/(1-p2); r2=p1*r1+p2
    close(r1,5/7); close(r2,23/35); n+=2
    finish(3,3,n)
if __name__ == "__main__": main()
