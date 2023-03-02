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


# returns working points of vsjets, vsmu, vsele in this order
def working_points(shape):
    base = os.path.basename(shape)
    wps = base.split("__")[:-1]
    jet_wp = wps[0]
    mu_wp = wps[1]
    ele_wp = wps[2]
    return [jet_wp, mu_wp, ele_wp]


def plot_rates(rates_dict, plot_output):
    for dm in ["DM0", "DM1", "DM10", "DM11"]:
        pts = rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["VLoose_vs_ele"][dm]["pt"]
        pt_center = np.zeros(len(pts) - 1)
        for i in range(len(pts) - 1):
            pt_center[i] = (pts[i + 1] + pts[i]) / 2
        plt.errorbar(
            pt_center,
            rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["Tight_vs_ele"][dm]["rate"],
            rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["Tight_vs_ele"][dm]["unc"],
            marker=".",
            linestyle="",
            markersize="7",
            label="TightvsMu+TightvsEle",
        )
        plt.errorbar(
            pt_center,
            rates_dict["VTight_vs_jets"]["VLoose_vs_mu"]["Tight_vs_ele"][dm]["rate"],
            rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["Tight_vs_ele"][dm]["unc"],
            marker=".",
            linestyle="",
            markersize="7",
            label="VLoosevsMu+TightvsEle",
        )
        plt.errorbar(
            pt_center,
            rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["VLoose_vs_ele"][dm]["rate"],
            rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["Tight_vs_ele"][dm]["unc"],
            marker=".",
            linestyle="",
            markersize="7",
            label="TightvsMu+VLoosevsEle",
        )
        plt.legend()
        plt.ylim(0, 0.15)
        plt.ylabel(r"jet $\rightarrow\tau_{\mathrm{h}}$ fake rate")
        plt.xlabel(r"$\mathrm{p_{T}}(\tau_{\mathrm{h}})\, (\mathrm{GeV})$")
        plt.savefig("{plot_output}/{dm}.png".format(plot_output=plot_output, dm=dm))
        plt.close()


def base_file(base_path, working_points, decay_mode):
    wp_vs_mu = working_points[1]
    wp_vs_ele = working_points[2]
    base_file = R.TFile(
        base_path
        + "/VVVLoose_vs_jets__{vs_mu}__{vs_ele}__{DM}.root".format(
            vs_mu=wp_vs_mu, vs_ele=wp_vs_ele, DM=decay_mode
        ),
        "READ",
    )
    return base_file


