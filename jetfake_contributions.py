#!/usr/bin/env python
# -*- coding: utf-8 -*-
# source utils/setup_cvmfs_sft.sh
# source utils/setup_python.sh
import Dumbledraw.dumbledraw as dd
import Dumbledraw.styles as styles
import ROOT as R

import argparse
from copy import deepcopy
import os

from root_numpy import hist2array
import numpy as np
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger("")


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
        "-in", "--input", type=str, required=True, help="Input root files."
    )
    parser.add_argument(
        "-out", "--plot_output", type=str, required=True, help="plot output path"
    )
    parser.add_argument("-c", "--channel", type=str, required=True, help="channel")
    return parser.parse_args()


def comparison_plot(hists, channel, output):
    plot = dd.Plot([0.3, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14)
    if channel == "emt":
        plot.setGraphStyle(
            "mc",
            "e2",
            markersize=0,
            fillcolor=styles.color_dict["unc"],
            linecolor=0,
        )
        plot.setGraphStyle("mc_unc", "hist", linecolor=R.kBlack, linewidth=2)
        plot.setGraphStyle(
            "mc_col", "hist", fillcolor=styles.color_dict["jetFakes"], linecolor=0
        )
        plot.setGraphStyle(
            "data",
            "pe0",
            linecolor=R.kBlack,
            markersize=0.75,
            markercolor=R.kBlack,
            linewidth=1,
        )
    # y_max = 1.5 * max(
    #     plot.subplot(0).get_hist("data").GetMaximum(),
    #     plot.subplot(0).get_hist("mc").GetMaximum(),
    # )
    # Assemble ratio plot.
    plot.subplot(0).setYlabel("N_{events}")
    # plot.setXlims(-4, 4)
    plot.scaleYLabelSize(0.8)
    plot.scaleYTitleOffset(1.1)
    plot.subplot(0).Draw(draw)
    plot.add_legend(width=0.15, height=0.15, pos=2)
    for hist in draw:
        plot.legend(0).add_entry(0, hist, hist, "l")
    plot.legend(0).Draw()
    plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
    plot.DrawCMS(position="outside")
    plot.save(output + "jetfake_contributions" + ".png")
    plot.save(output + "jetfake_contributions" + ".pdf")
    return plot


def main(args):
    channel = args.channel
    output = args.plot_output
    rfile = R.TFile("{}".format(args.input), "READ")
    nom = rfile.Get("jetFakes#{ch}-jetFakes#Nominal#pt_1".format(ch=channel))
    tau = rfile.Get("jetFakes#{ch}-jetFakes#tau_anti_iso#pt_1".format(ch=channel))
    if channel == "emt":
        lep1 = rfile.Get(
            "jetFakes#{ch}-jetFakes#ele1_anti_isoid#pt_1".format(ch=channel)
        )
        lep2 = rfile.Get(
            "jetFakes#{ch}-jetFakes#mu2_anti_isoid#pt_1".format(ch=channel)
        )
        lep1tau = rfile.Get(
            "jetFakes#{ch}-jetFakes#ele1tau_anti_isoid#pt_1".format(ch=channel)
        )
        lep2tau = rfile.Get(
            "jetFakes#{ch}-jetFakes#mu2tau_anti_isoid#pt_1".format(ch=channel)
        )
    elif channel == "met":
        lep1 = rfile.Get(
            "jetFakes#{ch}-jetFakes#mu1_anti_isoid#pt_1".format(ch=channel)
        )
        lep2 = rfile.Get(
            "jetFakes#{ch}-jetFakes#ele2_anti_isoid#pt_1".format(ch=channel)
        )
        lep1tau = rfile.Get(
            "jetFakes#{ch}-jetFakes#mu1tau_anti_isoid#pt_1".format(ch=channel)
        )
        lep2tau = rfile.Get(
            "jetFakes#{ch}-jetFakes#ele2tau_anti_isoid#pt_1".format(ch=channel)
        )
    elif channel == "mmt":
        lep2 = rfile.Get(
            "jetFakes#{ch}-jetFakes#mu2_anti_isoid#pt_1".format(ch=channel)
        )
        lep2tau = rfile.Get(
            "jetFakes#{ch}-jetFakes#mu2tau_anti_isoid#pt_1".format(ch=channel)
        )
    if channel in ["emt", "met"]:
        plot = dd.Plot([0.1, 0.1], "ModTDR", r=0.04, l=0.14)
        plot.add_hist(tau, "tau", "tau")
        plot.add_hist(lep1, "lep1", "lep1")
        plot.add_hist(lep2, "lep2", "lep2")
        plot.add_hist(lep1tau, "lep1tau", "lep1tau")
        plot.add_hist(lep2tau, "lep2tau", "lep2tau")
        plot.setGraphStyle(
            "tau", "hist", linecolor=R.TColor.GetColor("#ff595e"), linewidth=2
        )
        if channel == "emt":
            plot.setGraphStyle(
                "lep1", "hist", linecolor=R.TColor.GetColor("#ffca3a"), linewidth=2
            )
            plot.setGraphStyle(
                "lep2", "hist", linecolor=R.TColor.GetColor("#8ac926"), linewidth=2
            )
            plot.setGraphStyle(
                "lep1tau", "hist", linecolor=R.TColor.GetColor("#1982c4"), linewidth=2
            )
            plot.setGraphStyle(
                "lep2tau", "hist", linecolor=R.TColor.GetColor("#6a4c93"), linewidth=2
            )
        else:
            plot.setGraphStyle(
                "lep2", "hist", linecolor=R.TColor.GetColor("#ffca3a"), linewidth=2
            )
            plot.setGraphStyle(
                "lep1", "hist", linecolor=R.TColor.GetColor("#8ac926"), linewidth=2
            )
            plot.setGraphStyle(
                "lep2tau", "hist", linecolor=R.TColor.GetColor("#1982c4"), linewidth=2
            )
            plot.setGraphStyle(
                "lep1tau", "hist", linecolor=R.TColor.GetColor("#6a4c93"), linewidth=2
            )
        y_max = 1.5 * max(
            [
                plot.subplot(0).get_hist("tau").GetMaximum(),
                plot.subplot(0).get_hist("lep1").GetMaximum(),
                plot.subplot(0).get_hist("lep2").GetMaximum(),
            ]
        )
        y_min = 1.5 * min(
            [
                plot.subplot(0).get_hist("lep1tau").GetMinimum(),
                plot.subplot(0).get_hist("lep2tau").GetMinimum(),
            ]
        )
        if channel == "emt":
            plot.subplot(0).setYlims(-3, 10)
        else:
            plot.subplot(0).setYlims(-10, 35)
        plot.subplot(0).setYlabel("N_{events}")
        plot.scaleYLabelSize(0.8)
        plot.scaleYTitleOffset(1.1)
        plot.subplot(0).Draw(["tau", "lep1", "lep2", "lep1tau", "lep2tau"])
        plot.add_legend(width=0.15, height=0.15, pos=3)
        plot.legend(0).add_entry(0, "tau", "#tau anti iso", "l")
        if channel == "emt":
            plot.subplot(0).setXlabel(styles.x_label_dict["emt"]["pt_1"])
            plot.legend(0).add_entry(0, "lep1", "e anti iso", "l")
            plot.legend(0).add_entry(0, "lep2", "#mu anti iso", "l")
            plot.legend(0).add_entry(0, "lep1tau", "#tau+e anti iso", "l")
            plot.legend(0).add_entry(0, "lep2tau", "#tau+#mu anti iso", "l")
        else:
            plot.subplot(0).setXlabel(styles.x_label_dict["met"]["pt_1"])
            plot.legend(0).add_entry(0, "lep2", "e anti iso", "l")
            plot.legend(0).add_entry(0, "lep1", "#mu anti iso", "l")
            plot.legend(0).add_entry(0, "lep2tau", "#tau+e anti iso", "l")
            plot.legend(0).add_entry(0, "lep1tau", "#tau+#mu anti iso", "l")
        plot.legend(0).Draw()
        plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
        plot.DrawCMS(position="outside")
        plot.save(output + "jetfake_contributions" + ".png")
        plot.save(output + "jetfake_contributions" + ".pdf")
    elif channel == "mmt":
        plot = dd.Plot([0.1, 0.1], "ModTDR", r=0.04, l=0.14)
        plot.add_hist(tau, "tau", "tau")
        plot.add_hist(lep2, "lep2", "lep2")
        plot.add_hist(lep2tau, "lep2tau", "lep2tau")
        plot.setGraphStyle(
            "tau", "hist", linecolor=R.TColor.GetColor("#ff595e"), linewidth=2
        )
        plot.setGraphStyle(
            "lep2", "hist", linecolor=R.TColor.GetColor("#8ac926"), linewidth=2
        )
        plot.setGraphStyle(
            "lep2tau", "hist", linecolor=R.TColor.GetColor("#6a4c93"), linewidth=2
        )
        y_max = 1.5 * max(
            [
                plot.subplot(0).get_hist("tau").GetMaximum(),
                plot.subplot(0).get_hist("lep2").GetMaximum(),
            ]
        )
        y_min = 1.5 * min(
            [
                plot.subplot(0).get_hist("lep2tau").GetMinimum(),
            ]
        )
        plot.subplot(0).setYlims(-7, 30)
        # Assemble ratio plot.
        plot.subplot(0).setYlabel("N_{events}")
        plot.scaleYLabelSize(0.8)
        plot.scaleYTitleOffset(1.1)
        plot.subplot(0).setXlabel(styles.x_label_dict["mmt"]["pt_1"])
        plot.subplot(0).Draw(["tau", "lep2", "lep2tau"])
        plot.add_legend(width=0.15, height=0.15, pos=3)
        plot.legend(0).add_entry(0, "tau", "#tau anti iso", "l")
        plot.legend(0).add_entry(0, "lep2", "#mu anti iso", "l")
        plot.legend(0).add_entry(0, "lep2tau", "#tau+#mu anti iso", "l")
        plot.legend(0).Draw()
        plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
        plot.DrawCMS(position="outside")
        plot.save(output + "jetfake_contributions" + ".png")
        plot.save(output + "jetfake_contributions" + ".pdf")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
