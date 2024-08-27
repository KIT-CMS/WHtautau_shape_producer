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
    parser.add_argument("--input_mmt", help="Input root file.")
    parser.add_argument("--input_mtt", help="Input root file.")
    parser.add_argument("--input_ett", help="Input root file.")
    parser.add_argument("--channel", help="combined channel", required=True)
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


def sum_histograms_llt(file1, file2, file3, output_file):
    # Open the ROOT files
    emt_file = ROOT.TFile(file1, "READ")
    met_file = ROOT.TFile(file2, "READ")
    mmt_file = ROOT.TFile(file3, "READ")

    # Create a dictionary to store the histograms
    histograms = {}

    # Function to add histograms to the dictionary
    def add_histograms(file, channel):
        old_histgrams = []
        keys = file.GetListOfKeys()
        for key in keys:
            old_histgrams.append(key.GetName())
        keys_set = set(old_histgrams)
        for key in keys_set:
            if "anti_iso" not in key:
                name = key.replace("#{ch}-".format(ch=channel), "#llt-")
                hist = file.Get(key)
                if name in histograms:
                    histograms[name].Add(hist)
                else:
                    # print(key, hist, channel)
                    histograms[name] = hist.Clone()
                    histograms[name].SetTitle(name)
                    histograms[name].SetName(name)

    # Add histograms from all files
    add_histograms(emt_file, "emt")
    add_histograms(met_file, "met")
    add_histograms(mmt_file, "mmt")

    # Handle missing keys by adding a default histogram
    for name in histograms:
        hist_emt = emt_file.Get(name.replace("#llt", "#emt"))
        hist_met = met_file.Get(name.replace("#llt", "#met"))
        hist_mmt = mmt_file.Get(name.replace("#llt", "#mmt"))
        if not (hist_emt and not hist_emt.IsZombie()):
            miss_hist = emt_file.Get(
                name.replace("#llt", "#emt").replace(name.split("#")[-2], "Nominal")
            )
            histograms[name].Add(miss_hist)
        elif not (hist_met and not hist_met.IsZombie()):
            miss_hist = met_file.Get(
                name.replace("#llt", "#met").replace(name.split("#")[-2], "Nominal")
            )
            histograms[name].Add(miss_hist)
        elif not (hist_mmt and not hist_mmt.IsZombie()):
            miss_hist = mmt_file.Get(
                name.replace("#llt", "#mmt").replace(name.split("#")[-2], "Nominal")
            )
            histograms[name].Add(miss_hist)

    # Write the summed histograms to the output file
    output = ROOT.TFile(output_file, "RECREATE")
    for name, hist in histograms.items():
        hist.Write()

    # Close all files
    emt_file.Close()
    met_file.Close()
    mmt_file.Close()
    output.Close()


def sum_histograms_ltt(file1, file2, output_file):
    # Open the ROOT files
    ett_file = ROOT.TFile(file1, "READ")
    mtt_file = ROOT.TFile(file2, "READ")

    # Create a dictionary to store the histograms
    histograms = {}

    # Function to add histograms to the dictionary
    def add_histograms(file, channel):
        old_histgrams = []
        keys = file.GetListOfKeys()
        for key in keys:
            old_histgrams.append(key.GetName())
        keys_set = set(old_histgrams)
        for key in keys_set:
            if "anti_iso" not in key:
                name = key.replace("#{ch}".format(ch=channel), "#ltt")
                hist = file.Get(key)
                if name in histograms:
                    histograms[name].Add(hist)
                else:
                    histograms[name] = hist.Clone()
                    histograms[name].SetTitle(name)
                    histograms[name].SetName(name)

    # Add histograms from all files
    add_histograms(ett_file, "ett")
    add_histograms(mtt_file, "mtt")

    # Handle missing keys by adding a default histogram
    for name in histograms:
        hist_ett = ett_file.Get(name.replace("#ltt", "#ett"))
        hist_mtt = mtt_file.Get(name.replace("#ltt", "#mtt"))
        if not (hist_ett and not hist_ett.IsZombie()):
            miss_hist = ett_file.Get(
                name.replace("#ltt", "#ett").replace(name.split("#")[-2], "Nominal")
            )
            histograms[name].Add(miss_hist)
        elif not (hist_mtt and not hist_mtt.IsZombie()):
            miss_hist = mtt_file.Get(
                name.replace("#ltt", "#mtt").replace(name.split("#")[-2], "Nominal")
            )
            histograms[name].Add(miss_hist)

    # Write the summed histograms to the output file
    output = ROOT.TFile(output_file, "RECREATE")
    for name, hist in histograms.items():
        hist.Write()

    # Close all files
    ett_file.Close()
    mtt_file.Close()
    output.Close()


def main(args):
    output_file = args.output
    sum_channel = args.channel
    if sum_channel == "llt":
        sum_histograms_llt(args.input_emt, args.input_met, args.input_mmt, output_file)
    elif sum_channel == "ltt":
        sum_histograms_ltt(args.input_ett, args.input_mtt, output_file)
    else:
        raise ValueError("wrong channel")


if __name__ == "__main__":
    args = parse_args()
    main(args)
