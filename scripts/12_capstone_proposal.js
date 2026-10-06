// FA2 Capstone Proposal (max 10 pages): builds docs/capstone_proposal_FA2.docx with docx-js.
// Run: node scripts/12_capstone_proposal.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, AlignmentType,
  HeadingLevel, WidthType, BorderStyle, ShadingType, LevelFormat, Footer, PageNumber,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const FONT = "Times New Roman";
const W = 9360; // text width in DXA (Letter, 1-inch margins)

// ---------- helpers
// Inline markup: *italic*, **bold**, _{sub}, ^{sup}
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|_\{[^}]+\}|\^\{[^}]+\})/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, ...base }));
    else if (t.startsWith("*")) out.push(new TextRun({ text: t.slice(1, -1), italics: true, ...base }));
    else if (t.startsWith("_{")) out.push(new TextRun({ text: t.slice(2, -1), subScript: true, ...base }));
    else out.push(new TextRun({ text: t.slice(2, -1), superScript: true, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const p = (text, opts = {}) => new Paragraph({ children: runs(text), spacing: { after: 120 },
  alignment: AlignmentType.JUSTIFIED, ...opts });
const h1 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_1 });
const h2 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_2 });
const bullet = (text) => new Paragraph({ children: runs(text), numbering: { reference: "bullets", level: 0 },
  spacing: { after: 60 } });
const num = (text, ref = "numbers") => new Paragraph({ children: runs(text), numbering: { reference: ref, level: 0 },
  spacing: { after: 60 } });
const eq = (text, label) => new Paragraph({
  children: [...runs(text, { italics: false }), new TextRun({ text: `\t(${label})` })],
  tabStops: [{ type: "right", position: W }], alignment: AlignmentType.CENTER, spacing: { before: 80, after: 120 },
});
const caption = (text) => new Paragraph({ children: runs(text, { bold: true, size: 22 }), spacing: { before: 120, after: 80 } });
const note = (text) => new Paragraph({ children: runs(text, { size: 20 }), spacing: { before: 60, after: 160 } });

const border = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(widths, rows, header = true) {
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({
      tableHeader: header && i === 0,
      children: r.map((c, j) => new TableCell({
        borders, width: { size: widths[j], type: WidthType.DXA },
        margins: { top: 50, bottom: 50, left: 90, right: 90 },
        shading: header && i === 0 ? { fill: "E7E6E6", type: ShadingType.CLEAR, color: "auto" } : undefined,
        children: [new Paragraph({ children: runs(c, { size: 20, bold: header && i === 0 }) })],
      })),
    })),
  });
}

// ---------- content
const children = [];
const add = (...xs) => children.push(...xs);

add(
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: "FA2 · CAPSTONE PROPOSAL", bold: true, size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 120 },
    children: [new TextRun({ text: "Who Pays for Oil Shocks? Fuel Price Pass-Through to the Inflation of Poor Households across Philippine Regions",
      bold: true, size: 30 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: "Group members: [Name 1], [Name 2], [Name 3]", size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: "Graduate School of Applied Economics, University of Southeastern Philippines", size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
    children: [new TextRun({ text: "Submitted: Week 10, October 2026", size: 22 })] }),
);

add(h1("1. Motivation and Philippine Policy Relevance"));
add(
  p("The Philippines imports almost all of the oil it uses. When world oil prices rise, the *retail fuel price*—what households and firms pay at the pump—follows within weeks. The increase then spreads to jeepney and bus fares, to food, which must be grown, pumped and trucked, and to other goods. In 2026 the conflict in the Middle East produced one of the sharpest oil shocks in recent memory. Headline inflation, the yearly rise in the *consumer price index* (CPI), went from 2.4% in February to 4.1% in March and above 7% in April 2026. This is well above the 2–4% target of the Bangko Sentral ng Pilipinas (BSP), the central bank."),
  p("The government responded in several ways. Republic Act 12316 (March 2026) allowed the President to suspend fuel excise taxes when Dubai crude oil averages USD 80 per barrel or more. Excise taxes on liquefied petroleum gas (LPG) and kerosene were suspended. Public utility vehicle drivers received fuel subsidies, and the BSP raised its policy interest rate. Each measure carries an assumption about *who bears the cost* of a fuel price increase. That question has not been answered with Philippine data."),
  p("The best available evidence is a study of 122 countries by Kpodar and Liu (2022). It finds that fuel price increases are *progressive*: prices rise more for richer households, because richer households spend more on cars and fuel. If this holds in the Philippines, broad fuel tax cuts mainly help the better-off. There are reasons to doubt that it holds. Poor Filipino households spend more than half of their budget on food, ride public transport rather than drive, and cook with LPG, kerosene, wood or charcoal. Fuel prices reach these items indirectly. Regions also differ in poverty, diet and distance from fuel depots."),
  p("The Philippine Statistics Authority (PSA) publishes a monthly CPI for *all income households* and a separate CPI for the *bottom 30% income households*, for the whole country and for every region. With these two indices we can test directly whether fuel price increases hurt the poor more or less than the average household. The answer matters for four policy choices: (1) whether fuel excise relief under RA 12316 reaches the poor; (2) how large and how long emergency cash transfers should be; (3) whether fare and rice policy belong in the response to an oil shock; and (4) how the BSP should judge the spread of fuel prices to other prices."),
);

