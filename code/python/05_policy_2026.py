"""Objective 3 / RQ3: the 2026 oil shock and the policy response (decision D10).

Writes output/tables/
  rq3_context.csv          year-on-year inflation and fuel prices, Oct 2025-Aug 2026
  rq3_national.csv         (E1) models estimated on data to Dec 2025, applied to the 2026 fuel path,
                           against the actual change in each index
  rq3_regional.csv         (E2, E3) fuel-driven rise in each region and its peso cost for a family of
                           five at the official poverty line
  rq3_household_items.csv  (E4) responses of household fuels, fares and cereals in both baskets, 2013-2026
  rq3_decomposition.csv    (E5) contribution of each item group to the actual Dec 2025-Aug 2026 rise in each
                           basket (fixed-base Laspeyres, 2018 weights; descriptive, no model)
"""

import numpy as np
import pandas as pd

import data_io
from config import CLEAN, CUTOFF, H, REGIONS_17, START, TAB
from lp import local_projection

CUT = pd.Timestamp(CUTOFF)
MONTHS_2026 = pd.date_range("2026-01-01", "2026-08-01", freq="MS")
ITEMS = {"e0452": ("04.5.2", "LPG"), "e0453": ("04.5.3", "Kerosene and other liquid fuels"),
         "e0454": ("04.5.4", "Solid fuels (charcoal, wood)"), "t073": ("07.3", "Passenger transport services (fares)"),
         "f0111": ("01.1.1", "Cereals and cereal products"),
         "e045": ("04.5", "Electricity, gas and other fuels (total)")}


def cum_irf(df, y, unit=None, se="newey_west"):
    """Cumulative response of y to the fuel shock, estimated on data up to Dec 2025 only."""
    d = df[df.date <= CUT].reset_index(drop=True)
    r = local_projection(d, y, "d_fuel", time="t", unit=unit, horizons=H, p=12, se=se,
                         sample=d.date >= START, cumulative=True)
    return r[r.term == "shock"].set_index("h")


def fuel_driven(irf, fuel):
    """Fuel-driven change in 100 x ln P from Dec 2025 to each 2026 month: sum of B_(m-s) x f_s.

    The band puts every horizon at its 90% bound together (conservative, indicative only).
    """
    out = {}
    for k, m in enumerate(MONTHS_2026):
        shocks = fuel.iloc[: k + 1].to_numpy()
        lags = np.arange(k, -1, -1)
        out[m] = {c: float(np.sum(irf.loc[lags, c].to_numpy() * shocks)) for c in ("beta", "lo", "hi")}
    res = pd.DataFrame(out).T
    res["lo"], res["hi"] = res[["lo", "hi"]].min(axis=1), res[["lo", "hi"]].max(axis=1)
    return res


def actual(s):
    return 100 * np.log(s.loc[MONTHS_2026] / s.loc[CUT])


