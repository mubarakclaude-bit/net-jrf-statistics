#!/usr/bin/env python3
"""Independent Paper 2 Statistical Inference mathematical regression suite.

Run from the repository root:
    python verify_inference_math.py

Uses only the Python standard library. The suite deliberately separates:
  * mathematical regression calculations (independently recomputed),
  * source-content assertions for corrected examples/keys, and
  * catalog/mastery-pool integrity checks.

It does not claim that schema checks alone prove mathematical correctness.
"""
from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED = ROOT / "seed"
TOPICS = (1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17)


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def close(actual, expected, tol=1e-9):
    return math.isclose(actual, expected, rel_tol=tol, abs_tol=tol)


def poisson_pmf(k, rate):
    return math.exp(-rate) * rate**k / math.factorial(k)


class CatalogAndPoolTests(unittest.TestCase):
    def test_catalog_has_seventeen_inference_topics(self):
        catalog = load_json(SEED / "catalog.json")
        module = next(m for m in catalog["modules"] if m["id"] == "inference")
        self.assertEqual(len(module["topics"]), 17)
        self.assertEqual(
            [t["id"] for t in module["topics"]],
            [f"inference-t{i}" for i in range(1, 18)],
        )

    def test_all_non_deferred_mastery_pools_are_complete_and_well_formed(self):
        for n in TOPICS:
            with self.subTest(topic=n):
                pool = load_json(SEED / f"inference_t{n}_mastery.json")
                self.assertEqual(pool["topicId"], f"inference-t{n}")
                self.assertEqual(pool["count"], 20)
                self.assertEqual(len(pool["items"]), 20)
                ids = [q["id"] for q in pool["items"]]
                self.assertEqual(len(ids), len(set(ids)))
                for q in pool["items"]:
                    self.assertEqual(q["topic"], f"inference-t{n}")
                    self.assertTrue(q.get("stem"))
                    self.assertTrue(q.get("explanation"))
                    self.assertIn(q.get("answer"), ("A", "B", "C", "D"))
                    self.assertLess(ord(q["answer"]) - 65, len(q.get("options", [])))

    def test_multi_statement_keys_agree_with_individual_verdicts(self):
        for n in TOPICS:
            pool = load_json(SEED / f"inference_t{n}_mastery.json")
            for q in pool["items"]:
                if q.get("format") != "multi":
                    continue
                with self.subTest(topic=n, item=q["id"]):
                    self.assertIn("statements", q)
                    self.assertIn("verdicts", q)
                    true_items = sorted(
                        key for key, verdict in q["verdicts"].items()
                        if verdict["tf"] is True
                    )
                    option = q["options"][ord(q["answer"]) - 65]
                    option_letters = sorted(
                        ch for ch in option if ch in "ABCD"
                    )
                    self.assertEqual(true_items, option_letters)

    def test_t4_lesson_gap_is_detectable(self):
        # The catalog and mastery pool exist, but main has no lesson_t4.json.
        self.assertTrue((SEED / "inference_t4_mastery.json").exists())
        self.assertFalse((SEED / "lesson_t4.json").exists())


class Topic01SufficiencyTests(unittest.TestCase):
    def test_bernoulli_conditional_sample_probability(self):
        n, t = 12, 5
        self.assertEqual(math.comb(n, t), 792)
        self.assertTrue(close(1 / math.comb(n, t), 1 / 792))

    def test_normal_two_parameter_statistic_reconstructs_variance(self):
        n, sx, sx2 = 5, 20, 90
        xbar = sx / n
        unbiased_s2 = (sx2 - sx * sx / n) / (n - 1)
        self.assertEqual(xbar, 4)
        self.assertEqual(unbiased_s2, 2.5)


class Topic02CompletenessTests(unittest.TestCase):
    def test_uniform_location_range_mean(self):
        n = 4
        self.assertEqual((n - 1) / (n + 1), 3 / 5)

    def test_poisson_sum_parameterization(self):
        n, rate = 5, 0.7
        # E[z^T] for T~Poisson(n*rate) equals exp(n*rate*(z-1)).
        z = 0.8
        self.assertTrue(close(math.exp(n * rate * (z - 1)), math.exp(-0.7)))


