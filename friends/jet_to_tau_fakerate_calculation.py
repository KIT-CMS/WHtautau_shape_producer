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
    parser.add_argument(
        "--wp_vs_jets",
        default=[],
        type=lambda wp_jets: [wp for wp in wp_jets.split(",")],
        help="working points vs jets",
    )
    parser.add_argument(
        "--wp_vs_mu",
        default=[],
        type=lambda wp_mu: [wp for wp in wp_mu.split(",")],
        help="working points vs mu",
    )
    parser.add_argument(
        "--wp_vs_ele",
        default=[],
        type=lambda wp_ele: [wp for wp in wp_ele.split(",")],
        help="working points vs ele",
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


def plot_rates(rates_dict, wp_vs_jets, wp_vs_mu, wp_vs_ele, DM, plot_output):
    for wp_jets in wp_vs_jets:
        for dm in DM:
            for wp_mu in wp_vs_mu:
                for wp_ele in wp_vs_ele:
                    if wp_mu == "VLoose" and wp_ele == "VLoose":
                        continue
                    else:
                        pts = rates_dict[wp_jets][wp_mu][wp_ele][dm]["pt"]
                        pt_center = np.zeros(len(pts) - 1)
                        for i in range(len(pts) - 1):
                            pt_center[i] = (pts[i + 1] + pts[i]) / 2
                        plt.errorbar(
                            pt_center,
                            rates_dict[wp_jets][wp_mu][wp_ele][dm]["rate"],
                            rates_dict[wp_jets][wp_mu][wp_ele][dm]["stat_unc"],
                            marker=".",
                            linestyle="",
                            markersize="7",
                            label=r"vs$\mu$({wp_mu})+vsEle({wp_ele})".format(
                                wp_mu=wp_mu, wp_ele=wp_ele
                            ),
                        )
            plt.legend()
            plt.ylim(0, 0.2)
            plt.ylabel(r"jet $\rightarrow\tau_{\mathrm{h}}$ fake rate")
            plt.xlabel(r"$\mathrm{p_{T}}(\tau_{\mathrm{h}})\, (\mathrm{GeV})$")
            plt.savefig(
                "{plot_output}/{wps_jets}__{dm}.png".format(
                    plot_output=plot_output,
                    wps_jets=wp_jets,
                    dm=dm,
                )
            )
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


def rates(wps_vs_jets, wps_vs_mu, wps_vs_ele, DMs, base_path, syst_unc):
    rates_dict = {}
    for wps_jets in wps_vs_jets:
        rates_dict[wps_jets] = {}
        for wps_mu in wps_vs_mu:
            rates_dict[wps_jets][wps_mu] = {}
            for wps_ele in wps_vs_ele:
                if wps_mu == "VLoose" and wps_ele == "VLoose":
                    continue
                else:
                    rates_dict[wps_jets][wps_mu][wps_ele] = {}
                    for dm in DMs:
                        rates_dict[wps_jets][wps_mu][wps_ele][dm] = {
                            "pt": [],
                            "rate": [],
                            "rate_stat_up": [],
                            "rate_stat_down": [],
                            "rate_syst_up": [],
                            "rate_syst_down": [],
                            "stat_unc": [],
                        }
    procs_to_subtract = {
        "ggzz": "ggZZ#mmt-VV#Nominal#pt_3",
        "zz": "ZZ#mmt-VV#Nominal#pt_3",
        "wz": "WZ#mmt-VV#Nominal#pt_3",
        "vvv": "VVV#mmt-VVV#Nominal#pt_3",
        # "ggh": "ggH#mmt-H#Nominal#pt_3",
        # "qqh": "qqH#mmt-H#Nominal#pt_3",
        "ggzh": "ggZH#mmt-H#Nominal#pt_3",
        "zh": "ZH#mmt-H#Nominal#pt_3",
        # "tth": "ttH#mmt-H#Nominal#pt_3",
        # "zzz": "ZZZ#mmt-ZZZ#Nominal#pt_3",
        # "www": "WWW#mmt-WWW#Nominal#pt_3",
        # "wwz": "WWZ#mmt-WWZ#Nominal#pt_3",
        # "wzz": "WZZ#mmt-WZZ#Nominal#pt_3",
        "rem_ttbar": "rem_ttbar#mmt-TT#Nominal#pt_3",
    }
    for wps_jets in wps_vs_jets:
        for wps_mu in wps_vs_mu:
            for wps_ele in wps_vs_ele:
                for dm in DMs:
                    if wps_mu == "VLoose" and wps_ele == "VLoose":
                        continue
                    else:
                        tight_file = R.TFile(
                            base_path
                            + "/{wps_jets}_vs_jets__{wps_mu}_vs_mu__{wps_ele}_vs_ele__{dm}.root".format(
                                wps_jets=wps_jets, wps_mu=wps_mu, wps_ele=wps_ele, dm=dm
                            ),
                            "READ",
                        )
                        tight_data = tight_file.Get("data#mmt#Nominal#pt_3")
                        base_file = R.TFile(
                            base_path
                            + "/VVVLoose_vs_jets__{wps_mu}_vs_mu__{wps_ele}_vs_ele__{dm}.root".format(
                                wps_jets=wps_jets, wps_mu=wps_mu, wps_ele=wps_ele, dm=dm
                            ),
                            "READ",
                        )
                        base_data = base_file.Get("data#mmt#Nominal#pt_3")
                        for syst_shift, scale in enumerate(
                            [-1, -(1 + syst_unc), -(1 - syst_unc)]
                        ):
                            tight_diff = tight_data.Clone()
                            base_diff = base_data.Clone()
                            for proc in procs_to_subtract.values():
                                tight_hist = tight_file.Get(proc)
                                base_hist = base_file.Get(proc)
                                tight_diff.Add(tight_hist, scale)
                                base_diff.Add(base_hist, scale)
                            ratio_hist = tight_diff.Clone()
                            ratio_hist.Divide(base_diff)
                            if syst_shift == 0:
                                for bin_i in range(1, tight_data.GetNbinsX() + 1):
                                    rates_dict[wps_jets][wps_mu][wps_ele][dm][
                                        "rate"
                                    ].append(ratio_hist.GetBinContent(bin_i))
                                    rates_dict[wps_jets][wps_mu][wps_ele][dm][
                                        "stat_unc"
                                    ].append(ratio_hist.GetBinError(bin_i))
                                    rates_dict[wps_jets][wps_mu][wps_ele][dm][
                                        "rate_stat_up"
                                    ].append(
                                        ratio_hist.GetBinContent(bin_i)
                                        + ratio_hist.GetBinError(bin_i)
                                    )
                                    rates_dict[wps_jets][wps_mu][wps_ele][dm][
                                        "rate_stat_down"
                                    ].append(
                                        ratio_hist.GetBinContent(bin_i)
                                        - ratio_hist.GetBinError(bin_i)
                                    )
                                    rates_dict[wps_jets][wps_mu][wps_ele][dm][
                                        "pt"
                                    ].append(tight_data.GetBinLowEdge(bin_i))
                                rates_dict[wps_jets][wps_mu][wps_ele][dm]["pt"].append(
                                    tight_data.GetBinLowEdge(tight_data.GetNbinsX() + 1)
                                )
                            elif syst_shift == 1:
                                for bin_i in range(1, tight_data.GetNbinsX() + 1):
                                    rates_dict[wps_jets][wps_mu][wps_ele][dm][
                                        "rate_syst_down"
                                    ].append(ratio_hist.GetBinContent(bin_i))
                            elif syst_shift == 2:
                                for bin_i in range(1, tight_data.GetNbinsX() + 1):
                                    rates_dict[wps_jets][wps_mu][wps_ele][dm][
                                        "rate_syst_up"
                                    ].append(ratio_hist.GetBinContent(bin_i))
                            del tight_diff
                            del base_diff
                            del ratio_hist
                        base_file.Close()
                        tight_file.Close()
                        del base_data
                        del tight_data
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


def cont_wp_jets(rates_dict, wp_vs_jets, wp_vs_mu, wp_vs_ele):
    content = []
    for wp_jets in wp_vs_jets:
        content.append(
            {
                "key": "{wp_jets}".format(wp_jets=wp_jets),
                "value": {
                    "nodetype": "category",
                    "input": "wp_vs_mu",
                    "content": cont_wp_mu(rates_dict, wp_jets, wp_vs_mu, wp_vs_ele),
                },
            }
        )
    return content


def cont_wp_mu(rates_dict, wp_jets, wp_vs_mu, wp_vs_ele):
    content = []
    for wp_mu in wp_vs_mu:
        content.append(
            {
                "key": "{wp_mu}".format(wp_mu=wp_mu),
                "value": {
                    "nodetype": "category",
                    "input": "wp_vs_ele",
                    "content": cont_wp_ele(rates_dict, wp_jets, wp_mu, wp_vs_ele),
                },
            }
        )
    return content


def cont_wp_ele(rates_dict, wp_jets, wp_mu, wp_vs_ele):
    content = []
    for wp_ele in wp_vs_ele:
        if wp_mu == "VLoose" and wp_ele == "VLoose":
            continue
        else:
            content.append(
                {
                    "key": "{wp_ele}".format(wp_ele=wp_ele),
                    "value": {
                        "nodetype": "category",
                        "input": "dm",
                        "content": decay_modes(rates_dict, wp_jets, wp_mu, wp_ele),
                    },
                }
            )
    return content


def data(rates_dict, wp_vs_jets, wp_vs_mu, wp_vs_ele):
    data = {
        "nodetype": "category",
        "input": "wp_vs_jets",
        "content": cont_wp_jets(rates_dict, wp_vs_jets, wp_vs_mu, wp_vs_ele),
    }
    return data


def correction_lib_format(rates_dict, wp_vs_jets, wp_vs_mu, wp_vs_ele):
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
                "data": data(rates_dict, wp_vs_jets, wp_vs_mu, wp_vs_ele),
            }
        ],
    }
    return corr_lib


def main(
    wp_vs_jets, wp_vs_mu, wp_vs_ele, base_path, output_file, plot_output, syst_unc
):
    DMs = ["DM0", "DM1", "DM10", "DM11"]
    rates_dict = rates(wp_vs_jets, wp_vs_mu, wp_vs_ele, DMs, base_path, syst_unc)
    plot_rates(rates_dict, wp_vs_jets, wp_vs_mu, wp_vs_ele, DMs, plot_output)
    with open("{output}".format(output=output_file), "w") as outfile:
        json.dump(
            correction_lib_format(rates_dict, wp_vs_jets, wp_vs_mu, wp_vs_ele), outfile
        )


if __name__ == "__main__":
    args = parse_arguments()
    base_path = args.base_path
    output_file = args.output_file
    plot_output = args.plot_output
    syst_unc = args.syst_unc / 100.0
    path = os.path.join(base_path, "*.root")
    wp_vs_jets = args.wp_vs_jets
    wp_vs_mu = args.wp_vs_mu
    wp_vs_ele = args.wp_vs_ele
    main(wp_vs_jets, wp_vs_mu, wp_vs_ele, base_path, output_file, plot_output, syst_unc)
