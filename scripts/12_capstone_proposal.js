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
  p("The Philippines imports almost all of the petroleum it uses. When world oil prices rise, the *retail fuel price*—what households and firms pay at the pump—follows quickly, and the increase spreads to transport fares, food and other goods. In 2026 the conflict in the Middle East produced one of the sharpest oil shocks in recent memory. Headline inflation rose from 2.4% in February to 4.1% in March and above 7% in April 2026, well above the 2–4% target of the Bangko Sentral ng Pilipinas (BSP)."),
  p("The government responded on several fronts: Republic Act 12316 (March 2026) allowed the President to suspend fuel excise taxes when Dubai crude averages USD 80 per barrel or more; excise taxes on liquefied petroleum gas (LPG) and kerosene were suspended; fuel subsidies were given to public utility vehicle drivers; and the BSP raised its policy rate. Each measure assumes something about *who bears the cost* of a fuel price shock, but this has not been measured for the Philippines."),
  p("The best available evidence comes from a cross-country study by Kpodar and Liu (2022), which finds that fuel price shocks are *progressive*: prices rise more for richer households, because they spend more on transport. If this holds in the Philippines, broad fuel tax cuts mainly help the better-off. There are reasons to doubt it. Poor Filipino households spend more than half of their budget on food and rely on public transport and cooking fuels, which fuel prices affect indirectly. Regions also differ widely in poverty, diet and distance from fuel supply."),
  p("The Philippine Statistics Authority (PSA) publishes a monthly consumer price index (CPI) for the *bottom 30% income households* alongside the CPI for *all income households*, for the country and every region. This allows a direct test that the cross-country study could not make. The results will inform four policy decisions: (1) whether fuel excise relief under RA 12316 reaches the poor; (2) how large and how long emergency cash transfers should be; (3) whether fare and rice policy should be part of the response to an oil shock; and (4) how the BSP should gauge the second-round effects of fuel prices."),
);

add(h1("2. Research Questions"));
add(
  p("**Main question.** When retail fuel prices rise, do poor Filipino households face larger price increases than all households, and does the answer depend on where they live?"),
  p("The study has three specific objectives, each with research questions (RQ):"),
  num("**Objective 1 (descriptive).** Describe the trends, volatility and co-movement of retail fuel prices, all-income inflation and bottom-30% inflation, nationally and by region, from 2001 to 2026."),
  num("**Objective 2 (estimation).** Estimate the *pass-through* of retail fuel prices to (RQ1) the price level; (RQ2) the *inflation gap* between all households and the bottom 30%; (RQ3) each CPI spending category; and (RQ4) the inflation gap in groups of regions (high poverty, high food share, Mindanao, island regions)."),
  num("**Objective 3 (policy).** Use the estimates and the 2026 oil shock to assess the targeting of fuel excise relief, fuel subsidies, fare regulation, monetary policy and cash transfers."),
  p("**Hypotheses.** H1: pass-through is positive and persistent. H2a (cross-country finding): the effect is progressive—all-income prices rise more. H2b (alternative): the effect is regressive—bottom-30% prices rise more, through food and fares. H3: transport and food carry most of the pass-through. H4: the inflation gap is wider in poorer, more food-dependent and more remote regions.", { spacing: { before: 120, after: 120 } }),
);

add(h1("3. Framework"));
add(
  h2("3.1 Key terms"),
  p("The proposal uses five terms consistently. The *retail fuel price* is the pump price of gasoline and diesel, measured by the PSA CPI sub-index for fuels and lubricants for personal transport. A *fuel price shock* is a month-to-month change in the retail fuel price. *Pass-through* is the change in a price index, in percentage points, for each 1% change in the retail fuel price. The *all-income CPI* and *bottom-30% CPI* are PSA's two price indices. The *inflation gap* is D = ln(all-income CPI / bottom-30% CPI); a fall in D means prices rose more for the poor (a *regressive* effect), and a rise means they rose more for the average household (a *progressive* effect)."),
  h2("3.2 Conceptual framework"),
  p("A rise in world oil prices, converted at the peso–dollar rate, raises the retail fuel price, whose level also depends on taxes and margins (Figure 1). The shock reaches consumer prices through three channels: the *direct* channel (motor fuel, LPG and kerosene that households buy), the *indirect* channel (fares, food and utilities whose costs rise) and the *second-round* channel (wages and expectations). How much each group's price index rises depends on two things: its *basket weights* (how much it spends on each item) and the *price changes within each category* (the poor may buy different varieties whose prices respond differently). The difference between the two indices is the inflation gap. Regional characteristics may change both. Policy can act at the retail fuel price (excise relief, subsidies), in the indirect channel (fare regulation), in the second round (monetary policy), or on household income (transfers)."),
);
add(new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({
  type: "png", data: fs.readFileSync(path.join(ROOT, "output/figures/figw0_framework.png")),
  transformation: { width: 430, height: 381 } })] }));
