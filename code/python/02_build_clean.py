"""Build the cleaned, analysis-ready datasets from the raw files.

Reads  data/raw/psa/*.csv, data/raw/extracts/*.csv, data/raw/bis/, data/raw/fao/
Writes data/clean/
  national_monthly.csv   one row per month, Jan 1994-Aug 2026: price indices, macro series, changes
  regional_panel.csv     one row per region x month (17 regions), Jan 1994-Aug 2026
  weights_2018.csv       2018 CPI basket weights, both baskets, national and regional
  region_info.csv        poverty statistics, food share and the analysis groups of each region
  items_2026.csv         national indices of the items used in the 2026 decomposition (new geographic code)

Rules (decisions D5-D7 in CLAUDE.md):
  * Regions follow PSA's old geographic code (17 regions; Negros in Regions VI and VII), because
    the bottom-30% back series exist only on that code.
  * The old-code tables end Dec 2025. Jan-Aug 2026 is added by applying the new-code monthly
    changes to the old-code level ("chaining"). Regions whose boundaries changed in 2024
    (VI, VII, XII, BARMM) are flagged new_geo_ext = 1 in those months.
  * Bottom-30% all items: PSA backcast 2000-2011, backcast 2012-2017, current series from 2018,
    all on 2018 = 100.
  * Changes are 100 x the change in the natural log (approximately the percentage change).
"""

import re

import numpy as np
import pandas as pd

from config import CHANGED_REGIONS, CLEAN, END, EXTRACTS, RAW, REGION_NAMES, REGIONS_17, T0
from regions import region_code

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
OLD = {"all": ["cpi_all_2018old_backcast_1994_2017", "cpi_all_2018old_2018_2025"],
       "b30": ["cpi_b30_2018old_backcast_allitems_2000_2011", "cpi_b30_2018old_backcast_2012_2017",
               "cpi_b30_2018old_2018_2025"]}
NEW = {"all": "cpi_all_2018new_2018_2026", "b30": "cpi_b30_2018new_2018_2026"}

# Series in the cleaned data: name -> (basket, COICOP code)
SERIES = {
    "cpi_all": ("all", "0"), "cpi_b30": ("b30", "0"),
    "fuel": ("all", "07.2.2"),          # fuels and lubricants for personal transport (the shock)
    "gasoline": ("all", "07.2.2.2"),    # 2018 onward only
    **{f"c{d:02d}": ("all", f"{d:02d}") for d in range(1, 14)},          # 13 COICOP divisions, all income
    **{f"b30_c{d:02d}": ("b30", f"{d:02d}") for d in range(1, 14)},      # same, bottom 30% (from 2012)
    **{f"{b}_{n}": (b, code) for b in ("all", "b30") for n, code in [
        ("e045", "04.5"), ("e0452", "04.5.2"), ("e0453", "04.5.3"), ("e0454", "04.5.4"),
        ("t073", "07.3"), ("f0111", "01.1.1")]},
}
REGIONAL_SERIES = ["cpi_all", "cpi_b30", "fuel"]
ITEMS_2026 = ["0", "01.1.1", "01.1.1.1", "01.1.3", "04.5.2", "04.5.3", "04.5.4", "07.2.2", "07.3.2"]


def split_commodity(label):
    m = re.match(r"^\s*([0-9][0-9.]*)\s+-\s+(.*)$", label)
    return (m.group(1), m.group(2).strip()) if m else ("", label.strip())


def read_index_table(stem):
    """One PSA index table -> long: region, coicop, item, date, value (annual averages dropped)."""
    raw = pd.read_csv(RAW / "psa" / f"{stem}.csv", dtype=str, keep_default_na=False)
    geo, com = raw.columns[0], raw.columns[1]
    months = [c for c in raw.columns if re.match(r"^\d{4} [A-Z][a-z]{2}$", c) and c[5:] in MONTHS]
    x = raw.melt(id_vars=[geo, com], value_vars=months, var_name="period", value_name="value")
    x["value"] = pd.to_numeric(x.value.str.strip(), errors="coerce")
    x = x.dropna(subset=["value"])
    x["date"] = pd.to_datetime(x.period.str[:4] + "-" + x.period.str[5:].map(MONTHS).astype(str) + "-01")
    x["region"] = x[geo].map(region_code)
    codes = x[com].map(split_commodity)
    x["coicop"], x["item"] = codes.str[0], codes.str[1]
    x["file"] = stem
    return x[["file", "region", "coicop", "item", "date", "value"]]


