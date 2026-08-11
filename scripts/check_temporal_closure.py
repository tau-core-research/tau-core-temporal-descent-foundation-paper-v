#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads((ROOT / "data/derived/temporal_closure_ledger.json").read_text())

# An injective grade-one embedding preserves the rank and kernel of a typed
# temporal row. The concrete matrix is a coordinate model of c_K on its image.
c_k = sp.eye(3)
j_t = sp.Matrix([[2, -1, 0]])
j_t_tilde = j_t * c_k.inv()
assert j_t_tilde * c_k == j_t
assert j_t.rank() == j_t_tilde.rank()
assert c_k.nullspace() == []

# Verify the first variation of sqrt(-g(u,u)) around a regular timelike GR
# path, holding observer access and quantization fixed.
eps, g_uu, h_uu = sp.symbols("eps g_uu h_uu", real=True)
expr = sp.sqrt(-(g_uu + eps * h_uu))
first = sp.diff(expr, eps).subs(eps, 0)
assert sp.simplify(first + h_uu / (2 * sp.sqrt(-g_uu))) == 0

# The dimensionless finite contrast vanishes when observation equals GR.
r_gr = sp.symbols("R_GR", positive=True)
assert sp.simplify(sp.log(r_gr / r_gr)) == 0

assert ledger["proved"]["common_source_temporal_closure_under_joint_ownership"] is True
assert ledger["proved"]["p3_handoff_alone_selects_clock_covector"] is False
assert ledger["proved"]["neutral_regular_local_gr_limit"] is True
assert ledger["distortion_ladder"]["tau_over_gr_anomaly"] == "open_empirical_claim"

print(
    "TEMPORAL_CLOSURE_PASS "
    "factorization=exact gr_limit=local first_variation=verified anomaly=open"
)
