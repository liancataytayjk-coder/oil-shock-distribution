"""The panel study (decision D16): every number, table and figure of paper/manuscript.*.

One method (local projections with region fixed effects and Driscoll-Kraay standard errors), one data set
(the 17-region PSA panel, shock dates January 2001-August 2026), three questions:
  RQ1  pass-through of retail fuel prices to the price level of all households and of the bottom 30%;
  RQ2  the gap between the two (all-income minus bottom-30% inflation), why it has its sign
       (budget-share calculation, descriptive), and five robustness checks;
  Geography: region-specific responses (shock x region indicators, common lags, region fixed effects,
       Driscoll-Kraay), a Wald test that all 17 are equal, and their correlation with poverty and food shares;
  RQ3  the 2026 shock: responses estimated on data to December 2025, applied to the 2026 fuel path, with a
       moving-block bootstrap (blocks of 12 months, all regions together) for the uncertainty of the
       prediction, and the peso cost for a family of five at the poverty line.

Writes
  output/tables/panel_estimates.csv     cumulative responses, h = 0..12, every specification
  output/tables/panel_2026.csv          predicted and actual 2026 path, Philippines, with 90% bootstrap bands
  output/tables/panel_2026_regions.csv  2026 by region
  output/tables/panel_regions_lp.csv    region-specific responses, h = 6 and 12 (geography)
  output/tables/panel_numbers.json      numbers quoted in the manuscript
  output/figures/figP1..figP4           pass-through, gap, robustness, 2026
  code/stata/teaching/expected_panel.csv  values the Stata teaching do-files should reproduce
"""

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import data_io  # noqa: E402
from config import FIG, H, P, ROOT, START, TAB  # noqa: E402
from linearmodels.panel import PanelOLS  # noqa: E402
from lp import _design, local_projection  # noqa: E402
from scipy import stats  # noqa: E402

CUT = pd.Timestamp("2025-12-01")
M26 = pd.date_range("2026-01-01", "2026-08-01", freq="MS")
CONTROLS = ("d_php_usd", "d_policy_rate", "d_ffpi")
B_REPS, BLOCK, SEED = 999, 12, 20261120
BLACK, LIGHT = "0.0", "0.85"
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False, "lines.linewidth": 1.4})


def f(x, d=3, sign=False):
    s = f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
    return s.replace("-", "−")


def panel_data():
    reg = data_io.panel()
    nat = data_io.national()
    reg = reg.merge(nat[["date", *CONTROLS, "d_dubai_php"]], on="date", how="left")
    return reg.sort_values(["region", "date"]).reset_index(drop=True), nat


def lp(df, y, x="d_fuel", sample=None, **kw):
    s = (df.date >= START) if sample is None else sample
    r = local_projection(df, y, x, time="t", unit="region", horizons=H, p=P, se="driscoll_kraay",
                         sample=s, cumulative=True, **kw)
    return r[r.term == "shock"].reset_index(drop=True)


