"""Objective 2: local projections for RQ1 and RQ2, the "why" decomposition and robustness checks.

Every model is estimated per horizon (h = 0..12) and cumulatively (running-sum outcome).
Writes output/tables/
  estimates.csv                 every coefficient path, with a column `core` (1 = main text, 0 = appendix)
  rq2_weights_decomposition.csv  RQ2 "why": category responses x difference in basket weights

Core (main text):
  RQ1  national: all-income CPI and bottom-30% CPI on the fuel index
  RQ2  national gap, and the 17-region pooled panel of the gap
  WHY  13 CPI divisions (all income), and four divisions in both baskets from 2013 (exploratory, D9)
  ROB  crude oil in pesos; macro controls; excluding 2020; 2001-2012 vs 2013-2026 (panel);
       leaving out one region at a time
Appendix: region-group interactions and every other robustness check.
"""

import numpy as np
import pandas as pd

import data_io
from config import H, P, REGIONS_17, ROOT, START, TAB
from lp import local_projection
from statsmodels.tsa.api import VAR

DIVISIONS = {
    "c01": "Food and non-alcoholic beverages", "c02": "Alcoholic beverages and tobacco",
    "c03": "Clothing and footwear", "c04": "Housing, water, electricity, gas",
    "c05": "Furnishings and household equipment", "c06": "Health", "c07": "Transport",
    "c08": "Information and communication", "c09": "Recreation, sport and culture",
    "c10": "Education services", "c11": "Restaurants and accommodation",
    "c12": "Financial services", "c13": "Personal care and miscellaneous",
}
GROUPS = ["high_poverty", "high_food", "mindanao", "island"]


class Runner:
    def __init__(self):
        self.rows = []

    def __call__(self, df, y, x, rq, spec, core, unit=None, se="newey_west", start=START, end=None,
                 drop=None, **kw):
        mask = df.date >= start
        if end:
            mask &= df.date <= end
        if drop is not None:
            mask &= ~drop
        horizons, p = kw.pop("horizons", H), kw.pop("p", P)
        for cum in (False, True):
            r = local_projection(df, y, x, time="t", unit=unit, horizons=horizons, p=p, se=se,
                                 sample=mask, cumulative=cum, **kw)
            r.insert(0, "cumulative", cum)
            r.insert(0, "shock", x)
            r.insert(0, "outcome", y)
            r.insert(0, "spec", spec)
            r.insert(0, "core", int(core))
            r.insert(0, "rq", rq)
            self.rows.append(r)

    def frame(self):
        return pd.concat(self.rows, ignore_index=True)


def main():
    nat = data_io.national()
    reg = data_io.panel()
    info = data_io.region_info()
    for g in GROUPS:
        reg[g] = reg.region.map(info[g])
    run = Runner()
    dk = dict(unit="region", se="driscoll_kraay")

    # RQ1 and RQ2 (core)
    run(nat, "d_cpi_all", "d_fuel", "RQ1", "baseline", True)
    run(nat, "d_cpi_b30", "d_fuel", "RQ1", "baseline", True)
    run(nat, "d_ratio", "d_fuel", "RQ2", "national", True)
    run(reg, "d_ratio", "d_fuel", "RQ2", "panel", True, **dk)

    # RQ2 "why": divisions (core, full table in the appendix) and both baskets from 2013 (exploratory)
    for c in DIVISIONS:
        run(nat, f"d_{c}", "d_fuel", "WHY", "division", True)
    for c in ["c01", "c04", "c07", "c11"]:
        run(nat, f"d_{c}", "d_fuel", "WHY", "2013- all income", True, start="2013-01-01")
        run(nat, f"d_b30_{c}", "d_fuel", "WHY", "2013- bottom 30%", True, start="2013-01-01")

    # Core robustness
    for y in ["d_cpi_all", "d_ratio"]:
        run(nat, y, "d_dubai_php", "ROB", "dubai crude php", True)
        run(nat, y, "d_fuel", "ROB", "macro controls", True, controls=("d_php_usd", "d_policy_rate", "d_ffpi"))
        run(nat, y, "d_fuel", "ROB", "excl 2020", True, drop=nat.date.dt.year == 2020)
        run(nat, y, "d_fuel", "ROB", "TZ leads 1..h", True, tz="full")          # decision D13
        run(nat, y, "d_fuel", "VARCHK", "LP no leads", False, tz=False)         # decision D14
    run(reg, "d_ratio", "d_fuel", "ROB", "panel TZ leads 1..h", True, tz="full", **dk)
    run(reg, "d_ratio", "d_fuel", "ROB", "panel 2001-2012", True, end="2012-12-01", **dk)
    run(reg, "d_ratio", "d_fuel", "ROB", "panel 2013-2026", True, start="2013-01-01", **dk)
    for r in REGIONS_17:
        sub = reg[reg.region != r].reset_index(drop=True)
        run(sub, "d_ratio", "d_fuel", "ROB", f"drop {r}", True, **dk)

    # Appendix: region groups and the other robustness checks
    for g in GROUPS:
        run(reg, "d_ratio", "d_fuel", "APP", f"x {g}", False, interact=(g,), **dk)
    for y in ["d_cpi_all", "d_ratio"]:
        run(nat, y, "d_fuel", "APP", "p=6", False, p=6)
        run(nat, y, "d_fuel", "APP", "p=18", False, p=18)
        run(nat, y, "d_fuel", "APP", "excl 2026", False, end="2025-12-01")
        run(nat, y, "d_fuel", "APP", "splice dummies", False, exog=("jan2012", "jan2018"))
        run(nat, y, "d_fuel", "APP", "asymmetry", False, interact=("pos",))
        run(nat, y, "d_fuel", "APP", "to Jun 2019", False, end="2019-06-01")
        run(nat, y, "d_gasoline", "APP", "gasoline 07.2.2.2", False, start="2019-01-01")
        run(nat, y, "d_wb_gasoline_php", "APP", "WB pump price", False, start="2018-01-01")
    run(nat, "d_ratio", "d_fuel", "APP", "national excl 2008", False, drop=nat.date.dt.year == 2008)
    run(reg, "d_ratio", "d_fuel", "APP", "panel excl 2008", False, drop=reg.date.dt.year == 2008, **dk)
    run(reg, "d_ratio", "d_fuel", "APP", "drop flagged 2026", False, drop=reg.new_geo_ext == 1, **dk)
    run(reg, "d_ratio", "d_fuel_nat", "APP", "national shock", False, **dk)
    run(nat, "d_ratio", "d_fuel", "APP", "national 2013-2026", False, start="2013-01-01")

    est = run.frame()
    TAB.mkdir(parents=True, exist_ok=True)
    est.to_csv(TAB / "estimates.csv", index=False)

    # RQ2 "why": what the gap would be if both groups faced the same price change within each division
    wa, wb = data_io.weights("all"), data_io.weights("b30")
    cum = est[(est.rq == "WHY") & (est.spec == "division") & est.cumulative & (est.h == H)]
    cum = cum.assign(coicop=cum.outcome.str[3:]).set_index("coicop")
    dec = pd.DataFrame({"w_all": wa, "w_b30": wb}).loc[[f"{d:02d}" for d in range(1, 14)]].join(cum[["beta", "se"]])
    dec["division"] = [DIVISIONS[f"c{c}"] for c in dec.index]
    dec["contrib_all"] = dec.beta * dec.w_all / 100
    dec["contrib_b30"] = dec.beta * dec.w_b30 / 100
    dec["contrib_gap"] = dec.contrib_all - dec.contrib_b30
    dec.to_csv(TAB / "rq2_weights_decomposition.csv", index_label="coicop")

    var_check(nat, est)
    expected_results(est)

    s = est[est.cumulative & (est.term == "shock") & est.h.isin([0, 6, 12])]
    print(s[s.rq.isin(["RQ1", "RQ2"])].pivot_table(index=["rq", "spec", "outcome"], columns="h",
                                                   values="beta").round(4).to_string())
    print("weights-only gap:", round(dec.contrib_gap.sum(), 4))


