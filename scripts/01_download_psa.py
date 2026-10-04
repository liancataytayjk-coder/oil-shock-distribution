"""Download PSA CPI tables (all-income and bottom-30%) from OpenSTAT.

Pulls every commodity for the national and regional rows of each table, one
geography at a time to stay under the PxWeb cell limit, and writes the API's
CSV responses, stacked but otherwise unchanged, to data/raw/psa/<table>.csv.gz. Provinces and cities are
skipped.

Usage: python scripts/01_download_psa.py [--force]
"""

import io
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

API = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/"
OUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "psa"

TABLES = {
    # All-income CPI, 2018=100
    "CPI/2018NEW/0012M4ACP22.px": "cpi_all_2018new_2018_2026",
    "CPI/2018NEW/0012M4ACP28.px": "cpi_all_2018new_backcast_1994_2017",
    "CPI/2018NEW/0012M4ACP25.px": "cpi_all_2018new_weights",
    "CPI/2018/0012M4ACP09.px": "cpi_all_2018old_2018_2025",
    "CPI/2018/0012M4ACP15.px": "cpi_all_2018old_backcast_1994_2017",
    "CPI/2018/0012M4ACP12.px": "cpi_all_2018old_weights",
    # All-income CPI, 2012=100
    "CPI/2012/0012M4ACPI1.px": "cpi_all_2012_2012_2021",
    "CPI/2012/0012M4ACPI4.px": "cpi_all_2012_1994_2011",
    "CPI/2012/0012M4ACPI3.px": "cpi_all_2012_weights",
    # Bottom-30% CPI, 2018=100
    "BIH/2018NEW/0022M4ABIR1.px": "cpi_b30_2018new_2018_2026",
    "BIH/2018NEW/0022M4ABIR3.px": "cpi_b30_2018new_weights",
    "BIH/2018/0022M4ABOT1.px": "cpi_b30_2018old_2018_2025",
    "BIH/2018/0022M4ABOT3.px": "cpi_b30_2018old_weights",
    "BIH/2018/0022M4ABOT4.px": "cpi_b30_2018old_backcast_2012_2017",
    "BIH/2018/0022M4ABOT5.px": "cpi_b30_2018old_backcast_allitems_2000_2011",
    # Bottom-30% CPI, 2012=100 and 2000=100
    "BIH/2012/0022M4AB301.px": "cpi_b30_2012_2012_2022",
    "BIH/2012/0022M4AB303.px": "cpi_b30_2012_weights",
    "BIH/2012/0022M4AB305.px": "cpi_b30_2000_2000_2017",
    "BIH/2012/0022M4AB311.px": "cpi_b30_2000_weights",
}

# Region rows in tables that label geography without leading dots.
UNDOTTED_REGIONS = re.compile(
    r"^(PHILIPPINES|NCR|AONCR|CAR|Reg(ion)? ?\w+|MIMAROPA( REGION)?|BARMM|ARMM|CARAGA|NIR)$",
    re.IGNORECASE,
)


def is_region(label: str, dotted: bool) -> bool:
    if label == "PHILIPPINES":
        return True
    if dotted:
        return label.startswith("..") and not label.startswith("....")
    return bool(UNDOTTED_REGIONS.match(label))


def post(table: str, query: dict) -> str:
    for attempt in range(5):
        try:
            r = requests.post(API + table, json=query, timeout=120)
            r.raise_for_status()
            try:
                return r.content.decode("utf-8-sig")
            except UnicodeDecodeError:  # some tables are served as Latin-1
                return r.content.decode("latin-1")
        except requests.RequestException:
            if attempt == 4:
                raise
            time.sleep(2 ** (attempt + 1))


def download(table: str, name: str, force: bool) -> None:
    out = OUT / f"{name}.csv.gz"
    if out.exists() and not force:
        print(f"skip {name} (exists)")
        return
    meta = requests.get(API + table, timeout=60).json()
    geo = next((v for v in meta["variables"] if v["code"] in ("Geolocation", "Area")), None)
    rest = [
        {"code": v["code"], "selection": {"filter": "all", "values": ["*"]}}
        for v in meta["variables"]
        if v is not geo
    ]
    if geo is None:
        geo_codes = [None]
    else:
        dotted = any(t.startswith("..") for t in geo["valueTexts"])
        geo_codes = [c for c, t in zip(geo["values"], geo["valueTexts"]) if is_region(t, dotted)]

    parts = []
    for code in geo_codes:
        sel = list(rest)
        if code is not None:
            sel.insert(0, {"code": geo["code"], "selection": {"filter": "item", "values": [code]}})
        parts.append(pd.read_csv(io.StringIO(post(table, {"query": sel, "response": {"format": "csv"}})),
                                 dtype=str, keep_default_na=False))
        time.sleep(0.5)
    df = pd.concat(parts, ignore_index=True)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"wrote {name}: {len(geo_codes)} geographies, {df.shape[0]} rows x {df.shape[1]} cols")


if __name__ == "__main__":
    force = "--force" in sys.argv
    for table, name in TABLES.items():
        download(table, name, force)
