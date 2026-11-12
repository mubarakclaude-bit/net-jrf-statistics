#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regression-t2 (topic 6.2): Gauss–Markov, BLUE, estimability. Anchor Q11; Q38 variants.
Every figure below is computed in verify_regression_t1_t4.py; nothing is recalled."""
import json, io, os, re, random

OUT  = "seed/lesson_rg2.json"
POOL = "seed/regression_t2_mastery.json"

S = []

S.append({"kind":"foundation","id":"s0","mins":7,"title":"Before the lesson — four things it will assume",
 "objective":"Check linearity, unbiasedness, the variance of a weighted sum and the rank idea behind estimability.",
 "ask":{"q":"If an estimator is a′y with fixed weights a, what is its variance when Var(y) = σ²I?","nudge":"Square each weight."},
 "body":["An estimator is a rule that turns data into a number. A linear estimator turns the data into that number by a weighted sum: a₁y₁ + a₂y₂ + … + aₙyₙ, with weights that are fixed in advance and do not depend on y. Unbiased means the rule hits the true value on average.",
         "Among all linear unbiased rules for a parameter there are usually infinitely many. They differ in how noisy they are. The Gauss–Markov theorem says which one is least noisy: the least-squares rule. This lesson proves it, and then asks the question the June paper asked in Q11, which is to find that best rule when the model has two unknowns and three equations.",
         "The earlier mark was lost on the divisors, not the method. The working was right and the answer was written with 2 and 6 swapped. The aim here is to check an answer by a test that takes thirty seconds: does it give the right expected value?"],
 "items":[
  {"ask":"For fixed weights a and Var(y) = σ²I, what is Var(a′y)?",
   "recall":"σ²a′a, which is σ² times the sum of the squared weights.",
   "refresh":["Var(a′y) = a′Var(y)a. With Var(y) = σ²I this is σ²a′Ia = σ²a′a = σ²(a₁² + a₂² + … + aₙ²).",
              "So the noise of a weighted sum is the sum of squared weights times σ². Big weights mean big noise. Two weights of 1/2 give (1/4 + 1/4)σ² = σ²/2; one weight of 1 gives σ². Spreading the weight reduces variance."]},
  {"ask":"What does it mean for a′y to be unbiased for ℓ′β in y = Xβ + u?",
   "recall":"E(a′y) = ℓ′β for every β, which means a′X = ℓ′.",
   "refresh":["E(a′y) = a′E(y) = a′Xβ. For this to equal ℓ′β whatever β is, the vector multiplying β must match: a′X = ℓ′. That single equation is the unbiasedness condition.",
              "It is a test you can run on any candidate answer: multiply the weights into the columns of X and see whether you get the target back."]},
  {"ask":"What is the rank of a matrix and what is its row space?",
   "recall":"Rank = the number of linearly independent rows (or columns); the row space is all weighted sums of the rows.",
   "refresh":["The rows of X are vectors. Their weighted sums fill a space, the row space of X. The rank is the dimension of that space.",
              "Example: the rows (1, 1, 0), (1, 1, 0), (1, 0, 1), (1, 0, 1) include only two different directions, so the rank is 2 even though X has 3 columns."]},
  {"ask":"What is the OLS estimator and its covariance matrix?",
   "recall":"β̂ = (X′X)⁻¹X′y and Var(β̂) = σ²(X′X)⁻¹.",
   "refresh":["From topic 6.1: β̂ = (X′X)⁻¹X′y. It is a linear estimator, since it is a fixed matrix times y.",
              "Var(β̂) = (X′X)⁻¹X′(σ²I)X(X′X)⁻¹ = σ²(X′X)⁻¹. If X′X is diagonal the inverse is diagonal, so the estimators are uncorrelated."]}]})

S.append({"kind":"intuition","id":"s1","mins":7,"title":"Best means least noisy among the unbiased linear rules",
 "objective":"State what BLUE means and why 'best' is only claimed inside a class.",
 "body":["Best Linear Unbiased Estimator: three adjectives, each one a restriction. Linear: a weighted sum of the data. Unbiased: right on average. Best: the smallest variance. The claim is never that least squares beats every possible estimator. It is that no other rule that is linear and unbiased is less noisy.",
         "Think of two scales weighing the same object. One reads the true weight plus noise. The other reads twice the true weight plus noise. Averaging them sensibly means trusting the second scale more, because its signal is larger relative to the same noise. The right weights come out of the algebra: (y₁ + 2y₂)/5.",
         "Leave the class and the claim no longer holds. A rule that is slightly biased can have a much smaller variance, and so a smaller total error. That is why the theorem does not rule out shrinkage estimators; it only says that among unbiased linear rules, none beats OLS."],
 "scenario":{"teaser":"Three readings, two unknowns: how to combine them.",
  "title":"Three equations, two unknowns",
  "body":["A laboratory measures two quantities, β₁ and β₂, through three instruments. Instrument one reads β₁ + β₂, instrument two reads 2β₁, and instrument three reads β₁ − β₂. Each reading carries independent noise with the same variance σ².",
          "There are three readings and only two unknowns, so the readings cannot all be matched exactly. Averaging in the obvious way, giving each reading equal weight, would treat instrument two the same as the others even though it speaks only about β₁ and speaks twice as loudly about it.",
          "The least-squares answer weights the readings by how much information each carries about each unknown. For β₁ it turns out to be (y₁ + 2y₂ + y₃)/6, and for β₂ it is (y₁ − y₃)/2. Instrument two is ignored for β₂ because it contains no β₂ at all."],
  "q":"Why does the estimator for β₂ give y₂ zero weight?",
  "answer":"Because y₂ = 2β₁ + u₂ has no β₂ in it. Its weight on β₂ must be 0 for the estimator to be unbiased for β₂ whatever β₁ is."},
 "ask":{"q":"Can a biased estimator ever have a smaller mean squared error than OLS?","nudge":"The theorem only compares inside one class."}})

S.append({"kind":"explore","id":"s2","mins":7,"title":"Unbiased is a restriction, not a virtue in itself",
 "objective":"See that giving up a little bias can lower the total error, and why Gauss–Markov stays inside the unbiased class.",
 "viz":{"type":"risk-curves","caption":"Squared-error risk: the sample mean is flat and unbiased; the shrinkage estimator wins near the target and loses far from it."},
 "body":["The flat line is the risk of the sample mean, an unbiased estimator. Its risk is its variance, the same for every θ. Gauss–Markov is a statement about this kind of estimator: nothing in the same class has a lower line.",
         "Now raise the shrinkage weight toward 0. The shrinkage estimator is biased, and its risk dips below the flat line near the target and rises above it far from the target. This is the trade the theorem does not forbid.",
         "So the theorem is exact and narrow. Inside the unbiased linear class OLS is optimal; outside it, a different trade-off can win somewhere."],
 "ask":{"q":"Where on the θ axis does the shrinkage estimator beat the sample mean?","nudge":"Look near the constant guess."}})

S.append({"kind":"theory","id":"s3","mins":9,"title":"The Gauss–Markov theorem",
 "objective":"State the assumptions and the conclusion, and see where each assumption is used.",
 "blocks":[
  {"t":"formula","h":"Setting","body":"y = Xβ + u,   E(u) = 0,   Var(u) = σ²I,   X fixed with full column rank"},
  {"t":"formula","h":"The theorem","body":"Among all estimators ℓ′β̃ = c′y that are linear in y and unbiased for ℓ′β:\n    Var(c′y) ≥ Var(ℓ′β̂) = σ²ℓ′(X′X)⁻¹ℓ\nwith equality only for c′y = ℓ′β̂."},
  {"t":"def","h":"What each assumption buys","body":"E(u) = 0: makes OLS unbiased.\nVar(u) = σ²I: makes Var(β̂) = σ²(X′X)⁻¹ and the proof's last step work. It means constant variance and zero correlation.\nFull column rank: makes β̂ unique. Without it use estimability.\nNormality: not needed."},
  {"t":"step","h":"Proof in four lines","body":"Take any linear unbiased c′y. Unbiasedness gives c′X = ℓ′. Write c = a + d, where a′ = ℓ′(X′X)⁻¹X′ is the OLS weight vector. Then d′X = c′X − a′X = ℓ′ − ℓ′ = 0. Also a′d = ℓ′(X′X)⁻¹X′d = ℓ′(X′X)⁻¹(d′X)′ = 0. So Var(c′y) = σ²c′c = σ²(a′a + d′d) ≥ σ²a′a, with equality exactly when d = 0."}],
 "table":{"caption":"What goes wrong when an assumption fails","head":["Assumption fails","Unbiased?","BLUE?","Remedy"],
  "rows":[["E(u) = 0 (omitted correlated regressor)","No","No","Add the regressor"],
          ["Var(u) not σ²I (heteroscedastic or correlated)","Yes","No","GLS (topic 6.7)"],
          ["Near multicollinearity","Yes","Yes","Accept large variance; see topic 6.5"],
          ["Errors not normal","Yes","Yes","Nothing needed for BLUE"]]},
 "flow":{"title":"Checking that an estimator is the BLUE","alt":"A top-to-bottom flow. First check the weights are fixed. Then check unbiasedness a prime X equals l prime. Then compare variance with sigma squared l prime X prime X inverse l.",
  "nodes":[{"id":"a","r":0,"c":1,"label":"Write the candidate as c′y","kind":"start"},
           {"id":"b","r":1,"c":1,"label":"Test c′X = ℓ′ (unbiased?)","kind":"step"},
           {"id":"c","r":2,"c":0,"label":"No: reject the candidate","kind":"end"},
           {"id":"d","r":2,"c":2,"label":"Yes: compute σ²c′c","kind":"step"},
           {"id":"e","r":3,"c":2,"label":"Equals σ²ℓ′(X′X)⁻¹ℓ? Then it is the BLUE","kind":"end"}],
  "edges":[{"from":"a","to":"b"},{"from":"b","to":"c"},{"from":"b","to":"d"},{"from":"d","to":"e"}],
  "note":"The unbiasedness test eliminates most wrong answers before any variance is computed."},
 "ask":{"q":"Which assumption is NOT needed for the Gauss–Markov conclusion?","nudge":"It is a distributional one."}})

S.append({"kind":"worked","id":"s4","mins":8,"title":"Q11 in full",
 "objective":"Find the BLUE of (β₁, β₂) for the three-equation model and check every option.",
 "ask":{"q":"Why are the divisors 6 and 2, and in which order?","nudge":"Read the diagonal of X′X."},
 "problem":"y₁ = β₁ + β₂ + u₁; y₂ = 2β₁ + u₂; y₃ = β₁ − β₂ + u₃, with V(uᵢ) = σ². Find the BLUE of β₁ and β₂ and the covariance matrix.",
 "steps":[
  {"say":"Write the model as y = Xβ + u.","math":"X = [[1, 1], [2, 0], [1, −1]]","why":"Each row holds the coefficients of (β₁, β₂) in one equation."},
  {"say":"Form X′X.","math":"X′X = [[1+4+1, 1+0−1], [1+0−1, 1+0+1]] = [[6, 0], [0, 2]]","why":"Entry (1,1) is the sum of squares of column one: 1² + 2² + 1² = 6. Entry (2,2) is 1² + 0² + (−1)² = 2. The off-diagonal entry is the dot product of the two columns: 1 + 0 − 1 = 0."},
  {"say":"Form X′y.","math":"X′y = (y₁ + 2y₂ + y₃,  y₁ + 0·y₂ − y₃)","why":"Each entry is a column of X dotted into y."},
  {"say":"Invert and solve.","math":"(X′X)⁻¹ = diag(1/6, 1/2)\nβ̂₁ = (y₁ + 2y₂ + y₃)/6\nβ̂₂ = (y₁ − y₃)/2","why":"A diagonal matrix inverts by inverting its diagonal. The larger sum of squares, 6, sits under β₁. The divisors are 6 then 2."},
  {"say":"Covariance matrix.","math":"Var(β̂) = σ²·diag(1/6, 1/2)\nVar(β̂₁) = σ²/6,   Var(β̂₂) = σ²/2,   Cov = 0","why":"The zero covariance is the diagonal X′X again."},
  {"say":"Test each option for unbiasedness by multiplying weights into X.","math":"Option with (1,2,1)/2 for β₁: E = (1/2)(1+4+1)β₁ = 3β₁   — biased\nOption with 6(y₁+y₂+y₃): E = 6(4β₁) = 24β₁   — biased\n(1,2,1)/6 and (1,0,−1)/2: E = β₁ and β₂   — unbiased","why":"Each wrong option fails in under a minute. The expected value of a wrong divisor is a multiple of the true value, not the true value."},
  {"say":"Verify with numbers.","math":"y = (7, 4, 3):  β̂₁ = (7 + 8 + 3)/6 = 3,   β̂₂ = (7 − 3)/2 = 2","why":"Consistency check: β₁ + β₂ = 5 against y₁ = 7, 2β₁ = 6 against y₂ = 4, β₁ − β₂ = 1 against y₃ = 3. The fit is a compromise."}],
 "after":"The habit: after finding an answer, multiply its weights into the columns of X. The target must come back."})

S.append({"kind":"recall","id":"s5","mins":2,"title":"Pause and recall","objective":"Retrieve the theorem and the checks before using them.",
 "intro":"Answer each before revealing it.",
 "items":[{"q":"What does BLUE stand for?","a":"Best linear unbiased estimator: least variance among linear unbiased rules."},
          {"q":"What is the unbiasedness test for c′y as an estimator of ℓ′β?","a":"c′X = ℓ′."},
          {"q":"What is Var(β̂)?","a":"σ²(X′X)⁻¹."},
          {"q":"Is normality needed for Gauss–Markov?","a":"No. Only E(u) = 0 and Var(u) = σ²I."},
          {"q":"What does a diagonal X′X imply about the estimators?","a":"They are uncorrelated."}]})

S.append({"kind":"completion","id":"s6","mins":8,"title":"Your turn — two readings, one unknown",
 "objective":"Find the BLUE for y₁ = β + u₁, y₂ = 2β + u₂ and compare it with two rivals.",
 "problem":"y₁ = β + u₁ and y₂ = 2β + u₂ with equal variances σ². Find the BLUE, its variance, and show that (y₁ + y₂)/3 is unbiased but worse.",
 "steps":[
  {"say":"X = (1, 2)′. Compute X′X.",
   "blank":{"prompt":"What is X′X?","answer":"5","accept":["5","five","1+4"],"hint":"1² + 2²."},
   "why":"1 + 4 = 5, and X′y = y₁ + 2y₂, so β̂ = (y₁ + 2y₂)/5."},
  {"say":"The variance is σ²(X′X)⁻¹.",
   "blank":{"prompt":"What is Var(β̂) as a multiple of σ²?","answer":"1/5","accept":["1/5","0.2","σ²/5","0.20"],"hint":"Invert the scalar 5."},
   "why":"σ²/5 = 0.2σ². Also the sum of squared weights: (1² + 2²)/25 = 5/25."},
  {"say":"Test the rival (y₁ + y₂)/3: E = (β + 2β)/3 = β, so it is unbiased. Its variance is (1/9 + 1/9)σ².",
   "blank":{"prompt":"What is its variance as a multiple of σ²?","answer":"2/9","accept":["2/9","0.2222","0.222","0.22"],"hint":"Square each weight 1/3 and add."},
   "why":"2/9 = 0.222 is greater than 1/5 = 0.2, as the theorem requires."},
  {"say":"Test the rival y₂/2: unbiased since E = β.",
   "blank":{"prompt":"What is its variance as a multiple of σ²?","answer":"1/4","accept":["1/4","0.25","σ²/4"],"hint":"The single weight is 1/2."},
   "why":"1/4 = 0.25 > 0.2. The rival (y₁ + y₂)/2 has E = 1.5β and is not even unbiased."}],
 "after":"Three unbiased rules, three variances: 0.2, 0.222 and 0.25 (times σ²). The BLUE is the smallest."})

S.append({"kind":"theory","id":"s7","mins":7,"title":"Estimability, and what breaks what",
 "objective":"Decide which linear functions can be estimated when X is rank-deficient, and classify the Q38 statements.",
 "blocks":[
  {"t":"def","h":"Estimable","body":"ℓ′β is estimable when some linear unbiased estimator of it exists, which holds exactly when ℓ′ lies in the row space of X. Equivalently, ℓ′ = c′X for some c."},
  {"t":"step","h":"A two-group example","body":"Two groups of two observations each, with parameters α, τ₁, τ₂. The rows of X are (1,1,0), (1,1,0), (1,0,1), (1,0,1). Rank is 2, with 3 parameters. Check τ₁ − τ₂ = (0, 1, −1): it is (1,1,0) − (1,0,1), a difference of rows, so it is estimable. α + τ₁ = (1,1,0) is a row, so it is estimable. τ₁ alone is (0,1,0), which is not a combination of the two row types, so it is not estimable."},
  {"t":"step","h":"Why estimable functions are well defined","body":"The normal equations have many solutions when X′X is singular, but an estimable ℓ′β̂ takes the same value on all of them. For group means 4 and 9, τ̂₁ − τ̂₂ = −5 for every solution, while τ̂₁ alone changes with the solution chosen."},
  {"t":"formula","h":"Omitted-variable bias","body":"True model y = β₁x₁ + β₂x₂ + u. Regressing y on x₁ alone gives\n    E(b₁*) = β₁ + β₂δ,   where δ = slope of x₂ on x₁\nBias = β₂δ. It vanishes when β₂ = 0 or when x₂ is uncorrelated with x₁."},
  {"t":"step","h":"Heteroscedasticity and multicollinearity","body":"Under heteroscedasticity E(β̂) = β still holds, since unbiasedness uses only E(u) = 0. But Var(β̂) ≠ σ²(X′X)⁻¹ and OLS is no longer best. Under near multicollinearity the assumptions all hold, so OLS stays unbiased and BLUE; its variance is inflated by 1/(1 − r²), which is 50.25 at r = 0.99. The estimates are unstable, not biased."}],
 "ask":{"q":"Which of omission, heteroscedasticity and near multicollinearity makes OLS biased?","nudge":"Only one violates E(u) = 0 for the fitted model."}})

S.append({"kind":"guided","id":"s8","mins":8,"title":"On your own — bias from an omitted variable",
 "objective":"Compute the expected value of a short regression when a relevant variable is left out.",
 "problem":"True model y = 1·x₁ + 2·x₂ + u. The regression of x₂ on x₁ has slope δ = 0.6. A student regresses y on x₁ alone. Find E(b₁*) and the bias.",
 "hints":["Direction: identify which variable has been left out and what its true coefficient is.",
          "Method: the short-regression slope has expectation β₁ + β₂δ.",
          "Next step: multiply β₂ by δ, then add β₁."],
 "answer":"Bias = 2 × 0.6 = 1.2, and E(b₁*) = 1 + 1.2 = 2.2.",
 "check":"The sign of the bias is the product of the signs of β₂ and δ, here positive, and |bias| ≤ |β₂| because |δ| < 1.",
 "scenario":{"teaser":"A regression with two nearly identical predictors, and the data are enough to estimate neither.",
  "title":"Two predictors that move together",
  "body":["An analyst regresses a score on two predictors whose correlation in the sample is 0.99. The overall F test is highly significant and R² is large, yet neither coefficient has a significant t statistic, and dropping one observation changes both estimates sharply.",
          "She wonders whether the estimates are biased. They are not. Unbiasedness needs E(u) = 0 and a fixed full-rank X, and both hold. Near collinearity does not break any Gauss–Markov assumption. What it does is inflate the variance of each coefficient by the factor 1/(1 − r²) = 50.25 at r = 0.99, so the standard deviation grows by about 7.1.",
          "In a simulation of 20,000 samples of size 50 at this correlation, the average of the two estimates was 1.008 and 0.993 for a true pair of 1 and 1, so there is no bias, but the spread of each estimate matched the formula and was about 7.9 times that of an orthogonal design with the same sample correlation removed."],
  "q":"Which of the following is NOT a consequence of near multicollinearity: large standard errors, unstable estimates, bias, or a high R² with insignificant t values?",
  "answer":"Bias. Near multicollinearity keeps OLS unbiased and BLUE and inflates the variance. This is the answer to Q38 of the June paper."},
 "solution":[
  {"say":"Identify the omitted variable's coefficient.","math":"β₂ = 2,   δ = 0.6","why":"x₂ is the variable left out; δ is how much of it rides on x₁."},
  {"say":"Bias.","math":"bias = β₂δ = 2 × 0.6 = 1.2","why":"The short regression credits x₁ with the part of x₂'s effect that travels with it."},
  {"say":"Expected slope.","math":"E(b₁*) = β₁ + β₂δ = 1 + 1.2 = 2.2","why":"Simulation with 40,000 samples gave 2.2008."}]})

S.append({"kind":"trapcheck","id":"s9","mins":6,"title":"Six statements","objective":"Separate what each assumption failure really breaks.",
 "intro":"Decide true or false on all six before revealing any.",
 "items":[
  {"claim":"Near multicollinearity makes the OLS estimators biased.","tf":False,"why":"Unbiasedness needs only E(u) = 0 and fixed X. Multicollinearity inflates variance, not bias."},
  {"claim":"Under heteroscedasticity OLS remains unbiased but is no longer BLUE.","tf":True,"why":"E(β̂) = β uses only E(u) = 0. Best needs Var(u) = σ²I."},
  {"claim":"Gauss–Markov requires the errors to be normally distributed.","tf":False,"why":"Only the first two moments are used: mean zero and variance σ²I."},
  {"claim":"Any unbiased linear estimator of β has the same variance as OLS.","tf":False,"why":"OLS has the smallest. For y₁ = β + u₁, y₂ = 2β + u₂ the rule (y₁ + y₂)/3 is unbiased with variance 2σ²/9, above σ²/5."},
  {"claim":"If X′X is diagonal the least squares estimators are uncorrelated.","tf":True,"why":"Cov(β̂) = σ²(X′X)⁻¹ is diagonal when X′X is."},
  {"claim":"In a rank-deficient design every linear function of β is estimable.","tf":False,"why":"ℓ′β is estimable only if ℓ′ is in the row space of X. In the two-group design τ₁ alone is not."}]})

S.append({"kind":"guided","id":"s10","mins":8,"title":"Transfer — estimability in a two-group design",
 "objective":"Decide estimability and estimate an estimable contrast.",
 "problem":"Four observations: group 1 has y = 3, 5 and group 2 has y = 8, 10. The model is y = α + τ₁ (group 1) or α + τ₂ (group 2) + u. Which of τ₁ − τ₂, α + τ₁, τ₁, α are estimable, and what is the estimate of τ₁ − τ₂?",
 "hints":["Direction: write each function as a vector over (α, τ₁, τ₂) and list the distinct rows of X.",
          "Method: ℓ′β is estimable when ℓ′ is a weighted sum of the rows (1,1,0) and (1,0,1).",
          "Next step: for an estimable contrast, use the group means."],
 "answer":"τ₁ − τ₂ and α + τ₁ are estimable; τ₁ and α alone are not. The estimate of τ₁ − τ₂ is 4 − 9 = −5.",
 "check":"The estimate −5 is the same for every solution of the normal equations; τ̂₁ alone is not.",
 "solution":[
  {"say":"The row types.","math":"rows of X: (1,1,0) twice, (1,0,1) twice;  rank 2, 3 parameters","why":"Only two directions."},
  {"say":"Test each function.","math":"τ₁ − τ₂ = (0,1,−1) = (1,1,0) − (1,0,1)   estimable\nα + τ₁ = (1,1,0)   estimable\nτ₁ = (0,1,0)   not a combination\nα = (1,0,0)   not a combination","why":"Estimable means in the row space."},
  {"say":"Estimate.","math":"ȳ₁ = (3+5)/2 = 4,   ȳ₂ = (8+10)/2 = 9\nτ̂₁ − τ̂₂ = 4 − 9 = −5","why":"Two different generalised-inverse solutions gave −5 each, while their τ̂₁ values differed."}]})

S.append({"kind":"theory","id":"s11","mins":6,"title":"Where this sits in the syllabus",
 "objective":"Place Gauss–Markov against the topics that extend or test it.",
 "blocks":[
  {"t":"step","h":"What this topic builds on","body":"Topic 6.1 supplies H and M, and HM = 0 is used in the proof. The generalised inverse behind estimability in a rank-deficient design belongs to topic 2.8."},
  {"t":"step","h":"What extends it","body":"Topic 6.7 replaces Var(u) = σ²I by a general covariance matrix and obtains the BLUE by generalised least squares. Topic 6.5 treats multicollinearity as a variance problem. Topic 6.6 treats correlated errors."},
  {"t":"step","h":"What it does not cover","body":"Restricted least squares is a separate estimator with its own properties and is not covered here. Nor is the choice between biased and unbiased estimators (ridge), which sits outside the Gauss–Markov class."}],
 "ask":{"q":"Which later topic gives the BLUE when Var(u) is not σ²I?","nudge":"It starts with the letter G."}})

S.append({"kind":"recall","id":"s12","mins":2,"title":"Second recall","objective":"Retrieve the parts that fade first.",
 "intro":"Answer, then reveal.",
 "items":[{"q":"In Q11, what are X′X and the two BLUE formulas?","a":"X′X = diag(6, 2); β̂₁ = (y₁ + 2y₂ + y₃)/6; β̂₂ = (y₁ − y₃)/2."},
          {"q":"Bias from omitting x₂?","a":"β₂δ, where δ is the slope of x₂ on x₁."},
          {"q":"Which statement is not a consequence of near multicollinearity?","a":"That the estimates are biased."},
          {"q":"When is ℓ′β estimable?","a":"When ℓ′ is in the row space of X."},
          {"q":"What does heteroscedasticity do to OLS?","a":"It stays unbiased, but it is not BLUE."}]})

S.append({"kind":"summary","id":"s13","mins":3,"title":"What you should now be able to do","objective":"Check the lesson against its objectives.",
 "body":["State the Gauss–Markov assumptions and conclusion, and say normality is not needed.",
         "Test any candidate estimator for unbiasedness with c′X = ℓ′, and compute its variance as σ²c′c.",
         "Solve a small three-equation model: X′X, X′y, the BLUE and its covariance matrix.",
         "Decide which linear functions are estimable in a rank-deficient design.",
         "Classify omission, heteroscedasticity and multicollinearity by what they break: bias, BLUE, or variance."]})

S.append({"kind":"theory","id":"s14","mins":8,"ext":True,"title":"Extension — the proof with Q11's numbers",
 "objective":"See the variance split a′a + d′d numerically.",
 "blocks":[
  {"t":"step","h":"The null direction","body":"For Q11, X′ is 2×3, so its null space is one-dimensional. The vector z = (1, −1, 1)/√3 satisfies X′z = 0: its first entry gives (1 − 2 + 1)/√3 = 0 and its second gives (1 − 1)/√3 = 0."},
  {"t":"step","h":"All competitors for β₁","body":"Any linear unbiased estimator of β₁ has weights c = (1,2,1)/6 + tz. Its variance is σ²c′c = σ²(1/6 + t²), because the OLS weights are orthogonal to z."},
  {"t":"step","h":"Read off","body":"At t = 0 the variance is σ²/6, the smallest. At t = 1 it is 7σ²/6, at t = 2 it is 25σ²/6. Every competitor is OLS plus a term that adds variance and nothing else."}],
 "ask":{"q":"Why is the cross term 2a′d zero?","nudge":"d is built to satisfy d′X = 0."}})

S.append({"kind":"quiz","id":"s15","mins":12,"title":"Mastery test",
 "objective":"Demonstrate it independently, on questions you have not seen.","setId":"regression_t2_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id":"regressiont2", "topicId":"regression-t2", "moduleId":"regression",
 "title":"Gauss–Markov, BLUE and Estimability",
 "breadcrumb":"Regression → Properties of least squares → Gauss–Markov, BLUE, estimability",
 "engine":"B", "engineName":"Test unbiasedness first with c′X = ℓ′, then compare variances; the best unbiased linear rule is least squares",
 "version":"1.0", "status":"approved",
 "estMin":sum(s["mins"] for s in CORE),
 "objectives":["State the Gauss–Markov theorem and the assumptions it needs, and say which it does not.",
               "Test a candidate estimator for unbiasedness with c′X = ℓ′ and compute its variance as σ²c′c.",
               "Find the BLUE and its covariance matrix in a small system such as Q11.",
               "Decide which linear parametric functions are estimable when X is rank-deficient.",
               "Classify omitted variables, heteroscedasticity and multicollinearity by what each breaks."],
 "prereq":[{"id":"p1","name":"Variance of a weighted sum","why":"Var(a′y) = σ²a′a is how every competitor is compared."},
           {"id":"p2","name":"The unbiasedness condition a′X = ℓ′","why":"It is the first test applied to every option."},
           {"id":"p3","name":"Rank and row space","why":"Estimability is membership of the row space."},
           {"id":"p4","name":"OLS and its covariance matrix","why":"The benchmark is σ²(X′X)⁻¹."}],
 "traps":["Swapping the divisors 6 and 2 in Q11 (the answer was 'right working, wrong quantity').",
          "Claiming near multicollinearity biases OLS.",
          "Requiring normality for BLUE.",
          "Treating an unbiased rule as best: (y₁ + y₂)/3 is unbiased and worse.",
          "Calling every parameter estimable in a rank-deficient design."],
 "revision":{
   "sheet":["BLUE = linear + unbiased + least variance.",
            "Assumptions: E(u) = 0, Var(u) = σ²I, X fixed and full rank. No normality.",
            "Var(β̂) = σ²(X′X)⁻¹. Unbiasedness test: c′X = ℓ′.",
            "Proof: c = a + d with d′X = 0 and a′d = 0, so Var = σ²(a′a + d′d).",
            "Q11: X′X = diag(6, 2); β̂₁ = (y₁ + 2y₂ + y₃)/6; β̂₂ = (y₁ − y₃)/2; variances σ²/6, σ²/2; covariance 0.",
            "Wrong Q11 options give expectations 3β₁, 24β₁, β₂/3: all biased.",
            "Estimable: ℓ′ in the row space of X. Two-group design: τ₁ − τ₂ and α + τ₁ yes; τ₁, α alone no.",
            "Omitted variable: E(b₁*) = β₁ + β₂δ. 2 × 0.6 = 1.2 bias.",
            "Heteroscedasticity: unbiased, not BLUE. Multicollinearity: unbiased, BLUE, variance × 1/(1 − r²) = 50.25 at r = 0.99."],
   "cards":[["BLUE","Least variance among linear unbiased estimators"],["Unbiasedness test","c′X = ℓ′"],["Var(β̂)","σ²(X′X)⁻¹"],["Q38 answer","Estimates are biased: NOT a consequence"],["Estimable","ℓ′ in row space of X"],["Variance of c′y","σ²c′c"]],
   "tricks":["Multiply the weights into X: the target must come back.","Diagonal X′X means uncorrelated estimators.","Near collinearity hurts the variance, never the mean."],
   "shortcuts":["Q11 divisors are 6 then 2: the diagonal of X′X.","VIF = 1/(1 − r²): 50.25 at 0.99.","(y₁ + 2y₂)/5 has variance σ²/5."],
   "remember":["Gauss–Markov needs the first two moments only.","A wrong divisor shows up at once as a biased estimator."]},
 "howto":"If short of time the lesson is scenes 4 (theorem), 5 (Q11 worked) and 8 (omission, heteroscedasticity, multicollinearity). It deliberately does not cover GLS (6.7), the full treatment of multicollinearity (6.5), or restricted least squares.",
 "refs":[{"title":"Econometrics","where":"Chapter 4, Least Squares Regression (Gauss–Markov)","site":"Bruce Hansen","url":"","type":"Free online textbook","free":True,"checked":"2026-11-06","why":"The Gauss–Markov theorem and its proof, scene 3."},
         {"title":"Econometric Analysis","where":"Chapter 4, Section 4.3","site":"William Greene","url":"","type":"Textbook","free":False,"checked":"2026-11-06","why":"Properties of least squares and omitted-variable bias, scenes 3 and 7."},
         {"title":"Linear Regression Analysis","where":"Chapter 3, Estimable functions","site":"Seber and Lee","url":"","type":"Textbook","free":False,"checked":"2026-11-06","why":"Estimability in the less-than-full-rank model, scene 7."}],
 "mastery":{"minQ":10,"pass":80,"draw":10,"fmtMin":{"numeric":70,"multi":70},
            "diffMix":{"easy":3,"moderate":5,"hard":2},"noHints":True,"retestDays":7,
            "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on "
                   "numerical and multi-statement items, answered without hints. Each paper is "
                   "drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style "
                   "paper; NTA publishes no official difficulty split."},
 "provenance":"Anchor Q11 (key B, marked D, wrong): answered wrongly through swapped divisors; the key was re-derived. The Q38 variants (bias, heteroscedasticity, multicollinearity) are placed here because they ask which OLS properties survive; Q38 itself (multicollinearity, key C, marked B) is anchored to topic 6.5 and used here only for the 'not biased' boundary. Verified by computing in verify_regression_t1_t4.py: X′X = diag(6, 2); weights (1,2,1)/6 and (1,0,−1)/2; variances σ²/6 and σ²/2; covariance 0; every Q11 option's expectation (3β₁ and β₂/3; 3β₁ and β₁/3; 24β₁; the key unbiased); the null vector of X′ and the variance 1/6 + t²; the two-reading model (variance 0.2 against 2/9 and 0.25); estimability by rank in the two-group design, and −5 identical across two solutions. By simulation: heteroscedastic OLS mean slope 0.5017 against 0.5 with variance 1.2399 against the sandwich 1.24 (100,000 draws); near-collinear estimates 1.008 and 0.993 for true 1, 1 (20,000 draws); omitted-variable mean 2.2008 against 2.2 (40,000 draws). The variance-inflation factor at r = 0.99 is 50.25. Bank defects: variant j26v-q11-06's explanation field holds the text of an unrelated Q12; variant stems are otherwise usable.",
 "scenes":S}

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id":"regression-t2-m-%02d"%i, "format":fmt, "topic":"regression-t2",
         "diff":diff, "stem":stem, "options":opts, "answer":ans, "explanation":exp}
    d.update(kw); return d

def verd(a,b,c,dd):
    return {"A":{"tf":a[0],"why":a[1]},"B":{"tf":b[0],"why":b[1]},
            "C":{"tf":c[0],"why":c[1]},"D":{"tf":dd[0],"why":dd[1]}}

I = []
I.append(q(1,"single","easy","In y = Xβ + u, the OLS estimator is BLUE when E(u) = 0 and V(u) = σ²I. Beyond these two moment conditions, the theorem needs:",
  ["no distributional assumption","normality of u","a large sample size","a random design matrix"],"A",
  "Gauss–Markov uses only the mean and variance of u, with X fixed. Normality is needed for exact t and F tests, not for BLUE. A large sample is not required, and a random X changes the setting."))
I.append(q(2,"single","easy","The variance–covariance matrix of the OLS estimator β̂ is:",
  ["σ²(X′X)⁻¹","σ²X′X","(X′X)⁻¹","σ²I"],"A",
  "Var(β̂) = (X′X)⁻¹X′(σ²I)X(X′X)⁻¹ = σ²(X′X)⁻¹. Dropping σ² gives (X′X)⁻¹, and σ²X′X has the wrong inverse structure."))
I.append(q(3,"numeric","easy","For y₁ = β + u₁ and y₂ = 2β + u₂ with V(uᵢ) = σ² = 10, the variance of the BLUE of β is:",
  ["2","2.5","5","10"],"A",
  "The BLUE is (y₁ + 2y₂)/5 with variance σ²/5 = 10/5 = 2. The value 2.5 is the variance of y₂/2 and 10 is the variance of y₁ alone.",
  check="The BLUE variance must be below both single-reading variances: below 10 for y₁ and below 2.5 for y₂/2."))
I.append(q(4,"single","easy","If X′X is a diagonal matrix, the least squares estimators of the parameters are:",
  ["uncorrelated","biased","not unique","identical"],"A",
  "Cov(β̂) = σ²(X′X)⁻¹, and the inverse of a diagonal matrix is diagonal, so the off-diagonal covariances are zero. Diagonal X′X implies full rank, hence uniqueness, and says nothing about bias."))
I.append(q(5,"single","easy","A linear parametric function ℓ′β is estimable if and only if:",
  ["ℓ′ lies in the row space of X","X is a square matrix","ℓ′ℓ = 1","ℓ is any vector"],"A",
  "Estimable means some c′y is unbiased, c′X = ℓ′, so ℓ′ is a combination of the rows of X. In a full-rank X every ℓ qualifies, but the condition itself is membership of the row space."))
I.append(q(6,"single","easy","Which of the following is NOT a consequence of near (not perfect) multicollinearity for OLS?",
  ["The estimates are biased","Small changes in the data cause large changes in the estimates","Standard errors are large while R² is high","The estimates can be large in magnitude"],"A",
  "Near multicollinearity breaks no Gauss–Markov assumption, so OLS stays unbiased and BLUE. What suffers is the variance, which is inflated by 1/(1 − r²). The other three are all symptoms of that inflation."))
I.append(q(7,"numeric","moderate","In the model y₁ = β₁ + β₂ + u₁, y₂ = 2β₁ + u₂, y₃ = β₁ − β₂ + u₃, the observations are y = (7, 4, 3). The BLUE of β₁ is:",
  ["3","9","84","2"],"A",
  "β̂₁ = (y₁ + 2y₂ + y₃)/6 = (7 + 8 + 3)/6 = 3. With the divisor 2 the value would be 9, 84 is 6(y₁ + y₂ + y₃), and 2 is β̂₂ = (7 − 3)/2.",
  check="Multiply the weights (1, 2, 1)/6 into the first column of X: (1 + 4 + 1)/6 = 1, and into the second: (1 + 0 − 1)/6 = 0."))
I.append(q(8,"single","moderate","Under heteroscedastic errors, the OLS estimator of β is:",
  ["unbiased but not BLUE","biased","BLUE","inconsistent"],"A",
  "Unbiasedness uses E(u) = 0 only, so it survives. The variance formula σ²(X′X)⁻¹ no longer holds and generalised least squares has smaller variance."))
I.append(q(9,"single","moderate","Which of the following DOES cause bias in the OLS estimator of a coefficient?",
  ["Omission of a relevant variable correlated with the regressor","A large sample","Multicollinearity among the regressors","Heteroscedastic errors"],"A",
  "Omitting a relevant correlated variable puts part of its effect into the error and breaks E(u) = 0 for the fitted model. The bias is β₂δ. Large samples, multicollinearity and heteroscedasticity leave OLS unbiased."))
I.append(q(10,"numeric","moderate","The true model has β₂ = 2 on x₂, and the regression of x₂ on x₁ has slope δ = 0.6. Leaving x₂ out, the bias in the slope on x₁ is:",
  ["1.2","2.0","0.6","2.6"],"A",
  "Bias = β₂δ = 2 × 0.6 = 1.2. The value 2.6 is β₂ + δ and 2.0 and 0.6 are the two factors taken alone.",
  check="The bias is a product of a coefficient and a slope less than 1 in size, so it cannot exceed β₂ = 2."))
I.append(q(11,"multi","moderate","Near (but not perfect) multicollinearity among the regressors of a linear model.",
  ["A, B and C only","A and B only","B, C and D only","A, B, C and D"],"A",
  "Unbiasedness and BLUE survive, standard errors grow, and a high R² with insignificant t values is the classic symptom. The estimates are not biased.",
  statements=["OLS estimators remain unbiased","The variances of the estimators are inflated","R² can be high while individual t statistics are insignificant","The OLS estimators become biased"],
  verdicts=verd((True,"E(u) = 0 and fixed X are unaffected."),
                (True,"The variance is multiplied by 1/(1 − r²)."),
                (True,"The F test pools the coefficients, while each t statistic suffers from its own inflated standard error."),
                (False,"No assumption needed for unbiasedness is violated."))))
I.append(q(12,"single","moderate","In a design with an intercept and two group effects (parameters α, τ₁, τ₂) and observations in both groups, which function is estimable?",
  ["τ₁ − τ₂","τ₁","α","τ₁ + τ₂"],"A",
  "(0, 1, −1) is the difference of the two row types (1,1,0) and (1,0,1), so it is in the row space. The other three are not combinations of those two rows."))
I.append(q(13,"numeric","moderate","In Q11's model with σ² = 12, the variance of the BLUE of β₁ is:",
  ["2","6","4","1"],"A",
  "Var(β̂₁) = σ²/6 = 12/6 = 2, using the squared weights (1 + 4 + 1)/36 = 1/6. The value 6 is the divisor, not the variance.",
  check="The sum of the squared weights is 6/36 = 1/6, so the variance is σ² times a number below 1: it must be below 12."))
I.append(q(14,"single","moderate","In y₁ = β + u₁, y₂ = 2β + u₂ with equal variances, the estimator (y₁ + y₂)/3 is:",
  ["unbiased but has larger variance than the BLUE","biased","the BLUE","unbiased with smaller variance than the BLUE"],"A",
  "E = (β + 2β)/3 = β, so it is unbiased. Its variance is 2σ²/9 ≈ 0.222σ², above the BLUE's σ²/5 = 0.2σ². No unbiased linear estimator can beat the BLUE."))
I.append(q(15,"multi","moderate","In the two-group design with parameters (α, τ₁, τ₂), each group having observations, the following functions.",
  ["A and B only","A, B and C only","C and D only","A, B, C and D"],"A",
  "The estimable ones are the contrast τ₁ − τ₂ and the group mean α + τ₁. The parameters α and τ₁ taken alone are not.",
  statements=["τ₁ − τ₂ is estimable","α + τ₁ is estimable","τ₁ alone is estimable","α alone is estimable"],
  verdicts=verd((True,"It is a difference of two row types."),
                (True,"It is the row (1,1,0) itself."),
                (False,"(0,1,0) is not a combination of (1,1,0) and (1,0,1)."),
                (False,"(1,0,0) is not a combination of those two rows."))))
I.append(q(16,"single","moderate","In the three-equation model of Q11, the covariance between the BLUEs of β₁ and β₂ is:",
  ["zero, because X′X is diagonal","σ²/6","−σ²/2","σ²/3"],"A",
  "X′X = diag(6, 2), so (X′X)⁻¹ = diag(1/6, 1/2) and the off-diagonal entry is zero. The values σ²/6 and σ²/2 are the two variances."))
I.append(q(17,"numeric","hard","Two regressors are correlated with r = 0.99. The variance inflation factor 1/(1 − r²) is:",
  ["50.25","7.09","100","0.0199"],"A",
  "1 − 0.9801 = 0.0199, and 1/0.0199 = 50.25. The value 7.09 is the square root, which inflates the standard deviation. The value 100 is 1/(1 − r) and 0.0199 is the denominator.",
  check="For r near 1, 1/(1 − r²) ≈ 1/(2(1 − r)) = 1/0.02 = 50, so the answer is close to 50."))
I.append(q(18,"numeric","hard","In the two-group design with group 1 responses 3, 5 and group 2 responses 8, 10, the estimate of the estimable contrast τ₁ − τ₂ is:",
  ["−5","5","13","4"],"A",
  "The estimable contrast equals the difference of group means: 4 − 9 = −5. It is the same for every solution of the normal equations, unlike τ̂₁ alone.",
  check="A contrast of two group effects equals the difference of group means, and group 1 has the smaller mean, so the sign is negative."))
I.append(q(19,"single","hard","In the proof of Gauss–Markov, a competing linear unbiased estimator is written c = a + d, where a are the OLS weights. Its variance exceeds that of OLS by σ²d′d because:",
  ["d′X = 0 makes a′d = 0, so the cross term vanishes","d is a constant vector","d′d is always zero","a and d have equal length"],"A",
  "Unbiasedness of both c and a gives d′X = 0. Then a′d = ℓ′(X′X)⁻¹X′d = 0, so Var(c′y) = σ²(a′a + d′d). The term d′d is positive unless d = 0."))
I.append(q(20,"single","hard","If the errors are in addition normally distributed, OLS is best among:",
  ["all unbiased estimators, linear or not","linear unbiased estimators only","all estimators, biased or not","only estimators with equal weights"],"A",
  "Under normality β̂ is a function of a complete sufficient statistic and unbiased, hence the minimum-variance unbiased estimator in the whole class. It still does not beat biased estimators on mean squared error everywhere."))

LET = "ABCD"
_r = random.Random(20260611); PAT = list("ABCD" * 5); _r.shuffle(PAT)
WANT = {"regression-t2-m-%02d" % (i + 1): PAT[i] for i in range(20)}

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

POOLD = {"moduleId":"regression","topicId":"regression-t2","source":"mastery",
         "label":"Gauss–Markov, BLUE and estimability — mastery test (unseen)","count":len(I),"items":I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT,"w",encoding="utf-8") as f:  json.dump(LES,f,ensure_ascii=False,indent=1)
with io.open(POOL,"w",encoding="utf-8") as f: json.dump(POOLD,f,ensure_ascii=False,indent=1)
print("wrote %s: %d scenes (%d core), estMin %d"%(OUT,len(S),len(CORE),LES["estMin"]))
print("wrote %s: %d items"%(POOL,len(I)))
