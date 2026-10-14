# Phase 7 — Delivery, reproducibility and handoff

## One-command rebuild

`run_all.sh` runs the whole pipeline in order:

1. clean, then build the panel;
2. replicate, then estimate;
3. run the episode analysis and the descriptive statistics;
4. draw the figures;
5. render the paper;
6. render the analysis report;
7. run `pytest`;
8. assemble the master document.

With `--download`, it runs the downloads first. Check that it runs end to end in a
fresh environment before you call the work finished.

## Packaging for the user

- **Commit** code, raw data (if size allows, roughly under 50 MB), templates and
  rendered documents to the working branch. Push only to the branch you were
  assigned.
- **Zip** for download if the user wants files outside git. Keep each zip under
  the upload limit, which was 30 MB in this environment, by splitting into three:
  1. code, documents and outputs;
  2. raw data from the main source;
  3. raw data from other sources.

  Put the zips in `deliverables/`, which is gitignored.
- **Send** the key files to the user, such as the `.docx` documents, with a
  one-line caption each.

## Handoff to a new session

Write or refresh `docs/session_handoff.Rmd` from `assets/session_handoff_template.Rmd`.
It must include:

- how to start a new session and which branch to check out (the default branch
  may not have the work);
- the must-upload list: files that are not in the repository, such as copyrighted
  PDFs, formatting templates, rubrics and names;
- the standing rules and the user's style preferences;
- a one-page summary of the study, with notation;
- the data facts and the answers to questions the user has asked;
- the headline results;
- the file map;
- the open items.

Also keep the "Documents" and "Open questions" sections of `CLAUDE.md` current.

## Before you say "done"

Check each of these:

- the tests pass;
- documents re-render with no hand edits;
- the page limits are checked;
- placeholders are listed for the user;
- unverified references are flagged;
- the decisions log is up to date;
- the commit is pushed.

Tell the user exactly what still needs their input.
