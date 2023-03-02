#!/usr/bin/env python
import argparse
import logging
import os
import pickle
import re
import yaml

from ntuple_processor import Histogram
from ntuple_processor import (
    dataset_from_crownoutput,
    dataset_from_artusoutput,
    Unit,
    UnitManager,
    GraphManager,
    RunManager,
)

from config.shapes.channel_selection import channel_selection
from config.shapes.file_names import files

from config.shapes.process_selection import (
    VV_process_selection,
    VH_process_selection,
    TT_process_selection,
    WWW_process_selection,
    WWZ_process_selection,
    WZZ_process_selection,
    ZZZ_process_selection,
    W_process_selection,
    DY_process_selection,
)

from config.shapes.control_binning import control_binning, minimal_control_plot_set
from config.shapes.variations import (
    anti_iso_ltt,
    anti_iso_llt_tau,
    anti_isoid_ele_2,
    anti_isoid_mu_1,
    anti_isoid_ele_1,
    anti_isoid_mu_2,
    anti_isoid_ele_2_tau,
    anti_isoid_mu_1_tau,
    anti_isoid_ele_1_tau,
    anti_isoid_mu_2_tau,
)

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
    parser = argparse.ArgumentParser(
        description="Produce shapes for the legacy NMSSM analysis."
    )
    parser.add_argument("--era", required=True, type=str, help="Experiment era.")
    parser.add_argument(
        "--channels",
        default=[],
        type=lambda channellist: [channel for channel in channellist.split(",")],
        help="Channels to be considered, seperated by a comma without space",
    )
    parser.add_argument(
        "--directory", required=True, type=str, help="Directory with Artus outputs."
    )
    parser.add_argument(
        "--emt-friend-directory",
        type=str,
        default=[],
        nargs="+",
        help="Directories arranged as Artus output and containing a friend tree for emt.",
    )
    parser.add_argument(
        "--met-friend-directory",
        type=str,
        default=[],
        nargs="+",
        help="Directories arranged as Artus output and containing a friend tree for met.",
    )
    parser.add_argument(
        "--mmt-friend-directory",
        type=str,
        default=[],
        nargs="+",
        help="Directories arranged as Artus output and containing a friend tree for mmt.",
    )
    parser.add_argument(
        "--ett-friend-directory",
        type=str,
        default=[],
        nargs="+",
        help="Directories arranged as Artus output and containing a friend tree for ett.",
    )
    parser.add_argument(
        "--mtt-friend-directory",
        type=str,
        default=[],
        nargs="+",
        help="Directories arranged as Artus output and containing a friend tree for mtt.",
    )
    parser.add_argument(
        "--optimization-level",
        default=2,
        type=int,
        help="Level of optimization for graph merging.",
    )
    parser.add_argument(
        "--num-processes", default=1, type=int, help="Number of processes to be used."
    )
    parser.add_argument(
        "--num-threads", default=1, type=int, help="Number of threads to be used."
    )
    parser.add_argument(
        "--skip-systematic-variations",
        action="store_true",
        help="Do not produce the systematic variations.",
    )
    parser.add_argument(
        "--output-file",
        required=True,
        type=str,
        help="ROOT file where shapes will be stored.",
    )
    parser.add_argument(
        "--control-plots",
        action="store_true",
        help="Produce shapes for control plots. Default is production of analysis shapes.",
    )
    parser.add_argument(
        "--control-plot-set",
        default=minimal_control_plot_set,
        type=lambda varlist: [variable for variable in varlist.split(",")],
        help="Variables the shapes should be produced for.",
    )
    parser.add_argument(
        "--only-create-graphs",
        action="store_true",
        help="Create and optimise graphs and create a pkl file containing the graphs to be processed.",
    )
    parser.add_argument(
        "--process-selection",
        default=None,
        type=lambda proclist: set([process for process in proclist.split(",")]),
        help="Subset of processes to be processed.",
    )
    parser.add_argument(
        "--graph-dir",
        default=None,
        type=str,
        help="Directory the graph file is written to.",
    )
    parser.add_argument(
        "--ntuple_type", default="artus", type=str, help="Options: crown or artus"
    )
    parser.add_argument(
        "--enable-booking-check",
        action="store_true",
        help="Enables check for double actions during booking. Takes long for all variations.",
    )
    return parser.parse_args()