def main():
    nat = data_io.national()
    reg = data_io.panel()
    info = data_io.region_info()
    n = nat.set_index("date")

    ctx = n[["cpi_all", "cpi_b30", "fuel"]]
    yoy = (100 * (ctx / ctx.shift(12) - 1)).loc["2025-10-01":"2026-08-01"]
    yoy.columns = ["inflation_all_yoy", "inflation_b30_yoy", "fuel_yoy"]
    yoy.to_csv(TAB / "rq3_context.csv")

    # E1: national out-of-sample test
    fuel = n.d_fuel.loc[MONTHS_2026]
    rows = []
    for y, lvl in [("d_cpi_all", "cpi_all"), ("d_cpi_b30", "cpi_b30")]:
        fd = fuel_driven(cum_irf(nat, y), fuel)
        fd["actual"], fd["series"] = actual(n[lvl]), lvl
        rows.append(fd)
    g = fuel_driven(cum_irf(nat, "d_ratio"), fuel)
    g["actual"], g["series"] = actual(n.cpi_all) - actual(n.cpi_b30), "gap_all_minus_b30"
    e1 = pd.concat(rows + [g]).rename_axis("date").reset_index()
    e1["fuel_cum"] = e1.date.map(actual(n.fuel))
    e1.to_csv(TAB / "rq3_national.csv", index=False)

    # E2 and E3: regional fuel-driven rise and peso cost
    irf_all = cum_irf(reg, "d_cpi_all", unit="region", se="driscoll_kraay")
    irf_b30 = cum_irf(reg, "d_cpi_b30", unit="region", se="driscoll_kraay")
    irf_nat = {"all": cum_irf(nat, "d_cpi_all"), "b30": cum_irf(nat, "d_cpi_b30")}
    out = []
    for r in REGIONS_17 + ["PH"]:
        s = n if r == "PH" else reg[reg.region == r].set_index("date")
        f = s.d_fuel.loc[MONTHS_2026]
        fa = fuel_driven(irf_nat["all"] if r == "PH" else irf_all, f).loc[MONTHS_2026[-1]]
        fb = fuel_driven(irf_nat["b30"] if r == "PH" else irf_b30, f).loc[MONTHS_2026[-1]]
        cpi23 = s.cpi_b30.loc["2023-01-01":"2023-12-01"].mean()
        line = info.threshold_2023[r] * 5 / 12 * s.cpi_b30.loc[CUT] / cpi23
        out.append({
            "region": r, "poverty_2018": info.poverty_2018[r],
            "fuel_change_pct": 100 * np.log(s.fuel.loc[MONTHS_2026[-1]] / s.fuel.loc[CUT]),
            "fuel_driven_all": fa.beta, "fuel_driven_b30": fb.beta,
            "fuel_driven_b30_lo": fb.lo, "fuel_driven_b30_hi": fb.hi,
            "actual_all": actual(s.cpi_all).iloc[-1], "actual_b30": actual(s.cpi_b30).iloc[-1],
            "poverty_line_family5_monthly_dec2025": line,
            "extra_cost_php_month": line * (np.exp(fb.beta / 100) - 1),
            "new_geo_ext": int(r != "PH" and s.new_geo_ext.loc[MONTHS_2026].any()),
        })
    pd.DataFrame(out).to_csv(TAB / "rq3_regional.csv", index=False)

    # E4: household fuels, fares and cereals, both baskets, 2013-2026
    wt = {b: data_io.weights(b) for b in ("all", "b30")}
    mech = []
    for name, (code, label) in ITEMS.items():
        for b in ("all", "b30"):
            r = local_projection(nat, f"d_{b}_{name}", "d_fuel", time="t", horizons=H, p=12, se="newey_west",
                                 sample=nat.date >= "2013-01-01", cumulative=True)
            for _, row in r[(r.term == "shock") & r.h.isin([6, 12])].iterrows():
                mech.append({"item": name, "label": label, "coicop": code, "basket": b, "h": row.h,
                             "beta": row.beta, "se": row.se, "weight": wt[b].get(code, np.nan),
                             "core": int(name != "e045")})
    pd.DataFrame(mech).to_csv(TAB / "rq3_household_items.csv", index=False)

    # E5: descriptive decomposition of the actual Dec 2025-Aug 2026 rise
    items = pd.read_csv(CLEAN / "items_2026.csv", dtype={"coicop": str}, parse_dates=["date"])
    rows = []
    for b in ("all", "b30"):
        q = items[items.basket == b]
        px = q.pivot(index="date", columns="coicop", values="value")
        names = q.drop_duplicates("coicop").set_index("coicop").item
        w = data_io.weights(b, geo_code="new")
        base, last = px.loc[CUT, "0"], MONTHS_2026[-1]
        for c in [c for c in px.columns if c != "0"]:
            rows.append({"basket": b, "coicop": c, "item": names[c], "weight": w.get(c),
                         "pct_change": 100 * (px.loc[last, c] / px.loc[CUT, c] - 1),
                         "contribution_pp": w.get(c) * (px.loc[last, c] - px.loc[CUT, c]) / base})
        rows.append({"basket": b, "coicop": "0", "item": "ALL ITEMS", "weight": 100.0,
                     "pct_change": 100 * (px.loc[last, "0"] / base - 1),
                     "contribution_pp": 100 * (px.loc[last, "0"] / base - 1)})
    e5 = pd.DataFrame(rows).pivot_table(index=["coicop", "item"], columns="basket",
                                        values=["weight", "pct_change", "contribution_pp"])
    e5.columns = [f"{a}_{b}" for a, b in e5.columns]
    e5["gap_pp"] = e5.contribution_pp_b30 - e5.contribution_pp_all
    e5.reset_index().to_csv(TAB / "rq3_decomposition.csv", index=False)
    print(e1[e1.date == MONTHS_2026[-1]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
