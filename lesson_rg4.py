#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regression-t4 (topic 6.4): R², adjusted R², model comparison. Q9 variants (adjusted R², added regressors).
Every figure below is computed in verify_regression_t1_t4.py; nothing is recalled."""
import json, io, os, re, random

OUT  = "seed/lesson_rg4.json"
POOL = "seed/regression_t4_mastery.json"

S = []

S.append({"kind":"foundation","id":"s0","mins":7,"title":"Before the lesson — four things it will assume",
 "objective":"Check R², the two degrees-of-freedom counts, nested models and the F statistic.",
 "ask":{"q":"Why is R² alone a poor way to choose between a small model and a larger one?","nudge":"What happens to the residual sum of squares when a regressor is added?"},
 "body":["R² answers one question: what share of the variation in y does the fitted model explain. It cannot answer a different question: is the extra regressor worth keeping. Adding any regressor, even a column of random numbers, leaves R² the same or higher. So a rule that picks the model with the highest R² always picks the biggest model.",
         "Two repairs exist. Adjusted R² divides each sum of squares by its degrees of freedom, so a parameter must pay for itself. Information criteria add a penalty per parameter directly. A third tool, the F test for nested models, asks whether the drop in the residual sum of squares is larger than chance would give.",
         "Part of Q9's bank asks for adjusted R² from n, k and R², and for what adding a regressor does. The working is one line; the usual loss is in the choice between n − k and n − k − 1, and in forgetting to subtract from 1. This lesson fixes the count first, then checks each answer against R² itself."],
 "items":[
  {"ask":"Define R² for a model with an intercept, and give its range.",
   "recall":"R² = RegSS/TSS = 1 − RSS/TSS, between 0 and 1.",
   "refresh":["R² is the explained share of the total variation. For the five-student data R² = 3.6/6 = 0.6. With an intercept it cannot be negative and cannot exceed 1.",
              "It is also the squared correlation between y and the fitted values. It does not say whether the model is correct, only how closely it fits."]},
  {"ask":"What are the degrees of freedom of RSS and of TSS?",
   "recall":"n − k and n − 1.",
   "refresh":["From topic 6.1 the residuals live in a space of dimension tr(M) = n − k, where k counts every coefficient including the intercept. TSS has n − 1 because the deviations from the mean add to zero.",
              "In Q9's variant the quantity k = 5 counts all five parameters, so n − k = 45 when n = 50. Reading k as the number of slopes only would give 44, which is a different answer."]},
  {"ask":"What does it mean for two models to be nested?",
   "recall":"The smaller model is the larger one with some coefficients set to zero.",
   "refresh":["Model B is nested in model A if B is A with a set of restrictions, usually some coefficients fixed at zero. Then A can fit everything B can, so RSS_A ≤ RSS_B.",
              "Models using different regressors, none containing the other, are non-nested. The F test below does not apply to them."]},
  {"ask":"State the F statistic for H₀: all slopes zero in terms of R².",
   "recall":"F = [R²/(k − 1)]/[(1 − R²)/(n − k)].",
   "refresh":["From topic 6.3. It divides the explained share by its degrees of freedom and the unexplained share by its own. The numerator degrees of freedom are the number of slopes.",
              "The nested version replaces R² by the increase in R² and k − 1 by the number of restrictions q."]}]})

S.append({"kind":"intuition","id":"s1","mins":7,"title":"Fit always improves; the question is whether it improves enough",
 "objective":"Explain why R² cannot choose a model, and what adjusted R² charges.",
 "body":["Adding a regressor gives the least-squares fit one more direction to use. At worst it ignores it, so the residual sum of squares cannot rise, and R² cannot fall. That is a fact about geometry, not about whether the new variable is relevant.",
         "A fair comparison has to charge for the extra direction. Adjusted R² does so by replacing each sum of squares with its average per degree of freedom: 1 − [RSS/(n − k)] / [TSS/(n − 1)]. Adding a regressor lowers n − k, which raises the first average unless RSS falls enough to compensate. The exact break-even is simple: adjusted R² rises precisely when the new coefficient's t statistic exceeds 1 in absolute value.",
         "That break-even is lenient. A t of 1.1 is nowhere near significant, yet adjusted R² rises. Adjusted R² is a mild penalty. The F test, AIC and BIC apply stronger ones."],
 "scenario":{"teaser":"Two models for the same twenty observations, one with two extra regressors.",
  "title":"Is the larger model worth it?",
  "body":["An analyst has 20 observations with total variation TSS = 72214. A model with two parameters, an intercept and one regressor, leaves a residual sum of squares of 9000, so R² = 0.875. A larger model with four parameters leaves RSS = 5344, so R² = 0.926.",
          "The larger model has the higher R², by construction. Adjusted R² gives 0.9121 against 0.8685, so the larger model still wins after the charge for two extra parameters. The nested F test asks whether the drop of 3656 in RSS, spread over the two added coefficients, is large compared with the residual average 5344/16 = 334: F = 1828/334 = 5.47, which exceeds the 5% point of F(2, 16), 3.634.",
          "AIC agrees (119.76 against 126.19) and so does BIC (123.74 against 128.18). When four criteria point the same way the choice is easy. The interesting cases are those where they disagree, and the lesson shows why."],
  "q":"Which of R², adjusted R² and the nested F test could not have favoured the smaller model if the larger model's RSS were lower?",
  "answer":"R². Adding regressors never raises RSS, so R² always favours the larger model. Adjusted R² and F can favour the smaller model if the drop in RSS is too small."},
 "ask":{"q":"Does a rise in adjusted R² after adding a regressor mean that regressor is significant?","nudge":"What t statistic is the break-even?"}})

S.append({"kind":"explore","id":"s2","mins":7,"title":"How large must R² be to count?",
 "objective":"See that the evidence R² gives depends on n, and find the threshold for one regressor at n = 20.",
 "viz":{"type":"r-null","caption":"Set n = 20. With one regressor, R² = r², and the 5% two-sided critical |r| is about 0.444, so R² must exceed 0.197."},
 "body":["With a single regressor R² is the square of the correlation r. The picture shows how r behaves when the true correlation is zero. At n = 20 the 5% two-sided critical value is |r| = 0.444, so R² has to exceed 0.197 before it is evidence of anything.",
         "Slide n to 5 and the threshold becomes 0.771. Slide to 60 and it falls below 0.07. The same R² means different things in different sample sizes.",
         "This is why R² should be read with n and k beside it, and why adjusted R² and the F test bring them in."],
 "ask":{"q":"Would an R² of 0.15 be significant at n = 20 with one regressor?","nudge":"Compare with 0.197."}})

S.append({"kind":"theory","id":"s3","mins":9,"title":"R², adjusted R², F for nested models, AIC, BIC and Cp",
 "objective":"State each criterion and what it penalises.",
 "blocks":[
  {"t":"formula","h":"R² and adjusted R²","body":"R² = 1 − RSS/TSS\nR̄² = 1 − [RSS/(n − k)] / [TSS/(n − 1)] = 1 − (1 − R²)(n − 1)/(n − k)"},
  {"t":"step","h":"What adjusted R² does","body":"R̄² < R² whenever k > 1, and R̄² can be negative. It is negative when R² < (k − 1)/(n − 1). It never exceeds 1. It equals 1 − s²/s_y², where s² is the residual variance estimate and s_y² the sample variance of y."},
  {"t":"formula","h":"F for nested models (q restrictions)","body":"F = [(RSS_r − RSS_f)/q] / [RSS_f/(n − k_f)]\n  = [(R²_f − R²_r)/q] / [(1 − R²_f)/(n − k_f)]\non (q, n − k_f) degrees of freedom."},
  {"t":"formula","h":"Information criteria (Gaussian errors, constants dropped)","body":"AIC = n ln(RSS/n) + 2k\nBIC = n ln(RSS/n) + k ln n\nSmaller is better. BIC's penalty per parameter ln n exceeds AIC's 2 once n ≥ 8."},
  {"t":"formula","h":"Mallows Cp","body":"Cp = RSS_p/σ̂² − (n − 2p),   σ̂² = RSS of the full model/(n − k_full)\nFor a model with little bias, Cp is close to its parameter count p."}],
 "table":{"caption":"Which criterion to use","head":["Tool","Compares","Penalty","Valid for"],
  "rows":[["R²","descriptive fit","none","one model"],["Adjusted R²","models, same y","mild: |t| > 1","any models, same y"],["Nested F","two models","significance level","nested only"],["AIC","models, same y","2 per parameter","any models, same y"],["BIC","models, same y","ln n per parameter","any models, same y"],["Cp","subsets","via σ̂² of full model","subsets of a full model"]]},
 "flow":{"title":"Choosing how to compare models","alt":"A top-to-bottom flow. First check the dependent variable is the same. If the models are nested use the F test. If not, use AIC or BIC. Adjusted R squared is a quick screen.",
  "nodes":[{"id":"a","r":0,"c":1,"label":"Same dependent variable y?","kind":"start"},
           {"id":"b","r":1,"c":1,"label":"Nested models?","kind":"step"},
           {"id":"c","r":2,"c":0,"label":"Yes: F test on the added coefficients","kind":"end"},
           {"id":"d","r":2,"c":2,"label":"No: compare AIC or BIC (lower wins)","kind":"end"},
           {"id":"e","r":1,"c":3,"label":"Different y: no valid comparison on R² or RSS","kind":"note"}],
  "edges":[{"from":"a","to":"b"},{"from":"b","to":"c"},{"from":"b","to":"d"}],
  "note":"R² and RSS from regressions with different dependent variables (for example y and ln y) are not comparable."},
 "ask":{"q":"When is adjusted R² negative?","nudge":"Compare R² with (k − 1)/(n − 1)."}})

S.append({"kind":"worked","id":"s4","mins":8,"title":"Comparing two models on twenty observations, every criterion",
 "objective":"Compute R², adjusted R², nested F, AIC, BIC and Cp for the models in the first scenario.",
 "ask":{"q":"Do all the criteria prefer the larger model?","nudge":"Compute each, then compare."},
 "problem":"n = 20, TSS = 72214. Model R (k = 2): RSS = 9000. Model F (k = 4): RSS = 5344. Compare them.",
 "steps":[
  {"say":"R² for each.","math":"R²_R = 1 − 9000/72214 = 0.8754\nR²_F = 1 − 5344/72214 = 0.9260","why":"The larger model's R² is higher, as it must be."},
  {"say":"Adjusted R².","math":"R̄²_R = 1 − (0.12463)(19/18) = 0.8685\nR̄²_F = 1 − (0.07400)(19/16) = 0.9121","why":"The factor (n − 1)/(n − k) is 19/18 for the small model and 19/16 for the large one. The larger model survives the charge."},
  {"say":"Nested F for the two added coefficients (q = 2).","math":"F = [(9000 − 5344)/2] / [5344/16] = 1828/334 = 5.473\nF(2, 16) 5% point = 3.634","why":"5.473 > 3.634, so reject the restrictions. The same F in R² form: [(0.9260 − 0.8754)/2]/[0.0740/16]."},
  {"say":"AIC and BIC.","math":"AIC_R = 20 ln(450) + 4 = 126.19,   AIC_F = 20 ln(267.2) + 8 = 119.76\nBIC_R = 20 ln(450) + 2 ln 20 = 128.18,   BIC_F = 20 ln(267.2) + 4 ln 20 = 123.74","why":"Smaller is better, so both prefer F. The difference is 6.43 for AIC and 4.43 for BIC."},
  {"say":"Cp for the small model.","math":"σ̂² = 5344/16 = 334\nCp_R = 9000/334 − (20 − 2·2) = 26.95 − 16 = 10.95   against p = 2","why":"A Cp far above p signals that the small model is biased, which agrees with the F test. For the full model Cp = 4 exactly."}],
 "after":"All six measures agree here. When the answer is clear every method finds it; the value of knowing them is for the unclear cases."})

S.append({"kind":"recall","id":"s5","mins":2,"title":"Pause and recall","objective":"Retrieve the formulas before using them.",
 "intro":"Answer each before revealing it.",
 "items":[{"q":"Write adjusted R² in terms of R², n and k.","a":"1 − (1 − R²)(n − 1)/(n − k)."},
          {"q":"Does adding a regressor lower R²?","a":"Never. It stays the same or rises."},
          {"q":"When does adjusted R² rise on adding a regressor?","a":"Exactly when the new coefficient's |t| exceeds 1."},
          {"q":"Can adjusted R² be negative?","a":"Yes, when R² < (k − 1)/(n − 1)."},
          {"q":"Which is larger, BIC's penalty per parameter or AIC's, for n = 20?","a":"BIC: ln 20 = 2.996 against 2."}]})

S.append({"kind":"completion","id":"s6","mins":8,"title":"Your turn — a negative adjusted R²",
 "objective":"Compute adjusted R² for a poorly fitting model with many parameters.",
 "problem":"n = 20, k = 6 parameters and R² = 0.10. Find the adjusted R².",
 "steps":[
  {"say":"Start from the unexplained share.",
   "blank":{"prompt":"What is 1 − R²?","answer":"0.9","accept":["0.9","0.90","9/10"],"hint":"1 − 0.10."},
   "why":"0.9 is the share the model leaves unexplained."},
  {"say":"The adjustment factor is (n − 1)/(n − k).",
   "blank":{"prompt":"What is (n − 1)/(n − k)?","answer":"19/14","accept":["19/14","1.357","1.36","1.3571"],"hint":"n − 1 = 19 and n − k = 14."},
   "why":"19/14 = 1.3571."},
  {"say":"Multiply, then subtract from 1.",
   "blank":{"prompt":"What is the adjusted R², to two decimals?","answer":"-0.22","accept":["-0.22","−0.22","-0.2214","−0.2214","-0.221"],"hint":"1 − 0.9 × 1.3571."},
   "why":"0.9 × 1.3571 = 1.2214, so R̄² = −0.2214."},
  {"say":"Check against the threshold (k − 1)/(n − 1).",
   "blank":{"prompt":"What is (k − 1)/(n − 1)?","answer":"5/19","accept":["5/19","0.263","0.2632","0.26"],"hint":"5 over 19."},
   "why":"0.2632. R² = 0.10 is below it, so the adjusted value must be negative, as found."}],
 "after":"A negative adjusted R² is a signal, not an error: the model fits worse than a constant once its parameters are charged."})

S.append({"kind":"theory","id":"s7","mins":7,"title":"Why adjusted R² rises exactly when |t| > 1, and the no-intercept trap",
 "objective":"Derive the break-even for adjusted R² and explain why R² from a model with no intercept cannot be compared.",
 "blocks":[
  {"t":"step","h":"Adjusted R² and s²","body":"R̄² = 1 − s²/s_y², with s_y² = TSS/(n − 1) unchanged when a regressor is added. So R̄² rises exactly when s² = RSS/(n − k) falls."},
  {"t":"step","h":"What the t statistic does","body":"Let m = n − k before the addition. Adding one regressor with t statistic t gives RSS_old = RSS_new·(1 + t²/(m − 1)). Then s²_new < s²_old when RSS_new/(m − 1) < RSS_new(1 + t²/(m − 1))/m. Multiply out by m(m − 1)/RSS_new: m < m − 1 + t², which is t² > 1."},
  {"t":"step","h":"Checked on a case","body":"Start with n = 20, k = 3, R² = 0.5, so R̄² = 0.4412. Add a regressor with t = 0.8: R² rises to 0.5192 but R̄² falls to 0.4291. With |t| = 1 exactly R̄² is unchanged. A check on 4000 random data sets confirmed the rule every time, and that R² never fell."},
  {"t":"step","h":"R² without an intercept","body":"When the model has no intercept the software reports an uncentred R² = 1 − RSS/Σy². For y = 10, 12, 13, 15, 16 on x = 1..5 the no-intercept fit gives 0.9227 and the model with an intercept gives 0.9868. Measured against the centred total, the no-intercept fit gives −2.03. The two R² values are on different scales and must not be compared."},
  {"t":"step","h":"Different dependent variable","body":"R² and RSS from a regression of ln y cannot be compared with those of a regression of y. Their totals measure different things. AIC, after adding the Jacobian term, can compare them; plain R² cannot."}],
 "ask":{"q":"Why is |t| > 1 a weak test for keeping a regressor?","nudge":"Compare with the usual critical value near 2."}})

S.append({"kind":"guided","id":"s8","mins":8,"title":"On your own — adjusted R² from n, k and R²",
 "objective":"Compute adjusted R² for the Q9 variant and check it.",
 "problem":"With n = 50, k = 5 and R² = 0.55, find the adjusted R².",
 "hints":["Direction: decide what k counts. Here k = 5 is the number of parameters, so n − k = 45.",
          "Method: R̄² = 1 − (1 − R²)(n − 1)/(n − k).",
          "Next step: compute 0.45 × 49/45 first, then subtract from 1."],
 "answer":"R̄² = 1 − 0.49 = 0.51.",
 "check":"The answer must lie below R² = 0.55 and close to it, since n is large relative to k. The value 0.49 is the unexplained share and 0.45 is 1 − R².",
 "scenario":{"teaser":"A regression through the origin reports an R² that looks better than the same model with an intercept.",
  "title":"The R² that looks too good",
  "body":["An analyst fits y on x for five points, x = 1, 2, 3, 4, 5 and y = 10, 12, 13, 15, 16, once with an intercept and once forcing the line through the origin. The software reports R² = 0.9868 for the first and R² = 0.9227 for the second.",
          "The second figure uses a different denominator. With no intercept the software compares RSS with Σy², the total about zero, rather than with the total about the mean. That denominator is much larger, because the y values are far from zero, which flatters the fit.",
          "Measure the no-intercept fit against the usual centred total and R² becomes −2.03. A line forced through the origin fits these data far worse than a horizontal line at the mean. The reported 0.9227 hid that."],
  "q":"Can the R² of a no-intercept model be compared with the R² of a model with an intercept?",
  "answer":"No. They use different totals. On a common, centred footing the no-intercept fit is −2.03 against 0.9868."},
 "solution":[
  {"say":"Count the degrees of freedom.","math":"n − 1 = 49,   n − k = 50 − 5 = 45","why":"k counts every parameter, including the intercept."},
  {"say":"Form the adjustment.","math":"(1 − R²)(n − 1)/(n − k) = 0.45 × 49/45 = 0.49","why":"The inflation 49/45 raises the unexplained share from 0.45 to 0.49."},
  {"say":"Subtract.","math":"R̄² = 1 − 0.49 = 0.51","why":"If k = 5 had counted only the slopes the divisor would be 44 and the answer 0.4989, which rounds to 0.50. Read the definition of k."}]})

S.append({"kind":"trapcheck","id":"s9","mins":6,"title":"Six statements","objective":"Separate true properties of the criteria from tempting false ones.",
 "intro":"Decide true or false on all six before revealing any.",
 "items":[
  {"claim":"Adding an irrelevant regressor can lower R².","tf":False,"why":"R² stays the same or rises. Least squares can always set the new coefficient to zero."},
  {"claim":"Adjusted R² can be negative.","tf":True,"why":"It is negative when R² < (k − 1)/(n − 1). For R² = 0.10, n = 20, k = 6 it is −0.2214."},
  {"claim":"A rise in adjusted R² after adding a regressor shows that its coefficient is significant at 5%.","tf":False,"why":"The break-even is |t| > 1. Significance at 5% needs |t| above about 2."},
  {"claim":"The nested F test can compare a model in x with a model in a different set of regressors that does not contain it.","tf":False,"why":"It needs nested models, the smaller one obtained from the larger by restrictions."},
  {"claim":"BIC penalises an extra parameter more heavily than AIC once n ≥ 8.","tf":True,"why":"The BIC penalty per parameter is ln n, which exceeds 2 from n = 8 (ln 8 = 2.079)."},
  {"claim":"R² can be used to compare a regression of y with a regression of ln y.","tf":False,"why":"The dependent variables differ, so the totals differ. The R² values are not on a common footing."}]})

S.append({"kind":"guided","id":"s10","mins":8,"title":"Transfer — what a weak regressor does",
 "objective":"Predict the effect of adding a regressor with a small t statistic.",
 "problem":"A model with n = 20, k = 3 and R² = 0.5 gains a fourth parameter whose t statistic is 0.8. Find the new R² and adjusted R², and say what happened.",
 "hints":["Direction: first find the old adjusted R² from n, k and R².",
          "Method: RSS_old/RSS_new = 1 + t²/(m − 1), where m = n − k_old = 17.",
          "Next step: the new unexplained share is 0.5 divided by that ratio; then apply the adjustment with k = 4."],
 "answer":"R² rises from 0.5 to 0.5192; adjusted R² falls from 0.4412 to 0.4291, because |t| = 0.8 < 1.",
 "check":"R² must rise or stay put, and adjusted R² must fall because |t| < 1.",
 "solution":[
  {"say":"Old adjusted R².","math":"1 − 0.5 × 19/17 = 1 − 0.55882 = 0.44118","why":"n − k = 17."},
  {"say":"New unexplained share.","math":"ratio = 1 + 0.64/16 = 1.04\n1 − R²_new = 0.5/1.04 = 0.48077,   R²_new = 0.51923","why":"The new regressor trims RSS by under 4%."},
  {"say":"New adjusted R².","math":"1 − 0.48077 × 19/16 = 1 − 0.57091 = 0.42909","why":"The fit gained little and the extra parameter was charged more than it earned."}]})

S.append({"kind":"theory","id":"s11","mins":6,"title":"Where this sits in the syllabus",
 "objective":"Place model comparison against the topics around it.",
 "blocks":[
  {"t":"step","h":"What it builds on","body":"The sums of squares and the F statistic are from topic 6.3, and the counts n − k and n − 1 from topic 6.1."},
  {"t":"step","h":"What it leads to","body":"Topic 6.5 explains why a high R² can sit beside insignificant t statistics: near multicollinearity. Topic 6.11 uses nested F tests to compare models with and without dummy variables."},
  {"t":"step","h":"What it does not cover","body":"Cross-validation, likelihood-ratio tests beyond the Gaussian case, and stepwise search are not covered. AIC and BIC appear here as formulas with Gaussian errors only."}],
 "ask":{"q":"Which topic explains a high R² with insignificant individual t values?","nudge":"Collinear regressors."}})

S.append({"kind":"recall","id":"s12","mins":2,"title":"Second recall","objective":"Retrieve the parts that fade first.",
 "intro":"Answer, then reveal.",
 "items":[{"q":"Adjusted R² for n = 50, k = 5, R² = 0.55?","a":"0.51."},
          {"q":"The nested F in the 20-observation comparison?","a":"5.473 against a 5% point of 3.634."},
          {"q":"What is the sign of AIC's and BIC's preference?","a":"Smaller is better."},
          {"q":"What does a Cp far above p suggest?","a":"The model is biased: it leaves out something."},
          {"q":"Why is a no-intercept R² not comparable?","a":"It is measured against Σy², not the centred total."}]})

S.append({"kind":"summary","id":"s13","mins":3,"title":"What you should now be able to do","objective":"Check the lesson against its objectives.",
 "body":["Compute adjusted R² from n, k and R², with k counting every parameter.",
         "State that R² never falls when a regressor is added and that adjusted R² rises exactly when |t| > 1.",
         "Run the nested F test in RSS and R² forms.",
         "Compare AIC, BIC and Cp values and know which direction wins.",
         "Recognise comparisons that are not valid: different dependent variable, no intercept, non-nested F."]})

S.append({"kind":"theory","id":"s14","mins":8,"ext":True,"title":"Extension — the identity behind the break-even",
 "objective":"Prove RSS_old = RSS_new(1 + t²/(m − 1)).",
 "blocks":[
  {"t":"step","h":"The added-variable F","body":"Dropping one regressor from the larger model is a single restriction. The F statistic is (RSS_old − RSS_new)/(RSS_new/(m − 1)), where m − 1 = n − k_new."},
  {"t":"step","h":"Single restriction means F = t²","body":"For one restriction the partial F equals the square of the t statistic of the dropped coefficient, as shown in topic 6.3. So RSS_old − RSS_new = t²·RSS_new/(m − 1)."},
  {"t":"step","h":"Rearrange","body":"RSS_old = RSS_new(1 + t²/(m − 1)). This is the identity used in the break-even and in the transfer example."}],
 "ask":{"q":"Which earlier topic gave F = t² for one restriction?","nudge":"The ANOVA lesson."}})

S.append({"kind":"quiz","id":"s15","mins":12,"title":"Mastery test",
 "objective":"Demonstrate it independently, on questions you have not seen.","setId":"regression_t4_mastery"})

CORE = [s for s in S if not s.get("ext")]

LES = {
 "id":"regressiont4", "topicId":"regression-t4", "moduleId":"regression",
 "title":"R², Adjusted R² and Model Comparison",
 "breadcrumb":"Regression → Inference in the linear model → R², adjusted R² and model comparison",
 "engine":"B", "engineName":"Fit always improves; charge for each parameter and compare only like with like",
 "version":"1.0", "status":"approved",
 "estMin":sum(s["mins"] for s in CORE),
 "objectives":["Compute adjusted R² from n, k and R², counting k correctly.",
               "State what adding a regressor does to R² and to adjusted R², and why.",
               "Run and read the nested F test, AIC, BIC and Cp for two models.",
               "Recognise a negative adjusted R² and a no-intercept R² that is not comparable.",
               "Decide whether a model comparison is valid before computing it."],
 "prereq":[{"id":"p1","name":"R² and TSS","why":"Adjusted R² rescales the same two sums of squares."},
           {"id":"p2","name":"Degrees of freedom n − k and n − 1","why":"Adjusted R² divides by exactly these."},
           {"id":"p3","name":"Nested models","why":"The F test applies only to them."},
           {"id":"p4","name":"F in terms of R²","why":"The nested F is the same formula applied to the change in R²."}],
 "traps":["Forgetting to subtract from 1 in adjusted R² (0.49 for 0.51).",
          "Counting only the slopes in k, so n − k becomes n − k − 1.",
          "Reading a rise in adjusted R² as significance.",
          "Comparing R² across models with different dependent variables.",
          "Comparing a no-intercept R² with an ordinary one."],
 "revision":{
   "sheet":["R² = 1 − RSS/TSS; never falls when a regressor is added.",
            "Adjusted R² = 1 − (1 − R²)(n − 1)/(n − k); below R² when k > 1; can be negative.",
            "Negative when R² < (k − 1)/(n − 1): for n = 20, k = 6 the threshold is 0.2632.",
            "n = 50, k = 5, R² = 0.55 gives 0.51 (the Q9 variant).",
            "Adjusted R² rises exactly when |t| of the added coefficient exceeds 1.",
            "Nested F = [(RSS_r − RSS_f)/q]/[RSS_f/(n − k_f)]; example 5.473 against 3.634.",
            "AIC = n ln(RSS/n) + 2k; BIC = n ln(RSS/n) + k ln n; smaller wins; BIC heavier for n ≥ 8.",
            "Cp = RSS_p/σ̂² − (n − 2p); near p for a good subset. Example 10.95 against p = 2.",
            "No-intercept R² uses Σy²; centred it is −2.03 in the example, 0.9227 as reported."],
   "cards":[["Adjusted R²","1 − (1 − R²)(n − 1)/(n − k)"],["Adjusted R² rises when","|t| of the added coefficient > 1"],["Adjusted R² negative when","R² < (k − 1)/(n − 1)"],["BIC vs AIC penalty","ln n vs 2; BIC heavier for n ≥ 8"],["Nested F","[(RSS_r − RSS_f)/q] / [RSS_f/(n − k_f)]"],["Mallows Cp target","Cp ≈ p"]],
   "tricks":["Slopes only is the wrong k; k counts the intercept too.","Check an adjusted R² against R²: it must be a little smaller.","Smaller AIC or BIC wins."],
   "shortcuts":["19/14 = 1.357, 49/45 = 1.089.","ln 8 = 2.079 is where BIC overtakes AIC.","(k − 1)/(n − 1) is the R² below which adjusted R² is negative."],
   "remember":["R² cannot choose a model.","Compare only models with the same dependent variable."]},
 "howto":"If short of time, the lesson is scenes 4 (formulas), 5 (the worked comparison) and 9 (the Q9 variant). Skip the extension. It deliberately does not cover multicollinearity (6.5), dummy variables (6.11), cross-validation or stepwise search.",
 "refs":[{"title":"Econometrics","where":"Chapter 28, Model Selection","site":"Bruce Hansen","url":"","type":"Free online textbook","free":True,"checked":"2026-11-06","why":"AIC, BIC and adjusted R², scenes 3 and 7."},
         {"title":"Applied Regression Analysis","where":"Chapter 15, Selecting the best regression","site":"Draper and Smith","url":"","type":"Textbook","free":False,"checked":"2026-11-06","why":"Mallows Cp and adjusted R², scene 3."},
         {"title":"Introductory Econometrics","where":"Chapter 6, Section 6.3","site":"Jeffrey Wooldridge","url":"","type":"Textbook","free":False,"checked":"2026-11-06","why":"The adjusted R² and its interpretation, scenes 3 and 8."}],
 "mastery":{"minQ":10,"pass":80,"draw":10,"fmtMin":{"numeric":70,"multi":70},
            "diffMix":{"easy":3,"moderate":5,"hard":2},"noHints":True,"retestDays":7,
            "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on "
                   "numerical and multi-statement items, answered without hints. Each paper is "
                   "drawn to the mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style "
                   "paper; NTA publishes no official difficulty split."},
 "provenance":"Anchor: the Q9 variant bank (adjusted R² from n = 50, k = 5, R² = 0.55; adding an irrelevant regressor; adjusted R² can be negative; high R² with insignificant t values). Q9 itself is the F statistic and is taught in topic 6.3. Verified by computing in verify_regression_t1_t4.py: the variant answer 0.51 and its wrong forms (0.49 without the subtraction, 0.4989 with k read as slopes only); the five-student adjusted R² 0.4667 and its wrong forms 0.2 and 0.7; the negative case 0.1, n = 20, k = 6 giving −0.2214 and the threshold 5/19 = 0.2632; the 20-observation comparison: R² 0.8754 and 0.9260, adjusted R² 0.8685 and 0.9121, nested F 1828/334 = 5.473 against 3.634 and its R² form, AIC 126.19 and 119.76, BIC 128.18 and 123.74, Cp 10.95 and 4; ln 8 = 2.079 and ln 7 = 1.946; the no-intercept data giving 0.9227 uncentred, −2.031 centred and 0.9868 with an intercept. The rules 'R² never falls' and 'adjusted R² rises exactly when |t| > 1' were checked on 4000 random data sets each with no exception, and the transfer case (R² 0.5 to 0.5192, adjusted 0.4412 to 0.4291) by closed form. Bank defects: several variant stems end with the next question's text in the explanation field, and j26v-q09-02 mistypes 'F-statistic'; keys were rechecked against the formulas. Scope: the F statistic for all slopes is topic 6.3; multicollinearity is 6.5.",
 "scenes":S}

def q(i, fmt, diff, stem, opts, ans, exp, **kw):
    d = {"id":"regression-t4-m-%02d"%i, "format":fmt, "topic":"regression-t4",
         "diff":diff, "stem":stem, "options":opts, "answer":ans, "explanation":exp}
    d.update(kw); return d

def verd(a,b,c,dd):
    return {"A":{"tf":a[0],"why":a[1]},"B":{"tf":b[0],"why":b[1]},
            "C":{"tf":c[0],"why":c[1]},"D":{"tf":dd[0],"why":dd[1]}}

I = []
I.append(q(1,"numeric","easy","With n = 50, k = 5 (parameters including the intercept) and R² = 0.55, the adjusted R² is:",
  ["0.51","0.49","0.45","0.55"],"A",
  "R̄² = 1 − (1 − R²)(n − 1)/(n − k) = 1 − 0.45 × 49/45 = 1 − 0.49 = 0.51. The value 0.49 is the adjusted unexplained share, 0.45 is 1 − R², and 0.55 is R² itself.",
  check="Adjusted R² must lie below R² = 0.55, and with n large against k it must be only slightly below, which rules out 0.45 and 0.49."))
I.append(q(2,"single","easy","Adding an irrelevant regressor to a linear model with an intercept will:",
  ["leave R² unchanged or increase it","decrease R²","decrease the residual sum of squares to zero","always increase the adjusted R²"],"A",
  "Least squares can set the new coefficient to zero, so the residual sum of squares cannot rise and R² cannot fall. Adjusted R² can fall, and RSS reaches zero only when the model fits perfectly."))
I.append(q(3,"single","easy","The adjusted R² can be:",
  ["negative","greater than 1","equal to n","undefined for every model"],"A",
  "When R² is below (k − 1)/(n − 1) the adjustment pushes the value below zero. It cannot exceed 1, since the unexplained share is non-negative."))
I.append(q(4,"single","easy","A very high R² together with individually insignificant t statistics suggests:",
  ["multicollinearity","autocorrelation","heteroscedasticity","a specification error in the dependent variable"],"A",
  "Collinear regressors jointly explain y well, so R² and the overall F are high, while each coefficient has an inflated standard error and a small t. Autocorrelation and heteroscedasticity do not produce this pattern."))
I.append(q(5,"single","easy","In a linear model with an intercept, R² has which of these properties?",
  ["It lies between 0 and 1","It can exceed 1","It always falls when a regressor is added","It is unaffected by the number of regressors"],"A",
  "R² = 1 − RSS/TSS with 0 ≤ RSS ≤ TSS when the intercept is present. It never falls when a regressor is added, and it generally rises with the number of regressors."))
I.append(q(6,"numeric","easy","For the five points x = 1, 2, 3, 4, 5, y = 2, 4, 5, 4, 5, the fitted line has R² = 0.6. The adjusted R² (n = 5, k = 2) is:",
  ["0.47","0.20","0.70","0.60"],"A",
  "R̄² = 1 − 0.4 × 4/3 = 1 − 0.5333 = 0.4667. Using n − k − 1 = 2 as the divisor gives 0.20, and inverting the ratio gives 0.70.",
  check="Adjusted R² must be below R² = 0.6 and, with n = 5, noticeably below; the value 0.60 is ruled out."))
I.append(q(7,"single","moderate","Adding one regressor raises the adjusted R² exactly when the absolute value of its t statistic is:",
  ["greater than 1","greater than 2","greater than 1.96","greater than 0.5"],"A",
  "R̄² = 1 − s²/s_y² rises exactly when s² falls, and s² falls exactly when t² > 1. Significance at 5% needs |t| near 2 and is a stricter requirement."))
I.append(q(8,"numeric","moderate","With n = 20, k = 6 and R² = 0.10, the adjusted R² is:",
  ["−0.22","0.10","0.22","−0.10"],"A",
  "R̄² = 1 − 0.9 × 19/14 = 1 − 1.2214 = −0.2214. The threshold (k − 1)/(n − 1) = 5/19 = 0.263 is above R² = 0.10, so the answer must be negative.",
  check="R² = 0.10 is below (k − 1)/(n − 1) = 0.263, so the adjusted value is negative; this rules out 0.10 and 0.22."))
I.append(q(9,"numeric","moderate","Two nested models with n = 20 have RSS = 9000 (k = 2) and RSS = 5344 (k = 4). The F statistic for the two added coefficients is:",
  ["5.47","10.95","0.18","3.63"],"A",
  "F = [(9000 − 5344)/2]/[5344/16] = 1828/334 = 5.47. Forgetting to divide by q = 2 gives 10.95, inverting the ratio gives 0.18, and 3.63 is the critical value rather than the statistic.",
  check="The numerator average, 1828, is about 5.5 times the denominator average, 334, so F lies between 5 and 6."))
I.append(q(10,"single","moderate","Compared with AIC, the BIC penalty for each additional parameter is:",
  ["larger once n ≥ 8, since ln n exceeds 2","always smaller","identical for every n","larger only when n < 8"],"A",
  "AIC adds 2 per parameter and BIC adds ln n, and ln 8 = 2.079 exceeds 2 while ln 7 = 1.946 does not. BIC therefore favours smaller models at all but tiny sample sizes."))
I.append(q(11,"multi","moderate","Regarding R² and adjusted R² in a linear model with an intercept.",
  ["A, B and D only","A, B and C only","B, C and D only","A, B, C and D"],"A",
  "R² never falls on adding a regressor, adjusted R² never exceeds R², and adjusted R² can be negative. Comparing R² across different dependent variables is invalid.",
  statements=["R² never decreases when a regressor is added","Adjusted R² never exceeds R²","R² can be used to compare a regression of y with a regression of ln y","Adjusted R² can be negative"],
  verdicts=verd((True,"The new coefficient can be set to zero."),
                (True,"R̄² = 1 − (1 − R²)(n − 1)/(n − k) and (n − 1)/(n − k) ≥ 1."),
                (False,"The totals TSS differ because the dependent variables differ."),
                (True,"When R² < (k − 1)/(n − 1)."))))
I.append(q(12,"single","moderate","A regression through the origin reports R² = 0.9227 while the same data with an intercept give 0.9868. The reported figure for the first model:",
  ["uses Σy² as the total, so it is not comparable with the second","proves that the model without an intercept fits better","must be wrong software output","is the correlation between x and y"],"A",
  "Without an intercept the software measures RSS against Σy², not the total about the mean. The two figures use different denominators."))
I.append(q(13,"numeric","moderate","In the comparison with n = 20, TSS = 72214, the larger model has k = 4 and RSS = 5344 (R² = 0.926). Its adjusted R² is:",
  ["0.91","0.93","0.87","0.89"],"A",
  "R̄² = 1 − (5344/16)/(72214/19) = 1 − 334/3800.7 = 0.9121. The value 0.93 is the R² rounded and 0.87 is the smaller model's adjusted R².",
  check="Adjusted R² must be below R² = 0.926, which rules out 0.93."))
I.append(q(14,"single","moderate","For a subset regression with little omitted-variable bias, Mallows' Cp is expected to be:",
  ["close to the number of parameters p","close to zero","close to n","far above p"],"A",
  "Cp estimates the standardised total error of the subset model. Without bias its expected value is about p. A Cp far above p signals omitted variables."))
I.append(q(15,"single","moderate","Two models for the same dependent variable have AIC values of 119.76 and 126.19. The preferred model is:",
  ["the one with AIC 119.76","the one with AIC 126.19","neither, because AIC needs nested models","the one with the larger R² in all cases"],"A",
  "A smaller AIC is better, and AIC can compare non-nested models for the same y. The larger-R² model need not have the smaller AIC, because AIC charges for parameters."))
I.append(q(16,"multi","moderate","On comparing regression models.",
  ["A, B and D only","A and B only","B, C and D only","A, B, C and D"],"A",
  "The nested F needs nested models, AIC and BIC apply to non-nested models for the same y, and BIC's heavier penalty tends to pick smaller models. R² cannot pick the smallest model, since it never falls with more regressors.",
  statements=["The nested F test requires one model to be a restricted version of the other","AIC and BIC can compare non-nested models with the same dependent variable","Maximising R² picks the smallest adequate model","BIC's larger penalty tends to favour smaller models than AIC does"],
  verdicts=verd((True,"The test is built on the drop in RSS from restrictions."),
                (True,"They need only the likelihood and the number of parameters."),
                (False,"R² never falls with extra regressors, so maximising it picks the largest model."),
                (True,"ln n exceeds 2 once n ≥ 8."))))
I.append(q(17,"numeric","hard","With the 20-observation data, the restricted model (k = 2, RSS = 9000) has Mallows' Cp, using σ̂² = 5344/16 = 334 from the full model, equal to:",
  ["10.95","26.95","16","2"],"A",
  "Cp = RSS_p/σ̂² − (n − 2p) = 9000/334 − (20 − 4) = 26.95 − 16 = 10.95. The value 26.95 omits the correction, and p = 2 is the target for an unbiased model.",
  check="A Cp near p = 2 would indicate no bias. The value 10.95 is far above it, agreeing with the significant F."))
I.append(q(18,"numeric","hard","A simple regression with n = 1000 has R² = 0.01. The adjusted R² to four decimals is:",
  ["0.0090","0.0100","0.0010","−0.0090"],"A",
  "R̄² = 1 − 0.99 × 999/998 = 1 − 0.99100 = 0.0090. With n this large the adjustment is small, but it does reduce the figure slightly.",
  check="Adjusted R² must be a little below R² = 0.01, so it cannot equal 0.0100 and cannot be negative."))
I.append(q(19,"numeric","hard","The AIC of the restricted model is 126.19 and of the full model 119.76, with the same dependent variable. The AIC difference is:",
  ["6.43","3.22","12.85","2.00"],"A",
  "126.19 − 119.76 = 6.43. Doubling gives 12.85 and halving gives 3.22. A difference above about 6 is usually read as strong support for the lower-AIC model.",
  check="The difference must equal the gap between the two AIC values given, a little over 6."))
I.append(q(20,"numeric","hard","For y = 10, 12, 13, 15, 16 on x = 1..5, the line through the origin has slope 3.8727. Measured against the total about the mean, its R² is:",
  ["−2.03","0.92","0.99","−0.92"],"A",
  "RSS about the origin line is far larger than TSS about the mean, so 1 − RSS/TSS is −2.031. The reported 0.9227 uses Σy² as the total, and 0.99 is the R² of the model with an intercept.",
  check="A line forced through the origin through data far from the origin fits worse than a horizontal line at the mean, so the centred R² must be negative."))

LET = "ABCD"
_r = random.Random(20260613); PAT = list("ABCD" * 5); _r.shuffle(PAT)
WANT = {"regression-t4-m-%02d" % (i + 1): PAT[i] for i in range(20)}

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

POOLD = {"moduleId":"regression","topicId":"regression-t4","source":"mastery",
         "label":"R², adjusted R² and model comparison — mastery test (unseen)","count":len(I),"items":I}

os.makedirs("seed", exist_ok=True)
with io.open(OUT,"w",encoding="utf-8") as f:  json.dump(LES,f,ensure_ascii=False,indent=1)
with io.open(POOL,"w",encoding="utf-8") as f: json.dump(POOLD,f,ensure_ascii=False,indent=1)
print("wrote %s: %d scenes (%d core), estMin %d"%(OUT,len(S),len(CORE),LES["estMin"]))
print("wrote %s: %d items"%(POOL,len(I)))