def rates(shapes, base_path):
    rates_dict = {
        "VTight_vs_jets": {
            "Tight_vs_mu": {
                "Tight_vs_ele": {
                    "DM0": {"pt": [], "rate": [], "unc": []},
                    "DM1": {"pt": [], "rate": [], "unc": []},
                    "DM10": {"pt": [], "rate": [], "unc": []},
                    "DM11": {"pt": [], "rate": [], "unc": []},
                },
                "VLoose_vs_ele": {
                    "DM0": {"pt": [], "rate": [], "unc": []},
                    "DM1": {"pt": [], "rate": [], "unc": []},
                    "DM10": {"pt": [], "rate": [], "unc": []},
                    "DM11": {"pt": [], "rate": [], "unc": []},
                },
            },
            "VLoose_vs_mu": {
                "Tight_vs_ele": {
                    "DM0": {"pt": [], "rate": [], "unc": []},
                    "DM1": {"pt": [], "rate": [], "unc": []},
                    "DM10": {"pt": [], "rate": [], "unc": []},
                    "DM11": {"pt": [], "rate": [], "unc": []},
                },
            },
        }
    }
    # base proc in closure test is the ttbar shape
    base_proc = "TT#mmt-TT#Nominal#pt_3"
    procs_to_add = {
        "wjets": "Wjets#mmt-W#Nominal#pt_3",
        "dy": "DY#mmt-DY#Nominal#pt_3",
        "rem_vv": "rem_VV#mmt-VV#Nominal#pt_3",
    }
    for shape in shapes:
        if not "VVVLoose_vs_jets" in shape:
            wp = working_points(shape)
            tight_file = R.TFile(shape, "READ")
            tight = tight_file.Get(base_proc)
            tight_diff = tight.Clone()
            if "DM0." in shape:
                base_DM0 = base_file(base_path, wp, "DM0")
                base = base_DM0.Get(base_proc)
                base_diff = base.Clone()
                for proc in procs_to_add.values():
                    tight_hist = tight_file.Get(proc)
                    base_hist = base_DM0.Get(proc)
                    tight_diff.Add(tight_hist, 1)
                    base_diff.Add(base_hist, 1)
                ratio_hist = tight_diff.Clone()
                ratio_hist.Divide(base_diff)
                for bin_i in range(1, tight.GetNbinsX() + 1):
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["rate"].append(
                        ratio_hist.GetBinContent(bin_i)
                    )
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["unc"].append(
                        ratio_hist.GetBinError(bin_i)
                    )
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["pt"].append(
                        tight.GetBinLowEdge(bin_i)
                    )
                rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["pt"].append(
                    tight.GetBinLowEdge(tight.GetNbinsX() + 1)
                )
                base_DM0.Close()
                del base
                del base_diff
                del ratio_hist
            elif "DM1." in shape:
                base_DM1 = base_file(base_path, wp, "DM1")
                base = base_DM1.Get(base_proc)
                base_diff = base.Clone()
                for proc in procs_to_add.values():
                    tight_hist = tight_file.Get(proc)
                    base_hist = base_DM1.Get(proc)
                    tight_diff.Add(tight_hist, 1)
                    base_diff.Add(base_hist, 1)
                ratio_hist = tight_diff.Clone()
                ratio_hist.Divide(base_diff)
                for bin_i in range(1, tight.GetNbinsX() + 1):
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM1"]["rate"].append(
                        ratio_hist.GetBinContent(bin_i)
                    )
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM1"]["unc"].append(
                        ratio_hist.GetBinError(bin_i)
                    )
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM1"]["pt"].append(
                        tight.GetBinLowEdge(bin_i)
                    )
                rates_dict[wp[0]][wp[1]][wp[2]]["DM1"]["pt"].append(
                    tight.GetBinLowEdge(tight.GetNbinsX() + 1)
                )
                base_DM1.Close()
                del base
                del base_diff
                del ratio_hist
            elif "DM10" in shape:
                base_DM10 = base_file(base_path, wp, "DM10")
                base = base_DM10.Get(base_proc)
                base_diff = base.Clone()
                for proc in procs_to_add.values():
                    tight_hist = tight_file.Get(proc)
                    base_hist = base_DM10.Get(proc)
                    tight_diff.Add(tight_hist, 1)
                    base_diff.Add(base_hist, 1)
                ratio_hist = tight_diff.Clone()
                ratio_hist.Divide(base_diff)
                for bin_i in range(1, tight.GetNbinsX() + 1):
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM10"]["rate"].append(
                        ratio_hist.GetBinContent(bin_i)
                    )
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM10"]["unc"].append(
                        ratio_hist.GetBinError(bin_i)
                    )
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM10"]["pt"].append(
                        tight.GetBinLowEdge(bin_i)
                    )
                rates_dict[wp[0]][wp[1]][wp[2]]["DM10"]["pt"].append(
                    tight.GetBinLowEdge(tight.GetNbinsX() + 1)
                )
                base_DM10.Close()
                del base
                del base_diff
                del ratio_hist
            elif "DM11" in shape:
                base_DM11 = base_file(base_path, wp, "DM11")
                base = base_DM11.Get(base_proc)
                base_diff = base.Clone()
                for proc in procs_to_add.values():
                    tight_hist = tight_file.Get(proc)
                    base_hist = base_DM11.Get(proc)
                    tight_diff.Add(tight_hist, 1)
                    base_diff.Add(base_hist, 1)
                ratio_hist = tight_diff.Clone()
                ratio_hist.Divide(base_diff)
                for bin_i in range(1, tight.GetNbinsX() + 1):
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM11"]["rate"].append(
                        ratio_hist.GetBinContent(bin_i)
                    )
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM11"]["unc"].append(
                        ratio_hist.GetBinError(bin_i)
                    )
                    rates_dict[wp[0]][wp[1]][wp[2]]["DM11"]["pt"].append(
                        tight.GetBinLowEdge(bin_i)
                    )
                rates_dict[wp[0]][wp[1]][wp[2]]["DM11"]["pt"].append(
                    tight.GetBinLowEdge(tight.GetNbinsX() + 1)
                )
                base_DM11.Close()
                del base
                del base_diff
                del ratio_hist
            tight_file.Close()
            del tight
            del tight_diff
        # print(
        #     rates_dict,
        #     len(rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["pt"]),
        #     len(rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["rate"]),
        # )
    return rates_dict


