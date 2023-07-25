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
        "-mc", "--mc", type=str, required=True, help="Input root files."
    )
    parser.add_argument(
        "-data", "--data", type=str, required=True, help="Input root files."
    )
    parser.add_argument(
        "-out", "--plot_output", type=str, required=True, help="plot output path"
    )
    parser.add_argument("-c", "--channel", type=str, required=True, help="channel")
    return parser.parse_args()


def comparison_plot(data, mc, quantity, output):
    plot = dd.Plot([0.3, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14)
    plot.add_hist(data, "data", "data")
    plot.add_hist(mc, "mc_col", "mc_col")
    plot.add_hist(mc, "mc", "mc")
    plot.add_hist(mc, "mc_unc", "mc_unc")
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
    y_max = 1.5 * max(
        plot.subplot(0).get_hist("data").GetMaximum(),
        plot.subplot(0).get_hist("mc").GetMaximum(),
    )
    plot.subplot(0).setYlims(0, y_max)
    # Assemble ratio plot.
    plot.subplot(2).normalize(["data", "mc", "mc_unc"], "mc")
    plot.subplot(2).setXlabel("{}".format(quantity))
    plot.subplot(0).setYlabel("N_{events}")
    plot.subplot(2).setYlabel("ratio to")
    # plot.setXlims(-4, 4)
    plot.subplot(2).setYlims(0.6, 1.4)
    plot.scaleYLabelSize(0.8)
    plot.scaleYTitleOffset(1.1)
    plot.subplot(2).setXlabel(styles.x_label_dict["emt"][quantity])
    plot.subplot(0).Draw(["mc_col", "mc", "mc_unc", "data"])
    plot.subplot(2).Draw(["data", "mc", "mc_unc"])
    plot.subplot(2).setGrid()
    plot.add_legend(width=0.15, height=0.15, pos=2)
    plot.legend(0).add_entry(0, "data", "data", "l")
    plot.legend(0).add_entry(0, "mc_col", "mc", "f")
    plot.legend(0).Draw()
    plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
    plot.DrawCMS(position="outside")
    plot.save(output + "closure_data_mc_{quantity}".format(quantity=quantity) + ".png")
    plot.save(output + "closure_data_mc_{quantity}".format(quantity=quantity) + ".pdf")
    return plot


def main(args):
    channel = args.channel
    output = args.plot_output
    rfile_jf_data = R.TFile("{}".format(args.data), "READ")
    rfile_jf_mc = R.TFile("{}".format(args.mc), "READ")
    pt_3_jf_data = rfile_jf_data.Get(
        "jetFakes#{ch}-jetFakes#Nominal#pt_3".format(ch=channel)
    )
    pt_3_jf_mc = rfile_jf_mc.Get(
        "jetFakes#{ch}-jetFakes#Nominal#pt_3".format(ch=channel)
    )
    pt_w_jf_data = rfile_jf_data.Get(
        "jetFakes#{ch}-jetFakes#Nominal#pt_W_lt".format(ch=channel)
    )
    pt_w_jf_mc = rfile_jf_mc.Get(
        "jetFakes#{ch}-jetFakes#Nominal#pt_W_lt".format(ch=channel)
    )
    for quantity in [
        (pt_3_jf_data, pt_3_jf_mc, "pt_3"),
        (pt_w_jf_data, pt_w_jf_mc, "pt_W_lt"),
    ]:
        comparison_plot(quantity[0], quantity[1], quantity[2], output)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
