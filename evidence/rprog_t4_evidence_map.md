# R Programming T4 — Evidence map

## Scope
Matrix construction, column-major filling, dimensions, indexing, element-wise arithmetic, matrix multiplication, transpose, determinant, inverse/linear systems, diagonal and row/column summaries.

## Primary references
- R Core Team, matrix(): https://stat.ethz.ch/R-manual/R-devel/library/base/html/matrix.html
- R Core Team, matrix multiplication: https://stat.ethz.ch/R-manual/R-devel/library/base/html/matmult.html
- R Core Team, solve(): https://stat.ethz.ch/R-manual/R-devel/library/base/html/solve.html

## Claim-to-evidence map
| Claim | Source | Validation |
|---|---|---|
| matrix() fills by columns unless byrow=TRUE | Base R matrix documentation | Lesson examples and verifier |
| A[i,j] is row then column; drop=FALSE preserves dimensions | Base R matrix documentation | Structural checks |
| * is element-wise; %*% is matrix product | Base R matrix operator documentation | Mastery items |
| Matrix product requires matching inner dimensions | Base R matrix multiplication semantics | Dimension examples |
| t(), det(), solve() semantics | Base R linear algebra documentation | Worked examples and mastery |
| diag(), rowSums(), colSums() | Base R matrix and summary functions | Mastery examples |

## Calculation audit
- A=[[1,2],[3,4]], B=[[2,0],[1,2]]: A%*%B=[[4,4],[10,8]].
- A*B=[[2,0],[3,8]] (elementwise).
- det([[2,1],[3,2]])=4−3=1.
- A(3×2)%*%B(2×4) has dimension 3×4 and 12 entries.
