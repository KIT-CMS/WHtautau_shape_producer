#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Dumbledraw.dumbledraw as dd
import Dumbledraw.styles as styles
import ROOT as R

import argparse
import numpy as np
import matplotlib.pyplot as plt
import logging
import os

logger = logging.getLogger("")


_process_map = {
    "data": "data",
    "ggZZ": "VV",
    "WWZ": "WWZ",
    "WZZ": "WZZ",
    "WWW": "WWW",
    "ZZZ": "ZZZ",
    "WZ": "VV",
    "ZZ": "VV",
    "TT": "TT",
    "rem_ttbar": "TT",
    "Wjets": "W",
    "DY": "DY",
    "rem_VV": "VV",
    "rem_VH": "VH",
    "WH": "VH",
    "ZH": "VH",
    "jetFakes": "jetFakes",
}


def setup_logging(output_file, level=logging.DEBUG):
    logger.setLevel(level)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(output_file, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Shape comparison.")
    parser.add_argument(
        "-emt", "--emt_input", type=str, required=True, help="Input root files."
    )
    parser.add_argument(
        "-met", "--met_input", type=str, required=True, help="Input root files."
    )
    parser.add_argument(
        "-var", "--variable", type=str, required=True, help="m_tt or pt_W"
    )
    parser.add_argument(
        "-out", "--output", type=str, required=True, help="output plot files."
    )
    return parser.parse_args()


def add_hists(keys_dict, channel, proc, var, rfile_emt, rfile_met):
    if channel == "emt":
        for k, key in enumerate(keys_dict[channel][proc][var]):
            print(key)
            if k == 0:
                hist = rfile_emt.Get(key).Clone()
            else:
                temp_hist = rfile_emt.Get(key)
                hist.Add(temp_hist)
                del temp_hist
    else:
        for k, key in enumerate(keys_dict[channel][proc][var]):
            print(key)
            if k == 0:
                hist = rfile_met.Get(key).Clone()
            else:
                temp_hist = rfile_met.Get(key)
                hist.Add(temp_hist)
                del temp_hist
    return hist


def main(rfile_emt, rfile_met, variable, out_file):

    channels = ["emt", "met"]
    vars = ["m_tt_lt", "pt_W_lt"]
    # procs_reducible = ["Wjets", "rem_VV", "TT", "DY"]
    procs_reducible = ["jetFakes"]
    procs_rare = ["rem_VH", "WWZ", "WWW", "WZZ", "ZZZ", "ggZZ", "rem_ttbar"]
    procs_sig = ["ZH", "WH"]
    keys_dict = {
        "emt": {
            "keys_reducible": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_rare": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_sig": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_data": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_wz": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_zz": {"m_tt_lt": [], "pt_W_lt": []},
        },
        "met": {
            "keys_reducible": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_rare": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_sig": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_data": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_wz": {"m_tt_lt": [], "pt_W_lt": []},
            "keys_zz": {"m_tt_lt": [], "pt_W_lt": []},
        },
    }

    for ch in channels:
        for var in vars:
            for proc in procs_reducible:
                keys_dict["{ch}".format(ch=ch)]["keys_reducible"][
                    "{var}".format(var=var)
                ].append(
                    "{proc}#{ch}-{sel}#Nominal#{var}".format(
                        proc=proc,
                        ch=ch,
                        var=var,
                        sel=_process_map["{proc}".format(proc=proc)],
                    )
                )
            for proc in procs_rare:
                keys_dict["{ch}".format(ch=ch)]["keys_rare"][
                    "{var}".format(var=var)
                ].append(
                    "{proc}#{ch}-{sel}#Nominal#{var}".format(
                        proc=proc,
                        ch=ch,
                        var=var,
                        sel=_process_map["{proc}".format(proc=proc)],
                    )
                )
            for proc in procs_sig:
                keys_dict["{ch}".format(ch=ch)]["keys_sig"][
                    "{var}".format(var=var)
                ].append(
                    "{proc}#{ch}-{sel}#Nominal#{var}".format(
                        proc=proc,
                        ch=ch,
                        var=var,
                        sel=_process_map["{proc}".format(proc=proc)],
                    )
                )
            keys_dict["{ch}".format(ch=ch)]["keys_data"][
                "{var}".format(var=var)
            ].append("data#{ch}#Nominal#{var}".format(ch=ch, var=var))
            keys_dict["{ch}".format(ch=ch)]["keys_wz"]["{var}".format(var=var)].append(
                "{proc}#{ch}-{sel}#Nominal#{var}".format(
                    proc="WZ",
                    ch=ch,
                    var=var,
                    sel=_process_map["WZ"],
                )
            )
            keys_dict["{ch}".format(ch=ch)]["keys_zz"]["{var}".format(var=var)].append(
                "{proc}#{ch}-{sel}#Nominal#{var}".format(
                    proc="ZZ",
                    ch=ch,
                    var=var,
                    sel=_process_map["ZZ"],
                )
            )
    print(keys_dict)
    hist_reducibel_emt_m_tt_lt = add_hists(
        keys_dict, "emt", "keys_reducible", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_reducibel_emt_pt_W_lt = add_hists(
        keys_dict, "emt", "keys_reducible", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_rare_emt_m_tt_lt = add_hists(
        keys_dict, "emt", "keys_rare", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_rare_emt_pt_W_lt = add_hists(
        keys_dict, "emt", "keys_rare", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_sig_emt_m_tt_lt = add_hists(
        keys_dict, "emt", "keys_sig", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_sig_emt_pt_W_lt = add_hists(
        keys_dict, "emt", "keys_sig", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_wz_emt_m_tt_lt = add_hists(
        keys_dict, "emt", "keys_wz", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_wz_emt_pt_W_lt = add_hists(
        keys_dict, "emt", "keys_wz", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_zz_emt_m_tt_lt = add_hists(
        keys_dict, "emt", "keys_zz", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_zz_emt_pt_W_lt = add_hists(
        keys_dict, "emt", "keys_zz", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_data_emt_m_tt_lt = add_hists(
        keys_dict, "emt", "keys_data", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_data_emt_pt_W_lt = add_hists(
        keys_dict, "emt", "keys_data", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_reducibel_met_m_tt_lt = add_hists(
        keys_dict, "met", "keys_reducible", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_reducibel_met_pt_W_lt = add_hists(
        keys_dict, "met", "keys_reducible", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_rare_met_m_tt_lt = add_hists(
        keys_dict, "met", "keys_rare", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_rare_met_pt_W_lt = add_hists(
        keys_dict, "met", "keys_rare", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_sig_met_m_tt_lt = add_hists(
        keys_dict, "met", "keys_sig", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_sig_met_pt_W_lt = add_hists(
        keys_dict, "met", "keys_sig", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_wz_met_m_tt_lt = add_hists(
        keys_dict, "met", "keys_wz", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_wz_met_pt_W_lt = add_hists(
        keys_dict, "met", "keys_wz", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_zz_met_m_tt_lt = add_hists(
        keys_dict, "met", "keys_zz", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_zz_met_pt_W_lt = add_hists(
        keys_dict, "met", "keys_zz", "pt_W_lt", rfile_emt, rfile_met
    )
    hist_data_met_m_tt_lt = add_hists(
        keys_dict, "met", "keys_data", "m_tt_lt", rfile_emt, rfile_met
    )
    hist_data_met_pt_W_lt = add_hists(
        keys_dict, "met", "keys_data", "pt_W_lt", rfile_emt, rfile_met
    )

    hist_data_tot_m_tt_lt = hist_data_met_m_tt_lt.Clone()
    hist_data_tot_m_tt_lt.Add(hist_data_emt_m_tt_lt)
    hist_data_tot_pt_W_lt = hist_data_met_pt_W_lt.Clone()
    hist_data_tot_pt_W_lt.Add(hist_data_emt_pt_W_lt)

    plot = dd.Plot([0.3, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14)
    total_bkg_m_tt_lt = hist_reducibel_emt_m_tt_lt.Clone()
    for proc in [
        hist_rare_emt_m_tt_lt,
        hist_wz_emt_m_tt_lt,
        hist_zz_emt_m_tt_lt,
        hist_rare_met_m_tt_lt,
        hist_wz_met_m_tt_lt,
        hist_zz_met_m_tt_lt,
        hist_reducibel_met_m_tt_lt,
    ]:
        total_bkg_m_tt_lt.Add(proc)
    total_bkg_pt_W_lt = hist_reducibel_emt_pt_W_lt.Clone()
    for proc in [
        hist_rare_emt_pt_W_lt,
        hist_wz_emt_pt_W_lt,
        hist_zz_emt_pt_W_lt,
        hist_rare_met_pt_W_lt,
        hist_wz_met_pt_W_lt,
        hist_zz_met_pt_W_lt,
        hist_reducibel_met_pt_W_lt,
    ]:
        total_bkg_pt_W_lt.Add(proc)

    if variable == "m_tt_lt":
        plot.add_hist(total_bkg_m_tt_lt, "total_bkg")
        plot.setGraphStyle(
            "total_bkg",
            "e2",
            markersize=0,
            fillcolor=styles.color_dict["unc"],
            linecolor=0,
        )
        plot.add_hist(
            hist_data_tot_m_tt_lt,
            "data_obs",
        )
        plot.add_hist(
            hist_reducibel_met_m_tt_lt,
            "red_met",
        )
        plot.add_hist(
            hist_reducibel_emt_m_tt_lt,
            "red_emt",
        )
        plot.add_hist(
            hist_rare_met_m_tt_lt,
            "rare_met",
        )
        plot.add_hist(
            hist_rare_emt_m_tt_lt,
            "rare_emt",
        )
        plot.add_hist(
            hist_sig_met_m_tt_lt,
            "sig_met",
        )
        plot.add_hist(
            hist_sig_emt_m_tt_lt,
            "sig_emt",
        )
        plot.add_hist(
            hist_zz_met_m_tt_lt,
            "zz_met",
        )
        plot.add_hist(
            hist_zz_emt_m_tt_lt,
            "zz_emt",
        )
        plot.add_hist(
            hist_wz_met_m_tt_lt,
            "wz_met",
        )
        plot.add_hist(
            hist_wz_emt_m_tt_lt,
            "wz_emt",
        )
    elif variable == "pt_W_lt":
        plot.add_hist(total_bkg_pt_W_lt, "total_bkg")
        plot.setGraphStyle(
            "total_bkg",
            "e2",
            markersize=0,
            fillcolor=styles.color_dict["unc"],
            linecolor=0,
        )
        plot.add_hist(
            hist_data_tot_pt_W_lt,
            "data_obs",
        )
        plot.add_hist(
            hist_reducibel_met_pt_W_lt,
            "red_met",
        )
        plot.add_hist(
            hist_reducibel_emt_pt_W_lt,
            "red_emt",
        )
        plot.add_hist(
            hist_rare_met_pt_W_lt,
            "rare_met",
        )
        plot.add_hist(
            hist_rare_emt_pt_W_lt,
            "rare_emt",
        )
        plot.add_hist(
            hist_sig_met_pt_W_lt,
            "sig_met",
        )
        plot.add_hist(
            hist_sig_emt_pt_W_lt,
            "sig_emt",
        )
        plot.add_hist(
            hist_zz_met_pt_W_lt,
            "zz_met",
        )
        plot.add_hist(
            hist_zz_emt_pt_W_lt,
            "zz_emt",
        )
        plot.add_hist(
            hist_wz_met_pt_W_lt,
            "wz_met",
        )
        plot.add_hist(
            hist_wz_emt_pt_W_lt,
            "wz_emt",
        )
    bkg_processes = [
        "wz_met",
        "wz_emt",
        "red_met",
        "red_emt",
        "rare_met",
        "rare_emt",
        "zz_met",
        "zz_emt",
        "sig_met",
        "sig_emt",
    ]
    for proc in bkg_processes:
        plot.setGraphStyle(proc, "hist", fillcolor=styles.color_dict[proc])
    plot.subplot(0).setGraphStyle("data_obs", "e0")
    plot.subplot(2).setGraphStyle("data_obs", "e0")
    plot.create_stack(bkg_processes, "stack")
    plot.subplot(2).normalize(["total_bkg", "data_obs"], "total_bkg")

    # set axes limits and labels
    plot.subplot(0).setYlims(
        0,
        54,
    )

    plot.subplot(2).setYlims(
        0.75,
        5,
    )
    plot.subplot(1).setYlims(0.1, 101)
    plot.subplot(1).setYlabel("")  # otherwise number labels are not drawn on axis
    if variable == "m_tt_lt":
        x_label = "m_{#tau#tau} / GeV"
    elif variable == "pt_W_lt":
        x_label = "p_{T} W boson / GeV"
    plot.subplot(2).setXlabel(x_label)
    plot.subplot(0).setYlabel("N_{events}")
    plot.subplot(2).setYlabel("")
    plot.subplot(2).setGrid()
    plot.scaleYLabelSize(0.8)
    plot.scaleYTitleOffset(1.1)

    procs_to_draw = ["stack", "total_bkg", "data_obs"]
    plot.subplot(0).Draw(procs_to_draw)
    plot.subplot(2).Draw(["total_bkg", "data_obs"])

    for i in range(2):
        plot.add_legend(width=0.625, height=0.15)
        for process in bkg_processes:
            plot.legend(i).add_entry(
                0,
                process,
                styles.legend_label_dict[process],
                "f",
            )

        plot.legend(i).add_entry(0, "total_bkg", "Bkg. stat. unc.", "f")
        plot.legend(i).add_entry(0, "data_obs", "Observed", "PE2L")
        plot.legend(i).setNColumns(2)
    plot.legend(0).Draw()
    plot.legend(1).setAlpha(0.0)
    plot.legend(1).Draw()
    for i in range(2):
        plot.add_legend(reference_subplot=2, pos=1, width=0.6, height=0.03)
        plot.legend(i + 2).add_entry(0, "data_obs", "Observed", "PE2L")
        plot.legend(i + 2).add_entry(0, "total_bkg", "Bkg. stat. unc.", "f")
        plot.legend(i + 2).setNColumns(4)
    plot.legend(2).Draw()
    plot.legend(3).setAlpha(0.0)
    plot.legend(3).Draw()
    # draw additional labels
    plot.DrawCMS()
    plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")

    posChannelCategoryLabelLeft = None
    plot.DrawChannelCategoryLabel(
        "%s, %s" % ("emt", ""),
        begin_left=posChannelCategoryLabelLeft,
    )

    plot.save("{out_file}.png".format(out_file=out_file))
    plot.save("{out_file}.pdf".format(out_file=out_file))
    return plot


if __name__ == "__main__":
    args = parse_arguments()
    rfile_emt = R.TFile("{}".format(args.emt_input), "READ")
    rfile_met = R.TFile("{}".format(args.met_input), "READ")
    var = args.variable
    out_file = args.output
    main(rfile_emt, rfile_met, var, out_file)
