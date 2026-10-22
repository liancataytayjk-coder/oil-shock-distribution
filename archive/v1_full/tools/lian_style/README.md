# House style tools (vendored)

Copy of the `lian-signature-style` skill's scripts and assets, so the pipeline can
apply the house style (Times New Roman, black and white, three-line tables,
1-inch margins) and make PDFs without the skill installed.

- `scripts/docx_style.py finish in.docx [--spacing double|onehalf|single]`
- `scripts/render.py file.docx|file.pptx --png` (needs LibreOffice Writer/Impress)
- `scripts/check_style.py file`
- `scripts/lian_deck.py`: the `Deck` builder used by `scripts/13_presentation.py`

Used by `scripts/08_paper.py` (reference .docx) and `scripts/14_submissions.py`.
