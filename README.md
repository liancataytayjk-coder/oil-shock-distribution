# Who Pays for Oil Shocks?

Fuel price pass-through to the inflation of poor households across Philippine regions
(Lian Cataytay, Graduate School of Applied Economics, University of Southeastern Philippines).

| What | Where |
|---|---|
| Working paper (chapter form) | `paper/working_paper.pdf` / `.docx` |
| Journal article (IMRAD, with online appendix) | `paper/article.pdf` / `.docx` |
| Codebook (every raw and cleaned variable, sources, regions, results map) | `codebook/codebook.xlsx` |
| Raw data, as downloaded, with source log | `data/raw/` |
| Cleaned, analysis-ready data (CSV) | `data/clean/` |
| Code: Python | `code/python/` (run `./run_all.sh`) |
| Code: Stata 17 | `code/stata/` (run `00_master.do`) |
| Tables and figures | `output/tables/`, `output/figures/` |
| House-style tools (Word/PDF formatting) | `tools/lian_style/` |
| Complete first version (archived) | `archive/v1_full/` |

To rebuild everything with Python 3.11:

```bash
python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt
./run_all.sh              # add --download to refetch the PSA tables
```

PDFs need LibreOffice Writer (`apt-get install libreoffice-writer libreoffice-math`).
