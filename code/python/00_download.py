"""Optional: download the PSA raw files again (the stored copies in data/raw/ are enough to replicate).

PSA OpenSTAT tables are pulled through the PxWeb API, one geography at a time (to stay under
the cell limit), keeping the national and regional rows only. Responses are saved as plain CSV,
stacked but otherwise unchanged. The other sources (World Bank, BSP, BIS, FAO) are single files;
download them by hand from the links in data/raw/source_log.md and the codebook.

Usage: python code/python/00_download.py [--force]
"""

import io
import re
import sys
import time

import pandas as pd
import requests

from config import RAW

API = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/"
TABLES = {
    "CPI/2018/0012M4ACP15.px": "cpi_all_2018old_backcast_1994_2017",
    "CPI/2018/0012M4ACP09.px": "cpi_all_2018old_2018_2025",
    "CPI/2018/0012M4ACP12.px": "cpi_all_2018old_weights",
    "CPI/2018NEW/0012M4ACP22.px": "cpi_all_2018new_2018_2026",
    "CPI/2018NEW/0012M4ACP25.px": "cpi_all_2018new_weights",
    "BIH/2018/0022M4ABOT5.px": "cpi_b30_2018old_backcast_allitems_2000_2011",
    "BIH/2018/0022M4ABOT4.px": "cpi_b30_2018old_backcast_2012_2017",
    "BIH/2018/0022M4ABOT1.px": "cpi_b30_2018old_2018_2025",
    "BIH/2018/0022M4ABOT3.px": "cpi_b30_2018old_weights",
    "BIH/2018NEW/0022M4ABIR1.px": "cpi_b30_2018new_2018_2026",
    "BIH/2018NEW/0022M4ABIR3.px": "cpi_b30_2018new_weights",
}
POVERTY = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1F/FY/0031F3DF020.px"
UNDOTTED_REGIONS = re.compile(
    r"^(PHILIPPINES|NCR|AONCR|CAR|Reg(ion)? ?\w+|MIMAROPA( REGION)?|BARMM|ARMM|CARAGA|NIR)$", re.IGNORECASE)


def is_region(label, dotted):
    if label == "PHILIPPINES":
        return True
    if dotted:
        return label.startswith("..") and not label.startswith("....")
    return bool(UNDOTTED_REGIONS.match(label))


def post(url, query):
    for attempt in range(5):
        try:
            r = requests.post(url, json=query, timeout=120)
            r.raise_for_status()
            try:
                return r.content.decode("utf-8-sig")
            except UnicodeDecodeError:  # some tables are served as Latin-1
                return r.content.decode("latin-1")
        except requests.RequestException:
            if attempt == 4:
                raise
            time.sleep(2 ** (attempt + 1))


def download(table, name, force):
    out = RAW / "psa" / f"{name}.csv"
    if out.exists() and not force:
        print("skip", name)
        return
    meta = requests.get(API + table, timeout=60).json()
    geo = next((v for v in meta["variables"] if v["code"] in ("Geolocation", "Area")), None)
    rest = [{"code": v["code"], "selection": {"filter": "all", "values": ["*"]}}
            for v in meta["variables"] if v is not geo]
    dotted = any(t.startswith("..") for t in geo["valueTexts"])
    codes = [c for c, t in zip(geo["values"], geo["valueTexts"]) if is_region(t, dotted)]
    parts = []
    for code in codes:
        sel = [{"code": geo["code"], "selection": {"filter": "item", "values": [code]}}] + rest
        text = post(API + table, {"query": sel, "response": {"format": "csv"}})
        parts.append(pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False))
        time.sleep(0.5)
    pd.concat(parts, ignore_index=True).to_csv(out, index=False)
    print("wrote", name, len(codes), "geographies")


if __name__ == "__main__":
    force = "--force" in sys.argv
    for t, n in TABLES.items():
        download(t, n, force)
    out = RAW / "psa" / "poverty_population_2018_2023.csv"
    if force or not out.exists():
        meta = requests.get(POVERTY, timeout=60).json()
        q = [{"code": v["code"], "selection": {"filter": "all", "values": ["*"]}} for v in meta["variables"]]
        r = requests.post(POVERTY, json={"query": q, "response": {"format": "csv"}}, timeout=120)
        r.raise_for_status()
        out.write_bytes(r.content)
        print("wrote poverty table")
