"""SA3 presentation deck in the house style (black and white, Times New Roman, 16:9).

Every number comes from output/tables/paper_numbers.json and every figure from
output/figures/, so the deck changes when the analysis changes. Writes
docs/presentation_SA3.pptx (the PDF is made by scripts/14_submissions.py).
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "lian_style" / "scripts"))
from lian_deck import Deck  # noqa: E402

FIG = ROOT / "output" / "figures"
n = json.loads((ROOT / "output" / "tables" / "paper_numbers.json").read_text())


def pos(x):
    """Drop the minus sign for wording such as '0.021 pp more'."""
    return str(x).replace("−", "")


d = Deck(short_title="Who Pays for Oil Shocks? · SA3 Capstone")

d.title_slide(
    "Who Pays for Oil Shocks? Fuel Price Pass-Through to the Inflation of Poor Households across Philippine Regions",
    ["Capstone Paper Presentation (SA3)",
     "Graduate School of Applied Economics, University of Southeastern Philippines"],
    byline="Prepared by: **Lian Cataytay**",
    date="November 2026",
)

# 1. Motivation
s = d.slide("1. Why this question matters now",
            "The 2026 oil shock pushed inflation above target, and the poor's inflation even higher.")
left, right = d.columns(2)
d.text(s, left, [
    f"**Pump prices:** the fuel index was {n['yoy_fuel_apr']}% above a year earlier in April 2026",
    f"**Headline inflation:** {n['yoy_all_feb']}% in February → {n['yoy_all_apr']}% in April → {n['yoy_all_aug']}% in August",
    f"**Bottom 30% of households:** {n['yoy_b30_apr']}% in April and {n['yoy_b30_aug']}% in August",
    "**BSP target:** 2–4%",
], heading="The shock")
d.panel(s, right, [
    "**RA 12316:** lets the President suspend fuel excise taxes when Dubai crude ≥ USD 80/barrel",
    "**Excise suspended** on LPG and kerosene, not on gasoline and diesel",
    "**Fuel subsidies** for public utility vehicle drivers",
    f"**BSP** raised its policy rate {n['n_hikes_word']} times, to {n['policy_aug']}%",
], heading="The policy response")
d.source(s, "Sources: PSA CPI (2018 = 100); RA 12316; BSP. Inflation is year on year.")

# 2. Gap and question
s = d.slide("2. Research gap and questions",
            "Cross-country evidence says fuel shocks hurt the rich more; is that true in the Philippines?")
top, bottom = d.split(d.body(), 1.0)
left, right = d.columns(2, top)
d.text(s, left, [
    "**Kpodar and Liu (2022), 122 countries:** fuel price shocks are *progressive*: prices rise more for richer households",
    "**But Filipino poor households** spend over half their budget on food and ride public transport",
    "**PSA publishes a bottom-30% CPI** by region, so we can test this directly",
], heading="The gap")
d.text(s, right, [
    "**Objective 1 (descriptive):** trends in fuel prices and both inflation rates, 2001–2026",
    "**Objective 2 (estimation):** pass-through (RQ1), the inflation gap (RQ2), categories (RQ3), regions (RQ4)",
    "**Objective 3 (policy):** the 2026 shock, its peso cost and the policy response",
], heading="Three objectives")
d.callout(s, bottom, "Research question:",
          "When fuel prices rise, do poor Filipino households face larger price increases than the average household, "
          "and does it depend on where they live?")

# 3. Key terms
s = d.slide("3. Key terms and notation", "Each term keeps the same meaning on every slide.")
d.table(s, d.body(), [
    ["Term", "Meaning and formula"],
    ["Fuel price shock", "Monthly change in PSA's retail fuel index 07.2.2: f_{t} = 100·Δln F_{t}"],
    ["Inflation (group g)", "π^{g}_{t} = 100·Δln P^{g}_{t}; A = all income households, B = bottom 30%"],
    ["Pass-through", "β_{h}: change in inflation h months later per 1% fuel rise; cumulative B_{h} = β_{0} + … + β_{h}"],
    ["Inflation gap", "D_{t} = 100·ln(P^{A}_{t} / P^{B}_{t}); a fall means prices rose more for the poor (*regressive*)"],
    ["Basket weight", "w^{g}_{k}: share of group g's 2018 budget spent on category k"],
    ["Region groups", "Our own dummies G_{r}: high poverty, high food share, Mindanao, island regions"],
], col_widths=[1.2, 4], first_col_bold=True, size=16)
d.source(s, "Both CPIs are official PSA indices; the gap and the region groups are our constructions.")

# 4. Theory
s = d.slide("4. Theoretical framework",
            "A group's pass-through equals the fuel content of what it buys.")
left, right = d.columns(2, widths=[1, 1.15])
d.image(s, left, FIG / "figw0_framework.png", caption="Solid: transmission; dashed: where policy acts.")
d.text(s, right, [
    "**Cost-push pricing** (Leontief input–output): each good's price rises with its fuel cost share, π_{k} ≈ φ_{k} f",
    "**Cost-of-living index:** π^{g} ≈ Σ_{k} w^{g}_{k} φ_{k} f, so pass-through = fuel intensity of the basket",
    "**Gap = weights effect + within-category effect** (the poor buy different items in each category)",
    "**Oil-specific channels:** direct, indirect and second-round (Kilian 2008; Blanchard and Galí 2010)",
    "**Welfare cost** ≈ budget-share-weighted price rise (Deaton 1989)",
])

# 5. Data and method
s = d.slide("5. Data and empirical strategy",
            "Local projections on monthly PSA data, 2001–August 2026, national and 17 regions.")
top, bottom = d.split(d.body(), 1.25)
d.table(s, top, [
    ["Variable", "Source", "Coverage"],
    ["All-income CPI and 13 categories", "PSA OpenSTAT", "1994–Aug 2026, national and 17 regions"],
    ["Bottom-30% CPI", "PSA OpenSTAT", "2000–Aug 2026, national and 17 regions"],
    ["Retail fuel index 07.2.2 (shock)", "PSA OpenSTAT", "1994–Aug 2026, national and 17 regions"],
    ["Crude oil, pump price, FX, policy rate, food", "World Bank, BSP, BIS, FAO", "Robustness and controls"],
], col_widths=[2.4, 1.8, 2.6], size=15)
d.text(s, bottom, [
    "**Model** (Jordà 2005; Kpodar and Liu 2022), for each h = 0…12: π_{t+h} = α_{h} + β_{h} f_{t} + 12 lags + leads + trend + ε",
    "**Errors:** Newey–West (national), region fixed effects and Driscoll–Kraay (panel); 90% bands",
], bullets=False, size=16)

# 6. Validation
s = d.slide("6. Validation before any Philippine estimate",
            "Our code reproduces the reference study's European results under rules set in advance.")
left, right = d.columns(2, widths=[1.3, 1])
d.image(s, left, FIG / "figr_eu_validation.png")
d.table(s, right, [
    ["Shock (EU, impact)", "Ours", "Paper"],
    ["Pump price after tax", n["rep_after"], "0.055"],
    ["Pump price before tax", n["rep_before"], "0.020"],
    ["Brent crude in euro", n["rep_brent"], "0.015"],
], col_widths=[2, 1, 1], align=["l", "r", "r"], size=16)
d.source(s, "Response of monthly HICP inflation to a 1% fuel price rise, 2005–Jun 2019. A simulation test also passed.")

# 7. Objective 1
s = d.slide("7. Objective 1: the poor's inflation has been higher",
            f"Bottom-30% prices rose {pos(n['d_cum_gap_ph'])} log points more than all-income prices since 2001.")
left, right = d.columns(2, widths=[1.5, 1])
d.image(s, left, FIG / "figd1_trends.png")
d.text(s, right, [
    f"**Average inflation, 2001–2026:** {n['d_b30_mean_ann']}% (bottom 30%) vs {n['d_all_mean_ann']}% (all)",
    f"**Higher for the poor** in {n['d_years_b30_higher']} of {n['d_years_total']} years",
    f"**Fuel-shock episodes:** poor's inflation higher in {n['d_episodes_b30_higher']} of {n['d_n_episodes']}",
    f"**Peak gap in 2008** (rice crisis): {n['d_2008_b30']}% vs {n['d_2008_all']}%",
])
d.source(s, "Source: PSA CPI; authors' calculations. Year-on-year rates.")

# 8. RQ1
s = d.slide("8. RQ1: fuel prices pass through quickly and keep building",
            f"A 10% fuel price rise raises the price level by about {n['rq1_all_c12_10pct']}% after a year.")
left, right = d.columns(2, widths=[1.3, 1])
d.image(s, left, FIG / "fig1_rq1_passthrough.png")
d.text(s, right, [
    f"**Impact:** {n['rq1_all_c0']} pp per 1% fuel rise (s.e. {n['rq1_all_c0_se']})",
    f"**After 12 months:** {n['rq1_all_c12']} (all) and {n['rq1_b30_c12']} (bottom 30%)",
    f"**Larger than the cross-country** developing-economy impact ({n['kl_dev_b0']})",
    f"**Crude oil understates it:** only about {n['crude_share']}% of the retail estimate",
])
d.source(s, "Cumulative responses, 90% bands. National, Newey–West standard errors.")

# 9. RQ2 and RQ4 pooled
s = d.slide("9. RQ2: the poor pay more, not less",
            "The gap falls after a fuel shock: the effect is regressive, the opposite of the cross-country finding.")
top, bottom = d.split(d.body(), 1.0)
d.image(s, top, FIG / "fig2_rq2_rq4_ratio.png")
d.text(s, bottom, [
    f"**National:** {n['rq2_c6']} after 6 months (s.e. {n['rq2_c6_se']}), significant at h = {n['rq2_sig_h']}  ·  "
    f"**17-region panel:** {n['rq4_c6']} (s.e. {n['rq4_c6_se']}), significant",
    f"**Meaning:** a 10% fuel rise leaves the poor's price level about {n['gap6_10pct']}% higher than the average household's",
], bullets=False, size=16)

# 10. RQ3
s = d.slide("10. RQ3: which prices carry the shock?",
            "Transport, utilities and food carry the shock; budget shares alone would predict the opposite gap.")
left, right = d.columns(2, widths=[1.3, 1])
d.image(s, left, FIG / "fig3_rq3_components.png")
d.text(s, right, [
    f"**Largest responses:** transport {n['rq3_transport']}, housing and utilities {n['rq3_housing']}, food {n['rq3_food']}",
    f"**{n['rq3_nsig']} of 13** categories respond significantly",
    f"**Weights alone** predict a *progressive* gap ({n['rq3_gap_pred']})",
    f"**Within categories, responses differ:** utilities {n['rq3b_c04_b30']} (poor) vs {n['rq3b_c04_all']}; "
    f"transport {n['rq3b_c07_b30']} vs {n['rq3b_c07_all']}",
])
d.source(s, "Cumulative response after 12 months, all-income CPI divisions, 90% CI. Within-category comparison is exploratory (2013–2026).")

# 11. RQ4
s = d.slide("11. RQ4: do regions differ?",
            "The gap tends to be wider in Mindanao and island regions, but the evidence is weak.")
left, right = d.columns(2, widths=[1.3, 1])
d.image(s, left, FIG / "fig4_rq4_groups.png")
d.text(s, right, [
    f"**Mindanao:** {n['rq4_mindanao']} extra (s.e. {n['rq4_mindanao_se']})",
    f"**Island regions:** {n['rq4_island']} (s.e. {n['rq4_island_se']})",
    f"**High poverty:** {n['rq4_high_poverty']} (s.e. {n['rq4_high_poverty_se']})",
    f"**High food share:** {n['rq4_high_food']} (s.e. {n['rq4_high_food_se']})",
    "**None survives** a correction for testing four groups",
])
d.source(s, "Additional cumulative effect on the gap after 12 months; 17-region panel, Driscoll–Kraay errors.")

# 12. Robustness
s = d.slide("12. How robust is the regressive result?",
            "The sign holds in almost every check, but the effect is concentrated in 2001–2012.")
left, right = d.columns(2, widths=[1.3, 1])
d.image(s, left, FIG / "fig5_robustness.png")
d.text(s, right, [
    f"**Leave one region out:** {n['loo_min']} to {n['loo_max']}",
    f"**2001–2012:** {n['split_p1']}; **2013–2026:** {n['split_p2']}",
    f"**Near zero** with macro controls ({n['rob_macro']}), the gasoline index and the World Bank pump price",
    "**Read with care:** regressive in sign, strongest in the 2000s",
])
d.source(s, "Cumulative gap response after 6 months, 90% CI. Open squares: supplementary analyses.")

# 13. Objective 3: out of sample
s = d.slide("13. Objective 3: what explains the 2026 surge?",
            f"A model estimated only on data to 2025 explains about half of the 2026 price rise.")
top, bottom = d.split(d.body(), 0.9)
d.image(s, top, FIG / "fig6_2026_out_of_sample.png")
d.text(s, bottom, [
    f"**Dec 2025–Aug 2026:** fuel-driven {n['e1_all_fd']} of {n['e1_all_act']} log points (all), "
    f"{n['e1_b30_fd']} of {n['e1_b30_act']} (bottom 30%)  ·  **Prices did not fall** when fuel eased in May–June",
], bullets=False, size=16)

# 14. Peso cost and decomposition
s = d.slide("14. The cost to poor families, and why it was higher",
            f"Fuel added about PHP {n['e3_ph_cost']} a month to a poverty-line family's costs; rice drove the extra gap.")
left, right = d.columns(2, widths=[1, 1.2])
d.panel(s, left, [
    f"**National:** PHP {n['e3_ph_cost']} a month for a family of five at the poverty line",
    f"**By region:** PHP {n['e3_min']} ({n['e3_min_reg']}) to {n['e3_max']} ({n['e3_max_reg']})",
    f"**All price increases:** about PHP {n['e3_ph_actual_cost']} a month",
    f"**Highest actual rise:** {n['e2_top_names']}",
], heading="Peso cost by August 2026")
d.image(s, right, FIG / "fig7_2026_gap_decomposition.png",
        caption=f"Contributions to the {n['e5_total_gap']} pp gap: cereals {n['e5_cereals_gap']}.")

# 15. Policy
s = d.slide("15. Policy implications", "Transfers sized to the poor's own price index are better targeted than fuel tax cuts.")
d.table(s, d.body(), [
    ["Instrument (2026)", "What the evidence says"],
    ["Excise relief, gasoline and diesel", f"Mainly helps the better-off: motor fuel is {n['w_fuel_all']}% of the average basket, {n['w_fuel_b30']}% of the poor's"],
    ["Excise relief, LPG and kerosene", "Distribution-neutral for LPG (same weight and response); kerosene matters more for the poor but is small"],
    ["Fuel subsidies for drivers", "Protect poor commuters only if tied to fare restraint"],
    ["Policy rate increases", "Appropriate: pass-through builds for at least a year"],
    ["Targeted cash transfers", f"Best targeted; size with the bottom-30% CPI (PHP {n['e3_ph_cost']}–{n['e3_ph_actual_cost']} a month)"],
    ["Rice price and supply measures", f"Needed: cereals explain {n['e5_cereals_gap']} pp of the 2026 gap"],
], col_widths=[1.6, 3.6], first_col_bold=True, size=15)

# 16. Limitations and data appendix
s = d.slide("16. Limitations and reproducibility",
            "The results are descriptive of transmission, not a clean causal test, and every number can be rebuilt.")
left, right = d.columns(2)
d.text(s, left, [
    "**Retail prices may respond** to local conditions; an identified oil supply shock is the next step",
    "**Bottom 30% vs all**, not poorest vs richest",
    "**2026 analysis** covers eight months; rice and trade policy cannot be separated from fuel",
], heading="Limitations")
d.panel(s, right, [
    "**All data public:** PSA OpenSTAT, World Bank, BSP, BIS, FAO, Eurostat",
    "**Data appendix** in the paper links every figure and table to its source and script",
    "**One command** (./run_all.sh) rebuilds every number",
    "**Pre-registered** estimation plan and replication test",
], heading="Data and reproducibility")

d.takeaway("In the Philippines, the poor pay more when fuel prices rise.", [
    f"**Pass-through is fast and lasting:** a 10% fuel rise lifts prices about {n['rq1_all_c12_10pct']}% within a year",
    "**Regressive, not progressive:** the poor's prices rise more, through food, utilities and fares",
    "**2026:** fuel explains about half of the surge; rice drove the poor's extra inflation",
    "**Policy:** protect the poor with transfers sized to their price index, not broad fuel tax cuts",
])
d.closing("Thank you", "Questions and discussion")
d.save(ROOT / "docs" / "presentation_SA3.pptx")