# ---------------------------------------------------------------- estimates
def estimates(reg):
    s01 = reg.date >= START
    specs = {
        ("RQ1", "baseline", "d_cpi_all"): lp(reg, "d_cpi_all"),
        ("RQ1", "baseline", "d_cpi_b30"): lp(reg, "d_cpi_b30"),
        ("RQ2", "baseline", "d_ratio"): lp(reg, "d_ratio"),
        ("ROB", "excl 2008", "d_ratio"): lp(reg, "d_ratio", sample=s01 & (reg.date.dt.year != 2008)),
        ("ROB", "2001-2012", "d_ratio"): lp(reg, "d_ratio", sample=s01 & (reg.date <= "2012-12-01")),
        ("ROB", "2013-2026", "d_ratio"): lp(reg, "d_ratio", sample=reg.date >= "2013-01-01"),
        ("ROB", "crude in pesos", "d_ratio"): lp(reg, "d_ratio", x="d_dubai_php"),
        ("ROB", "crude in pesos", "d_cpi_all"): lp(reg, "d_cpi_all", x="d_dubai_php"),
        ("ROB", "crude in pesos", "d_cpi_b30"): lp(reg, "d_cpi_b30", x="d_dubai_php"),
        ("ROB", "macro and food controls", "d_ratio"): lp(reg, "d_ratio", controls=CONTROLS),
        ("ROB", "food price control", "d_ratio"): lp(reg, "d_ratio", controls=("d_ffpi",)),
    }
    for r in sorted(reg.region.unique()):
        sub = reg[reg.region != r].reset_index(drop=True)
        specs[("LOO", f"drop {r}", "d_ratio")] = lp(sub, "d_ratio")
    rows = []
    for (rq, spec, y), q in specs.items():
        q = q.assign(rq=rq, spec=spec, outcome=y, shock="d_dubai_php" if "crude" in spec else "d_fuel")
        rows.append(q[["rq", "spec", "outcome", "shock", "h", "beta", "se", "lo", "hi", "nobs"]])
    est = pd.concat(rows, ignore_index=True)
    est.to_csv(TAB / "panel_estimates.csv", index=False)
    return est


# ---------------------------------------------------------------- geography
def regional_responses(reg, y, h):
    """Equation (3) with the shock interacted with each region's indicator (lags common to all regions).
    Returns the 17 responses, their Driscoll-Kraay covariance and the Wald test that they are all equal."""
    regions = sorted(reg.region.unique())
    d = _design(reg, y, "d_fuel", "region", "t", h, P, [], [], True, True, [])
    d = d[(reg.date >= START).to_numpy()]
    d["region"], d["tt"] = reg.loc[d.index, "region"], reg.loc[d.index, "t"]
    d = d.dropna()
    for r in regions:
        d[f"sx_{r}"] = d["shock"] * (d["region"] == r)
    regs = [c for c in d.columns if c not in ("dep", "region", "tt", "shock")]
    idx = pd.MultiIndex.from_arrays([d.region, d.tt])
    res = PanelOLS(d["dep"].set_axis(idx), d[regs].set_axis(idx).assign(const=1.0), entity_effects=True,
                   drop_absorbed=True).fit(cov_type="kernel", kernel="bartlett", bandwidth=h + 1)
    names = [f"sx_{r}" for r in regions]
    b, V = res.params[names].to_numpy(), res.cov.loc[names, names].to_numpy()
    k = len(regions)
    R = np.hstack([np.eye(k - 1), -np.ones((k - 1, 1))])           # beta_r - beta_last = 0 for all r
    W = float((R @ b) @ np.linalg.solve(R @ V @ R.T, R @ b))
    out = pd.DataFrame({"region": regions, "outcome": y, "h": h, "beta": b, "se": np.sqrt(np.diag(V)),
                        "nobs": int(res.nobs)})
    return out, W, float(stats.chi2.sf(W, k - 1))


def geography(reg):
    info = data_io.region_info()
    tabs, tests = [], []
    for y in ("d_cpi_all", "d_ratio"):
        for h in (6, 12):
            t, W, pval = regional_responses(reg, y, h)
            tabs.append(t)
            tests.append({"outcome": y, "h": h, "wald": W, "df": len(t) - 1, "p": pval})
    tab = pd.concat(tabs, ignore_index=True).merge(
        info[["region_name", "poverty_2018", "food_share_2018"]], left_on="region", right_index=True)
    tab["lo"], tab["hi"] = tab.beta - 1.645 * tab.se, tab.beta + 1.645 * tab.se
    tab.to_csv(TAB / "panel_regions_lp.csv", index=False)
    return tab, pd.DataFrame(tests)


