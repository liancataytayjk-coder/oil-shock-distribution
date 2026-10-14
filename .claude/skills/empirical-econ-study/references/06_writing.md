# Phase 6 — Writing: one set of numbers, many documents

Every document is rendered from a template. Numbers come from `output/tables/`
through a numbers dictionary `n` (saved as `output/tables/paper_numbers.json`) and
pre-built tables `t`. Nobody types an estimate. If the analysis changes, one
rebuild updates every document, so documents cannot disagree with each other or
with the code.

Read `style_guide.md` before writing any of these.

## 6.0 Mechanics

The rendering pipeline is `paper/<doc>_template.md` → Jinja2 → `paper/<doc>.md` →
pandoc with `--citeproc` and `references.bib` → `.docx`. Use
`scripts/render_doc.py`. Points to watch:

- **Jinja and pandoc conflict.** Pandoc uses `{#refs}`, which Jinja reads as a
  comment, so set the Jinja comment delimiters to `<#-- --#>`. Put the reference
  list at the end with `::: {#refs}` and `:::`.
- **Literal "@".** Escape a literal "@" outside citations (`\@`), or citeproc will
  try to resolve it as a citation.
- **Tables.** Leave a blank line before and after every markdown table.
- **Figures.** Use `![Caption.](../output/figures/x.png){width=80%}`, and pass
  `--resource-path`.
- **Previewing.** LibreOffice may not work in the container. To preview, convert
  the `.docx` to HTML with pandoc and print it to PDF with Playwright Chromium;
  this gives an approximate page count.
- **Word-native documents.** When a document needs exact Word formatting (page
  limit, letter size, numbered equations, a fixed font), build it with docx-js:
  `node scripts/<n>_<doc>.js`. It uses a small inline-markup helper:
  - `*italic*` and `**bold**`;
  - `_{sub}` and `^{sup}`;
  - keep italics and subscripts in separate runs.

## 6.1 Document recipes

### Concept note (input, usually from the user)

Keep it as `docs/concept_note.md`.

### Capstone or thesis proposal (study not yet done)

It must contain no results. Default limit: 10 pages, Times New Roman 12, Letter.
Sections:

1. **Motivation and policy relevance.** Explain the problem in everyday terms,
   then the current episode (sourced facts), the policy responses, the
   literature's prior finding, and why the local case may differ.
2. **Research questions.** The main question, the three objectives *in
   paragraphs*, the RQs and the hypotheses (including competing ones).
3. **Key terms and notation.** For each term, give the word definition, then the
   formula, then a one-line numerical example. Cover:
   - the index (Laspeyres formula with weights);
   - the log change;
   - the shock;
   - inflation (monthly and annual);
   - pass-through β_h and the cumulative B_h;
   - the gap D;
   - the group dummies.

   Say which items are official statistics and which are the study's own
   constructions.
4. **Theoretical framework.**
   - General theory, as equations: cost-push pricing and the cost-of-living index
     → pass-through = basket intensity → gap decomposition → welfare cost.
   - Topic-specific theory.
   - The conceptual framework figure.
5. **Data and empirical strategy.**
   - A variables table: variable, symbol, source, coverage and use. This is a
     table that should stay a table.
   - The estimating equation, with each term explained in words.
   - The RQs mapped to outcomes, in prose.
   - The panel equation.
   - Standard errors explained plainly.
   - Validation, robustness and the policy analysis, in paragraphs.
6. **Workplan and timeline.** Write it week by week *in paragraphs*, with the
   output of each step. Write the risks and responses as a paragraph as well.
7. **References**, all verified.

Leave group-member placeholders, such as `[Name 1]`, for the user to fill.

### Working paper (thesis-style, three-objective rule)

- **Chapter 1, Introduction:** background, rationale, objectives (Obj 1
  descriptive, Obj 2 estimation, Obj 3 policy; RQs under Obj 2), significance,
  scope and limitations, definition of terms.
- **Chapter 2, Review of Related Literature:** organised by theme (transmission;
  empirical pass-through; incidence; local studies; regional evidence); synthesis
  and gap; conceptual framework.
- **Chapter 3, Digression, the model and how to implement it:**
  - the question an impulse response answers;
  - the local projection idea;
  - the specification term by term;
  - from monthly effects to the level;
  - standard errors;
  - the panel and group differences;
  - checking the implementation;
  - a step-by-step implementation with code excerpts;
  - common pitfalls.

  This chapter is a tutorial: someone new to the method should be able to
  reproduce the study from it.
- **Chapter 4, Methodology:** design; data (sources, collection, processing);
  methods *by objective*; validation; software and reproducibility; ethics.
- **Chapter 5, Results and Discussion:** in three sections, one per objective, in
  the same order as Chapter 1. Each result is followed by what it means
  economically and how it compares with the literature.
- **Chapter 6, Summary, Conclusions and Recommendations:** one paragraph of
  summary per objective, the conclusions, and recommendations addressed to named
  agencies, plus further research.

### Journal manuscript (IMRAD)

Structure:

- Introduction: motivation, this paper, literature and contribution.
- Methods: data, specification, the episode analysis, validation and
  pre-specification.
- Results, ordered by RQ, then robustness, then the episode.
- Discussion: findings, policy, limitations, conclusion.
- Declarations.
- References, then tables, then figures at the end.

Tone for the manuscript:

- Concise, with the limitations stated plainly.
- Fragile results are presented as fragile.
- Pre-registered, supplementary and exploratory analyses are labelled.

Keep `paper/SUBMISSION_CHECKLIST.md` for what remains before submission: journal
format, word limit, references flagged as unverified, cover letter, data
statement.

### Analysis report (simple, visual)

One analysis per page, in four parts:

1. **Context and process:** why the analysis was done and how, in a short
   paragraph.
2. **The figure.**
3. **What the figure shows:** a literal reading of the figure.
4. **What it means:** the economics.

Parts:

- A: checking the tools (simulation, replication).
- B: the data at a glance (Objective 1).
- C: the estimates (Objective 2).
- D: the current episode and policy (Objective 3).

Open with a "how to read this report" box that explains log points, responses,
the gap and the bands.

### Statistical annex

Every estimate in full tables (all horizons, standard errors, number of
observations, robustness, interactions), generated. The analysis report points
here instead of printing tables.

### Master document (for learning)

A narrative of the whole process, written from `docs/master_narrative_template.md`.
It covers:

- what was done at each phase;
- why each decision was made;
- what went wrong and how it was fixed.

Then append, as appendices, every other document:

- the concept note;
- `CLAUDE.md`;
- the source log;
- the policy facts;
- the analysis report;
- the annex;
- the working paper;
- the manuscript;
- the checklist;
- the bibliography;
- **all code**;
- the git log.

Demote the headings of appended documents and strip their YAML front matter. Use
`scripts/11_master_document.py` from the worked example as the model.

### Session handoff

Use `assets/session_handoff_template.Rmd`. Update it whenever the project changes
materially, so a fresh session can resume.

## 6.2 Formatting templates from the user

If the user supplies a template (journal, school or IMF style), follow it exactly:
margins, fonts, heading levels, citation style. If they mention one but it has not
arrived, say so immediately. Ask them to re-upload it or commit it to the
repository. Until it arrives, propose a fallback and do not apply it silently.
