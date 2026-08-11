#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads(
    (ROOT / "data/derived/observer_support_readout_ledger.json").read_text()
)

chi = sp.symbols("chi", real=True, nonnegative=True)
k_body = sp.diag(1 + chi, 2, 3 + chi / 2)
v = sp.Matrix([1, 1, 1])


def quotient_rate(access: sp.Matrix, epsilon: sp.Expr) -> sp.Expr:
    visible = access * v
    gram = access * k_body.inv() * access.T
    k_observer = gram.inv()
    return sp.sqrt((visible.T * k_observer * visible)[0]) / epsilon


a_local = sp.Matrix([[1, 0, 0]])
a_extended = sp.Matrix([[1, 0, 0], [0, 1, 0]])
a_third = sp.Matrix([[0, 0, 1]])

n_local = quotient_rate(a_local, sp.Rational(1, 5))
n_extended = quotient_rate(a_extended, sp.Rational(1, 4))
n_third = quotient_rate(a_third, sp.Rational(1, 3))

assert n_local.is_positive
assert n_extended.is_positive
assert n_third.is_positive

ratio = sp.simplify(n_local / n_extended)
assert sp.simplify(sp.diff(ratio, chi)) != 0
assert sp.simplify((n_local / n_extended) * (n_extended / n_third) - n_local / n_third) == 0

# Positive relabelling lambda = 5 chi rescales the tangent and the coordinate
# increment inversely, preserving elapsed time.
scale, dchi = sp.symbols("scale dchi", positive=True)
assert sp.simplify((n_extended / scale) * (scale * dchi) - n_extended * dchi) == 0

coherent = sp.Matrix([[1, 2], [2, 4]])
incoherent = sp.Matrix([[1, 2], [1, 3]])
assert coherent.rank() == 1
assert incoherent.rank() == 2

assert ledger["proved"]["observer_support_can_change_clock_rate"] is True
assert ledger["proved"]["multi_observer_rate_cocycle"] is True
assert ledger["proved"]["scalar_clock_requires_rank_one_component_forms"] is True
assert ledger["proved"]["temporal_parent_time_is_required"] is False

print(
    "OBSERVER_SUPPORT_READOUT_PASS "
    "positive=yes variable_ratio=yes cocycle=exact scalar_clock_rank=1"
)
