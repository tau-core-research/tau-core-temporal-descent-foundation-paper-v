#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads((ROOT / "data/derived/future_orientation_ledger.json").read_text())

f, omega, sigma, lapse = sp.symbols("f omega sigma lapse", positive=True)
j_t = 2 * f**2 * omega / (sigma**2 * lapse)
g_tt = -(sigma**2 * lapse)
j_sq = sp.simplify(g_tt * j_t**2)

assert j_sq == -4 * f**4 * omega**2 / (sigma**2 * lapse)
assert sp.simplify(j_sq.subs(omega, -omega) - j_sq) == 0
assert sp.simplify(j_t.subs(omega, -omega) + j_t) == 0

# Positive amplitude rescaling cancels after unit normalization.
c = sp.symbols("c", positive=True)
unit_sign = sp.simplify(j_t / sp.sqrt(-j_sq))
scaled_unit_sign = sp.simplify((c**2 * j_t) / sp.sqrt(-(c**4 * j_sq)))
assert sp.simplify(unit_sign - scaled_unit_sign) == 0
assert ledger["proved"]["current_parent_selects_one_frequency_sign"] is False

# A selected signed body reference compares with the current, but the
# charge-even energy cannot select the relative sign.
a, j = sp.symbols("a j", real=True, nonzero=True)
relative_pair = (a * j, a * (-j))
assert relative_pair[0] == -relative_pair[1]
assert sp.expand(j**2 - (-j)**2) == 0
assert ledger["proved"]["conditional_common_clock_flow_packet_exists"] is True
assert ledger["proved"]["current_seed_scalar_supplies_causal_sign_line"] is False

# Endpoint frequency transfer is invariant under the connected diagonal
# orientation reversal, but not under a one-ended reversal.
u_s, u_o, k_s, k_o = sp.symbols("u_s u_o k_s k_o", nonzero=True, real=True)
ratio = sp.simplify((u_s * k_s) / (u_o * k_o))
ratio_diag = sp.simplify(((-u_s) * (-k_s)) / ((-u_o) * (-k_o)))
ratio_one_end = sp.simplify(((-u_s) * k_s) / (u_o * k_o))
assert sp.simplify(ratio_diag - ratio) == 0
assert sp.simplify(ratio_one_end + ratio) == 0
assert ledger["proved"]["relative_clock_ratio_requires_absolute_future_sign"] is False
assert ledger["proved"]["diagonal_global_Z2_is_clock_terminal_null"] is True

# Scalar Fenchel--Young control for the positive contact metric.
v, eta, h = sp.symbols("v eta h", real=True, positive=True)
fenchel_gap = sp.simplify(h * v**2 / 2 + eta**2 / (2 * h) - eta * v)
assert sp.simplify(fenchel_gap - h * (v - eta / h)**2 / 2) == 0
assert ledger["proved"]["ctc_p1_closes_local_handoff_conditionally"] is True
assert ledger["proved"]["current_reduct_entails_ctc_p1"] is False
assert ledger["temporal_mvp_selection"] == "adopts_CTC_P1_as_the_single_enriched_parent_selection_law"
assert ledger["neutral_tau_over_gr_prediction"] == 0
assert ledger["joint_character_weights"] == {
    "length": 1,
    "clock": 1,
    "action": 2,
    "hbar": 2,
    "c": 0,
    "conditional_gravity_ratio": 0,
}
print("FUTURE_ORIENTATION_PASS common_packet=conditional diagonal_Z2=terminal_null CTC=conditional current_reduct=no_go")
