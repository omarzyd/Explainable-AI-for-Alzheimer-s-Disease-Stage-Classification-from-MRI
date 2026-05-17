# Contributing

Contributions to the **implementation** are welcome. The **manuscript** remains author-controlled.

## Before contributing

1. Read [NOTICE.md](NOTICE.md) — MIT code vs. protected PDF.
2. Cite the [manuscript in preparation (2026)](docs/reports/citation.bib) if you use methods, benchmarks, or figures.
3. Do not rehost [`docs/reports/Explainable AI for AD Stage Classification.pdf`](docs/reports/Explainable%20AI%20for%20AD%20Stage%20Classification.pdf).

## Protected paths (author review required)

| Path | Reason |
|------|--------|
| `docs/reports/*.pdf` | Copyrighted manuscript |
| `CITATION.cff`, `NOTICE.md`, `docs/reports/COPYRIGHT.md` | Citation & legal metadata |

See [.github/CODEOWNERS](.github/CODEOWNERS).

## Implementation guidelines

1. Fork and branch: `git checkout -b feature/description`.
2. `pip install -r requirements.txt`
3. Edit under `notebooks/`; keep experiments self-contained (preprocess → train → evaluate → XAI).
4. Match paper terminology (patient-level splits, Liquid Finder, OvA) where applicable.
5. Update `README.md` if adding or renaming notebooks.

## Pull requests

- Summarize architecture, dataset, and XAI methods changed.
- Do not commit ADNI volumes or large image dumps.
- Note whether results affect claims in the manuscript (authors must reconcile).

## Academic integrity

Reusing prose, figures, or the Liquid Finder description without citation is prohibited. Forks must attribute the authors and link to this repository.
