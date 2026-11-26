"""Prepare the data for the Stata teaching sequence (code/stata/teaching/).

Writes code/stata/teaching/data/:
    regional_panel.csv            the 17-region monthly panel (copied unchanged from data/clean/)
    national_monthly.csv          the national series the do-files use (columns of data/clean/national_monthly.csv)
    weights_2018.csv              2018 budget shares of the 13 divisions (rows of data/clean/weights_2018.csv)
    region_info.csv               poverty, poverty line and food share by region (copied unchanged)
    rq2_weights_decomposition.csv Python's budget-share calculation, used by step 8 to check step 5
    stata_data.xlsx               the same five tables in one workbook, with a README and a data dictionary

The CSV files are what Stata reads; the workbook is for looking at the data in Excel. Values are copied as text,
so every number is exactly the one Python used.

    python 12_stata_data.py          build the data folder
    python 12_stata_data.py zip      also build study_kit/stata_pack.zip (run after study_kit/build_kit.py)
"""

import shutil
import sys
import zipfile
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "data" / "clean"
TEACH = ROOT / "code" / "stata" / "teaching"
DATA = TEACH / "data"
DIVS = [f"{c:02d}" for c in range(1, 14)]

NATIONAL_COLS = (["date_str", "date", "year", "month", "t", "cpi_all", "cpi_b30", "fuel", "ratio",
                  "d_cpi_all", "d_cpi_b30", "d_fuel", "d_ratio"] + [f"c{c}" for c in DIVS] + [f"d_c{c}" for c in DIVS]
                 + ["dubai_usd", "php_usd", "dubai_php", "policy_rate", "ffpi",
                    "d_dubai_php", "d_php_usd", "d_policy_rate", "d_ffpi"])

DIVISION_NAMES = {
    "01": "food and non-alcoholic beverages", "02": "alcoholic beverages and tobacco",
    "03": "clothing and footwear", "04": "housing, water, electricity, gas and other fuels",
    "05": "furnishings and household equipment", "06": "health", "07": "transport",
    "08": "information and communication", "09": "recreation, sport and culture", "10": "education services",
    "11": "restaurants and accommodation services", "12": "insurance and financial services",
    "13": "personal care, social protection and miscellaneous goods and services"}

DLOG = "100 x monthly change in the natural log (about the % change from the previous month)"

