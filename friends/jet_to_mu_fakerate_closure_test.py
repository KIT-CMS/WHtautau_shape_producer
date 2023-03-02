import ROOT as R
import argparse
import os
import glob
import numpy as np
import json
import matplotlib.pyplot as plt


def parse_arguments():
    parser = argparse.ArgumentParser(description="Shape comparison.")
    parser.add_argument(
        "-base",
        "--base_path",
        type=str,
        required=True,
        help="Input root file of sig region.",
    )
    parser.add_argument(
        "-out",
        "--output_file",
        type=str,
        required=True,
        help="output json",
    )
    parser.add_argument(
        "--plot_output",
        type=str,
        required=True,
        help="plot of rates",
    )
    return parser.parse_args()


def plot_rates(rates_dict, plot_output):
    pts = rates_dict["Tight"]["pt"]
    pt_center = np.zeros(len(pts) - 1)
    for i in range(len(pts) - 1):
        pt_center[i] = (pts[i + 1] + pts[i]) / 2
    plt.errorbar(
        pt_center,
        rates_dict["Tight"]["rate"],
        rates_dict["Tight"]["unc"],
        marker=".",
        linestyle="",
        markersize="7",
    )
    plt.ylim(0, 0.06)
    plt.ylabel(r"jet $\rightarrow\mu$ fake rate")
    plt.xlabel(r"$\mathrm{p_{T}}(\mu)\, (\mathrm{GeV})$")
    plt.savefig("{plot_output}/jet_to_mu_fakerates.png".format(plot_output=plot_output))
    plt.close()


def base_file(base_path):
    base_file = R.TFile(
        base_path + "/id_wp_mu_Loose.root",
        "READ",
    )
    return base_file


def rates(shapes, base_path):
    rates_dict = {
        "Tight": {"pt": [], "rate": [], "unc": []},
    }
    # base proc in closure test is the ttbar shape
    base_proc = "TT#eem-TT#Nominal#pt_3"
    procs_to_add = {
        "wjets": "Wjets#eem-W#Nominal#pt_3",
        "dy": "DY#eem-DY#Nominal#pt_3",
        "rem_vv": "rem_VV#eem-VV#Nominal#pt_3",
    }
    for shape in shapes:
        if not "Loose" in shape:
            tight_file = R.TFile(shape, "READ")
            tight = tight_file.Get(base_proc)
            tight_diff = tight.Clone()
            base = base_file(base_path)
            base_tt = base.Get(base_proc)
            base_diff = base_tt.Clone()
            for proc in procs_to_add.values():
                tight_hist = tight_file.Get(proc)
                base_hist = base.Get(proc)
                tight_diff.Add(tight_hist, 1)
                base_diff.Add(base_hist, 1)
            ratio_hist = tight_diff.Clone()
            ratio_hist.Divide(base_diff)
            for bin_i in range(1, tight.GetNbinsX() + 1):
                rates_dict["Tight"]["rate"].append(ratio_hist.GetBinContent(bin_i))
                rates_dict["Tight"]["unc"].append(ratio_hist.GetBinError(bin_i))
                rates_dict["Tight"]["pt"].append(tight.GetBinLowEdge(bin_i))
            rates_dict["Tight"]["pt"].append(tight.GetBinLowEdge(tight.GetNbinsX() + 1))
            base.Close()
            del base_tt
            del base_diff
            del ratio_hist
            tight_file.Close()
            del tight
            del tight_diff
    return rates_dict


def correction_lib_format(rates_dict):
    corr_lib = {
        "schema_version": 2,
        "corrections": [
            {
                "name": "jet_to_lep_fakerate",
                "description": "rates to estimate the contribution from jets that fake muons",
                "version": 0,
                "inputs": [
                    {
                        "name": "id_wp_mu",
                        "type": "string",
                        "description": "Loose for no WP and iso and Tight for medium WP and iso<0.15",
                    },
                    {
                        "name": "pt",
                        "type": "real",
                        "description": "Reconstructed muon pT",
                    },
                ],
                "output": {
                    "name": "rate",
                    "type": "real",
                    "description": "pT-dependent rate",
                },
                "data": {
                    "nodetype": "category",
                    "input": "id_wp_mu",
                    "content": [
                        {
                            "key": "Tight",
                            "value": {
                                "nodetype": "binning",
                                "input": "pt",
                                "edges": rates_dict["Tight"]["pt"],
                                "content": rates_dict["Tight"]["rate"],
                                "flow": "clamp",
                            },
                        },
                    ],
                },
            },
        ],
    }
    return corr_lib


def main(shapes, base_path, output_file, plot_output):
    rates_dict = rates(shapes, base_path)
    print(rates_dict)
    plot_rates(rates_dict, plot_output)
    with open("{output}".format(output=output_file), "w") as outfile:
        json.dump(correction_lib_format(rates_dict), outfile)


if __name__ == "__main__":
    args = parse_arguments()
    base_path = args.base_path
    output_file = args.output_file
    plot_output = args.plot_output
    path = os.path.join(base_path, "*.root")
    shapes = glob.glob(path)
    main(shapes, base_path, output_file, plot_output)