class Topic03RaoBlackwellLehmannScheffeTests(unittest.TestCase):
    def test_poisson_zero_probability_umvue_is_unbiased(self):
        n, rate = 5, 0.8
        a = (n - 1) / n
        # T~Poisson(n*rate); E[a^T] = exp(n*rate*(a-1)).
        self.assertTrue(close(math.exp(n * rate * (a - 1)), math.exp(-rate)))

    def test_bernoulli_p_squared_umvue_is_unbiased(self):
        n, p = 8, 0.3
        # E[T(T-1)] = n(n-1)p^2 for T~Binomial(n,p).
        expected = n * (n - 1) * p**2 / (n * (n - 1))
        self.assertTrue(close(expected, p**2))

    def test_uniform_theta_squared_umvue(self):
        n, theta = 6, 3.0
        expected_max_sq = n * theta**2 / (n + 2)
        estimator_scale = (n + 2) / n
        self.assertTrue(close(estimator_scale * expected_max_sq, theta**2))


class Topic04MLETests(unittest.TestCase):
    def test_geometric_mle_and_invariant_mean(self):
        n, total = 6, 24
        p_hat = n / total
        self.assertEqual(p_hat, 0.25)
        self.assertEqual(1 / p_hat, 4)

    def test_uniform_boundary_mle(self):
        sample = (1.2, 3.8, 2.5)
        self.assertEqual(max(sample), 3.8)

    def test_normal_variance_mle_and_unbiased_estimator(self):
        n, ss = 16, 60
        self.assertEqual(ss / n, 3.75)
        self.assertEqual(ss / (n - 1), 4.0)


class Topic05MethodOfMomentsTests(unittest.TestCase):
    def test_gamma_shape_scale_moments(self):
        mean, variance = 6.0, 4.0
        beta = variance / mean
        alpha = mean / beta
        self.assertEqual(beta, 2 / 3)
        self.assertEqual(alpha, 9)
        self.assertTrue(close(alpha * beta, mean))
        self.assertTrue(close(alpha * beta**2, variance))

    def test_uniform_endpoints_from_mean_and_variance(self):
        mean, variance = 10.0, 3.0
        half_range = math.sqrt(3 * variance)
        self.assertEqual((mean - half_range, mean + half_range), (7.0, 13.0))

    def test_exponential_rate_moment_bias(self):
        n, rate = 5, 2.0
        expected_estimator = n * rate / (n - 1)
        self.assertEqual(expected_estimator, 2.5)
        self.assertEqual(expected_estimator - rate, 0.5)


class Topic06CramerRaoTests(unittest.TestCase):
    def test_bernoulli_information_and_bound(self):
        p, n = 0.4, 25
        information = n / (p * (1 - p))
        bound = 1 / information
        self.assertEqual(information, 25 / 0.24)
        self.assertTrue(close(bound, 0.0096))

    def test_poisson_information_and_bound(self):
        rate, n = 4.0, 16
        self.assertEqual(n / rate, 4)
        self.assertEqual(rate / n, 0.25)

    def test_crlb_for_bernoulli_variance_function(self):
        p, n = 0.4, 25
        bound = (1 - 2 * p) ** 2 * p * (1 - p) / n
        self.assertTrue(close(bound, 0.000384))


class Topic07BayesTests(unittest.TestCase):
    def test_beta_binomial_posterior(self):
        a, b, n, x = 2, 3, 10, 7
        post_a, post_b = a + x, b + n - x
        self.assertEqual((post_a, post_b), (9, 6))
        self.assertEqual(post_a / (post_a + post_b), 0.6)
        self.assertTrue(close((post_a - 1) / (post_a + post_b - 2), 8 / 13))

    def test_gamma_poisson_posterior(self):
        a, rate, total, n = 3, 2, 14, 7
        self.assertEqual((a + total, rate + n), (17, 9))

    def test_normal_normal_posterior_values(self):
        mu0, tau2, xbar, sigma2, n = 50.0, 16.0, 56.0, 8.0, 4
        precision = 1 / tau2 + n / sigma2
        post_var = 1 / precision
        post_mean = (mu0 / tau2 + n * xbar / sigma2) / precision
        self.assertTrue(close(post_var, 16 / 9))
        self.assertTrue(close(post_mean, 166 / 3))

    def test_gamma_median_approximation(self):
        shape, rate = 17, 9
        approximation = (shape - 1 / 3) / rate
        self.assertTrue(close(approximation, 50 / 27))


