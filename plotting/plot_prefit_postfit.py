#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Dumbledraw.dumbledraw as dd
import Dumbledraw.rootfile_parser as rootfile_parser
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
    parser.add_argument("-e", "--era", type=str, required=True, help="Era")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="ROOT file with shapes of processes",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="outputfile",
    )
    parser.add_argument(
        "--channels",
        type=str,
        default=None,
        help="Enable control plotting for given variable",
    )
    parser.add_argument(
        "--prefit", action="store_true", help="if true, prefit shapes, else postfit"
    )
    parser.add_argument(
        "--tag", type=str, default=None, help="plots are stored in plots/tag/"
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="category of the fit. options: [pt_W_plus, pt_W_minus, m_tt_plus, m_tt_minus]",
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
    channel = info["channel"]
    era = args.era
    cat = args.category
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
    category_dict = {
        "pt_W_plus": "1",
        "m_tt_plus": "2",
        "pt_W_minus": "3",
        "m_tt_minus": "4",
        "m_tt_control": "5",
    }
    VVV_processes = ["WWW", "WWZ", "WZZ", "ZZZ"]

    bkg_processes = [
        "jetFakes",
        "ggZZ",
        "rem_VH",
        "rem_ttbar",
        "VVV",
        "ZZ",
        "WZ",
        "ZH",
    ]
    signal_processes = [
        "WHplus",
        "WHminus",
    ]
    if args.prefit:
        fittype = "prefit"
    else:
        fittype = "postfit"
    print(cat)
    rootfile = rootfile_parser.Rootfile_parser(args.input, fittype)
    print(rootfile)
    legend_bkg_processes = copy.deepcopy(bkg_processes)
    legend_bkg_processes.reverse()
    legend_sig_processes = copy.deepcopy(signal_processes)
    # create plot
    width = 600
    plot = dd.Plot([0.3, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14, width=width)
    # get background histograms
    total_bkg = None
    for index, process in enumerate(bkg_processes):
        if index == 0:
            total_bkg = rootfile.get(era, channel, category_dict[cat], process).Clone()
            plot.add_hist(
                rootfile.get(era, channel, category_dict[cat], process),
                process,
                "bkg",
            )
        elif "VVV" in process:
            for v, vvv in enumerate(VVV_processes):
                if v == 0:
                    triboson = rootfile.get(
                        era, channel, category_dict[cat], vvv
                    ).Clone()
                else:
                    triboson.Add(rootfile.get(era, channel, category_dict[cat], vvv))
            total_bkg.Add(triboson)
            plot.add_hist(
                triboson,
                process,
                "bkg",
            )
        else:
            total_bkg.Add(rootfile.get(era, channel, category_dict[cat], process))
            plot.add_hist(
                rootfile.get(era, channel, category_dict[cat], process),
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
            era, channel, category_dict[cat], signal
        ).Clone()
    for signal in sig_dict:
        plot.subplot(0).add_hist(sig_dict[signal], signal)
        plot.subplot(2).add_hist(sig_dict[signal], signal)
        plot.subplot(0).setGraphStyle(
            signal, "hist", linecolor=styles.color_dict[signal], linewidth=2
        )
    # add data hist
    plot.add_hist(
        rootfile.get(era, channel, category_dict[cat], "data_obs"),
        "data_obs",
    )

    plot.subplot(0).get_hist("data_obs").GetXaxis().SetMaxDigits(4)

    # data graph style
    plot.subplot(0).setGraphStyle("data_obs", "e0")
    plot.subplot(2).setGraphStyle("data_obs", "e0")

    # stack background processess
    plot.create_stack(bkg_processes, "stack")

    # normalize stacks by bin-width
    # if args.normalize_by_bin_width:
    #     plot.subplot(0).normalizeByBinWidth()
    #     plot.subplot(1).normalizeByBinWidth()

    # add signal to bkg in ratio plot
    for signal in sig_dict:
        plot.subplot(2).get_hist(signal).Add(plot.subplot(2).get_hist("total_bkg"))
        plot.subplot(2).setGraphStyle(
            signal, "hist", linecolor=styles.color_dict[signal], linewidth=3
        )
    # normalize ratio plot
    plot.subplot(2).normalize(
        ["total_bkg", "data_obs", "WHplus", "WHminus"], "total_bkg"
    )
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
    if "m_tt" in cat:
        plot.subplot(2).setXlabel("m(#tau#tau) / GeV")
    elif "pt_W" in cat:
        plot.subplot(2).setXlabel("p_{T}(W) / GeV")
    else:
        plot.subplot(2).setXlabel(cat)
    plot.subplot(0).setYlabel("N_{events}")

    plot.subplot(2).setYlabel("")
    plot.subplot(2).setGrid()
    plot.scaleYLabelSize(0.8)
    plot.scaleYTitleOffset(1.1)

    # draw subplots. Argument contains names of objects to be drawn in corresponding order.

    procs_to_draw = ["stack", "total_bkg", "data_obs", "WHplus", "WHminus"]
    plot.subplot(0).Draw(procs_to_draw)
    plot.subplot(2).Draw(["total_bkg", "WHplus", "WHminus", "data_obs"])
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
    if args.prefit == True:
        prepost = "prefit"
    else:
        prepost = "postfit"
    if not os.path.exists(
        "{output}/{pre_post}".format(output=args.output, pre_post=prepost)
    ):
        os.makedirs("{output}/{pre_post}".format(output=args.output, pre_post=prepost))
    plot.save(
        "{output}/{pre_post}/{cat}.{format}".format(
            output=args.output, pre_post=prepost, cat=cat, format="pdf"
        )
    )
    plot.save(
        "{output}/{pre_post}/{cat}.{format}".format(
            output=args.output, pre_post=prepost, cat=cat, format="png"
        )
    )


if __name__ == "__main__":
    args = parse_arguments()
    setup_logging("{}_plot_shapes.log".format(args.era), logging.DEBUG)
    channels = args.channels.split(",")
    infolist = []
    for ch in channels:
        infolist.append({"args": args, "channel": ch})
    pool = Pool(1)
    pool.map(main, infolist)
    # for info in infolist:
    #     main(info)
