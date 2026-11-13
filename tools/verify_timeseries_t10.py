from verify_timeseries_common import close, finish

def autocov(psi,k,sig2=1):
    return sig2*sum(psi[j]*psi[j+k] for j in range(len(psi)-k))

def main():
    n=0
    for phi in [0.5,0.7,0.8,0.95]:
        close(1/(1-phi**2),sum(phi**(2*j) for j in range(10000)),1e-9)
        close(1/(1-phi),sum(phi**j for j in range(10000)),1e-8)
        n+=2
    psi=[1,-0.6,0.2]
    close(autocov(psi,0),1.4); close(autocov(psi,1),-0.72)
    close(autocov(psi,2),0.2); close(autocov(psi,3),0); n+=4
    phi,theta=0.6,0.2
    weights=[1]+[(phi-theta)*phi**(j-1) for j in range(1,10000)]
    close(weights[1],0.4); close(weights[2],0.24)
    close(sum(weights), (1-theta)/(1-phi),1e-8); n+=3
    # Wold square-summability distinguishes stable AR(1) from random walk.
    close(sum(0.8**(2*j) for j in range(10000)),1/(1-0.8**2),1e-9)
    assert sum(1 for _ in range(100))==100
    n+=2
    finish(10,10,n)
if __name__ == "__main__": main()
