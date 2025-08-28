import os
import argparse
import logging
import multiprocessing
import ROOT

logger = logging.getLogger("")

_process_map = {
    "WHplus": "VH",
    "WHminus": "VH",
    "WWW": "WWW",
    "rem_VV": "VV",
    "ggZZ": "VV",
    "WWZ": "WWZ",
    "ZZZ": "ZZZ",
    "rem_ttbar": "TT",
    "WZ": "VV",
    "WZZ": "WZZ",
    "Wjets": "W",
    "ZH": "VH",
    "jetFakes": "jetFakes",
    "DY": "DY",
    "rem_VH": "VH",
    "ZZ": "ZZ",
    "TT": "TT",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_emt", help="Input root file.")
    parser.add_argument("--input_met", help="Input root file.")
    parser.add_argument("-o", "--output", help="Output directory.")
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


def main(args):
    input_file_emt = ROOT.TFile(args.input_emt, "READ")
    input_file_met = ROOT.TFile(args.input_met, "READ")
    output_file = ROOT.TFile(args.output, "RECREATE")
    output_file.cd()
    # Loop over histograms to extract relevant information for synced files.
    logging.info(
        "Reading input histograms from files emt %s met %s",
        args.input_emt,
        args.input_met,
    )
    for key in input_file_emt.GetListOfKeys():
        if "anti_iso" not in key.GetName():
            emt_hist = input_file_emt.Get(key.GetName())
            met_hist = input_file_met.Get(key.GetName().replace("#emt", "#met"))
            print(key.GetName())
            comb_hist = emt_hist.Clone()
            comb_hist.Add(met_hist, 1.0)
            comb_hist.SetTitle(key.GetName())
            comb_hist.SetName(key.GetName())
            comb_hist.Write()

    logging.info("Successfully written all histograms to file.")


if __name__ == "__main__":
    args = parse_args()
    setup_logging("convert_to_synced_shapes.log", level=logging.INFO)
    main(args)
