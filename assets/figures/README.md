# Figure assets

PNG figures for the repository README, generated from local ADNI slices when available.

## Regenerate

```bash
pip install matplotlib pillow numpy
python scripts/generate_readme_figures.py
```

Requires `data/dataset_images/` with `CN`, `MCI`, and `AD` folders (any split). Full EDA plots are in [`notebooks/preprocessing/eda-adni.ipynb`](../../notebooks/preprocessing/eda-adni.ipynb).

## Files

| File | Description |
|------|-------------|
| `eda-class-distribution.png` | Slice counts per diagnostic class |
| `samples-stages-cn-mci-ad.png` | Example CN / MCI / AD axial slices |
| `liquid-finder-concept.png` | Liquid Finder Z-selection concept |
| `pipeline-brain-stages.png` | Slice → crop → model → XAI flow |
| `pipeline-stages-slices.png` | CN / MCI / AD inputs side by side |
