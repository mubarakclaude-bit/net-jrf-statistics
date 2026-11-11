# Evidence map — Unit III, Design of Experiments, Topic 3B.4

- Topic: design-t4, Balanced incomplete block designs and incidence matrices.
- No official PYQ is claimed; mastery items are original practice.
- Parameters: v treatments, b blocks, r replications, k treatments per block, λ pair concurrence.
- Identities: bk=vr and λ(v−1)=r(k−1).
- With N as a v×b treatment-by-block incidence matrix: row sums r, column sums k, NN′=(r−λ)I_v+λJ_v.
- Exact example uses blocks 12,13,14,23,24,34: v=4,b=6,r=3,k=2,λ=1; row sums 3; column sums 2; NN′=2I₄+J₄; bk=12=vr; λ(v−1)=3=r(k−1).
- Parameter identities are necessary arithmetic conditions, not a proof of existence.
- verify_design_t4.py checks the matrix, counts and parameter identities; lesson_design_t4.py checks the lesson contract.
