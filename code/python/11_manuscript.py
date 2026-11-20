"""The manuscript for the Asian Economic Journal (decision D16): the panel study.

Renders paper/manuscript_template.md three ways, with the journal's author-date style:
  paper/manuscript.*             reading version (author shown, tables and figures in the text)
  paper/manuscript_submission.*  blinded main file, tables and figures at the end, one per page
  paper/manuscript_title_page.*  separate title page with the word count
Numbers: output/tables/panel_numbers.json (10_panel_study.py) and paper_numbers.json (07_papers.py).
"""

import importlib.util
import json
import sys
from pathlib import Path

import pandas as pd

import data_io
from config import TAB

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
spec = importlib.util.spec_from_file_location("papers", Path(__file__).with_name("07_papers.py"))
P7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P7)
f, md, stars = P7.f, P7.md, P7.stars

META = dict(author="Lian Cataytay", date="November 2026",
            affiliation="Graduate School of Applied Economics, University of Southeastern Philippines, Davao City")


def cell(b, s, d=3):
    return f"{f(b, d)}{stars(b, s)} ({f(s, d)})"


def tables(pn):
    est = pd.read_csv(TAB / "panel_estimates.csv")
    g = lambda spec, y, h: est[(est.spec == spec) & (est.outcome == y) & (est.h == h)].iloc[0]  # noqa: E731
    t = {}
    t["responses"] = md(["Months after the shock (*h*)", "All households", "Bottom 30%", "Gap (all − bottom 30%)"],
                        [[h, cell(g("baseline", "d_cpi_all", h).beta, g("baseline", "d_cpi_all", h).se),
                          cell(g("baseline", "d_cpi_b30", h).beta, g("baseline", "d_cpi_b30", h).se),
                          cell(g("baseline", "d_ratio", h).beta, g("baseline", "d_ratio", h).se, 4)]
                         for h in (0, 1, 3, 6, 9, 12)], [2.2, 3, 3, 3.2])
    dec = pd.read_csv(TAB / "rq2_weights_decomposition.csv", dtype={"coicop": str}).set_index("coicop")
    big = ["01", "04", "07", "11"]
    names = {"01": "Food and non-alcoholic beverages", "04": "Housing, water, electricity, gas and other fuels",
             "07": "Transport", "11": "Restaurants and accommodation"}
    rows = [[names[c], f(dec.loc[c, "w_all"], 1), f(dec.loc[c, "w_b30"], 1), cell(dec.loc[c, "beta"], dec.loc[c, "se"]),
             f(dec.loc[c, "contrib_gap"], 4, sign=True)] for c in big]
    oth = dec.drop(big)
    rows.append(["Other nine divisions", f(oth.w_all.sum(), 1), f(oth.w_b30.sum(), 1), "", f(oth.contrib_gap.sum(), 4, sign=True)])
    gap12 = g("baseline", "d_ratio", 12).beta
    rows += [["(a) Gap implied by budget shares", "", "", "", f(dec.contrib_gap.sum(), 4, sign=True)],
             ["(b) Estimated gap, panel", "", "", "", f(gap12, 4)],
             ["(c) Within-category part, (b) − (a)", "", "", "", f(gap12 - dec.contrib_gap.sum(), 4)]]
    t["decomp"] = md(["CPI division", "Weight, all (%)", "Weight, bottom 30% (%)", "Response, 12 months",
                      "Contribution to the gap"], rows, [5, 1.6, 1.8, 2.6, 2.4])
    loo6 = est[est.spec.str.startswith("drop ") & (est.h == 6)]
    loo12 = est[est.spec.str.startswith("drop ") & (est.h == 12)]
    rob = [("Baseline", "baseline", "d_ratio"), ("Excluding 2008", "excl 2008", "d_ratio"),
           ("Shock dates 2001–2012", "2001-2012", "d_ratio"), ("Shock dates 2013–2026", "2013-2026", "d_ratio"),
           ("Shock: Dubai crude oil in pesos", "crude in pesos", "d_ratio"),
           ("Controls: exchange rate, policy rate, world food prices", "macro and food controls", "d_ratio"),
           ("Control: world food prices only", "food price control", "d_ratio")]
    rows = [[lab, cell(g(s, y, 6).beta, g(s, y, 6).se, 4), cell(g(s, y, 12).beta, g(s, y, 12).se, 4)] for lab, s, y in rob]
    rows.insert(1, ["One region left out (range over 17 regions)", f"{f(loo6.beta.min(), 4)} to {f(loo6.beta.max(), 4)}",
                    f"{f(loo12.beta.min(), 4)} to {f(loo12.beta.max(), 4)}"])
    t["robust"] = md(["Specification", "Gap, 6 months", "Gap, 12 months"], rows, [5.5, 3, 3])
    path = pd.read_csv(TAB / "panel_2026.csv")
    last = path[path.date == "2026-08-01"].set_index("series")
    lab = {"d_cpi_all": "All households", "d_cpi_b30": "Bottom 30%", "d_ratio": "Gap (all − bottom 30%)"}
    t["e2026"] = md(["Price index", "Predicted from fuel", "90% bootstrap band", "Actual", "Share predicted (%)"],
                    [[lab[s], f(r.fuel_driven, 2), f"[{f(r.lo, 2)}, {f(r.hi, 2)}]", f(r.actual, 2),
                      f(100 * r.fuel_driven / r.actual, 0)] for s, r in last.iterrows()], [3, 2.2, 2.6, 1.6, 2])
    regs = pd.read_csv(TAB / "panel_2026_regions.csv")
    t["regions"] = md(["Region", "Poverty 2018 (%)", "Fuel price change (%)", "Bottom 30%: predicted", "Bottom 30%: actual",
                       "Cost (PHP/month)"],
                      [[r.region_name + ("†" if r.new_geo_ext else ""), f(r.poverty_2018, 1), f(r.fuel_change, 1),
                        f(r.fuel_driven_b30, 2), f(r.actual_b30, 2), f"{r.cost_php_month:,.0f}"]
                       for _, r in regs.sort_values("cost_php_month", ascending=False).iterrows()],
                      [4.2, 1.6, 1.8, 2, 2, 1.8])
    ep = pd.read_csv(TAB / "desc_episodes.csv")
    t["episodes"] = md(["Episode", "Months", "Peak fuel price change, y/y (%)", "Inflation, all (%)",
                        "Inflation, bottom 30% (%)", "Gap, bottom 30% − all (pp)"],
                       [[f"{r.start} to {r.end}", r.months, f(r.peak_fuel_yoy, 1), f(r.mean_infl_all, 2),
                         f(r.mean_infl_b30, 2), f(r.mean_gap_b30_minus_all, 2, sign=True)] for _, r in ep.iterrows()],
                       [2.8, 1.2, 2.2, 1.8, 2, 2.2])
    return t