add(h1("2. Research Questions"));
add(
  p("**Main question.** When retail fuel prices rise, do poor Filipino households face larger price increases than the average household, and does the answer depend on where they live?"),
  p("The study has three objectives. **Objective 1** is descriptive. It documents how retail fuel prices, all-income inflation and bottom-30% inflation have moved from 2001 to 2026, nationally and by region: their averages, their ups and downs, the major fuel price episodes, and how closely the three series move together."),
  p("**Objective 2** estimates *pass-through*: how much consumer prices rise after a fuel price increase. It asks four research questions (RQ). RQ1 asks how much the all-income and bottom-30% price levels rise, and how quickly. RQ2 asks whether the bottom 30% face a larger or smaller rise than all households; that is, how the *inflation gap* responds. RQ3 asks which spending categories (food, transport, housing and utilities, and the rest) carry the increase, and whether differences in what each group buys explain the gap. RQ4 asks whether the gap is wider in four groups of regions: high-poverty regions, regions with a high food share, Mindanao, and island regions."),
  p("**Objective 3** draws policy lessons. It uses the estimates to explain the 2026 oil shock, to put a peso value on its cost to a poor family, and to judge how well fuel excise relief, fuel subsidies, fare regulation, monetary policy and cash transfers reach the poor."),
  p("**Hypotheses.** H1: pass-through is positive and lasts several months. H2 has two competing versions. H2a, the cross-country finding, says the effect is progressive (all-income prices rise more). H2b, the alternative, says it is regressive (bottom-30% prices rise more, through food and fares). H3: transport and food carry most of the pass-through. H4: the inflation gap is wider in poorer, more food-dependent and more remote regions."),
);

