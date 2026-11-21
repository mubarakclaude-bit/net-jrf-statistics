#!/usr/bin/env python3
"""Independent arithmetic and content regression checks for Probability T2-T13
and Regression T1-T15. Uses only the Python standard library.
"""
import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_json(path):
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


class ProbabilityRegressionMathAudit(unittest.TestCase):
    def test_chebyshev_extremal_distribution_is_valid_for_k_at_least_one(self):
        k = 2.0
        p_each = 1.0 / (2.0 * k * k)
        p_centre = 1.0 - 1.0 / (k * k)
        variance = 2.0 * p_each * (k ** 2)
        tail = 2.0 * p_each
        self.assertGreaterEqual(p_centre, 0.0)
        self.assertAlmostEqual(variance, 1.0)
        self.assertAlmostEqual(tail, 1.0 / (k * k))
        # For k < 1 the proposed centre mass is negative: the construction
        # cannot be a probability distribution and Chebyshev is vacuous.
        self.assertLess(1.0 - 1.0 / (0.5 ** 2), 0.0)

    def test_uniform_n4_two_sided_tail_and_critical_value(self):
        # Under bivariate normality and rho=0, n=4 gives Uniform(-1,1).
        # Its density is 1/2, hence P(|r| >= c) = 1-c.
        self.assertAlmostEqual(1.0 - 0.97, 0.03)
        self.assertAlmostEqual(1.0 - 0.95, 0.05)
        self.assertLess(0.03, 0.05)

    def test_probability_t7_assumptions_and_k_qualification_are_explicit(self):
        lesson = read_json("seed/lesson_pr7.json")
        pool = read_json("seed/probability_t7_mastery.json")
        scene = next(s for s in lesson["scenes"] if s["id"] == "s4")
        item14 = next(q for q in pool["items"] if q["id"] == "pr-t7-m-14")
        item18 = next(q for q in pool["items"] if q["id"] == "pr-t7-m-18")
        self.assertIn("strictly positive", scene["problem"])
        self.assertIn("k ≥ 1", item14["stem"])
        self.assertIn("strictly positive", item18["stem"])

    def test_probability_t13_sampling_distribution_conditions_are_explicit(self):
        lesson = read_json("seed/lesson_pr13.json")
        pool = read_json("seed/probability_t13_mastery.json")
        scene = next(s for s in lesson["scenes"] if s["id"] == "s6")
        item = next(q for q in pool["items"] if q["id"] == "pr-t13-m-07")
        self.assertIn("bivariate normal", scene["problem"])
        self.assertIn("ρ = 0", scene["problem"])
        self.assertIn("Under ρ = 0", item["statements"][2])
        self.assertIn("Under ρ = 0", item["statements"][3])

    def test_probability_t13_tail_probability_correction_is_present(self):
        pool = read_json("seed/probability_t13_mastery.json")
        item = next(q for q in pool["items"] if q["id"] == "pr-t13-m-19")
        self.assertIn("0.03", item["options"][3])
        self.assertNotIn("0.06", item["options"][3])
        self.assertIn("0.03", item["explanation"])

    def test_regression_blue_items_state_error_covariance_assumption(self):
        pool = read_json("seed/regression_t2_mastery.json")
        stems = {q["id"]: q["stem"] for q in pool["items"]}
        self.assertIn("uncorrelated errors", stems["regression-t2-m-03"])
        self.assertIn("spherical errors", stems["regression-t2-m-07"])
        self.assertIn("spherical errors", stems["regression-t2-m-13"])

    def test_conditional_density_on_triangular_support(self):
        # f(x,y)=2 on 0<y<x<1.
        x, y = 0.4, 0.25
        self.assertAlmostEqual(2.0 * x, 0.8)       # f_X(x)
        self.assertAlmostEqual(1.0 / x, 2.5)      # f(Y|X=x)
        self.assertAlmostEqual(1.0 / (1.0-y), 4.0/3.0)
        self.assertAlmostEqual(x / 2.0, 0.2)      # E(Y|X=x)

    def test_bivariate_normal_conditional_moments(self):
        mu_x, mu_y, sx, sy, rho, y = 10.0, 20.0, 4.0, 5.0, 0.6, 15.0
        mean = mu_x + rho * sx / sy * (y - mu_y)
        variance = sx*sx * (1.0-rho*rho)
        probability = 0.5 * (1.0 + math.erf(((10.0-mean)/math.sqrt(variance))/math.sqrt(2.0)))
        self.assertAlmostEqual(mean, 7.6)
        self.assertAlmostEqual(variance, 10.24)
        self.assertAlmostEqual(probability, 0.7733726476, places=8)

    def test_poisson_mixture_total_variance(self):
        mean = 0.6*2.0 + 0.4*5.0
        within = 0.6*2.0 + 0.4*5.0
        between = 0.6*(2.0**2) + 0.4*(5.0**2) - mean**2
        self.assertAlmostEqual(mean, 3.2)
        self.assertAlmostEqual(within + between, 5.36)

    def test_exponential_poisson_mixture_variance(self):
        lam = 2.0
        variance = 1.0/lam + 1.0/(lam*lam)
        self.assertAlmostEqual(variance, 0.75)

    def test_cumulants_and_beta_gamma_moments(self):
        self.assertAlmostEqual(5*0.2*0.8*0.6, 0.48)  # Binomial third cumulant
        self.assertAlmostEqual(3.0/(2.0**2), 0.75)   # Gamma variance
        self.assertAlmostEqual(5.0/16.0, 0.3125)     # Beta(2,3) upper tail

    def test_markov_chebyshev_and_jensen_examples(self):
        self.assertAlmostEqual(4.0/20.0, 0.2)
        self.assertAlmostEqual(1.0/(2.5**2), 0.16)
        self.assertGreater((1.0+1.0/3.0)/2.0, 1.0/((1.0+3.0)/2.0))

    def test_independence_complement_and_union_examples(self):
        self.assertAlmostEqual(1.0 - 0.8**7, 0.7902848)
        self.assertAlmostEqual(1.0 - 0.95**20, 0.6415140776, places=9)
        self.assertAlmostEqual(0.3+0.4-0.3*0.4, 0.58)

    def test_clt_and_chebyshev_sample_mean_examples(self):
        p = 0.5 * (1.0 + math.erf(1.0/math.sqrt(2.0))) - 0.5 * (1.0 + math.erf(-1.0/math.sqrt(2.0)))
        self.assertAlmostEqual(p, 0.6826894921, places=9)
        self.assertAlmostEqual(25.0/100.0, 0.25)

    def test_exponential_conditioning_and_poisson_splitting(self):
        self.assertAlmostEqual(4.0/2.0, 2.0)  # E[X | X+Y=4]
        self.assertAlmostEqual(4.0*(1.0/3.0)*(2.0/3.0)**3, 32.0/81.0)
        self.assertAlmostEqual(math.exp(-4.0), 0.0183156389, places=9)

    def test_bayes_examples(self):
        ppv = 0.95*0.01 / (0.95*0.01 + 0.10*0.99)
        machine_posterior = 0.05*0.40 / (0.02*0.60 + 0.05*0.40)
        self.assertAlmostEqual(ppv, 0.0875576037, places=9)
        self.assertAlmostEqual(machine_posterior, 0.625)

    def test_regression_hat_matrix_and_residual_df(self):
        self.assertEqual(24-5, 19)
        self.assertAlmostEqual(3.0*(20-4), 48.0)
        self.assertAlmostEqual(1.0/3.0 + (2.0-1.0)**2/2.0, 5.0/6.0)

    def test_regression_anova_and_adjusted_r_squared(self):
        f = (66870.0/3.0)/(5344.0/16.0)
        f_from_r2 = (0.55/4.0)/(0.45/45.0)
        adj = 1.0 - 0.45*49.0/45.0
        self.assertAlmostEqual(f, 66.7365269461, places=8)
        self.assertAlmostEqual(f_from_r2, 13.75)
        self.assertAlmostEqual(adj, 0.51)

    def test_regression_dw_bp_and_gls(self):
        dw = ((2-1)**2+(1-2)**2+(0-1)**2)/(1+4+1+0)
        self.assertAlmostEqual(dw, 0.5)
        self.assertAlmostEqual(80*0.12, 9.6)
        self.assertAlmostEqual((2.0+0.25*4.0)/(1.0+0.25), 2.4)

    def test_regression_iv_and_simultaneous_equations(self):
        self.assertAlmostEqual(0.60/0.30, 2.0)
        self.assertAlmostEqual(0.48/0.08, 6.0)
        self.assertAlmostEqual((8.0+3.0*2.0-4.0*1.0)/3.0, 10.0/3.0)

    def test_regression_dummy_logit_and_restriction_calculations(self):
        self.assertAlmostEqual(100.0*(math.exp(0.2)-1.0), 22.1402758, places=6)
        self.assertAlmostEqual(1.0/(1.0+math.exp(1.0)), 0.2689414214, places=9)
        self.assertAlmostEqual(math.log(2.0)*0.25, 0.1732867951, places=9)
        self.assertAlmostEqual(((24.0-20.0)/1.0)/(20.0/10.0), 2.0)

    def test_regression_measurement_error_and_k_class(self):
        self.assertAlmostEqual((9.0/(9.0+3.0))*2.0, 1.5)
        self.assertAlmostEqual((20.0-0.5*5.0)/(10.0-0.5*4.0), 2.1875)


if __name__ == "__main__":
    unittest.main(verbosity=2)
