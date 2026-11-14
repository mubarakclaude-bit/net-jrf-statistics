from verify_timeseries_common import close, finish
import cmath

def stationary_ar2(a, b):
    # Directly solve 1-a*z-b*z**2 = 0; compare with the strict triangle.
    roots = ((-a + cmath.sqrt(a*a + 4*b)) / (2*b),
             (-a - cmath.sqrt(a*a + 4*b)) / (2*b))
    triangle = (a+b < 1 and b-a < 1 and abs(b) < 1)
    roots_ok = all(abs(z) > 1 + 1e-10 for z in roots)
    return triangle, roots_ok, roots

def main():
    n = 0
    for a,b,want in [(1.2,-0.4,True),(1.2,-0.2,False),(0.6,0.4,False),(0.5,0.3,True)]:
        tri, roots_ok, roots = stationary_ar2(a,b)
        assert tri == roots_ok == want, (a,b,roots)
        n += 1
    tri, roots_ok, roots = stationary_ar2(1.2,-0.2)
    assert any(abs(abs(z)-1) < 1e-10 for z in roots)
    close(abs(stationary_ar2(1.2,-0.4)[2][0]), 1.5811388300841898)
    for phi, expected in [(0.5,1.3333333333333333),(0.8,2.777777777777778),(0.95,10.256410256410256)]:
        close(1/(1-phi**2), expected); n += 1
    def rho(theta): return -theta/(1+theta**2)
    for theta in [0.5,0.7,1.5,2.0]:
        close(rho(theta), rho(1/theta)); n += 1
    # Full covariance equivalence requires rescaling innovation variance.
    theta, sig2 = 2.0, 1.0
    theta_star, sig2_star = 1/theta, theta**2*sig2
    close(sig2*(1+theta**2), sig2_star*(1+theta_star**2)); n += 1
    finish(1,1,n)
if __name__ == "__main__": main()
