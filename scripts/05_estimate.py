"""Estimate RQ1-RQ4 and the robustness checks (estimation plan in CLAUDE.md).

Writes:
  output/tables/estimates.csv        every coefficient path (long format)
  output/tables/rq3_gap_decomposition.csv
  output/tables/region_groups.csv    group dummies used in RQ4
"""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ospd.lp import local_projection  # noqa: E402
from ospd.regions import REGIONS_17, region_code  # noqa: E402

PROC = ROOT / "data" / "processed"
OUT = ROOT / "output" / "tables"
H, P = 12, 12
START = "2001-01-01"
DIVISIONS = {
    "c01": "Food and non-alcoholic beverages", "c02": "Alcoholic beverages and tobacco",
    "c03": "Clothing and footwear", "c04": "Housing, water, electricity, gas",
    "c05": "Furnishings and household equipment", "c06": "Health", "c07": "Transport",
    "c08": "Information and communication", "c09": "Recreation, sport and culture",
    "c10": "Education services", "c11": "Restaurants and accommodation",
    "c12": "Financial services", "c13": "Personal care and miscellaneous",
}


def load():
    panel = pd.read_parquet(PROC / "panel_regional.parquet")
    macro = pd.read_parquet(PROC / "macro_national.parquet")
    nat = panel[panel.region == "PH"].merge(macro, on="date", how="left")
    nat = nat.sort_values("date").reset_index(drop=True)
    nat["pos"] = (nat.d_fuel > 0).astype(float)
    nat["jan2012"] = (nat.date == "2012-01-01").astype(float)
    nat["jan2018"] = (nat.date == "2018-01-01").astype(float)
    reg = panel[panel.region.isin(REGIONS_17)].merge(
        nat[["date", "d_fuel"]].rename(columns={"d_fuel": "d_fuel_nat"}), on="date", how="left")
    reg = reg.sort_values(["region", "date"]).reset_index(drop=True)
    return nat, reg


def region_groups():
    pov = pd.read_csv(ROOT / "data" / "raw" / "psa" / "poverty_population_2018_2023.csv", encoding="latin-1")
    lab = pov.iloc[:, 0]
    top = lab.str.match(r"^\.\.[^.]") | lab.str.startswith("PHILIPPINES")
    pov = pov[top].copy()
    pov["region"] = pov.iloc[:, 0].str.replace(r"(\s+([0-9]+|[a-z]+[0-9]*)/,?)+\s*$", "", regex=True).map(
        lambda s: region_code(re.sub(r"\s+r\d.*$", "", s)))
    pov = pov[pov.region.isin(REGIONS_17)].set_index("region")
    g = pd.DataFrame(index=REGIONS_17)
    g["poverty_2018"] = pd.to_numeric(pov["Poverty Incidence among Population (%) 2018"], errors="coerce")
    g["poverty_2023"] = pd.to_numeric(pov["Poverty Incidence among Population (%) 2023"], errors="coerce")
    # Weights tables give each region's share of the national basket, so the
    # food share of a region's own basket is w(01) / w(all items).
    w = pd.read_parquet(PROC / "psa_cpi_weights.parquet")
    w = w[w.file == "cpi_all_2018old_weights"].pivot(index="region", columns="commodity_code", values="weight")
    g["food_share_2018"] = (100 * w["01"] / w["0"]).reindex(g.index)
    g["high_poverty"] = (g.poverty_2018 > g.poverty_2018.median()).astype(float)
    g["high_food"] = (g.food_share_2018 > g.food_share_2018.median()).astype(float)
    g["mindanao"] = g.index.isin(["R09", "R10", "R11", "R12", "R13", "BARMM"]).astype(float)
    g["island"] = g.index.isin(["R04B", "R06", "R07", "R08"]).astype(float)
    return g