class Topic08DecisionTheoryTests(unittest.TestCase):
    def test_binomial_minimax_rule_has_constant_risk(self):
        n = 16
        a = math.sqrt(n) / 2
        denominator = n + 2 * a
        # Algebraically cancel p and p^2 after variance + squared bias.
        constant_risk = a**2 / denominator**2
        self.assertTrue(close(constant_risk, 0.01))
        self.assertTrue(close(1 / (4 * (1 + math.sqrt(n)) ** 2), 0.01))

    def test_binomial_risk_crossings(self):
        # For n=16, p(1-p)/16 = 0.01 at p=.2 and .8.
        roots = ((1 - math.sqrt(0.36)) / 2, (1 + math.sqrt(0.36)) / 2)
        self.assertEqual(roots, (0.2, 0.8))


class Topic10LikelihoodRatioTests(unittest.TestCase):
    def test_normal_mean_known_variance_lrt(self):
        n, xbar, mu0, variance = 16, 11.0, 10.0, 16.0
        minus2log_lambda = n * (xbar - mu0) ** 2 / variance
        self.assertEqual(minus2log_lambda, 1.0)

    def test_normal_variance_lrt(self):
        n, t = 10, 20.0
        statistic = n * math.log(n / t) + t - n
        self.assertTrue(close(statistic, 3.0685281944, tol=1e-8))

    def test_normal_unknown_variance_lrt_lambda(self):
        n, t_stat = 9, 2.0
        lam = (1 + t_stat**2 / (n - 1)) ** (-n / 2)
        self.assertTrue(close(lam, 0.1613, tol=1e-3))


class Topic11SequentialTests(unittest.TestCase):
    def test_bernoulli_sprt_boundaries_and_slope(self):
        p0, p1, alpha, beta = 0.3, 0.6, 0.05, 0.10
        A = (1 - beta) / alpha
        B = beta / (1 - alpha)
        u = math.log(p1 / p0)
        v = math.log((1 - p1) / (1 - p0))
        slope = -v / (u - v)
        self.assertEqual(A, 18)
        self.assertTrue(close(B, 0.1052631579, tol=1e-8))
        self.assertTrue(close(slope, 0.44671, tol=1e-4))

    def test_asn_approximations(self):
        log_a, log_b = math.log(18), math.log(0.1 / 0.95)
        e0 = 0.3 * math.log(2) + 0.7 * math.log(0.4 / 0.7)
        e1 = 0.6 * math.log(2) + 0.4 * math.log(0.4 / 0.7)
        asn0 = (0.05 * log_a + 0.95 * log_b) / e0
        asn1 = (0.90 * log_a + 0.10 * log_b) / e1
        self.assertTrue(close(asn0, 10.85, tol=2e-3))
        self.assertTrue(close(asn1, 12.37, tol=2e-3))


class Topic12PowerTests(unittest.TestCase):
    def test_exact_binomial_size_and_power(self):
        n = 5
        size = sum(math.comb(n, k) * 0.5**k * 0.5**(n-k) for k in (4, 5))
        power = sum(math.comb(n, k) * 0.75**k * 0.25**(n-k) for k in (4, 5))
        self.assertEqual(size, 3 / 16)
        self.assertTrue(close(power, 81 / 128))

    def test_normal_sample_size_for_target_power(self):
        z_alpha, z_power, sigma, delta = 1.645, 1.282, 5.0, 2.0
        n_min = ((z_alpha + z_power) * sigma / delta) ** 2
        self.assertTrue(close(n_min, 53.54580625, tol=1e-7))
        self.assertEqual(math.ceil(n_min), 54)

    def test_corrected_mastery_answer_key(self):
        pool = load_json(SEED / "inference_t12_mastery.json")
        item = next(q for q in pool["items"] if q["id"] == "inf-t12-m-10")
        self.assertEqual(item["answer"], "A")
        self.assertIn("0.6387", item["explanation"])