# (file, variable, meaning, unit / values)
DICTIONARY = [
    ("regional_panel", "region", "Region code (old geographic code, 17 regions)",
     "NCR, CAR, R01 ... R13, R04A, R04B, BARMM"),
    ("regional_panel", "region_name", "Region name", "text"),
    ("regional_panel", "date_str", "Month", "text, YYYY-MM; Stata: monthly(date_str, \"YM\")"),
    ("regional_panel", "date", "First day of the month", "text, YYYY-MM-DD"),
    ("regional_panel", "year", "Calendar year", "1994-2026"),
    ("regional_panel", "month", "Calendar month", "1-12"),
    ("regional_panel", "t", "Linear time trend: months since January 1994", "0, 1, 2, ..."),
    ("regional_panel", "cpi_all", "Headline index: CPI of all households, all items", "index, 2018 = 100"),
    ("regional_panel", "cpi_b30", "Low-income index: CPI of the bottom 30% by income per person, all items",
     "index, 2018 = 100 (from 2000)"),
    ("regional_panel", "fuel", "Retail fuel price index: CPI 07.2.2, fuels and lubricants for personal transport",
     "index, 2018 = 100"),
    ("regional_panel", "d_cpi_all", "Inflation of all households (pi_all)", DLOG),
    ("regional_panel", "d_cpi_b30", "Inflation of low-income households (pi_low)", DLOG),
    ("regional_panel", "d_fuel", "The fuel shock f_rt: change in the retail fuel price index", DLOG),
    ("regional_panel", "ratio", "Relative price level: 100 x ln(cpi_all / cpi_b30)", "log points"),
    ("regional_panel", "d_ratio", "The gap D: d_cpi_all - d_cpi_b30 (negative = low-income prices rose more)",
     "percentage points"),
    ("regional_panel", "new_geo_ext", "1 if the month was extended with the new geographic code (Jan-Aug 2026, "
     "regions VI, VII, XII, BARMM)", "0/1"),
    ("regional_panel", "d_fuel_nat", "National fuel shock (same for every region in a month)", DLOG),
    ("national_monthly", "date_str ... t", "Month and trend, as in regional_panel", ""),
    ("national_monthly", "cpi_all, cpi_b30, fuel, ratio", "National headline, low-income and fuel indices; "
     "relative price level", "index, 2018 = 100; log points"),
    ("national_monthly", "d_cpi_all, d_cpi_b30, d_fuel, d_ratio", "Their monthly changes, as in regional_panel",
     DLOG),
    ("national_monthly", "c01 ... c13", "CPI of the 13 divisions (COICOP 2018), all households, national",
     "index, 2018 = 100"),
    ("national_monthly", "d_c01 ... d_c13", "Monthly change of each division index (used in step 5)", DLOG),
    ("national_monthly", "dubai_usd", "World crude price: Dubai crude (World Bank Pink Sheet)", "US$ per barrel"),
    ("national_monthly", "php_usd", "Exchange rate (BSP)", "pesos per US$"),
    ("national_monthly", "dubai_php", "World crude price in pesos: dubai_usd x php_usd", "pesos per barrel"),
    ("national_monthly", "policy_rate", "BSP policy rate (BIS)", "% per year"),
    ("national_monthly", "ffpi", "FAO Food Price Index", "index, 2014-2016 = 100"),
    ("national_monthly", "d_dubai_php", "Monthly change of the crude price in pesos (robustness shock, step 7)",
     DLOG),
    ("national_monthly", "d_php_usd", "Monthly change of the exchange rate (control, step 7)", DLOG),
    ("national_monthly", "d_policy_rate", "Monthly change of the policy rate (control, step 7)", "percentage points"),
    ("national_monthly", "d_ffpi", "Monthly change of the FAO Food Price Index (control, step 7)", DLOG),
    ("weights_2018", "basket", "Whose basket", "all = all households; b30 = low-income households"),
    ("weights_2018", "geo_code", "Geographic code", "old (17 regions)"),
    ("weights_2018", "region", "Region code; PH = Philippines", "as in regional_panel"),
    ("weights_2018", "coicop", "Division code; 0 = all items", "text, 0 and 01-13"),
    ("weights_2018", "item", "Division name", "text"),
    ("weights_2018", "weight", "Budget share: weight of the division in the basket of the region (all items = "
     "region's weight in the national basket)", "percent"),
    ("region_info", "region, region_name", "Region code and name; PH = Philippines", "text"),
    ("region_info", "poverty_2018, poverty_2023", "Poverty incidence among the population (PSA)", "percent"),
    ("region_info", "threshold_2023", "Annual poverty threshold per person, 2023 (PSA)", "pesos per year"),
    ("region_info", "food_share_2018", "Food share of the region's all-households basket", "percent"),
    ("region_info", "high_poverty, high_food", "1 if above the median of the 17 regions", "0/1"),
    ("region_info", "mindanao, island", "1 for Mindanao regions; 1 for island regions (IV-B, VI, VII, VIII)", "0/1"),
    ("rq2_weights_decomposition", "coicop, division", "Division code and name", "text"),
    ("rq2_weights_decomposition", "w_all, w_b30", "National 2018 budget shares of the two groups", "percent"),
    ("rq2_weights_decomposition", "beta, se", "Twelve-month response of the division index to a 1% fuel rise "
     "and its standard error", "% per 1% fuel"),
    ("rq2_weights_decomposition", "contrib_all, contrib_b30, contrib_gap",
     "beta x share / 100 for each group; contrib_gap = contrib_all - contrib_b30", "percentage points"),
]

README = [
    "Data for the Stata teaching sequence: Who Pays for Oil Shocks? (Lian Cataytay, November 2026)",
    "",
    "Stata reads the CSV files in this folder; this workbook holds the same tables for viewing in Excel.",
    "Each sheet is one CSV file; the sheet 'dictionary' explains every variable.",
    "",
    "regional_panel     17 regions x 392 months (January 1994 to August 2026). One row = one region in one month.",
    "                   The estimation sample starts in January 2001 (low-income index from 2000, plus 12 lags).",
    "national_monthly   The Philippines, one row per month: national indices, the 13 divisions, crude, exchange rate,",
    "                   policy rate and world food prices.",
    "weights_2018       2018 CPI budget shares of all households and low-income households, all items and 13 divisions.",
    "region_info        Poverty incidence, poverty threshold and food share by region.",
    "rq2_weights_decomposition   Python's budget-share calculation (step 8 checks step 5 against it).",
    "",
    "Sources: Philippine Statistics Authority (CPI, all-income and bottom-30%, 2018 = 100; weights; poverty);",
    "World Bank Commodity Price Data (Dubai crude); Bangko Sentral ng Pilipinas (exchange rate);",
    "Bank for International Settlements (policy rate); FAO (Food Price Index).",
    "",
    "Monthly changes (variables starting with d_) are 100 x the change in the natural log from the previous month.",
    "Missing values are empty cells (Stata shows them as .).",
    "",
    "To run: open Stata 17, cd to the folder that holds 00_setup.do (or the repository's top folder),",
    "then do 00_setup.do, 01_data.do, ... 09_figures.do in one session. See stata_tutorial.pdf.",
]


