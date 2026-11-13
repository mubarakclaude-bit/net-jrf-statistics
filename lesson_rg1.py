#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regression-t1 (topic 6.1): hat matrix, residual maker, quadratic forms.
Every figure below is computed in verify_regression_t1_t4.py; nothing is recalled."""
import json, io, os, re

OUT  = "seed/lesson_rg1.json"
POOL = "seed/regression_t1_mastery.json"

S = []

S.append({"kind":"foundation","id":"s0","mins":7,"title":"Before the lesson — four things it will assume",
 "objective":"Check the four pieces of matrix algebra and distribution theory this topic is built on.",
 "ask":{"q":"If a matrix P satisfies PP = P, what can you say about the vector Py, applied twice?","nudge":"Apply P to Py and use the rule."},
 "body":["Least squares has a picture behind it. The data vector y sits in n-dimensional space. The columns of the design matrix X span a flat sheet inside that space, the column space of X. Fitting the model means finding the point on that sheet nearest to y. The fitted vector is that nearest point, and the residual is the straight line joining y to it.",
         "Two matrices do all the work. The hat matrix H turns y into the nearest point. The residual maker M turns y into the leftover. Every result in this topic, from the degrees of freedom of a variance estimate to the distribution of the residual sum of squares, comes from what H and M are as matrices: symmetric, idempotent, with a known trace.",
         "The earlier marks lost in this part of the paper were lost on the count n − k, not on the idea. This lesson therefore verifies each count by a trace, and shows every count on a small case you can check by hand."],
 "items":[
  {"ask":"What does it mean for a matrix to be idempotent, and what is the trace of a matrix?",
   "recall":"Idempotent: A·A = A. The trace is the sum of the diagonal entries.",
   "refresh":["A matrix A is idempotent when multiplying it by itself changes nothing: AA = A. A projection behaves like this, because projecting a point that is already on the sheet leaves it where it is. The identity matrix and the zero matrix are the two trivial examples.",
              "The trace of a square matrix is the sum of its diagonal entries. For [[2, 1], [0, 3]] it is 2 + 3 = 5. The trace has one property used all through this topic: tr(AB) = tr(BA) whenever both products exist, even if AB and BA are different sizes."]},
  {"ask":"Write the normal equations and the OLS estimator for y = Xβ + u.",
   "recall":"X′Xβ̂ = X′y, so β̂ = (X′X)⁻¹X′y when X′X is invertible.",
   "refresh":["Least squares chooses β to make the sum of squared errors (y − Xβ)′(y − Xβ) as small as possible. Setting its derivative with respect to β to zero gives −2X′(y − Xβ) = 0, which rearranges to X′Xβ = X′y. These are the normal equations.",
              "If X has full column rank, X′X is invertible and β̂ = (X′X)⁻¹X′y. Check the sizes: X′ is k×n, y is n×1, so X′y is k×1, and (X′X)⁻¹ is k×k. The product is a k×1 vector, one number per coefficient."]},
  {"ask":"If z = Ay and Var(y) = σ²I, what is Var(z)?",
   "recall":"Var(z) = A·Var(y)·A′ = σ²AA′.",
   "refresh":["For a fixed matrix A and a random vector y, the covariance matrix of Ay is A·Var(y)·A′. The matrix A multiplies on the left and its transpose on the right, so the dimensions agree.",
              "When Var(y) = σ²I the middle factor is a scalar times the identity and it slides out: Var(Ay) = σ²AA′. If A is also symmetric and idempotent, AA′ = AA = A, so Var(Ay) = σ²A. That single line is where Var(ŷ) = σ²H and Var(e) = σ²M come from."]},
  {"ask":"What distribution does a sum of squares of independent standard normals have, and with how many degrees of freedom?",
   "recall":"Chi-square, with degrees of freedom equal to the number of independent squares.",
   "refresh":["If z₁, …, z_m are independent N(0, 1), then z₁² + … + z_m² follows a chi-square distribution with m degrees of freedom. Its mean is m.",
              "The number to track is m, the count of independent squares. A residual sum of squares has n terms but they are not independent: the residuals obey k linear constraints. Counting those constraints correctly is what gives n − k, and it is the same count the trace of M will give."]}]})

S.append({"kind":"intuition","id":"s1","mins":7,"title":"Fitting is projecting",
 "objective":"Describe ŷ as the nearest point to y on the column space of X, and e as the perpendicular leftover.",
 "body":["Take the simplest case: five people, one explanatory variable. The column space of X is a two-dimensional sheet inside five-dimensional space, spanned by a column of ones and the column of x-values. The vector y has five coordinates. Dropping a perpendicular from y to that sheet gives the fitted vector ŷ. The perpendicular itself is the residual vector e.",
         "Perpendicular is the whole story. Because e meets the sheet at a right angle, it is orthogonal to every column of X: X′e = 0. Because ŷ lies on the sheet and e does not, ŷ′e = 0 as well. And by Pythagoras on that right-angled triangle, y′y = ŷ′ŷ + e′e. The total splits into a fitted part and a residual part, with nothing left over.",
         "Now name the two machines. H, the hat matrix, takes any y to its shadow on the sheet: ŷ = Hy. It is called the hat matrix because it puts the hat on y. M = I − H takes y to what is left: e = My. Applying H to something already on the sheet changes nothing, which is why H·H = H."],
 "scenario":{"teaser":"Five practice-test results, and which one the fitted line follows most closely.",
  "title":"Hours of practice against test score",
  "body":["A tutor records hours of practice x = 1, 2, 3, 4, 5 for five students and their test scores y = 2, 4, 5, 4, 5. She fits a straight line by least squares and gets ŷ = 2.2 + 0.6x, so the fitted scores are 2.8, 3.4, 4.0, 4.6 and 5.2.",
          "The residuals are y − ŷ = −0.8, 0.6, 1.0, −0.6 and −0.2. They sum to zero, because the model has an intercept and the column of ones is one of the columns of X. The sum of their squares is 0.64 + 0.36 + 1.00 + 0.36 + 0.04 = 2.40.",
          "She then asks a different question. If one student's score were raised by one point, how much of that change would the fitted line absorb for that student, and how much would it spread to the others? The hat matrix answers it. Its diagonal entry h_ii is the share of a change in y_i that comes back as a change in ŷ_i."],
  "q":"For the students at 1 hour and at 3 hours of practice, which fitted value moves more when that student's own score moves by 1?",
  "answer":"The student at 1 hour. The diagonal entry is h = 1/5 + (x − 3)²/10, which is 0.6 at x = 1 and 0.2 at x = 3. A point far from the mean of x pulls the line toward itself; a point near the mean barely moves it."},
 "ask":{"q":"Why is the residual vector perpendicular to every column of X?","nudge":"Least squares picks the nearest point on the sheet. What does nearest imply about the direction of the join?"}})

S.append({"kind":"explore","id":"s2","mins":7,"title":"The count n − k, seen as a distribution",
 "objective":"See that e′e/σ² is a chi-square with n − k degrees of freedom and read its critical value.",
 "viz":{"type":"chisq-tail","caption":"Set the degrees of freedom to 3 for the five-point example: n − k = 5 − 2. Notice how the critical value moves as the count changes."},
 "body":["The chi-square picture is the one used in the next theorem: the scaled residual sum of squares e′e/σ² is chi-square with n − k degrees of freedom. Slide the degrees of freedom to 3, the count for the five-student example, and read the 5% critical value, 7.815.",
         "Now slide it to 5, which is what you get if you wrongly use n. The critical value rises to 11.07. A test or interval built on the wrong count would be too lenient, because it expects a larger sum of squares than the data can produce.",
         "Move the observed statistic past the critical value and watch the p-value fall below the size α. Nothing in the picture depends on the regression itself: the entire regression content is the choice of the degrees of freedom."],
 "ask":{"q":"If a regression has 20 observations and 4 coefficients, which degrees of freedom do you set the slider to?","nudge":"Subtract the number of coefficients, not the number of slopes."}})

S.append({"kind":"theory","id":"s3","mins":9,"title":"H and M: definitions and the four properties",
 "objective":"State H and M, and the properties that every later result uses.",
 "blocks":[
  {"t":"formula","h":"The two matrices","body":"H = X(X′X)⁻¹X′          (n × n)\nM = I − H\nŷ = Hy,    e = My = y − ŷ"},
  {"t":"formula","h":"Four properties","body":"1. Symmetric:   H′ = H,   M′ = M\n2. Idempotent:  HH = H,   MM = M\n3. Annihilation: HX = X,   MX = 0,   HM = 0\n4. Trace:  tr(H) = k,   tr(M) = n − k"},
  {"t":"def","h":"Idempotent","body":"A square matrix A with AA = A. Applying it twice is the same as applying it once. A projection has this property because the projected point is already on the target sheet."},
  {"t":"step","h":"Why trace equals rank","body":"An idempotent matrix has eigenvalues that are only 0 or 1. If A has eigenvalue λ with eigenvector v, then Av = λv and AAv = λ²v. But AA = A, so λ² = λ, which forces λ = 0 or 1. The trace is the sum of the eigenvalues, so it counts the eigenvalues equal to 1, which is the rank. For H the rank is the dimension of the column space of X, which is k when X has full column rank."},
  {"t":"step","h":"Why the trace of H is k, directly","body":"tr(H) = tr(X(X′X)⁻¹X′). Move X′ round to the front, which the cyclic rule allows: tr(X′X(X′X)⁻¹) = tr(I_k) = k. The second line is a k×k identity, so its trace is k. Then tr(M) = tr(I_n) − tr(H) = n − k."}],
 "table":{"caption":"What each matrix does","head":["Matrix","Sends y to","Lives in","Rank","Trace"],
  "rows":[["H","fitted vector ŷ","column space of X","k","k"],["M = I − H","residual vector e","the perpendicular space","n − k","n − k"]]},
 "flow":{"title":"From y to the variance estimate","alt":"A top-to-bottom flow. y splits through H into the fitted vector and through M into the residual vector. The residual vector feeds the quadratic form e prime e, which is divided by n minus k to give the variance estimate.",
  "nodes":[{"id":"a","r":0,"c":1,"label":"Data vector y","kind":"start"},
           {"id":"b","r":1,"c":0,"label":"ŷ = Hy  (rank k)","kind":"step"},
           {"id":"c","r":1,"c":2,"label":"e = My  (rank n − k)","kind":"step"},
           {"id":"d","r":2,"c":2,"label":"e′e = y′My, a quadratic form","kind":"step"},
           {"id":"e","r":3,"c":2,"label":"s² = e′e/(n − k)","kind":"end"}],
  "edges":[{"from":"a","to":"b"},{"from":"a","to":"c"},{"from":"c","to":"d"},{"from":"d","to":"e"}],
  "note":"The divisor n − k is the trace of M. It is the rank of the space the residuals live in."},
 "ask":{"q":"Which property says the fitted vector and the residual vector carry no information about each other?","nudge":"It is a product of H and M."}})

S.append({"kind":"worked","id":"s4","mins":8,"title":"Every number for the five-student data",
 "objective":"Build H from X, read off the leverages and confirm the trace is 2.",
 "ask":{"q":"Which entries of H are largest, and where do they sit?","nudge":"Look at the diagonal and at which x-values are far from the mean."},
 "problem":"x = 1, 2, 3, 4, 5 and y = 2, 4, 5, 4, 5, with a model that has an intercept. Find β̂, the hat-matrix diagonal, the trace, e′e and s².",
 "steps":[
  {"say":"Form X′X and X′y.","math":"X′X = [[5, 15], [15, 55]]\nX′y = (Σy, Σxy) = (20, 66)","why":"The first column of X is ones, so X′X has n = 5 and Σx = 15 in its top row, and Σx² = 55 in the corner. For X′y, Σy = 2+4+5+4+5 = 20 and Σxy = 2+8+15+16+25 = 66."},
  {"say":"Invert X′X.","math":"det = 5·55 − 15·15 = 275 − 225 = 50\n(X′X)⁻¹ = (1/50)·[[55, −15], [−15, 5]]","why":"For a 2×2 matrix swap the diagonal, negate the off-diagonal, and divide by the determinant. Check: the product with X′X must be the identity; the top-left entry is (55·5 − 15·15)/50 = 1."},
  {"say":"Solve for β̂.","math":"β̂ = (1/50)·(55·20 − 15·66, −15·20 + 5·66)\n   = (1/50)·(110, 30) = (2.2, 0.6)","why":"This matches ŷ = 2.2 + 0.6x. Check the residuals later: they must sum to zero."},
  {"say":"Read the diagonal of H.","math":"h_ii = 1/5 + (x_i − 3)²/10\n    = 0.6, 0.3, 0.2, 0.3, 0.6","why":"For a straight-line model the diagonal has this closed form, with x̄ = 3 and Sxx = Σ(x − 3)² = 10. The entries are symmetric about the mean and largest at the ends."},
  {"say":"Check the trace.","math":"tr(H) = 0.6 + 0.3 + 0.2 + 0.3 + 0.6 = 2 = k","why":"The trace must equal the number of coefficients. If your diagonal does not add to 2 an entry is wrong. This is the quickest check available."},
  {"say":"Residuals and s².","math":"e = (−0.8, 0.6, 1.0, −0.6, −0.2)\ne′e = 0.64 + 0.36 + 1.00 + 0.36 + 0.04 = 2.4\ns² = 2.4/(5 − 2) = 0.8","why":"Divide by n − k = tr(M) = 3, not by 5. The residuals sum to zero, as the intercept requires."},
  {"say":"Estimated variance of one residual.","math":"Var(e₁) is estimated by s²(1 − h₁₁) = 0.8 × 0.4 = 0.32","why":"Var(e) = σ²M, whose diagonal is σ²(1 − h_ii). Residuals at high-leverage points have smaller variance, because the line is pulled toward them."}],
 "after":"The habit to keep: whenever a count of degrees of freedom appears, write it as a trace and add the diagonal before you trust it."})

S.append({"kind":"recall","id":"s5","mins":2,"title":"Pause and recall","objective":"Retrieve the properties before using them.",
 "intro":"Answer each before revealing it.",
 "items":[{"q":"State H and M in terms of X.","a":"H = X(X′X)⁻¹X′ and M = I − H."},
          {"q":"What is tr(H), and tr(M)?","a":"k and n − k, when X has full column rank."},
          {"q":"What does HX equal, and MX?","a":"HX = X, and MX = 0."},
          {"q":"Why is e′e not divided by n?","a":"The residuals live in a space of dimension n − k, so dividing by n gives an estimate that is too small."},
          {"q":"What is the largest a leverage h_ii can be?","a":"1. The leverages lie between 0 and 1 and add up to k."}]})

S.append({"kind":"completion","id":"s6","mins":8,"title":"Your turn — a three-point hat matrix",
 "objective":"Complete the construction of H for x = 0, 1, 2 and check its trace.",
 "problem":"A model with an intercept and slope is fitted to three points at x = 0, 1, 2. Build H and confirm tr(H) = 2.",
 "steps":[
  {"say":"X has a column of ones and the column (0, 1, 2). Form X′X.",
   "blank":{"prompt":"What is the determinant of X′X = [[3, 3], [3, 5]]?","answer":"6","accept":["6","six","3·5 − 3·3 = 6","15 − 9"],"hint":"Multiply the diagonal, subtract the product of the off-diagonal."},
   "why":"3·5 − 3·3 = 6. The inverse is (1/6)·[[5, −3], [−3, 3]]."},
  {"say":"Each entry of H is h_ij = (1/3) + (x_i − 1)(x_j − 1)/2, since x̄ = 1 and Sxx = 2. Compute the first diagonal entry.",
   "blank":{"prompt":"What is h₁₁?","answer":"5/6","accept":["5/6","0.8333","0.833","0.83"],"hint":"x₁ − 1 = −1, so the second term is (−1)(−1)/2."},
   "why":"1/3 + 1/2 = 5/6."},
  {"say":"The middle point sits at the mean of x.",
   "blank":{"prompt":"What is h₂₂?","answer":"1/3","accept":["1/3","0.3333","0.333","0.33"],"hint":"x₂ − 1 = 0, so the second term vanishes."},
   "why":"A point at x̄ has the smallest possible leverage, 1/n."},
  {"say":"By symmetry h₃₃ = h₁₁.",
   "blank":{"prompt":"What is tr(H)?","answer":"2","accept":["2","two","k","5/6+1/3+5/6"],"hint":"Add 5/6 + 1/3 + 5/6."},
   "why":"5/6 + 2/6 + 5/6 = 12/6 = 2 = k. The full matrix is H = (1/6)·[[5, 2, −1], [2, 2, 2], [−1, 2, 5]]."}],
 "after":"A three-point example is small enough to check by hand. The structure to carry away: H comes from X alone, never from y."})

S.append({"kind":"theory","id":"s7","mins":7,"title":"What H and M give you: variances and the chi-square",
 "objective":"Derive Var(ŷ), Var(e), Cov(ŷ, e) and the distribution of e′e.",
 "blocks":[
  {"t":"formula","h":"Variances","body":"Var(ŷ) = σ²H,    Var(e) = σ²M,    Cov(ŷ, e) = σ²HM = 0"},
  {"t":"step","h":"Why","body":"ŷ = Hy and Var(y) = σ²I, so Var(ŷ) = H(σ²I)H′ = σ²HH′ = σ²H, using symmetry and idempotence. The same line with M gives σ²M. For the covariance, Cov(Hy, My) = H(σ²I)M′ = σ²HM = 0 because HM = H(I − H) = H − HH = 0."},
  {"t":"step","h":"The residual sum of squares is a quadratic form","body":"e′e = (My)′(My) = y′M′My = y′My. A quadratic form is y′Ay for a symmetric matrix A. Because MX = 0, My = M(Xβ + u) = Mu, so e′e = u′Mu: the sum of squares depends on the errors only, never on β."},
  {"t":"step","h":"Its expectation","body":"E(u′Mu) = E(tr(u′Mu)) = E(tr(Muu′)) = tr(M·σ²I) = σ²tr(M) = σ²(n − k). Hence s² = e′e/(n − k) is unbiased for σ². The first equality holds because a scalar equals its own trace; the second uses tr(AB) = tr(BA)."},
  {"t":"step","h":"Its distribution","body":"If u ~ N(0, σ²I) and M is symmetric idempotent of rank n − k, then u′Mu/σ² follows a chi-square with n − k degrees of freedom. Rotate to the eigenvectors of M: n − k of them carry eigenvalue 1 and k carry 0, so the quadratic form is exactly a sum of n − k independent squared standard normals."},
  {"t":"def","h":"Leverage","body":"h_ii, the i-th diagonal entry of H. It satisfies 0 ≤ h_ii ≤ 1, and Σh_ii = k. A common flag for a high-leverage point is h_ii > 2k/n."}],
 "ask":{"q":"Why is the residual vector not distributed like the error vector?","nudge":"Compare Var(e) = σ²M with Var(u) = σ²I."}})

S.append({"kind":"guided","id":"s8","mins":8,"title":"On your own — counting from the trace",
 "objective":"Use traces to find the expected residual sum of squares.",
 "problem":"A regression with an intercept and three slopes is fitted to n = 20 observations with σ² = 3. Find tr(H), tr(M), E(e′e) and the expected value of e′e/n.",
 "hints":["Direction: count the coefficients first. An intercept and three slopes is how many columns of X?",
          "Method: tr(H) equals the number of columns and tr(M) = n − tr(H); then E(e′e) = σ²tr(M).",
          "Next step: multiply σ² by tr(M), then divide by n to see what the tempting estimator e′e/n targets."],
 "answer":"tr(H) = 4, tr(M) = 16, E(e′e) = 48 and E(e′e/n) = 2.4.",
 "check":"E(e′e) = 48 is below σ²n = 60, as it must be: fitting four coefficients absorbs four of the twenty squared errors.",
 "scenario":{"teaser":"An analyst reports the average squared residual as the error variance.",
  "title":"The shortcut that is always too small",
  "body":["An analyst fits a regression with an intercept and three slopes to 20 observations. She reports the mean squared residual, e′e/20, as her estimate of the error variance, because it matches the usual meaning of mean.",
          "A reviewer objects. The residuals are not twenty free numbers. They satisfy four linear constraints, X′e = 0, one for each column of X, so only sixteen of them can vary freely. A sum of squares that has lost four free directions is smaller than twenty independent squared errors would be.",
          "The trace makes the objection exact. E(e′e) = σ²tr(M) = 16σ², so e′e/20 has expectation 0.8σ². The analyst's estimate is too low by a fifth, on average, however the data come out."],
  "q":"By what factor is e′e/n biased as an estimate of σ² here, and what restores unbiasedness?",
  "answer":"Its expectation is (n − k)/n times σ², which is 16/20 = 0.8. Dividing by n − k = 16 instead of n restores unbiasedness."},
 "solution":[
  {"say":"Count the columns.","math":"k = 1 + 3 = 4","why":"One column of ones and three slope columns."},
  {"say":"Take the traces.","math":"tr(H) = k = 4\ntr(M) = n − k = 20 − 4 = 16","why":"These are fixed by the dimensions alone."},
  {"say":"Take the expectation.","math":"E(e′e) = σ²tr(M) = 3 × 16 = 48\nE(e′e/n) = 48/20 = 2.4","why":"2.4 is less than σ² = 3, which is the bias showing."}]})

S.append({"kind":"trapcheck","id":"s9","mins":6,"title":"Six statements","objective":"Separate true properties of H and M from tempting false ones.",
 "intro":"Decide true or false on all six before revealing any.",
 "items":[
  {"claim":"The trace of M equals the number of observations n.","tf":False,"why":"tr(M) = n − k. It is tr(I) = n minus tr(H) = k."},
  {"claim":"The residuals e = My have covariance matrix σ²I, so they are uncorrelated with equal variance.","tf":False,"why":"Var(e) = σ²M. The off-diagonal entries of M are not zero and the diagonal entries 1 − h_ii differ across observations."},
  {"claim":"The fitted vector and the residual vector are uncorrelated.","tf":True,"why":"Cov(ŷ, e) = σ²HM = 0. They are also orthogonal as vectors, ŷ′e = 0, in every sample."},
  {"claim":"If an idempotent matrix is not symmetric it can still be used as an orthogonal projection.","tf":False,"why":"An idempotent matrix such as [[1, 1], [0, 0]] projects obliquely. Orthogonal projection needs symmetry as well."},
  {"claim":"For a model with an intercept the residuals always sum to zero.","tf":True,"why":"The column of ones is a column of X and X′e = 0, so 1′e = Σe_i = 0. Without an intercept this can fail."},
  {"claim":"With X having 3 columns but rank 2, tr(H) = 3.","tf":False,"why":"The trace of an idempotent matrix is its rank, which is the rank of X, here 2. Counting columns instead of rank gives the wrong degrees of freedom."}]})

S.append({"kind":"guided","id":"s10","mins":8,"title":"Transfer — fit, residuals and s² from a given H",
 "objective":"Apply H to a new y without refitting a line.",
 "problem":"With x = 0, 1, 2 the hat matrix is H = (1/6)·[[5, 2, −1], [2, 2, 2], [−1, 2, 5]]. The responses are y = (1, 3, 2). Find ŷ, e, e′e and s².",
 "hints":["Direction: you already have H. You do not need to refit anything.",
          "Method: ŷ = Hy, then e = y − ŷ, then divide e′e by tr(M).",
          "Next step: multiply each row of H by y, working in sixths, and take n − k = 3 − 2 = 1 as the divisor."],
 "answer":"ŷ = (1.5, 2, 2.5), e = (−0.5, 1, −0.5), e′e = 1.5 and s² = 1.5.",
 "check":"The residuals sum to zero, and ŷ is the line 1.5 + 0.5x at x = 0, 1, 2.",
 "solution":[
  {"say":"Multiply H by y.","math":"6ŷ₁ = 5·1 + 2·3 − 1·2 = 9\n6ŷ₂ = 2·1 + 2·3 + 2·2 = 12\n6ŷ₃ = −1·1 + 2·3 + 5·2 = 15","why":"Dividing by 6 gives 1.5, 2 and 2.5."},
  {"say":"Subtract.","math":"e = y − ŷ = (1 − 1.5, 3 − 2, 2 − 2.5) = (−0.5, 1, −0.5)","why":"The residuals sum to −0.5 + 1 − 0.5 = 0."},
  {"say":"Sum of squares and variance.","math":"e′e = 0.25 + 1 + 0.25 = 1.5\ns² = 1.5/(3 − 2) = 1.5","why":"With 3 points and 2 coefficients only one degree of freedom is left, so the estimate rests on a single free residual direction."}]})

S.append({"kind":"theory","id":"s11","mins":6,"title":"Where this sits in the syllabus",
 "objective":"Place H and M against the topics that use them.",
 "blocks":[
  {"t":"step","h":"What this topic feeds","body":"Topic 6.2 (Gauss–Markov) proves that OLS is best by writing any competing estimator as OLS plus a term, and the algebra uses HM = 0. Topic 6.3 (ANOVA and the F test) is a statement about the quadratic forms y′Hy and y′My. Topic 6.4 (R² and model comparison) reads R² as a ratio of those two quadratic forms."},
  {"t":"step","h":"What feeds this topic","body":"Quadratic forms and positive definiteness are developed in topic 2.3, and the generalised inverse, needed when X has less than full column rank, in topic 2.8. This lesson uses only the symmetric-idempotent case."},
  {"t":"step","h":"What it does not cover","body":"Influence measures such as Cook's distance, and diagnostics beyond the leverage cut-off 2k/n, are outside this lesson. Heteroscedastic errors change Var(e) and are handled in topic 6.7."}],
 "ask":{"q":"Which later topic needs HM = 0 for its proof?","nudge":"It is the one about the best estimator."}})

S.append({"kind":"recall","id":"s12","mins":2,"title":"Second recall","objective":"Retrieve the parts that fade first.",
 "intro":"Answer, then reveal.",
 "items":[{"q":"What is Var(e)?","a":"σ²M, not σ²I."},
          {"q":"What does u′Mu/σ² follow, under normal errors?","a":"Chi-square with n − k degrees of freedom."},
          {"q":"What is the leverage cut-off often used?","a":"h_ii > 2k/n."},
          {"q":"What is tr(H) when X has rank r < k?","a":"r, the rank."},
          {"q":"In the five-student data, what are the leverages?","a":"0.6, 0.3, 0.2, 0.3, 0.6, adding to 2."}]})

S.append({"kind":"summary","id":"s13","mins":3,"title":"What you should now be able to do","objective":"Check the lesson against its objectives.",
 "body":["Write H = X(X′X)⁻¹X′ and M = I − H, and state that both are symmetric and idempotent.",
         "Read tr(H) = k and tr(M) = n − k, and use them as the degrees of freedom.",
         "Compute leverages for a one-variable model and check that they sum to k.",
         "Derive Var(ŷ) = σ²H, Var(e) = σ²M and Cov(ŷ, e) = 0.",
         "Show E(e′e) = σ²(n − k) and that e′e/σ² is chi-square with n − k degrees of freedom."]})

S.append({"kind":"theory","id":"s14","mins":8,"ext":True,"title":"Extension — the chi-square result in full",
 "objective":"Prove that u′Mu/σ² is chi-square with n − k degrees of freedom.",
 "blocks":[
  {"t":"step","h":"Diagonalise M","body":"M is symmetric, so M = QΛQ′ with Q orthogonal and Λ diagonal. Its eigenvalues are 0 or 1, and exactly n − k of them equal 1 because the trace is n − k."},
  {"t":"step","h":"Rotate the errors","body":"Let w = Q′u. If u ~ N(0, σ²I) then Var(w) = Q′(σ²I)Q = σ²I, so the w_i are independent N(0, σ²). Since Q′ is orthogonal the rotation does not change the distribution."},
  {"t":"step","h":"Read off the sum","body":"u′Mu = u′QΛQ′u = w′Λw = Σλ_i w_i². Exactly n − k of the λ_i are 1 and the rest are 0, so u′Mu = (a sum of n − k independent squares of N(0, σ²)). Dividing by σ² gives a sum of n − k independent squared standard normals, which is chi-square with n − k degrees of freedom."}],
 "ask":{"q":"Which two properties of M are used in this proof?","nudge":"One decides the eigenvalues, the other counts them."}})

S.append({"kind":"quiz","id":"s15","mins":12,"title":"Mastery test",
 "objective":"Demonstrate it independently, on questions you have not seen.","setId":"regression_t1_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id":"regressiont1", "topicId":"regression-t1", "moduleId":"regression",
 "title":"Hat Matrix, Residual Maker and Quadratic Forms",
 "breadcrumb":"Regression → Least-squares algebra → Hat matrix and residual maker",
 "engine":"B", "engineName":"Fitting is projecting: H puts the hat on y, M keeps the leftover, and traces count the degrees of freedom",
 "version":"1.0", "status":"approved",
 "estMin":sum(s["mins"] for s in CORE),
 "objectives":["Write H and M from X and state that both are symmetric and idempotent.",
               "Use tr(H) = k and tr(M) = n − k to count degrees of freedom.",
               "Compute and interpret leverages for a simple regression and check they add to k.",
               "Derive Var(ŷ) = σ²H, Var(e) = σ²M and Cov(ŷ, e) = 0.",
               "Show that E(e′e) = σ²(n − k) and that e′e/σ² is chi-square with n − k degrees of freedom."],
 "prereq":[{"id":"p1","name":"Idempotent matrices and the trace","why":"Every count of degrees of freedom here is the trace of an idempotent matrix."},
           {"id":"p2","name":"The normal equations and β̂","why":"H is built from (X′X)⁻¹X′, the matrix that produces β̂."},
           {"id":"p3","name":"Variance of a linear function Ay","why":"Var(ŷ) and Var(e) come from the rule Var(Ay) = A·Var(y)·A′."},
           {"id":"p4","name":"Sums of squares of standard normals","why":"The distribution of e′e is a chi-square count."}],
 "traps":["Writing tr(M) = n instead of n − k.",
          "Dividing e′e by n and calling it unbiased.",
          "Using Var(e) = σ²I; the correct matrix is σ²M.",
          "Counting columns of X rather than its rank when X is rank-deficient.",
          "Assuming the residuals sum to zero when the model has no intercept."],
 "revision":{
   "sheet":["H = X(X′X)⁻¹X′, ŷ = Hy.  M = I − H, e = My.",
            "H and M: symmetric, idempotent, HM = 0, HX = X, MX = 0.",
            "tr(H) = k, tr(M) = n − k. Eigenvalues are 0 or 1.",
            "Var(ŷ) = σ²H, Var(e) = σ²M, Cov(ŷ, e) = 0.",
            "e′e = y′My = u′Mu. E(e′e) = σ²(n − k). e′e/σ² ~ χ²(n − k).",
            "Leverage h_ii in [0, 1], Σh_ii = k; one-variable case h_ii = 1/n + (x_i − x̄)²/Sxx.",
            "Five-student data: leverages 0.6, 0.3, 0.2, 0.3, 0.6; e′e = 2.4; s² = 0.8.",
            "Rank-deficient X: tr(H) is the rank, so the residual degrees of freedom are n − rank."],
   "cards":[["tr(H)","k, the rank of X"],["tr(M)","n − k"],["Var(e)","σ²M"],["Cov(ŷ, e)","0, since HM = 0"],["Leverage flag","h_ii > 2k/n"],["E(e′e)","σ²(n − k)"],["MX","0"]],
   "tricks":["H puts the hat on y; M is what is left.","Trace of an idempotent matrix = its rank.","A point far from x̄ has high leverage."],
   "shortcuts":["tr(M) = n − k gives the divisor of s².","1/n ≤ h_ii ≤ 1 when there is an intercept.","The five-student leverages 0.6, 0.3, 0.2, 0.3, 0.6 add to 2."],
   "remember":["Degrees of freedom are traces.","Residuals have variance σ²M, not σ²I."]},
 "howto":"If short of time, the lesson is scenes 4 (theory), 5 (worked example) and 8 (variances and the chi-square). Skip the extension. This topic deliberately does not cover Gauss–Markov (6.2), the F test (6.3) or R² (6.4), which each use H and M but own their own results.",
 "refs":[{"title":"Econometrics","where":"Chapter 3, The Algebra of Least Squares","site":"Bruce Hansen","url":"","type":"Free online textbook","free":True,"checked":"2026-11-06","why":"Projection matrices and leverage, scenes 3 and 7."},
         {"title":"Econometric Analysis","where":"Chapter 3, Least Squares","site":"William Greene","url":"","type":"Textbook","free":False,"checked":"2026-11-06","why":"The projection and residual-maker matrices, scene 3."},
         {"title":"Linear Regression Analysis","where":"Chapter 3, Estimation","site":"Seber and Lee","url":"","type":"Textbook","free":False,"checked":"2026-11-06","why":"The chi-square distribution of the residual sum of squares, scene 7 and the extension."}],
 "mastery":{"minQ":10,"pass":80,"draw":10,"fmtMin":{"numeric":70,"multi":70},
            "diffMix":{"easy":3,"moderate":5,"hard":2},"noHints":True,"retestDays":7,
            "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on "
                   "numerical and multi-statement items, answered without hints. Each paper is "
                   "drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style "
                   "paper; NTA publishes no official difficulty split."},
 "provenance":"No June 2026 question anchors this topic. Q9 was checked against the backlog's note that it might belong here: its stem is the F statistic written in R², so it is taught in topic 6.3 and its variants in 6.3 and 6.4. Verified by computing, in verify_regression_t1_t4.py: the five-student fit (2.2 + 0.6x, residuals −0.8, 0.6, 1.0, −0.6, −0.2, e′e = 2.4, s² = 0.8); H symmetric and idempotent; HX = X; MX = 0; HM = 0; tr(H) = 2 and tr(M) = 3; eigenvalues of H are 0 or 1; leverages 0.6, 0.3, 0.2, 0.3, 0.6; the n = 3 hat matrix and the transfer case (fitted 1.5, 2, 2.5; e′e = 1.5). By simulation with 200,000 draws: E(e′e) = 11.998 against the exact 12, and the 95th percentile of e′e/σ² is 7.76 against the chi-square(3) value 7.815. A rank-deficient one-way design gave tr(H) = 2 for 3 columns, and an indicator column for one observation gave h = 1 and e = 0 exactly. Scope: Gauss–Markov, the F test and R² are left to 6.2, 6.3 and 6.4.",
 "scenes":S}

# ─────────────────────────────── pool: exactly 20 items ───────────────────────────────
def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id":"regression-t1-m-%02d"%i, "format":fmt, "topic":"regression-t1",
         "diff":diff, "stem":stem, "options":opts, "answer":ans, "explanation":exp}
    d.update(kw); return d

def verd(a,b,c,dd):
    return {"A":{"tf":a[0],"why":a[1]},"B":{"tf":b[0],"why":b[1]},
            "C":{"tf":c[0],"why":c[1]},"D":{"tf":dd[0],"why":dd[1]}}

I = []
# Author each item with the correct option FIRST (answer A); WANT then spreads the keys.
I.append(q(1,"single","easy","In the model y = Xβ + u, the matrix that maps y to the fitted vector ŷ is:",
  ["X(X′X)⁻¹X′","(X′X)⁻¹X′","I − X(X′X)⁻¹X′","X′X"],"A",
  "ŷ = Xβ̂ = X(X′X)⁻¹X′y, so the map is X(X′X)⁻¹X′, called the hat matrix. The matrix (X′X)⁻¹X′ produces β̂, not ŷ. I − H produces the residuals. X′X is the k×k cross-product matrix."))
I.append(q(2,"single","easy","The residual vector e can be written as:",
  ["My, where M = I − X(X′X)⁻¹X′","Hy, where H = X(X′X)⁻¹X′","(X′X)⁻¹X′y","Xβ̂"],"A",
  "e = y − ŷ = y − Hy = (I − H)y = My. Hy is the fitted vector, (X′X)⁻¹X′y is the coefficient vector and Xβ̂ is again the fitted vector."))
I.append(q(3,"numeric","easy","In a regression with an intercept and three slopes fitted to n = 20 observations, tr(H) is:",
  ["4","3","16","20"],"A",
  "tr(H) equals the number of columns of X, which is 1 + 3 = 4. Three is the number of slopes only. Sixteen is tr(M) = n − k and twenty is tr(I).",
  check="tr(H) + tr(M) must equal tr(I) = 20; with tr(M) = 16 the partner is 4."))
I.append(q(4,"single","easy","Which statement about M = I − X(X′X)⁻¹X′ is correct?",
  ["MX = 0","MX = X","MX = I","M is not symmetric"],"A",
  "MX = X − X(X′X)⁻¹X′X = X − X = 0, so M annihilates every column of X. The statement MX = X describes H, not M. M is symmetric because H is."))
I.append(q(5,"numeric","easy","In a regression with 4 coefficients fitted to 20 observations and σ² = 3, E(e′e) equals:",
  ["48","60","12","57"],"A",
  "E(e′e) = σ²tr(M) = 3 × (20 − 4) = 48. Sixty is σ²n, which would apply to the errors themselves. Twelve is σ²k and fifty-seven is σ²(n − 1).",
  check="E(e′e) must be below σ²n = 60, because fitting coefficients absorbs some error."))
I.append(q(6,"single","easy","The eigenvalues of the hat matrix H are:",
  ["only 0 and 1","only 1","between −1 and 1","all positive and distinct"],"A",
  "H is idempotent, so any eigenvalue satisfies λ² = λ, which gives 0 or 1. The eigenvalue 1 appears k times and 0 appears n − k times, so not all are 1, and they are not distinct."))
I.append(q(7,"numeric","moderate","For x = 1, 2, 3, 4, 5 in a model with an intercept, the leverage h₁₁ of the first observation is:",
  ["0.6","0.2","0.3","0.4"],"A",
  "h_ii = 1/n + (x_i − x̄)²/Sxx = 1/5 + (1 − 3)²/10 = 0.2 + 0.4 = 0.6. The value 0.2 is the leverage at the mean, x = 3, and 0.3 is at x = 2 or 4. Using 1 − h gives 0.4.",
  check="The leverages must add up to k = 2: 0.6 + 0.3 + 0.2 + 0.3 + 0.6 = 2."))
I.append(q(8,"single","moderate","Under y = Xβ + u with Var(u) = σ²I, the covariance matrix of the residual vector e is:",
  ["σ²M","σ²I","σ²H","σ²(X′X)⁻¹"],"A",
  "Var(e) = Var(Mu) = M(σ²I)M′ = σ²M. The residuals are therefore correlated and have unequal variances 1 − h_ii. σ²I is the error covariance, σ²H is Var(ŷ) and σ²(X′X)⁻¹ is Var(β̂)."))
I.append(q(9,"multi","moderate","Consider the hat matrix H = X(X′X)⁻¹X′ for a full-rank X with k columns and n rows.",
  ["A, B and D only","A and B only","B, C and D only","A, B, C and D"],"A",
  "HX = X, symmetry and HM = 0 hold. The trace of H is k, not n, so the statement that it equals n is false.",
  statements=["HX = X","H is symmetric","tr(H) = n","HM = 0, where M = I − H"],
  verdicts=verd((True,"H projects onto the column space of X, so X is unchanged."),
                (True,"H′ = X(X′X)⁻¹X′ = H, since (X′X)⁻¹ is symmetric."),
                (False,"tr(H) = k, the number of columns. It equals n only when H = I."),
                (True,"HM = H − HH = H − H = 0."))))
I.append(q(10,"single","moderate","The fitted values ŷ and the residuals e are uncorrelated because:",
  ["HM = 0, so Cov(ŷ, e) = σ²HM = 0","H is the identity","M has rank n","X has an intercept"],"A",
  "Cov(Hy, My) = H(σ²I)M′ = σ²HM = σ²(H − HH) = 0. H is not the identity, M has rank n − k, and an intercept is not needed for this covariance to vanish."))
I.append(q(11,"numeric","moderate","A regression with n = 5 and k = 2 has a residual sum of squares of 2.4. The unbiased estimate of σ² is:",
  ["0.8","0.48","1.2","2.4"],"A",
  "s² = e′e/(n − k) = 2.4/3 = 0.8. Dividing by n gives 0.48, dividing by k gives 1.2 and leaving it undivided gives 2.4.",
  check="The unbiased estimate must exceed e′e/n = 0.48, so it rules out 0.48 and anything smaller."))
I.append(q(12,"single","moderate","If u ~ N(0, σ²I), then e′e/σ² follows:",
  ["a chi-square with n − k degrees of freedom","a chi-square with n degrees of freedom","a chi-square with k degrees of freedom","a t distribution with n − k degrees of freedom"],"A",
  "e′e = u′Mu, and M is symmetric idempotent of rank n − k, so the quadratic form is a sum of n − k independent squared normals. Using n or k gives the wrong count, and a t distribution is a ratio, not a sum of squares."))
I.append(q(13,"single","moderate","Which of these 2×2 matrices is idempotent but is not a hat matrix of any regression?",
  ["[[1, 1], [0, 0]]","[[1, 0], [0, 0]]","[[0, 0], [0, 1]]","[[0.5, 0.5], [0.5, 0.5]]"],"A",
  "[[1, 1], [0, 0]] squared equals itself but is not symmetric, so it is an oblique projection. The other three are symmetric and idempotent, so each is a hat matrix for some X."))
I.append(q(14,"numeric","moderate","For x = 0, 1, 2 the middle row of H is (1/3, 1/3, 1/3). With y = (1, 3, 2) the fitted value ŷ₂ is:",
  ["2","3","1.5","2.5"],"A",
  "ŷ₂ = (1 + 3 + 2)/3 = 2. The observed y₂ is 3, which gives a residual of 1. The values 1.5 and 2.5 are the other two fitted values.",
  check="The weights sum to 1, so ŷ₂ is an average of the y values and must lie between 1 and 3."))
I.append(q(15,"single","moderate","The leverages h_ii of a regression with k coefficients always:",
  ["sum to k","sum to n","sum to n − k","are equal to 1/n"],"A",
  "Σh_ii = tr(H) = k. They sum to n − k only for M. They are all 1/n only for a model that fits just a constant."))
I.append(q(16,"multi","moderate","For the residuals e = My of a model that includes an intercept:",
  ["A, B and C only","A and B only","B, C and D only","A, B, C and D"],"A",
  "e = My, the residuals have mean zero because of the intercept, and E(e) = 0. Their covariance is σ²M, not σ²I, so the statement about equal variances is false.",
  statements=["e = My","Σe_i = 0","E(e) = 0","Var(e) = σ²I"],
  verdicts=verd((True,"This is the definition of the residual maker."),
                (True,"The column of ones lies in X and X′e = 0."),
                (True,"E(e) = ME(u) = 0."),
                (False,"Var(e) = σ²M, whose diagonal 1 − h_ii varies and whose off-diagonals are not zero."))))
I.append(q(17,"numeric","hard","For x = 0, 1, 2 with an intercept, the leverage of the third observation is:",
  ["5/6","1/3","2/3","1"],"A",
  "h₃₃ = 1/3 + (2 − 1)²/2 = 1/3 + 1/2 = 5/6. At x = 1 the leverage is 1/3, and the three leverages 5/6, 1/3, 5/6 add to 2.",
  check="A leverage must be at most 1 and at least 1/n = 1/3; the end points must exceed the centre."))
I.append(q(18,"numeric","hard","With s² = 0.8 and h₁₁ = 0.6, the estimated variance of the first residual is:",
  ["0.32","0.8","0.48","1.28"],"A",
  "Var(e₁) is estimated by s²(1 − h₁₁) = 0.8 × 0.4 = 0.32. Using s² alone assumes Var(e) = σ²I. The value 0.48 is s²h₁₁ and 1.28 is s²(1 + h₁₁).",
  check="The variance of a residual must be smaller than s² whenever the leverage is positive."))
I.append(q(19,"single","hard","A design matrix X has 3 columns but rank 2, and n = 4. The degrees of freedom of the residual sum of squares are:",
  ["2","1","3","4"],"A",
  "tr(M) = n − rank(X) = 4 − 2 = 2. Counting columns would give 1. The rank, not the number of columns, is the dimension of the column space, and the trace of H equals that rank."))
I.append(q(20,"single","hard","A regression includes a separate indicator column for observation 1 (1 for that observation, 0 elsewhere). What follows for that observation?",
  ["h₁₁ = 1 and e₁ = 0","h₁₁ = 0 and e₁ = 0","h₁₁ = 1 and e₁ = y₁","h₁₁ = 1/n and e₁ is unrestricted"],"A",
  "The indicator column makes the fitted line pass exactly through y₁, so ŷ₁ = y₁ and e₁ = 0. Since ŷ₁ = Σh₁ⱼyⱼ equals y₁ for every y, h₁₁ = 1. The five-point calculation confirms h₁₁ = 1 and e₁ = 0."))

# Key spread: spread the keys evenly, 5 of each letter.
LET = "ABCD"
PAT = "CBDACBADCBADBCADBDCA"
WANT = {"regression-t1-m-%02d" % (i + 1): PAT[i] for i in range(20)}

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

POOLD = {"moduleId":"regression","topicId":"regression-t1","source":"mastery",
         "label":"Hat matrix, residual maker and quadratic forms — mastery test (unseen)","count":len(I),"items":I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT,"w",encoding="utf-8") as f:  json.dump(LES,f,ensure_ascii=False,indent=1)
with io.open(POOL,"w",encoding="utf-8") as f: json.dump(POOLD,f,ensure_ascii=False,indent=1)
print("wrote %s: %d scenes (%d core), estMin %d"%(OUT,len(S),len(CORE),LES["estMin"]))
print("wrote %s: %d items"%(POOL,len(I)))
