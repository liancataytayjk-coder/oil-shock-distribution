"""Draw every figure in black and white for print (no colour, serif font, no titles inside the image).

Each figure is written as a 300-dpi PNG and TIFF and as a vector PDF to output/figures/.
Main text: fig01-fig08. Appendix: figA1-figA4.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from config import FIG, REGIONS_17, TAB  # noqa: E402

BLACK, DARK, MID, LIGHT = "0.0", "0.25", "0.55", "0.85"
plt.rcParams.update({
    "font.family": "DejaVu Serif", "font.size": 9, "axes.edgecolor": BLACK, "axes.labelcolor": BLACK,
    "xtick.color": BLACK, "ytick.color": BLACK, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": False, "legend.frameon": False, "figure.dpi": 100, "hatch.linewidth": 0.6,
    "lines.linewidth": 1.4,
})
A = dict(color=BLACK, linestyle="-", marker="o", markersize=3.5, markerfacecolor=BLACK)
B = dict(color=BLACK, linestyle="--", marker="s", markersize=3.5, markerfacecolor="white")
SHORT = {"NCR": "NCR", "CAR": "CAR", "R01": "I", "R02": "II", "R03": "III", "R04A": "IV-A", "R04B": "MIMAROPA",
         "R05": "V", "R06": "VI", "R07": "VII", "R08": "VIII", "R09": "IX", "R10": "X", "R11": "XI",
         "R12": "XII", "R13": "XIII", "BARMM": "BARMM"}


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG / f"{name}.tiff", dpi=300, bbox_inches="tight", pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)


def zero(ax, horizontal=True):
    (ax.axhline if horizontal else ax.axvline)(0, color=BLACK, linewidth=0.6)


def irf(ax, q, style, label=None, band="fill"):
    if band == "fill":
        ax.fill_between(q.h, q.lo, q.hi, color=LIGHT, linewidth=0)
    else:
        for c in ("lo", "hi"):
            ax.plot(q.h, q[c], color=BLACK, linestyle=":", linewidth=0.8)
    ax.plot(q.h, q.beta, label=label, **style)
    zero(ax)
    ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel("Months after the shock")


def pick(est, rq, spec, outcome, cum=True, term="shock", h=None):
    q = est[(est.rq == rq) & (est.spec == spec) & (est.outcome == outcome) & (est.cumulative == cum)
            & (est.term == term)].sort_values("h")
    return q if h is None else q[q.h == h].iloc[0]


def box(ax, x, y, w, h, text, fill="white", size=9, weight="normal", align="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.02",
                                facecolor=fill, edgecolor=BLACK, linewidth=0.9))
    tx = x + w / 2 if align == "center" else x + 0.02
    ax.text(tx, y + h / 2, text, ha=align, va="center", fontsize=size, fontweight=weight, linespacing=1.5)


def arrow(ax, x0, y0, x1, y1, style="-|>", ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=BLACK, linewidth=1.1, linestyle=ls, shrinkA=0, shrinkB=0))


def fig01_conceptual():
    """Conceptual framework: X -> Y."""
    fig, ax = plt.subplots(figsize=(7.4, 2.1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    box(ax, 0.01, 0.20, 0.27, 0.60, "X\n\nRetail fuel price shock\n" r"$f_t = 100\,\Delta\ln F_t$",
        fill=LIGHT, size=9)
    box(ax, 0.42, 0.06, 0.57, 0.88, "Y\n\n"
        r"$Y_1$:  inflation, all income households ($\pi^A_t$)" "\n"
        r"$Y_2$:  inflation, bottom 30% households ($\pi^B_t$)" "\n"
        r"$Y_3$:  inflation gap ($\Delta D_t = \pi^A_t - \pi^B_t$)", align="left", size=9)
    arrow(ax, 0.28, 0.5, 0.42, 0.5)
    ax.text(0.35, 0.56, "pass-through", ha="center", fontsize=8, style="italic")
    save(fig, "fig01_conceptual_framework")


def fig02_lp_explainer():
    """How a local projection works: (a) the timing of one regression, (b) one regression per horizon."""
    fig, axes = plt.subplots(2, 1, figsize=(6.8, 5.6), gridspec_kw={"height_ratios": [1, 1.25]})
    ax = axes[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("(a) What one regression uses, for a horizon h", loc="left", fontsize=9)
    segs = [(0.01, 0.29, r"$t-12, \ldots, t-1$", "History: 12 past months\nof inflation and fuel\n(held constant)", "white"),
            (0.32, 0.16, r"$t$", "The shock\n" r"$f_t$" "\n(effect = " r"$\beta_h$" ")", LIGHT),
            (0.50, 0.30, r"$t+1, \ldots, t+h-1$", "Later fuel shocks\n(Teulings–Zubanov leads;\nheld constant)", "white"),
            (0.82, 0.17, r"$t+h$", "Outcome\n" r"$\pi_{t+h}$", LIGHT)]
    for x, w, top, body, fill in segs:
        ax.text(x + w / 2, 0.88, top, ha="center", fontsize=9)
        box(ax, x, 0.12, w, 0.62, body, fill=fill, size=8.5)
    arrow(ax, 0.0, 0.03, 1.0, 0.03)
    ax.text(1.0, -0.06, "months", ha="right", fontsize=8)

    ax = axes[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("(b) One regression for each month ahead, then assemble", loc="left", fontsize=9)
    lines = [(r"$h=0$", r"$\pi_t$ on $f_t$ + history", r"$\beta_0$"),
             (r"$h=1$", r"$\pi_{t+1}$ on $f_t$ + history", r"$\beta_1$"),
             (r"$h=2$", r"$\pi_{t+2}$ on $f_t$ + history + $f_{t+1}$", r"$\beta_2$"),
             (r"$\vdots$", r"$\vdots$", r"$\vdots$"),
             (r"$h=12$", r"$\pi_{t+12}$ on $f_t$ + history + $f_{t+1}, \ldots, f_{t+11}$", r"$\beta_{12}$")]
    for i, (a, b, c) in enumerate(lines):
        y = 0.92 - i * 0.13
        ax.text(0.02, y, a, fontsize=9, va="center")
        ax.text(0.12, y, b, fontsize=9, va="center")
        ax.text(0.80, y, "→  " + c, fontsize=9, va="center")
    box(ax, 0.06, 0.0, 0.88, 0.22,
        r"Impulse response: $\beta_0, \beta_1, \ldots, \beta_{12}$ plotted against $h$ (90% bands)" "\n"
        r"Cumulative effect on the price level: $B_h = \beta_0 + \beta_1 + \cdots + \beta_h$", fill=LIGHT, size=9)
    fig.tight_layout()
    save(fig, "fig02_local_projection")


def fig03_trends():
    d = pd.read_csv(TAB / "desc_yoy_national.csv", parse_dates=["date"]).set_index("date")
    fig, axes = plt.subplots(3, 1, figsize=(7.0, 6.4), sharex=True, gridspec_kw={"height_ratios": [2, 1.2, 1.2]})
    axes[0].plot(d.index, d.yoy_cpi_all, color=BLACK, linestyle="-", linewidth=1.1, label="All income households")
    axes[0].plot(d.index, d.yoy_cpi_b30, color=BLACK, linestyle="--", linewidth=1.1, label="Bottom 30% households")
    axes[0].set_ylabel("Inflation, % y/y")
    axes[0].legend(loc="upper right")
    axes[0].set_title("(a) Headline inflation", loc="left", fontsize=9)
    g = d.yoy_gap
    axes[1].fill_between(d.index, 0, g.where(g > 0, 0), color=MID, linewidth=0, label="Bottom 30% higher")
    axes[1].fill_between(d.index, 0, g.where(g < 0, 0), facecolor="white", edgecolor=BLACK, hatch="////",
                         linewidth=0, label="All income higher")
    zero(axes[1])
    axes[1].set_ylabel("pp")
    axes[1].legend(loc="upper right", ncol=2)
    axes[1].set_title("(b) Inflation gap: bottom 30% minus all income", loc="left", fontsize=9)
    axes[2].plot(d.index, d.yoy_fuel, color=BLACK, linewidth=1.0)
    zero(axes[2])
    axes[2].set_ylabel("% y/y")
    axes[2].set_title("(c) Retail fuel index (CPI 07.2.2)", loc="left", fontsize=9)
    fig.tight_layout()
    save(fig, "fig03_trends")


def fig04_rq1(est):
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    irf(ax, pick(est, "RQ1", "baseline", "d_cpi_all"), A, "All-income CPI (90% band shaded)")
    irf(ax, pick(est, "RQ1", "baseline", "d_cpi_b30"), B, "Bottom-30% CPI (90% band dotted)", band="lines")
    ax.set_ylabel("Cumulative response (pp per 1% fuel)")
    ax.legend(loc="lower right")
    save(fig, "fig04_rq1_passthrough")


def fig05_rq2(est):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), sharey=True)
    for ax, (spec, title) in zip(axes, [("national", "(a) National"), ("panel", "(b) 17-region panel")]):
        irf(ax, pick(est, "RQ2", spec, "d_ratio"), A)
        ax.set_title(title, loc="left", fontsize=9)
    axes[0].set_ylabel("Cumulative response of\nln(CPI all / CPI bottom 30%)")
    axes[0].annotate("Below 0: prices of the bottom 30% rise more", xy=(0.2, -0.038), fontsize=8)
    fig.tight_layout()
    save(fig, "fig05_rq2_gap")


def forest(ax, rows):
    rows = rows[::-1]
    for i, (lab, b, s, open_marker) in enumerate(rows):
        ax.errorbar(b, i, xerr=1.645 * s, fmt="s" if open_marker else "o", color=BLACK, ecolor=BLACK,
                    elinewidth=1.0, markersize=4.5, capsize=2, markerfacecolor="white" if open_marker else BLACK)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    zero(ax, horizontal=False)


def fig06_robustness(est):
    c = est[est.cumulative & (est.h == 6) & (est.term == "shock") & (est.outcome == "d_ratio")]
    get = lambda rq, spec: tuple(c[(c.rq == rq) & (c.spec == spec)][["beta", "se"]].iloc[0])  # noqa: E731
    rows = [("Baseline, national", *get("RQ2", "national"), False),
            ("Dubai crude in pesos (national)", *get("ROB", "dubai crude php"), False),
            ("Macro controls (national)", *get("ROB", "macro controls"), False),
            ("Excluding 2020 (national)", *get("ROB", "excl 2020"), False),
            ("Baseline, 17-region panel", *get("RQ2", "panel"), False),
            ("Panel, 2001–2012", *get("ROB", "panel 2001-2012"), True),
            ("Panel, 2013–2026", *get("ROB", "panel 2013-2026"), True)]
    loo = c[(c.rq == "ROB") & c.spec.str.startswith("drop ")]
    rows.append(("Panel, one region left out (range)", float("nan"), 0.0, False))
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    forest(ax, rows)
    ax.plot([loo.beta.min(), loo.beta.max()], [0, 0], color=BLACK, linewidth=4, solid_capstyle="butt")
    ax.set_xlabel("Cumulative response of ln(CPI all / CPI bottom 30%) after 6 months, 90% CI\n"
                  "Open squares: split of the panel sample (specified after the first results)")
    save(fig, "fig06_robustness")


def fig07_rq3_2026():
    e1 = pd.read_csv(TAB / "rq3_national.csv", parse_dates=["date"])
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), sharey=True)
    for ax, (series, title) in zip(axes, [("cpi_all", "(a) All-income CPI"), ("cpi_b30", "(b) Bottom-30% CPI")]):
        q = e1[e1.series == series]
        m = q.date.dt.strftime("%b")
        ax.fill_between(m, q.lo, q.hi, color=LIGHT, linewidth=0)
        ax.plot(m, q.actual, label="Actual", **A)
        ax.plot(m, q.beta, label="Fuel-driven, model estimated on 2001–2025 (range shaded)", **B)
        zero(ax)
        ax.set_title(title, loc="left", fontsize=9)
        ax.set_xlabel("2026")
    axes[0].set_ylabel("Change since Dec 2025 (100 × log points)")
    h, lab = axes[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.07))
    fig.tight_layout()
    save(fig, "fig07_rq3_2026")


def fig08_rq3_decomposition():
    e5 = pd.read_csv(TAB / "rq3_decomposition.csv", dtype={"coicop": str}).set_index("coicop")
    parts = [("Rice and other cereals", e5.loc["01.1.1", "gap_pp"]),
             ("Other food", e5.loc["01.1", "gap_pp"] - e5.loc["01.1.1", "gap_pp"]),
             ("Passenger transport fares", e5.loc["07.3", "gap_pp"]),
             ("Cooking and household fuels", e5.loc["04.5", "gap_pp"]),
             ("Tobacco", e5.loc["02.3", "gap_pp"]),
             ("Own-vehicle fuel", e5.loc["07.2", "gap_pp"]),
             ("Housing rent", e5.loc["04.1", "gap_pp"])]
    parts.append(("All other items", e5.loc["0", "gap_pp"] - sum(v for _, v in parts)))
    parts = parts[::-1]
    vals = [v for _, v in parts]
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    for i, v in enumerate(vals):
        ax.barh(i, v, height=0.6, color=MID if v > 0 else "white", edgecolor=BLACK, linewidth=0.7,
                hatch=None if v > 0 else "////")
        ax.text(v + (0.03 if v >= 0 else -0.03), i, f"{v:+.2f}", va="center", ha="left" if v >= 0 else "right",
                fontsize=8)
    ax.set_yticks(range(len(parts)), [n for n, _ in parts])
    zero(ax, horizontal=False)
    ax.set_xlim(min(vals) - 0.45, max(vals) + 0.45)
    ax.set_xlabel(f"Contribution to the gap (pp); total gap = {e5.loc['0', 'gap_pp']:+.2f} pp\n"
                  "Grey: raised the bottom-30% CPI more; hatched: raised the all-income CPI more")
    save(fig, "fig08_rq3_decomposition")


def figA1_divisions():
    dec = pd.read_csv(TAB / "rq2_weights_decomposition.csv", dtype={"coicop": str})
    dec = dec[dec.coicop != "12"].sort_values("beta")   # financial services: weight ~0, table only
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    y = range(len(dec))
    ax.errorbar(dec.beta, y, xerr=1.645 * dec.se, fmt="o", color=BLACK, ecolor=BLACK, elinewidth=1.0,
                markersize=4.5, capsize=2)
    ax.set_yticks(list(y), [f"{d}  ({w:.0f}% / {b:.0f}%)" for d, w, b in zip(dec.division, dec.w_all, dec.w_b30)])
    zero(ax, horizontal=False)
    ax.set_xlabel("Cumulative response after 12 months (pp per 1% fuel), 90% CI\n"
                  "Labels: basket weight, all income / bottom 30%")
    save(fig, "figA1_divisions")


def figA2_region_groups(est):
    c = est[est.cumulative & (est.h == 12)]
    rows = [("Pooled (all regions)", *c[(c.rq == "RQ2") & (c.spec == "panel") & (c.term == "shock")][["beta", "se"]].iloc[0], False)]
    for g, lab in [("high_poverty", "High poverty"), ("high_food", "High food share"),
                   ("mindanao", "Mindanao"), ("island", "Island regions")]:
        r = c[(c.spec == f"x {g}") & (c.term == f"shock_x_{g}")][["beta", "se"]].iloc[0]
        rows.append((f"{lab}: extra effect", *r, False))
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    forest(ax, rows)
    ax.set_xlabel("Cumulative response of ln(CPI all / CPI bottom 30%) after 12 months, 90% CI")
    save(fig, "figA2_region_groups")


def figA3_robustness_all(est):
    c = est[est.cumulative & (est.h == 6) & (est.term == "shock") & (est.outcome == "d_ratio")]
    get = lambda rq, spec: tuple(c[(c.rq == rq) & (c.spec == spec)][["beta", "se"]].iloc[0])  # noqa: E731
    rows = [("Baseline, national", *get("RQ2", "national"), False)]
    for spec, lab in [("p=6", "6 lags"), ("p=18", "18 lags"), ("excl 2026", "Shock dates to Dec 2025"),
                      ("splice dummies", "Base-change dummies"), ("to Jun 2019", "Reference study's window"),
                      ("gasoline 07.2.2.2", "Gasoline index, 2019–"), ("WB pump price", "World Bank pump price, 2018–25"),
                      ("national excl 2008", "Excluding 2008, national"), ("national 2013-2026", "National, 2013–2026")]:
        rows.append((lab, *get("APP", spec), False))
    rows += [("Baseline, 17-region panel", *get("RQ2", "panel"), False)]
    for spec, lab in [("panel excl 2008", "Panel, excluding 2008"), ("drop flagged 2026", "Panel, re-mapped 2026 months dropped"),
                      ("national shock", "Panel, national fuel index")]:
        rows.append((lab, *get("APP", spec), False))
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    forest(ax, rows)
    ax.set_xlabel("Cumulative response of ln(CPI all / CPI bottom 30%) after 6 months, 90% CI")
    save(fig, "figA3_robustness_other")


def figA4_regional():
    r = pd.read_csv(TAB / "desc_regional.csv")
    r = r[r.region.isin(REGIONS_17)].sort_values("cum_gap_2001_2025")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.2), sharey=True)
    y = range(len(r))
    axes[0].plot(r.infl_all_2001_2025, y, "o", color=BLACK, markersize=4.5, label="All income")
    axes[0].plot(r.infl_b30_2001_2025, y, "s", color=BLACK, markerfacecolor="white", markersize=4.5, label="Bottom 30%")
    for i, (a, b) in enumerate(zip(r.infl_all_2001_2025, r.infl_b30_2001_2025)):
        axes[0].plot([a, b], [i, i], color=MID, linewidth=0.8)
    axes[0].set_yticks(list(y), [SHORT[x] for x in r.region])
    axes[0].set_xlabel("Average inflation 2001–2025, % y/y")
    axes[0].set_title("(a) Average inflation", loc="left", fontsize=9)
    axes[1].barh(list(y), r.cum_gap_2001_2025, color=MID, edgecolor=BLACK, linewidth=0.6, height=0.6)
    zero(axes[1], horizontal=False)
    axes[1].set_xlabel("Change in 100 × ln(CPI all/CPI b30), Dec 2000–Dec 2025\n(negative: poor's prices rose more)")
    axes[1].set_title("(b) Cumulative gap", loc="left", fontsize=9)
    h, lab = axes[0].get_legend_handles_labels()
    fig.tight_layout()
    fig.legend(h, lab, loc="lower center", ncol=2, bbox_to_anchor=(0.3, -0.06))
    save(fig, "figA4_regional")


def main():
    est = pd.read_csv(TAB / "estimates.csv")
    fig01_conceptual()
    fig02_lp_explainer()
    fig03_trends()
    fig04_rq1(est)
    fig05_rq2(est)
    fig06_robustness(est)
    fig07_rq3_2026()
    fig08_rq3_decomposition()
    figA1_divisions()
    figA2_region_groups(est)
    figA3_robustness_all(est)
    figA4_regional()
    print("figures written to", FIG)


if __name__ == "__main__":
    main()
