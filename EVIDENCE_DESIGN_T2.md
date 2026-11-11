# Evidence map — Unit III, Design of Experiments, Topic 3B.2

## Scope
- Catalog topic: `design-t2`, “CRD, RBD, Latin square”.
- Covers balanced CRD allocation, complete RBD and p×p Latin square layout, ANOVA decomposition and design selection.
- Questions are original practice; no official PYQ is claimed.

## Formula claims
- CRD: treatment df a−1; error df N−a; total df N−1.
- Complete RBD: treatment df a−1; block df b−1; error df (a−1)(b−1); total df ab−1.
- Latin square: rows, columns and treatments each have p−1 df; error df (p−1)(p−2); total df p²−1.
- Latin square SS components use squared row, column and treatment totals divided by p, less CF=G²/p².

## Exact worked-example checks
- RBD: G=123; CF=5043/4; total SS=137/4; treatment SS=25/2; block SS=251/12; error SS=5/6; treatment F=45 with df (2,6).
- Latin square: G=96; CF=1024; total SS=20; row SS=8/3; column SS=8; treatment SS=14/3; error SS=14/3; treatment F=1 with df (2,2).

## Assumptions and limits
- Standard RBD model assumes additive treatment and block effects; with one observation per cell, treatment-by-block interaction is not separately estimable.
- Standard Latin square requires p treatments, p rows and p columns. The additive model does not separately estimate treatment-by-row or treatment-by-column interactions with one observation per cell.
- Randomisation must preserve the layout; arbitrary cell shuffling is invalid.
