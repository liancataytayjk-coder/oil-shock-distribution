"""Render both papers from their templates and the output tables, in the house style, with PDFs.

Every number in the text comes from output/tables (the `n` dictionary, saved as
output/tables/paper_numbers.json) and every table is built here (`t`), so a rerun of the
pipeline updates both papers. Writes paper/working_paper.{md,docx,pdf} and
paper/article.{md,docx,pdf}. The PDF step needs LibreOffice (skipped if not installed).
"""

import json
import shutil
import subprocess
import sys

import jinja2
import numpy as np
import pandas as pd
import pypandoc

import data_io
from catalog import RESULTS, SOURCES
from config import PAPER, ROOT, TAB

STYLE = ROOT / "tools" / "lian_style"
NAMES = {
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


def cell(r, d=3):
    return f"{f(r.beta, d)}{stars(r.beta, r.se)} ({f(r.se, d)})"


def md(header, rows, widths=None):
    """Pipe table; widths (relative, e.g. [3, 1, 1]) set pandoc's column widths through the dash counts."""
    sep = "|" + "".join("-" * max(3, int(w * 6)) + "|" for w in widths) if widths else "|" + "---|" * len(header)
    return "\n".join(["| " + " | ".join(header) + " |", sep] +
                     ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def numbers_and_tables():
    est = pd.read_csv(TAB / "estimates.csv")
    e1 = pd.read_csv(TAB / "rq3_national.csv", parse_dates=["date"])
    e2 = pd.read_csv(TAB / "rq3_regional.csv")
    e4 = pd.read_csv(TAB / "rq3_household_items.csv")
    e5 = pd.read_csv(TAB / "rq3_decomposition.csv", dtype={"coicop": str}).set_index("coicop")
    ctx = pd.read_csv(TAB / "rq3_context.csv", parse_dates=["date"]).set_index("date")
    dec = pd.read_csv(TAB / "rq2_weights_decomposition.csv", dtype={"coicop": str}).set_index("coicop")
    info = data_io.region_info()
    nat = data_io.national().set_index("date")

    def g(rq, spec, outcome, h, cum=True, term="shock"):
        q = est[(est.rq == rq) & (est.spec == spec) & (est.outcome == outcome) & (est.h == h)
                & (est.cumulative == cum) & (est.term == term)]
        assert len(q) == 1, (rq, spec, outcome, h, cum, term, len(q))
        return q.iloc[0]

    n, t = {}, {}
    # RQ1
    for y, k in [("d_cpi_all", "all"), ("d_cpi_b30", "b30")]:
        for h in (0, 3, 6, 12):
            r = g("RQ1", "baseline", y, h)
            n[f"rq1_{k}_c{h}"], n[f"rq1_{k}_c{h}_se"] = f(r.beta), f(r.se)
    n["rq1_all_c12_10pct"] = f(10 * g("RQ1", "baseline", "d_cpi_all", 12).beta, 1)
    n["all6_10pct"] = f(10 * g("RQ1", "baseline", "d_cpi_all", 6).beta, 1)
    n["crude_c12"] = f(g("ROB", "dubai crude php", "d_cpi_all", 12).beta)
    n["crude_share"] = f(100 * g("ROB", "dubai crude php", "d_cpi_all", 12).beta /
                         g("RQ1", "baseline", "d_cpi_all", 12).beta, 0)
    # RQ2
    for h in (3, 6, 12):
        for spec, k in [("national", "rq2"), ("panel", "pan")]:
            r = g("RQ2", spec, "d_ratio", h)
            n[f"{k}_c{h}"], n[f"{k}_c{h}_se"] = f(r.beta, 4), f(r.se, 4)
    sig = est[(est.rq == "RQ2") & (est.spec == "national") & est.cumulative & (est.term == "shock")
              & ((est.hi < 0) | (est.lo > 0))].h.tolist()
    n["rq2_sig_h"] = ", ".join(str(h) for h in sig)
    sigp = est[(est.rq == "RQ2") & (est.spec == "panel") & est.cumulative & (est.term == "shock")
               & ((est.hi < 0) | (est.lo > 0))].h.tolist()
    n["pan_sig_from"], n["pan_sig_n"] = min(sigp), len(sigp)
    n["gap6_10pct"] = f(-10 * g("RQ2", "panel", "d_ratio", 6).beta, 1)
    loo = est[(est.rq == "ROB") & est.spec.str.startswith("drop ") & est.cumulative & (est.h == 6)]
    n["loo_min"], n["loo_max"] = f(loo.beta.min(), 4), f(loo.beta.max(), 4)
    for spec, k in [("dubai crude php", "crude"), ("macro controls", "macro"), ("excl 2020", "x20")]:
        r = g("ROB", spec, "d_ratio", 6)
        n[f"rob_{k}"], n[f"rob_{k}_se"] = f(r.beta, 4), f(r.se, 4)
    for spec, k in [("panel 2001-2012", "p1"), ("panel 2013-2026", "p2")]:
        r = g("ROB", spec, "d_ratio", 6)
        n[f"split_{k}"], n[f"split_{k}_se"] = f(r.beta, 4), f(r.se, 4)
    for spec, k in [("gasoline 07.2.2.2", "gas"), ("WB pump price", "wb"), ("panel excl 2008", "px08")]:
        r = g("APP", spec, "d_ratio", 6)
        n[f"app_{k}"] = f(r.beta, 4)
    # lead convention (D13) and VAR (D14)
    for y, k in [("d_cpi_all", "all"), ("d_ratio", "gap")]:
        d = 3 if k == "all" else 4
        for h in (1, 2, 6, 12):
            r = g("ROB", "TZ leads 1..h", y, h)
            n[f"tz_{k}_c{h}"], n[f"tz_{k}_c{h}_se"] = f(r.beta, d), f(r.se, d)
    for h in (1, 2):
        n[f"rq1_all_c{h}"] = f(g("RQ1", "baseline", "d_cpi_all", h).beta)
    r = g("ROB", "panel TZ leads 1..h", "d_ratio", 6)
    n["tz_pan_c6"], n["tz_pan_c6_se"] = f(r.beta, 4), f(r.se, 4)
    var = pd.read_csv(TAB / "var_comparison.csv").set_index(["outcome", "h"])
    for y, k in [("d_cpi_all", "all"), ("d_ratio", "gap")]:
        d = 3 if k == "all" else 4
        for h in (6, 12):
            v = var.loc[(y, h)]
            n[f"var_{k}_c{h}"], n[f"var_{k}_c{h}_lo"], n[f"var_{k}_c{h}_hi"] = f(v["var"], d), f(v.var_lo, d), f(v.var_hi, d)
            n[f"var1_{k}_c{h}"], n[f"lpnl_{k}_c{h}"] = f(v.var_onetime, d), f(v.lp_noleads, d)
    # RQ2 why
    for c, k in [("07", "transport"), ("04", "housing"), ("01", "food"), ("11", "restaurants")]:
        n[f"div_{k}"], n[f"div_{k}_se"] = f(dec.loc[c, "beta"]), f(dec.loc[c, "se"])
    n["div_nsig"] = int(((dec.beta / dec.se) > 1.645).sum())
    n["gap_weights_only"] = f(dec.contrib_gap.sum(), 4, sign=True)
    for c, k in [("01", "food"), ("04", "housing"), ("07", "transport"), ("11", "restaurants")]:
        n[f"dec_{k}"] = f(dec.loc[c, "contrib_gap"], 4, sign=True)
    n["dec_other"] = f(dec.drop(["01", "04", "07", "11"]).contrib_gap.sum(), 4, sign=True)
    n["within12"] = f(g("RQ2", "national", "d_ratio", 12).beta - dec.contrib_gap.sum(), 4)
    n["within12_pan"] = f(g("RQ2", "panel", "d_ratio", 12).beta - dec.contrib_gap.sum(), 4)
    for c in ("c04", "c07", "c01"):
        n[f"why_{c}_all"] = f(g("WHY", "2013- all income", f"d_{c}", 12).beta)
        n[f"why_{c}_b30"] = f(g("WHY", "2013- bottom 30%", f"d_b30_{c}", 12).beta)
    for c, k in [("01", "food"), ("07", "transport"), ("07.2.2", "fuel")]:
        wa, wb = data_io.weights("all").get(c), data_io.weights("b30").get(c)
        n[f"w_{k}_all"], n[f"w_{k}_b30"] = f(wa, 2 if k == "fuel" else 1), f(wb, 2 if k == "fuel" else 1)
    b0a, b0b = g("RQ1", "baseline", "d_cpi_all", 0).beta, g("RQ1", "baseline", "d_cpi_b30", 0).beta
    n["direct_share_all"] = f(data_io.weights("all")["07.2.2"] / b0a, 0)
    n["direct_share_b30"] = f(data_io.weights("b30")["07.2.2"] / b0b, 0)
    # region groups (appendix)
    for gname in ["high_poverty", "high_food", "mindanao", "island"]:
        r = g("APP", f"x {gname}", "d_ratio", 12, term=f"shock_x_{gname}")
        n[f"grp_{gname}"], n[f"grp_{gname}_se"] = f(r.beta, 4), f(r.se, 4)
    # reference study (S12)
    tg = pd.read_csv(ROOT / "data" / "reference" / "kpodar_liu_2021_targets.csv")
    tg = tg[tg.source.str.startswith("annex_table")]
    n["kl_dev_cum6"] = f(tg[tg["sample"] == "developing"].beta.sum())
    n["kl_adv_b0"] = f(tg[(tg["sample"] == "advanced") & (tg.h.astype(str) == "0")].beta.iloc[0])
    n["kl_dev_b0"] = f(tg[(tg["sample"] == "developing") & (tg.h.astype(str) == "0")].beta.iloc[0])
    # 2026 context
    for m in ["2026-02-01", "2026-03-01", "2026-04-01", "2026-08-01"]:
        k = pd.Timestamp(m).strftime("%b").lower()
        n[f"yoy_all_{k}"] = f(ctx.loc[m, "inflation_all_yoy"], 1)
        n[f"yoy_b30_{k}"] = f(ctx.loc[m, "inflation_b30_yoy"], 1)
        n[f"yoy_fuel_{k}"] = f(ctx.loc[m, "fuel_yoy"], 0)
    n["peso_dep_feb_aug"] = f(100 * np.log(nat.loc["2026-08-01", "php_usd"] / nat.loc["2026-02-01", "php_usd"]), 1)
    n["policy_feb"], n["policy_aug"] = f(nat.loc["2026-02-01", "policy_rate"], 2), f(nat.loc["2026-08-01", "policy_rate"], 2)
    hikes = int((nat.loc["2026-03-01":"2026-08-01", "policy_rate"].diff() > 0).sum())
    n["n_hikes_word"] = ["no", "one", "two", "three", "four", "five", "six"][hikes]
    # RQ3: national out-of-sample
    aug, apr = e1[e1.date == "2026-08-01"].set_index("series"), e1[e1.date == "2026-04-01"].set_index("series")
    for s, k in [("cpi_all", "all"), ("cpi_b30", "b30"), ("gap_all_minus_b30", "gap")]:
        n[f"e1_{k}_fd"], n[f"e1_{k}_lo"], n[f"e1_{k}_hi"], n[f"e1_{k}_act"] = (
            f(aug.loc[s, "beta"], 2), f(aug.loc[s, "lo"], 2), f(aug.loc[s, "hi"], 2), f(aug.loc[s, "actual"], 2))
        n[f"e1_{k}_share"] = f(100 * aug.loc[s, "beta"] / aug.loc[s, "actual"], 0)
    n["fuel_cum_aug"], n["fuel_cum_apr"] = f(aug.loc["cpi_all", "fuel_cum"], 1), f(apr.loc["cpi_all", "fuel_cum"], 1)
    # RQ3: regions and peso cost
    r2, ph = e2[e2.region != "PH"], e2[e2.region == "PH"].iloc[0]
    n["e3_ph_cost"] = f(ph.extra_cost_php_month, 0)
    n["e3_ph_line"] = f"{ph.poverty_line_family5_monthly_dec2025:,.0f}"
    n["e3_ph_actual_cost"] = f(ph.poverty_line_family5_monthly_dec2025 * (np.exp(ph.actual_b30 / 100) - 1), 0)
    lo, hi = r2.loc[r2.extra_cost_php_month.idxmin()], r2.loc[r2.extra_cost_php_month.idxmax()]
    n["e3_min"], n["e3_min_reg"] = f(lo.extra_cost_php_month, 0), NAMES[lo.region]
    n["e3_max"], n["e3_max_reg"] = f(hi.extra_cost_php_month, 0), NAMES[hi.region]
    top = [NAMES[r] for r in r2.sort_values("actual_b30", ascending=False).head(5).region]
    n["e2_top_names"] = ", ".join(top[:-1]) + " and " + top[-1]
    mind = r2[r2.region.isin(["R09", "R10", "R11", "R12", "R13", "BARMM"])]
    luz = r2[r2.region.isin(["NCR", "CAR", "R01", "R02", "R03", "R04A"])]
    n["e2_mind_share"] = f(100 * mind.fuel_driven_b30.mean() / mind.actual_b30.mean(), 0)
    n["e2_luz_share"] = f(100 * luz.fuel_driven_b30.mean() / luz.actual_b30.mean(), 0)
    n["lpg_relief_share"] = f(100 * 37 / ph.extra_cost_php_month, 0)
    # RQ3: household items and decomposition
    m4 = e4[e4.h == 12].set_index(["item", "basket"])
    for item in ["e0452", "e0453", "e0454", "t073", "f0111"]:
        for b in ("all", "b30"):
            n[f"e4_{item}_{b}"] = f(m4.loc[(item, b), "beta"])
            n[f"e4_{item}_{b}_w"] = f(m4.loc[(item, b), "weight"], 2)
    for c, k in [("0", "total"), ("01.1.1", "cereals"), ("07.3", "fares"), ("04.5", "hhfuel"),
                 ("07.2", "ownfuel"), ("04.1", "rent")]:
        n[f"e5_{k}_gap"] = f(e5.loc[c, "gap_pp"], 2, sign=True)
    n["e5_all_total"], n["e5_b30_total"] = f(e5.loc["0", "pct_change_all"], 2), f(e5.loc["0", "pct_change_b30"], 2)
    n["e5_cereal_pct_all"], n["e5_cereal_pct_b30"] = f(e5.loc["01.1.1.1", "pct_change_all"], 1), f(e5.loc["01.1.1.1", "pct_change_b30"], 1)
    n["e5_cereal_w_all"], n["e5_cereal_w_b30"] = f(e5.loc["01.1.1.1", "weight_all"], 1), f(e5.loc["01.1.1.1", "weight_b30"], 1)
    n["e5_fares_pct_all"], n["e5_fares_pct_b30"] = f(e5.loc["07.3", "pct_change_all"], 1), f(e5.loc["07.3", "pct_change_b30"], 1)
    # data facts
    reg = data_io.panel()
    n["panel_obs_h0"] = int(g("RQ2", "panel", "d_ratio", 0).nobs)
    n["panel_obs_h12"] = int(g("RQ2", "panel", "d_ratio", 12).nobs)
    n["nat_obs_h0"] = int(g("RQ1", "baseline", "d_cpi_all", 0).nobs)
    n["poverty_min"], n["poverty_max"] = f(info.loc[info.index != "PH", "poverty_2018"].min(), 1), \
        f(info.loc[info.index != "PH", "poverty_2018"].max(), 1)
    n["n_regions"] = int(reg.region.nunique())

    descriptive(n, t)

    # ---- tables
    t["main"] = md(["Horizon (months)", "CPI, all income", "CPI, bottom 30%", "Gap, national", "Gap, 17-region panel"],
                   [[h, cell(g("RQ1", "baseline", "d_cpi_all", h)), cell(g("RQ1", "baseline", "d_cpi_b30", h)),
                     cell(g("RQ2", "national", "d_ratio", h), 4), cell(g("RQ2", "panel", "d_ratio", h), 4)]
                    for h in (0, 3, 6, 9, 12)])
    rows = []
    for rq, spec, lab in [("RQ2", "national", "Baseline, national"), ("ROB", "dubai crude php", "Shock: Dubai crude in pesos (national)"),
                          ("ROB", "macro controls", "Controls: exchange rate, policy rate, world food prices (national)"),
                          ("ROB", "excl 2020", "Excluding 2020 (national)"),
                          ("ROB", "TZ leads 1..h", "Leads 1 to h, Teulings–Zubanov (national)†"),
                          ("RQ2", "panel", "Baseline, 17-region panel"),
                          ("ROB", "panel TZ leads 1..h", "Leads 1 to h, Teulings–Zubanov (panel)†"),
                          ("ROB", "panel 2001-2012", "Panel, 2001–2012†"), ("ROB", "panel 2013-2026", "Panel, 2013–2026†")]:
        rows.append([lab, cell(g(rq, spec, "d_ratio", 6), 4), cell(g(rq, spec, "d_ratio", 12), 4)])
    v6, v12 = var.loc[("d_ratio", 6)], var.loc[("d_ratio", 12)]
    rows.insert(5, ["VAR, fuel ordered first (national)†", f"{f(v6['var'], 4)} [{f(v6.var_lo, 4)}, {f(v6.var_hi, 4)}]",
                    f"{f(v12['var'], 4)} [{f(v12.var_lo, 4)}, {f(v12.var_hi, 4)}]"])
    loo12 = est[(est.rq == "ROB") & est.spec.str.startswith("drop ") & est.cumulative & (est.h == 12)]
    rows.append(["Panel, leaving out one region at a time (range)", f"{f(loo.beta.min(), 4)} to {f(loo.beta.max(), 4)}",
                 f"{f(loo12.beta.min(), 4)} to {f(loo12.beta.max(), 4)}"])
    t["robust"] = md(["Specification", "Gap, h = 6", "Gap, h = 12"], rows, [5, 3, 3])
    t["crude_all"] = cell(g("ROB", "dubai crude php", "d_cpi_all", 12))
    t["rq1"] = md(["Horizon (months)", "CPI, all income", "CPI, bottom 30%", "Difference (all − bottom 30%)"],
                  [[h, cell(g("RQ1", "baseline", "d_cpi_all", h)), cell(g("RQ1", "baseline", "d_cpi_b30", h)),
                    f(g("RQ1", "baseline", "d_cpi_all", h).beta - g("RQ1", "baseline", "d_cpi_b30", h).beta)]
                   for h in (0, 1, 3, 6, 9, 12)])
    t["gap_side"] = md(["Horizon (months)", "National (Newey–West)", "17-region panel (Driscoll–Kraay)",
                        "Panel observations"],
                       [[h, cell(g("RQ2", "national", "d_ratio", h), 4), cell(g("RQ2", "panel", "d_ratio", h), 4),
                         f"{int(g('RQ2', 'panel', 'd_ratio', h).nobs):,}"] for h in range(13)])
    big = ["01", "04", "07", "11"]
    rows = [[f"{c} {dec.loc[c, 'division']}", f(dec.loc[c, "w_all"], 1), f(dec.loc[c, "w_b30"], 1),
             cell(dec.loc[c]), f(dec.loc[c, "contrib_gap"], 4, sign=True)] for c in big]
    oth = dec.drop(big)
    rows.append(["Other nine divisions", f(oth.w_all.sum(), 1), f(oth.w_b30.sum(), 1), "", f(oth.contrib_gap.sum(), 4, sign=True)])
    rows.append(["(a) Gap from budget shares alone", "", "", "", f(dec.contrib_gap.sum(), 4, sign=True)])
    rows.append(["(b) Estimated gap, national", "", "", "", f(g("RQ2", "national", "d_ratio", 12).beta, 4)])
    rows.append(["(c) Estimated gap, 17-region panel", "", "", "", f(g("RQ2", "panel", "d_ratio", 12).beta, 4)])
    rows.append(["Within-category part, (b) − (a) and (c) − (a)", "", "", "",
                 f"{n['within12']} and {n['within12_pan']}"])
    t["decomp_main"] = md(["Division", "Weight, all (%)", "Weight, bottom 30% (%)", "Response after 12 months",
                           "Contribution to the gap"], rows, [5, 1.6, 1.8, 3, 2.6])
    vv = pd.read_csv(TAB / "var_comparison.csv")
    t["var"] = md(["Horizon", "CPI all: LP", "CPI all: LP, no leads", "CPI all: VAR", "CPI all: VAR, one-time",
                   "Gap: LP", "Gap: LP, no leads", "Gap: VAR", "Gap: VAR, one-time"],
                  [[h] + [f(q[c], 3 if y == "d_cpi_all" else 4) for y in ("d_cpi_all", "d_ratio")
                          for q in [vv[(vv.outcome == y) & (vv.h == h)].iloc[0]] for c in ("lp", "lp_noleads", "var", "var_onetime")]
                   for h in (0, 1, 2, 3, 6, 9, 12)])
    loo_rows = []
    for r in sorted(est[(est.rq == "ROB") & est.spec.str.startswith("drop ")].spec.unique()):
        reg_code = r.replace("drop ", "")
        loo_rows.append([NAMES[reg_code], cell(g("ROB", r, "d_ratio", 6), 4), cell(g("ROB", r, "d_ratio", 12), 4)])
    t["loo"] = md(["Region left out", "Gap, h = 6", "Gap, h = 12"], loo_rows)
    t["divisions"] = md(["COICOP division", "Weight, all income (%)", "Weight, bottom 30% (%)", "Response after 12 months",
                         "Contribution to the gap if prices were the same"],
                        [[f"{c} {r.division}", f(r.w_all, 1), f(r.w_b30, 1), f"{f(r.beta)}{stars(r.beta, r.se)} ({f(r.se)})",
                          f(r.contrib_gap, 4, sign=True)] for c, r in dec.sort_values("beta", ascending=False).iterrows()]
                        + [["Total", "100.0", "100.0", "", f(dec.contrib_gap.sum(), 4, sign=True)]], [5, 1.6, 1.8, 3, 2.6])
    why = []
    for c, lab in [("c01", "01 Food and non-alcoholic beverages"), ("c04", "04 Housing, water, electricity, gas"),
                   ("c07", "07 Transport"), ("c11", "11 Restaurants and accommodation")]:
        why.append([lab, cell(g("WHY", "2013- all income", f"d_{c}", 12)), cell(g("WHY", "2013- bottom 30%", f"d_b30_{c}", 12))])
    t["why"] = md(["Division", "All-income index", "Bottom-30% index"], why)
    labels = {"high_poverty": "High poverty (2018 incidence above the median)",
              "high_food": "High food share (above the median)", "mindanao": "Mindanao",
              "island": "Island regions (MIMAROPA, VI, VII, VIII)"}
    t["groups"] = md(["Group G", "Other regions, h = 12", "Extra effect in G, h = 12"],
                     [[lab, cell(g("APP", f"x {k}", "d_ratio", 12), 4),
                       cell(g("APP", f"x {k}", "d_ratio", 12, term=f"shock_x_{k}"), 4)] for k, lab in labels.items()], [5, 3, 3])
    rows = []
    for rq, spec, lab in [("APP", "p=6", "6 lags"), ("APP", "p=18", "18 lags"), ("APP", "excl 2026", "Shock dates to Dec 2025 only"),
                          ("APP", "splice dummies", "Dummies for the base-change months (Jan 2012, Jan 2018)"),
                          ("APP", "to Jun 2019", "Reference study's window (to Jun 2019)"),
                          ("APP", "gasoline 07.2.2.2", "Shock: gasoline index, 2019–2026"),
                          ("APP", "WB pump price", "Shock: World Bank pump price, 2018–2025"),
                          ("APP", "national excl 2008", "National, excluding 2008"),
                          ("APP", "national 2013-2026", "National, 2013–2026"),
                          ("APP", "panel excl 2008", "Panel, excluding 2008"),
                          ("APP", "drop flagged 2026", "Panel, dropping the re-mapped 2026 months"),
                          ("APP", "national shock", "Panel, national instead of regional fuel index")]:
        a = cell(g(rq, spec, "d_ratio", 6), 4)
        try:
            c = cell(g(rq, spec, "d_cpi_all", 12))
        except AssertionError:
            c = "—"
        rows.append([lab, a, cell(g(rq, spec, "d_ratio", 12), 4), c])
    asy = g("APP", "asymmetry", "d_cpi_all", 12, term="shock_x_pos")
    rows.append(["Asymmetry: extra effect of fuel increases (CPI all, h = 12)", "", "", cell(asy)])
    t["robust_app"] = md(["Specification", "Gap, h = 6", "Gap, h = 12", "CPI all, h = 12"], rows)
    full = []
    groups = [("Baseline", [("RQ2", "national", "National baseline"), ("RQ2", "panel", "17-region panel baseline")]),
              ("Lag length", [("APP", "p=6", "6 lags"), ("APP", "p=18", "18 lags")]),
              ("Lead convention", [("ROB", "TZ leads 1..h", "Leads 1 to h (national)"),
                                   ("ROB", "panel TZ leads 1..h", "Leads 1 to h (panel)")]),
              ("Alternative shocks", [("ROB", "dubai crude php", "Dubai crude in pesos"),
                                      ("APP", "gasoline 07.2.2.2", "Gasoline index 07.2.2.2, 2019–2026"),
                                      ("APP", "WB pump price", "World Bank pump price, 2018–2025"),
                                      ("APP", "national shock", "Panel with the national fuel index")]),
              ("Samples", [("ROB", "excl 2020", "Excluding 2020"), ("APP", "excl 2026", "Shock dates to December 2025"),
                           ("APP", "national excl 2008", "Excluding 2008 (national)"),
                           ("APP", "panel excl 2008", "Excluding 2008 (panel)"),
                           ("APP", "to Jun 2019", "Shock dates to June 2019 (reference study's window)"),
                           ("APP", "national 2013-2026", "National, 2013–2026"),
                           ("ROB", "panel 2001-2012", "Panel, 2001–2012"), ("ROB", "panel 2013-2026", "Panel, 2013–2026"),
                           ("APP", "drop flagged 2026", "Panel without the re-mapped 2026 months")]),
              ("Controls", [("ROB", "macro controls", "Exchange rate, policy rate, world food prices"),
                            ("APP", "splice dummies", "Dummies for the splice months (January 2012, January 2018)")])]
    for gname, specs in groups:
        full.append([f"*{gname}*", "", "", ""])
        for rq, spec, lab in specs:
            try:
                c = cell(g(rq, spec, "d_cpi_all", 12))
            except AssertionError:
                c = "—"
            full.append([lab, cell(g(rq, spec, "d_ratio", 6), 4), cell(g(rq, spec, "d_ratio", 12), 4), c])
    full.append(["*Other*", "", "", ""])
    full.append(["Asymmetry: extra effect of fuel increases", cell(g("APP", "asymmetry", "d_ratio", 6, term="shock_x_pos"), 4),
                 cell(g("APP", "asymmetry", "d_ratio", 12, term="shock_x_pos"), 4), cell(asy)])
    full.append(["Panel, one region left out (range; Table A5)", f"{f(loo.beta.min(), 4)} to {f(loo.beta.max(), 4)}",
                 f"{f(loo12.beta.min(), 4)} to {f(loo12.beta.max(), 4)}", "—"])
    full.append(["VAR, fuel ordered first (Table A6)", f(var.loc[("d_ratio", 6)]["var"], 4), f(var.loc[("d_ratio", 12)]["var"], 4),
                 f(var.loc[("d_cpi_all", 12)]["var"])])
    t["robust_full"] = md(["Specification", "Gap, h = 6", "Gap, h = 12", "CPI all, h = 12"], full, [5, 2.6, 2.6, 2.6])
    t["regional2026"] = md(
        ["Region", "Poverty 2018 (%)", "Fuel price rise (%)", "Fuel-driven rise, bottom-30% CPI", "Actual rise, bottom-30% CPI",
         "Fuel-driven extra cost (PHP/month)"],
        [[NAMES[r.region] + ("†" if r.new_geo_ext else ""), f(r.poverty_2018, 1), f(r.fuel_change_pct, 1),
          f"{f(r.fuel_driven_b30, 2)} [{f(r.fuel_driven_b30_lo, 2)}, {f(r.fuel_driven_b30_hi, 2)}]", f(r.actual_b30, 2),
          f(r.extra_cost_php_month, 0)] for _, r in e2.iterrows()])
    names = {"e0452": "04.5.2 Gas (LPG)", "e0453": "04.5.3 Liquid fuels (kerosene)",
             "e0454": "04.5.4 Solid fuels (charcoal, wood)", "t073": "07.3 Passenger transport (fares)",
             "f0111": "01.1.1 Cereals and cereal products"}
    t["household"] = md(["Item", "Weight, all (%)", "Weight, bottom 30% (%)", "Response, all-income index",
                         "Response, bottom-30% index"],
                        [[lab, f(m4.loc[(i, "all"), "weight"], 2), f(m4.loc[(i, "b30"), "weight"], 2),
                          cell(m4.loc[(i, "all")]), cell(m4.loc[(i, "b30")])] for i, lab in names.items()], [4, 1.5, 1.7, 2.6, 2.6])
    return n, t


def descriptive(n, t):
    sm = pd.read_csv(TAB / "desc_summary.csv")
    an = pd.read_csv(TAB / "desc_annual.csv").set_index("year")
    ep = pd.read_csv(TAB / "desc_episodes.csv")
    cc = pd.read_csv(TAB / "desc_crosscorr.csv").set_index("lag")
    rg = pd.read_csv(TAB / "desc_regional.csv").set_index("region")
    adf = pd.read_csv(TAB / "desc_adf.csv")
    keys = {"Fuel index (07.2.2)": "fuel", "CPI, all income": "all", "CPI, bottom 30%": "b30",
            "Gap: ln(CPI all/CPI b30)": "gap"}
    periods = {"2001–2026 (full)": "full", "2001–2012": "p1", "2013–2019": "p2", "2020–2025": "p3", "2026 (Jan–Aug)": "p4"}
    full = sm[sm.period == "2001–2026 (full)"].set_index("variable")
    for v, k in keys.items():
        n[f"d_{k}_mean_ann"], n[f"d_{k}_sd"] = f(full.loc[v, "annualised_mean"], 2), f(full.loc[v, "sd"], 3)
        n[f"d_{k}_min"], n[f"d_{k}_max"] = f(full.loc[v, "min"], 2), f(full.loc[v, "max"], 2)
    for p, k in periods.items():
        q = sm[sm.period == p].set_index("variable")
        for v, kk in keys.items():
            n[f"d_{kk}_{k}_ann"] = f(q.loc[v, "annualised_mean"], 2)
    n["d_years_b30_higher"], n["d_years_total"] = int((an.loc[:2025, "yoy_gap"] > 0).sum()), int(len(an.loc[:2025]))
    n["d_2008_b30"], n["d_2008_all"], n["d_2008_gap"] = (f(an.loc[2008, "yoy_cpi_b30"], 1), f(an.loc[2008, "yoy_cpi_all"], 1),
                                                        f(an.loc[2008, "yoy_gap"], 1))
    n["d_2025_gap"] = f(an.loc[2025, "yoy_gap"], 1)
    n["d_n_episodes"], n["d_episodes_b30_higher"] = len(ep), int((ep.mean_gap_b30_minus_all > 0).sum())
    r17 = rg.drop(index="PH")
    n["d_cum_gap_ph"] = f(rg.loc["PH", "cum_gap_2001_2025"], 1)
    n["d_cum_gap_min"], n["d_cum_gap_max"] = f(r17.cum_gap_2001_2025.max(), 1), f(r17.cum_gap_2001_2025.min(), 1)
    n["d_cum_gap_min_reg"] = NAMES[r17.cum_gap_2001_2025.idxmax()]
    n["d_cum_gap_max_reg"] = NAMES[r17.cum_gap_2001_2025.idxmin()]
    n["d_corr_pov_gap"] = f(r17[["poverty_2018", "cum_gap_2001_2025"]].corr().iloc[0, 1], 2)
    n["d_corr_food_gap"] = f(r17[["food_share_2018", "cum_gap_2001_2025"]].corr().iloc[0, 1], 2)
    n["d_infl_all_ph"], n["d_infl_b30_ph"] = f(rg.loc["PH", "infl_all_2001_2025"], 2), f(rg.loc["PH", "infl_b30_2001_2025"], 2)
    n["d_adf_level_pmin"] = f(adf[adf.form == "level"].p_value.min(), 2)
    n["d_adf_diff_pmax"] = f(adf[adf.form != "level"].p_value.max(), 3)
    n["d_cc0_all"], n["d_cc0_gap"] = f(cc.loc[0, "CPI, all income"], 2), f(cc.loc[0, "Gap: ln(CPI all/CPI b30)"], 2)
    n["d_cc1_all"], n["d_cc6_all"] = f(cc.loc[1, "CPI, all income"], 2), f(cc.loc[6, "CPI, all income"], 2)
    full_only = sm[sm.period.isin(["2001–2026 (full)", "2001–2012", "2013–2019", "2020–2025", "2026 (Jan–Aug)"])]
    t["d_summary"] = md(["Period", "Variable", "N", "Mean (pp/month)", "Annualised mean", "SD", "Min", "Max"],
                        [[r.period, r.variable, r.n, f(r["mean"]), f(r.annualised_mean, 2), f(r.sd), f(r["min"], 2),
                          f(r["max"], 2)] for _, r in full_only.iterrows()])
    fo = sm[sm.period == "2001–2026 (full)"]
    t["d_summary_full"] = md(["Variable", "N", "Mean (pp/month)", "Annualised mean", "SD", "Min", "Max"],
                             [[r.variable, r.n, f(r["mean"]), f(r.annualised_mean, 2), f(r.sd), f(r["min"], 2),
                               f(r["max"], 2)] for _, r in fo.iterrows()])
    t["d_annual"] = md(["Year", "Inflation, all income (%)", "Inflation, bottom 30% (%)", "Gap, b30 − all (pp)", "Fuel index (% y/y)"],
                       [[f"{y}{'*' if y == 2026 else ''}", f(r.yoy_cpi_all, 2), f(r.yoy_cpi_b30, 2), f(r.yoy_gap, 2, sign=True),
                         f(r.yoy_fuel, 1)] for y, r in an.iterrows()])
    t["d_episodes"] = md(["Episode", "Months", "Peak fuel rise (% y/y)", "Inflation, all (%)", "Inflation, b30 (%)", "Gap (pp)"],
                         [[f"{r.start} to {r.end}", r.months, f(r.peak_fuel_yoy, 1), f(r.mean_infl_all, 2),
                           f(r.mean_infl_b30, 2), f(r.mean_gap_b30_minus_all, 2, sign=True)] for _, r in ep.iterrows()])
    t["d_crosscorr"] = md(["Months later (k)", "CPI, all income", "CPI, bottom 30%", "Gap"],
                          [[k, f(r.iloc[0]), f(r.iloc[1]), f(r.iloc[2])] for k, r in cc.iterrows()])
    t["d_regional"] = md(["Region", "Poverty 2018 (%)", "Food share (%)", "Inflation, all (%)", "Inflation, b30 (%)",
                          "Cumulative gap", "Inflation b30, Aug 2026 (%)"],
                         [[NAMES[reg], f(r.poverty_2018, 1), f(r.food_share_2018, 1), f(r.infl_all_2001_2025, 2),
                           f(r.infl_b30_2001_2025, 2), f(r.cum_gap_2001_2025, 1), f(r.infl_b30_aug2026_yoy, 1)]
                          for reg, r in rg.iterrows()])
    t["d_adf"] = md(["Series", "Form", "ADF statistic", "p-value", "Lags", "N"],
                    [[r.series, r.form, f(r.adf_stat, 2), f(r.p_value, 3), r.lags, r.nobs] for _, r in adf.iterrows()])


def review_matrix():
    rm = pd.read_csv(PAPER / "review_matrix.csv")
    out = []
    for theme, q in rm.groupby("theme", sort=False):
        out.append(f"**{theme}**\n\n" + md(["Author (year)", "Country / sample", "Method", "Key findings"],
                                            [[r["author_year"], r["sample"], r["method"], r["findings"]] for _, r in q.iterrows()]))
    return "\n\n".join(out), rm


ARTICLE_THEMES = {
    "kilian_2009": "Theory: how oil shocks reach prices", "blanchard_gali_2010": "Theory: how oil shocks reach prices",
    "kanzig_2021": "Theory: how oil shocks reach prices",
    "kpodar_liu_2022": "Evidence on pass-through to inflation", "kpodar_abdallah_2017": "Evidence on pass-through to inflation",
    "gelos_ustyugova_2017": "Evidence on pass-through to inflation", "choi_etal_2018": "Evidence on pass-through to inflation",
    "jongwanich_park_2011": "Evidence on pass-through to inflation", "valera_etal_2025": "Evidence on pass-through to inflation",
    "allon_pineda_etal_2026": "Evidence on pass-through to inflation",
    "coady_etal_2015": "Who bears fuel price changes", "dorband_etal_2019": "Who bears fuel price changes",
    "fujii_2013": "Who bears fuel price changes", "jaravel_2021": "Who bears fuel price changes",
    "balie_etal_2021": "Rice prices and policy"}


def review_matrix_article():
    """The 15 studies reviewed in the article (column `article` in review_matrix.csv), grouped as in the text."""
    rm = pd.read_csv(PAPER / "review_matrix.csv")
    rm = rm[rm.article == 1].copy()
    rm["atheme"] = rm.key.map(ARTICLE_THEMES)
    order = list(dict.fromkeys(ARTICLE_THEMES.values()))
    keyorder = list(ARTICLE_THEMES)
    rm["o1"], rm["o2"] = rm.atheme.map(order.index), rm.key.map(keyorder.index)
    rows = []
    for _, r in rm.sort_values(["o1", "o2"]).iterrows():
        rows.append([r["author_year"], r["atheme"], r["sample"], r["method"], r["findings"]])
    assert len(rows) == 15
    return md(["Author (year)", "Strand", "Country / sample", "Method", "Key findings"], rows, [2.2, 2.2, 2.6, 2.8, 6])


def data_appendix(labels):
    src = []
    for s in SOURCES:
        links = "; ".join(f"<{u}>" for u in s["links"])
        src.append(f"**{s['id']}. {s['title']}.** {s['publisher']}. Used for: {s['use']}. Coverage: {s['coverage']}. "
                   f"Files: {', '.join('`' + p + '`' for p in s['files'])}. Link: {links}")
    rows = [[labels.get(o, o), c, s, py.replace("; ", ", "), st]
            for o, c, s, py, st, role in RESULTS if o in labels]
    return "\n\n".join(src), md(["Item", "Content", "Sources", "Python script", "Stata do-file"], rows)


WP_LABELS = {"fig01_conceptual_framework": "Figure 1", "fig02_local_projection": "Figure 2",
             "desc_summary.csv": "Table 2", "fig03_trends": "Figure 3", "desc_annual.csv": "Table 3",
             "desc_episodes.csv": "Table 4", "desc_regional.csv": "Table 5", "desc_adf.csv": "Table 6",
             "estimates.csv (RQ1)": "Table 7 (RQ1 columns)", "fig04_rq1_passthrough": "Figure 4",
             "estimates.csv (RQ2)": "Table 7 (gap columns)", "fig05_rq2_gap": "Figure 5",
             "estimates.csv (WHY 2013-)": "Table 8", "rq2_weights_decomposition.csv": "Table B1",
             "estimates.csv (ROB)": "Table 9", "fig06_robustness": "Figure 6", "fig07_rq3_2026": "Figure 7",
             "rq3_regional.csv": "Table 10", "fig08_rq3_decomposition": "Figure 8",
             "rq3_household_items.csv": "Table 11", "figA1_divisions": "Figure B1",
             "estimates.csv (APP)": "Tables B2–B3", "figA2_region_groups": "Figure B2",
             "figA3_robustness_other": "Figure B3", "figA4_regional": "Figure B4", "desc_crosscorr.csv": "Table B4"}
ART_LABELS = {"fig01_conceptual_framework": "Figure 1", "desc_summary.csv": "Table 1", "fig03_trends": "Figure 2",
              "estimates.csv (RQ1)": "Table 2", "fig04_rq1_passthrough": "Figure 3", "estimates.csv (RQ2)": "Table 3",
              "fig05_rq2_gap": "Figure 4", "rq2_weights_decomposition.csv": "Tables 4 and A2",
              "estimates.csv (WHY 2013-)": "Table 5", "estimates.csv (ROB)": "Tables 6, A3 and A5",
              "fig06_robustness": "Figure 5", "rq3_national.csv": "Figure 6", "fig07_rq3_2026": "Figure 6",
              "rq3_regional.csv": "Table 7", "rq3_decomposition.csv": "Figure 7", "fig08_rq3_decomposition": "Figure 7",
              "rq3_household_items.csv": "Table 8", "figA1_divisions": "Figure A1", "estimates.csv (APP)": "Tables A3–A4",
              "figA3_robustness_other": "Figure A2", "figA2_region_groups": "Figure A3", "var_comparison.csv": "Table A6",
              "figA5_var": "Figure A4", "figA4_regional": "Figure A5", "desc_annual.csv": "Table A7",
              "desc_episodes.csv": "Table A8", "desc_adf.csv": "Table A9", "desc_crosscorr.csv": "Table A10",
              "desc_regional.csv": "Table A11"}


PAGE_BREAK = "```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```"


def floats_to_end(text):
    """Journal submission layout: move every table and figure (marked <!--F--> ... <!--/F--> in the template)
    after the references, one per page, and leave '[Table k about here]' in the text."""
    import re
    blocks = re.findall(r"<!--F-->\n(.*?)\n<!--/F-->", text, flags=re.S)
    for b in blocks:
        m = re.search(r"(Table|Figure) (A?\d+)\.", b)
        text = text.replace(f"<!--F-->\n{b}\n<!--/F-->", f"*[{m.group(1)} {m.group(2)} about here]*", 1)
    return text + "\n\n" + "\n\n".join(f"{PAGE_BREAK}\n\n{b}" for b in blocks) + "\n"


def word_count(md_text):
    """Words of running text: no tables, figures, captions, notes, code or display equations."""
    import re
    body = re.sub(r"::: \{custom-style.*?\n:::", " ", md_text, flags=re.S)
    body = "\n".join(ln for ln in body.splitlines() if not ln.startswith(("|", "![", "Table:", "<!--")))
    body = body.split("---", 2)[-1] if body.startswith("---") else body
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    body = re.sub(r"\$\$.*?\$\$", " ", body, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9][\w'’.,%−-]*", body))


def render(template, out_name, n, t, extra, csl=None, spacing="double", to_end=False):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(PAPER), undefined=jinja2.StrictUndefined,
                             keep_trailing_newline=True, comment_start_string="<#--", comment_end_string="--#>")
    text = env.get_template(template).render(n=n, t=t, **extra)
    if to_end:
        text = floats_to_end(text)
    md_path = PAPER / f"{out_name}.md"
    md_path.write_text(text)
    docx = PAPER / f"{out_name}.docx"
    args = ["--citeproc", f"--bibliography={PAPER / 'references.bib'}", f"--resource-path={PAPER}:{ROOT}",
            "--metadata=link-citations:true", f"--reference-doc={STYLE / 'assets' / 'lian-article-reference.docx'}"]
    if csl:
        args.append(f"--csl={csl}")
    pypandoc.convert_file(str(md_path), "docx", outputfile=str(docx), extra_args=args)
    py = sys.executable
    subprocess.run([py, str(STYLE / "scripts" / "docx_style.py"), "finish", str(docx), "--spacing", spacing], check=True,
                   stdout=subprocess.DEVNULL)
    fix_bullets(docx)
    if shutil.which("soffice"):
        subprocess.run([py, str(STYLE / "scripts" / "render.py"), str(docx), "--outdir", str(PAPER)], check=True)
    print(f"wrote paper/{out_name}.md, .docx" + (", .pdf" if shutil.which("soffice") else ""))
    return text


def fix_bullets(docx):
    """Give pandoc's bullet lists a visible Times New Roman bullet (the symbol-font glyph is otherwise lost)."""
    import re
    import zipfile
    tmp = docx.with_suffix(".tmp")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/numbering.xml":
                def lvl(m):
                    b = m.group(0)
                    if 'w:numFmt w:val="bullet"' not in b:
                        return b
                    b = re.sub(r'<w:lvlText w:val="[^"]*"/>', '<w:lvlText w:val="•"/>', b)
                    return re.sub(r'<w:rFonts [^>]*/>', '<w:rFonts w:ascii="Times New Roman" '
                                  'w:hAnsi="Times New Roman" w:cs="Times New Roman"/>', b)
                data = re.sub(r'<w:lvl w:ilvl="(\d)".*?</w:lvl>', lvl, data.decode("utf-8"), flags=re.S).encode("utf-8")
            zout.writestr(item, data)
    tmp.replace(docx)


TITLE_PAGE = """---
title: "Who Pays for Oil Shocks? Fuel Price Pass-Through to the Inflation of Poor Households in the Philippines"
---

**Running head:** Who pays for oil shocks?

**Author:** {author}, {affiliation}, Philippines.

**Corresponding author:** {author}, {affiliation}, Philippines. E-mail: [to be added by the author].

**Word count:** about {words} words of text; about {total} words in the whole submission file, including the abstract, references, tables and figure captions (journal limit: 8,000 words plus 20%). The online appendix is a separate supplementary file.

**Acknowledgements:** [To be completed by the author.]

**Declaration of interest:** The author declares no competing interests. [To be confirmed by the author.]

**Funding:** [To be completed by the author.]

**Data availability:** All data are public. The replication package (raw data with a source log, cleaned data, Python and Stata 17 code, codebook) reproduces every number, table and figure: <https://github.com/liancataytayjk-coder/oil-shock-distribution>.
"""


def main():
    n, t = numbers_and_tables()
    t["review_matrix"], rm = review_matrix()
    n["n_studies"] = len(rm)
    t["sources_wp"], t["results_wp"] = data_appendix(WP_LABELS)
    t["sources_art"], t["results_art"] = data_appendix(ART_LABELS)
    (TAB / "paper_numbers.json").write_text(json.dumps(n, indent=1, ensure_ascii=False))
    meta = dict(author="Lian Cataytay", date="November 2026",
                affiliation="Graduate School of Applied Economics, University of Southeastern Philippines, Davao City")
    t["review15"] = review_matrix_article()
    render("working_paper_template.md", "working_paper", n, t, meta)
    # article for the Asian Economic Journal (decision D15): reading version, online appendix,
    # blinded submission with tables and figures at the end, and a separate title page
    csl = PAPER / "asian-economic-journal.csl"
    text = render("article_template.md", "article", n, t, dict(meta, blind=False), csl=csl)
    render("article_appendix_template.md", "article_online_appendix", n, t, dict(meta, blind=False), csl=csl)
    render("article_template.md", "article_submission", n, t, dict(meta, blind=True), csl=csl, to_end=True)
    main_text = text.split("# References", 1)[0]
    words = word_count(main_text)
    from docx import Document
    sub = Document(PAPER / "article_submission.docx")
    total = sum(len(p.text.split()) for p in sub.paragraphs) + sum(
        len(c.text.split()) for tb in sub.tables for row in tb.rows for c in row.cells)
    (PAPER / "_title_page.md").write_text(TITLE_PAGE.format(words=f"{words:,}", total=f"{total:,}", **meta))
    render("_title_page.md", "article_title_page", n, t, meta)
    (PAPER / "_title_page.md").unlink()
    print(len(n), "numbers;", f"article: about {words:,} words of text, {total:,} in the submission file")


if __name__ == "__main__":
    main()
