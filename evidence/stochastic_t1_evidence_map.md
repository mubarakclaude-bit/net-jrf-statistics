# Evidence map — Stochastic T1: Markov Chains and Chapman–Kolmogorov

## Scope and examination alignment
- Unit IX — Stochastic Processes; topic `stochastic-t1`.
- Covers discrete-time Markov property, row-stochastic transition matrices, n-step transition probabilities, Chapman–Kolmogorov, row-vector evolution, stationary distributions and absorbing states.
- The lesson uses original worked examples and mastery questions. No June 2026 PYQ is claimed as a direct anchor.

## Claim-to-evidence map
| Claim | Lesson focus | Independent check |
|---|---|---|
| Markov property: the present state screens off the past | Definition and conditional probability | Conceptual mastery item |
| Under the row convention, each row is a probability vector | Transition matrix conditions | Non-negativity and row-sum checks |
| (P^{(n)}) gives n-step transition probabilities | Matrix powers | Exact rational (P^2) and (P^3) |
| (P^{(m+n)}=P^{(m)}P^{(n)}=P^{(n)}P^{(m)}) for powers of the same matrix | Chapman–Kolmogorov | Both matrix products checked exactly |
| Row distribution evolves as αₙ=α₀Pⁿ | Distribution propagation | Row-vector convention item |
| Stationarity means πP=π | Stationary distribution | Exact π=(1/3,2/3) check |
| An absorbing state has a self-transition probability of one | Absorbing-state example | Exact transition-row check |

## Exact numerical anchors
For
[
P=\begin{pmatrix}1/2&1/2\\1/4&3/4\end{pmatrix},
]
[
P^2=\begin{pmatrix}3/8&5/8\\5/16&11/16\end{pmatrix},\qquad
P^3=\begin{pmatrix}11/32&21/32\\21/64&43/64\end{pmatrix}.
]
The stationary row vector is π=(1/3,2/3), satisfying πP=π and summing to one.

## References
- Norris, J. R., *Markov Chains*, Cambridge University Press — Markov property, transition matrices and stationary distributions.
- Ross, S. M., *Introduction to Probability Models* — discrete-time Markov chains and Chapman–Kolmogorov equations.
- Lawler, G. F., *Introduction to Stochastic Processes* — finite-state Markov-chain foundations.

## Limitations
The lesson focuses on finite-state, discrete-time chains and foundational calculations. General state-space chains and advanced recurrence theory are outside this topic's scope.
