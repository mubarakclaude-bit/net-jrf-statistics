# Evidence map — Unit VI, 6.3 ANOVA decomposition and overall F test

## Direct official anchor
- June 2026 UGC NET Statistics Paper 2, Q9 (j26-q09).
- The stem asks for the F-test statistic for significance of complete regression excluding the intercept, expressed through R², n and k.
- Official key: B. Response sheet Q114: learner marked A.
- Normalized expression: with k denoting total estimated parameters including the intercept, F=[R²/(k−1)]/[(1−R²)/(n−k)].
- The source scan renders the mathematical expression poorly; this lesson writes the standard algebraically equivalent ratio and makes the k convention explicit.

## Related practice variants
The ten repository variants linked to Q9 are heterogeneous. Relevant ANOVA/F items include F degrees of freedom, F=t² in simple regression, F from an ANOVA table, and the R² definition. Other variants concern adjusted R², multicollinearity and residual variance; they are not treated as direct subtopic evidence for this lesson.

## Mathematical claims
- Corrected TSS=RegSS+RSS for OLS with an intercept.
- Regression df=k−1; residual df=n−k; total df=n−1 when k includes the intercept.
- MSR=RegSS/(k−1); MSE=RSS/(n−k); F=MSR/MSE.
- R²=RegSS/TSS and 1−R²=RSS/TSS, yielding the compact F formula.
- Under the joint null and classical normal-error assumptions, F follows F(k−1,n−k).
- In simple regression, the overall F statistic equals the square of the slope t statistic.

## Verification
Exact rational arithmetic verifies compact F calculations and an ANOVA-table ratio. Mastery pool counts, format mix and balanced answer positions are checked. Mastery questions are original practice; the direct PYQ is identified separately.
