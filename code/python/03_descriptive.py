"""Objective 1: descriptive statistics and trend analysis (no model; decision D11).

Writes output/tables/
  desc_summary.csv        monthly changes by period: mean, SD, min, max, annualised mean      (core)
  desc_annual.csv         annual inflation of both groups, the gap and fuel                    (core)
  desc_episodes.csv       fuel-shock episodes (>= 3 months with fuel >= +15% year on year)     (core)
  desc_regional.csv       regional averages, cumulative gap, poverty and food share            (core)
  desc_adf.csv            augmented Dickey-Fuller unit-root tests                              (core)
  desc_yoy_national.csv   year-on-year series for the trends figure                            (core)
  desc_crosscorr.csv      correlations of fuel changes with later price changes               (appendix)
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

import data_io
from config import END, REGIONS_17, START, TAB

VARS = {"d_fuel": "Fuel index (07.2.2)", "d_cpi_all": "CPI, all income", "d_cpi_b30": "CPI, bottom 30%",
        "d_ratio": "Gap: ln(CPI all/CPI b30)"}
PERIODS = {"2001–2026 (full)": (START, END), "2001–2012": (START, "2012-12-01"),
           "2013–2019": ("2013-01-01", "2019-12-01"), "2020–2025": ("2020-01-01", "2025-12-01"),
           "2026 (Jan–Aug)": ("2026-01-01", END)}


def yoy(s):
    return 100 * (s / s.shift(12) - 1)


def main():
    TAB.mkdir(parents=True, exist_ok=True)
    nat = data_io.national().set_index("date")
    for c in ["cpi_all", "cpi_b30", "fuel"]:
        nat[f"yoy_{c}"] = yoy(nat[c])
    nat["yoy_gap"] = nat.yoy_cpi_b30 - nat.yoy_cpi_all

    rows = []
    for pname, (a, b) in PERIODS.items():
        s = nat.loc[a:b]
        for v, lab in VARS.items():
            x = s[v].dropna()
            rows.append({"period": pname, "variable": lab, "n": len(x), "mean": x.mean(), "sd": x.std(),
                         "min": x.min(), "max": x.max(), "annualised_mean": 12 * x.mean()})
    pd.DataFrame(rows).to_csv(TAB / "desc_summary.csv", index=False)

    yr = nat.loc[START:END, ["yoy_cpi_all", "yoy_cpi_b30", "yoy_gap", "yoy_fuel"]]
    annual = yr.groupby(yr.index.year).mean()
    annual.index.name = "year"
    annual.to_csv(TAB / "desc_annual.csv")

    flag = nat.loc[START:END, "yoy_fuel"] >= 15
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
    for r in [r for r in runs if len(r) >= 3]:
        s = nat.loc[r[0]:r[-1]]
        ep.append({"start": r[0].strftime("%Y-%m"), "end": r[-1].strftime("%Y-%m"), "months": len(r),
                   "peak_fuel_yoy": s.yoy_fuel.max(), "mean_infl_all": s.yoy_cpi_all.mean(),
                   "mean_infl_b30": s.yoy_cpi_b30.mean(), "mean_gap_b30_minus_all": s.yoy_gap.mean()})
    pd.DataFrame(ep).to_csv(TAB / "desc_episodes.csv", index=False)

    s = nat.loc[START:END]
    cc = [{"lag": k, **{lab: s.d_fuel.corr(s[v].shift(-k)) for v, lab in list(VARS.items())[1:]}} for k in range(13)]
    pd.DataFrame(cc).to_csv(TAB / "desc_crosscorr.csv", index=False)

    panel = data_io.panel()
    info = data_io.region_info()
    reg = []
    for r in REGIONS_17 + ["PH"]:
        q = (nat if r == "PH" else panel[panel.region == r].set_index("date")).sort_index()
        ya, yb = yoy(q.cpi_all), yoy(q.cpi_b30)
        reg.append({
            "region": r,
            "infl_all_2001_2025": ya.loc[START:"2025-12-01"].mean(),
            "infl_b30_2001_2025": yb.loc[START:"2025-12-01"].mean(),
            "cum_gap_2001_2025": q.ratio.loc["2025-12-01"] - q.ratio.loc["2000-12-01"],
            "fuel_sd_monthly": q.d_fuel.loc[START:END].std(),
            "infl_b30_aug2026_yoy": yb.loc[END], "infl_all_aug2026_yoy": ya.loc[END],
            "poverty_2018": info.poverty_2018.get(r), "food_share_2018": info.food_share_2018.get(r),
        })
    pd.DataFrame(reg).to_csv(TAB / "desc_regional.csv", index=False)

    adf = []
    series = {"ln fuel index": np.log(nat.fuel), "ln CPI all": np.log(nat.cpi_all),
              "ln CPI b30": np.log(nat.cpi_b30), "ln(CPI all/CPI b30)": nat.ratio / 100}
    for lab, x in series.items():
        x = x.loc[START:END].dropna()
        for form, z in [("level", x), ("first difference", x.diff().dropna())]:
            stat, p, lags, nobs, *_ = adfuller(z, autolag="AIC", regression="ct" if form == "level" else "c")
            adf.append({"series": lab, "form": form, "adf_stat": stat, "p_value": p, "lags": lags, "nobs": nobs})
    pd.DataFrame(adf).to_csv(TAB / "desc_adf.csv", index=False)

    nat.loc[START:END, ["yoy_cpi_all", "yoy_cpi_b30", "yoy_gap", "yoy_fuel"]].to_csv(TAB / "desc_yoy_national.csv")
    print(pd.DataFrame(rows).round(3).head(4).to_string(index=False))
    print(pd.DataFrame(ep).round(2).to_string(index=False))


if __name__ == "__main__":
    main()
