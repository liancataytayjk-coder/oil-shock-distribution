"""Build the monthly analysis datasets.

Outputs (data/processed/):
  panel_regional.parquet  region x month, 2018=100 levels and 100*dlog changes
  macro_national.parquet  month: crude prices, exchange rate, policy rate,
                          FAO food price index, World Bank pump price

Splicing rules (decisions D5-D6 in CLAUDE.md):
  * Regions follow the old geographic code (17 regions, Negros still in VI/VII),
    because the bottom-30% backcasts exist only on that code.
  * Old-code tables end Dec 2025. Jan-Aug 2026 is appended by chaining the
    new-code series' monthly growth onto the old-code level. For regions whose
    boundaries changed (VI, VII, XII, BARMM) those months are flagged.
  * Bottom-30% all items: 2000-2011 backcast, 2012-2017 backcast, 2018- (2018=100).
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"

OLD = {
    "all": ["cpi_all_2018old_backcast_1994_2017", "cpi_all_2018old_2018_2025"],
    "b30": ["cpi_b30_2018old_backcast_allitems_2000_2011", "cpi_b30_2018old_backcast_2012_2017",
            "cpi_b30_2018old_2018_2025"],
}
NEW = {"all": "cpi_all_2018new_2018_2026", "b30": "cpi_b30_2018new_2018_2026"}
CHANGED_REGIONS = {"R06", "R07", "R12", "BARMM"}

SERIES = {  # name: (basket, commodity code)
    "cpi_all": ("all", "0"),
    "cpi_b30": ("b30", "0"),
    "fuel": ("all", "07.2.2"),       # fuels and lubricants for personal transport
    "gasoline": ("all", "07.2.2.2"),  # 2018 onward only
    "diesel": ("all", "07.2.2.1"),
    "fuel_b30": ("b30", "07.2.2"),
    **{f"c{d:02d}": ("all", f"{d:02d}") for d in range(1, 14)},
    **{f"b30_c{d:02d}": ("b30", f"{d:02d}") for d in range(1, 14)},
}


def spliced(long, basket, code):
    s = long[long.commodity_code == code]
    old = (s[s.file.isin(OLD[basket])]
           .drop_duplicates(["region", "date"], keep="last")
           .pivot(index="date", columns="region", values="value"))
    new = s[s.file == NEW[basket]].pivot(index="date", columns="region", values="value")
    if old.empty:
        return new.drop(columns="NIR", errors="ignore")
    last = old.index.max()
    ext = new.loc[new.index > last]
    if not ext.empty and last in new.index:
        growth = ext.div(new.loc[last])
        ext = growth.mul(old.loc[last]).reindex(columns=old.columns)
        old = pd.concat([old, ext])
    return old


def build_regional():
    long = pd.read_parquet(PROC / "psa_cpi_long.parquet")
    frames = {}
    for name, (basket, code) in SERIES.items():
        wide = spliced(long, basket, code)
        frames[name] = wide.stack().rename(name)
    panel = pd.concat(frames, axis=1).reset_index().rename(columns={"level_1": "region"})
    panel = panel.sort_values(["region", "date"]).reset_index(drop=True)
    # complete monthly grid so lags are calendar lags
    grid = pd.MultiIndex.from_product([panel.region.unique(),
                                       pd.date_range(panel.date.min(), panel.date.max(), freq="MS")],
                                      names=["region", "date"])
    panel = panel.set_index(["region", "date"]).reindex(grid).reset_index()
    panel["t"] = (panel.date.dt.year - 1994) * 12 + panel.date.dt.month - 1
    panel["new_geo_ext"] = (panel.date > "2025-12-01") & panel.region.isin(CHANGED_REGIONS)
    panel["aggregate"] = panel.region.isin(["PH", "AONCR"])
    g = panel.groupby("region")
    for name in SERIES:
        panel[f"d_{name}"] = 100 * g[name].transform(lambda v: np.log(v).diff())
    panel["ratio"] = np.log(panel.cpi_all / panel.cpi_b30)
    panel["d_ratio"] = panel.d_cpi_all - panel.d_cpi_b30
    return panel


def build_macro():
    cmo = pd.read_excel(RAW / "wb" / "CMO-Historical-Data-Monthly.xlsx", sheet_name="Monthly Prices", header=None)
    hdr = cmo.iloc[4]
    cmo = cmo.iloc[6:].rename(columns=hdr)
    cmo = cmo.rename(columns={cmo.columns[0]: "period"})
    cmo["date"] = pd.to_datetime(cmo.period.str.replace("M", "-") + "-01")
    macro = cmo.set_index("date")[["Crude oil, Brent", "Crude oil, Dubai", "Crude oil, average"]]
    macro.columns = ["brent_usd", "dubai_usd", "crude_avg_usd"]
    macro = macro.apply(pd.to_numeric, errors="coerce")

    fx = pd.read_excel(RAW / "bsp" / "pesodollar.xlsx", sheet_name="monthly", header=None).iloc[7:, 1:4]
    fx.columns = ["year", "month", "php_usd"]
    fx["year"] = fx.year.ffill()
    fx = fx.dropna(subset=["month"])
    fx["php_usd"] = pd.to_numeric(fx.php_usd, errors="coerce")
    fx["date"] = pd.to_datetime(fx.year.astype(int).astype(str) + "-" + fx.month.str.strip() + "-01",
                                format="%Y-%B-%d", errors="coerce")
    macro = macro.join(fx.dropna(subset=["date"]).set_index("date").php_usd, how="outer")

    bis = pd.read_csv(RAW / "bis" / "bis_cbpol_ph_monthly.csv")
    bis["date"] = pd.to_datetime(bis.TIME_PERIOD + "-01")
    macro = macro.join(bis.set_index("date").OBS_VALUE.rename("policy_rate"), how="outer")

    fao = pd.read_csv(RAW / "fao" / "food_price_indices_data.csv", skiprows=3, usecols=[0, 1], names=["d", "ffpi"])
    fao = fao[fao.d.astype(str).str.match(r"^\d{4}-\d{2}$")]
    fao["date"] = pd.to_datetime(fao.d + "-01")
    macro = macro.join(fao.set_index("date").ffpi.astype(float), how="outer")

    wb = pd.read_excel(RAW / "wb" / "Global_Fuel_Prices_Database.xlsx",
                       sheet_name="Regular Gasoline (below RON 95)", header=None)
    cols = wb.iloc[0]
    ph = wb[wb[2] == "PHL"]
    if not ph.empty:
        row = ph.iloc[0, 4:]
        row.index = pd.to_datetime(cols.iloc[4:].values, errors="coerce").to_period("M").to_timestamp()
        macro = macro.join(pd.to_numeric(row, errors="coerce").rename("wb_gasoline_php"), how="outer")

    macro = macro.loc["1994-01-01":].dropna(how="all")
    macro["dubai_php"] = macro.dubai_usd * macro.php_usd
    macro["brent_php"] = macro.brent_usd * macro.php_usd
    for c in ["dubai_php", "brent_php", "dubai_usd", "php_usd", "ffpi", "wb_gasoline_php"]:
        if c in macro:
            macro[f"d_{c}"] = 100 * np.log(macro[c]).diff()
    macro["d_policy_rate"] = macro.policy_rate.diff()
    return macro.reset_index().rename(columns={"index": "date"})


if __name__ == "__main__":
    panel = build_regional()
    macro = build_macro()
    panel.to_parquet(PROC / "panel_regional.parquet", index=False)
    macro.to_parquet(PROC / "macro_national.parquet", index=False)
    cov = panel.groupby("region").agg(
        all_start=("cpi_all", lambda v: panel.loc[v.dropna().index, "date"].min()),
        b30_start=("cpi_b30", lambda v: panel.loc[v.dropna().index, "date"].min()),
        fuel_start=("fuel", lambda v: panel.loc[v.dropna().index, "date"].min()),
        end=("cpi_b30", lambda v: panel.loc[v.dropna().index, "date"].max()))
    print(cov.to_string())
    print(macro.dropna(subset=["dubai_php"]).date.agg(["min", "max"]))
    print(macro.tail(3).T.to_string())
