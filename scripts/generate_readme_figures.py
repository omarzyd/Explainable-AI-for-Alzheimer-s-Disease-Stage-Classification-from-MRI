"""Generate README figures from local ADNI slice data (if present)."""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "dataset_images"
OUT = ROOT / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

CLASSES = ["CN", "MCI", "AD"]
COLORS = {"CN": "#34d399", "MCI": "#fbbf24", "AD": "#f87171"}


def find_sample(split: str, label: str) -> Path | None:
    base = DATA / split / label
    if not base.exists():
        return None
    for p in sorted(base.rglob("*.png")):
        return p
    return None


def load_rgb(path: Path, size: int = 224) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    return np.asarray(img)


def save_fig(name: str):
    path = OUT / name
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="#0f172a", edgecolor="none")
    plt.close()
    print("wrote", path)


def fig_class_distribution():
    counts = {}
    for split in ("train", "val"):
        for c in CLASSES:
            d = DATA / split / c
            if d.exists():
                n = sum(1 for _ in d.rglob("*.png"))
                counts.setdefault(c, 0)
                counts[c] += n

    if not counts:
        return False

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#1e293b")
    labels = list(counts.keys())
    vals = [counts[k] for k in labels]
    bars = ax.bar(labels, vals, color=[COLORS[k] for k in labels], edgecolor="white", linewidth=0.6)
    ax.set_ylabel("Axial slices", color="#e2e8f0")
    ax.set_title("ADNI preprocessed cohort — class distribution (local sample)", color="#f8fafc", fontsize=13, pad=12)
    ax.tick_params(colors="#94a3b8")
    for spine in ax.spines.values():
        spine.set_color("#475569")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + max(vals) * 0.02, str(v), ha="center", color="#e2e8f0", fontsize=10)
    save_fig("eda-class-distribution.png")
    return True


def fig_stages_panel():
    imgs = {}
    for c in CLASSES:
        p = find_sample("val", c) or find_sample("train", c)
        if p:
            imgs[c] = (load_rgb(p), p.name)

    if len(imgs) < 2:
        return False

    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    fig.patch.set_facecolor("#0f172a")
    for ax, c in zip(axes, CLASSES):
        ax.set_facecolor("#0f172a")
        if c in imgs:
            arr, fname = imgs[c]
            ax.imshow(arr)
            ax.set_title(f"{c}\n{fname}", color=COLORS[c], fontsize=12, fontweight="bold")
        else:
            ax.text(0.5, 0.5, "N/A", ha="center", va="center", color="#64748b", transform=ax.transAxes)
            ax.set_title(c, color=COLORS[c])
        ax.axis("off")
    fig.suptitle("Representative axial slices (224×224) — disease stages", color="#f8fafc", fontsize=14, y=1.02)
    plt.tight_layout()
    save_fig("samples-stages-cn-mci-ad.png")
    return True


