"""Download PSA official poverty incidence among population by region (2018, 2021, 2023).

Writes the OpenSTAT CSV response unchanged to data/raw/psa/poverty_population_2018_2023.csv.
"""

from pathlib import Path

import requests

URL = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1F/FY/0031F3DF020.px"
OUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "psa" / "poverty_population_2018_2023.csv"

meta = requests.get(URL, timeout=60).json()
query = [{"code": v["code"], "selection": {"filter": "all", "values": ["*"]}} for v in meta["variables"]]
r = requests.post(URL, json={"query": query, "response": {"format": "csv"}}, timeout=120)
r.raise_for_status()
OUT.write_bytes(r.content)
print("wrote", OUT, len(r.content), "bytes")
