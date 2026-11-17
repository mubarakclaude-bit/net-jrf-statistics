#!/usr/bin/env python3
"""Independent arithmetic checks for the inference-t4 MLE lesson.
Run from the repository root: python3 verify_inference_t4.py
"""
import math

def close(a, b, tol=1e-12):
    assert abs(a-b) <= tol * max(1.0, abs(a), abs(b)), (a, b)

# Bernoulli sample 0, 1, 1, 1: score vanishes at the observed proportion.
x = [0, 1, 1, 1]
p_hat = sum(x) / len(x)
score = sum(x) / p_hat - (len(x)-sum(x)) / (1-p_hat)
close(p_hat, 0.75)
close(score, 0.0)
assert -sum(x)/(p_hat**2) - (len(x)-sum(x))/((1-p_hat)**2) < 0

# Poisson sample 1, 2, 3: lambda_hat is the sample mean.
pois = [1, 2, 3]
lam_hat = sum(pois) / len(pois)
close(lam_hat, 2.0)
close(-len(pois) + sum(pois)/lam_hat, 0.0)

# Exponential rate: lambda_hat = n / sum(x) = 1 / xbar.
life = [8.0, 12.0, 16.0]
rate_hat = len(life) / sum(life)
close(rate_hat, 1/12)
close(len(life)/rate_hat - sum(life), 0.0)

# Exponential rate MLE is biased for finite n>1: E[n/S] = n*lambda/(n-1).
n, lam = 5, 2.0
expected_rate_mle = n * lam / (n-1)
close(expected_rate_mle, 2.5)
close(expected_rate_mle - lam, lam/(n-1))

# Normal sample 1,2,3: MLE variance divides by n; unbiased variance divides by n-1.
normal = [1.0, 2.0, 3.0]
mean_hat = sum(normal)/len(normal)
mle_var = sum((v-mean_hat)**2 for v in normal)/len(normal)
unbiased_var = sum((v-mean_hat)**2 for v in normal)/(len(normal)-1)
close(mean_hat, 2.0)
close(mle_var, 2/3)
close(unbiased_var, 1.0)

# Uniform(0,theta): likelihood is zero below the sample maximum and decreases above it.
u = [0.2, 0.5, 0.8]
m = max(u)
def uniform_likelihood(theta):
    return theta**(-len(u)) if theta >= m else 0.0
assert uniform_likelihood(m) > uniform_likelihood(m+0.1) > 0
assert uniform_likelihood(m-0.01) == 0.0

# Constrained Bernoulli example: pbar=1/2 is already inside [1/3,2/3].
constrained = [0, 1]
pbar = sum(constrained)/len(constrained)
p_constrained = min(2/3, max(1/3, pbar))
close(p_constrained, 0.5)

# If both observations are zero, the likelihood decreases in p; constrained max is 1/3.
all_zero_likelihood = lambda p: (1-p)**2
assert all_zero_likelihood(1/3) > all_zero_likelihood(0.5) > all_zero_likelihood(2/3)

print("PASS: Bernoulli score and curvature")
print("PASS: Poisson score")
print("PASS: exponential-rate score, rate/scale and finite-sample bias")
print("PASS: normal MLE variance (n) versus unbiased variance (n-1)")
print("PASS: Uniform(0,theta) support and boundary maximum")
print("PASS: constrained Bernoulli examples")