# ---------------------------------------------------------------- 2026 with a block bootstrap
def designs(df, y, cut):
    """For each horizon, the estimation rows (shock dates 2001..cut, data truncated at cut), already demeaned
    by region is NOT done here: the bootstrap resamples months first and demeans within each draw."""
    d0 = df[df.date <= cut].reset_index(drop=True)
    out = []
    for h in range(H + 1):
        d = _design(d0, y, "d_fuel", "region", "t", h, P, [], [], True, True, [])
        d = d[(d0.date >= START).to_numpy()]
        d["region"], d["date"] = d0.loc[d.index, "region"], d0.loc[d.index, "date"]
        d = d.dropna()
        regs = [c for c in d.columns if c not in ("dep", "region", "date") and d[c].nunique() > 1]
        out.append((d, regs))
    return out


def fe_beta(d, regs, idx=None):
    """Within (fixed-effects) OLS coefficient on the shock, on rows idx (with repetition)."""
    z = d if idx is None else d.iloc[idx]
    cols = ["dep"] + regs
    m = z[cols] - z.groupby("region", sort=False)[cols].transform("mean")
    X, yv = m[regs].to_numpy(), m["dep"].to_numpy()
    b = np.linalg.lstsq(X, yv, rcond=None)[0]
    return b[regs.index("shock")]


def bootstrap_irfs(dsets, reps=B_REPS, block=BLOCK, seed=SEED):
    """Moving-block bootstrap over months (all regions of a month move together): (reps, H+1) responses."""
    months = np.array(sorted(set().union(*[set(d.date) for d, _ in dsets])))
    pos = {m: i for i, m in enumerate(months)}
    rows_by_month = []
    for d, _ in dsets:
        g = d.reset_index(drop=True).groupby(d.date.map(pos).to_numpy()).indices
        rows_by_month.append(g)
    n = len(months)
    rng = np.random.default_rng(seed)
    out = np.empty((reps, len(dsets)))
    for r in range(reps):
        starts = rng.integers(0, n - block + 1, size=int(np.ceil(n / block)))
        draw = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        for h, (d, regs) in enumerate(dsets):
            g = rows_by_month[h]
            idx = np.concatenate([g[m] for m in draw if m in g])
            out[r, h] = fe_beta(d.reset_index(drop=True), regs, idx)
    return out


def fuel_driven(B, fuel):
    """Change in 100 x ln P from Dec 2025 to each 2026 month: sum_s B_(m-s) f_s. B: (..., H+1)."""
    path = []
    for k in range(len(fuel)):
        lags = np.arange(k, -1, -1)
        path.append(np.tensordot(B[..., lags], fuel[: k + 1], axes=([-1], [0])))
    return np.stack(path, axis=-1)