def copy_text(src, dst, cols=None, rows=None):
    """Copy a CSV as text, keeping every value exactly as written; optionally keep some columns and rows."""
    d = pd.read_csv(src, dtype=str, keep_default_na=False)
    if rows is not None:
        d = d[rows(d)]
    if cols is not None:
        missing = [c for c in cols if c not in d.columns]
        assert not missing, f"{src.name}: missing columns {missing}"
        d = d[cols]
    d.to_csv(dst, index=False)
    return d


def typed(path):
    """Read a CSV for the workbook: codes stay text, numbers become numbers."""
    text = {"region", "region_name", "date_str", "date", "coicop", "item", "division", "basket", "geo_code"}
    d = pd.read_csv(path, dtype={c: str for c in text}, keep_default_na=False, na_values=[""])
    return d


def sheet(wb, name, d, widths=None):
    ws = wb.create_sheet(name)
    ws.append(list(d.columns))
    for row in d.itertuples(index=False):
        ws.append([None if (isinstance(v, float) and pd.isna(v)) else v for v in row])
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.freeze_panes = "A2"
    for i, col in enumerate(d.columns, start=1):
        w = (widths or {}).get(col, max(10, min(40, len(col) + 2)))
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws


def build():
    DATA.mkdir(exist_ok=True)
    shutil.copyfile(CLEAN / "regional_panel.csv", DATA / "regional_panel.csv")
    shutil.copyfile(CLEAN / "region_info.csv", DATA / "region_info.csv")
    copy_text(CLEAN / "national_monthly.csv", DATA / "national_monthly.csv", cols=NATIONAL_COLS)
    copy_text(CLEAN / "weights_2018.csv", DATA / "weights_2018.csv",
              rows=lambda d: (d.geo_code == "old") & (d.coicop.str.len() <= 2))
    shutil.copyfile(ROOT / "output" / "tables" / "rq2_weights_decomposition.csv",
                    DATA / "rq2_weights_decomposition.csv")

    # checks: the panel is 17 regions x the same months, and every number is identical to data/clean
    reg = pd.read_csv(DATA / "regional_panel.csv")
    assert reg.region.nunique() == 17 and reg.groupby("region").size().nunique() == 1
    nat_full = pd.read_csv(CLEAN / "national_monthly.csv")
    nat = pd.read_csv(DATA / "national_monthly.csv")
    pd.testing.assert_frame_equal(nat, nat_full[NATIONAL_COLS])
    w = pd.read_csv(DATA / "weights_2018.csv", dtype={"coicop": str})
    ph = w[(w.region == "PH") & (w.coicop.str.len() == 2)]
    assert len(ph) == 26, len(ph)   # 13 divisions x 2 baskets: what step 5 uses

    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    for line in README:
        ws.append([line])
    ws["A1"].font = Font(bold=True)
    ws.column_dimensions["A"].width = 120
    dic = pd.DataFrame(DICTIONARY, columns=["file", "variable", "meaning", "unit or values"])
    ws = sheet(wb, "dictionary", dic, widths={"file": 26, "variable": 34, "meaning": 80, "unit or values": 45})
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for name in ["regional_panel", "national_monthly", "weights_2018", "region_info", "rq2_weights_decomposition"]:
        sheet(wb, name, typed(DATA / f"{name}.csv"), widths={"region_name": 40, "item": 50, "division": 40})
    wb.save(DATA / "stata_data.xlsx")
    print(f"wrote {DATA.relative_to(ROOT)}/: regional_panel ({len(reg)} rows), national_monthly ({len(nat)} rows, "
          f"{nat.shape[1]} columns), weights_2018 ({len(w)} rows), region_info, rq2_weights_decomposition, "
          "stata_data.xlsx")


def pack():
    """study_kit/stata_pack.zip: everything needed to run the teaching sequence, in one folder."""
    out = ROOT / "study_kit" / "stata_pack.zip"
    top = "stata_pack"
    files = sorted(p for p in TEACH.rglob("*") if p.is_file() and p.suffix in {".do", ".csv", ".xlsx", ".md"})
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, f"{top}/{p.relative_to(TEACH)}")
        for p in ["stata_tutorial.pdf", "stata_tutorial.docx"]:
            if (ROOT / "study_kit" / p).exists():
                z.write(ROOT / "study_kit" / p, f"{top}/{p}")
    print(f"wrote study_kit/stata_pack.zip ({len(files) + 2} files, {out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    build()
    if "zip" in sys.argv[1:]:
        pack()