def correction_lib_format(rates_dict):
    corr_lib = {
        "schema_version": 2,
        "corrections": [
            {
                "name": "jet_to_tau_fakerate",
                "description": "rate to estimate jet to hadronic tau fakes",
                "version": 0,
                "inputs": [
                    {
                        "name": "wp_vs_jets",
                        "type": "string",
                        "description": "DeepTau2017v2p1VSjets working point: VVVLoose-VVTight",
                    },
                    {
                        "name": "wp_vs_mu",
                        "type": "string",
                        "description": "DeepTau2017v2p1VSmu working point: VLoose-Tight",
                    },
                    {
                        "name": "wp_vs_ele",
                        "type": "string",
                        "description": "DeepTau2017v2p1VSe working point: VVLoose-VVTight",
                    },
                    {
                        "name": "dm",
                        "type": "int",
                        "description": "decay mode of hadronic tau",
                    },
                    {
                        "name": "pt",
                        "type": "real",
                        "description": "Reconstructed tau pT",
                    },
                ],
                "output": {
                    "name": "rate",
                    "type": "real",
                    "description": "DM-pT-dependent rate",
                },
                "data": {
                    "nodetype": "category",
                    "input": "wp_vs_jets",
                    "content": [
                        {
                            "key": "VTight",
                            "value": {
                                "nodetype": "category",
                                "input": "wp_vs_mu",
                                "content": [
                                    {
                                        "key": "Tight",
                                        "value": {
                                            "nodetype": "category",
                                            "input": "wp_vs_ele",
                                            "content": [
                                                {
                                                    "key": "Tight",
                                                    "value": {
                                                        "nodetype": "category",
                                                        "input": "dm",
                                                        "content": [
                                                            {
                                                                "key": 0,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["Tight_vs_mu"][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM0"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "Tight_vs_mu"
                                                                    ][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM0"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                            {
                                                                "key": 1,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["Tight_vs_mu"][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM1"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "Tight_vs_mu"
                                                                    ][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM1"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                            {
                                                                "key": 10,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["Tight_vs_mu"][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM10"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "Tight_vs_mu"
                                                                    ][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM10"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                            {
                                                                "key": 11,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["Tight_vs_mu"][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM11"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "Tight_vs_mu"
                                                                    ][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM11"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                        ],
                                                    },
                                                },
                                                {
                                                    "key": "VLoose",
                                                    "value": {
                                                        "nodetype": "category",
                                                        "input": "dm",
                                                        "content": [
                                                            {
                                                                "key": 0,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["Tight_vs_mu"][
                                                                        "VLoose_vs_ele"
                                                                    ][
                                                                        "DM0"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "Tight_vs_mu"
                                                                    ][
                                                                        "VLoose_vs_ele"
                                                                    ][
                                                                        "DM0"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                            {
                                                                "key": 1,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["Tight_vs_mu"][
                                                                        "VLoose_vs_ele"
                                                                    ][
                                                                        "DM1"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "Tight_vs_mu"
                                                                    ][
                                                                        "VLoose_vs_ele"
                                                                    ][
                                                                        "DM1"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                            {
                                                                "key": 10,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["Tight_vs_mu"][
                                                                        "VLoose_vs_ele"
                                                                    ][
                                                                        "DM10"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "Tight_vs_mu"
                                                                    ][
                                                                        "VLoose_vs_ele"
                                                                    ][
                                                                        "DM10"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                            {
                                                                "key": 11,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["Tight_vs_mu"][
                                                                        "VLoose_vs_ele"
                                                                    ][
                                                                        "DM11"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "Tight_vs_mu"
                                                                    ][
                                                                        "VLoose_vs_ele"
                                                                    ][
                                                                        "DM11"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                        ],
                                                    },
                                                },
                                            ],
                                        },
                                    },
                                    {
                                        "key": "VLoose",
                                        "value": {
                                            "nodetype": "category",
                                            "input": "wp_vs_ele",
                                            "content": [
                                                {
                                                    "key": "Tight",
                                                    "value": {
                                                        "nodetype": "category",
                                                        "input": "dm",
                                                        "content": [
                                                            {
                                                                "key": 0,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["VLoose_vs_mu"][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM0"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "VLoose_vs_mu"
                                                                    ][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM0"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                            {
                                                                "key": 1,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["VLoose_vs_mu"][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM1"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "VLoose_vs_mu"
                                                                    ][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM1"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                            {
                                                                "key": 10,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["VLoose_vs_mu"][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM10"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "VLoose_vs_mu"
                                                                    ][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM10"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                            {
                                                                "key": 11,
                                                                "value": {
                                                                    "nodetype": "binning",
                                                                    "input": "pt",
                                                                    "edges": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ]["VLoose_vs_mu"][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM11"
                                                                    ][
                                                                        "pt"
                                                                    ],
                                                                    "content": rates_dict[
                                                                        "VTight_vs_jets"
                                                                    ][
                                                                        "VLoose_vs_mu"
                                                                    ][
                                                                        "Tight_vs_ele"
                                                                    ][
                                                                        "DM11"
                                                                    ][
                                                                        "rate"
                                                                    ],
                                                                    "flow": "clamp",
                                                                },
                                                            },
                                                        ],
                                                    },
                                                },
                                            ],
                                        },
                                    },
                                ],
                            },
                        },
                    ],
                },
            },
        ],
    }
    # print(
    #     corr_lib["fake_rates"]["data"]["content"]["content"]["value"]["content"][
    #         "value"
    #     ]
    # )
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
