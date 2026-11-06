#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regression-t5 (topic 6.5): multicollinearity. Anchor Q38 (key C, a negation question).
Every figure below is computed in verify_regression_t5.py; nothing is recalled."""
import json, io, os, re, random

OUT  = "seed/lesson_rg5.json"
POOL = "seed/regression_t5_mastery.json"

S = []

S.append({"kind":"foundation","id":"s0","mins":7,"title":"Before the lesson — four things it will assume",
 "objective":"Check the auxiliary regression, the variance formula, eigenvalues and the bias–variance idea.",
 "ask":{"q":"If two regressors carry almost the same information, what can the data tell you about each one separately?","nudge":"Think about which of their effects can be told apart."},
 "body":["Multicollinearity means that one regressor can be predicted from the others. When two predictors move together almost perfectly, the data show how the pair behaves, but give very little evidence about which of the two deserves the credit.",
         "Q38 of the June paper asked which of four statements is not a consequence of near multicollinearity. The key is that the estimates are biased. A common slip on a question phrased this way is to pick a statement that sounds harmful but is a genuine consequence, such as large estimates. This lesson therefore sorts the four statements by whether they concern the mean, the variance or the interpretation.",
         "Nothing here is new machinery. It reuses Var(β̂) = σ²(X′X)⁻¹ from topic 6.2 and the idea of a variance estimate from topic 6.1, and adds one number per regressor that measures how predictable it is from the others."],
 "items":[
  {"ask":"What is an auxiliary regression and what is its R²?",
   "recall":"Regress one regressor on all the others; its R² (call it R_j²) measures how well the others predict it.",
   "refresh":["Take the j-th column of X. Fit it by least squares on all the other columns. The R² of that fit, R_j², is 0 when the column is unrelated to the others and approaches 1 when it is almost a combination of them.",
              "With only two regressors, R_j² is the square of their correlation: R_j² = r². With three or more it can be large even when every pairwise correlation is moderate. That is the whole reason the check is run on the auxiliary regression and not on pairs."]},
  {"ask":"What is Var(β̂) and what does its diagonal give?",
   "recall":"Var(β̂) = σ²(X′X)⁻¹; the j-th diagonal entry is the variance of the j-th coefficient.",
   "refresh":["From topic 6.2: β̂ = (X′X)⁻¹X′y has covariance σ²(X′X)⁻¹. The square roots of the diagonal entries are the standard errors that go under each coefficient in a regression printout.",
              "Everything in this lesson is a statement about how large those diagonal entries are, and what makes them large."]},
  {"ask":"For a symmetric matrix, what do the eigenvalues add up to and multiply to?",
   "recall":"Sum = trace, product = determinant.",
   "refresh":["A symmetric matrix has real eigenvalues. Their sum equals the sum of the diagonal entries and their product equals the determinant.",
              "For the 2×2 correlation matrix [[1, r], [r, 1]] the eigenvalues are 1 + r and 1 − r. Check: the sum is 2, the trace, and the product is 1 − r², the determinant. As r approaches 1 the smaller eigenvalue approaches 0."]},
  {"ask":"What is the mean squared error of an estimator in terms of bias and variance?",
   "recall":"MSE = bias² + variance.",
   "refresh":["The expected squared distance of an estimator from the truth splits into the squared bias and the variance. An unbiased estimator has MSE equal to its variance.",
              "A biased estimator can have a smaller MSE than an unbiased one if the variance saved is larger than the bias² added. The remedies for multicollinearity use exactly this trade."]}]})

S.append({"kind":"intuition","id":"s1","mins":7,"title":"The data can see the pair, but not the members",
 "objective":"Explain why near-collinear regressors give stable sums and unstable differences, with the symptoms that follow.",
 "body":["Suppose two predictors rise and fall together almost exactly. A model with both asks the data to split one effect into two shares. The total effect is well measured, since the pair together predicts y well. But how much belongs to the first predictor and how much to the second hardly changes the fit, so the data cannot settle it.",
         "That is why the symptoms appear together. The fit is good: R² is high and the overall F test is significant. Each coefficient has a huge standard error, so each t statistic is small. A small change in the data, such as dropping one observation, can move the two coefficients a long way in opposite directions while their sum barely moves.",
         "None of this makes the average estimate wrong. If you could repeat the study many times, the estimates would centre on the truth. What changes is the spread around it. This is the point Q38 tests: the estimator is unbiased, and its variance is inflated."],
 "scenario":{"teaser":"A printout with R² of 0.81, a significant F, and no significant slope.",
  "title":"A good fit with no credit to give",
  "body":["An analyst regresses a score on two predictors using 20 observations. The printout reads R² = 0.8107 and F = 36.41 on (2, 17) degrees of freedom, far above the 5% critical value of 3.59. As a whole, the model predicts the score well.",
          "But the coefficient table says otherwise. The first slope is 0.143 with standard error 2.007, so t = 0.07. The second slope is 1.685 with standard error 1.861, so t = 0.91. With 17 degrees of freedom the 5% critical value is 2.11, so neither predictor looks useful on its own.",
          "The two predictors have a correlation of 0.9934. When the analyst drops the second one, the remaining slope becomes 1.949 with t = 8.53, and R² barely moves, from 0.8107 to 0.8016. The first predictor was carrying the effect all along. The second was sharing its credit and inflating its standard error."],
  "q":"Why does the first slope's t statistic jump from 0.07 to 8.53 when the second predictor is dropped?",
  "answer":"The standard error falls from 2.007 to 0.229. With the two predictors almost collinear, the variance of each slope is inflated by about 76 (the variance inflation factor). Dropping one removes the inflation."},
 "ask":{"q":"Does multicollinearity make the average of the estimates wrong?","nudge":"Distinguish the centre of the estimates from their spread."}})

S.append({"kind":"explore","id":"s2","mins":7,"title":"Giving up unbiasedness to buy a smaller variance",
 "objective":"See why the usual remedies, ridge and principal components, accept bias in exchange for variance.",
 "viz":{"type":"risk-curves","caption":"Squared-error risk against the true value: the unbiased estimator is flat; the shrunk estimator is biased but has far smaller risk near its target."},
 "body":["The flat line is an unbiased estimator. Its risk is its variance, the same everywhere. The curve that dips below it is a shrunk estimator: pulled toward a fixed target, it is biased, but it has much less variance.",
         "Near the target the shrunk estimator wins by a wide margin. Far from the target the bias takes over and it loses. Move the shrinkage weight and watch the crossing point.",
         "Ridge regression and principal components regression work the same way. They are biased by design. When the variance is inflated by a factor of 50, as it is here, a small bias can be a good price."],
 "ask":{"q":"When is shrinking toward a target a bad idea?","nudge":"Look at the right-hand end of the curve."}})

S.append({"kind":"theory","id":"s3","mins":9,"title":"The variance inflation factor, eigenvalues and the four statements",
 "objective":"State the variance formula with the VIF, the eigenvalue view and the effect of near multicollinearity on each property of OLS.",
 "blocks":[
  {"t":"formula","h":"The variance of one coefficient","body":"Var(b_j) = σ² / [ S_jj (1 − R_j²) ]\nS_jj = Σ(x_ij − x̄_j)²,   R_j² = R² of the auxiliary regression of x_j on the other regressors\nVIF_j = 1/(1 − R_j²)"},
  {"t":"step","h":"Reading the formula","body":"S_jj is the spread of x_j: more spread gives less variance. The factor 1/(1 − R_j²) is the inflation caused by the other regressors. If x_j is unrelated to the others, R_j² = 0 and the factor is 1. At R_j² = 0.9 it is 10, and at R_j² = 0.95 it is 20. The standard error is inflated by the square root of the VIF."},
  {"t":"formula","h":"Two regressors with correlation r","body":"VIF = 1/(1 − r²)\nr = 0.9  →  5.26   (standard error × 2.29)\nr = 0.99 →  50.25  (standard error × 7.09)"},
  {"t":"formula","h":"The eigenvalue view","body":"Eigenvalues of the correlation matrix: 1 + r and 1 − r.\nCondition number = √(λ_max/λ_min).   At r = 0.99: √(1.99/0.01) = 14.11\ntr[(X′X)⁻¹] = Σ 1/λ_i, dominated by the smallest eigenvalue."},
  {"t":"def","h":"Perfect multicollinearity","body":"One column of X is an exact combination of the others. Then X′X is singular, (X′X)⁻¹ does not exist, and the normal equations have infinitely many solutions. Only estimable functions of β (topic 6.2) are determined."}],
 "table":{"caption":"Q38's four statements and the property each one concerns","head":["Statement","Concerns","Under near multicollinearity"],
  "rows":[["Small data changes give large changes in estimates","variance","True: variance is inflated"],
          ["Estimates are large in magnitude","variance","True: E|b|² = |β|² + σ²·tr[(X′X)⁻¹]"],
          ["Estimates are biased","mean","FALSE: E(b) = β still"],
          ["Large standard errors, low t, yet R² very high","variance","True: the classic symptom"]]},
 "flow":{"title":"Near multicollinearity: detect, then choose","alt":"A top-to-bottom flow. Compute the variance inflation factor for each regressor. If all are small there is nothing to do. If some are large, ask whether the goal is prediction, interpretation of one coefficient, or estimating a combination. Each goal points to a different remedy.",
  "nodes":[{"id":"a","r":0,"c":1,"label":"Compute VIF_j for every regressor","kind":"start"},
           {"id":"b","r":1,"c":1,"label":"Any VIF above about 10?","kind":"step"},
           {"id":"c","r":2,"c":0,"label":"No: nothing to fix","kind":"end"},
           {"id":"d","r":2,"c":2,"label":"Yes: what is the goal?","kind":"step"},
           {"id":"e","r":3,"c":1,"label":"Prediction in the same pattern: leave it","kind":"end"},
           {"id":"f","r":3,"c":3,"label":"One coefficient: drop, combine, or add data. Shrink: ridge or PCR","kind":"end"}],
  "edges":[{"from":"a","to":"b"},{"from":"b","to":"c"},{"from":"b","to":"d"},{"from":"d","to":"e"},{"from":"d","to":"f"}],
  "note":"A VIF above 10 corresponds to R_j² above 0.90. The threshold is a convention, not a theorem."},
 "ask":{"q":"Which of Q38's four statements is false, and what property does it concern?","nudge":"It concerns the mean of the estimator."}})

S.append({"kind":"worked","id":"s4","mins":8,"title":"Reading the printout from the first scenario",
 "objective":"Diagnose the printout: compute the VIF, the t statistics and F, and explain the change on dropping a regressor.",
 "ask":{"q":"Which numbers on the printout point to multicollinearity and which would not?","nudge":"Compare R² and F with the t statistics."},
 "problem":"n = 20, k = 3. Printout: slopes 0.143 (se 2.007) and 1.685 (se 1.861); R² = 0.8107; correlation of the two regressors 0.9934; critical F(2, 17) = 3.59; critical t(17) = 2.11. Diagnose it.",
 "steps":[
  {"say":"Test each slope on its own.","math":"t₁ = 0.143/2.007 = 0.071\nt₂ = 1.685/1.861 = 0.905\n|t| < 2.11 for both","why":"Neither slope is significant. Checking the division is the habit: t is the coefficient over its own standard error."},
  {"say":"Test the whole regression.","math":"F = (0.8107/2)/(0.1893/17) = 0.40535/0.011135 = 36.40\n36.40 > 3.59","why":"The overall F test rejects. This is the form from topic 6.3: R² over k − 1, divided by 1 − R² over n − k."},
  {"say":"Name the pattern.","math":"high R², significant F, small t's","why":"The model as a whole predicts, and no single regressor can claim credit. This is the signature of near multicollinearity."},
  {"say":"Measure the inflation.","math":"VIF = 1/(1 − 0.9934²) = 1/0.01312 = 76.4\n√VIF = 8.74","why":"Each standard error is about 8.7 times what it would be if the regressors were unrelated."},
  {"say":"Drop the second regressor and compare.","math":"slope 1.949, t = 8.53, R² = 0.8016\nse = 1.949/8.53 = 0.229","why":"R² falls by only 0.0091 and the standard error falls from 2.007 to 0.229. The second regressor added almost no fit and a great deal of variance."},
  {"say":"What the fix does and does not change.","math":"dropping x₂: the coefficient on x₁ now estimates a different quantity","why":"The 1.949 includes whatever part of x₂'s effect travels with x₁. This is omitted-variable bias (topic 6.2), traded for a smaller variance."}],
 "after":"A large VIF is a diagnosis, not a verdict. Decide what you need the coefficients for before removing anything."})

S.append({"kind":"recall","id":"s5","mins":2,"title":"Pause and recall","objective":"Retrieve the formula and the four statements before using them.",
 "intro":"Answer each before revealing it.",
 "items":[{"q":"Write the VIF of a regressor.","a":"VIF_j = 1/(1 − R_j²), where R_j² is from regressing x_j on the other regressors."},
          {"q":"With two regressors correlated at 0.99, what is the VIF?","a":"1/(1 − 0.9801) = 50.25."},
          {"q":"Is OLS biased under near multicollinearity?","a":"No. It stays unbiased and BLUE; the variance is inflated."},
          {"q":"What symptom pair is classic?","a":"High R² and a significant F, with small individual t statistics."},
          {"q":"Which remedies accept bias?","a":"Ridge regression and principal components regression."}]})

S.append({"kind":"completion","id":"s6","mins":8,"title":"Your turn — VIFs from correlations and from R_j²",
 "objective":"Compute variance inflation factors and the matching standard-error inflation.",
 "problem":"Find the VIF for r = 0.9, and the VIF and standard-error inflation for an auxiliary R_j² = 0.95.",
 "steps":[
  {"say":"For two regressors VIF = 1/(1 − r²). Start with r = 0.9.",
   "blank":{"prompt":"What is 1 − r²?","answer":"0.19","accept":["0.19","19/100"],"hint":"0.9 squared is 0.81."},
   "why":"1 − 0.81 = 0.19."},
  {"say":"Invert.",
   "blank":{"prompt":"What is the VIF at r = 0.9, to two decimals?","answer":"5.26","accept":["5.26","5.263","5.3"],"hint":"1 divided by 0.19."},
   "why":"1/0.19 = 5.263. The standard error is inflated by √5.263 = 2.29."},
  {"say":"Now an auxiliary R_j² = 0.95.",
   "blank":{"prompt":"What is the VIF?","answer":"20","accept":["20","twenty","1/0.05"],"hint":"1 divided by 1 − 0.95."},
   "why":"1/0.05 = 20."},
  {"say":"The standard error is multiplied by the square root of the VIF.",
   "blank":{"prompt":"By what factor, to two decimals?","answer":"4.47","accept":["4.47","4.472","4.5"],"hint":"√20."},
   "why":"√20 = 4.472. A VIF of 20 means the standard error is 4.5 times larger than with an unrelated regressor."}],
 "after":"VIF is a variance factor. The standard error moves by its square root."})

S.append({"kind":"theory","id":"s7","mins":7,"title":"Why estimates are large, and the price of the remedies",
 "objective":"Derive E|b|², and compare OLS, principal components and ridge by exact bias and variance.",
 "blocks":[
  {"t":"step","h":"Why the estimates are large in magnitude","body":"E(b′b) = β′β + σ²·tr[(X′X)⁻¹], because E(b) = β and Var(b) = σ²(X′X)⁻¹, and E(b′b) is the squared length of the mean plus the total variance. For two standardised regressors with r = 0.99 and n = 50, tr[(X′X)⁻¹] = 2.0101. With β = (1, 1), |β|² = 2 and σ = 1, so E|b|² = 4.0101: the squared length of the estimates is, on average, twice that of the truth. The trace is Σ1/λ_i, so the smallest eigenvalue dominates."},
  {"t":"step","h":"Prediction: fine along the pattern, poor across it","body":"For a new point x₀, Var(ŷ₀) = σ²x₀′(X′X)⁻¹x₀. With r = 0.99 and n = 50, a point that follows the collinear pattern, (1, 1), has variance 0.0201σ². A point that breaks it, (1, −1), has variance 4.0000σ². The ratio is (1 + r)/(1 − r) = 199. So prediction within the data's own pattern is not damaged; prediction outside it is."},
  {"t":"formula","h":"Principal components regression","body":"Rotate the regressors to their eigenvector directions, which are uncorrelated. Keep the components with large eigenvalues; drop those with tiny ones.\nFor X′X = 50·[[1, 0.99], [0.99, 1]]: eigenvalues 99.5 and 0.5, first direction (1, 1)/√2.\nOLS total variance: 2.0101σ².   One component kept: 0.0101σ²."},
  {"t":"step","h":"The trade, exactly","body":"If β lies along the kept direction, β = (1, 1): PCR is unbiased and its MSE is 0.0101, against 2.0101 for OLS. If β lies along the dropped direction, β = (1, −1): PCR has bias² = 2 and MSE 2.0101, no better than OLS. PCR is a bet that the signal sits in the large-eigenvalue directions."},
  {"t":"step","h":"Ridge","body":"Ridge replaces X′X by X′X + λI. At β = (1, 1): λ = 0.5 gives bias (−0.005, −0.005) and MSE 0.5100; λ = 5 gives MSE 0.0302; OLS (λ = 0) gives 2.0101. A little shrinkage buys a very large variance reduction here. The price is that every coefficient is biased toward zero."},
  {"t":"step","h":"Perfect collinearity","body":"For x₂ = 2x₁ the columns of X have rank 2 of 3. Two solutions of the normal equations differ in b₁ but agree on b₁ + 2b₂ and on every fitted value. The estimable function b₁ + 2b₂ equals the slope of y on x₁ alone. Neither b₁ nor b₂ separately is estimable."}],
 "ask":{"q":"Why does prediction survive multicollinearity when interpretation does not?","nudge":"Which direction in x-space does the data fix well?"}})

S.append({"kind":"guided","id":"s8","mins":8,"title":"On your own — how much does the standard error grow?",
 "objective":"Compute the standard error of a coefficient at r = 0.99 and compare it with the uncorrelated case.",
 "problem":"Two standardised regressors, n = 50, σ = 1. Find sd(b₁) when the regressors are uncorrelated and when r = 0.99, and the ratio.",
 "hints":["Direction: for a standardised regressor S_jj = n = 50, and the variance is σ²/[S_jj(1 − R_j²)].",
          "Method: uncorrelated means R_j² = 0; with r = 0.99, R_j² = 0.9801.",
          "Next step: take square roots, then divide the second by the first."],
 "answer":"sd = 0.1414 uncorrelated; sd = 1.0025 at r = 0.99; ratio 7.09, which is √50.25.",
 "check":"The ratio must equal √VIF. Since VIF = 50.25, √50.25 = 7.09, matching.",
 "scenario":{"teaser":"Pairwise correlations all look moderate, and the variance is still enormous.",
  "title":"Collinearity that no pair reveals",
  "body":["An analyst builds three predictors. The first two are independent. The third is their sum plus a little noise: x₃ = x₁ + x₂ + 0.1ε. She checks the correlation matrix before fitting. The highest pairwise correlation is 0.705, comfortably below the usual worry level of 0.8 or 0.9.",
          "Then she computes VIFs, which regress each predictor on the other two. The auxiliary R² for x₃ is 2/2.01 = 0.995, because x₃ is almost exactly x₁ + x₂. Its VIF is 201. The VIFs of x₁ and x₂ are about 101 each, since each is almost determined by the other two.",
          "A simulation of 400,000 draws agreed: the correlation of x₁ with x₃ was 0.705, and the VIFs were about 201 and 101. A pairwise check would have looked fine and the model would have been close to singular."],
  "q":"Why does a VIF catch what a correlation matrix misses?",
  "answer":"A VIF uses the auxiliary regression of one predictor on all the others together. A predictor can be almost a combination of several others without being highly correlated with any one of them."},
 "solution":[
  {"say":"Uncorrelated case.","math":"Var(b₁) = σ²/(S₁₁) = 1/50 = 0.02\nsd = √0.02 = 0.1414","why":"R_j² = 0 so the inflation factor is 1."},
  {"say":"Correlated case.","math":"R_j² = 0.99² = 0.9801\nVar(b₁) = 1/[50(1 − 0.9801)] = 1/(50 × 0.0199) = 1.0050\nsd = 1.0025","why":"The same data size, but the standard error is seven times larger."},
  {"say":"Ratio.","math":"1.0025/0.1414 = 7.09 = √[1/(1 − r²)] = √50.25","why":"The ratio of standard errors is the square root of the VIF."}]})

S.append({"kind":"trapcheck","id":"s9","mins":6,"title":"Six statements","objective":"Separate what multicollinearity does from what it does not do.",
 "intro":"Decide true or false on all six before revealing any.",
 "items":[
  {"claim":"Near multicollinearity makes the OLS estimators biased.","tf":False,"why":"Unbiasedness needs only E(u) = 0 and fixed X. The estimates stay centred on the truth; their variance is inflated. This is Q38."},
  {"claim":"Estimates being large in magnitude is a consequence of near multicollinearity.","tf":True,"why":"E|b|² = |β|² + σ²tr[(X′X)⁻¹], and the trace grows as the smallest eigenvalue shrinks. It is a variance effect, not a bias."},
  {"claim":"If no pairwise correlation exceeds 0.8, multicollinearity is ruled out.","tf":False,"why":"With x₃ = x₁ + x₂ + 0.1ε the largest pairwise correlation is 0.705 but the VIF of x₃ is 201."},
  {"claim":"A significant overall F test together with insignificant individual t tests suggests multicollinearity.","tf":True,"why":"The regressors jointly predict y, but each one's standard error is inflated so that none is significant alone."},
  {"claim":"Multicollinearity makes predictions at points following the collinear pattern unreliable.","tf":False,"why":"At (1, 1) the prediction variance is 0.0201σ². Only points that break the pattern, such as (1, −1) with 4.0000σ², are badly predicted."},
  {"claim":"Ridge regression removes multicollinearity without introducing bias.","tf":False,"why":"Ridge biases every coefficient toward zero. It lowers the MSE, at λ = 0.5 from 2.0101 to 0.5100 in the worked case, by trading bias for variance."}]})

S.append({"kind":"guided","id":"s10","mins":8,"title":"Transfer — exact collinearity",
 "objective":"Decide what can be estimated when one regressor is exactly twice another.",
 "problem":"x = 1, 2, 3, 4, 5 and y = 2, 4, 5, 4, 5. A model has an intercept, x₁ = x and x₂ = 2x. Is β₁ estimable? Is β₁ + 2β₂? What value does the data give for the one that is?",
 "hints":["Direction: write the columns of X and look for a column that is a multiple of another.",
          "Method: ℓ′β is estimable when ℓ′ lies in the row space of X; every row has the form (1, x, 2x).",
          "Next step: test (0, 1, 0) and (0, 1, 2) against that row space, then fit y on x alone."],
 "answer":"β₁ and β₂ are not estimable separately; β₁ + 2β₂ is estimable and equals the slope 0.6.",
 "check":"Every row of X has x₂ = 2x₁, so β₁x₁ + β₂x₂ = (β₁ + 2β₂)x₁: the model only ever sees the combination β₁ + 2β₂.",
 "solution":[
  {"say":"Rank.","math":"X has 3 columns (1, x, 2x) but rank 2; X′X is singular","why":"The third column is twice the second."},
  {"say":"Estimability.","math":"rows of X: (1, 1, 2), (1, 2, 4), (1, 3, 6), …\n(0, 1, 2) = (1, 2, 4) − (1, 1, 2)   in the row space: estimable\n(0, 1, 0) is not a combination of the rows: not estimable","why":"Every row has the form (1, x, 2x), so the row space is spanned by (1, 0, 0) and (0, 1, 2). The function β₁ + 2β₂ is a difference of two rows."},
  {"say":"Value.","math":"β̂₁ + 2β̂₂ = 0.6 = slope of y on x","why":"Two different solutions of the normal equations gave b₁ = 0.12 and 1.52 but the same b₁ + 2b₂ = 0.6 and the same fitted values."}]})

S.append({"kind":"theory","id":"s11","mins":6,"title":"Where this sits in the syllabus",
 "objective":"Place multicollinearity against the topics that surround it.",
 "blocks":[
  {"t":"step","h":"What it builds on","body":"Topic 6.2 gives Var(β̂) = σ²(X′X)⁻¹, unbiasedness and estimability. Topic 6.3 gives the overall F test, whose significance beside insignificant t values is the symptom. Topic 6.4 reads the high R². Eigenvalues of a symmetric matrix are developed in topic 2.3, and the generalised inverse for the exact case in topic 2.8."},
  {"t":"step","h":"What it contrasts with","body":"Heteroscedasticity (topic 6.7) keeps OLS unbiased but removes the BLUE property, because Var(u) is no longer σ²I. Multicollinearity breaks no assumption of the Gauss–Markov theorem: OLS stays BLUE, and what is large is the variance that BLUE is the smallest of."},
  {"t":"step","h":"What it does not cover","body":"Ridge and principal components regression appear here as the bias–variance trade, with exact figures for one design. Their theory, including how λ and the number of components are chosen, is outside this lesson."}],
 "ask":{"q":"Which assumption of the Gauss–Markov theorem does near multicollinearity violate?","nudge":"Check each one: mean zero, variance σ²I, full column rank."}})

S.append({"kind":"recall","id":"s12","mins":2,"title":"Second recall","objective":"Retrieve the parts that fade first.",
 "intro":"Answer, then reveal.",
 "items":[{"q":"Which Q38 statement is the one that is NOT a consequence?","a":"That the estimates are biased."},
          {"q":"What is the VIF at r = 0.99, and the standard-error inflation?","a":"50.25 and √50.25 = 7.09."},
          {"q":"Which prediction is damaged, along the pattern or across it?","a":"Across it: variance ratio (1 + r)/(1 − r) = 199."},
          {"q":"What does PCR assume about where the signal is?","a":"In the directions with large eigenvalues."},
          {"q":"Why check VIFs and not only pairwise correlations?","a":"A regressor can be nearly a combination of several others without a high pairwise correlation: VIF 201 against a largest pairwise 0.705."}]})

S.append({"kind":"summary","id":"s13","mins":3,"title":"What you should now be able to do","objective":"Check the lesson against its objectives.",
 "body":["State that near multicollinearity leaves OLS unbiased and BLUE and inflates the variance.",
         "Compute a VIF from R_j² or r, and the matching standard-error inflation.",
         "Sort Q38's four statements into mean, variance and interpretation.",
         "Diagnose a printout: high R² and significant F beside small t statistics.",
         "Explain why ridge and principal components accept bias, and why prediction along the pattern survives."]})

S.append({"kind":"theory","id":"s14","mins":8,"ext":True,"title":"Extension — where the VIF comes from",
 "objective":"Derive Var(b_j) = σ²/[S_jj(1 − R_j²)].",
 "blocks":[
  {"t":"step","h":"Partial out the others","body":"Let x̃_j be the residual of x_j after regressing it on the other regressors. The coefficient b_j equals the slope of y on x̃_j, by the Frisch–Waugh result."},
  {"t":"step","h":"Variance of that slope","body":"Var(b_j) = σ²/Σx̃_ij². The residual sum of squares of the auxiliary regression is Σx̃_ij² = S_jj(1 − R_j²), because R_j² is the share of S_jj that the others explain."},
  {"t":"step","h":"Check","body":"For two standardised regressors with r = 0.99 and n = 50: S_jj = 50 and R_j² = 0.9801, so Var(b_j) = 1/(50 × 0.0199) = 1.0050, matching the diagonal of (X′X)⁻¹."}],
 "ask":{"q":"Why does more spread in x_j help?","nudge":"S_jj sits in the denominator."}})

S.append({"kind":"quiz","id":"s15","mins":12,"title":"Mastery test",
 "objective":"Demonstrate it independently, on questions you have not seen.","setId":"regression_t5_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id":"regressiont5", "topicId":"regression-t5", "moduleId":"regression",
 "title":"Multicollinearity",
 "breadcrumb":"Regression → Violations of assumptions → Multicollinearity",
 "engine":"B", "engineName":"The mean is untouched and the variance is inflated by 1/(1 − R_j²)",
 "version":"1.0", "status":"approved",
 "estMin":sum(s["mins"] for s in CORE),
 "objectives":["State what near multicollinearity does and does not do to the OLS estimator.",
               "Compute a variance inflation factor and the standard-error inflation from R_j² or r.",
               "Sort statements such as Q38's into mean, variance and interpretation effects.",
               "Diagnose a printout showing a high R² and significant F beside insignificant t statistics.",
               "Explain why ridge and principal components regression accept bias, and why prediction along the pattern survives."],
 "prereq":[{"id":"p1","name":"The auxiliary regression and R_j²","why":"The VIF is built from it."},
           {"id":"p2","name":"Var(β̂) = σ²(X′X)⁻¹","why":"Every statement here is about the size of its diagonal."},
           {"id":"p3","name":"Eigenvalues of a symmetric matrix","why":"The condition number and the trace of the inverse use them."},
           {"id":"p4","name":"MSE = bias² + variance","why":"It explains why the remedies accept bias."}],
 "traps":["Calling near multicollinearity a cause of bias (Q38: the estimates are NOT biased).",
          "Marking 'estimates are large in magnitude' as not a consequence; it is, through E|b|².",
          "Relying on pairwise correlations and missing a VIF of 201.",
          "Forgetting that the standard error moves by √VIF, not by VIF.",
          "Treating a large VIF as a reason to drop a variable without asking what the coefficient is for."],
 "revision":{
   "sheet":["Near multicollinearity: OLS unbiased and BLUE; variance inflated.",
            "Var(b_j) = σ²/[S_jj(1 − R_j²)]; VIF_j = 1/(1 − R_j²).",
            "Two regressors: VIF = 1/(1 − r²): r = 0.9 gives 5.26, r = 0.99 gives 50.25; standard error × √VIF (2.29, 7.09).",
            "Classic symptom: high R², significant F, small t's.",
            "Q38 answer: C, 'estimates are biased' is NOT a consequence.",
            "E|b|² = |β|² + σ²tr[(X′X)⁻¹] = 4.0101 against |β|² = 2 at r = 0.99, n = 50.",
            "Prediction variance along the pattern 0.0201σ², across it 4.0000σ²: ratio (1 + r)/(1 − r) = 199.",
            "Printout: R² 0.8107, F 36.40, t = 0.071 and 0.905, VIF 76.4; dropping x₂ gives t = 8.53, R² 0.8016.",
            "Hidden collinearity: x₃ = x₁ + x₂ + 0.1ε has largest pairwise r 0.705 but VIF 201.",
            "Bias–variance: PCR one component 0.0101, ridge λ = 0.5 gives 0.5100, OLS 2.0101."],
   "cards":[["VIF","1/(1 − R_j²)"],["Standard error inflation","√VIF"],["Q38: not a consequence","The estimates are biased"],["VIF 10 means R_j² of","0.90"],["Perfect collinearity","X′X singular; only estimable functions are determined"],["Remedies that accept bias","Ridge and principal components regression"]],
   "tricks":["Mean untouched, variance inflated.","Pairs can hide it; VIF cannot.","A negation question: sort each option into mean, variance or interpretation."],
   "shortcuts":["VIF 4 ↔ R_j² 0.75; 5 ↔ 0.80; 10 ↔ 0.90; 20 ↔ 0.95.","√50.25 = 7.09.","(1 + r)/(1 − r) = 199 at r = 0.99."],
   "remember":["Near multicollinearity breaks no Gauss–Markov assumption.","The standard error moves by √VIF."]},
 "howto":"If short of time, the lesson is scenes 3 (the formula and Q38 table), 4 (the printout) and 7 (E|b|² and the remedies). Skip the extension. It deliberately does not cover heteroscedasticity (6.7), restricted least squares, or the choice of the ridge parameter.",
 "refs":[{"title":"Econometrics","where":"Chapter 4, Section on multicollinearity","site":"Bruce Hansen","url":"","type":"Free online textbook","free":True,"checked":"2026-11-06","why":"The variance of a coefficient and the role of the other regressors, scenes 3 and 8."},
         {"title":"Econometric Analysis","where":"Chapter 4, Section 4.9, Multicollinearity","site":"William Greene","url":"","type":"Textbook","free":False,"checked":"2026-11-06","why":"Symptoms, VIF and remedies, scenes 3 and 7."},
         {"title":"Applied Regression Analysis","where":"Chapter 16, Ridge regression and principal components","site":"Draper and Smith","url":"","type":"Textbook","free":False,"checked":"2026-11-06","why":"Ridge and principal components regression, scene 7."}],
 "mastery":{"minQ":10,"pass":80,"draw":10,"fmtMin":{"numeric":70,"multi":70},
            "diffMix":{"easy":3,"moderate":5,"hard":2},"noHints":True,"retestDays":7,
            "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on "
                   "numerical and multi-statement items, answered without hints. Each paper is "
                   "drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style "
                   "paper; NTA publishes no official difficulty split."},
 "provenance":"Anchor: Q38, a negation question whose key is that the estimates are biased. It was answered wrongly by marking another option, so the lesson sorts every option by whether it concerns the mean or the variance. The four variants (omitted-variable bias, heteroscedasticity, principal components regression, damage to interpretation) are covered here and in topic 6.2. Verified by computing in verify_regression_t5.py: VIF 1.0, 1.333, 5.263 and 50.25 for r = 0, 0.5, 0.9, 0.99 and equal to the diagonal of the inverse correlation matrix; eigenvalues 0.01 and 1.99 and condition number 14.11; perfect collinearity with x₂ = 2x₁ (rank 2, two solutions differing in b₁ and agreeing on b₁ + 2b₂ = 0.6); hidden collinearity x₃ = x₁ + x₂ + 0.1ε (pairwise 0.7053, R² 0.9950, VIF 201, simulated at 400,000 draws as 200.8 and 100.7); the exact E|b|² = 4.0101; prediction variances 0.0201 and 4.0000, ratio 199; PCR and ridge bias and variance by exact formula (OLS 2.0101, PCR 0.0101 with β on the kept direction and 2.0101 on the dropped one, ridge 0.5100 and 0.0302); a seeded 20-observation data set giving R² 0.8107, F 36.40, t 0.071 and 0.905, VIF 76.4, and after dropping x₂ a slope t of 8.53 and R² 0.8016. By simulation: unbiasedness (means 1.0012 and 0.9986 for true 1, 1 at 60,000 draws), E|b|² (3.4489 against the exact 3.4455 for that sample design), and the correlation −0.98 between the two estimates. Three hand-rounded figures were wrong until the script caught them (the trace 2.01 against the exact 2.0101, and two prediction variances). Scope: heteroscedasticity is 6.7; ridge parameter choice is not covered.",
 "scenes":S}

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id":"regression-t5-m-%02d"%i, "format":fmt, "topic":"regression-t5",
         "diff":diff, "stem":stem, "options":opts, "answer":ans, "explanation":exp}
    d.update(kw); return d

def verd(a,b,c,dd):
    return {"A":{"tf":a[0],"why":a[1]},"B":{"tf":b[0],"why":b[1]},
            "C":{"tf":c[0],"why":c[1]},"D":{"tf":dd[0],"why":dd[1]}}

I = []
I.append(q(1,"single","easy","Which of the following is NOT a consequence of near (but not perfect) multicollinearity for the OLS estimator?",
  ["The estimates are biased","Small changes in the data produce large changes in the estimates","The estimates have high standard errors and low t values although R² is very high","The estimates are large in magnitude"],"A",
  "Near multicollinearity breaks no Gauss–Markov assumption, so the estimator stays unbiased and BLUE. The other three are all effects of the inflated variance, including large estimates, since E|b|² = |β|² + σ²tr[(X′X)⁻¹]."))
I.append(q(2,"single","easy","Multicollinearity primarily damages:",
  ["the interpretation of individual coefficients","the R² of the model","the overall F test","prediction within the range of the data"],"A",
  "The data fix the combined effect of the collinear regressors well but not the split between them, so each coefficient is imprecise. R², F and in-pattern prediction are not harmed."))
I.append(q(3,"single","easy","Principal components regression addresses multicollinearity by:",
  ["using orthogonal linear combinations of the regressors","transforming the dependent variable","weighting the observations","dropping observations"],"A",
  "Rotating to the eigenvector directions gives uncorrelated components. The components with tiny eigenvalues are the unstable ones and are dropped or shrunk. Transforming y, weighting observations or deleting rows does not remove the dependence among regressors."))
I.append(q(4,"numeric","easy","If regressing x_j on the other regressors gives R_j² = 0.75, the variance inflation factor of x_j is:",
  ["4","0.25","1.33","3"],"A",
  "VIF_j = 1/(1 − R_j²) = 1/0.25 = 4. The value 0.25 is 1 − R_j² and 1.33 is 1/R_j².",
  check="A VIF is never below 1, which excludes 0.25."))
I.append(q(5,"single","easy","The variance inflation factor of the j-th regressor is defined as:",
  ["1/(1 − R_j²), where R_j² is from regressing x_j on the other regressors","1/R_j²","1 − R_j²","R_j²/(1 − R_j²)"],"A",
  "VIF_j = 1/(1 − R_j²) is the factor by which Var(b_j) exceeds its value when x_j is uncorrelated with the others. The other three are not the inflation factor."))
I.append(q(6,"single","easy","When one regressor is an exact linear combination of the others, the matrix X′X is:",
  ["singular, so the OLS solution is not unique","diagonal","the identity matrix","negative definite"],"A",
  "An exact dependence among the columns gives a rank-deficient X, hence a singular X′X and infinitely many solutions of the normal equations. Only estimable functions are determined."))
I.append(q(7,"numeric","moderate","Two regressors have correlation r = 0.9. The variance inflation factor of each is:",
  ["5.26","10.0","1.9","0.19"],"A",
  "VIF = 1/(1 − r²) = 1/0.19 = 5.26. The value 0.19 is 1 − r², the value 1.9 is 1 + r, and 10.0 is the result of treating r = 0.9 as R_j² of 0.9 in 1/(1 − R_j²).",
  check="At r = 0.9 the factor must lie above 1 and well below the 50 seen at r = 0.99."))
I.append(q(8,"numeric","moderate","A regressor has VIF = 20. By what factor is its standard error inflated, compared with an uncorrelated regressor?",
  ["4.47","20","10","2.5"],"A",
  "Variance is inflated by the VIF and the standard error by its square root: √20 = 4.47. The value 20 is the variance factor.",
  check="The standard-error factor is smaller than the variance factor 20, which rules out 20."))
I.append(q(9,"single","moderate","A regression reports R² = 0.81 and a significant overall F, yet every slope has an insignificant t statistic. The most likely reason is:",
  ["near multicollinearity among the regressors","autocorrelated errors","omitted-variable bias","a wrongly specified dependent variable"],"A",
  "Collinear regressors jointly explain y, so R² and F are high, while each coefficient's standard error is inflated and its t is small. The other three do not produce this particular pattern."))
I.append(q(10,"multi","moderate","In a regression with two highly but not perfectly correlated regressors.",
  ["A, B and C only","A and B only","B, C and D only","A, B, C and D"],"A",
  "The estimator is unbiased, its variance is inflated by the VIF, and predictions at points that follow the collinear pattern are precise. The estimates are not biased.",
  statements=["The OLS estimators remain unbiased","The variances of the coefficient estimates are inflated","Predictions at points following the collinear pattern remain precise","The OLS estimators become biased"],
  verdicts=verd((True,"E(u) = 0 and fixed X are untouched."),
                (True,"Var(b_j) is multiplied by 1/(1 − R_j²)."),
                (True,"Var(ŷ₀) = 0.0201σ² at (1, 1) for r = 0.99, n = 50."),
                (False,"Unbiasedness does not need uncorrelated regressors."))))
I.append(q(11,"single","moderate","Why can a check of the pairwise correlations miss multicollinearity?",
  ["A regressor can be almost a combination of several others without a high correlation with any one","Pairwise correlations are always biased","Pairwise correlations ignore the sign","The VIF is the same as the largest pairwise correlation"],"A",
  "In the example x₃ = x₁ + x₂ + 0.1ε the largest pairwise correlation is 0.705 but the VIF of x₃ is 201. The VIF uses the regression on all the other regressors together."))
I.append(q(12,"numeric","moderate","For two standardised regressors with r = 0.9, the variance of a prediction at a point that breaks the pattern, (1, −1), compared with a point that follows it, (1, 1), is larger by the factor:",
  ["19","9.5","1.9","81"],"A",
  "The ratio is (1 + r)/(1 − r) = 1.9/0.1 = 19. The value 1.9 is 1 + r and 81 is 1/(1 − r)².",
  check="The ratio must be much larger than 1, and at r = 0.99 it would be 199, so a smaller r gives a smaller ratio, 19."))
I.append(q(13,"single","moderate","Which of the following DOES cause bias in the OLS estimator of a coefficient?",
  ["Omission of a relevant variable correlated with the regressor","Near multicollinearity among the regressors","Heteroscedastic errors","A large sample"],"A",
  "Omitting a relevant correlated variable violates E(u) = 0 for the fitted model and gives bias β₂δ. Near multicollinearity, heteroscedasticity and sample size leave OLS unbiased."))
I.append(q(14,"numeric","moderate","The eigenvalues of the correlation matrix of the regressors are 100 and 0.04. The condition index √(λ_max/λ_min) is:",
  ["50","2500","5","25"],"A",
  "√(100/0.04) = √2500 = 50, well above the common warning level of 30. The value 2500 is the ratio before taking the square root.",
  check="A condition index of 50 exceeds 30, and the ratio 2500 exceeds the index, so 2500 is the unrooted figure."))
I.append(q(15,"single","moderate","Ridge regression reduces the effect of multicollinearity by:",
  ["accepting some bias in exchange for a smaller variance","removing all bias from OLS","increasing the sample size","making the regressors uncorrelated"],"A",
  "Ridge adds λ to the diagonal of X′X, which shrinks the coefficients and cuts the variance. It is biased by design. At λ = 0.5 in the worked example the MSE falls from 2.0101 to 0.5100."))
I.append(q(16,"multi","moderate","Regarding remedies for multicollinearity.",
  ["A, B and C only","A and B only","B, C and D only","A, B, C and D"],"A",
  "Principal components regression uses orthogonal combinations, ridge is biased, and keeping all components reproduces OLS. PCR is not unbiased in general: it is unbiased only if the true coefficients lie in the kept directions.",
  statements=["Principal components regression uses orthogonal linear combinations of the regressors","Ridge regression is biased","Principal components regression keeping all components is the same as OLS","Principal components regression is always unbiased"],
  verdicts=verd((True,"The components are the eigenvector directions of X′X."),
                (True,"It shrinks every coefficient toward zero."),
                (True,"Dropping nothing leaves the full least-squares fit."),
                (False,"With β along the dropped direction the bias² was 2 in the worked case."))))
I.append(q(17,"numeric","hard","Two standardised regressors have r = 0.99, n = 50, σ = 1 and true β = (1, 1), so tr[(X′X)⁻¹] = 2.0101. The expected squared length E|b|² of the OLS estimate is:",
  ["4.01","2.00","2.01","6.02"],"A",
  "E|b|² = |β|² + σ²tr[(X′X)⁻¹] = 2 + 2.0101 = 4.0101. The value 2.00 is the squared length of the truth alone and 2.01 is the variance part alone.",
  check="Since E(b) = β the estimates are on average longer than β by the total variance, so the answer exceeds |β|² = 2."))
I.append(q(18,"numeric","hard","Three predictors satisfy x₃ = x₁ + x₂ + 0.1ε with x₁, x₂ independent standard normals. The VIF of x₃ is:",
  ["201","1.99","101","0.995"],"A",
  "The auxiliary R² of x₃ on x₁ and x₂ is 2/2.01 = 0.995, so VIF = 1/(1 − 0.995) = 201. The value 1.99 is the VIF a pairwise correlation of 0.705 would suggest, and 101 is the VIF of x₁ or x₂.",
  check="R² of 0.995 gives 1/0.005 = 200, so the answer must be about 200."))
I.append(q(19,"numeric","hard","In the r = 0.99, n = 50 design with β = (1, 1), OLS has MSE 2.0101. Ridge with λ = 0.5 has bias (−0.005, −0.005) and total variance 0.5100. Its total MSE is approximately:",
  ["0.51","2.01","0.01","0.005"],"A",
  "MSE = bias² + variance = 2 × 0.005² + 0.5099 ≈ 0.51. The squared bias is only 0.00005, negligible beside the variance. Ridge cuts the MSE from 2.01 to 0.51.",
  check="Ridge reduces MSE below OLS's 2.0101 here, and bias² is tiny, so the answer is the variance, about 0.51."))
I.append(q(20,"single","hard","In a model with an intercept, x₁ = x and x₂ = 2x. Which function of the coefficients is estimable?",
  ["β₁ + 2β₂","β₁ alone","β₂ alone","β₁ − 2β₂"],"A",
  "Every row of X has the form (1, x, 2x), so the model sees only (β₁ + 2β₂)x. The combination β₁ + 2β₂ is in the row space. Neither coefficient alone, nor β₁ − 2β₂, is."))

LET = "ABCD"
_r = random.Random(20260615); PAT = list("ABCD" * 5); _r.shuffle(PAT)
WANT = {"regression-t5-m-%02d" % (i + 1): PAT[i] for i in range(20)}

def swapletters(t, a, b):
    sw = lambda L: b if L == a else a if L == b else L
    def fix(m):
        head, body = m.group(1), m.group(2)
        return head + re.sub(r"[ABCD]", lambda n: sw(n.group(0)), body)
    return re.sub(r"([Oo]ptions?\s+)([ABCD](?:\s*(?:,|and|or)\s*[ABCD])*)", fix, t)

def relabel(items):
    for it in items:
        w = WANT.get(it["id"])
        if not w or not it.get("options"): continue
        i, j = LET.index(it["answer"]), LET.index(w)
        if i == j: continue
        o = it["options"]; o[i], o[j] = o[j], o[i]
        it["answer"] = w
        a, b = LET[i], LET[j]
        for fld in ("explanation", "check"):
            if it.get(fld): it[fld] = swapletters(it[fld], a, b)
    return items

relabel(I)
_k = {}
for _it in I: _k[_it["answer"]] = _k.get(_it["answer"], 0) + 1
print("key spread:", {L: _k.get(L, 0) for L in LET}, "cap", -(-len(I) * 2 // 5))

POOLD = {"moduleId":"regression","topicId":"regression-t5","source":"mastery",
         "label":"Multicollinearity — mastery test (unseen)","count":len(I),"items":I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT,"w",encoding="utf-8") as f:  json.dump(LES,f,ensure_ascii=False,indent=1)
with io.open(POOL,"w",encoding="utf-8") as f: json.dump(POOLD,f,ensure_ascii=False,indent=1)
print("wrote %s: %d scenes (%d core), estMin %d"%(OUT,len(S),len(CORE),LES["estMin"]))
print("wrote %s: %d items"%(POOL,len(I)))
