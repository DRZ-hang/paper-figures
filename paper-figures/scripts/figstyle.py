#!/usr/bin/env python3
"""figstyle.py — apply a journal preset to matplotlib and export figures consistently.

Used by the `paper-figures` skill so every figure in a paper shares one style and
exports at the journal's required size / resolution / format.

Quick use inside a plotting script
-----------------------------------
    from figstyle import apply_preset, save_figure
    apply_preset("nature", column="single")   # sets size, fonts, dpi, line widths
    fig, ax = plt.subplots()
    ...
    save_figure(fig, number="1", preset="nature")   # -> figures/Fig1.pdf + Fig1.png

CLI
---
    python figstyle.py --list                 # show available presets
    python figstyle.py --show nature          # print one preset's settings

Presets live in ../assets/presets.json (edit/add journals there). Widths are in mm,
fonts in points. Bundled journal presets are starting points — verify against the
journal's current author guidelines before final submission.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

MM_PER_INCH = 25.4
_PRESETS_PATH = Path(__file__).resolve().parent.parent / "assets" / "presets.json"


def _load() -> dict:
    with open(_PRESETS_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def list_presets() -> dict:
    """Return {name: label} for every preset."""
    data = _load()
    return {name: spec.get("label", "") for name, spec in data["presets"].items()}


def get_preset(name: str) -> dict:
    data = _load()
    presets = data["presets"]
    if name not in presets:
        raise KeyError(
            f"Unknown preset '{name}'. Available: {', '.join(presets)}. "
            f"Add it to {_PRESETS_PATH}."
        )
    spec = dict(presets[name])
    # resolve palette name -> list of hex colors
    pal = spec.get("palette")
    if isinstance(pal, str):
        spec["palette_colors"] = data.get("palettes", {}).get(pal, [])
    return spec


def apply_preset(name: str = "generic", column: str = "single", aspect: float = 0.72):
    """Configure matplotlib rcParams from a preset. Returns the spec dict.

    column: "single" | "onehalf" | "double" — sets default figure width to that
            column width (mm). aspect = height/width for the default figure size;
            override by passing figsize to plt.subplots() afterwards.
    """
    import matplotlib as mpl
    import matplotlib.pyplot as plt  # noqa: F401  (ensures backend init)

    spec = get_preset(name)
    width_mm = spec["widths_mm"].get(column, spec["widths_mm"]["single"])
    width_in = width_mm / MM_PER_INCH
    height_in = width_in * aspect

    rc = {
        "figure.figsize": (width_in, height_in),
        "figure.dpi": 150,  # screen preview; export dpi handled in save_figure
        "savefig.dpi": spec["dpi_raster"],
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "font.family": spec["font_family"],
        "font.size": spec["font_size_pt"],
        "axes.labelsize": spec["axes_label_pt"],
        "axes.titlesize": spec["title_pt"],
        "xtick.labelsize": spec["tick_label_pt"],
        "ytick.labelsize": spec["tick_label_pt"],
        "legend.fontsize": spec["tick_label_pt"],
        "lines.linewidth": spec["line_width_pt"],
        "axes.linewidth": spec["axes_line_width_pt"],
        "xtick.major.width": spec["axes_line_width_pt"],
        "ytick.major.width": spec["axes_line_width_pt"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        # Keep text editable + embedded in PDF/PS (TrueType type 42).
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "figure.constrained_layout.use": True,
    }
    mpl.rcParams.update(rc)

    colors = spec.get("palette_colors")
    if colors:
        mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=colors)

    return spec


def save_figure(fig, number, preset: str = "generic", outdir: str = "figures",
                kind: str = "raster", formats=None, prefix: str = "Fig"):
    """Save a figure at the preset's resolution/formats with consistent naming.

    number: figure number, e.g. "1" or "S1" -> Fig1.* / FigS1.*
    kind:   "raster" (photos/heatmaps -> dpi_raster) or "line" (line art -> dpi_line_art)
    formats: override the preset's export_formats, e.g. ["pdf", "png"]
    Returns the list of written paths.
    """
    spec = get_preset(preset)
    Path(outdir).mkdir(parents=True, exist_ok=True)
    dpi = spec["dpi_line_art"] if kind == "line" else spec["dpi_raster"]
    fmts = formats if formats is not None else spec["export_formats"]

    written = []
    base = f"{prefix}{number}"
    for fmt in fmts:
        path = os.path.join(outdir, f"{base}.{fmt}")
        save_dpi = dpi if fmt in ("png", "tiff", "tif", "jpg", "jpeg") else None
        fig.savefig(path, dpi=save_dpi, bbox_inches="tight", pad_inches=0.02)
        written.append(path)
        print(f"[figstyle] wrote {path}" + (f" @ {save_dpi} dpi" if save_dpi else " (vector)"))
    return written


def _cli():
    p = argparse.ArgumentParser(description="Inspect paper-figures journal presets.")
    p.add_argument("--list", action="store_true", help="list available presets")
    p.add_argument("--show", metavar="NAME", help="print one preset's settings")
    args = p.parse_args()

    if args.show:
        print(json.dumps(get_preset(args.show), indent=2, ensure_ascii=False))
    else:  # default to listing
        print("Available presets (edit assets/presets.json to add/modify):\n")
        for name, label in list_presets().items():
            print(f"  {name:<10} {label}")
        print("\nUse: apply_preset('<name>', column='single'|'onehalf'|'double')")


if __name__ == "__main__":
    _cli()
