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
    binsize = np.zeros(len(pts) - 1)
    for i in range(len(pts) - 1):
        pt_center[i] = (pts[i + 1] + pts[i]) / 2
        binsize[i] =(pts[i + 1] - pts[i])/2
    plt.errorbar(
        pt_center,
        rates_dict["Tight"]["rate"],
        rates_dict["Tight"]["unc"],
        xerr=binsize,
        marker=".",
        linestyle="",
        markersize="7",
    )
    plt.grid()
    #plt.ylim(0, 0.0224)
    plt.ylabel(r"jet $\rightarrow \mathrm{e}$ fake rate")
    plt.xlabel(r"$\mathrm{p_{T}} (\mathrm{e})\, (\mathrm{GeV})$")
    plt.savefig(
        "{plot_output}/jet_to_ele_fakerates.png".format(plot_output=plot_output)
    )
    plt.close()


def base_file(base_path):
    base_file = R.TFile(
        base_path + "/id_wp_ele_Loose.root",
        "READ",
    )
    return base_file


def rates(shapes, base_path):
    rates_dict = {
        "Tight": {"pt": [], "rate": [], "unc": []},
    }
    procs_to_subtract = {
        "ggzz": "ggZZ#mme-VV#Nominal#pt_3",
        "zz": "ZZ#mme-VV#Nominal#pt_3",
        "wz": "WZ#mme-VV#Nominal#pt_3",
        "zzz": "ZZZ#mme-ZZZ#Nominal#pt_3",
        "www": "WWW#mme-WWW#Nominal#pt_3",
        "wwz": "WWZ#mme-WWZ#Nominal#pt_3",
        "wzz": "WZZ#mme-WZZ#Nominal#pt_3",
        "rem_vh": "rem_VH#mme-VH#Nominal#pt_3",
        "rem_ttbar": "rem_ttbar#mme-TT#Nominal#pt_3",
    }
    for shape in shapes:
        if "id_wp_ele_Tight" in shape:
            tight_file = R.TFile(shape, "READ")
            tight_data = tight_file.Get("data#mme#Nominal#pt_3")
            tight_diff = tight_data.Clone()
            base = base_file(base_path)
            base_data = base.Get("data#mme#Nominal#pt_3")
            base_diff = base_data.Clone()
            for proc in procs_to_subtract.values():
                tight_hist = tight_file.Get(proc)
                base_hist = base.Get(proc)
                tight_diff.Add(tight_hist, -1)
                base_diff.Add(base_hist, -1)
            ratio_hist = tight_diff.Clone()
            ratio_hist.Divide(base_diff)
            for bin_i in range(1, tight_data.GetNbinsX() + 1):
                rates_dict["Tight"]["rate"].append(ratio_hist.GetBinContent(bin_i))
                rates_dict["Tight"]["unc"].append(ratio_hist.GetBinError(bin_i))
                rates_dict["Tight"]["pt"].append(tight_data.GetBinLowEdge(bin_i))
            rates_dict["Tight"]["pt"].append(
                tight_data.GetBinLowEdge(tight_data.GetNbinsX() + 1)
            )
            base.Close()
            del base_data
            del base_diff
            del ratio_hist
            tight_file.Close()
            del tight_data
            del tight_diff
    return rates_dict


def correction_lib_format(rates_dict):
    corr_lib = {
        "schema_version": 2,
        "corrections": [
            {
                "name": "jet_to_lep_fakerate",
                "description": "rates to estimate the contribution from jets that fake electrons",
                "version": 0,
                "inputs": [
                    {
                        "name": "id_wp_ele",
                        "type": "string",
                        "description": "Loose for no WP and iso and Tight for medium WP and iso<0.15",
                    },
                    {
                        "name": "pt",
                        "type": "real",
                        "description": "Reconstructed electron pT",
                    },
                ],
                "output": {
                    "name": "rate",
                    "type": "real",
                    "description": "pT-dependent rate",
                },
                "data": {
                    "nodetype": "category",
                    "input": "id_wp_ele",
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
