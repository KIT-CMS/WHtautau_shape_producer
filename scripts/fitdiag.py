import ROOT
import csv

# Open the ROOT file


def correlations():
    f = ROOT.TFile("fitDiagnostics.Test_incl_llt_alleras.root")
    corr_hist = f.Get(
        "fit_b"
    ).correlationHist()  # Use "fit_s" for signal+background fit

    # Collect all non-diagonal correlations
    correlations = []
    nbins = corr_hist.GetNbinsX()

    for i in range(1, nbins + 1):
        for j in range(
            i + 1, nbins + 1
        ):  # j > i to avoid double counting and skip diagonal
            param1 = corr_hist.GetXaxis().GetBinLabel(i)
            param2 = corr_hist.GetYaxis().GetBinLabel(j)
            value = corr_hist.GetBinContent(i, j)
            correlations.append((param1, param2, value))

    # Sort by absolute correlation value, descending
    correlations.sort(key=lambda x: abs(x[2]), reverse=True)
    top_50 = correlations[:300]
    # Print the top correlations
    for param1, param2, value in top_50:
        print(f"{param1} vs {param2}: correlation = {value:.3f}")


def pre_postfitunc():
    f = ROOT.TFile("fitDiagnostics.Test_incl_llt_alleras.root")
    output_csv = "nuisance_summary.csv"
    use_signal_fit = True  # True = fit_s, False = fit_b

    # Get fit results
    fit = f.Get("fit_s") if use_signal_fit else f.Get("fit_b")

    # Load prefit nuisances
    prefit_dir = f.Get("norm_prefit") or f.Get("shapes_prefit")
    if not prefit_dir:
        raise RuntimeError(
            "Prefit information not found in 'norm_prefit' or 'shapes_prefit'."
        )

    # Load parameter list
    params = fit.floatParsFinal()
    n_params = params.getSize()

    # === COLLECT RESULTS ===
    results = []

    for i in range(n_params):
        post = params.at(i)
        name = post.GetName()
        post_val = post.getVal()
        post_err = post.getError()

        # Default prefit (usually 0 ± 1 for nuisances)
        pre_val = 0.0
        pre_err = 1.0

        # Try to get from the prefit shapes/norms (some nuisances may be missing)
        if f.Get("prefit"):
            prefit_params = f.Get("prefit").floatParsFinal()
            for j in range(prefit_params.getSize()):
                pre = prefit_params.at(j)
                if pre.GetName() == name:
                    pre_val = pre.getVal()
                    pre_err = pre.getError()
                    break

        results.append(
            {
                "name": name,
                "prefit_val": pre_val,
                "prefit_err": pre_err,
                "postfit_val": post_val,
                "postfit_err": post_err,
            }
        )

    # === PRINT TO TERMINAL ===
    for r in results:
        print(f"{r['name']}:")
        print(f"  Prefit:  {r['prefit_val']:.3f} ± {r['prefit_err']:.3f}")
        print(f"  Postfit: {r['postfit_val']:.3f} ± {r['postfit_err']:.3f}")
        print()

    # === SAVE TO CSV ===
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Parameter",
                "Prefit Value",
                "Prefit Error",
                "Postfit Value",
                "Postfit Error",
            ]
        )
        for r in results:
            writer.writerow(
                [
                    r["name"],
                    f"{r['prefit_val']:.3f}",
                    f"{r['prefit_err']:.3f}",
                    f"{r['postfit_val']:.3f}",
                    f"{r['postfit_err']:.3f}",
                ]
            )

    print(f"\n✅ Saved results to: {output_csv}")


pre_postfitunc()