add(h1("3. Key Terms and Notation"));
add(
  p("This section defines every term used in the proposal, first in words and then as a formula. Subscripts show *when* and *where*: *t* is the month, *r* is the region, and *k* is a spending category. A superscript *g* shows the household group: *g* = *A* for all income households and *g* = *B* for the bottom 30%."),
  p("**Consumer price index (CPI).** The CPI tracks the cost of a fixed basket of goods and services compared with a base year (2018 = 100). The PSA computes it as a weighted average of item prices, where each weight is the share of the group's budget spent on that item in 2018:"),
  eq("P^{g}_{t} = 100 × Σ_{k} w^{g}_{k} (p_{k,t} / p_{k,2018}),  with  Σ_{k} w^{g}_{k} = 1", "1"),
  p("Here *p*_{k,t} is the price of item *k* and *w*^{g}_{k} is its *basket weight*. The PSA uses the same price survey for both groups; what differs is the weights. The bottom-30% weights come from the spending of households in the poorest 30% of the per-person income distribution in the 2018 Family Income and Expenditure Survey. The *all-income CPI* is *P*^{A}_{t} and the *bottom-30% CPI* is *P*^{B}_{t}. Both are official PSA indices; we do not construct them."),
  p("**Log change.** We measure changes in logarithms. For small changes, 100 times the change in the natural log of a series is close to its percentage change, and log changes over several months simply add up:"),
  eq("100·Δln X_{t} = 100 × (ln X_{t} − ln X_{t−1}) ≈ percentage change in X from month t−1 to month t", "2"),
  p("**Retail fuel price and fuel price shock.** The retail fuel price *F*_{t} is the PSA CPI sub-index 07.2.2, \"fuels and lubricants for personal transport\" (mainly gasoline and diesel at the pump). A *fuel price shock* is its monthly log change, *f*_{t} = 100·Δln *F*_{t}. A shock of *f*_{t} = 5 means pump prices rose about 5% in month *t*."),
  p("**Inflation.** *Monthly inflation* for group *g* is π^{g}_{t} = 100·Δln *P*^{g}_{t}. *Annual inflation*, the figure reported in the news, is 100 × (ln *P*^{g}_{t} − ln *P*^{g}_{t−12})."),
  p("**Pass-through.** The pass-through at horizon *h* is how much monthly inflation in month *t* + *h* changes when fuel prices rise by 1% in month *t*, holding everything else constant. *Cumulative pass-through* adds these up and gives the effect on the price level after *h* months:"),
  eq("β_{h} = ∂π_{t+h} / ∂f_{t},      B_{h} = β_{0} + β_{1} + … + β_{h}", "3"),
  p("For example, *B*_{12} = 0.05 would mean that a 10% fuel price rise makes the CPI 0.5% higher a year later than it would otherwise be."),
  p("**Inflation gap.** The inflation gap compares the two price levels. Its monthly change equals the difference between the two inflation rates:"),
  eq("D_{t} = 100 × ln(P^{A}_{t} / P^{B}_{t}),      ΔD_{t} = π^{A}_{t} − π^{B}_{t}", "4"),
  p("If *D* falls, prices rose faster for the bottom 30%: the shock is *regressive*. If *D* rises, prices rose faster for the average household: the shock is *progressive*. The pass-through to the gap equals *B*^{A}_{h} − *B*^{B}_{h}, so a negative value supports H2b and a positive value supports H2a. The gap is our construction from the two PSA indices."),
  p("**Region groups.** For RQ4, a dummy variable *G*_{r} equals 1 if region *r* belongs to a group and 0 otherwise. The groups are our own, defined in advance from PSA data: *high poverty* (2018 poverty incidence above the median of the 17 regions), *high food share* (food weight in the region's 2018 all-income basket above the median), *Mindanao* (Regions IX, X, XI, XII, XIII and BARMM), and *island regions* (MIMAROPA, VI, VII and VIII)."),
);

