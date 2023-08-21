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
        "--syst_unc",
        type=float,
        required=True,
        help="systematic uncertainty on the yield of subtraced processes in %",
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
            rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["Tight_vs_ele"][dm]["stat_unc"],
            marker=".",
            linestyle="",
            markersize="7",
            label="TightvsMu+TightvsEle",
        )
        plt.errorbar(
            pt_center,
            rates_dict["VTight_vs_jets"]["VLoose_vs_mu"]["Tight_vs_ele"][dm]["rate"],
            rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["Tight_vs_ele"][dm]["stat_unc"],
            marker=".",
            linestyle="",
            markersize="7",
            label="VLoosevsMu+TightvsEle",
        )
        plt.errorbar(
            pt_center,
            rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["VLoose_vs_ele"][dm]["rate"],
            rates_dict["VTight_vs_jets"]["Tight_vs_mu"]["Tight_vs_ele"][dm]["stat_unc"],
            marker=".",
            linestyle="",
            markersize="7",
            label="TightvsMu+VLoosevsEle",
        )
        plt.legend()
        # plt.ylim(0, 0.15)
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


def rates(shapes, base_path, syst_unc):
    rates_dict = {
        "VTight_vs_jets": {
            "Tight_vs_mu": {
                "Tight_vs_ele": {
                    "DM0": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                    "DM1": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                    "DM10": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                    "DM11": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                },
                "VLoose_vs_ele": {
                    "DM0": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                    "DM1": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                    "DM10": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                    "DM11": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                },
            },
            "VLoose_vs_mu": {
                "Tight_vs_ele": {
                    "DM0": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                    "DM1": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                    "DM10": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                    "DM11": {
                        "pt": [],
                        "rate": [],
                        "rate_stat_up": [],
                        "rate_stat_down": [],
                        "rate_syst_up": [],
                        "rate_syst_down": [],
                        "stat_unc": [],
                    },
                },
            },
        }
    }
    procs_to_subtract = {
        "ggzz": "ggZZ#mmt-VV#Nominal#pt_3",
        "zz": "ZZ#mmt-VV#Nominal#pt_3",
        "wz": "WZ#mmt-VV#Nominal#pt_3",
        "zzz": "ZZZ#mmt-ZZZ#Nominal#pt_3",
        "www": "WWW#mmt-WWW#Nominal#pt_3",
        "wwz": "WWZ#mmt-WWZ#Nominal#pt_3",
        "wzz": "WZZ#mmt-WZZ#Nominal#pt_3",
        "rem_vh": "rem_VH#mmt-VH#Nominal#pt_3",
        "rem_ttbar": "rem_ttbar#mmt-TT#Nominal#pt_3",
    }
    for shape in shapes:
        if not "VVVLoose_vs_jets" in shape:
            wp = working_points(shape)
            tight_file = R.TFile(shape, "READ")
            tight_data = tight_file.Get("data#mmt#Nominal#pt_3")
            if "DM0." in shape:
                for syst_shift, scale in enumerate(
                    [-1, -(1 + syst_unc), -(1 - syst_unc)]
                ):
                    tight_diff = tight_data.Clone()
                    base_DM0 = base_file(base_path, wp, "DM0")
                    base_data = base_DM0.Get("data#mmt#Nominal#pt_3")
                    base_diff = base_data.Clone()
                    for proc in procs_to_subtract.values():
                        tight_hist = tight_file.Get(proc)
                        base_hist = base_DM0.Get(proc)
                        tight_diff.Add(tight_hist, scale)
                        base_diff.Add(base_hist, scale)
                    ratio_hist = tight_diff.Clone()
                    ratio_hist.Divide(base_diff)
                    if syst_shift == 0:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["rate"].append(
                                ratio_hist.GetBinContent(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["stat_unc"].append(
                                ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM0"][
                                "rate_stat_up"
                            ].append(
                                ratio_hist.GetBinContent(bin_i)
                                + ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM0"][
                                "rate_stat_down"
                            ].append(
                                ratio_hist.GetBinContent(bin_i)
                                - ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["pt"].append(
                                tight_data.GetBinLowEdge(bin_i)
                            )
                        rates_dict[wp[0]][wp[1]][wp[2]]["DM0"]["pt"].append(
                            tight_data.GetBinLowEdge(tight_data.GetNbinsX() + 1)
                        )
                        base_DM0.Close()
                    elif syst_shift == 1:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM0"][
                                "rate_syst_down"
                            ].append(ratio_hist.GetBinContent(bin_i))
                        base_DM0.Close()
                    elif syst_shift == 2:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM0"][
                                "rate_syst_up"
                            ].append(ratio_hist.GetBinContent(bin_i))
                        base_DM0.Close()
                    del tight_diff
                    del base_data
                    del base_diff
                    del ratio_hist
            elif "DM1." in shape:
                for syst_shift, scale in enumerate(
                    [-1, -(1 + syst_unc), -(1 - syst_unc)]
                ):
                    tight_diff = tight_data.Clone()
                    base_DM1 = base_file(base_path, wp, "DM1")
                    base_data = base_DM1.Get("data#mmt#Nominal#pt_3")
                    base_diff = base_data.Clone()
                    for proc in procs_to_subtract.values():
                        tight_hist = tight_file.Get(proc)
                        base_hist = base_DM1.Get(proc)
                        tight_diff.Add(tight_hist, scale)
                        base_diff.Add(base_hist, scale)
                    ratio_hist = tight_diff.Clone()
                    ratio_hist.Divide(base_diff)
                    if syst_shift == 0:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM1"]["rate"].append(
                                ratio_hist.GetBinContent(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM1"]["stat_unc"].append(
                                ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM1"][
                                "rate_stat_up"
                            ].append(
                                ratio_hist.GetBinContent(bin_i)
                                + ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM1"][
                                "rate_stat_down"
                            ].append(
                                ratio_hist.GetBinContent(bin_i)
                                - ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM1"]["pt"].append(
                                tight_data.GetBinLowEdge(bin_i)
                            )
                        rates_dict[wp[0]][wp[1]][wp[2]]["DM1"]["pt"].append(
                            tight_data.GetBinLowEdge(tight_data.GetNbinsX() + 1)
                        )
                        base_DM1.Close()
                    elif syst_shift == 1:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM1"][
                                "rate_syst_down"
                            ].append(ratio_hist.GetBinContent(bin_i))
                        base_DM1.Close()
                    elif syst_shift == 2:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM1"][
                                "rate_syst_up"
                            ].append(ratio_hist.GetBinContent(bin_i))
                        base_DM1.Close()
                    del tight_diff
                    del base_data
                    del base_diff
                    del ratio_hist
            elif "DM10" in shape:
                for syst_shift, scale in enumerate(
                    [-1, -(1 + syst_unc), -(1 - syst_unc)]
                ):
                    tight_diff = tight_data.Clone()
                    base_DM10 = base_file(base_path, wp, "DM10")
                    base_data = base_DM10.Get("data#mmt#Nominal#pt_3")
                    base_diff = base_data.Clone()
                    for proc in procs_to_subtract.values():
                        tight_hist = tight_file.Get(proc)
                        base_hist = base_DM10.Get(proc)
                        tight_diff.Add(tight_hist, scale)
                        base_diff.Add(base_hist, scale)
                    ratio_hist = tight_diff.Clone()
                    ratio_hist.Divide(base_diff)
                    if syst_shift == 0:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM10"]["rate"].append(
                                ratio_hist.GetBinContent(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM10"]["stat_unc"].append(
                                ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM10"][
                                "rate_stat_up"
                            ].append(
                                ratio_hist.GetBinContent(bin_i)
                                + ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM10"][
                                "rate_stat_down"
                            ].append(
                                ratio_hist.GetBinContent(bin_i)
                                - ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM10"]["pt"].append(
                                tight_data.GetBinLowEdge(bin_i)
                            )
                        rates_dict[wp[0]][wp[1]][wp[2]]["DM10"]["pt"].append(
                            tight_data.GetBinLowEdge(tight_data.GetNbinsX() + 1)
                        )
                        base_DM10.Close()
                    elif syst_shift == 1:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM10"][
                                "rate_syst_down"
                            ].append(ratio_hist.GetBinContent(bin_i))
                        base_DM10.Close()
                    elif syst_shift == 2:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM10"][
                                "rate_syst_up"
                            ].append(ratio_hist.GetBinContent(bin_i))
                        base_DM10.Close()
                    del tight_diff
                    del base_data
                    del base_diff
                    del ratio_hist
            elif "DM11" in shape:
                for syst_shift, scale in enumerate(
                    [-1, -(1 + syst_unc), -(1 - syst_unc)]
                ):
                    tight_diff = tight_data.Clone()
                    base_DM11 = base_file(base_path, wp, "DM11")
                    base_data = base_DM11.Get("data#mmt#Nominal#pt_3")
                    base_diff = base_data.Clone()
                    for proc in procs_to_subtract.values():
                        tight_hist = tight_file.Get(proc)
                        base_hist = base_DM11.Get(proc)
                        tight_diff.Add(tight_hist, scale)
                        base_diff.Add(base_hist, scale)
                    ratio_hist = tight_diff.Clone()
                    ratio_hist.Divide(base_diff)
                    if syst_shift == 0:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM11"]["rate"].append(
                                ratio_hist.GetBinContent(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM11"]["stat_unc"].append(
                                ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM11"][
                                "rate_stat_up"
                            ].append(
                                ratio_hist.GetBinContent(bin_i)
                                + ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM11"][
                                "rate_stat_down"
                            ].append(
                                ratio_hist.GetBinContent(bin_i)
                                - ratio_hist.GetBinError(bin_i)
                            )
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM11"]["pt"].append(
                                tight_data.GetBinLowEdge(bin_i)
                            )
                        rates_dict[wp[0]][wp[1]][wp[2]]["DM11"]["pt"].append(
                            tight_data.GetBinLowEdge(tight_data.GetNbinsX() + 1)
                        )
                        base_DM11.Close()
                    elif syst_shift == 1:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM11"][
                                "rate_syst_down"
                            ].append(ratio_hist.GetBinContent(bin_i))
                        base_DM11.Close()
                    elif syst_shift == 2:
                        for bin_i in range(1, tight_data.GetNbinsX() + 1):
                            rates_dict[wp[0]][wp[1]][wp[2]]["DM11"][
                                "rate_syst_up"
                            ].append(ratio_hist.GetBinContent(bin_i))
                        base_DM11.Close()
                    del tight_diff
                    del base_data
                    del base_diff
                    del ratio_hist
    return rates_dict


