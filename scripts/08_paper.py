"""Render the manuscript from paper/manuscript_template.md and the output tables.

Every number in the text comes from output/tables via the `n` dictionary, so
`./run_all.sh` regenerates the paper after any data or specification change.

Writes paper/manuscript.md, paper/manuscript.docx and output/tables/paper_numbers.json.
"""

import json
from pathlib import Path

import jinja2
import numpy as np
import pandas as pd
import pypandoc

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "output" / "tables"
PAPER = ROOT / "paper"

REGION_NAMES = {
    "NCR": "National Capital Region", "CAR": "Cordillera (CAR)", "R01": "I Ilocos", "R02": "II Cagayan Valley",
    "R03": "III Central Luzon", "R04A": "IV-A CALABARZON", "R04B": "MIMAROPA", "R05": "V Bicol",
    "R06": "VI Western Visayas", "R07": "VII Central Visayas", "R08": "VIII Eastern Visayas",
    "R09": "IX Zamboanga Peninsula", "R10": "X Northern Mindanao", "R11": "XI Davao", "R12": "XII SOCCSKSARGEN",
    "R13": "XIII Caraga", "BARMM": "BARMM", "PH": "Philippines",
}


def f(x, d=3, sign=False):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "n.a."
    s = f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
    return s.replace("-", "−")


def stars(b, se):
    t = abs(b / se) if se else 0
    return "***" if t > 2.576 else "**" if t > 1.96 else "*" if t > 1.645 else ""


