# Evidence map — Unit III, Design of Experiments, Topic 3B.8

- Topic: design-t8, Connectedness and orthogonality of block designs.
- No official PYQ is claimed; mastery items are original practice.
- Connectedness: all v−1 independent treatment contrasts are estimable after eliminating block effects.
- Treatment concurrence graph: treatments are vertices; an edge joins treatments occurring together in a block. One connected component is equivalent to connectedness under the standard incidence model.
- Adjusted treatment information matrix: C=R−NK⁻¹N′. Connected iff rank(C)=v−1; for c components, rank(C)=v−c.
- Orthogonality: centred contrast spaces have zero cross-products. Complete RBD treatment contrasts are orthogonal to block contrasts; Latin-square treatment contrasts are orthogonal to row and column contrasts.
- Connectedness, pair balance and orthogonality are distinct properties.
- verify_design_t8.py checks graph reachability, rank identities and BIBD concurrence-graph edge count; lesson_design_t8.py checks lesson and mastery contracts.