class Runner:
    def __init__(self):
        self.rows = []

    def __call__(self, df, y, x, rq, spec, unit=None, se="newey_west", start=START, end=None,
                 drop=None, **kw):
        mask = df.date >= start
        if end:
            mask &= df.date <= end
        if drop is not None:
            mask &= ~drop
        horizons, p = kw.pop("horizons", H), kw.pop("p", P)
        for cum in (False, True):
            r = local_projection(df, y, x, time="t", unit=unit, horizons=horizons, p=p, se=se,
                                 sample=mask, cumulative=cum, **kw)
            r.insert(0, "cumulative", cum)
            r.insert(0, "shock", x)
            r.insert(0, "outcome", y)
            r.insert(0, "spec", spec)
            r.insert(0, "rq", rq)
            self.rows.append(r)

    def frame(self):
        return pd.concat(self.rows, ignore_index=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nat, reg = load()
    groups = region_groups()
    groups.to_csv(OUT / "region_groups.csv", index_label="region")
    for c in ["high_poverty", "high_food", "mindanao", "island"]:
        reg[c] = reg.region.map(groups[c])
    run = Runner()

    # RQ1 and RQ2 baseline
    run(nat, "d_cpi_all", "d_fuel", "RQ1", "baseline")
    run(nat, "d_cpi_b30", "d_fuel", "RQ1", "baseline")
    run(nat, "d_ratio", "d_fuel", "RQ2", "baseline")

    # RQ3 components
    for c in DIVISIONS:
        run(nat, f"d_{c}", "d_fuel", "RQ3", "baseline")

    # RQ3b (exploratory, added after seeing RQ2/RQ3; D9): same divisions in the
    # all-income and bottom-30% baskets, bottom-30% component indices exist from 2012
    for c in ["c01", "c04", "c07", "c11"]:
        run(nat, f"d_{c}", "d_fuel", "RQ3b", "2013- all-income", start="2013-01-01")
        run(nat, f"d_b30_{c}", "d_fuel", "RQ3b", "2013- bottom 30%", start="2013-01-01")
    run(nat, "d_ratio", "d_fuel", "RQ3b", "2013- ratio", start="2013-01-01")
    # Subsample stability of the regional result (exploratory, D9)
    run(reg, "d_ratio", "d_fuel", "RQ3b", "regional 2001-2012", end="2012-12-01", unit="region",
        se="driscoll_kraay")
    run(reg, "d_ratio", "d_fuel", "RQ3b", "regional 2013-", start="2013-01-01", unit="region",
        se="driscoll_kraay")
    run(reg, "d_ratio", "d_fuel", "RQ3b", "regional excl 2008", drop=reg.date.dt.year == 2008,
        unit="region", se="driscoll_kraay")
    run(nat, "d_ratio", "d_fuel", "RQ3b", "national excl 2008", drop=nat.date.dt.year == 2008)

    # RQ4 regional panel
    dk = dict(unit="region", se="driscoll_kraay")
    run(reg, "d_ratio", "d_fuel", "RQ4", "pooled", **dk)
    for g in ["high_poverty", "high_food", "mindanao", "island"]:
        run(reg, "d_ratio", "d_fuel", "RQ4", f"x {g}", interact=(g,), **dk)

    # Robustness, national RQ1 and RQ2
    for y in ["d_cpi_all", "d_ratio"]:
        run(nat, y, "d_dubai_php", "ROB", "a dubai crude php")
        run(nat, y, "d_fuel", "ROB", "b macro controls", controls=("d_php_usd", "d_policy_rate", "d_ffpi"))
        run(nat, y, "d_fuel", "ROB", "c p=6", p=6)
        run(nat, y, "d_fuel", "ROB", "c p=18", p=18)
        run(nat, y, "d_fuel", "ROB", "d excl 2020", drop=nat.date.dt.year == 2020)
        run(nat, y, "d_fuel", "ROB", "d excl 2026", end="2025-12-01")
        run(nat, y, "d_fuel", "ROB", "e splice dummies", exog=("jan2012", "jan2018"))
        run(nat, y, "d_fuel", "ROB", "f asymmetry", interact=("pos",))
        run(nat, y, "d_fuel", "ROB", "g to Jun 2019", end="2019-06-01")
        run(nat, y, "d_gasoline", "ROB", "h gasoline 07.2.2.2", start="2019-01-01")
        run(nat, y, "d_wb_gasoline_php", "ROB", "i WB pump price", start="2018-01-01")

    # Robustness, regional
    for r in REGIONS_17:
        sub = reg[reg.region != r].reset_index(drop=True)
        run(sub, "d_ratio", "d_fuel", "ROB", f"j drop {r}", **dk)
    run(reg, "d_ratio", "d_fuel", "ROB", "k drop flagged 2026", drop=reg.new_geo_ext, **dk)
    run(reg, "d_ratio", "d_fuel_nat", "ROB", "l national shock", **dk)

    est = run.frame()
    est.to_csv(OUT / "estimates.csv", index=False)

    # RQ3 gap decomposition at h = 12 (cumulative)
    w = pd.read_parquet(PROC / "psa_cpi_weights.parquet")
    w = w[(w.region == "PH") & w.file.isin(["cpi_all_2018old_weights", "cpi_b30_2018old_weights"])]
    w = w[w.commodity_code.isin([f"{d:02d}" for d in range(1, 14)])]
    w = w.pivot(index="commodity_code", columns="file", values="weight")
    w.columns = ["w_all", "w_b30"]
    cum = est[(est.rq == "RQ3") & est.cumulative & (est.h == H) & (est.term == "shock")]
    cum = cum.assign(commodity_code=cum.outcome.str[3:]).set_index("commodity_code")
    dec = w.join(cum[["beta", "se"]])
    dec["division"] = [DIVISIONS[f"c{c}"] for c in dec.index]
    dec["contrib_all"] = dec.beta * dec.w_all / 100
    dec["contrib_b30"] = dec.beta * dec.w_b30 / 100
    dec["contrib_gap"] = dec.contrib_all - dec.contrib_b30
    dec.to_csv(OUT / "rq3_gap_decomposition.csv", index_label="coicop")

    summarize(est, dec, groups)


def summarize(est, dec, groups):
    pd.set_option("display.width", 220)
    s = est[est.term == "shock"]
    def path(rq, spec, outcome, cum):
        q = s[(s.rq == rq) & (s.spec == spec) & (s.outcome == outcome) & (s.cumulative == cum)]
        return q.set_index("h")
    for rq, spec, y in [("RQ1", "baseline", "d_cpi_all"), ("RQ1", "baseline", "d_cpi_b30"),
                        ("RQ2", "baseline", "d_ratio"), ("RQ4", "pooled", "d_ratio")]:
        for cum in (False, True):
            q = path(rq, spec, y, cum)
            print(f"{rq} {y} {'cumulative' if cum else 'per-horizon'}")
            print(q[["beta", "se", "lo", "hi"]].T.round(4).to_string())
    print("\nRQ3 gap decomposition (cumulative h=12):")
    print(dec[["division", "w_all", "w_b30", "beta", "se", "contrib_gap"]].round(4).to_string())
    print("sum contrib_gap:", round(dec.contrib_gap.sum(), 4))
    print("\nRQ3b exploratory (cumulative h=6, h=12):")
    e = s[(s.rq == "RQ3b") & s.cumulative & s.h.isin([6, 12])]
    print(e.pivot_table(index=["spec", "outcome"], columns="h", values=["beta", "se"]).round(4).to_string())
    print("\nRQ4 interactions (cumulative h=6, h=12):")
    i = est[(est.rq == "RQ4") & est.cumulative & est.h.isin([6, 12])]
    print(i[["spec", "term", "h", "beta", "se"]].round(4).to_string(index=False))
    print(groups.round(2).to_string())
    print("\nRobustness (cumulative h=6 and h=12, term=shock):")
    r = s[(s.rq == "ROB") & s.cumulative & s.h.isin([6, 12])]
    print(r.pivot_table(index=["outcome", "spec"], columns="h", values=["beta", "se"]).round(4).to_string())
    a = est[(est.spec == "f asymmetry") & est.cumulative & est.h.isin([6, 12])]
    print(a[["outcome", "term", "h", "beta", "se"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
