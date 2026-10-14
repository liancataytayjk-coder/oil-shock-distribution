# Writing style guide

These rules come from the user's own requests across the worked example. They
apply to every document, and to chat answers too.

## 1. Write as simply as possible, and avoid the curse of knowledge

The *curse of knowledge* is assuming that the reader already knows what you know.
The reader is a smart economics student, or an adviser outside this subfield, who
has never run a local projection.

- **Define each term the first time it appears, in plain words, then use it the
  same way everywhere.** "Pass-through is how much consumer prices rise, in
  percentage points, for each 1% rise in fuel prices." Do not switch later to
  "elasticity" or "sensitivity" for the same thing.
- **Spell out abbreviations on first use.** For example: consumer price index (CPI),
  Bangko Sentral ng Pilipinas (BSP), liquefied petroleum gas (LPG).
- **Say why, not only what.** Not "we include 12 lags" but "the twelve past values
  account for earlier movements and for seasonal patterns, such as higher prices
  every December."
- **Explain econometric jargon in one plain clause:**
  - *fixed effects*: "let each region have its own average";
  - *standard errors*: "measure how uncertain the estimate is";
  - *Driscoll–Kraay*: "allow for correlation over time and across regions";
  - *Teulings–Zubanov leads*: "so that β is not confused with the effect of later shocks".
- **Prefer short sentences and the active voice.** Use "we will estimate", not "it
  is to be estimated". One idea per sentence where possible.
- **Use concrete local examples.** Jeepney fares, rice that is pumped, trucked and
  milled, LPG for cooking.

## 2. Keep the technical terms, with mathematical notation

Simplicity does not mean dropping precision. For each key variable or concept,
give three things in this order:

1. the words;
2. the formula (numbered if referred to later);
3. a one-line numerical example of how to read it.

Example:

> **Inflation gap.** The gap compares the two price levels; its monthly change
> equals the difference between the two inflation rates:
> D_t = 100 × ln(P^A_t / P^B_t), ΔD_t = π^A_t − π^B_t.
> If D falls, prices rose faster for the bottom 30%: the shock is *regressive*.

Keep notation consistent across every document:

- **Indices:** t month, r region, k category.
- **Groups:** superscript g, with A = all income and B = bottom 30%.
- **Variables:** f = shock, π = inflation, β_h and B_h = pass-through, D = gap,
  w = weights, G = group dummy, θ = interaction.

## 3. Prefer paragraphs to bullets and tables

Write workplans, timelines, objectives, robustness lists and risks as paragraphs,
whenever they can be. Keep a table only where it is the clearest form:

- variable and data-source lists;
- notation;
- coefficient tables;
- region-group membership.

Keep bullets only for genuinely list-like items, such as a must-upload list.

## 4. Be honest about what the evidence shows

- Separate official statistics from the study's own constructions. For example:
  "the bottom-30% CPI is PSA's; the gap and the region groups are ours".
- State fragility plainly: "significant only at h = 3, 4, 7, 8"; "about zero with
  macro controls".
- Label each analysis pre-registered, supplementary or exploratory.
- Do not overclaim policy implications. Tie each one to a specific estimate.

## 5. Figures and captions

- Captions are full sentences that say what is plotted, the units, and what the
  bands mean.
- No title inside the image.

## 6. Chat answers to the user

- Lead with the direct answer.
- Then give the evidence and the file names.
- Use plain language.
- When the user asks several questions at once, answer each under its own short
  heading, in their order.
