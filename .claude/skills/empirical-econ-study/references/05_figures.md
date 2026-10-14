# Phase 5 — Figures and tables

Journals print in greyscale, and they caption figures in the text. Make figures
that survive both.

## Figure rules

- **Colour:** black and white only.
  - Tell series apart with line style and marker: series 1 solid with filled
    circles, series 2 dashed with open squares.
  - Confidence bands: light grey fill for the first series, dotted bound lines for
    the second.
  - Bars: grey fill or hatching.
- **Type:** serif font, size 9.
- **Axes:** no top or right spines, no grid, a thin zero line.
- **No title inside the image.** The caption lives in the document, so the same
  image works in every document.
- **Labels:** axes in plain words ("Months after the shock", "Percentage points").
  Legends without frames, placed where they do not cover data.
- **Formats:** each figure as 300-dpi PNG and TIFF (LZW), plus a vector PDF with
  `metadata={"CreationDate": None}`, so reruns are byte-identical and git diffs
  stay clean.
- Use `scripts/fig_style.py` (`setup()`, `save()`, `irf()`, styles `A` and `B`).

## Standard figure set for this design

1. Impulse responses: the group price indices, cumulative, with bands.
2. The distributional gap response, national and panel.
3. Category responses, as a dot plot or bars.
4. Heterogeneity: θ_h by group.
5. Robustness: a forest plot of the decisive-horizon estimate across checks.
6. The episode: actual against model-predicted paths.
7. Unit ranking, such as the regional burden.
8. Descriptive figures:
   - long-run series;
   - the cumulative gap with episodes shaded;
   - cross-correlations.
9. Validation: the replication against the targets.
10. A conceptual framework diagram, drawn in matplotlib with boxes and arrows;
    dashed arrows show policy levers.

## Tables

Generate tables in the document script from `estimates.csv`, using a markdown
table helper. Pandoc needs a blank line before and after every table. Use
significance stars at 10%, 5% and 1%. Always report the standard error in
parentheses. Put the full set of estimates in a statistical annex, not in the
paper body.
