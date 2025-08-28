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

# from root_numpy import hist2array
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
        "--input_ggzh", type=str, required=True, help="Input root files."
    )
    parser.add_argument("--input", type=str, required=True, help="Input root files.")
    parser.add_argument(
        "-out", "--plot_output", type=str, required=True, help="plot output path"
    )
    parser.add_argument("-c", "--channel", type=str, required=True, help="channel")
    return parser.parse_args()


def main(args):
    channel = args.channel
    output = args.plot_output
    procs_to_subtract = {
        "ggzz": "ggZZ#{ch}-VV-sig#Nominal#predicted_max_value".format(ch=channel),
        "zz": "ZZ#{ch}-VV-sig#Nominal#predicted_max_value".format(ch=channel),
        "wz": "WZ#{ch}-VV-sig#Nominal#predicted_max_value".format(ch=channel),
        "vvv": "VVV#{ch}-VVV-sig#Nominal#predicted_max_value".format(ch=channel),
        "ggzh": "ggZH#{ch}-H-sig#Nominal#predicted_max_value".format(ch=channel),
        "rem_ttbar": "rem_ttbar#{ch}-TT-sig#Nominal#predicted_max_value".format(
            ch=channel
        ),
    }

    rfile_ggzh = R.TFile("{}".format(args.input_ggzh), "READ")
    rfile = R.TFile("{}".format(args.input), "READ")
    ggzh = rfile_ggzh.Get(
        "ggZH#{ch}-H-sig#Nominal#predicted_max_value".format(ch=channel)
    )
    zh = rfile.Get("ZH#{ch}-H-sig#Nominal#predicted_max_value".format(ch=channel))
    WH_tautau_minus = rfile.Get(
        "WH_htt_minus#{ch}-H-sig#Nominal#predicted_max_value".format(ch=channel)
    )
    WH_tautau_plus = rfile.Get(
        "WH_htt_plus#{ch}-H-sig#Nominal#predicted_max_value".format(ch=channel)
    )
    tot_bkg = zh.Clone()
    for proc in procs_to_subtract.values():
        print(proc)
        temp_hist = rfile.Get(proc)
        print(temp_hist)
        tot_bkg.Add(temp_hist, 1)
    sig = WH_tautau_minus.Clone()
    sig.Add(WH_tautau_plus, 1)

    print("-----------")
    print(args.input_ggzh)
    print("integral ggzh", ggzh.Integral())
    print("integral ggzh/whtt", ggzh.Integral() / sig.Integral())
    print("-----------")
    print("significanc sig/np.sqrt(tot.bkg)")
    for bin_i in range(1, sig.GetNbinsX() + 1):
        print(sig.GetBinContent(bin_i) / np.sqrt(tot_bkg.GetBinContent(bin_i)))
    print("-----------")
    print("bin fraction ggzh/tot.bkg")
    for bin_i in range(1, sig.GetNbinsX() + 1):
        print(ggzh.GetBinContent(bin_i) / tot_bkg.GetBinContent(bin_i))
    print("-----------")
    print("bin fraction ggzh/sig")
    for bin_i in range(1, sig.GetNbinsX() + 1):
        print(ggzh.GetBinContent(bin_i) / sig.GetBinContent(bin_i))
    print("-----------")
    print("significance change 1-[sig/np.sqrt(tot.bkg+ggzh)]/[sig/np.sqrt(tot.bkg)]")
    for bin_i in range(1, sig.GetNbinsX() + 1):
        print(
            1
            - (
                sig.GetBinContent(bin_i)
                / np.sqrt(tot_bkg.GetBinContent(bin_i) + ggzh.GetBinContent(bin_i))
            )
            / (sig.GetBinContent(bin_i) / np.sqrt(tot_bkg.GetBinContent(bin_i)))
        )
    print("-----------")
    print("bin ratio ggzh/zh to compare shape")
    for bin_i in range(1, sig.GetNbinsX() + 1):
        print(ggzh.GetBinContent(bin_i) / zh.GetBinContent(bin_i))

    yield_factor = (ggzh.Integral() + zh.Integral()) / zh.Integral()
    print("-----------")
    print(
        "deviation from the total yield difference ggzh between zh to compare shape. yield factor:",
        yield_factor,
    )
    for bin_i in range(1, sig.GetNbinsX() + 1):
        print(
            (
                (ggzh.GetBinContent(bin_i) + zh.GetBinContent(bin_i))
                / zh.GetBinContent(bin_i)
            )
            / yield_factor
        )
    # ggzh.Scale(1.0 / ggzh.Integral())
    # zh.Scale(1.0 / zh.Integral())
    plot = plot = dd.Plot([0.28, [0.2, 0.23]], "ModTDR", r=0.04, l=0.14, width=600)
    plot.add_hist(ggzh, "ggzh", "ggzh")
    plot.add_hist(ggzh, "ggzh_ratio", "ggzh_ratio")
    plot.setGraphStyle("ggzh_ratio", "e0")
    plot.setGraphStyle(
        "ggzh", "hist", linecolor=R.TColor.GetColor("#264653"), linewidth=3
    )
    # plot.add_hist(lep1, "lep1", "lep1")
    plot.add_hist(zh, "zh", "zh")
    plot.setGraphStyle(
        "zh", "hist", linecolor=R.TColor.GetColor("#2a9d8f"), linewidth=3
    )
    # plot.add_hist(lep1tau, "lep1tau", "lep1tau")
    plot.add_hist(WH_tautau_minus, "WH_tautau_minus", "WH_tautau_minus")
    plot.setGraphStyle(
        "WH_tautau_minus", "hist", linecolor=R.TColor.GetColor("#e9c46a"), linewidth=3
    )
    plot.add_hist(WH_tautau_plus, "WH_tautau_plus", "WH_tautau_plus")
    plot.setGraphStyle(
        "WH_tautau_plus", "hist", linecolor=R.TColor.GetColor("#e76f51"), linewidth=3
    )
    plot.add_hist(tot_bkg, "tot_bkg", "tot_bkg")
    plot.setGraphStyle(
        "tot_bkg", "hist", linecolor=R.TColor.GetColor("#fcb9b2"), linewidth=3
    )
    ratio_hist = ggzh.Clone()
    ratio_hist.Divide(zh)
    plot.add_hist(ratio_hist, "ratio_hist", "ratio_hist")
    plot.setGraphStyle(
        "ratio_hist", "hist", linecolor=R.TColor.GetColor("#000000"), linewidth=1
    )
    # plot.subplot(0).setYlims(0, plot.subplot(0).get_hist("tot_bkg").GetMaximum() * 1.2)
    plot.subplot(2)._nydivisions = (3, 3, 0)  #
    plot.subplot(0).setYlims(0, 0.3)
    # plot.subplot(2).setYlims(0.1, 0.47)
    plot.subplot(0).setYlabel("N_{events}")
    plot.subplot(2).setXlabel("predicted_max_value")
    # plot.subplot(2).setYlabel("")
    plot.subplot(2).setYlabel("ggzh/zh")
    plot.scaleYLabelSize(0.8)
    plot.scaleYTitleOffset(1.1)
    plot.subplot(2).setGrid()
    plot.subplot(2).Draw(["ratio_hist"])
    plot.scaleYLabelSize(0.8)
    plot.scaleYTitleOffset(1.1)
    plot.subplot(0).Draw(["ggzh", "zh"])
    plot.add_legend(width=0.15, height=0.15, pos=1)
    plot.legend(0).add_entry(0, "ggzh", "ggzh", "f")
    plot.legend(0).add_entry(0, "zh", "zh", "f")
    # plot.legend(0).add_entry(0, "WH_tautau_minus", "WH_htt_minus", "f")
    # plot.legend(0).add_entry(0, "WH_tautau_plus", "WH_htt_plus", "f")
    # plot.legend(0).add_entry(0, "tot_bkg", "tot_bkg", "f")
    plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
    plot.DrawCMS(position="outside", own_work=True)
    plot.legend(0).Draw()
    # plot.subplot(2).normalize(["ggzh_ratio", "zh"], "zh")

    # Access the underlying matplotlib axis
    plot.save(output + "ggZH_contribution" + ".png")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
