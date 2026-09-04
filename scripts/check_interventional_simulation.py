#!/usr/bin/env python3
"""Finite witness for the interventional-simulation theorem in Paper V."""

from itertools import product


def recursive_solution(xi, i0=None, i2=None):
    x0 = xi[0] if i0 is None else i0
    x1 = 2.0 * x0 + xi[1]
    decision = int(x1 >= 0.0)
    x2 = x1 + decision + xi[2] if i2 is None else i2
    return x0, x1, decision, x2


def simultaneous_solution(xi, i0=None, i2=None):
    # A topological solve of the simultaneous local-equation relation.
    x0, x1, decision, x2 = recursive_solution(xi, i0=i0, i2=i2)
    assert x0 - (xi[0] if i0 is None else i0) == 0.0
    assert x1 - (2.0 * x0 + xi[1]) == 0.0
    assert decision == int(x1 >= 0.0)
    assert x2 - (x1 + decision + xi[2] if i2 is None else i2) == 0.0
    return x0, x1, decision, x2


xis = [(-1.0, 0.25, 0.5), (0.5, -0.75, -0.25), (2.0, 1.0, -3.0)]
interventions = [(None, None), (-2.0, None), (3.0, -1.0)]
for xi, (i0, i2) in product(xis, interventions):
    assert recursive_solution(xi, i0, i2) == simultaneous_solution(xi, i0, i2)

# Shared exogenous data preserve the same counterfactual coupling.
for xi in xis:
    recursive_pair = (
        recursive_solution(xi, i0=-1.0),
        recursive_solution(xi, i0=1.0),
    )
    simultaneous_pair = (
        simultaneous_solution(xi, i0=-1.0),
        simultaneous_solution(xi, i0=1.0),
    )
    assert recursive_pair == simultaneous_pair


def bernoulli(p, bit):
    return p if bit else 1.0 - p


def sequential_probability(bits, intervene_x1=None):
    x0, x1, decision, x2 = bits
    p0 = bernoulli(0.4, x0)
    p1 = float(x1 == intervene_x1) if intervene_x1 is not None else bernoulli(0.2 + 0.6 * x0, x1)
    pd = float(decision == x1)  # adaptive decision node
    p2 = bernoulli(0.1 + 0.4 * x0 + 0.3 * decision, x2)
    return p0 * p1 * pd * p2


def factor_graph_probability(bits, intervene_x1=None):
    # The same four source-frozen local factors, now read simultaneously.
    x0, x1, decision, x2 = bits
    factors = [
        bernoulli(0.4, x0),
        float(x1 == intervene_x1)
        if intervene_x1 is not None
        else bernoulli(0.2 + 0.6 * x0, x1),
        float(decision == x1),
        bernoulli(0.1 + 0.4 * x0 + 0.3 * decision, x2),
    ]
    out = 1.0
    for factor in factors:
        out *= factor
    return out


states = list(product((0, 1), repeat=4))
for intervention in (None, 0, 1):
    seq = [sequential_probability(s, intervention) for s in states]
    fac = [factor_graph_probability(s, intervention) for s in states]
    assert all(abs(a - b) < 1e-15 for a, b in zip(seq, fac))
    assert abs(sum(seq) - 1.0) < 1e-15

print(
    "FINITE_INTERVENTIONAL_SIMULATION_PASS "
    "deterministic=yes stochastic=yes adaptive=yes shared_counterfactual=yes"
)
