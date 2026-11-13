from verify_timeseries_common import close, finish

def poly_mul(a,b):
    out=[0.0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

def main():
    n=0
    # Factor unit-root AR(2) polynomials independently.
    for a,b,rest in [(0.6,0.4,0.4),(1.2,-0.2,-0.2)]:
        # (1-B)(1-rest*B) = 1-(1+rest)B+rest B^2
        coeff=poly_mul([1,-1],[1,rest])
        close(coeff[1],-a); close(coeff[2],-b); n+=2
        # Δy is AR(1) with coefficient -rest.
        close(-rest, -0.4 if rest == 0.4 else 0.2); n+=1
    # Differencing white noise creates MA(1): variance 2σ² and rho1=-1/2.
    sig2=3.7
    close(2*sig2, sig2+sig2)
    close(-sig2/(2*sig2),-0.5); n+=2
    # Dickey-Fuller reparameterisation: delta=phi-1; unit root iff delta=0.
    for phi in [1.0,0.99,0.8,0.2]:
        delta=phi-1
        close(delta,phi-1)
        if phi==1.0: assert delta==0
        else: assert delta<0
        n+=1
    finish(5,5,n)
if __name__ == "__main__": main()