def main():
    est = pd.read_csv(TAB / "estimates.csv")
    rep = pd.read_csv(TAB / "replication_eu_ph.csv")
    e1 = pd.read_csv(TAB / "e1_national_2026.csv", parse_dates=["date"])
    e2 = pd.read_csv(TAB / "e2_regional_2026.csv")
    e4 = pd.read_csv(TAB / "e4_mechanism.csv")
    e5 = pd.read_csv(TAB / "e5_decomposition_2026.csv", dtype={"coicop": str}).set_index("coicop")
    ctx = pd.read_csv(TAB / "context_2026.csv", parse_dates=["date"]).set_index("date")
    groups = pd.read_csv(TAB / "region_groups.csv").set_index("region")
    panel = pd.read_parquet(ROOT / "data" / "processed" / "panel_regional.parquet")

    def g(rq, spec, outcome, h, cum=True, term="shock"):
        q = est[(est.rq == rq) & (est.spec == spec) & (est.outcome == outcome) & (est.h == h)
                & (est.cumulative == cum) & (est.term == term)]
        assert len(q) == 1, (rq, spec, outcome, h, cum, term, len(q))
        return q.iloc[0]

    n = {}
    # --- RQ1
    for y, k in [("d_cpi_all", "all"), ("d_cpi_b30", "b30")]:
        for h in (0, 3, 6, 12):
            r = g("RQ1", "baseline", y, h)
            n[f"rq1_{k}_c{h}"], n[f"rq1_{k}_c{h}_se"] = f(r.beta), f(r.se)
    n["rq1_all_b0_10pct"] = f(10 * g("RQ1", "baseline", "d_cpi_all", 0).beta, 2)
    n["rq1_all_c12_10pct"] = f(10 * g("RQ1", "baseline", "d_cpi_all", 12).beta, 1)
    n["crude_c12"] = f(g("ROB", "a dubai crude php", "d_cpi_all", 12).beta)
    n["crude_c6"] = f(g("ROB", "a dubai crude php", "d_cpi_all", 6).beta)
    n["crude_share"] = f(100 * g("ROB", "a dubai crude php", "d_cpi_all", 12).beta /
                         g("RQ1", "baseline", "d_cpi_all", 12).beta, 0)
    # --- RQ2 / RQ4 pooled
    for h in (3, 6, 12):
        r = g("RQ2", "baseline", "d_ratio", h)
        n[f"rq2_c{h}"], n[f"rq2_c{h}_se"], n[f"rq2_c{h}_lo"], n[f"rq2_c{h}_hi"] = f(r.beta, 4), f(r.se, 4), f(r.lo, 4), f(r.hi, 4)
        r = g("RQ4", "pooled", "d_ratio", h)
        n[f"rq4_c{h}"], n[f"rq4_c{h}_se"], n[f"rq4_c{h}_lo"], n[f"rq4_c{h}_hi"] = f(r.beta, 4), f(r.se, 4), f(r.lo, 4), f(r.hi, 4)
    loo = est[(est.rq == "ROB") & est.spec.str.startswith("j drop") & est.cumulative & (est.h == 6) & (est.term == "shock")]
    n["loo_min"], n["loo_max"] = f(loo.beta.min(), 4), f(loo.beta.max(), 4)
    sig_h = est[(est.rq == "RQ2") & est.cumulative & (est.term == "shock") & ((est.hi < 0) | (est.lo > 0))].h.tolist()
    n["rq2_sig_h"] = ", ".join(str(h) for h in sig_h)
    for spec, k in [("regional 2001-2012", "p1"), ("regional 2013-", "p2"), ("regional excl 2008", "x08"),
                    ("2013- ratio", "nat13"), ("national excl 2008", "natx08")]:
        r = g("RQ3b", spec, "d_ratio", 6)
        n[f"split_{k}"], n[f"split_{k}_se"] = f(r.beta, 4), f(r.se, 4)
    for spec, k in [("b macro controls", "macro"), ("h gasoline 07.2.2.2", "gas"), ("i WB pump price", "wb"),
                    ("g to Jun 2019", "paperwin"), ("d excl 2026", "x26")]:
        r = g("ROB", spec, "d_ratio", 6)
        n[f"rob_{k}"], n[f"rob_{k}_se"] = f(r.beta, 4), f(r.se, 4)
    asy_neg = g("ROB", "f asymmetry", "d_cpi_all", 12)
    asy_pos = g("ROB", "f asymmetry", "d_cpi_all", 12, term="shock_x_pos")
    n["asy_neg"], n["asy_pos_extra"], n["asy_pos_extra_se"] = f(asy_neg.beta), f(asy_pos.beta), f(asy_pos.se)
    # --- RQ3
    dec = pd.read_csv(TAB / "rq3_gap_decomposition.csv", dtype={"coicop": str}).set_index("coicop")
    for c, k in [("07", "transport"), ("04", "housing"), ("01", "food"), ("11", "restaurants"), ("10", "education")]:
        n[f"rq3_{k}"], n[f"rq3_{k}_se"] = f(dec.loc[c, "beta"]), f(dec.loc[c, "se"])
    n["rq3_nsig"] = int(((dec.beta / dec.se) > 1.645).sum())
    n["rq3_gap_pred"] = f(dec.contrib_gap.sum(), 4, sign=True)
    for c in ("c04", "c07", "c01"):
        n[f"rq3b_{c}_all"] = f(g("RQ3b", "2013- all-income", f"d_{c}", 12).beta)
        n[f"rq3b_{c}_b30"] = f(g("RQ3b", "2013- bottom 30%", f"d_b30_{c}", 12).beta)
    # --- RQ4 interactions
    for gname in ["high_poverty", "high_food", "mindanao", "island"]:
        r = g("RQ4", f"x {gname}", "d_ratio", 12, term=f"shock_x_{gname}")
        n[f"rq4_{gname}"], n[f"rq4_{gname}_se"] = f(r.beta, 4), f(r.se, 4)
    n["food_share_min"], n["food_share_max"] = f(groups.food_share_2018.min(), 1), f(groups.food_share_2018.max(), 1)
    # --- replication
    rr = rep[rep.spec.str.endswith("[cluster]")].set_index(["spec", "h"]).beta
    n["rep_after"] = f(rr[("G1 after tax [cluster]", 0)])
    n["rep_before"] = f(rr[("G2 before tax + tax control [cluster]", 0)])
    n["rep_brent"] = f(rr[("G2 Brent in euro [cluster]", 0)])
    n["rep_hicp0"] = f(rr[("G3 HICP fuels CP0722 [cluster]", 0)])
    n["rep_hicp1"] = f(rr[("G3 HICP fuels CP0722 [cluster]", 1)])
    ph = rep[rep.spec.str.startswith("PH alone")].set_index("h").beta
    n["rep_ph0"], n["rep_ph1"] = f(ph[0]), f(ph[1])
    # --- 2026 context
    for m in ["2026-02-01", "2026-03-01", "2026-04-01", "2026-08-01"]:
        k = pd.Timestamp(m).strftime("%b").lower()
        n[f"yoy_all_{k}"] = f(ctx.loc[m, "inflation_all_yoy"], 1)
        n[f"yoy_b30_{k}"] = f(ctx.loc[m, "inflation_b30_yoy"], 1)
        n[f"yoy_fuel_{k}"] = f(ctx.loc[m, "fuel_yoy"], 0)
    # --- E1
    aug = e1[e1.date == "2026-08-01"].set_index("series")
    apr = e1[e1.date == "2026-04-01"].set_index("series")
    for s, k in [("cpi_all", "all"), ("cpi_b30", "b30"), ("ratio_all_over_b30", "gap")]:
        n[f"e1_{k}_fd"], n[f"e1_{k}_lo"], n[f"e1_{k}_hi"], n[f"e1_{k}_act"] = (
            f(aug.loc[s, "beta"], 2), f(aug.loc[s, "lo"], 2), f(aug.loc[s, "hi"], 2), f(aug.loc[s, "actual"], 2))
        n[f"e1_{k}_share"] = f(100 * aug.loc[s, "beta"] / aug.loc[s, "actual"], 0)
        n[f"e1_{k}_fd_apr"], n[f"e1_{k}_act_apr"] = f(apr.loc[s, "beta"], 2), f(apr.loc[s, "actual"], 2)
    n["fuel_cum_aug"] = f(aug.loc["cpi_all", "fuel_cum"], 1)
    n["fuel_cum_apr"] = f(apr.loc["cpi_all", "fuel_cum"], 1)
    # --- E2 / E3
    r2 = e2[e2.region != "PH"]
    phr = e2[e2.region == "PH"].iloc[0]
    n["e3_ph_cost"] = f(phr.extra_cost_php_month, 0)
    n["e3_ph_line"] = f(phr.poverty_line_family5_monthly_dec2025, 0)
    act_cost = phr.poverty_line_family5_monthly_dec2025 * (np.exp(phr.actual_b30 / 100) - 1)
    n["e3_ph_actual_cost"] = f(act_cost, 0)
    lo, hi = r2.loc[r2.extra_cost_php_month.idxmin()], r2.loc[r2.extra_cost_php_month.idxmax()]
    n["e3_min"], n["e3_min_reg"] = f(lo.extra_cost_php_month, 0), REGION_NAMES[lo.region]
    n["e3_max"], n["e3_max_reg"] = f(hi.extra_cost_php_month, 0), REGION_NAMES[hi.region]
    a_hi = r2.sort_values("actual_b30", ascending=False).head(5)
    n["e2_top_actual"] = ", ".join(f"{REGION_NAMES[r.region]} ({f(r.actual_b30, 1)})" for _, r in a_hi.iterrows())
    n["e2_ncr_actual"] = f(r2.set_index("region").loc["NCR", "actual_b30"], 1)
    n["e2_ncr_fd"] = f(r2.set_index("region").loc["NCR", "fuel_driven_b30"], 1)
    mind = r2[r2.region.isin(["R09", "R10", "R11", "R12", "R13", "BARMM"])]
    n["e2_mind_share"] = f(100 * mind.fuel_driven_b30.mean() / mind.actual_b30.mean(), 0)
    luz = r2[r2.region.isin(["NCR", "CAR", "R01", "R02", "R03", "R04A"])]
    n["e2_luz_share"] = f(100 * luz.fuel_driven_b30.mean() / luz.actual_b30.mean(), 0)
    n["lpg_relief_share"] = f(100 * 37 / phr.extra_cost_php_month, 0)
    # --- E4
    m4 = e4[e4.h == 12].set_index(["item", "basket"])
    for item in ["e0452", "e0453", "e0454", "t073", "f0111", "e045"]:
        for b in ("all", "b30"):
            n[f"e4_{item}_{b}"] = f(m4.loc[(item, b), "beta"])
            n[f"e4_{item}_{b}_w"] = f(m4.loc[(item, b), "weight"], 2)
    # --- E5
    for c, k in [("0", "total"), ("01.1", "food"), ("01.1.1", "cereals"), ("07.3", "fares"), ("04.5", "hhfuel"),
                 ("07.2", "ownfuel"), ("04.1", "rent"), ("02.3", "tobacco")]:
        n[f"e5_{k}_gap"] = f(e5.loc[c, "gap_pp"], 2, sign=True)
    n["e5_all_total"], n["e5_b30_total"] = f(e5.loc["0", "pct_change_all"], 2), f(e5.loc["0", "pct_change_b30"], 2)
    n["e5_cereal_pct_all"], n["e5_cereal_pct_b30"] = f(e5.loc["01.1.1.1", "pct_change_all"], 1), f(e5.loc["01.1.1.1", "pct_change_b30"], 1)
    n["e5_cereal_w_all"], n["e5_cereal_w_b30"] = f(e5.loc["01.1.1.1", "weight_all"], 1), f(e5.loc["01.1.1.1", "weight_b30"], 1)
    n["e5_fares_pct_all"], n["e5_fares_pct_b30"] = f(e5.loc["07.3", "pct_change_all"], 1), f(e5.loc["07.3", "pct_change_b30"], 1)
    # --- reference-study cumulative responses (sum of Annex Table betas, h = 0..6)
    tg = pd.read_csv(ROOT / "replication" / "kpodar_liu_2021_targets.csv")
    tg = tg[tg.source.str.startswith("annex_table")]
    n["kl_dev_cum6"] = f(tg[tg["sample"] == "developing"].beta.sum())
    n["kl_adv_cum6"] = f(tg[tg["sample"] == "advanced"].beta.sum())
    n["kl_dev_b0"], n["kl_adv_b0"] = f(tg[(tg["sample"] == "developing") & (tg.h == "0")].beta.iloc[0]), \
        f(tg[(tg["sample"] == "advanced") & (tg.h == "0")].beta.iloc[0])
    w = pd.read_parquet(ROOT / "data" / "processed" / "psa_cpi_weights.parquet")
    w = w[(w.region == "PH") & (w.commodity_code == "07.2.2")].set_index("file").weight
    wa, wb = w["cpi_all_2018old_weights"], w["cpi_b30_2018old_weights"]
    n["w_fuel_all"], n["w_fuel_b30"] = f(wa, 2), f(wb, 2)
    b0a, b0b = g("RQ1", "baseline", "d_cpi_all", 0).beta, g("RQ1", "baseline", "d_cpi_b30", 0).beta
    n["direct_share_all"], n["direct_share_b30"] = f(100 * wa / 100 / b0a, 0), f(100 * wb / 100 / b0b, 0)

    macro = pd.read_parquet(ROOT / "data" / "processed" / "macro_national.parquet").set_index("date")
    n["peso_dep_feb_aug"] = f(100 * np.log(macro.loc["2026-08-01", "php_usd"] / macro.loc["2026-02-01", "php_usd"]), 1)
    n["policy_feb"], n["policy_aug"] = f(macro.loc["2026-02-01", "policy_rate"], 2), f(macro.loc["2026-08-01", "policy_rate"], 2)
    n["n_hikes"] = int((macro.loc["2026-03-01":"2026-08-01", "policy_rate"].diff() > 0).sum())
    for c, k in [("01", "food"), ("07", "transport")]:
        n[f"w_{k}_all"], n[f"w_{k}_b30"] = f(dec.loc[c, "w_all"], 1), f(dec.loc[c, "w_b30"], 1)
    n["gap6_10pct"] = f(-10 * g("RQ4", "pooled", "d_ratio", 6).beta, 1)
    n["all6_10pct"] = f(10 * g("RQ1", "baseline", "d_cpi_all", 6).beta, 1)
    names = [REGION_NAMES[r] for r in a_hi.region]
    n["e2_top_names"] = ", ".join(names[:-1]) + " and " + names[-1]
    n["n_hikes_word"] = ["no", "one", "two", "three", "four", "five", "six"][n["n_hikes"]]
    n["gap_yoy_apr"] = f(ctx.loc["2026-04-01", "inflation_b30_yoy"] - ctx.loc["2026-04-01", "inflation_all_yoy"], 1)
    n["gap_yoy_aug"] = f(ctx.loc["2026-08-01", "inflation_b30_yoy"] - ctx.loc["2026-08-01", "inflation_all_yoy"], 1)

    # --- data facts
    ph_rows = panel[panel.region == "PH"]
    n["n_months"] = int(ph_rows[(ph_rows.date >= "2001-01-01")].d_ratio.notna().sum())
    n["poverty_min"], n["poverty_max"] = f(groups.poverty_2018.min(), 1), f(groups.poverty_2018.max(), 1)

    tables = make_tables(est, g, groups, e2, e4, f, stars)
    (TAB / "paper_numbers.json").write_text(json.dumps(n, indent=1, ensure_ascii=False))

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(PAPER), undefined=jinja2.StrictUndefined,
                             keep_trailing_newline=True,
                             comment_start_string="<#--", comment_end_string="--#>")  # pandoc uses {#refs}
    text = env.get_template("manuscript_template.md").render(n=n, t=tables)
    (PAPER / "manuscript.md").write_text(text)
    pypandoc.convert_file(str(PAPER / "manuscript.md"), "docx", outputfile=str(PAPER / "manuscript.docx"),
                          extra_args=["--citeproc", f"--bibliography={PAPER / 'references.bib'}",
                                      f"--resource-path={PAPER}:{ROOT}", "--metadata=link-citations:true"])
    print("wrote paper/manuscript.md and paper/manuscript.docx;", len(n), "numbers")


