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
        "-in", "--input", type=str, required=True, help="Input root files."
    )
    parser.add_argument(
        "-out", "--plot_output", type=str, required=True, help="plot output path"
    )
    parser.add_argument("-c", "--channel", type=str, required=True, help="channel")
    return parser.parse_args()


def main(args):
    channel = args.channel
    output = args.plot_output
    rfile = R.TFile("{}".format(args.input), "READ")
    nom = rfile.Get(
        "jetFakes#{ch}-jetFakes-misc#Nominal#predicted_max_value".format(ch=channel)
    )
    tau = rfile.Get(
        "jetFakes#{ch}-jetFakes-misc#tau_anti_iso#predicted_max_value".format(
            ch=channel
        )
    )
    if channel == "emt":
        # lep1 = rfile.Get(
        #     "jetFakes#{ch}-jetFakes-misc#ele1_anti_isoid#predicted_max_value".format(ch=channel)
        # )
        lep2 = rfile.Get(
            "jetFakes#{ch}-jetFakes-misc#mu2_anti_isoid#predicted_max_value".format(
                ch=channel
            )
        )
        # lep1tau = rfile.Get(
        #     "jetFakes#{ch}-jetFakes-misc#ele1tau_anti_isoid#predicted_max_value".format(ch=channel)
        # )
        lep2tau = rfile.Get(
            "jetFakes#{ch}-jetFakes-misc#mu2tau_anti_isoid#predicted_max_value".format(
                ch=channel
            )
        )
    elif channel == "met":
        # lep1 = rfile.Get(
        #     "jetFakes#{ch}-jetFakes-misc#mu1_anti_isoid#predicted_max_value".format(ch=channel)
        # )
        lep2 = rfile.Get(
            "jetFakes#{ch}-jetFakes-misc#ele2_anti_isoid#predicted_max_value".format(
                ch=channel
            )
        )
        # lep1tau = rfile.Get(
        #     "jetFakes#{ch}-jetFakes-misc#mu1tau_anti_isoid#predicted_max_value".format(ch=channel)
        # )
        lep2tau = rfile.Get(
            "jetFakes#{ch}-jetFakes-misc#ele2tau_anti_isoid#predicted_max_value".format(
                ch=channel
            )
        )
    elif channel == "mmt":
        lep2 = rfile.Get(
            "jetFakes#{ch}-jetFakes-misc#mu2_anti_isoid#predicted_max_value".format(
                ch=channel
            )
        )
        lep2tau = rfile.Get(
            "jetFakes#{ch}-jetFakes-misc#mu2tau_anti_isoid#predicted_max_value".format(
                ch=channel
            )
        )
    if channel in ["emt", "met", "mmt"]:
        plot = dd.Plot([0.1, 0.1], "ModTDR", r=0.04, l=0.14)
        plot.add_hist(tau, "tau", "tau")
        # plot.add_hist(lep1, "lep1", "lep1")
        plot.add_hist(lep2, "lep2", "lep2")
        # plot.add_hist(lep1tau, "lep1tau", "lep1tau")
        plot.add_hist(lep2tau, "lep2tau", "lep2tau")
        plot.setGraphStyle("tau", "hist", fillcolor=R.TColor.GetColor("#2a9d8f"))
        plot.add_hist(nom, "nom", "nom")
        plot.setGraphStyle(
            "nom", "hist", linecolor=R.TColor.GetColor("#283618"), linewidth=2
        )
        # plot.setGraphStyle("lep1", "hist", fillcolor=R.TColor.GetColor("#264653"))
        if channel in ["emt", "mmt"]:
            plot.setGraphStyle("lep2", "hist", fillcolor=R.TColor.GetColor("#e9c46a"))
            plot.setGraphStyle(
                "lep2tau", "hist", fillcolor=R.TColor.GetColor("#003049")
            )
        else:
            plot.setGraphStyle("lep2", "hist", fillcolor=R.TColor.GetColor("#f4a261"))
            plot.setGraphStyle(
                "lep2tau", "hist", fillcolor=R.TColor.GetColor("#003049")
            )

        # plot.setGraphStyle(
        #     "lep1tau", "hist", fillcolor=R.TColor.GetColor("#f4a261")
        # )
        # y_max = 1.5 * max(
        #     [
        #         plot.subplot(0).get_hist("tau").GetMaximum(),
        #         plot.subplot(0).get_hist("lep1").GetMaximum(),
        #         plot.subplot(0).get_hist("lep2").GetMaximum(),
        #     ]
        # )
        # y_min = 1.5 * min(
        #     [
        #         plot.subplot(0).get_hist("lep1tau").GetMinimum(),
        #         plot.subplot(0).get_hist("lep2tau").GetMinimum(),
        #     ]
        # )
        if channel == "emt":
            plot.subplot(0).setYlims(-8, 25)
        else:
            plot.subplot(0).setYlims(-10, 35)
        plot.subplot(0).setYlabel("N_{events}")
        if channel == "emt":
            # plot.subplot(0).setXlabel(styles.x_label_dict["emt"]["predicted_max_value"])
            plot.subplot(0).setXlabel("predicted_max_value")
        else:
            # plot.subplot(0).setXlabel(styles.x_label_dict["met"]["predicted_max_value"])
            plot.subplot(0).setXlabel("predicted_max_value")
        plot.scaleYLabelSize(0.8)
        plot.scaleYTitleOffset(1.1)
        plot.add_legend(width=0.15, height=0.15, pos=1)
        plot.legend(0).add_entry(0, "tau", "jet#rightarrow#tau fakes", "f")
        if channel in ["emt", "mmt"]:
            plot.create_stack(["tau", "lep2"], "stack")
            plot.create_stack(["lep2tau"], "stack2")
            plot.subplot(0).Draw(["stack", "stack2", "nom"])
            # plot.legend(0).add_entry(0, "lep1", "e anti iso", "f")
            plot.legend(0).add_entry(0, "lep2", "jet#rightarrow#mu fakes", "f")
            # plot.legend(0).add_entry(0, "lep1tau", "#tau+e anti iso", "f")
            plot.legend(0).add_entry(0, "lep2tau", "double counting", "f")
            plot.legend(0).add_entry(0, "nom", "Total yield from jet fakes", "l")
            plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
            plot.DrawCMS(position="outside", own_work=True)
        else:
            plot.subplot(0).setYlims(
                1.2 * plot.subplot(0).get_hist("lep2tau").GetMinimum(),
                1.2 * plot.subplot(0).get_hist("lep2").GetMaximum(),
            )
            plot.create_stack(["tau", "lep2"], "stack")
            plot.create_stack(["lep2tau"], "stack2")
            plot.subplot(0).Draw(["stack", "stack2", "nom"])
            plot.legend(0).add_entry(0, "lep2", "jet#rightarrowe fakes", "f")
            # plot.legend(0).add_entry(0, "lep1", "#mu anti iso", "l")
            plot.legend(0).add_entry(0, "lep2tau", "double counting", "f")
            plot.legend(0).add_entry(0, "nom", "Total yield from jet fakes", "l")
            plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
            plot.DrawCMS(position="outside", own_work=True)
            # plot.legend(0).add_entry(0, "lep1tau", "#tau+#mu anti iso", "l")
        plot.legend(0).Draw()
        plot.save(output + "jetfake_contributions" + ".png")
        plot.save(output + "jetfake_contributions" + ".pdf")
    # elif channel == "mmt":
    #     print("Hihihih")
    #     total_bkg = rfile.Get(
    #         "jetFakes#{ch}-jetFakes-misc#tau_anti_iso#predicted_max_value".format(
    #             ch=channel
    #         )
    #     ).Clone()
    #     total_bkg.Add(lep2)
    #     total_bkg.Add(lep2tau)

    #     plot = dd.Plot([0.1, 0.1], "ModTDR", r=0.04, l=0.14)

    #     plot.create_stack(["tau", "lep2"], "stack")
    #     plot.subplot(0).setYlims(y_min, y_max)
    #     plot.add_hist(total_bkg, "total_bkg")
    #     plot.add_hist(tau, "tau", "tau")
    #     plot.add_hist(lep2, "lep2", "lep2")
    #     plot.add_hist(lep2tau, "lep2tau", "lep2tau")
    #     plot.add_hist(nom, "nom", "nom")
    #     # Assemble ratio plot.
    #     plot.subplot(0).setYlabel("N_{events}")
    #     plot.scaleYLabelSize(0.8)
    #     plot.scaleYTitleOffset(1.1)
    #     y_max = 1.2 * plot.subplot(0).get_hist("stack").GetMaximum()
    #     y_min = 1.2 * min(
    #         [
    #             plot.subplot(0).get_hist("lep2tau").GetMinimum(),
    #         ]
    #     )

    #     # plot.subplot(0).setXlabel(styles.x_label_dict["mmt"]["predicted_max_value"])
    #     plot.subplot(0).setXlabel("predicted_max_value")
    #     plot.subplot(0).Draw(["stack", "lep2tau", "nom"])
    #     plot.add_legend(width=0.15, height=0.15, pos=1)
    #     plot.legend(0).add_entry(0, "tau", "jet#rightarrow#tau fakes", "f")
    #     plot.legend(0).add_entry(0, "lep2", "jet#rightarrow#mu fakes", "f")
    #     plot.legend(0).add_entry(0, "lep2tau", "double counting", "f")
    #     plot.legend(0).add_entry(0, "nom", "Total yield from jet fakes", "l")
    #     plot.subplot(0).setYlims(y_min, 50)
    #     plot.legend(0).Draw()
    #     plot.DrawLumi("59.8 fb^{-1} (2018, 13 TeV)")
    #     plot.DrawCMS(position="outside", own_work=True)
    #     plot.save(output + "jetfake_contributions" + ".png")
    #     plot.save(output + "jetfake_contributions" + ".pdf")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
