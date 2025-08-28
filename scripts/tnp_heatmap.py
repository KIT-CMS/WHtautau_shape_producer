#!/usr/bin/env python3
# make_heatmaps.py
import json
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # <--- add this line
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def pick_category_value(category_node, key="mc"):
    """category_node["content"] is a list of {"key": ..., "value": ...} dicts."""
    for kv in category_node.get("content", []):
        if kv.get("key") == key:
            return float(kv.get("value"))
    raise KeyError(f'Key "{key}" not found in category node.')

def extract_matrix(corr_obj, key="mc"):
    """
    Extract (pt_edges, eta_edges, matrix) for a correction that is binned in pt -> abs(eta) -> category(type).
    Returns:
        pt_edges: 1D list of bin edges along pT (GeV)
        eta_edges: 1D list of |eta| bin edges
        Z: 2D np.array with shape (n_pt_bins, n_eta_bins)
             Rows correspond to pt bins (low->high), columns to eta bins (low->high).
    """
    data = corr_obj["data"]
    assert data["nodetype"] == "binning" and data["input"] == "pt", "Unexpected structure at top-level."
    pt_edges = data["edges"]
    pt_bins = data["content"]
    # Peek inside first pt bin to get eta edges
    first_eta = pt_bins[0]
    assert first_eta["nodetype"] == "binning" and first_eta["input"] == "abs(eta)"
    eta_edges = first_eta["edges"]

    n_pt = len(pt_edges) - 1
    n_eta = len(eta_edges) - 1
    Z = np.zeros((n_pt, n_eta), dtype=float)

    # Loop over pt bins
    for i_pt, eta_block in enumerate(pt_bins):
        assert eta_block["nodetype"] == "binning" and eta_block["input"] == "abs(eta)"
        eta_contents = eta_block["content"]
        if len(eta_contents) != n_eta:
            raise ValueError("Inconsistent number of eta bins.")
        # Loop over eta bins
        for j_eta, cat_node in enumerate(eta_contents):
            assert cat_node["nodetype"] == "category" and cat_node["input"] == "type"
            Z[i_pt, j_eta] = pick_category_value(cat_node, key=key)

    return pt_edges, eta_edges, Z

def plot_heatmap(pt_edges, eta_edges, Z, title, out_path, annotate=False):
    """
    Plot Z on a uniform grid: each cell is same size (indices), axes labeled by real bin edges.
    """
    n_pt, n_eta = Z.shape

    fig, ax = plt.subplots(figsize=(7.8, 5.6))
    im = ax.imshow(Z, origin="lower", aspect="auto", interpolation="nearest")

    # Fix bounds to avoid negative tick values from pixel half-edges
    ax.set_xlim(-0.5, n_eta - 0.5)
    ax.set_ylim(-0.5, n_pt  - 0.5)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("SF")

    # Label axes with *edges* so the rightmost/topmost edges are shown
    # X (|eta|) bin boundaries
    ax.set_xticks(np.arange(n_eta + 1) - 0.5)
    ax.set_xticklabels([f"{e:.1f}" for e in eta_edges], rotation=0)
    ax.set_xlabel(r"$|\eta|$")

    # Y (pT) bin boundaries
    ax.set_yticks(np.arange(n_pt + 1) - 0.5)
    ax.set_yticklabels([f"{e:.0f}" for e in pt_edges])
    ax.set_ylabel(r"$p_{\mathrm{T}}$ (GeV)")

   # ax.set_title(title)

    # Gridlines on bin boundaries
    ax.grid(which="both", axis="both", linestyle="-", linewidth=0.5, color="w")
    ax.tick_params(which="both", length=0)

    # Optional per-cell annotations at centers
    if annotate:
        for i in range(n_pt):
            for j in range(n_eta):
                ax.text(j, i, f"{Z[i, j]:.3g}", ha="center", va="center", fontsize=7)

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)



def main():
    parser = argparse.ArgumentParser(description="Make pT–|eta| heatmaps from correction JSON.")
    parser.add_argument("--json_path",default=None, help="Path to the JSON file you pasted (schema_version=2).")
    parser.add_argument("--key", default="mc", choices=["mc", "emb"], help="Which category to plot.")
    parser.add_argument("--only", default=None, help="Optional: plot only this correction name (exact match).")
    parser.add_argument("--annotate", action="store_true", help="Write numbers into each bin.")
    parser.add_argument("--outdir", default="heatmaps", help="Output directory for PNGs.")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    with open(args.json_path, "r") as f:
        payload = json.load(f)

    corrections = payload.get("corrections", [])
    if not corrections:
        raise ValueError("No 'corrections' found in JSON.")

    made_any = False
    for corr in corrections:
        name = corr.get("name", "unnamed")
        if args.only and name != args.only:
            continue

        # Only handle the (pt -> |eta| -> category(type)) layout
        try:
            pt_edges, eta_edges, Z = extract_matrix(corr, key=args.key)
        except Exception as e:
            # Skip corrections that don’t match the expected layout
            print(f"Skipping '{name}' ({e})")
            continue

        title = f"{name} — {args.key}"
        out_path = outdir / f"{name}_{args.key}.pdf"
        plot_heatmap(pt_edges, eta_edges, Z, title, out_path, annotate=args.annotate)
        print(f"Saved: {out_path}")
        made_any = True

    if not made_any:
        raise SystemExit("No matching corrections were plotted. Try without --only or inspect structure.")

if __name__ == "__main__":
    main()
