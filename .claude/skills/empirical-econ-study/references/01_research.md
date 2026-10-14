# Phase 1 — Research: from concept note to a pinned-down specification

Goal: one document (`CLAUDE.md`) that says exactly what the study will estimate and
why, so that every later choice can be checked against it.

## 1.1 Read the concept note and frame the questions

Extract from the concept note:

1. **Main question.** State it in one sentence, in plain words.
2. **Research questions (RQ1, RQ2, …).** Make each one answerable by one model or
   one table.
3. **Hypotheses.** When the literature points one way and local conditions point
   the other, write *competing* hypotheses. Example: H2a, progressive (the
   cross-country finding), against H2b, regressive (the local alternative). A test
   between two named hypotheses is more interesting than a test against zero.
4. **Three objectives.** These are required for working papers and proposals:
   - **Objective 1, descriptive:** trends, volatility, episodes, co-movement.
   - **Objective 2, estimation:** the model, which answers the RQs.
   - **Objective 3, policy:** what the estimates imply for named instruments.

   Map every RQ to an objective.

## 1.2 Read the reference paper like a replicator

The text of a paper often leaves the specification ambiguous. The annex tables
usually settle it. For each element of the main equation, write down the answer
and the evidence that settles it:

- **Outcome.** Is it a one-period change or a cumulative change? Look at the lag
  coefficients along the diagonal across horizons. In the worked example, the
  coefficient on lag (12 − h) stayed at about 0.47. That only happens if the
  outcome is a single month (decision D1).
- **Seasonal adjustment.** A large coefficient on lag 12 in monthly data means the
  data are not seasonally adjusted (D2).
- **Deterministic terms.** Check for a constant, a trend and fixed effects by
  looking at which rows the tables report (D3).
- **Correction terms.** For Teulings–Zubanov leads, check in which horizon column
  "Lead 1" first appears; this sets the lead set (D4).
- **Shock variable, units, sample, horizons, band width, standard-error type.**
  If the text and the table notes disagree (for example "clustered" against
  "robust"), list it as an open question and check both in the replication.

Put the answers in a "Reference specification" section of `CLAUDE.md`. Each
inferred element becomes a numbered decision, with the table and the coefficient
that justify it.

## 1.3 Record the targets

Type the reference paper's coefficients for every number you will try to
reproduce (figure values, annex table cells) into
`replication/<paper>_targets.csv`. Use columns `source, sample, outcome, shock,
h, beta, se, note`. Phase 3 compares against this file.

## 1.4 Check which data exist before promising anything

Before fixing the RQs, check:

- **Does the reference paper's own dataset exist publicly?** The worked example's
  fuel price database did not. A substitute was chosen and validated (D5).
- **What is the finest geography and frequency for each variable?**
- **Do official distributional indices exist?** In the worked example, PSA
  publishes a CPI for the bottom 30% income households. Know who constructs each
  category: an official agency, or the study itself. The user will ask, and the
  paper must say.

Write a short feasibility note: what can be estimated, what cannot, and what the
substitute is.

## 1.5 Theory

Find two layers of theory and cite verified sources:

1. A **general economic theory** that predicts the sign or size of the effect. In
   the worked example there were two:
   - **Cost-push pricing:** the Leontief input–output price model gives π_k ≈ φ_k·f.
   - **Cost-of-living index theory:** π^g = Σ_k w^g_k π_k, so pass-through equals
     the fuel intensity of the group's basket. Add the gap decomposition into a
     weights effect and a within-category effect, and Deaton (1989) for the
     welfare cost.
2. A **topic-specific theory**, for example for oil prices:
   - Kilian (2008), direct and indirect channels;
   - Blanchard and Galí (2010), second-round effects;
   - Arze del Granado, Coady and Gillingham (2012), incidence.

Write the theory as equations that lead to the estimating equation and to each
hypothesis. A framework diagram (shock → channels → group price indices → gap,
with dashed arrows for policy levers) helps every document.

## 1.6 Output of Phase 1

`CLAUDE.md`, built from `assets/CLAUDE_template.md`, containing:

- the brief;
- the reference specification;
- decisions D1…;
- the targets file;
- the open questions;
- a draft of the RQs and hypotheses.

Commit it.
