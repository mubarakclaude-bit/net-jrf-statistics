# R Programming T6 — Evidence map

## Scope
Summary functions, NA propagation, na.rm, is.na, NA/NaN/Inf distinctions, vector length and observed/missing counts.

## Primary references
- R Core Team, NA and NaN: https://stat.ethz.ch/R-manual/R-devel/library/base/html/NA.html
- R Core Team, mean(): https://stat.ethz.ch/R-manual/R-devel/library/base/html/mean.html
- R Core Team, Summary functions: https://stat.ethz.ch/R-manual/R-devel/library/base/html/summary.html

## Claim-to-evidence map
| Claim | Source | Validation |
|---|---|---|
| na.rm omits missing values for a calculation | Base R summary docs | Worked and mastery examples |
| is.na detects NA and NaN | Base R NA docs | Mastery checks |
| length includes missing positions | Base R length semantics | Count examples |
| Inf is not removed by na.rm | Base R missing-value semantics | Trap check |
| mean, median and range have distinct meanings | Base R summary docs | Worked calculations |
