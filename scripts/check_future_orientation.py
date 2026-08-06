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
assert ledger["joint_character_weights"] == {
    "length": 1,
    "clock": 1,
    "action": 2,
    "hbar": 2,
    "c": 0,
    "conditional_gravity_ratio": 0,
}
print("FUTURE_ORIENTATION_PASS timelike_current=true common_packet=conditional sign_pair=degenerate seed_type=no_go")
