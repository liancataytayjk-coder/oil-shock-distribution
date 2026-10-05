"""Draw the paper figures from output/tables/estimates.csv.

Writes PNG (200 dpi) and PDF versions to output/figures/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "output" / "tables"
FIG = ROOT / "output" / "figures"

BLUE, ORANGE = "#2a78d6", "#eb6834"  # categorical slots 1-2 (dataviz reference palette)
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "legend.frameon": False, "figure.dpi": 100,
})


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", metadata={"CreationDate": None})  # byte-stable reruns
    plt.close(fig)


def irf(ax, q, color, label=None):
    ax.fill_between(q.h, q.lo, q.hi, color=color, alpha=0.15, linewidth=0)
    ax.plot(q.h, q.beta, color=color, linewidth=2, marker="o", markersize=3.5, label=label)
    ax.axhline(0, color=INK2, linewidth=0.8)
    ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel("Months after the shock")


def pick(est, rq, spec, outcome, cum=True, term="shock"):
    q = est[(est.rq == rq) & (est.spec == spec) & (est.outcome == outcome)
            & (est.cumulative == cum) & (est.term == term)]
    return q.sort_values("h")


def fig1(est):
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    a = pick(est, "RQ1", "baseline", "d_cpi_all")
    b = pick(est, "RQ1", "baseline", "d_cpi_b30")
    irf(ax, a, BLUE, "All-income CPI")
    irf(ax, b, ORANGE, "Bottom-30% CPI")
    ax.set_ylabel("Cumulative response (pp per 1 pp fuel)")
    ax.legend(loc="lower right")
    ax.set_title("Figure 1. Pass-through of fuel prices to the price level", loc="left", color=INK, fontsize=10)
    save(fig, "fig1_rq1_passthrough")


def fig2(est):
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.2), sharey=True)
    for ax, (rq, spec, title) in zip(axes, [("RQ2", "baseline", "National"),
                                            ("RQ4", "pooled", "17-region panel")]):
        irf(ax, pick(est, rq, spec, "d_ratio"), BLUE)
        ax.set_title(title, loc="left", color=INK, fontsize=9)
    axes[0].set_ylabel("Cumulative response of\nln(CPI all / CPI bottom 30%)")
    axes[0].annotate("Below 0: prices of the bottom 30% rise more", xy=(0.2, -0.038), fontsize=8, color=INK2)
    fig.suptitle("Figure 2. Distributional effect of a 1 pp fuel price increase", x=0.02, ha="left",
                 color=INK, fontsize=10)
    fig.tight_layout()
    save(fig, "fig2_rq2_rq4_ratio")


def fig3(est):
    dec = pd.read_csv(TAB / "rq3_gap_decomposition.csv", dtype={"coicop": str})
    # Financial services (weight 0.03% / 0.0003%) is reported in the table only.
    dec = dec[dec.coicop != "12"].sort_values("beta")
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    y = range(len(dec))
    ax.errorbar(dec.beta, y, xerr=1.645 * dec.se, fmt="o", color=BLUE, ecolor=BLUE, elinewidth=1.5,
                markersize=5, capsize=0)
    ax.set_yticks(list(y), [f"{d}  ({w:.0f}% / {b:.0f}%)" for d, w, b in zip(dec.division, dec.w_all, dec.w_b30)])
    ax.axvline(0, color=INK2, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Cumulative response after 12 months (pp per 1 pp fuel), 90% CI")
    ax.set_title("Figure 3. Pass-through by CPI division\n(basket weight: all-income / bottom 30%)",
                 loc="left", color=INK, fontsize=10)
    save(fig, "fig3_rq3_components")


def forest(ax, rows, title):
    rows = rows[::-1]
    y = range(len(rows))
    ax.errorbar([r[1] for r in rows], y, xerr=[1.645 * r[2] for r in rows], fmt="o", color=BLUE,
                ecolor=BLUE, elinewidth=1.5, markersize=5, capsize=0)
    ax.set_yticks(list(y), [r[0] for r in rows])
    ax.axvline(0, color=INK2, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.set_title(title, loc="left", color=INK, fontsize=9)


def fig4(est):
    c = est[est.cumulative & (est.h == 12)]
    rows = [("Pooled (all regions)", *c[(c.rq == "RQ4") & (c.spec == "pooled")][["beta", "se"]].iloc[0])]
    for g, lab in [("high_poverty", "High poverty"), ("high_food", "High food share"),
                   ("mindanao", "Mindanao"), ("island", "Island regions")]:
        r = c[(c.spec == f"x {g}") & (c.term == f"shock_x_{g}")][["beta", "se"]].iloc[0]
        rows.append((f"{lab}: extra effect", *r))
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    forest(ax, rows, "Figure 4. Regional differences in the gap, 12 months (90% CI)")
    ax.set_xlabel("Cumulative response of ln(CPI all / CPI bottom 30%)")
    save(fig, "fig4_rq4_groups")


def fig5(est):
    c = est[est.cumulative & (est.h == 6) & (est.term == "shock") & (est.outcome == "d_ratio")]
    get = lambda rq, spec: c[(c.rq == rq) & (c.spec == spec)][["beta", "se"]].iloc[0]  # noqa: E731
    rows = [("Baseline, national", *get("RQ2", "baseline")), ("Baseline, regional panel", *get("RQ4", "pooled"))]
    for spec, lab in [("a dubai crude php", "Dubai crude in pesos"), ("b macro controls", "FX, policy rate, FAO"),
                      ("c p=6", "6 lags"), ("c p=18", "18 lags"), ("d excl 2020", "Excluding 2020"),
                      ("d excl 2026", "Excluding 2026"), ("e splice dummies", "Base-change dummies"),
                      ("g to Jun 2019", "Paper's window (to Jun 2019)"),
                      ("h gasoline 07.2.2.2", "Gasoline index, 2019-"), ("i WB pump price", "World Bank pump price, 2018-25")]:
        rows.append((lab, *get("ROB", spec)))
    for spec, lab in [("national excl 2008", "Excluding 2008, national*"),
                      ("regional excl 2008", "Excluding 2008, regional*"),
                      ("regional 2001-2012", "Regional, 2001-2012*"), ("regional 2013-", "Regional, 2013-2026*")]:
        rows.append((lab, *get("RQ3b", spec)))
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    forest(ax, rows, "Figure 5. Robustness of the distributional effect, 6 months (90% CI)")
    ax.set_xlabel("Cumulative response of ln(CPI all / CPI bottom 30%)\n* exploratory, added after the first run")
    save(fig, "fig5_robustness")


def fig6():
    e1 = pd.read_csv(TAB / "e1_national_2026.csv", parse_dates=["date"])
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.2), sharey=True)
    for ax, (series, title) in zip(axes, [("cpi_all", "All-income CPI"), ("cpi_b30", "Bottom-30% CPI")]):
        q = e1[e1.series == series]
        m = q.date.dt.strftime("%b")
        ax.plot(m, q.actual, color=BLUE, linewidth=2, marker="o", markersize=3.5, label="Actual")
        ax.fill_between(m, q.lo, q.hi, color=ORANGE, alpha=0.15, linewidth=0)
        ax.plot(m, q.beta, color=ORANGE, linewidth=2, linestyle="--", marker="o", markersize=3.5,
                label="Fuel-driven (pre-2026 model)")
        ax.axhline(0, color=INK2, linewidth=0.8)
        ax.set_title(title, loc="left", color=INK, fontsize=9)
        ax.set_xlabel("2026")
    axes[0].set_ylabel("Change since Dec 2025 (100 x log points)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.06))
    fig.suptitle("Figure 6. The 2026 shock: actual price rise vs. fuel-driven rise predicted\n"
                 "by a model estimated only on 2001-2025 data", x=0.02, ha="left", color=INK, fontsize=10)
    fig.tight_layout()
    save(fig, "fig6_2026_out_of_sample")


def fig7():
    e5 = pd.read_csv(TAB / "e5_decomposition_2026.csv", dtype={"coicop": str}).set_index("coicop")
    parts = [("Rice and other cereals", e5.loc["01.1.1", "gap_pp"]),
             ("Other food", e5.loc["01.1", "gap_pp"] - e5.loc["01.1.1", "gap_pp"]),
             ("Passenger transport fares", e5.loc["07.3", "gap_pp"]),
             ("Cooking and household fuels", e5.loc["04.5", "gap_pp"]),
             ("Tobacco", e5.loc["02.3", "gap_pp"]),
             ("Own-vehicle fuel", e5.loc["07.2", "gap_pp"]),
             ("Housing rent", e5.loc["04.1", "gap_pp"])]
    known = sum(v for _, v in parts)
    parts.append(("All other items", e5.loc["0", "gap_pp"] - known))
    parts = parts[::-1]
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    vals = [v for _, v in parts]
    ax.barh([n for n, _ in parts], vals, color=[ORANGE if v > 0 else BLUE for v in vals], height=0.6)
    for i, v in enumerate(vals):
        ax.text(v + (0.03 if v >= 0 else -0.03), i, f"{v:+.2f}", va="center", ha="left" if v >= 0 else "right",
                fontsize=8, color=INK2)
    ax.axvline(0, color=INK2, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(min(vals) - 0.4, max(vals) + 0.4)
    ax.set_xlabel(f"Contribution to the gap (pp); total gap = {e5.loc['0', 'gap_pp']:+.2f} pp\n"
                  "positive: raised the bottom-30% CPI more than the all-income CPI")
    ax.set_title("Figure 7. What made the poor's prices rise faster, Dec 2025-Aug 2026", loc="left",
                 color=INK, fontsize=10)
    save(fig, "fig7_2026_gap_decomposition")


if __name__ == "__main__":
    est = pd.read_csv(TAB / "estimates.csv")
    for f in (fig1, fig2, fig3, fig4, fig5):
        f(est)
    fig6()
    fig7()
    print("figures written to", FIG)
