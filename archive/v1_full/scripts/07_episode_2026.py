"""2026 episode and mechanism analyses (D10, "2026 episode plan" in CLAUDE.md).

E1  national out-of-sample test: pre-2026 estimates applied to the 2026 fuel path
E2  regional fuel-driven rise in CPI_all and CPI_b30, Jan-Aug 2026
E3  peso cost for a poverty-line family of five
E4  mechanism: bottom-30% vs all-income sub-indices (2013-2026)
E5  descriptive: contribution of each item group to the actual Dec 2025-Aug 2026
    rise in each basket (fixed-base Laspeyres, 2018 weights); no model

Writes output/tables/e1_national_2026.csv, e2_regional_2026.csv,
e4_mechanism.csv, e5_decomposition_2026.csv and context_2026.csv.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ospd.lp import local_projection  # noqa: E402
from ospd.regions import REGIONS_17, region_code  # noqa: E402

PROC = ROOT / "data" / "processed"
OUT = ROOT / "output" / "tables"
CUTOFF = pd.Timestamp("2025-12-01")
MONTHS_2026 = pd.date_range("2026-01-01", "2026-08-01", freq="MS")
H = 12


def cum_irf(df, y, unit=None, se="newey_west"):
    """Cumulative IRF of y to d_fuel estimated on data up to CUTOFF only."""
    d = df[df.date <= CUTOFF].reset_index(drop=True)
    r = local_projection(d, y, "d_fuel", time="t", unit=unit, horizons=H, p=12, se=se,
                         sample=d.date >= "2001-01-01", cumulative=True)
    return r[r.term == "shock"].set_index("h")


def fuel_driven(irf, fuel):
    """Fuel-driven change in 100*ln P from Dec 2025 to each month of 2026.

    fuel: Series of d_fuel indexed by MONTHS_2026. Returns point and a
    comonotone band (all horizons at their 90% bound together; conservative).
    """
    out = {}
    for k, m in enumerate(MONTHS_2026):
        shocks = fuel.iloc[: k + 1].to_numpy()
        lags = np.arange(k, -1, -1)  # horizon of each shock at month m
        out[m] = {col: float(np.sum(irf.loc[lags, col].to_numpy() * shocks)) for col in ("beta", "lo", "hi")}
    res = pd.DataFrame(out).T
    # with negative shocks lo/hi swap roles; keep the band ordered
    res["lo"], res["hi"] = res[["lo", "hi"]].min(axis=1), res[["lo", "hi"]].max(axis=1)
    return res


def actual(series):
    base = series.loc[CUTOFF]
    return 100 * np.log(series.loc[MONTHS_2026] / base)


def poverty_thresholds():
    pov = pd.read_csv(ROOT / "data" / "raw" / "psa" / "poverty_population_2018_2023.csv", encoding="latin-1")
    lab = pov.iloc[:, 0]
    pov = pov[lab.str.match(r"^\.\.[^.]") | lab.str.startswith("PHILIPPINES")].copy()
    pov["region"] = pov.iloc[:, 0].str.replace(r"(\s+([0-9]+|[a-z]+[0-9]*)/,?)+\s*$", "", regex=True).str.replace(
        r"\s+r\d.*$", "", regex=True).map(region_code)
    pov = pov.set_index("region")
    return pd.DataFrame({
        "threshold_2023": pd.to_numeric(pov["Annual Per Capita Poverty Threshold (in PhP) 2023"], errors="coerce"),
        "poverty_2018": pd.to_numeric(pov["Poverty Incidence among Population (%) 2018"], errors="coerce"),
    })


def main():
    panel = pd.read_parquet(PROC / "panel_regional.parquet")
    nat = panel[panel.region == "PH"].sort_values("date").reset_index(drop=True)
    reg = panel[panel.region.isin(REGIONS_17)].sort_values(["region", "date"]).reset_index(drop=True)
    thr = poverty_thresholds()

    # context: year-on-year inflation in 2026
    ctx = nat.set_index("date")[["cpi_all", "cpi_b30", "fuel"]]
    yoy = (100 * (ctx / ctx.shift(12) - 1)).loc["2025-10-01":"2026-08-01"].round(2)
    yoy.columns = ["inflation_all_yoy", "inflation_b30_yoy", "fuel_yoy"]
    yoy.to_csv(OUT / "context_2026.csv")

    # E1 national
    fuel_nat = nat.set_index("date").d_fuel.loc[MONTHS_2026]
    rows = []
    for y, lvl in [("d_cpi_all", "cpi_all"), ("d_cpi_b30", "cpi_b30")]:
        fd = fuel_driven(cum_irf(nat, y), fuel_nat)
        fd["actual"] = actual(nat.set_index("date")[lvl])
        fd["series"] = lvl
        rows.append(fd)
    e1 = pd.concat(rows).rename_axis("date").reset_index()
    gap_irf = cum_irf(nat, "d_ratio")
    g = fuel_driven(gap_irf, fuel_nat)
    g["actual"] = actual(nat.set_index("date").cpi_all) - actual(nat.set_index("date").cpi_b30)
    g["series"] = "ratio_all_over_b30"
    e1 = pd.concat([e1, g.rename_axis("date").reset_index()], ignore_index=True)
    e1["fuel_cum"] = e1.date.map(100 * np.log(nat.set_index("date").fuel.loc[MONTHS_2026] /
                                               nat.set_index("date").fuel.loc[CUTOFF]))
    e1.to_csv(OUT / "e1_national_2026.csv", index=False)

    # E2 regional, E3 peso cost
    irf_all = cum_irf(reg, "d_cpi_all", unit="region", se="driscoll_kraay")
    irf_b30 = cum_irf(reg, "d_cpi_b30", unit="region", se="driscoll_kraay")
    out = []
    for r in REGIONS_17 + ["PH"]:
        src = nat if r == "PH" else reg[reg.region == r]
        s = src.set_index("date")
        f = s.d_fuel.loc[MONTHS_2026]
        fa = fuel_driven(irf_all if r != "PH" else cum_irf(nat, "d_cpi_all"), f).loc[MONTHS_2026[-1]]
        fb = fuel_driven(irf_b30 if r != "PH" else cum_irf(nat, "d_cpi_b30"), f).loc[MONTHS_2026[-1]]
        cpi23 = s.cpi_b30.loc["2023-01-01":"2023-12-01"].mean()
        monthly_thr = thr.threshold_2023.get(r, np.nan) * 5 / 12 * s.cpi_b30.loc[CUTOFF] / cpi23
        out.append({
            "region": r,
            "poverty_2018": thr.poverty_2018.get(r, np.nan),
            "fuel_change_pct": 100 * np.log(s.fuel.loc[MONTHS_2026[-1]] / s.fuel.loc[CUTOFF]),
            "fuel_peak_pct": 100 * np.log(s.fuel.loc[MONTHS_2026].max() / s.fuel.loc[CUTOFF]),
            "fuel_driven_all": fa.beta, "fuel_driven_b30": fb.beta,
            "fuel_driven_b30_lo": fb.lo, "fuel_driven_b30_hi": fb.hi,
            "actual_all": actual(s.cpi_all).iloc[-1], "actual_b30": actual(s.cpi_b30).iloc[-1],
            "poverty_line_family5_monthly_dec2025": monthly_thr,
            "extra_cost_php_month": monthly_thr * (np.exp(fb.beta / 100) - 1),
            "new_geo_ext": bool(s.new_geo_ext.loc[MONTHS_2026].any()) if r != "PH" else False,
        })
    e2 = pd.DataFrame(out)
    e2.to_csv(OUT / "e2_regional_2026.csv", index=False)

    # E4 mechanism, 2013-2026, full data
    w = pd.read_parquet(PROC / "psa_cpi_weights.parquet")
    w = w[w.region == "PH"]
    wt = {b: w[w.file == f"cpi_{b}_2018old_weights"].set_index("commodity_code").weight for b in ("all", "b30")}
    codes = {"e045": "04.5", "e0452": "04.5.2", "e0453": "04.5.3", "e0454": "04.5.4", "t073": "07.3", "f0111": "01.1.1"}
    mech = []
    for name, code in codes.items():
        for b in ("all", "b30"):
            r = local_projection(nat, f"d_{b}_{name}", "d_fuel", time="t", horizons=H, p=12, se="newey_west",
                                 sample=nat.date >= "2013-01-01", cumulative=True)
            r = r[(r.term == "shock") & r.h.isin([6, 12])]
            for _, row in r.iterrows():
                mech.append({"item": name, "coicop": code, "basket": b, "h": row.h, "beta": row.beta,
                             "se": row.se, "weight": wt[b].get(code, np.nan),
                             "contribution": row.beta * wt[b].get(code, np.nan) / 100})
    e4 = pd.DataFrame(mech)
    e4.to_csv(OUT / "e4_mechanism.csv", index=False)

    # E5 descriptive decomposition of the actual 2026 rise (new geographic code tables)
    long = pd.read_parquet(PROC / "psa_cpi_long.parquet")
    wall = pd.read_parquet(PROC / "psa_cpi_weights.parquet")
    rows = []
    for b in ("all", "b30"):
        q = long[(long.file == f"cpi_{b}_2018new_2018_2026") & (long.region == "PH")]
        ww = wall[(wall.file == f"cpi_{b}_2018new_weights") & (wall.region == "PH")].set_index("commodity_code").weight
        px = q.pivot(index="date", columns="commodity_code", values="value")
        names = q.drop_duplicates("commodity_code").set_index("commodity_code").commodity
        groups = [c for c in ww.index if pd.Series(c).str.match(r"^\d{2}\.\d$").iloc[0]]
        groups += ["01.1.1", "01.1.1.1", "01.1.3", "04.5.2", "04.5.3", "04.5.4", "07.2.2", "07.3.2"]
        base = px.loc[CUTOFF, "0"]
        for c in groups:
            if c in px:
                rows.append({"basket": b, "coicop": c, "item": names.get(c, ""), "weight": ww.get(c),
                             "pct_change": 100 * (px.loc[MONTHS_2026[-1], c] / px.loc[CUTOFF, c] - 1),
                             "contribution_pp": ww.get(c) * (px.loc[MONTHS_2026[-1], c] - px.loc[CUTOFF, c]) / base})
        rows.append({"basket": b, "coicop": "0", "item": "ALL ITEMS", "weight": 100.0,
                     "pct_change": 100 * (px.loc[MONTHS_2026[-1], "0"] / base - 1),
                     "contribution_pp": 100 * (px.loc[MONTHS_2026[-1], "0"] / base - 1)})
    e5 = pd.DataFrame(rows).pivot_table(index=["coicop", "item"], columns="basket",
                                        values=["weight", "pct_change", "contribution_pp"])
    e5.columns = [f"{a}_{b}" for a, b in e5.columns]
    e5["gap_pp"] = e5.contribution_pp_b30 - e5.contribution_pp_all
    e5 = e5.reset_index()
    e5.to_csv(OUT / "e5_decomposition_2026.csv", index=False)
    print(e5.round(3).to_string(index=False))

    pd.set_option("display.width", 220)
    print(yoy.to_string())
    print(e1.round(3).to_string(index=False))
    print(e2.round(2).to_string(index=False))
    print(e4[e4.h == 12].pivot_table(index=["item", "coicop"], columns="basket",
                                     values=["beta", "se", "weight", "contribution"]).round(4).to_string())


if __name__ == "__main__":
    main()
