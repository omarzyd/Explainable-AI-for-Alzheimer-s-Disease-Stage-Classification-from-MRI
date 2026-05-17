# Data directory

Optional local ADNI slice cache for reproducing *Zayed et al. (2026)*. The full preprocessed cohort is obtained via Kaggle or `gdown` as described in the [reproducibility runbook](../docs/PIPELINE.md).

## Recommended sources

| Source | Use |
|--------|-----|
| [Kaggle — Alzheimer's multiclass (augmented)](https://www.kaggle.com/datasets/aryansinghal10/alzheimers-multiclass-dataset-equal-and-augmented) | Public training images |
| ADNI `adni_nifti_preprocessed` | Private Kaggle dataset or `gdown` in notebook setup cells |

## Layout (when present locally)

```
data/dataset_images/
├── train/
│   ├── CN/
│   ├── MCI/
│   └── AD/
└── test/   (if applicable)
```

Patient folders contain axial slices extracted from NIfTI volumes (`*_z###.png`).

> Large binaries are listed in `.gitignore`. Clone the Kaggle datasets above if this folder is empty.