def application_2026(reg, nat):
    natd = nat.set_index("date")
    fuel = natd.d_fuel.loc[M26].to_numpy()
    res, boot = {}, {}
    for y in ("d_cpi_all", "d_cpi_b30", "d_ratio"):
        ds = designs(reg, y, CUT)
        res[y] = np.array([fe_beta(d, regs) for d, regs in ds])
        boot[y] = bootstrap_irfs(ds)
    # check: the point estimates equal the package estimator on the truncated data
    chk = lp(reg[reg.date <= CUT].reset_index(drop=True), "d_cpi_all").beta.to_numpy()
    assert np.allclose(chk, res["d_cpi_all"], atol=1e-10), "fixed-effects bootstrap design differs from lp.py"
    act = {"d_cpi_all": 100 * np.log(natd.cpi_all.loc[M26] / natd.cpi_all.loc[CUT]).to_numpy(),
           "d_cpi_b30": 100 * np.log(natd.cpi_b30.loc[M26] / natd.cpi_b30.loc[CUT]).to_numpy()}
    act["d_ratio"] = act["d_cpi_all"] - act["d_cpi_b30"]
    rows = []
    for y in res:
        point, draws = fuel_driven(res[y], fuel), fuel_driven(boot[y], fuel)
        lo, hi = np.percentile(draws, [5, 95], axis=0)
        for k, m in enumerate(M26):
            rows.append({"series": y, "date": m.date(), "fuel_driven": point[k], "lo": lo[k], "hi": hi[k],
                         "actual": act[y][k], "fuel_cum": 100 * np.log(natd.fuel.loc[m] / natd.fuel.loc[CUT])})
    path = pd.DataFrame(rows)
    path.to_csv(TAB / "panel_2026.csv", index=False)

    # peso cost for a family of five at the national poverty line, with bootstrap bands
    info = data_io.region_info()
    cpi23 = natd.cpi_b30.loc["2023-01-01":"2023-12-01"].mean()
    line = info.threshold_2023["PH"] * 5 / 12 * natd.cpi_b30.loc[CUT] / cpi23
    fd_b30 = fuel_driven(boot["d_cpi_b30"], fuel)[:, -1]
    fd_all = fuel_driven(boot["d_cpi_all"], fuel)[:, -1]
    cost_b30 = line * (np.exp(fd_b30 / 100) - 1)
    extra = line * (np.exp(fd_b30 / 100) - np.exp(fd_all / 100))
    pt_b30 = fuel_driven(res["d_cpi_b30"], fuel)[-1]
    pt_all = fuel_driven(res["d_cpi_all"], fuel)[-1]
    cost = {"line": line, "cost_b30": line * (np.exp(pt_b30 / 100) - 1),
            "cost_b30_lo": np.percentile(cost_b30, 5), "cost_b30_hi": np.percentile(cost_b30, 95),
            "extra": line * (np.exp(pt_b30 / 100) - np.exp(pt_all / 100)),
            "extra_lo": np.percentile(extra, 5), "extra_hi": np.percentile(extra, 95),
            "actual_cost_b30": line * (np.exp(act["d_cpi_b30"][-1] / 100) - 1),
            "p_gap_nonneg": float((fuel_driven(boot["d_ratio"], fuel)[:, -1] >= 0).mean())}

    # regions: each region's own fuel path, the same panel responses
    reg_rows = []
    for r in sorted(reg.region.unique()):
        s = reg[reg.region == r].set_index("date")
        fr = s.d_fuel.loc[M26].to_numpy()
        cpi23r = s.cpi_b30.loc["2023-01-01":"2023-12-01"].mean()
        liner = info.threshold_2023[r] * 5 / 12 * s.cpi_b30.loc[CUT] / cpi23r
        fb = fuel_driven(res["d_cpi_b30"], fr)[-1]
        fg = fuel_driven(res["d_ratio"], fr)[-1]
        reg_rows.append({"region": r, "region_name": info.region_name[r], "poverty_2018": info.poverty_2018[r],
                         "fuel_change": 100 * np.log(s.fuel.loc[M26[-1]] / s.fuel.loc[CUT]),
                         "fuel_driven_b30": fb, "actual_b30": 100 * np.log(s.cpi_b30.loc[M26[-1]] / s.cpi_b30.loc[CUT]),
                         "fuel_driven_gap": fg,
                         "actual_gap": 100 * (np.log(s.cpi_all.loc[M26[-1]] / s.cpi_all.loc[CUT])
                                              - np.log(s.cpi_b30.loc[M26[-1]] / s.cpi_b30.loc[CUT])),
                         "cost_php_month": liner * (np.exp(fb / 100) - 1),
                         "new_geo_ext": int(s.new_geo_ext.loc[M26].any())})
    regions = pd.DataFrame(reg_rows)
    regions.to_csv(TAB / "panel_2026_regions.csv", index=False)
    return path, cost, regions, res


# ---------------------------------------------------------------- figures
def save(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)