def var_irf(nat, y, x="d_fuel", p=P, horizons=H, start=START, repl=1000):
    """VAR(p) in (fuel, y) with a constant and trend, fuel ordered first (Cholesky).

    Returns, for h = 0..H, the cumulative response of y to a fuel innovation scaled to 1% on impact
    ('var', with a 90% Monte Carlo band) and to a one-time 1% fuel change with later fuel held at zero
    ('var_onetime', the VAR counterpart of the local projection with Teulings-Zubanov leads).
    """
    first = pd.Timestamp(start) - pd.DateOffset(months=p)          # p pre-sample months supply the lags
    d = nat[nat.date >= first].set_index("date")[[x, y]].dropna()
    d.index.freq = "MS"
    res = VAR(d).fit(p, trend="ct")
    irf = res.irf(horizons)
    p00 = irf.orth_irfs[0, 0, 0]
    cum = np.cumsum(irf.orth_irfs[:, 1, 0]) / p00
    lo, hi = irf.cum_errband_mc(orth=True, repl=repl, signif=0.10, seed=0)
    a, sig = res.coefs, res.sigma_u.values
    b0 = sig[1, 0] / sig[0, 0]
    f = np.zeros(horizons + 1)
    f[0] = 1.0
    r = np.zeros(horizons + 1)
    for h in range(horizons + 1):
        r[h] = b0 * f[h] + sum(a[j - 1][1, 1] * r[h - j] + a[j - 1][1, 0] * f[h - j] for j in range(1, min(h, p) + 1))
    return pd.DataFrame({"h": range(horizons + 1), "var": cum, "var_lo": lo[:, 1, 0] / p00,
                         "var_hi": hi[:, 1, 0] / p00, "var_onetime": np.cumsum(r), "nobs": res.nobs})


def var_check(nat, est):
    """Supplementary check (decision D14): VAR with fuel first next to the local projections."""
    rows = []
    for y in ["d_cpi_all", "d_ratio"]:
        v = var_irf(nat, y)
        pick = lambda spec, rq: est[(est.rq == rq) & (est.spec == spec) & (est.outcome == y) & est.cumulative  # noqa: E731
                                    & (est.term == "shock")].set_index("h")
        base = pick("baseline" if y == "d_cpi_all" else "national", "RQ1" if y == "d_cpi_all" else "RQ2")
        v["lp"], v["lp_lo"], v["lp_hi"] = v.h.map(base.beta), v.h.map(base.lo), v.h.map(base.hi)
        v["lp_noleads"] = v.h.map(pick("LP no leads", "VARCHK").beta)
        v.insert(0, "outcome", y)
        rows.append(v)
    out = pd.concat(rows, ignore_index=True)
    out.to_csv(TAB / "var_comparison.csv", index=False)
    print(out[out.h.isin([0, 6, 12])].round(4).to_string(index=False))


def expected_results(est):
    """Cumulative estimates for the Stata replication to compare against (code/stata/07_compare.do)."""
    keep = est[est.cumulative & est.term.str.startswith("shock")].copy()
    keep = keep[~keep.spec.str.startswith("drop ") | keep.spec.isin(["drop NCR", "drop BARMM"])]
    cols = ["rq", "spec", "outcome", "shock", "term", "h", "beta", "se", "nobs"]
    out = ROOT / "code" / "stata" / "expected_results.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    keep[cols].to_csv(out, index=False, float_format="%.10g")


if __name__ == "__main__":
    main()
