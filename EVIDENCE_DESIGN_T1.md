# Evidence map — Unit III, Design of Experiments, Topic 3B.1

## Scope and PYQ treatment
- Catalog topic: `design-t1`, “ANOVA tables and degrees of freedom”.
- This lesson covers one-way completely randomised design (CRD) and complete randomised block design (RBD) ANOVA tables.
- No direct June 2026 Paper 2 question is claimed. Questions in the mastery pool are original practice, not official PYQs.
- Factorial ANOVA, Latin squares, incomplete block designs, missing observations and multiple-comparison procedures are out of scope except for boundary notes.

## Formula claims
- Correction factor: CF = G²/N.
- CRD: SS_Total = Σy²−CF; SS_Treatment = ΣTᵢ²/nᵢ−CF; SS_Error = SS_Total−SS_Treatment.
- CRD degrees of freedom: a−1, N−a, N−1.
- Complete RBD: SS_Treatment = ΣTᵢ²/b−CF; SS_Block = ΣBⱼ²/a−CF; SS_Error = SS_Total−SS_Treatment−SS_Block.
- Complete RBD degrees of freedom: a−1, b−1, (a−1)(b−1), ab−1.
- Treatment F statistic: MS_Treatment/MS_Error, with model-appropriate numerator and denominator df.

## Independent arithmetic
- CRD example: treatment totals (30,42,26), G=98, N=12, Σy²=850. CF=800⅓; total SS=149/3; treatment SS=104/3; error SS=15. Treatment/error df=2/9; F=52/5=10.4.
- RBD example: 4 treatments × 3 blocks; G=120, Σy²=1244, CF=1200. Total SS=44; treatment SS=34; block SS=20/3; error SS=10/3. df=(3,2,6,11); treatment F=20.4.
- Transfer example: 3 treatments × 5 shifts; treatment SS=48, error SS=12; df treatment/error=2/8; F=16.

## Assumptions and limits
- CRD one-way fixed-effects model: independent, homoscedastic errors; normality for exact finite-sample F inference.
- Complete RBD model is additive in treatment and block effects. With one observation per cell, treatment-by-block interaction is not separately estimable from error.
- A significant omnibus F establishes that not all treatment means are equal; post-hoc or planned comparisons are needed to identify differences.
- Randomisation supports the design-based basis for inference; block effects are nuisance variation, not additional treatments.

## Verification
- `verify_design_t1.py` uses exact integer/rational calculations to check the worked totals, SS decompositions, df identities and F ratios.
- `lesson_design_t1.py` checks lesson identity, scene sequence, mastery contract, difficulty, format and key distribution.