def figure_regions(geo, est):
    pooled = {y: est[(est.rq.isin(["RQ1", "RQ2"])) & (est.spec == "baseline") & (est.outcome == y) & (est.h == 6)].iloc[0]
              for y in ("d_cpi_all", "d_ratio")}
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.4), sharey=True)
    q0 = geo[(geo.outcome == "d_ratio") & (geo.h == 6)].sort_values("beta")
    order = list(q0.region)
    labels = dict(zip(geo.region, geo.region_name))
    for ax, (y, title, xl) in zip(axes, [("d_cpi_all", "(a) Pass-through, all households", "% per 1% fuel"),
                                        ("d_ratio", "(b) Gap, all − low-income households", "pp per 1% fuel")]):
        q = geo[(geo.outcome == y) & (geo.h == 6)].set_index("region").loc[order]
        ypos = np.arange(len(q))
        ax.errorbar(q.beta, ypos, xerr=[q.beta - q.lo, q.hi - q.beta], fmt="o", color=BLACK, ecolor=BLACK,
                    markersize=3.5, capsize=1.5, elinewidth=0.8)
        ax.axvline(pooled[y].beta, color=BLACK, linestyle="--", linewidth=0.8)
        ax.axvline(0, color=BLACK, linewidth=0.6)
        ax.set_title(title, loc="left", fontsize=9)
        ax.set_xlabel(f"Cumulative response after 6 months ({xl})")
    axes[0].set_yticks(np.arange(len(order)), [labels[r] for r in order], fontsize=7)
    fig.tight_layout()
    save(fig, "figP5_regions")


def figures(est, path):
    g = lambda rq, spec, y: est[(est.rq == rq) & (est.spec == spec) & (est.outcome == y)].sort_values("h")  # noqa: E731
    a, b, gap = g("RQ1", "baseline", "d_cpi_all"), g("RQ1", "baseline", "d_cpi_b30"), g("RQ2", "baseline", "d_ratio")
    fig, ax = plt.subplots(figsize=(5.4, 3.3))
    ax.fill_between(a.h, a.lo, a.hi, color=LIGHT, linewidth=0)
    ax.plot(b.h, b.lo, color=BLACK, linestyle=":", linewidth=0.8)
    ax.plot(b.h, b.hi, color=BLACK, linestyle=":", linewidth=0.8)
    ax.plot(a.h, a.beta, color=BLACK, marker="o", markersize=3.5, label="All households (90% band shaded)")
    ax.plot(b.h, b.beta, color=BLACK, linestyle="--", marker="s", markersize=3.5, markerfacecolor="white",
            label="Bottom 30% (90% band dotted)")
    ax.axhline(0, color=BLACK, linewidth=0.6)
    ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel("Months after the shock")
    ax.set_ylabel("Cumulative response (% per 1% fuel)")
    ax.legend(loc="lower right")
    save(fig, "figP1_passthrough")

    fig, ax = plt.subplots(figsize=(5.4, 3.3))
    ax.fill_between(gap.h, gap.lo, gap.hi, color=LIGHT, linewidth=0)
    ax.plot(gap.h, gap.beta, color=BLACK, marker="o", markersize=3.5)
    ax.axhline(0, color=BLACK, linewidth=0.6)
    ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel("Months after the shock")
    ax.set_ylabel("Cumulative response (pp per 1% fuel)")
    ax.text(0.2, gap.lo.min() * 0.98, "Below zero: the bottom 30%'s prices rise more", fontsize=8)
    save(fig, "figP2_gap")

    h6 = est[est.h == 6]
    pick = lambda spec, y="d_ratio": h6[(h6.spec == spec) & (h6.outcome == y)].iloc[0]  # noqa: E731
    rows = [("Baseline", pick("baseline")), ("Excluding 2008", pick("excl 2008")),
            ("2001–2012", pick("2001-2012")), ("2013–2026", pick("2013-2026")),
            ("Shock: Dubai crude in pesos", pick("crude in pesos")),
            ("Controls: exchange rate, policy rate, world food prices", pick("macro and food controls")),
            ("Control: world food prices only", pick("food price control"))][::-1]
    loo = h6[h6.rq == "LOO"]
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    for i, (lab, r) in enumerate(rows, start=1):
        ax.errorbar(r.beta, i, xerr=[[r.beta - r.lo], [r.hi - r.beta]], fmt="o", color=BLACK, ecolor=BLACK,
                    markersize=4.5, capsize=2, elinewidth=1.0)
    ax.plot([loo.beta.min(), loo.beta.max()], [0, 0], color=BLACK, linewidth=4, solid_capstyle="butt")
    ax.set_yticks(range(len(rows) + 1), ["One region left out (range)"] + [r[0] for r in rows])
    ax.axvline(0, color=BLACK, linewidth=0.6)
    ax.set_xlabel("Cumulative response of the gap after 6 months (pp per 1% shock), 90% CI")
    save(fig, "figP3_robustness")

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.7))
    titles = {"d_cpi_all": "(a) All households", "d_cpi_b30": "(b) Bottom 30%", "d_ratio": "(c) Gap, all − bottom 30%"}
    for ax, (y, t) in zip(axes, titles.items()):
        q = path[path.series == y]
        x = range(len(q))
        ax.fill_between(x, q.lo, q.hi, color=LIGHT, linewidth=0)
        ax.plot(x, q.actual, color=BLACK, marker="o", markersize=3, label="Actual")
        ax.plot(x, q.fuel_driven, color=BLACK, linestyle="--", marker="s", markersize=3, markerfacecolor="white",
                label="Predicted from fuel (90% band)")
        ax.axhline(0, color=BLACK, linewidth=0.6)
        ax.set_xticks(list(x), [m.strftime("%b")[0] for m in M26])
        ax.set_title(t, loc="left", fontsize=9)
    axes[0].set_ylabel("Change since Dec 2025 (100 × log)")
    h_, l_ = axes[0].get_legend_handles_labels()
    fig.legend(h_, l_, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.1))
    fig.tight_layout()
    save(fig, "figP4_2026")


