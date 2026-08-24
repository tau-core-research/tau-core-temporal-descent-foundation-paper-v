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
assert ledger["proved"]["pulled_back_stable_cell_count_is_reparameterization_invariant"] is True
assert ledger["proved"]["tick_intensity_identifies_parent_front_rate_without_independent_calibration"] is False
assert ledger["proved"]["arbitrarily_many_uncalibrated_observers_identify_parent_front_rate"] is False
assert ledger["proved"]["absolute_proto_rate_is_invariant_without_parent_scale_anchor"] is False
assert ledger["proved"]["source_calibrated_proto_rate_is_reparameterization_invariant"] is True
assert ledger["proved"]["calibrated_order_proves_literal_parent_evolution"] is False
assert ledger["proved"]["clock_mobility_product_is_reparameterization_invariant"] is True
assert ledger["proved"]["calibrated_eocc_proves_literal_parent_evolution"] is False

# The local tick law has an exact reciprocal rate--resolution counterfamily.
nu, transmission, front_rate, c = sp.symbols(
    "nu transmission front_rate c", positive=True
)
intensity = nu * transmission * front_rate
intensity_twin = (nu / c) * transmission * (c * front_rate)
assert sp.simplify(intensity_twin - intensity) == 0

# Any number of observers leaves two common logarithmic scale directions.
for observer_count in range(2, 13):
    jacobian = sp.Matrix.hstack(
        sp.eye(observer_count),
        sp.ones(observer_count, 1),
        sp.ones(observer_count, 1),
    )
    assert jacobian.rank() == observer_count
    assert len(jacobian.nullspace()) == 2

# A source-owned positive one-form removes coordinate relabelling from the
# physical rate, while an unowned common scale remains record-invisible.
kappa, fprime, e = sp.symbols("kappa fprime e", positive=True)
physical_rate = intensity / (nu * transmission * kappa)
physical_rate_relabelled = (intensity / fprime) / (
    nu * transmission * (kappa / fprime)
)
assert sp.simplify(physical_rate_relabelled - physical_rate) == 0
assert sp.simplify(physical_rate / e - physical_rate) != 0

# The coordinate EOCC response and clock density transform oppositely, so
# their physical product and the proto-time current are chart invariant.
gamma_rho = sp.symbols("gamma_rho", positive=True)
gamma_lambda = fprime * gamma_rho
gamma_hat = kappa * gamma_rho
gamma_hat_lambda = (kappa / fprime) * gamma_lambda
coordinate_current = -1 / gamma_rho
coordinate_current_lambda = -1 / gamma_lambda
parent_current = coordinate_current / kappa
parent_current_lambda = coordinate_current_lambda / (kappa / fprime)
assert sp.simplify(gamma_hat_lambda - gamma_hat) == 0
assert sp.simplify(parent_current_lambda - parent_current) == 0

full_anchor_jacobian = sp.Matrix(
    [
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ]
)
assert full_anchor_jacobian.rank() == 4

print(
    "OBSERVER_SUPPORT_READOUT_PASS "
    "positive=yes variable_ratio=yes cocycle=exact scalar_clock_rank=1 "
    "tick_rate_resolution=nonidentifiable calibrated_rate=invariant "
    "eocc_clock_mobility=invariant calibrated_orbit=nonidentifying"
)