def extra_numbers(pn, n):
    nat = data_io.national().set_index("date")
    y = nat[["d_dubai_php", "d_ffpi", "d_fuel"]].rolling(12).sum().loc["2001-12-01":"2026-08-01"]
    x = {"corr_fuel_food": f(y.d_fuel.corr(y.d_ffpi), 2), "corr_crude_food": f(y.d_dubai_php.corr(y.d_ffpi), 2),
         "lpg_share": f(100 * 37 / float(pn["php_cost_b30"].replace(",", "")), 0)}
    ep = pd.read_csv(TAB / "desc_episodes.csv")
    x["n_episodes"], x["n_episodes_b30"] = len(ep), int((ep.mean_gap_b30_minus_all > 0).sum())
    return x


def main():
    pn = json.loads((TAB / "panel_numbers.json").read_text())
    n = json.loads((TAB / "paper_numbers.json").read_text())
    x = extra_numbers(pn, n)
    t = tables(pn)
    csl = PAPER / "asian-economic-journal.csl"
    ctx = dict(META, pn=pn, x=x)
    text = P7.render("manuscript_template.md", "manuscript", n, t, dict(ctx, blind=False), csl=csl)
    P7.render("manuscript_template.md", "manuscript_submission", n, t, dict(ctx, blind=True), csl=csl, to_end=True)
    words = P7.word_count(text.split("# References", 1)[0])
    from docx import Document
    sub = Document(PAPER / "manuscript_submission.docx")
    total = sum(len(p.text.split()) for p in sub.paragraphs) + sum(
        len(c.text.split()) for tb in sub.tables for row in tb.rows for c in row.cells)
    tp = P7.TITLE_PAGE.replace("Who Pays for Oil Shocks? Fuel Price Pass-Through to the Inflation of Poor Households in the Philippines",
                               "Who Pays for Oil Shocks? Evidence from Philippine Regional Price Indices")
    tp = tp.replace("The online appendix is a separate supplementary file.", "There is no supplementary appendix.")
    (PAPER / "_ms_title_page.md").write_text(tp.format(words=f"{words:,}", total=f"{total:,}", **META))
    P7.render("_ms_title_page.md", "manuscript_title_page", n, t, META)
    (PAPER / "_ms_title_page.md").unlink()
    print(f"manuscript: about {words:,} words of text; {total:,} in the submission file")


if __name__ == "__main__":
    sys.exit(main())