def values(rates_dict, wp_jets, wp_mu, wp_ele, dm):
    content = []
    for bin in range(len(rates_dict[wp_jets][wp_mu][wp_ele][dm]["pt"]) - 1):
        content.append(
            {
                "nodetype": "category",
                "input": "syst",
                "content": [
                    {
                        "key": "syst_up",
                        "value": rates_dict[wp_jets][wp_mu][wp_ele][dm]["rate_syst_up"][
                            bin
                        ],
                    },
                    {
                        "key": "syst_down",
                        "value": rates_dict[wp_jets][wp_mu][wp_ele][dm][
                            "rate_syst_down"
                        ][bin],
                    },
                    {
                        "key": "stat_up",
                        "value": rates_dict[wp_jets][wp_mu][wp_ele][dm]["rate_stat_up"][
                            bin
                        ],
                    },
                    {
                        "key": "stat_down",
                        "value": rates_dict[wp_jets][wp_mu][wp_ele][dm][
                            "rate_stat_down"
                        ][bin],
                    },
                    {
                        "key": "nom",
                        "value": rates_dict[wp_jets][wp_mu][wp_ele][dm]["rate"][bin],
                    },
                ],
            }
        )
    return content


def decay_modes(rates_dict, wp_vs_jets, wp_vs_mu, wp_vs_ele):
    content = []
    for dm in [(0, "DM0"), (1, "DM1"), (10, "DM10"), (11, "DM11")]:
        content.append(
            {
                "key": dm[0],
                "value": {
                    "nodetype": "binning",
                    "input": "pt",
                    "edges": rates_dict[wp_vs_jets][wp_vs_mu][wp_vs_ele][dm[1]]["pt"],
                    "content": values(
                        rates_dict,
                        wp_vs_jets,
                        wp_vs_mu,
                        wp_vs_ele,
                        dm[1],
                    ),
                    "flow": "clamp",
                },
            }
        )
    return content


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
                    {
                        "name": "syst",
                        "type": "string",
                        "description": "Systematic variation: 'nom', 'up', 'down'",
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
                                                        "content": decay_modes(
                                                            rates_dict,
                                                            "VTight_vs_jets",
                                                            "Tight_vs_mu",
                                                            "Tight_vs_ele",
                                                        ),
                                                    },
                                                },
                                                {
                                                    "key": "VLoose",
                                                    "value": {
                                                        "nodetype": "category",
                                                        "input": "dm",
                                                        "content": decay_modes(
                                                            rates_dict,
                                                            "VTight_vs_jets",
                                                            "Tight_vs_mu",
                                                            "VLoose_vs_ele",
                                                        ),
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
                                                        "content": decay_modes(
                                                            rates_dict,
                                                            "VTight_vs_jets",
                                                            "VLoose_vs_mu",
                                                            "Tight_vs_ele",
                                                        ),
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


def main(shapes, base_path, output_file, plot_output, syst_unc):
    rates_dict = rates(shapes, base_path, syst_unc)
    print(rates_dict)
    plot_rates(rates_dict, plot_output)
    with open("{output}".format(output=output_file), "w") as outfile:
        json.dump(correction_lib_format(rates_dict), outfile)


if __name__ == "__main__":
    args = parse_arguments()
    base_path = args.base_path
    output_file = args.output_file
    plot_output = args.plot_output
    syst_unc = args.syst_unc / 100.0
    print("hi", syst_unc)
    path = os.path.join(base_path, "*.root")
    shapes = glob.glob(path)
    main(shapes, base_path, output_file, plot_output, syst_unc)
