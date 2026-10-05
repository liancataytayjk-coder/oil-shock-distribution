# Action list to finalise "Who Pays for Oil Shocks?"

The manuscript (`paper/manuscript.docx`, generated from `paper/manuscript_template.md`
by `scripts/08_paper.py`) is a complete IMRAD draft. Every number in it comes from
`output/tables/`, so edit the template, not the .docx, and rerun `./run_all.sh`.
The items below are what stands between the draft and submission.

## A. Decisions for you and your adviser (before anything else)

- [ ] **Framing.** The draft leads with "not progressive; regressive in sign, concentrated
      in 2001–2012, and the 2026 excess burden came through rice". Confirm, or choose a
      narrower headline (for example pass-through plus the 2026 episode).
- [ ] **Distribution outcome.** The draft uses the monthly change in ln(CPI_all/CPI_b30)
      and reports cumulative (level) responses. Confirm this reading of the reference study.
- [ ] **Supplementary analyses.** Decide whether the within-category comparison (RQ3b)
      and the 2026 episode stay in the main text (current draft) or move to an appendix.
- [ ] **Title.** The draft title adds "Rice" and "2001–2026" to the concept-note title.

## B. Checks only you can do

- [ ] Read the *Energy Economics* version of Kpodar and Liu (2022) via the USeP library
      and confirm the specification matches the working paper (horizons, leads, trend,
      standard errors). Update CLAUDE.md D1–D4 if anything differs.
- [ ] Confirm from PSA's technical notes: (i) how the bottom-30% CPI is built (basket,
      weights from 2018 FIES, same price collection?); (ii) whether pre-2019 BARMM values
      use ARMM or BARMM boundaries. Adjust Section 2.1 wording if needed.
- [ ] Check the 2026 policy facts flagged "secondary" in `paper/policy_context_2026.md`
      against the official issuances: EO 114 (April 2026) and EO 125 (25 Sep 2026), the
      LPG/kerosene excise amounts, Pantawid Pasada amounts, LTFRB fare order.
- [ ] Read USDA GAIN report RP2026-0007 before citing it on rice (Section 3.6); add DA or
      PSA rice-price sources if you prefer domestic citations.
- [ ] Check the three bibliography entries marked "to be checked" (given names in
      Wihardja and Pradana 2024, Pagaduan 2022, Armas 2021; volume year of Blanchard and
      Galí 2010) and the AEJ reference style.
- [ ] Read every paragraph against the tables. You must be able to defend each number
      and claim in review.

## C. Analyses that would strengthen the paper (I can run these)

- [ ] **Identified oil supply shock as an instrument** (Känzig 2021 or Baumeister and
      Hamilton 2019 series; check that the public files reach 2026). This answers the main
      endogeneity objection. Highest priority.
- [ ] **Policy event dummies**: TRAIN excise steps (Jan 2018–2020), the 2026 LPG/kerosene
      suspensions, fare orders. Robustness for Table 3.
- [ ] **Joint inference for the 2026 fuel-driven paths** (bootstrap) to replace the
      "indicative" comonotone ranges in Section 3.6 and Table 6.
- [ ] **Top-70% CPI** for a sharper rich–poor contrast, if the bottom 30%'s share of total
      household spending can be found in published FIES tables.
- [ ] **Extend to September 2026** when PSA releases it (rerun `./run_all.sh --download`);
      this captures the 28 Sep fare increase and the second excise suspension.
- [ ] Regional map figure of 2026 bottom-30% inflation (public boundary files).

## D. Submission package (Asian Economic Journal, Wiley)

- [ ] Check AEJ author guidelines for length, abstract limit, reference style, figure
      format, and anonymised manuscript requirements; adjust the template.
- [ ] Complete the declarations: AI-use statement (required by Wiley; describe the use of
      Claude Code for data processing, coding and drafting, and confirm your review and
      responsibility), funding, conflicts, acknowledgements.
- [ ] Title page with author details separate from the anonymised manuscript.
- [ ] Cover letter (I can draft it once the framing is fixed).
- [ ] Replication package: this repository at a tagged commit, with README, data licence
      notes (PSA, World Bank ODbL, Eurostat, FAO, BIS) and `./run_all.sh` instructions.
- [ ] Adviser and, ideally, one external reader review before submission.
