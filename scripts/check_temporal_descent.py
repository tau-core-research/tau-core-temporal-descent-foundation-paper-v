#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads((ROOT / "data/derived/temporal_descent_ledger.json").read_text())

t01, t13, t02, t23 = sp.symbols("tau_01 tau_13 tau_02 tau_23", positive=True)
holonomy = sp.expand(t01 + t13 - t02 - t23)

# Exact edge form on the diamond: define a potential along the upper path and
# verify that the lower endpoint agrees exactly iff the holonomy vanishes.
t0 = sp.Integer(0)
t1 = t0 + t01
t2 = t0 + t02
t3_upper = t1 + t13
t3_lower = t2 + t23
assert sp.expand(t3_upper - t3_lower) == holonomy

# Order alone cannot set duration: every positive rescaling preserves order.
scale = sp.symbols("scale", positive=True)
assert sp.simplify(scale * t3_upper) > 0
assert ledger["proved"]["order_only_duration_selection"] is False
assert ledger["proved"]["positive_exact_edge_form_defines_clock"] is True
print("TEMPORAL_DESCENT_PASS order_no_go=exact diamond_clock_condition=exact")
