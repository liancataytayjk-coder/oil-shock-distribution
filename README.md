# Who Pays for Oil Shocks?

Fuel price pass-through to the inflation of poor households across Philippine regions
(Lian Cataytay, Graduate School of Applied Economics, University of Southeastern Philippines).

| What | Where |
|---|---|
| Handoff guide (start here) | `handoff/HANDOFF_GUIDE.pdf` / `.docx`; zips via `handoff/build_handoff.py` |
| Research proposal, short national pitch | `paper/proposal_pitch.pdf` / `.docx` |
| Working paper (chapter form) | `paper/working_paper.pdf` / `.docx` |
| Journal article for the *Asian Economic Journal* (reading version) | `paper/article.pdf` / `.docx` |
| Article: online appendix, blinded submission file, title page | `paper/article_online_appendix.*`, `paper/article_submission.*`, `paper/article_title_page.*` |
| Reference check of the 15 reviewed studies | `paper/reference_check.md` |
| Study kit: 10-day plan, defense questions with answers, LP on any data | `study_kit/study_kit.pdf` / `.docx`, `study_kit/lp_any.py`, `study_kit/lp_any.do` |
| Codebook (every raw and cleaned variable, sources, regions, results map) | `codebook/codebook.xlsx` |
| Raw data, as downloaded, with source log | `data/raw/` |
| Cleaned, analysis-ready data (CSV) | `data/clean/` |
| Code: Python | `code/python/` (run `./run_all.sh`) |
| Code: Stata 17 (replication and check against Python; written, not yet run) | `code/stata/` (run `00_master.do`; see its README) |
| Tables and figures | `output/tables/`, `output/figures/` |
| Local projections tutorial (theory + code) | `tutorial/README.md` |
| Local projections booklet (theory, code, interpretation; Word + PDF) | `tutorial/lp_booklet.docx`, `.pdf` (built by `tutorial/build_booklet.py`) |
| House-style tools (Word/PDF formatting) | `tools/lian_style/` |
| Complete first version (archived) | `archive/v1_full/` |

To rebuild everything with Python 3.11:

```bash
python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt
./run_all.sh              # add --download to refetch the PSA tables
```

PDFs need LibreOffice Writer (`apt-get install libreoffice-writer libreoffice-math`).
