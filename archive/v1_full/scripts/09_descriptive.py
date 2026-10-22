"""Descriptive statistics and trend analysis (working paper Objective 1; D11).

No model: summary statistics, annual inflation, fuel-shock episodes,
correlations, regional summaries and unit-root tests.

Writes output/tables/desc_*.csv.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ospd.regions import REGIONS_17  # noqa: E402

PROC = ROOT / "data" / "processed"
OUT = ROOT / "output" / "tables"
START, END = "2001-01-01", "2026-08-01"
VARS = {"d_fuel": "Fuel index (07.2.2)", "d_cpi_all": "CPI, all income", "d_cpi_b30": "CPI, bottom 30%",
        "d_ratio": "Gap: ln(CPI all/CPI b30)"}
PERIODS = {"2001–2026 (full)": (START, END), "2001–2012": (START, "2012-12-01"),
           "2013–2019": ("2013-01-01", "2019-12-01"), "2020–2025": ("2020-01-01", "2025-12-01"),
           "2026 (Jan–Aug)": ("2026-01-01", END)}


def main():
    panel = pd.read_parquet(PROC / "panel_regional.parquet")
    nat = panel[panel.region == "PH"].set_index("date").sort_index()
    for c in ["cpi_all", "cpi_b30", "fuel"]:
        nat[f"yoy_{c}"] = 100 * (nat[c] / nat[c].shift(12) - 1)
    nat["yoy_gap"] = nat.yoy_cpi_b30 - nat.yoy_cpi_all

    # 1. summary statistics of monthly changes, by period
    rows = []
    for pname, (a, b) in PERIODS.items():
        s = nat.loc[a:b]
        for v, lab in VARS.items():
            x = s[v].dropna()
            rows.append({"period": pname, "variable": lab, "n": len(x), "mean": x.mean(), "sd": x.std(),
                         "min": x.min(), "max": x.max(), "annualised_mean": 12 * x.mean()})
    pd.DataFrame(rows).to_csv(OUT / "desc_summary.csv", index=False)

    # 2. annual inflation (average of monthly year-on-year rates)
    yr = nat.loc["2001-01-01":END, ["yoy_cpi_all", "yoy_cpi_b30", "yoy_gap", "yoy_fuel"]]
    annual = yr.groupby(yr.index.year).mean()
    annual.index.name = "year"
    annual.to_csv(OUT / "desc_annual.csv")

    # 3. fuel-shock episodes: runs of months with fuel up >= 15% y/y
    flag = nat.loc["2001-01-01":END, "yoy_fuel"] >= 15
    runs, cur = [], []
    for d, f in flag.items():
        if f:
            cur.append(d)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    ep = []
    for r in runs:
        if len(r) < 3:
            continue
        s = nat.loc[r[0]:r[-1]]
        ep.append({"start": r[0].strftime("%Y-%m"), "end": r[-1].strftime("%Y-%m"), "months": len(r),
                   "peak_fuel_yoy": s.yoy_fuel.max(), "mean_infl_all": s.yoy_cpi_all.mean(),
                   "mean_infl_b30": s.yoy_cpi_b30.mean(), "mean_gap_b30_minus_all": s.yoy_gap.mean()})
    pd.DataFrame(ep).to_csv(OUT / "desc_episodes.csv", index=False)

    # 4. correlations of fuel changes with later price changes (lags 0..12)
    s = nat.loc[START:END]
    cc = [{"lag": k, **{lab: s.d_fuel.corr(s[v].shift(-k)) for v, lab in list(VARS.items())[1:]}} for k in range(13)]
    pd.DataFrame(cc).to_csv(OUT / "desc_crosscorr.csv", index=False)

    # 5. regional summary
    groups = pd.read_csv(OUT / "region_groups.csv").set_index("region")
    # national values: poverty from the 2026 episode table, food share from the national weights
    e2 = pd.read_csv(OUT / "e2_regional_2026.csv").set_index("region")
    w = pd.read_parquet(PROC / "psa_cpi_weights.parquet")
    w = w[(w.file == "cpi_all_2018old_weights") & (w.region == "PH")].set_index("commodity_code").weight
    groups.loc["PH", ["poverty_2018", "food_share_2018"]] = [e2.loc["PH", "poverty_2018"], 100 * w["01"] / w["0"]]
    reg = []
    for r in REGIONS_17 + ["PH"]:
        q = panel[panel.region == r].set_index("date").sort_index()
        yoy_all = 100 * (q.cpi_all / q.cpi_all.shift(12) - 1)
        yoy_b30 = 100 * (q.cpi_b30 / q.cpi_b30.shift(12) - 1)
        reg.append({
            "region": r,
            "infl_all_2001_2025": yoy_all.loc["2001-01-01":"2025-12-01"].mean(),
            "infl_b30_2001_2025": yoy_b30.loc["2001-01-01":"2025-12-01"].mean(),
            "cum_gap_2001_2025": 100 * (q.ratio.loc["2025-12-01"] - q.ratio.loc["2000-12-01"]),
            "fuel_sd_monthly": q.d_fuel.loc[START:END].std(),
            "infl_b30_aug2026_yoy": yoy_b30.loc[END], "infl_all_aug2026_yoy": yoy_all.loc[END],
            "poverty_2018": groups.poverty_2018.get(r, np.nan),
            "food_share_2018": groups.food_share_2018.get(r, np.nan),
        })
    pd.DataFrame(reg).to_csv(OUT / "desc_regional.csv", index=False)

    # 6. unit-root tests (ADF with constant, AIC lag choice), 2001-2026
    adf = []
    for v, lab in {"fuel": "ln fuel index", "cpi_all": "ln CPI all", "cpi_b30": "ln CPI b30"}.items():
        x = np.log(nat.loc[START:END, v]).dropna()
        for form, series in [("level", x), ("first difference", x.diff().dropna())]:
            stat, p, lags, nobs, *_ = adfuller(series, autolag="AIC", regression="ct" if form == "level" else "c")
            adf.append({"series": lab, "form": form, "adf_stat": stat, "p_value": p, "lags": lags, "nobs": nobs})
    x = nat.loc[START:END, "ratio"].dropna()
    for form, series in [("level", x), ("first difference", x.diff().dropna())]:
        stat, p, lags, nobs, *_ = adfuller(series, autolag="AIC", regression="ct" if form == "level" else "c")
        adf.append({"series": "ln(CPI all/CPI b30)", "form": form, "adf_stat": stat, "p_value": p,
                    "lags": lags, "nobs": nobs})
    pd.DataFrame(adf).to_csv(OUT / "desc_adf.csv", index=False)

    # 7. series for the trend figure
    nat.loc[START:END, ["yoy_cpi_all", "yoy_cpi_b30", "yoy_gap", "yoy_fuel"]].to_csv(OUT / "desc_yoy_national.csv")

    pd.set_option("display.width", 200)
    print(pd.read_csv(OUT / "desc_summary.csv").round(3).to_string(index=False))
    print(annual.round(2).to_string())
    print(pd.DataFrame(ep).round(2).to_string(index=False))
    print(pd.DataFrame(cc).round(3).to_string(index=False))
    print(pd.DataFrame(reg).round(2).to_string(index=False))
    print(pd.DataFrame(adf).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