# ---------------------------------------------------------------- numbers for the manuscript
def numbers(est, path, cost, regions, res, nat):
    n = {}
    g = lambda rq, spec, y, h: est[(est.rq == rq) & (est.spec == spec) & (est.outcome == y) & (est.h == h)].iloc[0]  # noqa: E731
    for y, k in [("d_cpi_all", "all"), ("d_cpi_b30", "b30")]:
        for h in (0, 3, 6, 12):
            r = g("RQ1", "baseline", y, h)
            n[f"p_{k}_c{h}"], n[f"p_{k}_c{h}_se"] = f(r.beta), f(r.se)
    n["p_all_c12_10pct"] = f(10 * g("RQ1", "baseline", "d_cpi_all", 12).beta, 1)
    n["p_crude_c12"] = f(g("ROB", "crude in pesos", "d_cpi_all", 12).beta)
    for h in (0, 6, 12):
        for y, k in [("d_cpi_all", "all"), ("d_cpi_b30", "b30")]:
            r = g("ROB", "crude in pesos", y, h)
            n[f"crude_{k}_c{h}"], n[f"crude_{k}_c{h}_se"] = f(r.beta), f(r.se)
    for h in (0, 1, 3, 6, 9, 12):
        n[f"diff_c{h}"] = f(g("RQ1", "baseline", "d_cpi_b30", h).beta - g("RQ1", "baseline", "d_cpi_all", h).beta, 3)
    loo12x = est[(est.rq == "LOO") & (est.h == 12)]
    n["loo12_min"], n["loo12_max"] = f(loo12x.beta.min(), 4), f(loo12x.beta.max(), 4)
    n["p_crude_share"] = f(100 * g("ROB", "crude in pesos", "d_cpi_all", 12).beta / g("RQ1", "baseline", "d_cpi_all", 12).beta, 0)
    gap = est[(est.rq == "RQ2") & (est.spec == "baseline")]
    sig = gap[(gap.hi < 0) | (gap.lo > 0)].h.tolist()
    n["gap_sig_from"], n["gap_sig_to"], n["gap_sig_n"] = min(sig), max(sig), len(sig)
    for h in (1, 3, 6, 12):
        r = g("RQ2", "baseline", "d_ratio", h)
        n[f"gap_c{h}"], n[f"gap_c{h}_se"] = f(r.beta, 4), f(r.se, 4)
        n[f"gap_c{h}_t"] = f(abs(r.beta / r.se), 2)
    n["gap6_10pct"] = f(-10 * g("RQ2", "baseline", "d_ratio", 6).beta, 2)
    n["all6_10pct"] = f(10 * g("RQ1", "baseline", "d_cpi_all", 6).beta, 2)
    n["gap_rel_pct"] = f(100 * -g("RQ2", "baseline", "d_ratio", 6).beta / g("RQ1", "baseline", "d_cpi_all", 6).beta, 0)
    n["diff_sep_c6"] = f(g("RQ1", "baseline", "d_cpi_b30", 6).beta - g("RQ1", "baseline", "d_cpi_all", 6).beta, 4)
    for spec, k in [("excl 2008", "x08"), ("2001-2012", "p1"), ("2013-2026", "p2"), ("crude in pesos", "crude"),
                    ("macro and food controls", "ctl"), ("food price control", "food")]:
        for h in (6, 12):
            r = g("ROB", spec, "d_ratio", h)
            n[f"rob_{k}_c{h}"], n[f"rob_{k}_c{h}_se"] = f(r.beta, 4), f(r.se, 4)
    loo6, loo12 = est[(est.rq == "LOO") & (est.h == 6)], est[(est.rq == "LOO") & (est.h == 12)]
    n["loo_min"], n["loo_max"] = f(loo6.beta.min(), 4), f(loo6.beta.max(), 4)
    n["loo_sig_all"] = bool((loo6.hi < 0).all())
    # 2026
    last = path[path.date == M26[-1].date()].set_index("series")
    for y, k in [("d_cpi_all", "all"), ("d_cpi_b30", "b30"), ("d_ratio", "gap")]:
        r = last.loc[y]
        n[f"e_{k}_fd"], n[f"e_{k}_lo"], n[f"e_{k}_hi"], n[f"e_{k}_act"] = (f(r.fuel_driven, 2), f(r.lo, 2), f(r.hi, 2),
                                                                           f(r.actual, 2))
        n[f"e_{k}_share"] = f(100 * r.fuel_driven / r.actual, 0)
    n["e_fuel_cum_aug"] = f(last.loc["d_cpi_all", "fuel_cum"], 1)
    n["e_fuel_cum_apr"] = f(path[(path.series == "d_cpi_all") & (path.date == M26[3].date())].fuel_cum.iloc[0], 1)
    n["e_p_gap_nonneg"] = f(cost["p_gap_nonneg"], 3)
    for k in ("line", "cost_b30", "cost_b30_lo", "cost_b30_hi", "extra", "extra_lo", "extra_hi", "actual_cost_b30"):
        n[f"php_{k}"] = f"{cost[k]:,.0f}"
    rr = regions.set_index("region")
    lo, hi = rr.cost_php_month.idxmin(), rr.cost_php_month.idxmax()
    n["php_reg_min"], n["php_reg_min_name"] = f"{rr.cost_php_month[lo]:,.0f}", rr.region_name[lo]
    n["php_reg_max"], n["php_reg_max_name"] = f"{rr.cost_php_month[hi]:,.0f}", rr.region_name[hi]
    n["n_regions"] = int(regions.shape[0])
    n["obs_h0"] = f"{int(g('RQ2', 'baseline', 'd_ratio', 0).nobs):,}"
    n["obs_h12"] = f"{int(g('RQ2', 'baseline', 'd_ratio', 12).nobs):,}"
    n["b_reps"], n["block"] = f"{B_REPS:,}", BLOCK
    return n


