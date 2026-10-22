"""Load the cleaned datasets (data/clean/) for analysis."""

import warnings

import pandas as pd

warnings.simplefilter("ignore", pd.errors.PerformanceWarning)
warnings.simplefilter("ignore", FutureWarning)

from config import CLEAN


def national():
    d = pd.read_csv(CLEAN / "national_monthly.csv", parse_dates=["date"])
    return d.sort_values("date").reset_index(drop=True)


def panel():
    d = pd.read_csv(CLEAN / "regional_panel.csv", parse_dates=["date"])
    return d.sort_values(["region", "date"]).reset_index(drop=True)


def region_info():
    return pd.read_csv(CLEAN / "region_info.csv").set_index("region")


def weights(basket, geo_code="old", region="PH"):
    w = pd.read_csv(CLEAN / "weights_2018.csv", dtype={"coicop": str})
    w = w[(w.basket == basket) & (w.geo_code == geo_code) & (w.region == region)]
    return w.set_index("coicop").weight