def main(args):
    # Parse given arguments.
    friend_directories = {
        "emt": args.emt_friend_directory,
        "met": args.met_friend_directory,
        "mmt": args.mmt_friend_directory,
        "ett": args.ett_friend_directory,
        "mtt": args.mtt_friend_directory,
    }

    if ".root" in args.output_file:
        output_file = args.output_file
        log_file = args.output_file.replace(".root", ".log")
    else:
        output_file = "{}.root".format(args.output_file)
        log_file = "{}.log".format(args.output_file)

    nominals = {}
    nominals[args.era] = {}
    nominals[args.era]["datasets"] = {}
    nominals[args.era]["units"] = {}

    def get_nominal_datasets(era, channel):
        datasets = dict()

        def filter_friends(dataset, friend):
            if re.match("(gg|qq|tt|w|z|v)h", dataset.lower()):
                if "FakeFactors" in friend or "EMQCDWeights" in friend:
                    return False
            elif re.match("data", dataset.lower()):
                if "crosssection" in friend:
                    return False
            return True

        if "artus" in args.ntuple_type:
            for key, names in files[era][channel].items():
                datasets[key] = dataset_from_artusoutput(
                    key,
                    names,
                    channel + "_nominal",
                    args.directory,
                    [
                        fdir
                        for fdir in friend_directories[channel]
                        if filter_friends(key, fdir)
                    ],
                )
        else:
            for key, names in files[era][channel].items():
                datasets[key] = dataset_from_crownoutput(
                    key,
                    names,
                    args.era,
                    channel,
                    channel + "_nominal",
                    args.directory,
                    [
                        fdir
                        for fdir in friend_directories[channel]
                        if filter_friends(key, fdir)
                    ],
                    validate_samples=True,
                )
        return datasets

    def get_control_units(channel, era, datasets):
        return {
            "data": [
                Unit(
                    datasets["data"],
                    [channel_selection(channel, era)],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "ggzz": [
                Unit(
                    datasets["ggZZ"],
                    [
                        channel_selection(channel, era),
                        VV_process_selection(channel, era),
                        # VV_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "wz": [
                Unit(
                    datasets["WZ"],
                    [
                        channel_selection(channel, era),
                        VV_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "zz": [
                Unit(
                    datasets["ZZ"],
                    [
                        channel_selection(channel, era),
                        VV_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "rem_vh": [
                Unit(
                    datasets["rem_VH"],
                    [
                        channel_selection(channel, era),
                        VH_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "tt": [
                Unit(
                    datasets["TT"],
                    [
                        channel_selection(channel, era),
                        TT_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "rem_ttbar": [
                Unit(
                    datasets["rem_ttbar"],
                    [
                        channel_selection(channel, era),
                        TT_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "www": [
                Unit(
                    datasets["WWW"],
                    [
                        channel_selection(channel, era),
                        WWW_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "wwz": [
                Unit(
                    datasets["WWZ"],
                    [
                        channel_selection(channel, era),
                        WWZ_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "wzz": [
                Unit(
                    datasets["WZZ"],
                    [
                        channel_selection(channel, era),
                        WZZ_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "zzz": [
                Unit(
                    datasets["ZZZ"],
                    [
                        channel_selection(channel, era),
                        ZZZ_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "wh": [
                Unit(
                    datasets["WH"],
                    [
                        channel_selection(channel, era),
                        VH_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "zh": [
                Unit(
                    datasets["ZH"],
                    [
                        channel_selection(channel, era),
                        VH_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "wjets": [
                Unit(
                    datasets["Wjets"],
                    [
                        channel_selection(channel, era),
                        W_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "dy": [
                Unit(
                    datasets["DY"],
                    [
                        channel_selection(channel, era),
                        DY_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
            "rem_vv": [
                Unit(
                    datasets["rem_VV"],
                    [
                        channel_selection(channel, era),
                        VV_process_selection(channel, era),
                    ],
                    [
                        control_binning[channel][v]
                        for v in set(control_binning[channel].keys())
                        & set(args.control_plot_set)
                    ],
                )
            ],
        }

    # Step 1: create units and book actions
    for channel in args.channels:
        print(channel)
        nominals[args.era]["datasets"][channel] = get_nominal_datasets(
            args.era, channel
        )
        if args.control_plots:
            nominals[args.era]["units"][channel] = get_control_units(
                channel, args.era, nominals[args.era]["datasets"][channel]
            )
    um = UnitManager()

    # available sm processes are: {"data", "emb", "ztt", "zl", "zj", "ttt", "ttl", "ttj", "vvt", "vvl", "vvj", "w", "ggh", "qqh","vh","tth"}
    # necessary processes for analysis with emb and ff method are: {"data", "emb", "zl", "ttl","ttt", "vvl","ttt" "ggh", "qqh","vh","tth"}
    if args.process_selection is None:
        procS = {
            "data",
            "ggzz",
            "rem_vh",
            "rem_ttbar",
            "www",
            "wwz",
            "wzz",
            "zzz",
            "wh",
            "zh",
            "wz",
            "zz",
            # simulated fake estimation
            "dy",
            "tt",
            "wjets",
            "rem_vv",
        }
    else:
        procS = args.process_selection

    print("Processes to be computed: ", procS)
    dataS = {"data"} & procS
    simulatedProcsDS = {
        "emt": {
            "ggzz",
            "rem_vh",
            "rem_ttbar",
            "www",
            "wwz",
            "wzz",
            "zzz",
            "wh",
            "zh",
            "wz",
            "zz",
            "dy",
            "tt",
            "wjets",
            "rem_vv",
        },
        "met": {
            "ggzz",
            "rem_vh",
            "rem_ttbar",
            "www",
            "wwz",
            "wzz",
            "zzz",
            "wh",
            "zh",
            "wz",
            "zz",
            "dy",
            "tt",
            "wjets",
            "rem_vv",
        },
        "mmt": {
            "ggzz",
            "rem_vh",
            "rem_ttbar",
            "www",
            "wwz",
            "wzz",
            "zzz",
            "wh",
            "zh",
            "wz",
            "zz",
            "dy",
            "tt",
            "wjets",
            "rem_vv",
        },
        "mtt": {
            "ggzz",
            "rem_vh",
            "rem_ttbar",
            "www",
            "wwz",
            "wzz",
            "zzz",
            "wh",
            "zh",
            "wz",
            "zz",
            "dy",
            "tt",
            "wjets",
            "rem_vv",
        },
        "ett": {
            "ggzz",
            "rem_vh",
            "rem_ttbar",
            "www",
            "wwz",
            "wzz",
            "zzz",
            "wh",
            "zh",
            "wz",
            "zz",
            "dy",
            "tt",
            "wjets",
            "rem_vv",
        },
    }
    for ch_ in args.channels:
        print("procs:", (simulatedProcsDS[ch_] & procS))
        if ch_ == "emt":
            um.book(
                [
                    unit
                    for d in dataS | (simulatedProcsDS[ch_] & procS)
                    for unit in nominals[args.era]["units"][ch_][d]
                ],
                [
                    anti_iso_llt_tau,
                    anti_isoid_ele_1,
                    anti_isoid_mu_2,
                    anti_isoid_ele_1_tau,
                    anti_isoid_mu_2_tau,
                ],
                enable_check=args.enable_booking_check,
            )
        elif ch_ == "met":
            um.book(
                [
                    unit
                    for d in dataS | (simulatedProcsDS[ch_] & procS)
                    for unit in nominals[args.era]["units"][ch_][d]
                ],
                [
                    anti_iso_llt_tau,
                    anti_isoid_ele_2,
                    anti_isoid_mu_1,
                    anti_isoid_ele_2_tau,
                    anti_isoid_mu_1_tau,
                ],
                enable_check=args.enable_booking_check,
            )
        elif ch_ == "mmt":
            um.book(
                [
                    unit
                    for d in dataS | (simulatedProcsDS[ch_] & procS)
                    for unit in nominals[args.era]["units"][ch_][d]
                ],
                [anti_iso_llt_tau, anti_isoid_mu_2, anti_isoid_mu_2_tau],
                enable_check=args.enable_booking_check,
            )
        elif ch_ in ["ett", "mtt"]:
            um.book(
                [
                    unit
                    for d in dataS | (simulatedProcsDS[ch_] & procS)
                    for unit in nominals[args.era]["units"][ch_][d]
                ],
                [anti_iso_ltt],
                enable_check=args.enable_booking_check,
            )
        if args.skip_systematic_variations:
            pass
        else:
            # Book variations common to all channels
            if "artus" in args.ntuple_type:
                pass
            else:
                um.book(
                    [
                        unit
                        for d in simulatedProcsDS[ch_]
                        for unit in nominals[args.era]["units"][ch_][d]
                    ],
                    [
                        *mu_id_weight,
                    ],
                    enable_check=args.enable_booking_check,
                )

    # Step 2: convert units to graphs and merge them
    g_manager = GraphManager(um.booked_units, True)
    g_manager.optimize(args.optimization_level)
    graphs = g_manager.graphs
    for graph in graphs:
        print("%s" % graph)
    if args.only_create_graphs:
        if args.control_plots:
            graph_file_name = "control_unit_graphs-{}-{}-{}.pkl".format(
                args.era, ",".join(args.channels), ",".join(sorted(procS))
            )
        else:
            graph_file_name = "analysis_unit_graphs-{}-{}-{}-{}.pkl".format(
                args.tag, args.era, ",".join(args.channels), args.proc_arr
            )
        if args.graph_dir is not None:
            graph_file = os.path.join(args.graph_dir, graph_file_name)
        else:
            graph_file = graph_file_name
        logger.info("Writing created graphs to file %s.", graph_file)
        with open(graph_file, "wb") as f:
            pickle.dump(graphs, f)
    else:
        # Step 3: convert to RDataFrame and run the event loop
        r_manager = RunManager(graphs)
        r_manager.run_locally(output_file, args.num_processes, args.num_threads)
    return


if __name__ == "__main__":
    # from multiprocessing import set_start_method
    # set_start_method("spawn")
    args = parse_arguments()
    if ".root" in args.output_file:
        log_file = args.output_file.replace(".root", ".log")
    else:
        log_file = "{}.log".format(args.output_file)
    setup_logging(log_file, logging.DEBUG)
    main(args)
