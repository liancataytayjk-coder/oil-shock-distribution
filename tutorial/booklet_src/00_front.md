---
title: "Local Projections, Step by Step"
subtitle: "Theory, code, implementation and interpretation, with the Philippine fuel pass-through study as the worked example"
author: "{{ author }}"
date: "{{ date }}"
---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Contents {.unnumbered}

<!--CONTENTS-->

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# About this booklet

This booklet teaches one econometric tool, the *local projection*, from the first idea to the last sentence of a results section. It uses a real study as its running example: the author's study of how retail fuel prices pass through to the inflation of poor households in the Philippines, which replicates the design of @kpodar_liu_2022 on Philippine data. Every number in the booklet comes from a script that runs on the study's own data, so you can reproduce each one yourself.

The booklet has three parts. Part I explains the theory: what question a local projection answers, why it works, what each term in the regression does, and how to judge how precise the answer is. Part II implements the method step by step in Python, first by hand and then with the study's own estimator, and shows the same steps in Stata. Part III explains how to read and report the results, using the study's three research questions as worked examples, and ends with a list of common mistakes, a checklist, exercises with answers and a glossary.

You need only basic regression: what ordinary least squares (OLS) does, what a coefficient and a standard error mean, and how to read a confidence interval. Every other term is defined the first time it is used, first in words, then as a formula, then with an example. A short glossary at the end collects the definitions.

To follow the code, open the study's repository and run, from its top folder,

```bash
.venv/bin/python tutorial/lp_tutorial.py
.venv/bin/python tutorial/build_booklet.py
```

The first command prints seven tables, one for each step in Part II, writes the figures to `tutorial/figures/` and saves every number to `tutorial/tutorial_numbers.json`. The second command reads those numbers and the study's results (`output/tables/paper_numbers.json`) and writes this booklet. The shorter, web version of the same material is `tutorial/README.md`.

Three conventions are used throughout. A *month* is indexed by *t*. A *log change* times 100, $100\,\Delta \ln X_t = 100(\ln X_t - \ln X_{t-1})$, is used as the monthly percentage change; for small changes the two are almost equal (a rise from 100 to 101 is a log change of 0.995). And all confidence bands are 90% bands, as in the reference study.
