from verify_timeseries_common import close, finish
from math import log

def main():
    n=0
    for alpha in [0.1,0.2,0.3,0.4,0.5]:
        weights=[alpha*(1-alpha)**j for j in range(10000)]
        close(sum(weights),1,1e-10)
        close((1-alpha)/alpha, sum(j*w for j,w in enumerate(weights)),1e-8)
        n+=2
    close(log(0.5)/log(0.7),1.9433582098747315)
    close(log(0.5)/log(0.9),6.578813478960585); n+=2
    # 2x4 centred moving average: convolution of two 4-point means.
    w=[1/4]*4
    c=[(w[i] if i<len(w) else 0)+(w[i-1] if 0<=i-1<len(w) else 0) for i in range(5)]
    c=[x/2 for x in c]
    assert c==[0.125,0.25,0.25,0.25,0.125]
    close(sum(c),1); n+=2
    # 2x12 centred filter: thirteen terms, half-weighted ends.
    c12=[1/24]+[1/12]*11+[1/24]
    close(sum(c12),1); assert len(c12)==13; n+=2
    # k-term MA applied to white noise: variance σ²/k, rho_h=(k-h)/k.
    k,sig2=7,4
    close(sig2/k,4/7); close((k-1)/k,6/7); n+=2
    # Seasonal normalisation examples.
    vals=[0.92,1.05,1.10,0.95]; mean=sum(vals)/4
    close(mean,1.005)
    norm=[x/mean for x in vals]
    for x,e in zip(norm,[0.9154228855721393,1.044776119402985,1.0945273631840795,0.945273631840796]): close(x,e)
    close(sum(norm)/4,1); n+=6
    close(1-0.3,0.7); n+=1
    finish(8,8,n)
if __name__ == "__main__": main()