def geo_numbers(n, geo, tests):
    for y, k in [("d_cpi_all", "all"), ("d_ratio", "gap")]:
        for h in (6, 12):
            q = geo[(geo.outcome == y) & (geo.h == h)]
            tt = tests[(tests.outcome == y) & (tests.h == h)].iloc[0]
            d = 3 if k == "all" else 4
            lo, hi = q.loc[q.beta.idxmin()], q.loc[q.beta.idxmax()]
            n[f"geo_{k}_c{h}_min"], n[f"geo_{k}_c{h}_min_name"] = f(lo.beta, d), lo.region_name
            n[f"geo_{k}_c{h}_max"], n[f"geo_{k}_c{h}_max_name"] = f(hi.beta, d), hi.region_name
            n[f"geo_{k}_c{h}_mean"], n[f"geo_{k}_c{h}_sd"] = f(q.beta.mean(), d), f(q.beta.std(), d)
            n[f"geo_{k}_c{h}_wald"], n[f"geo_{k}_c{h}_p"] = f(tt.wald, 1), f(tt.p, 3)
            n[f"geo_{k}_c{h}_nsig"] = int((q.hi < 0).sum() if k == "gap" else (q.lo > 0).sum())
            n[f"geo_{k}_c{h}_npos"] = int((q.beta > 0).sum())
            n[f"geo_{k}_c{h}_corr_pov"] = f(q.beta.corr(q.poverty_2018), 2)
            n[f"geo_{k}_c{h}_corr_food"] = f(q.beta.corr(q.food_share_2018), 2)
    q = geo[(geo.outcome == "d_ratio") & (geo.h == 6)].sort_values("beta")
    n["geo_gap_top3"] = ", ".join(q.region_name.head(3))
    n["geo_wald_df"] = int(geo.region.nunique() - 1)