add(note("**Figure 1.** Conceptual framework. Solid arrows show the transmission of a fuel price shock; dashed arrows show where policy can intervene."));

add(h1("4. Data Sources and Empirical Strategy"));
add(h2("4.1 Data"));
add(p("All data are public, monthly and downloadable through official websites or application programming interfaces (Table 1). The main sample covers January 2001 to the latest available month, for the Philippines and its 17 regions."));
add(caption("Table 1. Data sources"));
add(table([2600, 2500, 2460, 1800], [
  ["Variable", "Source", "Coverage", "Use"],
  ["All-income CPI and 13 spending categories (2018 = 100)", "PSA OpenSTAT", "1994–2026; national and 17 regions", "Outcome"],
  ["Bottom-30% CPI (2018 = 100)", "PSA OpenSTAT", "2000–2026; national and 17 regions", "Outcome"],
  ["Retail fuel price: CPI sub-index 07.2.2", "PSA OpenSTAT", "1994–2026; national and 17 regions", "Fuel price shock"],
  ["Pump price, Manila (RON 91)", "World Bank Global Fuel Prices Database", "2017–2025", "Check of the fuel series"],
  ["Dubai and Brent crude oil prices", "World Bank Pink Sheet", "1960–2026", "Alternative shock"],
  ["Peso–dollar rate; policy rate", "BSP; Bank for International Settlements", "Monthly", "Control variables"],
  ["World food prices", "FAO Food Price Index", "1990–2026", "Control variable"],
  ["Poverty incidence; CPI basket weights", "PSA", "2018, 2021, 2023; 2018 basket", "Region groups"],
  ["EU consumer prices and pump prices", "Eurostat; European Commission Weekly Oil Bulletin", "2000–2019", "Validation"],
]));
add(note("*Note:* The reference study's own retail fuel price database is not public; the PSA fuel sub-index is used instead and will be checked against the World Bank pump price before use."));

add(h2("4.2 Empirical model"));
add(p("We will use *local projections* (Jordà, 2005), following the specification of Kpodar and Liu (2022). A local projection estimates the effect of a shock at each future month *h* with a separate regression, rather than simulating it from a single dynamic model. For *h* = 0, 1, …, 12:"));
add(eq("Δln y_{t+h} = α_{h} + Σ_{q=1}^{12} γ_{1q} Δln y_{t−q} + Σ_{q=1}^{12} γ_{2q} Δln F_{t−q} + β_{h} Δln F_{t} + Σ_{l=1}^{h−1} γ_{3l} Δln F_{t+l} + δ_{h} t + ε_{t+h}", "1"));
add(
  p("Here *y* is a price index, *F* is the retail fuel price and *t* is a linear time trend. The lags of *y* and *F* absorb past dynamics and seasonality; the leads of *F* (the Teulings–Zubanov correction) separate the effect of today's shock from later shocks. The coefficient β_{h} is the pass-through at month *h*. The sum β_{0} + β_{1} + … + β_{h} is the *cumulative pass-through*: the effect on the price level after *h* months."),
  bullet("**RQ1:** *y* = all-income CPI and bottom-30% CPI, national."),
  bullet("**RQ2:** the outcome is ΔD, the monthly change in the inflation gap. A negative cumulative pass-through supports H2b (regressive); a positive one supports H2a (progressive)."),
  bullet("**RQ3:** *y* = each of the 13 CPI spending categories; the results are combined with each group's basket weights to see whether weights alone explain the inflation gap."),
  bullet("**RQ4:** a panel of 17 regions with region fixed effects u_{r}, using each region's own retail fuel price, plus an interaction with a group dummy G_{r}:"),
);
add(eq("ΔD_{r,t+h} = u_{r} + … + β_{h} Δln F_{r,t} + θ_{h} (Δln F_{r,t} × G_{r}) + ε_{r,t+h}", "2"));
add(
  p("where θ_{h} measures the additional effect in the group (for example, Mindanao). Standard errors will be Newey–West for national series and Driscoll–Kraay for the regional panel, which allow for correlation over time and across regions. Confidence bands will be 90%, as in the reference study."),
  h2("4.3 Validation, robustness and policy analysis"),
  bullet("**Validation.** Before any Philippine estimate, the code must reproduce the reference study's published EU result (pass-through of about 0.055 from pump prices and 0.015 from crude oil), using pass/fail criteria written down in advance. The estimator will also be tested on simulated data with a known answer."),
  bullet("**Robustness.** Crude oil instead of the retail fuel price; controls for the exchange rate, policy rate and world food prices; 6 and 18 lags; excluding 2020 and 2026; leaving out one region at a time."),
  bullet("**Policy analysis (Objective 3).** Estimate the model on data up to December 2025, apply it to the 2026 fuel price path, and compare the predicted and actual price increase. Convert the predicted increase for the bottom 30% into pesos for a family of five at the official poverty line, by region, and compare it with the value of the 2026 relief measures."),
);