def read_weights(stem):
    raw = pd.read_csv(RAW / "psa" / f"{stem}.csv", dtype=str, keep_default_na=False)
    codes = raw.iloc[:, 1].map(split_commodity)
    return pd.DataFrame({
        "basket": stem.split("_")[1], "geo_code": "new" if "2018new" in stem else "old",
        "region": raw.iloc[:, 0].map(region_code), "coicop": codes.str[0], "item": codes.str[1],
        "weight": pd.to_numeric(raw.iloc[:, -1].str.strip(), errors="coerce"),
    })


def spliced(long, basket, code):
    """Old-code series (back series joined to the current series), extended into 2026 by chaining."""
    s = long[long.coicop == code]
    old = (s[s.file.isin(OLD[basket])].drop_duplicates(["region", "date"], keep="last")
           .pivot(index="date", columns="region", values="value"))
    new = s[s.file == NEW[basket]].pivot(index="date", columns="region", values="value")
    if old.empty:
        return new.drop(columns="NIR", errors="ignore")
    last = old.index.max()
    ext = new.loc[new.index > last]
    if not ext.empty and last in new.index:
        ext = ext.div(new.loc[last]).mul(old.loc[last]).reindex(columns=old.columns)
        old = pd.concat([old, ext])
    return old


def dlog(s):
    return 100 * np.log(s).diff()


def months_frame():
    d = pd.date_range(T0, END, freq="MS")
    return pd.DataFrame({"date": d, "year": d.year, "month": d.month,
                         "t": (d.year - 1994) * 12 + d.month - 1})


def macro():
    m = months_frame()[["date"]]
    for f, cols in [("wb_cmo_crude_monthly", ["brent_usd", "dubai_usd"]), ("bsp_php_usd_monthly", ["php_usd"]),
                    ("wb_gfpd_phl_gasoline", ["wb_gasoline_php"])]:
        x = pd.read_csv(EXTRACTS / f"{f}.csv")
        x["date"] = pd.to_datetime(x.date + "-01")
        m = m.merge(x[["date"] + cols], on="date", how="left")
    bis = pd.read_csv(RAW / "bis" / "bis_cbpol_ph_monthly.csv")
    bis["date"] = pd.to_datetime(bis.TIME_PERIOD + "-01")
    m = m.merge(bis[["date", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "policy_rate"}), on="date", how="left")
    fao = pd.read_csv(RAW / "fao" / "food_price_indices_data.csv", skiprows=3, usecols=[0, 1], names=["d", "ffpi"])
    fao = fao[fao.d.astype(str).str.match(r"^\d{4}-\d{2}$")]
    fao["date"] = pd.to_datetime(fao.d + "-01")
    m = m.merge(fao[["date", "ffpi"]].astype({"ffpi": float}), on="date", how="left")
    m["dubai_php"] = m.dubai_usd * m.php_usd
    for c in ["dubai_php", "php_usd", "ffpi", "wb_gasoline_php"]:
        m[f"d_{c}"] = dlog(m[c])
    m["d_policy_rate"] = m.policy_rate.diff()
    return m


def poverty():
    pov = pd.read_csv(RAW / "psa" / "poverty_population_2018_2023.csv", encoding="latin-1")
    lab = pov.iloc[:, 0]
    pov = pov[lab.str.match(r"^\.\.[^.]") | lab.str.startswith("PHILIPPINES")].copy()
    pov["region"] = (pov.iloc[:, 0].str.replace(r"(\s+([0-9]+|[a-z]+[0-9]*)/,?)+\s*$", "", regex=True)
                     .str.replace(r"\s+r\d.*$", "", regex=True).map(region_code))
    pov = pov.set_index("region")
    num = lambda c: pd.to_numeric(pov[c], errors="coerce")  # noqa: E731
    return pd.DataFrame({
        "poverty_2018": num("Poverty Incidence among Population (%) 2018"),
        "poverty_2023": num("Poverty Incidence among Population (%) 2023"),
        "threshold_2023": num("Annual Per Capita Poverty Threshold (in PhP) 2023"),
    })