def expected_for_stata(est, path, cost, geo=None, tests=None):
    out = ROOT / "code" / "stata" / "teaching"
    out.mkdir(parents=True, exist_ok=True)
    keep = est[est.rq.isin(["RQ1", "RQ2", "ROB"]) | est.spec.isin(["drop NCR", "drop BARMM"])]
    keep[["rq", "spec", "outcome", "shock", "h", "beta", "se", "nobs"]].to_csv(
        out / "expected_panel.csv", index=False, float_format="%.10g")
    last = path[path.date == M26[-1].date()][["series", "fuel_driven", "actual"]]
    last.to_csv(out / "expected_2026.csv", index=False, float_format="%.10g")
    if geo is not None:
        geo[["region", "outcome", "h", "beta", "se", "nobs"]].to_csv(out / "expected_regions.csv", index=False,
                                                                     float_format="%.10g")
        tests.to_csv(out / "expected_regions_wald.csv", index=False, float_format="%.10g")


def main():
    reg, nat = panel_data()
    est = estimates(reg)
    path, cost, regions, res = application_2026(reg, nat)
    figures(est, path)
    geo, tests = geography(reg)
    figure_regions(geo, est)
    n = numbers(est, path, cost, regions, res, nat)
    geo_numbers(n, geo, tests)
    (TAB / "panel_numbers.json").write_text(json.dumps(n, indent=1, ensure_ascii=False))
    expected_for_stata(est, path, cost, geo, tests)
    print(f"panel study: {len(est)} estimates; gap h6 {n['gap_c6']} ({n['gap_c6_se']}); "
          f"2026 gap fuel-driven {n['e_gap_fd']} [{n['e_gap_lo']}, {n['e_gap_hi']}] vs actual {n['e_gap_act']}; "
          f"extra cost PHP {n['php_extra']} [{n['php_extra_lo']}, {n['php_extra_hi']}]")


if __name__ == "__main__":
    main()
