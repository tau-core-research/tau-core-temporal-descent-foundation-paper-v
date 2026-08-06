#!/usr/bin/env python3
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
for directory in [ROOT / "figures", ROOT / "paperV_submission_source/figures"]:
    directory.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(8.4, 4.6))
ax.axis("off")
boxes = [
    (0.04, "Atemporal body\n$M_\\tau$"),
    (0.29, "Observer-source\nresolution $Q_{OS}$"),
    (0.55, "Resolved causal\nquotient $C_O$"),
    (0.80, "Positive path clock\n$d\\tau_{M,\\gamma}$"),
]
for x, label in boxes:
    ax.add_patch(plt.Rectangle((x, 0.55), 0.17, 0.24, facecolor="#e8f0f7", edgecolor="#1f4e79", linewidth=1.5))
    ax.text(x + 0.085, 0.67, label, ha="center", va="center", fontsize=10)
for x in [0.21, 0.46, 0.72]:
    ax.annotate("", xy=(x + 0.07, 0.67), xytext=(x, 0.67), arrowprops=dict(arrowstyle="->", lw=1.6, color="#333333"))
ax.text(0.5, 0.34, "order alone does not determine duration", ha="center", fontsize=11, color="#9b2c2c")
ax.text(0.5, 0.20, "physical open arrow: occupation and future orientation", ha="center", fontsize=11, color="#333333")
fig.tight_layout()
for directory in [ROOT / "figures", ROOT / "paperV_submission_source/figures"]:
    fig.savefig(directory / "fig_temporal_descent_spine.pdf", bbox_inches="tight")
plt.close(fig)

fig, ax = plt.subplots(figsize=(5.8, 4.2))
ax.axis("off")
pos = {"0": (0.12, 0.50), "1": (0.47, 0.80), "2": (0.47, 0.20), "3": (0.84, 0.50)}
edges = [("0", "1", r"$\tau_{01}$"), ("1", "3", r"$\tau_{13}$"), ("0", "2", r"$\tau_{02}$"), ("2", "3", r"$\tau_{23}$")]
for u, v, label in edges:
    ax.annotate("", xy=pos[v], xytext=pos[u], arrowprops=dict(arrowstyle="->", lw=1.6, color="#1f4e79"))
    mx, my = ((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2)
    ax.text(mx, my + (0.04 if my >= 0.5 else -0.04), label, ha="center", va="center", fontsize=10)
for node, (x, y) in pos.items():
    ax.add_patch(plt.Circle((x, y), 0.045, facecolor="white", edgecolor="#222222", linewidth=1.5))
    ax.text(x, y, node, ha="center", va="center", fontsize=10)
ax.text(0.5, 0.03, r"global synchronization: $\tau_{01}+\tau_{13}=\tau_{02}+\tau_{23}$", ha="center", fontsize=10)
fig.tight_layout()
for directory in [ROOT / "figures", ROOT / "paperV_submission_source/figures"]:
    fig.savefig(directory / "fig_clock_diamond.pdf", bbox_inches="tight")
plt.close(fig)
