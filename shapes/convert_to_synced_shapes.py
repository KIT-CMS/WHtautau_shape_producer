#!/usr/bin/env python3
# Script adapted from script in https://github.com/KIT-CMS/sm-htt-analysis/shapes/convert_to_synced_shapes.py
import os
import argparse
import logging
import multiprocessing

import ROOT

logger = logging.getLogger("")

_process_map = {
    "WH_htt_plus": "H",
    "WH_htt_minus": "H",
    "WH_hww_plus": "H",
    "WH_hww_minus": "H",
    "VVV": "VVV",
    "rem_VV": "VV",
    "ggZZ": "VV",
    "rem_ttbar": "TT",
    "WZ": "VV",
    "Wjets": "W",
    "jetFakes": "jetFakes",
    "DY": "DY",
    "rem_H": "H",
    "ggH": "H",
    "qqH": "H",
    "ggZH": "H",
    "ZH": "H",
    "ttH": "H",
    "ZZ": "ZZ",
    "TT": "TT",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--era", help="Experiment era.")
    parser.add_argument("-i", "--input", help="Input root file.")
    parser.add_argument("-o", "--output", help="Output directory.")
    parser.add_argument(
        "--gof",
        action="store_true",
        help="Convert shapes for GoF or control plots. "
        "Use variable as category indicator.",
    )
    parser.add_argument(
        "--mc", action="store_true", help="Use jet fake estimation based on mc shapes."
    )
    parser.add_argument(
        "--special", help="Use for special cases with no-trivial shapes.", default=""
    )
    parser.add_argument(
        "--variable-selection",
        default=None,
        type=str,
        nargs=1,
        help="Select final discriminator for shape creation.",
    )
    parser.add_argument(
        "-n", "--num-processes", default=1, type=int, help="Number of processes used."
    )
    parser.add_argument(
        "--region",
        default=None,
        type=str,
        help="signal region corresponding to the charge of the lepton from the W. Options: plus, minus",
    )
    return parser.parse_args()


def setup_logging(output_file, level=logging.INFO):
    logger.setLevel(level)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(output_file, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return


def correct_nominal_shape(hist, name, integral):
    if integral >= 0:
        # if integral is larger than 0, everything is fine
        sf = 1.0
    elif integral == 0.0:
        logger.info("Nominal histogram is empty: {}".format(name))
        # if integral of nominal is 0, we make sure to scale the histogram with 0.0
        sf = 0
    else:
        logger.info(
            "Nominal histogram is negative : {} {} --> fixing it now...".format(
                integral, name
            )
        )
        # if the histogram is negative, the make all negative bins positive,
        # and scale the histogram to a small positive value
        for i in range(hist.GetNbinsX()):
            if hist.GetBinContent(i + 1) < 0.0:
                logger.info("Negative Bin {} - {}".format(i, hist.GetBinContent(i + 1)))
                hist.SetBinContent(i + 1, 0.001)
                logger.info(
                    "After fixing: {} - {}".format(i, hist.GetBinContent(i + 1))
                )
        sf = 0.001 / hist.Integral()
    hist.Scale(sf)
    return hist


def write_hists_per_category(cat_hists: tuple):
    category, keys, channel, ofname, ifname, region = cat_hists
    infile = ROOT.TFile(ifname, "READ")
    print("hi", category, region)
    dir_name = "{CHANNEL}_{CATEGORY}_{REGION}".format(
        CHANNEL=channel, CATEGORY=category, REGION=region
    )
    if "{category}" in ofname:
        outfile = ROOT.TFile(ofname.format(category=dir_name), "RECREATE")
    else:
        outfile = ROOT.TFile(
            ofname.replace(".root", "-" + category + "-" + region + ".root"), "RECREATE"
        )
    outfile.cd()
    outfile.mkdir(dir_name)
    outfile.cd(dir_name)
    for name, name_output in sorted(keys.items(), key=lambda x: x[1]):
        hist = infile.Get(name)
        # Write shapes with partial correlations across eras.
        if "Era" in name_output:
            if (
                "_1ProngPi0Eff_" in name_output
                or "_qcd_iso" in name_output
                or "_3ProngEff_" in name_output
                or "_dyShape_" in name_output
            ):
                hist.SetTitle(name_output.replace("_Era", ""))
                hist.SetName(name_output.replace("_Era", ""))
                hist.Write()
        if "Era" in name_output:
            name_output = name_output.replace("Era", f"{args.era}")
        if "Channel" in name_output:
            name_output = name_output.replace("Channel", channel)
        if f"{channel}__{args.era}" in name_output:
            name_output = name_output.replace(
                f"{channel}__{args.era}", f"{channel}_{args.era}_"
            )
        if f"Up_{channel}_{args.era}" in name_output:
            name_output = name_output.replace(
                f"Up_{channel}_{args.era}", f"{channel}_{args.era}Up"
            )
        if f"Down_{channel}_{args.era}" in name_output:
            name_output = name_output.replace(
                f"Down_{channel}_{args.era}", f"{channel}_{args.era}Down"
            )
        hist.SetTitle(name_output)
        hist.SetName(name_output)
        hist.Write()
    outfile.Close()
    infile.Close()
    return


def main(args):
    input_file = ROOT.TFile(args.input)

    # Loop over histograms to extract relevant information for synced files.
    logging.info("Reading input histograms from file %s", args.input)
    hist_map = {}
    for key in input_file.GetListOfKeys():
        if "predicted_max_value" in key.GetName():
            split_name = key.GetName().split("#")
            channel = split_name[1].split("-")[0]
            if args.gof:
                # Use variable as category label for GOF test and control plots.
                category = split_name[3]
                process = split_name[0] if not "data" in split_name[0] else "data_obs"
            else:
                category = split_name[1].split("-")[-1]
                process = split_name[0] if not "data" in split_name[0] else "data_obs"
                # Skip discriminant variables we do not want in the sync file.
                # This is necessary because the sync file only allows for one type of histogram.
                # A combination of the runs for different variables can then be used in separate files.
                if args.variable_selection is None:
                    pass
                else:
                    if split_name[3] not in args.variable_selection:
                        continue
            variation = split_name[2]
            # Skip variations necessary for estimations which are of no further use.
            if "same_sign" in variation or "anti_iso" in variation:
                continue

            # Check if channel and category are already in the map
            if not channel in hist_map:
                hist_map[channel] = {}
            if not category in hist_map[channel]:
                hist_map[channel][category] = {}

            # Skip copying of jetFakes estimations based on underlying shapes to be able
            # to use one name in the synced file.
            # TODO: Should this be kept or do we want to put both version in the synced file and
            #       perform the switch on combine level.
            if args.mc:
                _process_map["jetFakes"] = "jetFakesMC"
                _process_map["QCD"] = "QCDMC"
                if process in ["jetFakes", "QCD"]:
                    continue
            else:
                if "MC" in process:
                    continue
            _rev_process_map = {val: key for key, val in _process_map.items()}
            if process in _rev_process_map.keys():
                # Check if MSSM sample.
                if "SUSY" in process:
                    # Read mass from dataset name in case of SUSY samples.
                    mass = split_name[0].split("_")[-1]
                    process = "_".join([_rev_process_map[process], mass])
                else:
                    if args.special != "TauES":
                        process = _rev_process_map[process]
                    else:
                        if not "emb" in process and not "jetFakes" in process:
                            process = _rev_process_map[process]
            name_output = "{process}".format(process=process)
            if "Nominal" not in variation:
                name_output += "_" + variation
            logging.debug(
                "Adding histogram with name %s as %s to category %s.",
                key.GetName(),
                name_output,
                channel + "_" + category,
            )
            hist_map[channel][category][key.GetName()] = name_output
    # Clean up
    input_file.Close()
    # Loop over map and create the output file.
    for channel in hist_map:
        ofname = os.path.join(
            args.output,
            "{ERA}-{CHANNELS}-synced.root".format(CHANNELS=channel, ERA=args.era),
        )
        logging.info(
            "Writing histograms to file %s with %s processes",
            ofname,
            args.num_processes,
        )

        if not os.path.exists(args.output):
            os.mkdir(args.output)
        print(args.region)
        with multiprocessing.Pool(args.num_processes) as pool:
            pool.map(
                write_hists_per_category,
                [
                    (*item, channel, ofname, args.input, args.region)
                    for item in sorted(hist_map[channel].items())
                ],
            )

    logging.info("Successfully written all histograms to file.")


if __name__ == "__main__":
    args = parse_args()
    setup_logging("convert_to_synced_shapes.log", level=logging.INFO)
    main(args)