add(h1("5. Workplan"));
add(caption("Table 2. Workplan, Weeks 11–18"));
add(table([1300, 4700, 3360], [
  ["Week", "Activities", "Output"],
  ["11", "Download and log all data; build the regional panel; check the fuel series against the pump price", "Clean dataset with source log"],
  ["12", "Validate the estimator: simulation test and EU replication of the reference study", "Validation note (pass/fail)"],
  ["13", "Objective 1: descriptive statistics, trends, fuel shock episodes, unit-root tests", "Descriptive tables and figures"],
  ["14", "Objective 2: estimate RQ1–RQ3 (national)", "Pass-through results"],
  ["15", "Objective 2: estimate RQ4 (regional panel) and robustness checks", "Regional and robustness results"],
  ["16", "Objective 3: 2026 out-of-sample test, peso costs, assessment of policy instruments", "Policy analysis"],
  ["17", "Write the full paper; adviser review", "Draft capstone paper"],
  ["18", "Revise; prepare presentation and replication files", "Final paper and presentation"],
]));
add(p("All steps will be scripted in Python so that every number can be reproduced with one command. Every specification choice will be recorded in a decision log before the results are seen.", { spacing: { before: 160, after: 120 } }));
add(caption("Table 3. Main risks and how we will handle them"));
add(table([3800, 5560], [
  ["Risk", "Response"],
  ["Retail fuel prices may respond to domestic conditions", "Re-estimate with world crude oil prices, which no Philippine region can affect"],
  ["Splicing of CPI base years", "Use PSA's own 2018-based back series; add dummies for the months where series are joined"],
  ["Regional boundary changes (e.g., Negros Island Region)", "Use the older 17-region coding, which matches the back series; test sensitivity"],
  ["Only a few months of 2026 data", "Treat the 2026 analysis as a test of the historical model, not as the main estimate"],
]));

add(h1("References"));
for (const r of [
  "Jordà, Ò. (2005). Estimation and inference of impulse responses by local projections. *American Economic Review*, 95(1), 161–182.",
  "Kpodar, K., & Liu, B. (2022). The distributional implications of the impact of fuel price increases on inflation. *Energy Economics*, 108, 105909.",
  "Teulings, C. N., & Zubanov, N. (2014). Is economic recovery a myth? Robust estimation of impulse responses. *Journal of Applied Econometrics*, 29(3), 497–514.",
  "Driscoll, J. C., & Kraay, A. C. (1998). Consistent covariance matrix estimation with spatially dependent panel data. *Review of Economics and Statistics*, 80(4), 549–560.",
  "Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.",
  "Republic of the Philippines. (2026). Republic Act No. 12316: An Act authorizing the President to suspend or reduce excise tax on petroleum products.",
  "Philippine Statistics Authority. (2026). OpenSTAT: Consumer Price Index for All Income Households and for the Bottom 30% Income Households (2018 = 100).",
]) add(new Paragraph({ children: runs(r, { size: 22 }), indent: { left: 720, hanging: 720 }, spacing: { after: 80 } }));

// ---------- document
const doc = new Document({
  creator: "Capstone group",
  title: "FA2 Capstone Proposal: Who Pays for Oil Shocks?",
  styles: {
    default: { document: { run: { font: FONT, size: 24 }, paragraph: { spacing: { line: 276 } } } },
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
