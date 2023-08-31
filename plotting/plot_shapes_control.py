#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Dumbledraw.dumbledraw as dd
import Dumbledraw.rootfile_parser_inputshapes_wh as rootfile_parser
import Dumbledraw.styles as styles
import ROOT
import argparse
import copy
import yaml
import os

import logging

logger = logging.getLogger("")
from multiprocessing import Pool
from multiprocessing import Process
import multiprocessing


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Plot categories using Dumbledraw from shapes produced by shape-producer module."
    )
    parser.add_argument(
        "-l", "--linear", action="store_true", help="Enable linear x-axis"
    )
    parser.add_argument("-e", "--era", type=str, required=True, help="Era")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="ROOT file with shapes of processes",
    )
    parser.add_argument(
        "--variables",
        type=str,
        default=None,
        help="Enable control plotting for given variable",
    )
    parser.add_argument(
        "--category-postfix",
        type=str,
        default=None,
        help="Enable control plotting for given category_postfix. Structure of a category: <variable>_<postfix>",
    )
    parser.add_argument(
        "--channels",
        type=str,
        default=None,
        help="Enable control plotting for given variable",
    )
    parser.add_argument(
        "--normalize-by-bin-width",
        action="store_true",
        help="Normelize plots by bin width",
    )
    parser.add_argument(
        "--fake-factor", action="store_true", help="Fake factor estimation method used"
    )
    parser.add_argument(
        "--embedding", action="store_true", help="Fake factor estimation method used"
    )
    parser.add_argument(
        "--draw-jet-fake-variation",
        type=str,
        default=None,
        help="Draw variation of jetFakes or QCD in derivation region.",
    )
    parser.add_argument(
        "--blinded", action="store_true", help="if true, no data is plottet"
    )
    parser.add_argument(
        "--simulation", action="store_true", help="if true, no data is plottet"
    )
    parser.add_argument(
        "--closure_test", action="store_true", help="if true, no data is plottet"
    )
    parser.add_argument(
        "--tag", type=str, default=None, help="plots are stored in plots/tag/"
    )

    return parser.parse_args()


