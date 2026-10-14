---
name: empirical-econ-study
description: End-to-end workflow for an empirical economics study that replicates a published design on new (often Philippine or developing-country) data, from finding the reference paper and collecting official data, through a pre-registered replication gate, estimation (local projections, panels, robustness) and black-and-white journal figures, to writing every document (proposal, working paper with the three-objective structure, IMRAD manuscript, analysis report, master document, session handoff) in plain, well-defined language. Use this skill whenever the user wants to plan, implement, continue, check or write up an applied econometrics or policy study, e.g. "help me implement this study", "find the data", "estimate the model", "replicate this paper", "write the methodology or results chapter", "make my proposal", or asks about pass-through, impulse responses, inflation, poverty or regional data, even if they never name this skill.
---

# Empirical economics study: research → data → analysis → writing

This skill turns a research idea (usually a concept note plus one reference paper)
into a finished, reproducible study and all the documents around it. It was
distilled from a complete study, *Who Pays for Oil Shocks? Fuel Price
Pass-Through to the Inflation of Poor Households across Philippine Regions*,
which replicated Kpodar and Liu (2022) on PSA data. That study is used as the
worked example throughout; the method is general.

The user is typically a graduate student in economics. Two needs shape every
phase. First, the work must survive a referee: every number reproducible, every
choice written down before the results are seen. Second, the user must be able to
*learn and defend* it, so the documents explain plainly what was done and why.

## The seven phases and their gates

Work through the phases in order. Each ends in a gate: a concrete check that must
pass before the next phase starts. Skipping a gate is the most common way an
applied study goes wrong (for example, running the national model on a broken
estimator, or reporting results before deciding which ones count).

| Phase | What happens | Gate (must pass) | Read |
|---|---|---|---|
| 1. Research | Read the concept note and the reference paper; write the project brief, research questions and hypotheses; extract the reference specification and its target coefficients | Brief written in `CLAUDE.md`; every element of the reference equation is pinned down or listed as an open question | `references/01_research.md` |
| 2. Data | Find official sources, download raw files untouched, log each one, clean, splice base years, reconcile geography, build panels | Every raw file in `data/raw/source_log.md`; proxies checked against an independent series | `references/02_data.md` |
| 3. Validation | Test the estimator on simulated data; replicate the reference paper's published result with pass/fail criteria fixed in advance | Simulation test passes; replication gate passes | `references/03_validation.md` |
| 4. Estimation | Pre-specify the estimation plan, then run the main models, heterogeneity and robustness | Plan written in the decisions log *before* the first estimate on the new data | `references/04_estimation.md` |
| 5. Figures and tables | Script every figure and table from the saved estimates | Black-and-white, no in-image titles, reproducible byte for byte | `references/05_figures.md` |
| 6. Writing | Render each document from templates that pull numbers from the output tables | No number typed by hand; terms defined; style rules met | `references/06_writing.md`, `references/style_guide.md` |
| 7. Delivery | Package code, data and documents; write the handoff; commit and push | `run_all.sh` rebuilds everything from `data/raw/`; tests pass | `references/07_delivery.md` |

Read the reference file for a phase when you reach it, not all at once.

## Where to start

Find out where the project is before doing anything:

1. Look for `CLAUDE.md`, `docs/session_handoff.Rmd`, `README.md` and `run_all.sh`
   in the repository. If they exist, the project is under way. Read them and
   continue from the first gate that has not passed.
2. If only a concept note and a reference paper exist, start at Phase 1. Set up
   the layout in `references/project_layout.md`.
3. If the user asks for one document (for example a proposal), check whether the
   study is finished. The proposal for an unfinished study must not contain
   results. Then follow that document's recipe in `references/06_writing.md`.

When the user asks "what do you need?" or "what next?", answer with a short,
ordered list tied to the phases and gates above. Name the exact files or
decisions you need from them, such as the reference paper PDF, a formatting
template, or the adviser's choice between two outcome definitions.

## Rules that hold in every phase

These rules are what made the worked example defensible. The reason for each is
given, so you can apply it to cases not listed here.

- **Raw data are never edited.** `data/raw/` holds untouched downloads, and each
  file has a line in `source_log.md` giving the URL, the date pulled, the base
  year, the coverage and notes. Anyone can then re-download and check.
- **Outputs are written only by scripts.** `data/processed/`, `output/` and every
  rendered `.md`/`.docx` come from code. To change a document, edit its
  *template* or script, never the output. Otherwise the next run silently undoes
  the change.
- **Every specification choice goes in the decisions log** in `CLAUDE.md`. Each
  entry has a number (D1, D2, …), a date, the decision and the evidence for it.
  Mark when it was made relative to the results:
  - *pre-registered*: before any estimate;
  - *supplementary*: specified before running, but after the main results were seen;
  - *exploratory*: added after seeing results.

  Readers trust a finding more when they can see it was not chosen after the fact.
- **No new-data estimate before the replication gate passes.** If the code cannot
  reproduce a published number, any new number it produces means nothing.
- **Report what you find, including what is fragile.**
  - If a result loses significance under some checks, say which checks.
  - If a correction for multiple tests kills an interaction, say so.
  - If a model explains only half of an episode, say that and find out what explains the rest.
- **Verify every reference before citing it**, using Crossref
  (`scripts/crossref_check.py`). Flag anything that cannot be verified, and never
  invent page numbers or DOIs. Policy facts (laws, dates, official statistics)
  need a source URL, kept in a sourced-facts file.
- **Write for a reader who does not know the field yet.** Follow
  `references/style_guide.md` in every document, every answer and every comment.

## Bundled scripts

Copy these into the project and adapt them. Do not rewrite them from scratch.

- `scripts/lp.py`: local projections with Teulings–Zubanov leads.
  - Handles a single series or a panel (unit fixed effects).
  - Standard errors: Newey–West, clustered, robust or Driscoll–Kraay.
  - Supports cumulative (running-sum) responses, controls, interactions and a sample mask.
- `scripts/test_lp.py`: simulation tests that the estimator recovers a known
  impulse response. Run it before any real estimate (Phase 3).
- `scripts/pxweb_download.py`: downloader for PxWeb statistical APIs (PSA
  OpenSTAT, and the same software used by Statistics Sweden, Finland, Norway and
  others). It pulls one geography at a time, retries, and falls back to Latin-1.
- `scripts/fig_style.py`: black-and-white journal figure style and a `save()` that
  writes 300-dpi PNG and TIFF plus a byte-stable PDF.
- `scripts/crossref_check.py`: looks up each reference title on Crossref and
  prints authors, journal, volume, pages, year and DOI for comparison.
- `scripts/render_doc.py`: renders a Jinja2 markdown template with the numbers
  dictionary, then pandoc to `.docx`, with citeproc. Its comment delimiters are
  changed because pandoc uses `{#refs}`.
- `assets/CLAUDE_template.md`: the project-brief skeleton (conventions, reference
  specification, decisions log, plans, results, open questions).
- `assets/session_handoff_template.Rmd`: the handoff file for starting a new session.

## Communicating with the user

- After each phase, state in a few plain sentences:
  - what was done;
  - what the gate showed;
  - what comes next;
  - anything the user must decide.
- When the user must choose (for example the outcome in levels or in changes),
  give both options, say what each implies, recommend one, and record the choice
  in the decisions log.
- Answer factual questions about the study ("did PSA make this category or did
  we?", "what proxies the oil shock?") directly. Name the source, and say clearly
  which parts are official statistics and which are the study's own constructions.
- If a file the user mentions has not arrived, say so at once and offer
  alternatives: re-upload it, commit it to the repository, or paste its rules.