def main():
    CLEAN.mkdir(parents=True, exist_ok=True)
    stems = OLD["all"] + OLD["b30"] + list(NEW.values())
    long = pd.concat([read_index_table(s) for s in stems], ignore_index=True)
    weights = pd.concat([read_weights(f"cpi_{b}_2018{g}_weights") for b in ("all", "b30") for g in ("old", "new")],
                        ignore_index=True)

    # all series, all regions, on the monthly grid
    frames = {n: spliced(long, b, c).stack().rename(n) for n, (b, c) in SERIES.items()}
    wide = pd.concat(frames, axis=1).reset_index().rename(columns={"level_1": "region"})
    grid = months_frame().merge(pd.DataFrame({"region": ["PH"] + REGIONS_17}), how="cross")
    wide = grid.merge(wide, on=["date", "region"], how="left").sort_values(["region", "date"])
    wide = pd.concat([wide.reset_index(drop=True)], axis=1)
    g = wide.groupby("region", sort=False)
    wide = pd.concat([wide, pd.DataFrame({f"d_{n}": g[n].transform(dlog) for n in SERIES})], axis=1)
    wide["ratio"] = 100 * np.log(wide.cpi_all / wide.cpi_b30)
    wide["d_ratio"] = wide.d_cpi_all - wide.d_cpi_b30

    # national file
    nat = wide[wide.region == "PH"].drop(columns="region").merge(macro(), on="date", how="left").copy()
    nat["pos"] = (nat.d_fuel > 0).astype(int)                      # fuel rose this month (asymmetry check)
    nat["jan2012"] = (nat.date == "2012-01-01").astype(int)        # splice months (D7)
    nat["jan2018"] = (nat.date == "2018-01-01").astype(int)
    nat.insert(0, "date_str", nat.date.dt.strftime("%Y-%m"))

    # regional panel (core series only)
    keep = ["region", "date", "year", "month", "t"] + REGIONAL_SERIES + [f"d_{s}" for s in REGIONAL_SERIES] + \
           ["ratio", "d_ratio"]
    reg = wide[wide.region.isin(REGIONS_17)][keep].copy()
    reg.insert(1, "region_name", reg.region.map(REGION_NAMES))
    reg["new_geo_ext"] = ((reg.date > "2025-12-01") & reg.region.isin(CHANGED_REGIONS)).astype(int)
    reg = reg.merge(nat[["date", "d_fuel"]].rename(columns={"d_fuel": "d_fuel_nat"}), on="date", how="left")
    reg.insert(2, "date_str", reg.date.dt.strftime("%Y-%m"))

    # region information and analysis groups (defined before estimation; D8)
    info = pd.DataFrame({"region": ["PH"] + REGIONS_17})
    info["region_name"] = info.region.map(REGION_NAMES)
    info = info.merge(poverty(), left_on="region", right_index=True, how="left")
    w = weights[(weights.basket == "all") & (weights.geo_code == "old")].pivot(
        index="region", columns="coicop", values="weight")
    info["food_share_2018"] = info.region.map(100 * w["01"] / w["0"])  # food share of the region's own basket
    r17 = info.region.isin(REGIONS_17)
    for col, src in [("high_poverty", "poverty_2018"), ("high_food", "food_share_2018")]:
        med = info.loc[r17, src].median()
        info[col] = np.where(r17, (info[src] > med).astype(int), np.nan)
    info["mindanao"] = np.where(r17, info.region.isin(["R09", "R10", "R11", "R12", "R13", "BARMM"]), np.nan)
    info["island"] = np.where(r17, info.region.isin(["R04B", "R06", "R07", "R08"]), np.nan)

    # items for the 2026 decomposition: national, new geographic code, Dec 2025-Aug 2026
    items = long[long.file.isin(NEW.values()) & (long.region == "PH") & (long.date >= "2025-12-01")].copy()
    items["basket"] = items.file.str.split("_").str[1]
    w_new = weights[(weights.geo_code == "new") & (weights.region == "PH")]
    groups2 = sorted({c for c in w_new.coicop if re.match(r"^\d{2}\.\d$", c)} | set(ITEMS_2026))
    items = items[items.coicop.isin(groups2)][["basket", "coicop", "item", "date", "value"]]
    items.insert(3, "date_str", items.date.dt.strftime("%Y-%m"))

    out = {"national_monthly": nat, "regional_panel": reg, "weights_2018": weights,
           "region_info": info, "items_2026": items}
    for name, df in out.items():
        df = df.copy()
        if "date" in df:
            df["date"] = df.date.dt.strftime("%Y-%m-%d")
        df.to_csv(CLEAN / f"{name}.csv", index=False, float_format="%.10g")
        print(f"{name}: {df.shape[0]} rows x {df.shape[1]} columns")


if __name__ == "__main__":
    main()