add(h1("4. Theoretical Framework"));
add(
  p("The study rests on two bodies of theory. A general theory of prices explains *how much* a cost increase raises each price and each group's cost of living. An oil-specific theory explains *through which channels* and *how fast* an oil price increase travels."),
  h2("4.1 General theory: cost-push pricing and the cost of living"),
  p("**Cost-push pricing (the input–output price model).** In the price model of Leontief (Miller & Blair, 2009), the price of each good covers the cost of the inputs used to make it plus wages and profits. Fuel is an input to almost everything: tractors and irrigation pumps for rice, trucks that move goods, boats between islands, and the jeepney itself. If margins and other costs stay the same, a rise in the fuel price raises the price of good *k* in proportion to the fuel it contains, both directly and through its other inputs:"),
  eq("π_{k,t} ≈ φ_{k} × f_{t}", "5"),
  p("where φ_{k} is the total fuel cost share of good *k*. For pump fuel φ_{k} is close to 1; for a jeepney fare it is large; for rice it is smaller but not zero."),
  p("**Cost-of-living index.** Equation (1) implies that a group's inflation is the weighted average of item inflation, using that group's weights: π^{g}_{t} ≈ Σ_{k} *w*^{g}_{k} π_{k,t}. Combining this with equation (5) gives the central prediction of the framework:"),
  eq("π^{g}_{t} ≈ Φ^{g} × f_{t},   where   Φ^{g} = Σ_{k} w^{g}_{k} φ_{k}", "6"),
  p("Pass-through for a group equals the *fuel intensity of its basket*, Φ^{g}. The shock is progressive if the average basket is more fuel-intensive (Φ^{A} > Φ^{B}), for example because it holds more gasoline. It is regressive if the poor basket is more fuel-intensive, for example because it holds more food and fares. Which effect dominates is an empirical question, and it may differ by region because baskets differ by region."),
  p("**Where the gap comes from.** The difference in inflation between the two groups splits into two parts:"),
  eq("π^{A}_{t} − π^{B}_{t} = Σ_{k} (w^{A}_{k} − w^{B}_{k}) π^{A}_{k,t} + Σ_{k} w^{B}_{k} (π^{A}_{k,t} − π^{B}_{k,t})", "7"),
  p("The first part is a *weights effect*: the groups divide their budgets differently across categories, such as food versus transport. The second is a *within-category effect*: inside a category the groups buy different items (more rice and less meat, for example), so even the group's \"food\" index can rise at a different rate. RQ3 measures both parts."),
  p("**Welfare cost.** Deaton (1989) shows that, for a small price change, the loss in a household's real income, as a share of its spending, is approximately its budget-share-weighted price change: Σ_{k} *w*_{k} π_{k}. The rise in the bottom-30% CPI is therefore the extra spending a poor family needs to keep buying the same basket. Multiplied by the poverty line, it gives the peso cost of a fuel shock to a poor family (Objective 3)."),
  h2("4.2 Oil-specific theory: how oil price shocks reach consumer prices"),
  p("Kilian (2008) describes two routes from an energy price increase to consumer prices. The *direct* route is the energy that households buy themselves: gasoline, diesel, LPG and kerosene. Its effect is immediate and proportional to the energy share of the budget. The *indirect* route works through production costs, as in equation (5); it takes months, as firms pass on higher costs for transport, food and services. Blanchard and Galí (2010) add a third, *second-round* route: if workers win higher wages and people come to expect higher inflation, prices keep rising after the oil shock has passed. They show that this route has weakened since the 1970s, because monetary policy is more credible, wages are more flexible and economies use less oil per unit of output."),
  p("Studies of fuel subsidies in developing countries give the distributional side. Arze del Granado, Coady and Gillingham (2012) find that higher fuel prices cut real incomes by a similar percentage across income groups, and that more than half of that loss comes through the indirect route. In peso terms, the richest fifth of households receives about six times as much from fuel subsidies as the poorest fifth. Kpodar and Liu (2022) estimate the direct and indirect routes together with monthly price data and find a progressive effect on average across countries. This study asks whether that holds in the Philippines, where the indirect route through food and fares may matter more for the poor."),
  h2("4.3 Conceptual framework"),
  p("Figure 1 puts the pieces together. A rise in world oil prices, converted at the peso–dollar exchange rate and combined with taxes and margins, raises the retail fuel price. The increase reaches consumer prices through the direct, indirect and second-round routes. How much each group's CPI rises depends on its basket weights and on the price changes within each category (equations 6 and 7), and these may differ across regions. The difference between the two CPIs is the inflation gap. Policy can act on the retail fuel price (excise relief, subsidies), on the indirect route (fare regulation), on the second round (monetary policy), or on household income (cash transfers)."),
);
add(new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({
  type: "png", data: fs.readFileSync(path.join(ROOT, "output/figures/figw0_framework.png")),
  transformation: { width: 340, height: 301 } })] }));
add(note("**Figure 1.** Conceptual framework. Solid arrows show how a fuel price shock is transmitted; dashed arrows show where policy can act."));

add(h1("5. Data Sources and Empirical Strategy"));
add(h2("5.1 Data"));
add(p("All data are public and monthly, and can be downloaded from official websites (Table 1). The main sample runs from January 2001 to the latest available month, for the Philippines and its 17 regions. Regional CPIs follow the 17-region coding used in PSA's 2018-based back series; the 2024 creation of the Negros Island Region is handled by linking the new series to the old regions and flagging the affected months."));
add(caption("Table 1. Variables and data sources"));
add(table([2900, 1000, 2300, 3160], [
  ["Variable", "Symbol", "Source", "Coverage and use"],
  ["All-income CPI and its 13 spending categories (2018 = 100)", "P^{A}", "PSA OpenSTAT", "1994–2026, national and 17 regions; outcome"],
  ["Bottom-30% CPI and its categories (2018 = 100)", "P^{B}", "PSA OpenSTAT", "2000–2026 (categories from 2012), national and 17 regions; outcome"],
  ["Retail fuel price: CPI sub-index 07.2.2", "F", "PSA OpenSTAT", "1994–2026, national and 17 regions; fuel price shock"],
  ["Pump price, Manila (RON 91)", "—", "World Bank Global Fuel Prices Database", "2017–2025; check of F"],
  ["Dubai crude oil price in pesos", "—", "World Bank Pink Sheet; BSP", "1960–2026; alternative shock"],
  ["Peso–dollar rate; policy rate; world food prices", "—", "BSP; BIS; FAO", "Monthly; control variables"],
  ["Poverty incidence; basket weights", "w^{g}_{k}", "PSA", "2018–2023; region groups, decomposition"],
  ["EU consumer and pump prices", "—", "Eurostat; EC Weekly Oil Bulletin", "2000–2019; validation"],
]));
add(note("*Note:* The reference study's own retail fuel price database is not public. The PSA fuel sub-index replaces it and will be checked against the World Bank pump price before use."));