class Topic13ConfidenceIntervalTests(unittest.TestCase):
    def test_normal_mean_interval(self):
        xbar, s, n, tcrit = 52.4, 6.0, 16, 2.131
        half = tcrit * s / math.sqrt(n)
        self.assertTrue(close(xbar - half, 49.2035, tol=1e-3))
        self.assertTrue(close(xbar + half, 55.5965, tol=1e-3))

    def test_variance_interval_and_square_root(self):
        ss, chi_upper, chi_lower = 36.0, 19.023, 2.700
        lower, upper = ss / chi_upper, ss / chi_lower
        self.assertTrue(close(lower, 1.892446, tol=1e-6))
        self.assertTrue(close(upper, 13.3333333333, tol=1e-8))
        self.assertTrue(close(math.sqrt(lower), 1.375662, tol=1e-6))
        self.assertTrue(close(math.sqrt(upper), 3.651484, tol=1e-6))

    def test_corrected_pool_rounding(self):
        pool = load_json(SEED / "inference_t13_mastery.json")
        item = next(q for q in pool["items"] if q["id"] == "inf-t13-m-10")
        self.assertEqual(item["options"][0], "(1.892, 13.333)")


class Topic14GoodnessOfFitTests(unittest.TestCase):
    def test_fair_coin_four_tosses(self):
        observed = [17, 52, 54, 31, 6]
        expected = [10, 40, 60, 40, 10]
        statistic = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
        self.assertEqual(statistic, 12.725)

    def test_poisson_pooled_tail_statistic(self):
        rate = 0.93
        observed = [42, 33, 17, 8]
        expected = [
            100 * poisson_pmf(0, rate),
            100 * poisson_pmf(1, rate),
            100 * poisson_pmf(2, rate),
            100 * (1 - sum(poisson_pmf(k, rate) for k in range(3))),
        ]
        statistic = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
        self.assertTrue(close(statistic, 0.752, tol=1e-3))
        self.assertTrue(expected[3] > 5)

    def test_corrected_pooling_explanation(self):
        lesson = load_json(SEED / "lesson_t14.json")
        scene = next(s for s in lesson["scenes"] if s["id"] == "s6")
        step = next(x for x in scene["steps"] if "Check the expected counts" in x["say"])
        self.assertIn("5.289, just above 5", step["answer"])


class Topic15TestSelectionTests(unittest.TestCase):
    def test_familywise_error_and_bonferroni(self):
        fwer20 = 1 - 0.95**20
        adjusted = 0.05 / 20
        adjusted_fwer = 1 - (1 - adjusted) ** 20
        self.assertTrue(close(fwer20, 0.641514, tol=1e-5))
        self.assertTrue(close(adjusted_fwer, 0.0488, tol=1e-3))

    def test_large_sample_p_value(self):
        p_value = math.erfc(2 / math.sqrt(2))
        self.assertTrue(close(p_value, 0.0455, tol=1e-4))


class Topic16ContingencyTests(unittest.TestCase):
    def test_three_centre_association_statistic(self):
        observed = [[45, 33, 22], [15, 27, 38]]
        row_totals, col_totals, total = [100, 80], [60, 60, 60], 180
        statistic = 0.0
        for i in range(2):
            for j in range(3):
                expected = row_totals[i] * col_totals[j] / total
                statistic += (observed[i][j] - expected) ** 2 / expected
        self.assertTrue(close(statistic, 17.865, tol=1e-3))

    def test_two_by_two_pearson_and_yates(self):
        pearson = 2 * (25 / 17 + 25 / 13)
        yates = 2 * (20.25 / 17 + 20.25 / 13)
        self.assertTrue(close(pearson, 6.7873303167, tol=1e-8))
        self.assertTrue(close(yates, 5.4977375566, tol=1e-8))
        self.assertLess(yates, pearson)


class Topic17UMPTests(unittest.TestCase):
    def test_exponential_rate_one_sided_cutoffs(self):
        chi_lower_tail_005 = 3.9403  # lower 5% point, as labelled in the lesson
        chi_upper_tail_005 = 18.3070
        theta0 = 1.0
        lower = chi_lower_tail_005 / (2 * theta0)
        upper = chi_upper_tail_005 / (2 * theta0)
        self.assertTrue(close(lower, 1.97015, tol=1e-5))
        self.assertTrue(close(upper, 9.1535, tol=1e-8))

    def test_exponential_rate_direction(self):
        # Larger rate shifts the sum left; H1: rate > rate0 is a lower-tail test.
        self.assertLess(1 / 2.0, 1 / 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
