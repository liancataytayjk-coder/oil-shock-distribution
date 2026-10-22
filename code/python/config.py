"""Paths and fixed settings shared by every script (the estimation plan in CLAUDE.md)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
EXTRACTS = RAW / "extracts"
CLEAN = ROOT / "data" / "clean"
TAB = ROOT / "output" / "tables"
FIG = ROOT / "output" / "figures"
PAPER = ROOT / "paper"

H = 12                    # horizons h = 0..12 months
P = 12                    # lags of the outcome and the shock
START = "2001-01-01"      # first shock date (bottom-30% CPI starts Jan 2000, plus 12 lags)
END = "2026-08-01"        # last month of data
CUTOFF = "2025-12-01"     # RQ3: models for the 2026 episode use data up to this month only
T0 = "1994-01-01"         # month counter t = 0 (used for the linear trend)

REGIONS_17 = ["NCR", "CAR", "R01", "R02", "R03", "R04A", "R04B", "R05", "R06", "R07", "R08",
              "R09", "R10", "R11", "R12", "R13", "BARMM"]
REGION_NAMES = {
    "PH": "Philippines", "NCR": "National Capital Region", "CAR": "Cordillera Administrative Region",
    "R01": "I Ilocos", "R02": "II Cagayan Valley", "R03": "III Central Luzon", "R04A": "IV-A CALABARZON",
    "R04B": "MIMAROPA", "R05": "V Bicol", "R06": "VI Western Visayas", "R07": "VII Central Visayas",
    "R08": "VIII Eastern Visayas", "R09": "IX Zamboanga Peninsula", "R10": "X Northern Mindanao",
    "R11": "XI Davao", "R12": "XII SOCCSKSARGEN", "R13": "XIII Caraga",
    "BARMM": "Bangsamoro Autonomous Region in Muslim Mindanao",
}
CHANGED_REGIONS = ["R06", "R07", "R12", "BARMM"]  # boundaries changed in 2024 (Negros Island Region)