add(h2("5.2 Empirical model"));
add(p("We will use *local projections* (Jordà, 2005), following the specification of Kpodar and Liu (2022). A local projection estimates the effect of a shock at each future month *h* with its own regression, instead of deriving all future effects from one model. Each regression is estimated by ordinary least squares. For *h* = 0, 1, …, 12:"));
add(eq("π_{t+h} = α_{h} + β_{h} f_{t} + Σ_{q=1}^{12} γ_{q} π_{t−q} + Σ_{q=1}^{12} λ_{q} f_{t−q} + Σ_{l=1}^{h−1} ρ_{l} f_{t+l} + δ_{h} t + ε_{t+h}", "8"));
add(
  p("The outcome π_{t+h} is monthly inflation *h* months after the shock, and β_{h} is the pass-through of equation (3). The twelve past values of inflation and of fuel shocks (the *lags*) account for earlier movements and for regular seasonal patterns, such as higher prices every December. The fuel shocks between month *t* and month *t* + *h* (the *leads*) are included so that β_{h} is not confused with the effect of later shocks; this is the Teulings and Zubanov (2014) correction. The term δ_{h}*t* is a linear time trend, and ε_{t+h} is the error. Adding up β_{0} to β_{h} gives the cumulative pass-through *B*_{h}."),
  p("The four research questions use the same equation with different outcomes. For RQ1 the outcome is national inflation for each group, π^{A} and π^{B}. For RQ2 it is the change in the inflation gap, ΔD. For RQ3 it is all-income inflation in each of the 13 spending categories; these estimates, multiplied by the difference in basket weights, measure the weights effect in equation (7). For RQ4 we stack the 17 regions into a *panel* and use each region's own fuel price. A *region fixed effect* *u*_{r} lets each region have its own average gap, and an *interaction term* lets the effect differ for a group of regions:"),
);
add(eq("ΔD_{r,t+h} = u_{r} + β_{h} f_{r,t} + θ_{h} (f_{r,t} × G_{r}) + (lags, leads, trend) + ε_{r,t+h}", "9"));
add(
  p("Here θ_{h} is the extra pass-through to the gap in that group, for example Mindanao, compared with the other regions. A negative θ_{h} means the shock is more regressive there."),
  p("*Standard errors* measure how uncertain each estimate is. Monthly data are correlated over time, and regions are hit by the same shocks, so ordinary standard errors would be too small. We will use Newey–West standard errors for national series, which allow for correlation over time (Newey & West, 1987), and Driscoll–Kraay standard errors for the regional panel, which also allow for correlation across regions (Driscoll & Kraay, 1998). We report 90% confidence bands, as the reference study does."),
  h2("5.3 Validation, robustness and policy analysis"),
  p("**Validation.** Before any Philippine estimate, our code must reproduce the published result of the reference study for the European Union: a pass-through of about 0.055 from pump prices and about 0.015 from crude oil. The pass/fail criteria will be written down before the test is run. The estimator will also be tested on simulated data for which the true answer is known."),
  p("**Robustness.** We will check whether the main results survive changes to the design. The checks are: crude oil prices instead of retail fuel prices (no Philippine region can move world crude prices, so this removes doubts that pump prices respond to local demand); controls for the exchange rate, the policy rate and world food prices; 6 and 18 lags instead of 12; samples without 2020 and without 2026; and dropping one region at a time."),
  p("**Policy analysis (Objective 3).** We will estimate the model on data up to December 2025 only, apply it to the actual 2026 fuel price path, and compare the predicted price increase with what happened. The predicted rise in the bottom-30% CPI, multiplied by the official monthly poverty line for a family of five (as in section 4.1), gives the peso cost of the 2026 fuel shock to a poor family in each region. We will compare that cost with the value of the 2026 relief measures."),
);