def setup_logging(output_file, level=logging.DEBUG):
    logger.setLevel(level)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(output_file, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def main(info):
    args = info["args"]
    variable = info["variable"]
    channel = info["channel"]
    channel_dict = {
        "ee": "#font[42]{#scale[0.85]{ee}}",
        "em": "#scale[0.85]{e}#mu",
        "emt": "#font[42]{#scale[0.85]{e}}#mu#tau_{#font[42]{h}}",
        "met": "#font[42]{#mu#scale[0.85]{e}#tau_{#font[42]{h}}}",
        "mmt": "#font[42]{#mu#mu#tau_{#font[42]{h}}}",
        "mtt": "#font[42]{#mu#tau_{#font[42]{h}}#tau_{#font[42]{h}}}",
        "ett": "#font[42]{#scale[0.85]{e}#tau_{#font[42]{h}}#tau_{#font[42]{h}}}",
        "mm": "#mu#mu",
        "mt": "#mu#tau_{#font[42]{h}}",
        "tt": "#tau_{#font[42]{h}}#tau_{#font[42]{h}}",
    }
    if args.linear == True:
        split_value = 0.1
    else:
        if args.normalize_by_bin_width:
            split_value = 10001
        else:
            split_value = 101

    split_dict = {
        c: split_value
        for c in ["met", "emt", "mmt", "ett", "mtt", "et", "mt", "tt", "em", "mm"]
    }
    VVV_processes = ["WWW", "WWZ", "WZZ", "ZZZ"]

    if args.simulation:
        bkg_processes = [
            "TT",
            "DY",
            "Wjets",
            "rem_VV",
            "ggZZ",
            "VHWW",
            "TTV",
            "VVV",
            "ZZ",
            "WZ",
        ]
    elif args.closure_test:
        bkg_processes = [
            "TT",
            "DY",
            "Wjets",
            "rem_VV",
        ]
    else:
        bkg_processes = [
            "jetFakes",
            "ggZZ",
            "VHWW",
            "TTV",
            "VVV",
            "ZZ",
            "WZ",
        ]
    signal_processes = [
        "WHplus",
        "WHminus",
    ]
    if "2016" in args.era:
        era = "Run2016"
    elif "2017" in args.era:
        era = "Run2017"
    elif "2018" in args.era:
        era = "Run2018"
    else:
        logger.critical("Era {} is not implemented.".format(args.era))
        raise Exception

    rootfile = rootfile_parser.Rootfile_parser(args.input, variable)
    legend_bkg_processes = copy.deepcopy(bkg_processes)
    legend_bkg_processes.reverse()
    legend_sig_processes = copy.deepcopy(signal_processes)
    # create plot
    width = 600
    if args.linear == True:
        plot = dd.Plot([0.3, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14, width=width)
    else:
        plot = dd.Plot([0.5, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14, width=width)

    # get background histograms
    total_bkg = None
    if args.draw_jet_fake_variation is None:
        stype = "Nominal"
    else:
        stype = args.draw_jet_fake_variation
    for index, process in enumerate(bkg_processes):
        if index == 0:
            total_bkg = rootfile.get(
                channel, process, args.category_postfix, shape_type=stype
            ).Clone()
            plot.add_hist(
                rootfile.get(channel, process, args.category_postfix, shape_type=stype),
                process,
                "bkg",
            )
        elif "VVV" in process:
            for v, vvv in enumerate(VVV_processes):
                if v == 0:
                    triboson = rootfile.get(
                        channel, vvv, args.category_postfix, shape_type=stype
                    ).Clone()
                else:
                    triboson.Add(
                        rootfile.get(
                            channel, vvv, args.category_postfix, shape_type=stype
                        )
                    )
            total_bkg.Add(triboson)
            plot.add_hist(
                triboson,
                process,
                "bkg",
            )
        else:
            total_bkg.Add(
                rootfile.get(channel, process, args.category_postfix, shape_type=stype)
            )
            plot.add_hist(
                rootfile.get(channel, process, args.category_postfix, shape_type=stype),
                process,
                "bkg",
            )

        plot.setGraphStyle(process, "hist", fillcolor=styles.color_dict[process])

    plot.add_hist(total_bkg, "total_bkg")
    plot.setGraphStyle(
        "total_bkg", "e2", markersize=0, fillcolor=styles.color_dict["unc"], linecolor=0
    )
    sig_dict = {}
    for signal in signal_processes:
        sig_dict[signal] = rootfile.get(
            channel, signal, args.category_postfix, shape_type=stype
        ).Clone()
    signal_scale = 10
    for signal in sig_dict:
        sig_dict[signal].Scale(signal_scale)
        plot.subplot(0).add_hist(sig_dict[signal], signal)
        plot.subplot(2).add_hist(sig_dict[signal], signal)
        plot.subplot(0).setGraphStyle(
            signal, "hist", linecolor=styles.color_dict[signal], linewidth=2
        )
        plot.subplot(2).setGraphStyle(
            signal, "hist", linecolor=styles.color_dict[signal], linewidth=2
        )
    # add data hist
    if args.closure_test:
        plot.add_hist(
            rootfile.get(channel, "jetFakes", args.category_postfix, shape_type=stype),
            "data_obs",
        )
    else:
        plot.add_hist(
            rootfile.get(channel, "data", args.category_postfix, shape_type=stype),
            "data_obs",
        )

    plot.subplot(0).get_hist("data_obs").GetXaxis().SetMaxDigits(4)
    if args.blinded:
        plot.subplot(0).setGraphStyle("data_obs", "e0", markersize=0, linewidth=0)
        plot.subplot(2).setGraphStyle("data_obs", "e0", markersize=0, linewidth=0)
    else:
        plot.subplot(0).setGraphStyle("data_obs", "e0")
        plot.subplot(2).setGraphStyle("data_obs", "e0")

    # stack background processess
    plot.create_stack(bkg_processes, "stack")
    plot.subplot(2).normalize(["total_bkg", "data_obs"], "total_bkg")
    # normalize stacks by bin-width
    if args.normalize_by_bin_width:
        plot.subplot(0).normalizeByBinWidth()
        plot.subplot(1).normalizeByBinWidth()

    # set the size of the y axis
    y_max = 1.6 * max(
        plot.subplot(0).get_hist("data_obs").GetMaximum(),
        plot.subplot(0).get_hist("total_bkg").GetMaximum(),
    )
    # set axes limits and labels
    plot.subplot(0).setYlims(
        0,
        y_max,
    )
    plot.subplot(2).setYlims(
        0.1,
        2.1,
    )
    if args.linear != True:
        plot.subplot(1).setYlims(0.1, split_dict[channel])
        plot.subplot(1).setYlabel("")  # otherwise number labels are not drawn on axis
        plot.subplot(1).setLogY()
    if variable != None:
        if variable in styles.x_label_dict[channel]:
            x_label = styles.x_label_dict[channel][variable]
        else:
            x_label = variable
        plot.subplot(2).setXlabel(x_label)
    else:
        plot.subplot(2).setXlabel("NN output")
    if args.normalize_by_bin_width:
        plot.subplot(0).setYlabel("N/(bin width) (1/GeV)")
    else:
        plot.subplot(0).setYlabel("N_{events}")

    plot.subplot(2).setYlabel("")
    plot.subplot(2).setGrid()
    plot.scaleYLabelSize(0.8)
    plot.scaleYTitleOffset(1.1)

    # draw subplots. Argument contains names of objects to be drawn in corresponding order.

    procs_to_draw = ["stack", "total_bkg", "data_obs", "WHplus", "WHminus"]
    plot.subplot(0).Draw(procs_to_draw)
    plot.subplot(2).Draw(["total_bkg", "data_obs"])
    # create legends
    for i in range(2):
        plot.add_legend(width=0.625, height=0.15)
        for process in legend_bkg_processes:
            plot.legend(i).add_entry(
                0,
                process,
                styles.legend_label_dict[process],
                "f",
            )
        for signal in legend_sig_processes:
            plot.legend(i).add_entry(
                0,
                signal,
                styles.legend_label_dict[signal],
                "f",
            )
        plot.legend(i).add_entry(0, "total_bkg", "Bkg. stat. unc.", "f")
        if args.closure_test:
            plot.legend(i).add_entry(
                0, "data_obs", "jet fake estimation method", "PE2L"
            )
        else:
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
    plot.DrawCMS(thesisstyle=True, preliminary=False)
    if "2016" in args.era:
        plot.DrawLumi("35.9 fb^{-1} (2016, 13 TeV)")
    elif "2017" in args.era:
        plot.DrawLumi("41.5 fb^{-1} (2017, 13 TeV)")
    elif "2018" in args.era:
        plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
    else:
        logger.critical("Era {} is not implemented.".format(args.era))
        raise Exception

    posChannelCategoryLabelLeft = None
    plot.DrawChannelCategoryLabel(
        "%s" % (channel_dict[channel]),
        begin_left=posChannelCategoryLabelLeft,
    )
    # save plot
    if not args.embedding and not args.fake_factor:
        postfix = "fully_classic"
    if args.embedding and not args.fake_factor:
        postfix = "emb_classic"
    if not args.embedding and args.fake_factor:
        postfix = "classic_ff"
    if args.embedding and args.fake_factor:
        postfix = "emb_ff"
    if args.draw_jet_fake_variation is not None:
        postfix = args.draw_jet_fake_variation
    if not os.path.exists(
        "plots/%s/%s_plots_%s/%s" % (args.tag, args.era, postfix, channel)
    ):
        os.makedirs("plots/%s/%s_plots_%s/%s" % (args.tag, args.era, postfix, channel))
    if args.closure_test:
        plot.save(
            "plots/%s/%s_plots_%s/%s/%s_%s_%s_%s_closure_test.%s"
            % (
                args.tag,
                args.era,
                postfix,
                channel,
                args.era,
                channel,
                variable,
                args.category_postfix,
                "png",
            )
        )
    else:
        plot.save(
            "plots/%s/%s_plots_%s/%s/%s_%s_%s_%s.%s"
            % (
                args.tag,
                args.era,
                postfix,
                channel,
                args.era,
                channel,
                variable,
                args.category_postfix,
                "pdf",
            )
        )
        plot.save(
            "plots/%s/%s_plots_%s/%s/%s_%s_%s_%s.%s"
            % (
                args.tag,
                args.era,
                postfix,
                channel,
                args.era,
                channel,
                variable,
                args.category_postfix,
                "png",
            )
        )


if __name__ == "__main__":
    args = parse_arguments()
    setup_logging("{}_plot_shapes.log".format(args.era), logging.DEBUG)
    variables = args.variables.split(",")
    channels = args.channels.split(",")
    infolist = []

    if not args.embedding and not args.fake_factor:
        postfix = "fully_classic"
    if args.embedding and not args.fake_factor:
        postfix = "emb_classic"
    if not args.embedding and args.fake_factor:
        postfix = "classic_ff"
    if args.embedding and args.fake_factor:
        postfix = "emb_ff"
    for ch in channels:
        for v in variables:
            infolist.append({"args": args, "channel": ch, "variable": v})
    pool = Pool(1)
    pool.map(main, infolist)
    # for info in infolist:
    #     main(info)
