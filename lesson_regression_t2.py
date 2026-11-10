#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproducible authoring source for regression-t2.

Run from the repository root: python lesson_regression_t2.py
The complete lesson is embedded below; this regenerates its seed deterministically.
The existing regression_t2_mastery pool is validated and reused, not rewritten.
"""
import json, io, os
from collections import Counter

OUT = "seed/lesson_regression_t2.json"
POOL = "seed/regression_t2_mastery.json"
LESSON = json.loads(r'''{
 "id": "regressiont2",
 "moduleId": "regression",
 "topicId": "regression-t2",
 "title": "Gauss–Markov theorem, BLUE and estimability",
 "breadcrumb": "Regression → Linear estimation → Gauss–Markov, BLUE and estimability",
 "engine": "B",
 "engineName": "Translate the model into OLS weights, then verify unbiasedness, variance and estimability.",
 "version": "1.0",
 "status": "approved",
 "estMin": 99,
 "objectives": [
  "State the Gauss–Markov assumptions and identify the conclusion each supports.",
  "Calculate OLS/BLUE estimates and their covariance from a design matrix.",
  "Explain why OLS has minimum variance among linear unbiased estimators.",
  "Test whether a linear function of coefficients is estimable using the row space of X.",
  "Distinguish unbiasedness, efficiency, normality, heteroscedasticity and multicollinearity."
 ],
 "prereq": [
  {
   "id": "p1",
   "name": "Matrix multiplication and transpose",
   "why": "Form X′X and X′y with correct dimensions."
  },
  {
   "id": "p2",
   "name": "Expectation and variance of linear combinations",
   "why": "Unbiasedness and estimator variance are expectations of weighted errors."
  },
  {
   "id": "p3",
   "name": "Rank, linear independence and row space",
   "why": "Full rank gives unique coefficients; row-space membership determines estimability."
  },
  {
   "id": "p4",
   "name": "Inverse of a diagonal matrix",
   "why": "The Q11 cross-product matrix is diagonal."
  }
 ],
 "traps": [
  "Calling OLS BLUE without checking the error covariance assumptions.",
  "Treating normality as a Gauss–Markov condition.",
  "Reading best as a comparison with every estimator, not just linear unbiased estimators.",
  "Interchanging the divisors 6 and 2 in June 2026 Q11.",
  "Assuming heteroscedasticity or near multicollinearity automatically creates bias.",
  "Assuming each coefficient is estimable when X is rank deficient."
 ],
 "revision": {
  "sheet": [
   "Model y=Xβ+u; fixed X, full column rank, E(u)=0, Var(u)=σ²I.",
   "OLS β̂=(X′X)⁻¹X′y; E(β̂)=β; Var(β̂)=σ²(X′X)⁻¹.",
   "BLUE means minimum variance among linear unbiased estimators of the same target.",
   "Normality is not required for BLUE; it supports exact finite-sample normal-theory inference.",
   "Q11: X=[[1,1],[2,0],[1,−1]], X′X=diag(6,2).",
   "Q11: β̂₁=(y₁+2y₂+y₃)/6; β̂₂=(y₁−y₃)/2.",
   "Q11 covariance: σ²diag(1/6,1/2), covariance zero.",
   "Proof: c=a+d, X′d=0, a′d=0, variance difference=σ²d′d≥0.",
   "Estimability: ℓ′β estimable iff ℓ is in row(X).",
   "Heteroscedasticity can leave OLS unbiased but generally removes BLUE.",
   "Near multicollinearity inflates variance; perfect dependence causes rank deficiency."
  ],
  "cards": [
   [
    "What does BLUE mean?",
    "Best Linear Unbiased Estimator: minimum variance among linear unbiased estimators."
   ],
   [
    "Gauss–Markov assumptions?",
    "Fixed full-column-rank X; E(u)=0; Var(u)=σ²I."
   ],
   [
    "Is normality needed for BLUE?",
    "No."
   ],
   [
    "OLS covariance?",
    "σ²(X′X)⁻¹ under spherical errors."
   ],
   [
    "Q11 BLUE for β₁?",
    "(y₁+2y₂+y₃)/6."
   ],
   [
    "Q11 BLUE for β₂?",
    "(y₁−y₃)/2."
   ],
   [
    "Estimability test?",
    "ℓ′β is estimable iff ℓ lies in row(X)."
   ]
  ],
  "tricks": [
   "BLUE: best is restricted to Linear and Unbiased competitors.",
   "For diagonal X′X, invert each diagonal entry in place.",
   "Estimable means the target vector can be built from rows of X."
  ],
  "shortcuts": [
   "For Q11, X′X=diag(6,2).",
   "For Q11, Var(β̂₁)=σ²/6 and Var(β̂₂)=σ²/2.",
   "For design (1,2)′, the one-parameter BLUE weights are (1/5,2/5)."
  ],
  "remember": [
   "Unbiasedness is about the centre; efficiency is about the spread.",
   "When rank is deficient, test the target function, not the individual coefficient names."
  ]
 },
 "howto": "Work s0–s6 first if the Q11 calculation is your immediate need. Work s7–s10 to understand the theorem and estimability rather than memorise formulas. The optional final scene gives the compact matrix proof. This lesson does not derive t and F distributions, GLS in detail, or multicollinearity diagnostics; those belong to neighbouring topics.",
 "refs": [
  {
   "title": "Introduction to Linear Regression Analysis, 6th edition",
   "where": "Chapters 2–3: simple and multiple linear regression; least-squares properties",
   "site": "Douglas C. Montgomery, Elizabeth A. Peck and G. Geoffrey Vining",
   "url": "",
   "type": "Textbook",
   "free": false,
   "checked": "2026-11-10",
   "why": "Reference for the linear model, least-squares properties and variance calculations."
  },
  {
   "title": "Linear Models",
   "where": "Sections on estimable functions and the Gauss–Markov theorem",
   "site": "S. R. Searle",
   "url": "",
   "type": "Textbook",
   "free": false,
   "checked": "2026-11-10",
   "why": "Reference for estimability, rank deficiency and linear-model theory."
  },
  {
   "title": "Econometric Analysis, 8th edition",
   "where": "Chapter 2: The Linear Regression Model",
   "site": "William H. Greene",
   "url": "",
   "type": "Textbook",
   "free": false,
   "checked": "2026-11-10",
   "why": "Econometric treatment of OLS, covariance assumptions and efficiency."
  }
 ],
 "mastery": {
  "minQ": 10,
  "pass": 80,
  "draw": 10,
  "fmtMin": {
   "numeric": 70,
   "multi": 70
  },
  "diffMix": {
   "easy": 3,
   "moderate": 5,
   "hard": 2
  },
  "noHints": true,
  "retestDays": 7,
  "note": "Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."
 },
 "provenance": "Anchor: June 2026 Paper 2 Q11, transcribed in seed/pyq_j26_full.json. The recorded key is B and the candidate marked D. The lesson recalculates X′X=diag(6,2), X′y=(y₁+2y₂+y₃,y₁−y₃)′, β̂₁=(y₁+2y₂+y₃)/6 and β̂₂=(y₁−y₃)/2; matrix products, variance weights and estimability claims are checked in verify_regression_t2.py. The six Q11 variants cover theorem conditions, covariance, a two-observation BLUE and estimability. The existing regression_t2_mastery pool is reused without modification. Scope: Gauss–Markov, BLUE and estimability; detailed GLS, heteroscedasticity tests and multicollinearity diagnostics remain in neighbouring regression topics.",
 "scenes": [
  {
   "kind": "foundation",
   "id": "s0",
   "mins": 7,
   "title": "Prerequisites and the linear model",
   "objective": "Check matrix, expectation, variance and rank facts needed for BLUE.",
   "ask": {
    "q": "Which condition or calculation decides this claim?",
    "nudge": "Identify the target quantity first, then match it to the model condition."
   },
   "body": [
    "Write the regression model as y = Xβ + u. Here y is n × 1, X is n × k, β is k × 1 and u is n × 1. Each row of X describes one observation; each column represents one coefficient.",
    "The Gauss–Markov theorem is about the quality of an estimator under stated conditions. It does not say that least squares is automatically best in every regression. We will check the assumptions and then prove the variance comparison."
   ],
   "items": [
    {
     "ask": "What are the dimensions of X and β?",
     "recall": "X is n × k and β is k × 1.",
     "refresh": [
      "X has one row per observation and one column per coefficient.",
      "The product Xβ has dimension n × 1, the same as y."
     ]
    },
    {
     "ask": "What does E(u)=0 imply for E(y)?",
     "recall": "E(y)=Xβ for fixed X.",
     "refresh": [
      "Take expectations in y=Xβ+u.",
      "Since Xβ is fixed and E(u)=0, the expectation of y is Xβ."
     ]
    },
    {
     "ask": "What does Var(u)=σ²I mean?",
     "recall": "All errors have variance σ² and distinct errors have zero covariance.",
     "refresh": [
      "The diagonal entries give equal variances.",
      "The off-diagonal entries are zero, so errors are uncorrelated."
     ]
    },
    {
     "ask": "Why is full column rank important?",
     "recall": "It makes X′X invertible and the OLS coefficient vector unique.",
     "refresh": [
      "Full column rank means no column of X is an exact linear combination of the others.",
      "Then X′X is positive definite and invertible."
     ]
    }
   ]
  },
  {
   "kind": "intuition",
   "id": "s1",
   "mins": 7,
   "title": "Unbiasedness does not settle efficiency",
   "objective": "Explain why unbiased estimators can have different variances.",
   "body": [
    "An estimator can be centred correctly and still fluctuate too much. Unbiasedness concerns its expectation. Efficiency concerns its variance. The Gauss–Markov theorem links these ideas by identifying the least-variable estimator within a particular class.",
    "The word best in BLUE is deliberately limited: compare linear unbiased estimators of the same target. It does not compare OLS with every nonlinear estimator or every biased estimator."
   ],
   "scenario": {
    "teaser": "Two ways to estimate the same calibration level",
    "title": "A laboratory calibration",
    "body": [
     "A laboratory measures an unknown calibration level β twice. The first reading has expectation β, while the second has expectation 2β. Both errors have mean zero, are independent, and have the same variance σ². Halving the second reading gives an unbiased estimate. A weighted combination of both readings can also be unbiased. These two estimates are not equally precise: their random-error weights differ, and variance depends on the squares of those weights.",
     "The theorem tells us which weights minimise variance while preserving unbiasedness. We will derive them from the design vector rather than guess them. This is the central distinction in the word BLUE: an estimator can be unbiased without being the best linear unbiased estimator."
    ],
    "q": "Why can two unbiased estimators have different variances?",
    "answer": "Their weights on the random errors differ. Unbiasedness constrains the expected value; variance depends on the squared weights."
   },
   "ask": {
    "q": "Which condition or calculation decides this claim?",
    "nudge": "Identify the target quantity first, then match it to the model condition."
   }
  },
  {
   "kind": "explore",
   "id": "s2",
   "mins": 5,
   "title": "A visual analogy for bounds",
   "objective": "Distinguish an analogy about bounds from the Gauss–Markov variance result.",
   "viz": {
    "type": "ineq-bounds",
    "caption": "Analogy only: this visual plots a probability bound, not regression estimator variances."
   },
   "body": [
    "The existing visual library has no regression-specific variance-comparison chart. This panel is therefore only an analogy for comparing a bound with a true quantity. Its controls are not regression parameters, and it does not prove the Gauss–Markov theorem.",
    "For Gauss–Markov, the comparison is exact: the variance of any linear unbiased competitor minus the variance of OLS is a non-negative quantity. The next scenes derive that difference."
   ],
   "ask": {
    "q": "Which condition or calculation decides this claim?",
    "nudge": "Identify the target quantity first, then match it to the model condition."
   }
  },
  {
   "kind": "theory",
   "id": "s3",
   "mins": 9,
   "title": "The Gauss–Markov theorem",
   "objective": "State the assumptions and conclusion of the theorem.",
   "blocks": [
    {
     "t": "def",
     "h": "Model and assumptions",
     "body": "y=Xβ+u, with fixed X of full column rank k, E(u)=0 and Var(u)=σ²I, where σ²>0."
    },
    {
     "t": "formula",
     "h": "OLS estimator",
     "body": "β̂=(X′X)⁻¹X′y. Under E(u)=0, E(β̂)=β. Under Var(u)=σ²I, Var(β̂)=σ²(X′X)⁻¹."
    },
    {
     "t": "def",
     "h": "BLUE",
     "body": "Best Linear Unbiased Estimator. Best means minimum variance among all linear unbiased estimators of the same target."
    },
    {
     "t": "step",
     "h": "Normality is not required",
     "body": "The errors need not be normally distributed for OLS to be BLUE. Normality supports exact finite-sample normal-theory t and F inference; it is not a Gauss–Markov condition."
    }
   ],
   "flow": {
    "title": "Conditions before claiming BLUE",
    "alt": "Fixed full-rank design, zero-mean errors, spherical error covariance, then OLS is BLUE.",
    "nodes": [
     {
      "id": "a",
      "r": 0,
      "c": 1,
      "label": "Fixed X, full rank",
      "kind": "start"
     },
     {
      "id": "b",
      "r": 1,
      "c": 1,
      "label": "E(u)=0",
      "kind": "step"
     },
     {
      "id": "c",
      "r": 2,
      "c": 1,
      "label": "Var(u)=σ²I",
      "kind": "step"
     },
     {
      "id": "d",
      "r": 3,
      "c": 1,
      "label": "OLS is BLUE",
      "kind": "end"
     }
    ],
    "edges": [
     {
      "from": "a",
      "to": "b"
     },
     {
      "from": "b",
      "to": "c"
     },
     {
      "from": "c",
      "to": "d"
     }
    ],
    "note": "Normality is not a gate in this theorem."
   },
   "table": {
    "caption": "Assumptions and their roles",
    "head": [
     "Condition",
     "Role"
    ],
    "rows": [
     [
      "E(u)=0",
      "Unbiasedness"
     ],
     [
      "Var(u)=σ²I",
      "Gauss–Markov variance comparison"
     ],
     [
      "Full column rank",
      "Unique OLS coefficient vector"
     ],
     [
      "Normality",
      "Exact finite-sample normal-theory inference, not BLUE"
     ]
    ]
   },
   "ask": {
    "q": "Which condition or calculation decides this claim?",
    "nudge": "Identify the target quantity first, then match it to the model condition."
   }
  },
  {
   "kind": "worked",
   "id": "s4",
   "mins": 9,
   "title": "June 2026 Q11: calculate both BLUEs",
   "objective": "Derive the coefficient estimates and their covariance matrix.",
   "ask": {
    "q": "Which condition or calculation decides this claim?",
    "nudge": "Identify the target quantity first, then match it to the model condition."
   },
   "problem": "Let y₁=β₁+β₂+u₁; y₂=2β₁+u₂; y₃=β₁−β₂+u₃, with Var(uᵢ)=σ² and zero covariances. Find the BLUEs.",
   "steps": [
    {
     "say": "Read the coefficients into the design matrix.",
     "math": "X=[[1,1],[2,0],[1,−1]],   y=[y₁,y₂,y₃]′.",
     "why": "Each row corresponds to one equation; columns correspond to β₁ and β₂."
    },
    {
     "say": "Form X′X.",
     "math": "X′X=[[1,2,1],[1,0,−1]]·[[1,1],[2,0],[1,−1]]=[[6,0],[0,2]].",
     "why": "The off-diagonal sums cancel and both diagonal entries are positive."
    },
    {
     "say": "Invert and calculate X′y.",
     "math": "(X′X)⁻¹=diag(1/6,1/2);   X′y=[y₁+2y₂+y₃, y₁−y₃]′.",
     "why": "The inverse of a diagonal matrix is obtained by inverting its diagonal entries."
    },
    {
     "say": "Apply the OLS formula.",
     "math": "β̂₁=(y₁+2y₂+y₃)/6;   β̂₂=(y₁−y₃)/2.",
     "why": "The divisors are 6 and 2. Interchanging them is the key trap in Q11."
    },
    {
     "say": "Calculate the covariance matrix.",
     "math": "Var(β̂)=σ²(X′X)⁻¹=σ² diag(1/6,1/2).",
     "why": "The variances are σ²/6 and σ²/2; the covariance is zero."
    }
   ],
   "after": "Check the weights by multiplying their row vectors by X: they must return (1,0) and (0,1)."
  },
  {
   "kind": "recall",
   "id": "s5",
   "mins": 2,
   "title": "Recall the theorem",
   "objective": "Retrieve the assumptions and formulas.",
   "intro": "Answer before revealing.",
   "items": [
    {
     "q": "What does BLUE stand for?",
     "a": "Best Linear Unbiased Estimator."
    },
    {
     "q": "Is normality required for BLUE?",
     "a": "No."
    },
    {
     "q": "What is Var(β̂) under spherical errors?",
     "a": "σ²(X′X)⁻¹."
    },
    {
     "q": "What class does 'best' refer to?",
     "a": "All linear unbiased estimators of the same target."
    },
    {
     "q": "What gives a unique β̂?",
     "a": "Full column rank of X."
    }
   ]
  },
  {
   "kind": "completion",
   "id": "s6",
   "mins": 8,
   "title": "Complete the Q11 calculation",
   "objective": "Reconstruct the main matrix steps.",
   "problem": "For X=[[1,1],[2,0],[1,−1]], complete the OLS calculation.",
   "steps": [
    {
     "say": "Calculate the cross-product matrix.",
     "blank": {
      "prompt": "What is X′X?",
      "answer": "diag(6,2)",
      "accept": [
       "[[6,0],[0,2]]"
      ],
      "hint": "The off-diagonal products cancel."
     },
     "why": "This matrix determines the coefficient weights."
    },
    {
     "say": "Invert the cross-product matrix.",
     "blank": {
      "prompt": "What is (X′X)⁻¹?",
      "answer": "diag(1/6,1/2)",
      "accept": [
       "[[1/6,0],[0,1/2]]"
      ],
      "hint": "Invert 6 and 2 separately."
     },
     "why": "Keep the order of the two coefficients."
    },
    {
     "say": "Multiply by X′y.",
     "blank": {
      "prompt": "Give both coefficient estimates.",
      "answer": "β̂₁=(y₁+2y₂+y₃)/6; β̂₂=(y₁−y₃)/2",
      "accept": [
       "(y1+2y2+y3)/6 and (y1-y3)/2"
      ],
      "hint": "The first component of X′y is y₁+2y₂+y₃."
     },
     "why": "These are the OLS estimates and, under the theorem's conditions, the BLUEs."
    }
   ],
   "after": "Do not swap the divisors. They come from the corresponding diagonal entries of (X′X)⁻¹."
  },
  {
   "kind": "theory",
   "id": "s7",
   "mins": 7,
   "title": "Why OLS has the smallest variance",
   "objective": "Follow the orthogonality argument in the Gauss–Markov proof.",
   "blocks": [
    {
     "t": "step",
     "h": "Any linear unbiased estimator",
     "body": "For a target ℓ′β, write a competitor as c′y. Unbiasedness for every β requires X′c=ℓ."
    },
    {
     "t": "step",
     "h": "Separate the OLS weights",
     "body": "Let a=X(X′X)⁻¹ℓ. Then X′a=ℓ. Since X′c=ℓ too, write c=a+d, where X′d=0."
    },
    {
     "t": "formula",
     "h": "The cross term is zero",
     "body": "a′d=ℓ′(X′X)⁻¹X′d=0. Thus c′c=(a+d)′(a+d)=a′a+d′d."
    },
    {
     "t": "formula",
     "h": "Compare variances",
     "body": "Var(c′y)=σ²c′c=σ²a′a+σ²d′d≥Var(a′y), since d′d≥0. OLS is therefore best in the linear unbiased class."
    }
   ],
   "ask": {
    "q": "Which condition or calculation decides this claim?",
    "nudge": "Identify the target quantity first, then match it to the model condition."
   }
  },
  {
   "kind": "guided",
   "id": "s8",
   "mins": 8,
   "title": "Compare two unbiased estimators",
   "objective": "Choose the lower-variance estimator from a two-observation design.",
   "problem": "Let y₁=β+u₁ and y₂=2β+u₂, with independent errors of variance σ². Compare T₁=y₂/2 and T₂=(y₁+2y₂)/5.",
   "hints": [
    "Check each expectation using the design vector (1,2)′.",
    "For independent equal-variance errors, calculate σ² times the sum of squared weights.",
    "Compare 1/4 with 1/5."
   ],
   "answer": "Both are unbiased. Var(T₁)=σ²/4; Var(T₂)=σ²(1+4)/25=σ²/5. T₂ is the BLUE.",
   "check": "The smaller variance multiplier is 1/5, not 1/4.",
   "scenario": {
    "teaser": "A second reading carries twice the signal",
    "title": "Quality-control measurements",
    "body": [
     "A technician measures a process level β twice. The first instrument reading has expectation β; the second has expectation 2β. Both errors are independent and have the same variance. Halving the second reading is an unbiased way to estimate β, but it ignores the first reading. Combining the two readings with weights that preserve the expectation can reduce the variance.",
     "This is a one-parameter least-squares problem with design vector (1,2)′. The OLS weights are proportional to the design values and sum to the required unbiasedness constraint. The comparison is not based on which observation is numerically larger; it is based on the squared weights multiplying the error variance."
    ],
    "q": "Why does combining both readings improve precision?",
    "answer": "The BLUE uses weights (1/5,2/5), giving variance σ²/5, which is smaller than σ²/4 for y₂/2."
   },
   "solution": [
    {
     "say": "Check T₁.",
     "math": "E(y₂/2)=2β/2=β; Var(T₁)=σ²/4.",
     "why": "It is unbiased but uses only the second observation."
    },
    {
     "say": "Check T₂.",
     "math": "E[(y₁+2y₂)/5]=(β+4β)/5=β; Var(T₂)=(1+4)σ²/25=σ²/5.",
     "why": "Independence makes the variance the sum of squared weights times σ²."
    },
    {
     "say": "Compare.",
     "math": "σ²/5 < σ²/4.",
     "why": "T₂ has smaller variance."
    }
   ]
  },
  {
   "kind": "trapcheck",
   "id": "s9",
   "mins": 6,
   "title": "Six common traps",
   "objective": "Separate BLUE, unbiasedness, normality and estimability.",
   "intro": "Decide true or false before revealing.",
   "items": [
    {
     "claim": "Normality is necessary for OLS to be BLUE.",
     "tf": false,
     "why": "Normality is not a Gauss–Markov condition."
    },
    {
     "claim": "BLUE compares OLS with every unbiased estimator, linear or nonlinear.",
     "tf": false,
     "why": "The comparison is restricted to linear unbiased estimators."
    },
    {
     "claim": "With E(u)=0, heteroscedasticity alone need not bias OLS.",
     "tf": true,
     "why": "Zero mean preserves unbiasedness; unequal variances generally remove the BLUE guarantee."
    },
    {
     "claim": "Near multicollinearity automatically makes OLS biased.",
     "tf": false,
     "why": "It inflates variance and standard errors; it does not by itself break the zero-mean condition."
    },
    {
     "claim": "If X is rank deficient, every coefficient is individually estimable.",
     "tf": false,
     "why": "Some coefficient combinations may be estimable even when the full coefficient vector is not unique."
    },
    {
     "claim": "An estimable contrast can be unique when β itself is not unique.",
     "tf": true,
     "why": "A row-space linear function has the same value across solutions of the normal equations."
    }
   ]
  },
  {
   "kind": "guided",
   "id": "s10",
   "mins": 8,
   "title": "Transfer: estimability in a two-group model",
   "objective": "Use row-space membership to decide which effects can be estimated.",
   "problem": "The two group row types are (1,1,0) and (1,0,1), for parameters (α,τ₁,τ₂). Decide whether τ₁−τ₂, α+τ₁ and τ₁ alone are estimable.",
   "hints": [
    "Write the row space as the span of the two distinct design rows.",
    "A function ℓ′β is estimable iff ℓ is in the row space of X.",
    "Try expressing each target vector as a linear combination of the two row types."
   ],
   "answer": "τ₁−τ₂ is estimable because (0,1,−1)=(1,1,0)−(1,0,1). α+τ₁ is estimable because (1,1,0) is a row. τ₁ alone is not estimable because (0,1,0) is not in the span.",
   "check": "The difference of group effects is the difference of group means; individual effects depend on the non-unique parameterisation.",
   "solution": [
    {
     "say": "Write the row space.",
     "math": "Row(X)=span{(1,1,0),(1,0,1)}.",
     "why": "Estimable coefficient vectors are exactly those in this span."
    },
    {
     "say": "Express the contrast.",
     "math": "(1,1,0)−(1,0,1)=(0,1,−1).",
     "why": "The contrast τ₁−τ₂ is estimable."
    },
    {
     "say": "Test τ₁ alone.",
     "math": "a(1,1,0)+b(1,0,1)=(0,1,0) has no solution.",
     "why": "The first two coordinates force a=1 and b=−1, which makes the third coordinate −1 rather than 0."
    }
   ]
  },
  {
   "kind": "theory",
   "id": "s11",
   "mins": 6,
   "title": "Separate neighbouring regression ideas",
   "objective": "Distinguish rank deficiency, heteroscedasticity and near multicollinearity.",
   "blocks": [
    {
     "t": "def",
     "h": "Estimability",
     "body": "A linear function ℓ′β is estimable iff ℓ belongs to the row space of X. Full column rank makes every coefficient function estimable; rank deficiency restricts the identifiable combinations."
    },
    {
     "t": "def",
     "h": "Heteroscedasticity",
     "body": "If E(u)=0 but Var(u)=Ω≠σ²I, OLS remains unbiased. Its covariance is (X′X)⁻¹X′ΩX(X′X)⁻¹, and it is generally no longer BLUE."
    },
    {
     "t": "def",
     "h": "Multicollinearity",
     "body": "Near collinearity inflates coefficient variances but does not by itself create bias. Perfect linear dependence makes X rank deficient and can make individual coefficients non-estimable."
    }
   ],
   "ask": {
    "q": "Which condition or calculation decides this claim?",
    "nudge": "Identify the target quantity first, then match it to the model condition."
   }
  },
  {
   "kind": "recall",
   "id": "s12",
   "mins": 2,
   "title": "Second recall",
   "objective": "Retrieve the exam-critical results.",
   "intro": "Answer, then reveal.",
   "items": [
    {
     "q": "What are the Q11 BLUEs?",
     "a": "β̂₁=(y₁+2y₂+y₃)/6 and β̂₂=(y₁−y₃)/2."
    },
    {
     "q": "What is their covariance matrix?",
     "a": "σ² diag(1/6,1/2); covariance zero."
    },
    {
     "q": "When is ℓ′β estimable?",
     "a": "When ℓ lies in the row space of X."
    },
    {
     "q": "Does heteroscedasticity alone imply bias?",
     "a": "No, provided E(u)=0."
    },
    {
     "q": "Does normality enter the BLUE conditions?",
     "a": "No."
    }
   ]
  },
  {
   "kind": "summary",
   "id": "s13",
   "mins": 3,
   "title": "What you should now be able to do",
   "objective": "Apply the theorem and verify the result unaided.",
   "body": [
    "State the fixed-design, full-rank, zero-mean and spherical-error conditions.",
    "Explain BLUE as minimum variance among linear unbiased estimators.",
    "Calculate β̂=(X′X)⁻¹X′y and Var(β̂)=σ²(X′X)⁻¹.",
    "Reproduce both estimators in June 2026 Q11 and check their weights.",
    "Explain the variance proof using c=a+d and σ²d′d≥0.",
    "Test estimability using the row space of X.",
    "Distinguish heteroscedasticity, near multicollinearity and rank deficiency."
   ]
  },
  {
   "kind": "quiz",
   "id": "s14",
   "mins": 12,
   "title": "Mastery test",
   "objective": "Demonstrate the method on unseen questions.",
   "setId": "regression_t2_mastery"
  },
  {
   "kind": "theory",
   "id": "s15",
   "mins": 8,
   "ext": true,
   "title": "Optional: full matrix derivation",
   "objective": "Derive the OLS covariance and the variance comparison.",
   "blocks": [
    {
     "t": "step",
     "h": "Unbiasedness",
     "body": "β̂=(X′X)⁻¹X′(Xβ+u)=β+(X′X)⁻¹X′u. Taking expectations gives E(β̂)=β."
    },
    {
     "t": "step",
     "h": "Covariance",
     "body": "Var(β̂)=(X′X)⁻¹X′Var(u)X(X′X)⁻¹=σ²(X′X)⁻¹."
    },
    {
     "t": "step",
     "h": "Competing estimator",
     "body": "For ℓ′β, c′y is unbiased iff X′c=ℓ. Let a=X(X′X)⁻¹ℓ and c=a+d, so X′d=0."
    },
    {
     "t": "formula",
     "h": "Variance difference",
     "body": "Var(c′y)−Var(a′y)=σ²[(a+d)′(a+d)−a′a]=σ²d′d≥0."
    }
   ],
   "ask": {
    "q": "Which condition or calculation decides this claim?",
    "nudge": "Identify the target quantity first, then match it to the model condition."
   }
  }
 ]
}''')

def main():
    with io.open(POOL, encoding="utf-8") as f:
        pool = json.load(f)
    assert pool["topicId"] == LESSON["topicId"]
    assert pool["count"] == 20 and len(pool["items"]) == 20
    assert all(q["topic"] == LESSON["topicId"] for q in pool["items"])
    assert Counter(q["diff"] for q in pool["items"]) == {"easy": 6, "moderate": 10, "hard": 4}
    assert sum(q["format"] == "numeric" for q in pool["items"]) >= 4
    assert sum(q["format"] == "multi" for q in pool["items"]) >= 2
    assert all("check" in q for q in pool["items"] if q["format"] == "numeric")
    assert max(Counter(q["answer"] for q in pool["items"]).values()) <= 8
    assert LESSON["scenes"][-2]["setId"] == "regression_t2_mastery"
    LESSON["estMin"] = sum(s["mins"] for s in LESSON["scenes"] if not s.get("ext"))
    os.makedirs("seed", exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(LESSON, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s (%d core scenes, %d minutes)" %
          (OUT, sum(not s.get("ext") for s in LESSON["scenes"]), LESSON["estMin"]))
    print("validated and reused %s (%d mastery questions)" % (POOL, pool["count"]))

if __name__ == "__main__":
    main()