add(h1("6. Workplan and Timeline"));
add(
  p("The work runs from Week 11 to Week 18 and follows the three objectives in order, so that each step builds on a checked result from the step before."),
  p("In **Week 11** we will download every data series, record its source, date and base year in a data log, and build the national and regional datasets. We will also compare the PSA fuel sub-index with the World Bank pump price to confirm that it tracks pump prices. The output is a clean dataset with its source log."),
  p("In **Week 12** we will validate the estimator before using it on Philippine data. We will first check that it recovers a known answer from simulated data, and then that it reproduces the reference study's European results within the pass/fail ranges set in advance. The output is a short validation note. If the validation fails, we will correct the code before going further."),
  p("In **Week 13** we will complete Objective 1: summary statistics by sub-period, annual inflation for both groups, the main fuel price episodes, correlations between fuel prices and inflation at different delays, and unit-root tests to confirm that monthly changes are stable enough for the regressions. The output is the descriptive tables and figures."),
  p("**Weeks 14 and 15** are for Objective 2. In Week 14 we will estimate the national models for RQ1 to RQ3. In Week 15 we will estimate the regional panel for RQ4 and run the robustness checks. The output is the pass-through results with their confidence bands."),
  p("In **Week 16** we will complete Objective 3: the 2026 out-of-sample test, the peso cost for a poor family by region, and the assessment of the policy instruments."),
  p("In **Week 17** we will write the full paper and submit it to our adviser for review. In **Week 18** we will revise the paper and prepare the presentation and the replication files."),
  p("All steps will be scripted in Python, so that one command reproduces every number in the paper. Each modelling choice will be recorded in a decision log, with its reason, before the results are seen."),
  p("We foresee four risks. First, pump prices may partly respond to conditions inside the Philippines rather than to world oil prices; we will re-estimate the model with world crude oil prices, which no Philippine region can influence. Second, the CPI series are joined at points where PSA changed the base year; we will use PSA's own 2018-based back series and test the results with dummy variables for the months where the series are joined. Third, regional boundaries changed when the Negros Island Region was created in 2024; we will use the older 17-region coding, which matches the back series, and test the results without the affected months. Fourth, only a few months of 2026 data are available; we will therefore treat the 2026 analysis as a test of the historical model rather than as the main estimate."),
);

add(h1("References"));
for (const r of [
  "Arze del Granado, F. J., Coady, D., & Gillingham, R. (2012). The unequal benefits of fuel subsidies: A review of evidence for developing countries. *World Development*, 40(11), 2234–2248.",
  "Blanchard, O. J., & Galí, J. (2010). The macroeconomic effects of oil price shocks: Why are the 2000s so different from the 1970s? In J. Galí & M. Gertler (Eds.), *International dimensions of monetary policy* (pp. 373–421). University of Chicago Press.",
  "Deaton, A. (1989). Rice prices and income distribution in Thailand: A non-parametric analysis. *Economic Journal*, 99(395), 1–37.",
  "Driscoll, J. C., & Kraay, A. C. (1998). Consistent covariance matrix estimation with spatially dependent panel data. *Review of Economics and Statistics*, 80(4), 549–560.",
  "Jordà, Ò. (2005). Estimation and inference of impulse responses by local projections. *American Economic Review*, 95(1), 161–182.",
  "Kilian, L. (2008). The economic effects of energy price shocks. *Journal of Economic Literature*, 46(4), 871–909.",
  "Kpodar, K., & Liu, B. (2022). The distributional implications of the impact of fuel price increases on inflation. *Energy Economics*, 108, 105909.",
  "Miller, R. E., & Blair, P. D. (2009). *Input–output analysis: Foundations and extensions* (2nd ed.). Cambridge University Press.",
  "Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.",
  "Philippine Statistics Authority. (2026). OpenSTAT: Consumer Price Index for All Income Households and for the Bottom 30% Income Households (2018 = 100).",
  "Republic of the Philippines. (2026). Republic Act No. 12316: An Act authorizing the President to suspend or reduce excise tax on petroleum products.",
  "Teulings, C. N., & Zubanov, N. (2014). Is economic recovery a myth? Robust estimation of impulse responses. *Journal of Applied Econometrics*, 29(3), 497–514.",
]) add(new Paragraph({ children: runs(r, { size: 22 }), indent: { left: 720, hanging: 720 }, spacing: { after: 80 } }));

// ---------- document
const doc = new Document({
  creator: "Capstone group",
  title: "FA2 Capstone Proposal: Who Pays for Oil Shocks?",
  styles: {
    default: { document: { run: { font: FONT, size: 24 }, paragraph: { spacing: { line: 252 } } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 26, bold: true }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, bold: true, italics: true }, paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 20 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(ROOT, "docs", "capstone_proposal_FA2.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out);
});
