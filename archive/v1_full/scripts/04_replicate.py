"""Replication gate: re-estimate Kpodar and Liu (2021) on EU data.

G1  HICP all-items on Weekly Oil Bulletin Euro-super 95, after tax (Fig. 7)
G2  same with before-tax price (+ tax control) and with Brent in euro (Fig. 7)
G3  HICP all-items on HICP fuels and lubricants CP0722 (Annex Table 1 shape)
PH  Philippines alone, 2000-Jun 2019 (indicative; Annex Table 2)

Writes output/tables/replication_*.csv and prints the gate verdicts.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ospd.lp import local_projection  # noqa: E402

RAW = ROOT / "data" / "raw"
OUT = ROOT / "output" / "tables"
END = "2019-06-01"
EU = ["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GR", "HR", "HU", "IE", "IT",
      "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK", "UK"]
HICP_GEO = {"GR": "EL"}  # Eurostat codes Greece as EL


def eurostat_tsv(path):
    d = pd.read_csv(path, sep="\t", compression="gzip")
    key = d.columns[0]
    keys = d[key].str.split(",", expand=True)
    keys.columns = key.split("\\")[0].split(",")
    d = pd.concat([keys, d.drop(columns=key)], axis=1)
    long = d.melt(id_vars=list(keys.columns), var_name="period", value_name="value")
    long["value"] = pd.to_numeric(long.value.astype(str).str.extract(r"([-\d.]+)")[0], errors="coerce")
    long["date"] = pd.to_datetime(long.period.str.strip() + "-01")
    return long.dropna(subset=["value"])


def hicp():
    h = eurostat_tsv(RAW / "eurostat" / "prc_hicp_midx_cp00_cp0722.tsv.gz")
    w = h.pivot_table(index=["geo", "date"], columns="coicop", values="value").reset_index()
    inv = {v: k for k, v in HICP_GEO.items()}
    w["country"] = w.geo.replace(inv)
    return w[w.country.isin(EU)].rename(columns={"CP00": "hicp", "CP0722": "hicp_fuel"})


def oil_bulletin():
    path = RAW / "eurostat" / "Weekly_Oil_Bulletin_Prices_History.xlsx"
    out = []
    for sheet, tag in [("Prices with taxes", "with_tax"), ("Prices wo taxes", "wo_tax")]:
        d = pd.read_excel(path, sheet_name=sheet, header=None)
        cols = d.iloc[0].astype(str)
        d = d.iloc[3:]
        d = d[pd.to_datetime(d[0], errors="coerce").notna()]
        dates = pd.to_datetime(d[0])
        for c in EU:
            name = f"{c}_price_{tag}_euro95"
            if name in cols.values:
                v = pd.to_numeric(d[cols[cols == name].index[0]], errors="coerce")
                out.append(pd.DataFrame({"country": c, "date": dates.values, tag: v.values}))
    wob = pd.concat(out).groupby(["country", "date"]).first().reset_index()
    wob["date"] = wob.date.dt.to_period("M").dt.to_timestamp()
    return wob.groupby(["country", "date"])[["with_tax", "wo_tax"]].mean().reset_index()


def brent_eur():
    cmo = pd.read_excel(RAW / "wb" / "CMO-Historical-Data-Monthly.xlsx", sheet_name="Monthly Prices", header=None)
    cmo = cmo.iloc[6:, [0, 2]]
    cmo.columns = ["period", "brent_usd"]
    cmo["date"] = pd.to_datetime(cmo.period.str.replace("M", "-") + "-01")
    fx = eurostat_tsv(RAW / "eurostat" / "ert_bil_eur_m_usd.tsv.gz")[["date", "value"]].rename(columns={"value": "usd_per_eur"})
    b = cmo.merge(fx, on="date")
    b["brent_eur"] = pd.to_numeric(b.brent_usd, errors="coerce") / b.usd_per_eur
    return b[["date", "brent_eur"]]


def prep(df, cols):
    df = df.sort_values(["country", "date"]).copy()
    grid = pd.MultiIndex.from_product([df.country.unique(), pd.date_range(df.date.min(), df.date.max(), freq="MS")],
                                      names=["country", "date"])
    df = df.set_index(["country", "date"]).reindex(grid).reset_index()
    for c in cols:
        df[f"d_{c}"] = 100 * df.groupby("country")[c].transform(lambda v: np.log(v).diff())
    df["t"] = (df.date.dt.year - 2000) * 12 + df.date.dt.month - 1
    return df


def run(df, y, x, label, **kw):
    r = local_projection(df, y, x, time="t", unit=kw.pop("unit", "country"), horizons=6, p=12, **kw)
    r.insert(0, "spec", label)
    return r


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    eu = hicp().merge(oil_bulletin(), on=["country", "date"], how="left").merge(brent_eur(), on="date", how="left")
    eu["tax"] = eu.with_tax - eu.wo_tax
    eu = eu[(eu.date >= "1999-01-01") & (eu.date <= END)]
    eu = prep(eu, ["hicp", "hicp_fuel", "with_tax", "wo_tax", "brent_eur", "tax"])
    wob = eu[eu.date >= "2005-01-01"]

    res = []
    for se in ["cluster", "robust"]:
        res += [
            run(wob, "d_hicp", "d_with_tax", f"G1 after tax [{se}]", se=se),
            run(wob, "d_hicp", "d_wo_tax", f"G2 before tax + tax control [{se}]", controls=("d_tax",), se=se),
            run(wob, "d_hicp", "d_brent_eur", f"G2 Brent in euro [{se}]", se=se),
            run(eu[eu.date >= "2000-01-01"], "d_hicp", "d_hicp_fuel", f"G3 HICP fuels CP0722 [{se}]", se=se),
        ]

    p = pd.read_parquet(ROOT / "data" / "processed" / "panel_regional.parquet")
    ph = p[(p.region == "PH") & (p.date <= END)].reset_index(drop=True)
    ph = ph[ph.date >= "1999-01-01"].reset_index(drop=True)
    res.append(run(ph, "d_cpi_all", "d_fuel", "PH alone, fuel index [newey_west]", unit=None, se="newey_west"))
    out = pd.concat(res, ignore_index=True)
    out = out[out.term == "shock"].drop(columns="term")
    out.to_csv(OUT / "replication_eu_ph.csv", index=False)

    pd.set_option("display.width", 200)
    print(out.pivot(index="spec", columns="h", values="beta").round(4).to_string())
    print(out.pivot(index="spec", columns="h", values="se").round(4).to_string())
    print(out.groupby("spec")[["nobs", "n_units"]].first().to_string())

    b = out[out.spec.str.endswith("[cluster]")].pivot(index="spec", columns="h", values="beta")
    s = out[out.spec.str.endswith("[cluster]")].pivot(index="spec", columns="h", values="se")
    g1 = b.loc["G1 after tax [cluster]"]
    g3, g3se = b.loc["G3 HICP fuels CP0722 [cluster]"], s.loc["G3 HICP fuels CP0722 [cluster]"]
    verdict = {
        "G1": bool(0.035 <= g1[0] <= 0.075 and (g1[2:7].abs() <= 0.01).all()),
        "G2": bool(g1[0] > b.loc["G2 before tax + tax control [cluster]", 0]
                   and g1[0] > b.loc["G2 Brent in euro [cluster]", 0]),
        "G3": bool(g3[0] / g3se[0] > 1.645 and g3[1] < g3[0] and (g3[2:7].abs() <= 0.01).all()),
    }
    print("Gate:", verdict, "PASS" if all(verdict.values()) else "FAIL")
    pd.Series(verdict).to_csv(OUT / "replication_gate.csv", header=["pass"])


if __name__ == "__main__":
    main()