def make_tables(est, g, groups, e2, e4, f, stars):
    t = {}
    # Table 2: main cumulative responses
    rows = ["| Horizon (months) | CPI, all income | CPI, bottom 30% | Gap ln(CPI all/CPI b30), national | Gap, 17-region panel |",
            "|---|---|---|---|---|"]
    for h in (0, 3, 6, 9, 12):
        cells = []
        for rq, spec, y, d in [("RQ1", "baseline", "d_cpi_all", 3), ("RQ1", "baseline", "d_cpi_b30", 3),
                               ("RQ2", "baseline", "d_ratio", 4), ("RQ4", "pooled", "d_ratio", 4)]:
            r = g(rq, spec, y, h)
            cells.append(f"{f(r.beta, d)}{stars(r.beta, r.se)} ({f(r.se, d)})")
        rows.append(f"| {h} | " + " | ".join(cells) + " |")
    t["main"] = "\n".join(rows)

    # Table 3: robustness of the gap at h = 6 and 12
    specs = [("RQ2", "baseline", "Baseline, national"), ("RQ4", "pooled", "Baseline, 17-region panel"),
             ("ROB", "a dubai crude php", "(a) Shock: Dubai crude in pesos"),
             ("ROB", "b macro controls", "(b) + PHP/USD, policy rate, FAO food index"),
             ("ROB", "c p=6", "(c) 6 lags"), ("ROB", "c p=18", "(c) 18 lags"),
             ("ROB", "d excl 2020", "(d) Excluding 2020"), ("ROB", "d excl 2026", "(d) Shock dates to Dec 2025 only"),
             ("ROB", "e splice dummies", "(e) Base-change dummies (Jan 2012, Jan 2018)"),
             ("ROB", "g to Jun 2019", "(g) Reference study's window (to Jun 2019)"),
             ("ROB", "h gasoline 07.2.2.2", "(h) Shock: gasoline index, 2019–2026"),
             ("ROB", "i WB pump price", "(i) Shock: World Bank pump price, 2018–2025"),
             ("ROB", "k drop flagged 2026", "(k) Panel, drop re-mapped 2026 observations"),
             ("ROB", "l national shock", "(l) Panel, national instead of regional shock"),
             ("RQ3b", "national excl 2008", "Supplementary: national, excluding 2008"),
             ("RQ3b", "regional excl 2008", "Supplementary: panel, excluding 2008"),
             ("RQ3b", "regional 2001-2012", "Supplementary: panel, 2001–2012"),
             ("RQ3b", "regional 2013-", "Supplementary: panel, 2013–2026")]
    rows = ["| Specification | Gap, h = 6 | Gap, h = 12 | CPI all, h = 12 |", "|---|---|---|---|"]
    for rq, spec, lab in specs:
        a, b = g(rq, spec, "d_ratio", 6), g(rq, spec, "d_ratio", 12)
        try:
            c = g("RQ1", "baseline", "d_cpi_all", 12) if rq == "RQ2" else g(rq, spec, "d_cpi_all", 12)
            cc = f"{f(c.beta)}{stars(c.beta, c.se)} ({f(c.se)})"
        except AssertionError:
            cc = "—"
        rows.append(f"| {lab} | {f(a.beta, 4)}{stars(a.beta, a.se)} ({f(a.se, 4)}) | "
                    f"{f(b.beta, 4)}{stars(b.beta, b.se)} ({f(b.se, 4)}) | {cc} |")
    t["robust"] = "\n".join(rows)

    # Table 4: CPI divisions
    dec = pd.read_csv(TAB / "rq3_gap_decomposition.csv", dtype={"coicop": str})
    rows = ["| COICOP division | Weight, all income (%) | Weight, bottom 30% (%) | Cumulative response, h = 12 |",
            "|---|---|---|---|"]
    for _, r in dec.sort_values("beta", ascending=False).iterrows():
        rows.append(f"| {r.coicop} {r.division} | {f(r.w_all, 1)} | {f(r.w_b30, 1)} | "
                    f"{f(r.beta)}{stars(r.beta, r.se)} ({f(r.se)}) |")
    t["components"] = "\n".join(rows)

    # Table 5: regional interactions
    labels = {"high_poverty": "High poverty (2018 incidence above median)",
              "high_food": "High food share of the regional basket (above median)",
              "mindanao": "Mindanao", "island": "Island regions (MIMAROPA, VI, VII, VIII)"}
    rows = ["| Group G | Base effect, h = 6 | Extra effect θ, h = 6 | Base effect, h = 12 | Extra effect θ, h = 12 |",
            "|---|---|---|---|---|"]
    for gname, lab in labels.items():
        cells = []
        for h in (6, 12):
            b = g("RQ4", f"x {gname}", "d_ratio", h)
            th = g("RQ4", f"x {gname}", "d_ratio", h, term=f"shock_x_{gname}")
            cells += [f"{f(b.beta, 4)}{stars(b.beta, b.se)} ({f(b.se, 4)})",
                      f"{f(th.beta, 4)}{stars(th.beta, th.se)} ({f(th.se, 4)})"]
        rows.append(f"| {lab} | " + " | ".join(cells) + " |")
    t["regions"] = "\n".join(rows)

    # Table 6: 2026 by region
    rows = ["| Region | Poverty 2018 (%) | Fuel price rise, Dec 2025–Aug 2026 (%) | Fuel-driven rise, bottom-30% CPI | Actual rise, bottom-30% CPI | Fuel-driven extra cost, poverty-line family of five (PHP/month) |",
            "|---|---|---|---|---|---|"]
    for _, r in e2.iterrows():
        pov = r.poverty_2018
        flag = "†" if r.new_geo_ext else ""
        rows.append(f"| {REGION_NAMES[r.region]}{flag} | {f(pov, 1)} | {f(r.fuel_change_pct, 1)} | "
                    f"{f(r.fuel_driven_b30, 2)} [{f(r.fuel_driven_b30_lo, 2)}, {f(r.fuel_driven_b30_hi, 2)}] | "
                    f"{f(r.actual_b30, 2)} | {f(r.extra_cost_php_month, 0)} |")
    t["regional2026"] = "\n".join(rows)

    # Table 7: mechanism
    names = {"e045": "04.5 Electricity, gas and other fuels", "e0452": "04.5.2 Gas (LPG)",
             "e0453": "04.5.3 Liquid fuels (kerosene)", "e0454": "04.5.4 Solid fuels (charcoal, wood)",
             "t073": "07.3 Passenger transport services (fares)", "f0111": "01.1.1 Cereals and cereal products"}
    m = e4[e4.h == 12].set_index(["item", "basket"])
    rows = ["| Item | Weight, all (%) | Weight, b30 (%) | Response, all-income index | Response, bottom-30% index |",
            "|---|---|---|---|---|"]
    for item, lab in names.items():
        a, b = m.loc[(item, "all")], m.loc[(item, "b30")]
        rows.append(f"| {lab} | {f(a.weight, 2)} | {f(b.weight, 2)} | {f(a.beta)}{stars(a.beta, a.se)} ({f(a.se)}) | "
                    f"{f(b.beta)}{stars(b.beta, b.se)} ({f(b.se)}) |")
    t["mechanism"] = "\n".join(rows)
    return t


if __name__ == "__main__":
    main()