def fig_liquid_finder():
    """Concept diagram: volume → CSF profile → Z-window → ventricular slice."""
    fig = plt.figure(figsize=(12, 4.2))
    fig.patch.set_facecolor("#0f172a")

    # Panel 1: schematic axial stack
    ax1 = fig.add_subplot(1, 4, 1)
    ax1.set_facecolor("#0f172a")
    ax1.set_title("1. NIfTI volume", color="#f8fafc", fontsize=11)
    for i, alpha in enumerate(np.linspace(0.15, 0.9, 8)):
        circ = plt.Circle((0.5, 0.15 + i * 0.09), 0.32 - i * 0.02, color="#64748b", alpha=alpha)
        ax1.add_patch(circ)
    ax1.annotate("Z slices", xy=(0.85, 0.5), color="#94a3b8", fontsize=9)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis("off")

    # Panel 2: CSF signal profile
    ax2 = fig.add_subplot(1, 4, 2)
    ax2.set_facecolor("#1e293b")
    z = np.linspace(0, 1, 120)
    csf = np.exp(-((z - 0.48) ** 2) / 0.012) + 0.3 * np.exp(-((z - 0.52) ** 2) / 0.008)
    ax2.fill_between(z, csf, color="#38bdf8", alpha=0.5)
    ax2.plot(z, csf, color="#7dd3fc", lw=2)
    ax2.axvspan(0.42, 0.58, color="#34d399", alpha=0.2, label="Liquid Finder window")
    ax2.set_title("2. CSF-guided Z profile", color="#f8fafc", fontsize=11)
    ax2.set_xlabel("Inferior → Superior", color="#94a3b8", fontsize=9)
    ax2.tick_params(colors="#94a3b8", labelsize=8)
    for spine in ax2.spines.values():
        spine.set_color("#475569")

    # Panel 3: use real MCI slice if available
    ax3 = fig.add_subplot(1, 4, 3)
    ax3.set_facecolor("#0f172a")
    p = find_sample("val", "MCI") or find_sample("train", "MCI")
    if p:
        ax3.imshow(load_rgb(p))
    ax3.set_title("3. Selected axial slice\n(ventricular level)", color="#f8fafc", fontsize=11)
    ax3.axis("off")

    # Panel 4: crop focus
    ax4 = fig.add_subplot(1, 4, 4)
    ax4.set_facecolor("#0f172a")
    if p:
        arr = load_rgb(p)
        h, w = arr.shape[:2]
        ch, cw = h // 4, w // 4
        crop = arr[ch : h - ch, cw : w - cw]
        ax4.imshow(crop)
        rect = mpatches.Rectangle((cw, ch), w - 2 * cw, h - 2 * ch, fill=False, edgecolor="#34d399", lw=2)
        ax4.add_patch(rect)
    ax4.set_title("4. Anatomical crop\n(periventricular ROI)", color="#f8fafc", fontsize=11)
    ax4.axis("off")

    fig.suptitle("Liquid Finder — CSF-guided Z-axis selection for ventricular slices", color="#e2e8f0", fontsize=13, y=1.05)
    plt.tight_layout()
    save_fig("liquid-finder-concept.png")
    return True


def fig_pipeline_montage():
    by_class = {}
    for c in CLASSES:
        p = find_sample("val", c) or find_sample("train", c)
        if p:
            by_class[c] = load_rgb(p)

    if len(by_class) < 2:
        return False

    ref = by_class["MCI"] if "MCI" in by_class else next(iter(by_class.values()))
    fig, axes = plt.subplots(2, 3, figsize=(11, 7))
    fig.patch.set_facecolor("#0f172a")
    titles = [
        "ADNI axial slice",
        "Liquid Finder crop",
        "CNN features",
        "Patient-level OvA",
        "Grad-CAM overlay",
        "XAI validation",
    ]
    for ax, title in zip(axes.flat, titles):
        ax.set_facecolor("#0f172a")
        arr = ref.copy()
        if "crop" in title.lower():
            h, w = arr.shape[:2]
            ch, cw = h // 5, w // 5
            arr = arr[ch : h - ch, cw : w - cw]
        ax.imshow(arr)
        if "Grad" in title:
            h, w = arr.shape[:2]
            yy, xx = np.mgrid[0:h, 0:w]
            cy, cx = h / 2, w / 2
            heat = np.exp(-((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * (h / 4.5) ** 2))
            ax.imshow(heat, cmap="hot", alpha=0.42)
        ax.set_title(title, color="#e2e8f0", fontsize=10)
        ax.axis("off")

    fig.suptitle("From MRI slice to explainable prediction", color="#f8fafc", fontsize=14)
    plt.tight_layout()
    save_fig("pipeline-brain-stages.png")

    # Second row: one panel per stage class
    fig2, axes2 = plt.subplots(1, 3, figsize=(11, 3.8))
    fig2.patch.set_facecolor("#0f172a")
    for ax, c in zip(axes2, CLASSES):
        ax.set_facecolor("#0f172a")
        if c in by_class:
            ax.imshow(by_class[c])
        ax.set_title(c, color=COLORS[c], fontsize=13, fontweight="bold")
        ax.axis("off")
    fig2.suptitle("Pipeline inputs by diagnostic stage", color="#f8fafc", fontsize=13)
    plt.tight_layout()
    save_fig("pipeline-stages-slices.png")
    return True


def main():
    if not DATA.exists():
        print("No data/dataset_images — skipping figure generation")
        return
    ok = [
        fig_class_distribution(),
        fig_stages_panel(),
        fig_liquid_finder(),
        fig_pipeline_montage(),
    ]
    print("done:", sum(ok), "figures")


if __name__ == "__main__":
    main()
