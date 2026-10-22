"""Draw all figures in black and white for journal print.

Conventions: no colour; series told apart by line style and marker shape;
confidence bands as light grey fill (first series) or dotted bound lines
(second series); bars with grey fill or hatching; serif font; no titles inside
the image (captions belong in the document). Each figure is written as 300-dpi
PNG and TIFF, and vector PDF, to output/figures/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "output" / "tables"
FIG = ROOT / "output" / "figures"

BLACK, DARK, MID, LIGHT = "0.0", "0.25", "0.55", "0.85"
plt.rcParams.update({
    "font.family": "DejaVu Serif", "font.size": 9, "axes.edgecolor": BLACK, "axes.labelcolor": BLACK,
    "xtick.color": BLACK, "ytick.color": BLACK, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": False, "legend.frameon": False, "figure.dpi": 100, "hatch.linewidth": 0.6,
    "lines.linewidth": 1.4,
})
A = dict(color=BLACK, linestyle="-", marker="o", markersize=3.5, markerfacecolor=BLACK)        # series 1
B = dict(color=BLACK, linestyle="--", marker="s", markersize=3.5, markerfacecolor="white")     # series 2


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG / f"{name}.tiff", dpi=300, bbox_inches="tight", pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", metadata={"CreationDate": None})  # byte-stable reruns
    plt.close(fig)


def zero(ax, horizontal=True):
    (ax.axhline if horizontal else ax.axvline)(0, color=BLACK, linewidth=0.6)


def irf(ax, q, style, label=None, band="fill"):
    if band == "fill":
        ax.fill_between(q.h, q.lo, q.hi, color=LIGHT, linewidth=0)
    else:
        ax.plot(q.h, q.lo, color=BLACK, linestyle=":", linewidth=0.8, marker=None)
        ax.plot(q.h, q.hi, color=BLACK, linestyle=":", linewidth=0.8, marker=None)
    ax.plot(q.h, q.beta, label=label, **style)
    zero(ax)
    ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel("Months after the shock")


def pick(est, rq, spec, outcome, cum=True, term="shock"):
    q = est[(est.rq == rq) & (est.spec == spec) & (est.outcome == outcome)
            & (est.cumulative == cum) & (est.term == term)]
    return q.sort_values("h")


def fig1(est):
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    irf(ax, pick(est, "RQ1", "baseline", "d_cpi_all"), A, "All-income CPI (90% band shaded)")
    irf(ax, pick(est, "RQ1", "baseline", "d_cpi_b30"), B, "Bottom-30% CPI (90% band dotted)", band="lines")
    ax.set_ylabel("Cumulative response (pp per 1% fuel)")
    ax.legend(loc="lower right")
    save(fig, "fig1_rq1_passthrough")


def fig2(est):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), sharey=True)
    for ax, (rq, spec, title) in zip(axes, [("RQ2", "baseline", "(a) National"),
                                            ("RQ4", "pooled", "(b) 17-region panel")]):
        irf(ax, pick(est, rq, spec, "d_ratio"), A)
        ax.set_title(title, loc="left", fontsize=9)
    axes[0].set_ylabel("Cumulative response of\nln(CPI all / CPI bottom 30%)")
    axes[0].annotate("Below 0: prices of the bottom 30% rise more", xy=(0.2, -0.038), fontsize=8)
    fig.tight_layout()
    save(fig, "fig2_rq2_rq4_ratio")


def fig3(est):
    dec = pd.read_csv(TAB / "rq3_gap_decomposition.csv", dtype={"coicop": str})
    # Financial services (weight 0.03% / 0.0003%) is reported in the table only.
    dec = dec[dec.coicop != "12"].sort_values("beta")
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    y = range(len(dec))
    ax.errorbar(dec.beta, y, xerr=1.645 * dec.se, fmt="o", color=BLACK, ecolor=BLACK, elinewidth=1.0,
                markersize=4.5, capsize=2)
    ax.set_yticks(list(y), [f"{d}  ({w:.0f}% / {b:.0f}%)" for d, w, b in zip(dec.division, dec.w_all, dec.w_b30)])
    zero(ax, horizontal=False)
    ax.set_xlabel("Cumulative response after 12 months (pp per 1% fuel), 90% CI\n"
                  "Labels: basket weight, all income / bottom 30%")
    save(fig, "fig3_rq3_components")


def forest(ax, rows):
    """rows: (label, beta, se, supplementary?)"""
    rows = rows[::-1]
    for i, (lab, b, s, supp) in enumerate(rows):
        ax.errorbar(b, i, xerr=1.645 * s, fmt="s" if supp else "o", color=BLACK, ecolor=BLACK,
                    elinewidth=1.0, markersize=4.5, capsize=2, markerfacecolor="white" if supp else BLACK)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    zero(ax, horizontal=False)


def fig4(est):
    c = est[est.cumulative & (est.h == 12)]
    rows = [("Pooled (all regions)", *c[(c.rq == "RQ4") & (c.spec == "pooled")][["beta", "se"]].iloc[0], False)]
    for g, lab in [("high_poverty", "High poverty"), ("high_food", "High food share"),
                   ("mindanao", "Mindanao"), ("island", "Island regions")]:
        r = c[(c.spec == f"x {g}") & (c.term == f"shock_x_{g}")][["beta", "se"]].iloc[0]
        rows.append((f"{lab}: extra effect", *r, False))
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    forest(ax, rows)
    ax.set_xlabel("Cumulative response of ln(CPI all / CPI bottom 30%) after 12 months, 90% CI")
    save(fig, "fig4_rq4_groups")


def fig5(est):
    c = est[est.cumulative & (est.h == 6) & (est.term == "shock") & (est.outcome == "d_ratio")]
    get = lambda rq, spec: tuple(c[(c.rq == rq) & (c.spec == spec)][["beta", "se"]].iloc[0])  # noqa: E731
    rows = [("Baseline, national", *get("RQ2", "baseline"), False),
            ("Baseline, regional panel", *get("RQ4", "pooled"), False)]
    for spec, lab in [("a dubai crude php", "Dubai crude in pesos"), ("b macro controls", "FX, policy rate, FAO"),
                      ("c p=6", "6 lags"), ("c p=18", "18 lags"), ("d excl 2020", "Excluding 2020"),
                      ("d excl 2026", "Shock dates to Dec 2025"), ("e splice dummies", "Base-change dummies"),
                      ("g to Jun 2019", "Reference study's window"),
                      ("h gasoline 07.2.2.2", "Gasoline index, 2019–"), ("i WB pump price", "World Bank pump price, 2018–25")]:
        rows.append((lab, *get("ROB", spec), False))
    for spec, lab in [("national excl 2008", "Excluding 2008, national"),
                      ("regional excl 2008", "Excluding 2008, regional"),
                      ("regional 2001-2012", "Regional, 2001–2012"), ("regional 2013-", "Regional, 2013–2026")]:
        rows.append((lab, *get("RQ3b", spec), True))
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    forest(ax, rows)
    ax.set_xlabel("Cumulative response of ln(CPI all / CPI bottom 30%) after 6 months, 90% CI\n"
                  "Open squares: supplementary analyses specified after the first results")
    save(fig, "fig5_robustness")


def fig6():
    e1 = pd.read_csv(TAB / "e1_national_2026.csv", parse_dates=["date"])
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
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.07))
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
    save(fig, "fig7_2026_gap_decomposition")


def figd1():
    """Objective 1: year-on-year inflation, both groups, and fuel prices, 2001-2026."""
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
    save(fig, "figd1_trends")


def figd2():
    """Objective 1: regional averages, 2001-2025, and cumulative gap."""
    r = pd.read_csv(TAB / "desc_regional.csv")
    r = r[r.region != "PH"].sort_values("cum_gap_2001_2025")
    names = {"NCR": "NCR", "CAR": "CAR", "R01": "I", "R02": "II", "R03": "III", "R04A": "IV-A", "R04B": "MIMAROPA",
             "R05": "V", "R06": "VI", "R07": "VII", "R08": "VIII", "R09": "IX", "R10": "X", "R11": "XI",
             "R12": "XII", "R13": "XIII", "BARMM": "BARMM"}
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.2), sharey=True)
    y = range(len(r))
    axes[0].plot(r.infl_all_2001_2025, y, "o", color=BLACK, markersize=4.5, label="All income")
    axes[0].plot(r.infl_b30_2001_2025, y, "s", color=BLACK, markerfacecolor="white", markersize=4.5, label="Bottom 30%")
    for i, (a, b) in enumerate(zip(r.infl_all_2001_2025, r.infl_b30_2001_2025)):
        axes[0].plot([a, b], [i, i], color=MID, linewidth=0.8)
    axes[0].set_yticks(list(y), [names[x] for x in r.region])
    axes[0].set_xlabel("Average inflation 2001–2025, % y/y")
    axes[0].set_title("(a) Average inflation", loc="left", fontsize=9)
    axes[1].barh(list(y), r.cum_gap_2001_2025, color=MID, edgecolor=BLACK, linewidth=0.6, height=0.6)
    zero(axes[1], horizontal=False)
    axes[1].set_xlabel("Change in ln(CPI all/CPI b30), Dec 2000–Dec 2025\n(× 100; negative: poor's prices rose more)")
    axes[1].set_title("(b) Cumulative gap", loc="left", fontsize=9)
    h, l = axes[0].get_legend_handles_labels()
    fig.tight_layout()
    fig.legend(h, l, loc="lower center", ncol=2, bbox_to_anchor=(0.3, -0.06))
    save(fig, "figd2_regional")


def figw0():
    """Working paper conceptual framework: top-to-bottom flow, policy on the left, moderators on the right."""
    from matplotlib.patches import FancyBboxPatch
    fig, ax = plt.subplots(figsize=(7.0, 6.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def box(cx, cy, w, h, text, shade="white"):
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.6", facecolor=shade,
                                    edgecolor=BLACK, linewidth=0.8))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=7, linespacing=1.3)

    def arrow(x0, y0, x1, y1, dashed=False):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=0.8, linestyle="--" if dashed else "-",
                                    shrinkA=0, shrinkB=0))

    # main column (x = 50)
    box(50, 92, 46, 7, "World oil price (Dubai crude) × peso–dollar rate", LIGHT)
    box(50, 78, 46, 8, "Retail fuel price\n(pump price including excise, VAT and margins)", LIGHT)
    box(50, 59, 46, 18, "Transmission channels\n\nDirect: motor fuel, LPG, kerosene\n"
                        "Indirect: fares, food, utilities\nSecond round: wages, expectations")
    box(34, 36, 24, 8, "CPI, all income\nhouseholds")
    box(66, 36, 24, 8, "CPI, bottom 30%\nhouseholds")
    box(50, 16, 48, 10, "Distributional gap = ln(CPI all / CPI b30)\nbelow 0: the poor pay more", LIGHT)
    arrow(50, 87.4, 50, 82.6)
    arrow(50, 73.4, 50, 68.6)
    arrow(40, 49.4, 34, 40.6)
    arrow(60, 49.4, 66, 40.6)
    arrow(34, 31.4, 44, 21.6)
    arrow(66, 31.4, 56, 21.6)
    # policy (left) and moderators (right)
    box(12, 70, 20, 22, "Policy instruments\n\nExcise relief\nFuel subsidies\nFare regulation\n"
                        "Cash transfers\nPolicy rate")
    arrow(22.6, 76, 26.4, 78, dashed=True)
    arrow(22.6, 64, 26.4, 59, dashed=True)
    arrow(12, 58.4, 25.2, 17, dashed=True)
    ax.text(2, 40, "transfers\noffset the\nburden", fontsize=7, style="italic")
    box(88, 57, 21, 29, "Moderators\n\nBasket weights\n\nWithin-category\nprice differences\n\nRegion: poverty,\nfood share,\ndistance")
    arrow(88, 41.4, 78.6, 37)
    ax.text(2, 3, "Solid arrows: transmission of the shock. Dashed arrows: points where policy can intervene.",
            fontsize=7.5)
    save(fig, "figw0_framework")


# ---------------------------------------------------------------- analysis-report figures (figr_*)

def figr_simulation():
    """Validation: estimator recovers a known impulse response from simulated data."""
    import sys
    sys.path.insert(0, str(ROOT))
    from ospd.lp import local_projection
    from tests.test_lp import simulate, true_irf
    df = simulate(20, 400)
    r = local_projection(df, "y", "x", time="t", unit="unit", horizons=8, p=12, se="driscoll_kraay")
    r = r[r.term == "shock"]
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    ax.fill_between(r.h, r.lo, r.hi, color=LIGHT, linewidth=0)
    ax.plot(r.h, r.beta, label="Estimated (90% band shaded)", **A)
    ax.plot(range(9), true_irf(8), label="True response", **B)
    zero(ax)
    ax.set_xlabel("Months after the shock")
    ax.set_ylabel("Response to a unit shock")
    ax.legend(loc="upper right")
    save(fig, "figr_simulation")


def figr_eu_validation():
    """Validation: EU responses to after-tax, before-tax and crude prices vs. reference values."""
    rep = pd.read_csv(TAB / "replication_eu_ph.csv")
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    styles = [("G1 after tax [cluster]", "After-tax pump price", A, 0.055),
              ("G2 before tax + tax control [cluster]", "Before-tax pump price", B, 0.020),
              ("G2 Brent in euro [cluster]", "Brent crude",
               dict(color=BLACK, linestyle=":", marker="^", markersize=3.8, markerfacecolor="white"), 0.015)]
    for spec, lab, st, ref in styles:
        q = rep[rep.spec == spec].sort_values("h")
        ax.plot(q.h, q.beta, label=lab, **st)
        ax.plot([-0.25], [ref], marker=st["marker"], color=BLACK, markersize=6, markerfacecolor=MID, linestyle="")
    zero(ax)
    ax.set_xticks(range(7))
    ax.set_xlabel("Months after the shock (grey markers at left: Kpodar–Liu values at month 0)")
    ax.set_ylabel("Response of monthly inflation (pp per 1%)")
    ax.legend(loc="upper right")
    save(fig, "figr_eu_validation")


def figr_crosscorr():
    cc = pd.read_csv(TAB / "desc_crosscorr.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), sharey=True)
    axes[0].bar(cc.lag - 0.2, cc["CPI, all income"], width=0.4, color=BLACK, label="All income")
    axes[0].bar(cc.lag + 0.2, cc["CPI, bottom 30%"], width=0.4, color="white", edgecolor=BLACK, hatch="////",
                linewidth=0.6, label="Bottom 30%")
    axes[0].legend(loc="upper right")
    axes[0].set_title("(a) Fuel change and later inflation", loc="left", fontsize=9)
    axes[1].bar(cc.lag, cc["Gap: ln(CPI all/CPI b30)"], width=0.6, color=MID, edgecolor=BLACK, linewidth=0.6)
    axes[1].set_title("(b) Fuel change and later change in the gap", loc="left", fontsize=9)
    for ax in axes:
        zero(ax)
        ax.set_xlabel("Months later (k)")
        ax.set_xticks(range(0, 13, 2))
    axes[0].set_ylabel("Correlation")
    fig.tight_layout()
    save(fig, "figr_crosscorr")


def figr_rq3b(est):
    rows = [("c01", "Food"), ("c04", "Housing, utilities"), ("c07", "Transport"), ("c11", "Restaurants")]
    get = lambda spec, y: est[(est.rq == "RQ3b") & (est.spec == spec) & (est.outcome == y) & est.cumulative  # noqa: E731
                              & (est.h == 12) & (est.term == "shock")].iloc[0]
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    for i, (c, lab) in enumerate(rows):
        a, b = get("2013- all-income", f"d_{c}"), get("2013- bottom 30%", f"d_b30_{c}")
        ax.barh(i + 0.2, a.beta, height=0.38, color=BLACK, label="All income" if i == 0 else None)
        ax.barh(i - 0.2, b.beta, height=0.38, color="white", edgecolor=BLACK, hatch="////", linewidth=0.6,
                label="Bottom 30%" if i == 0 else None)
        for y, v in ((i + 0.2, a.beta), (i - 0.2, b.beta)):
            ax.text(v + 0.005, y, f"{v:.2f}", va="center", fontsize=7.5)
    ax.set_yticks(range(len(rows)), [r[1] for r in rows])
    zero(ax, horizontal=False)
    ax.set_xlabel("Cumulative response after 12 months (pp per 1% fuel), 2013–2026")
    ax.legend(loc="lower right")
    save(fig, "figr_rq3b")


def figr_e2_regional():
    e2 = pd.read_csv(TAB / "e2_regional_2026.csv")
    e2 = e2[e2.region != "PH"].sort_values("actual_b30")
    names = {"NCR": "NCR", "CAR": "CAR", "R01": "I", "R02": "II", "R03": "III", "R04A": "IV-A", "R04B": "MIMAROPA",
             "R05": "V", "R06": "VI", "R07": "VII", "R08": "VIII", "R09": "IX", "R10": "X", "R11": "XI",
             "R12": "XII", "R13": "XIII", "BARMM": "BARMM"}
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.0), sharey=True, gridspec_kw={"width_ratios": [1.4, 1]})
    y = range(len(e2))
    axes[0].barh(list(y), e2.actual_b30, height=0.7, color=LIGHT, edgecolor=BLACK, linewidth=0.6,
                 label="Actual rise")
    axes[0].barh(list(y), e2.fuel_driven_b30, height=0.35, color=BLACK, label="Fuel-driven part (model)")
    axes[0].set_yticks(list(y), [names[r] for r in e2.region])
    axes[0].set_xlabel("Bottom-30% CPI, Dec 2025–Aug 2026\n(100 × log points)")
    axes[0].set_title("(a) Price rise for the poor", loc="left", fontsize=9)
    axes[1].barh(list(y), e2.extra_cost_php_month, height=0.6, color=MID, edgecolor=BLACK, linewidth=0.6)
    for i, v in enumerate(e2.extra_cost_php_month):
        axes[1].text(v + 8, i, f"{v:.0f}", va="center", fontsize=7.5)
    axes[1].set_xlim(0, e2.extra_cost_php_month.max() * 1.2)
    axes[1].set_xlabel("PHP per month, poverty-line\nfamily of five (fuel-driven)")
    axes[1].set_title("(b) Fuel-driven extra cost", loc="left", fontsize=9)
    h, l = axes[0].get_legend_handles_labels()
    fig.tight_layout()
    fig.legend(h, l, loc="lower center", ncol=2, bbox_to_anchor=(0.35, -0.07))
    save(fig, "figr_e2_regional")


def figr_e4_mechanism():
    e4 = pd.read_csv(TAB / "e4_mechanism.csv")
    e4 = e4[e4.h == 12]
    items = [("e0452", "LPG"), ("e0453", "Kerosene"), ("e0454", "Charcoal, wood"), ("t073", "Transport fares"),
             ("f0111", "Rice, cereals")]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    for i, (it, lab) in enumerate(items):
        for ax, col in zip(axes, ["weight", "beta"]):
            a = e4[(e4["item"] == it) & (e4.basket == "all")][col].iloc[0]
            b = e4[(e4["item"] == it) & (e4.basket == "b30")][col].iloc[0]
            ax.barh(i + 0.2, a, height=0.38, color=BLACK, label="All income" if i == 0 else None)
            ax.barh(i - 0.2, b, height=0.38, color="white", edgecolor=BLACK, hatch="////", linewidth=0.6,
                    label="Bottom 30%" if i == 0 else None)
    axes[0].set_yticks(range(len(items)), [x[1] for x in items])
    axes[0].set_xlabel("Share of the basket (%)")
    axes[0].set_title("(a) How much each group buys", loc="left", fontsize=9)
    axes[1].set_xlabel("Price response after 12 months\n(pp per 1% fuel)")
    axes[1].set_title("(b) How much its price responds", loc="left", fontsize=9)
    zero(axes[1], horizontal=False)
    axes[0].legend(loc="lower right")
    fig.tight_layout()
    save(fig, "figr_e4_mechanism")


if __name__ == "__main__":
    est = pd.read_csv(TAB / "estimates.csv")
    for f in (fig1, fig2, fig3, fig4, fig5):
        f(est)
    for f in (fig6, fig7, figd1, figd2, figw0, figr_simulation, figr_eu_validation, figr_crosscorr,
              figr_e2_regional, figr_e4_mechanism):
        f()
    figr_rq3b(est)
    print("figures written to", FIG)
