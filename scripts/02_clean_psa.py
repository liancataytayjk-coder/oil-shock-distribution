"""Reshape the raw PSA CPI downloads into one long table.

Output: data/processed/psa_cpi_long.parquet with one row per
(file, region, commodity, month): file, basket (all/b30), base, geo
(old/new geographic code), region (harmonised code), commodity_code,
commodity, date, value. Annual averages ("Ave") are dropped.
"""

import re
from pathlib import Path

import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ospd.regions import region_code  # noqa: E402

RAW = ROOT / "data" / "raw" / "psa"
OUT = ROOT / "data" / "processed" / "psa_cpi_long.parquet"

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

def parse_name(stem: str) -> dict:
    basket, base = stem.split("_")[1:3]
    geo = "new" if base.endswith("new") else ("old" if base.endswith("old") else "old")
    return dict(file=stem, basket=basket, base=re.sub(r"(new|old)$", "", base), geo=geo)


def split_commodity(label: str):
    m = re.match(r"^\s*([0-9][0-9.]*)\s+-\s+(.*)$", label)
    return (m.group(1), m.group(2).strip()) if m else ("", label.strip())


def stem(path: Path) -> str:
    return path.name.removesuffix(".csv.gz")


def tidy(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    geo_col = raw.columns[0]
    com_col = next(c for c in raw.columns if c.startswith("Commodity"))
    month_cols = [c for c in raw.columns if re.match(r"^\d{4} [A-Z][a-z]{2}$", c) and c[5:] in MONTHS]
    long = raw.melt(id_vars=[geo_col, com_col], value_vars=month_cols, var_name="period", value_name="value")
    long["value"] = pd.to_numeric(long["value"].str.strip(), errors="coerce")
    long = long.dropna(subset=["value"])
    long["date"] = pd.to_datetime(long["period"].str[:4] + "-" + long["period"].str[5:].map(MONTHS).astype(str) + "-01")
    long["region"] = long[geo_col].map(region_code)
    codes = long[com_col].map(split_commodity)
    long["commodity_code"] = codes.str[0]
    long["commodity"] = codes.str[1]
    for k, v in parse_name(stem(path)).items():
        long[k] = v
    return long[["file", "basket", "base", "geo", "region", "commodity_code", "commodity", "date", "value"]]


def weights(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    out = pd.DataFrame({
        "region": raw.iloc[:, 0].map(region_code),
        "commodity_code": raw.iloc[:, 1].map(lambda s: split_commodity(s)[0]),
        "commodity": raw.iloc[:, 1].map(lambda s: split_commodity(s)[1]),
        "weight": pd.to_numeric(raw.iloc[:, -1].str.strip(), errors="coerce"),
    })
    for k, v in parse_name(stem(path)).items():
        out[k] = v
    return out


if __name__ == "__main__":
    files = sorted(RAW.glob("*.csv.gz"))
    series = pd.concat([tidy(f) for f in files if not stem(f).endswith("weights")], ignore_index=True)
    wts = pd.concat([weights(f) for f in files if stem(f).endswith("weights")], ignore_index=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    series.to_parquet(OUT, index=False)
    wts.to_parquet(OUT.with_name("psa_cpi_weights.parquet"), index=False)
    print(series.groupby("file").agg(regions=("region", "nunique"), commodities=("commodity", "nunique"),
                                     start=("date", "min"), end=("date", "max")).to_string())
