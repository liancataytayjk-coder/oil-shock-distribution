"""Copy the columns we use from the three Excel source files into plain CSV files.

Values are copied as they are; only the layout changes (one row per month), so that Stata
and other programs can read them with a plain CSV import. Writes data/raw/extracts/:

  wb_cmo_crude_monthly.csv     World Bank Pink Sheet: Brent, Dubai and average crude, USD/barrel
  bsp_php_usd_monthly.csv      BSP: pesos per US dollar, monthly average
  wb_gfpd_phl_gasoline.csv     World Bank Global Fuel Prices Database: Manila regular gasoline, PHP/litre
"""

import pandas as pd

from config import EXTRACTS, RAW


def cmo():
    x = pd.read_excel(RAW / "wb" / "CMO-Historical-Data-Monthly.xlsx", sheet_name="Monthly Prices", header=None)
    hdr = x.iloc[4]
    x = x.iloc[6:].rename(columns=hdr)
    x = x.rename(columns={x.columns[0]: "period"})
    out = pd.DataFrame({
        "period": x.period.astype(str),                      # e.g. 2026M08
        "brent_usd": x["Crude oil, Brent"], "dubai_usd": x["Crude oil, Dubai"],
        "crude_avg_usd": x["Crude oil, average"],
    })
    out = out[out.period.str.match(r"^\d{4}M\d{2}$")]
    out.insert(0, "date", out.period.str[:4] + "-" + out.period.str[5:])
    return out.drop(columns="period")


def bsp():
    x = pd.read_excel(RAW / "bsp" / "pesodollar.xlsx", sheet_name="monthly", header=None).iloc[7:, 1:4]
    x.columns = ["year", "month", "php_usd"]
    x["year"] = x.year.ffill()                               # the year is written once per block in the sheet
    x = x.dropna(subset=["month"])
    d = pd.to_datetime(x.year.astype(int).astype(str) + "-" + x.month.astype(str).str.strip() + "-01",
                       format="%Y-%B-%d", errors="coerce")
    out = pd.DataFrame({"date": d.dt.strftime("%Y-%m"), "php_usd": pd.to_numeric(x.php_usd, errors="coerce")})
    return out.dropna()


def gfpd():
    x = pd.read_excel(RAW / "wb" / "Global_Fuel_Prices_Database.xlsx",
                      sheet_name="Regular Gasoline (below RON 95)", header=None)
    cols = x.iloc[0]
    row = x[x[2] == "PHL"].iloc[0, 4:]
    d = pd.to_datetime(cols.iloc[4:].values, errors="coerce").to_period("M").astype(str)
    out = pd.DataFrame({"date": d, "wb_gasoline_php": pd.to_numeric(row.values, errors="coerce")})
    return out.dropna()


if __name__ == "__main__":
    EXTRACTS.mkdir(parents=True, exist_ok=True)
    for name, f in [("wb_cmo_crude_monthly", cmo), ("bsp_php_usd_monthly", bsp), ("wb_gfpd_phl_gasoline", gfpd)]:
        df = f()
        df.to_csv(EXTRACTS / f"{name}.csv", index=False)
        print(f"{name}: {len(df)} rows, {df.date.iloc[0]} to {df.date.iloc[-1]}")
