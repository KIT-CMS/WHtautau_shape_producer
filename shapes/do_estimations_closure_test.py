#!/usr/bin/env python3
import argparse
import logging
import json

import ROOT


logger = logging.getLogger("")

_dataset_map = {
    "data": "data",
    "ZTT": "DY",
    "ZL": "DY",
    "ZJ": "DY",
    "TTT": "TT",
    "TTL": "TT",
    "TTJ": "TT",
    "VVT": "VV",
    "VVL": "VV",
    "VVJ": "VV",
    "EMB": "EMB",
    "W": "W",
    "ggZZ": "ggZZ",
    "WZ": "WZ",
    "ZZ": "ZZ",
    "TT": "TT",
    "rem_ttbar": "rem_ttbar",
    "triboson": "triboson",
    "Wjets": "Wjets",
    "DY": "DY",
    "rem_VV": "rem_VV",
    "WWZ": "WWZ",
    "WZZ": "WZZ",
    "WWW": "WWW",
    "ZZZ": "ZZZ",
}
_process_map = {
    "data": "data",
    "ZTT": "DY-ZTT",
    "ZL": "DY-ZL",
    "ZJ": "DY-ZJ",
    "TTT": "TT-TTT",
    "TTL": "TT-TTL",
    "TTJ": "TT-TTJ",
    "VVT": "VV-VVT",
    "VVL": "VV-VVL",
    "VVJ": "VV-VVJ",
    "EMB": "Embedded",
    "W": "W",
    "ggZZ": "VV",
    "WWZ": "WWZ",
    "WZZ": "WZZ",
    "WWW": "WWW",
    "ZZZ": "ZZZ",
    "WZ": "VV",
    "ZZ": "VV",
    "TT": "TT",
    "rem_ttbar": "TT",
    "Wjets": "W",
    "DY": "DY",
    "rem_VV": "VV",
}

_name_string = "{dataset}#{channel}{process}{selection}#{variation}#{variable}"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input root file.")
    parser.add_argument("-e", "--era", required=True, help="Experiment era.")
    parser.add_argument(
        "--emb-tt",
        action="store_true",
        help="Add embedded ttbar contamination variation to file.",
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


def replace_negative_entries_and_renormalize(histogram, tolerance):
    # This function is taken from https://github.com/KIT-CMS/shape-producer/blob/beddc4a43e2e326018d804e58d612d8688ec33b6/shape_producer/histogram.py#L189

    # Find negative entries and calculate norm.
    norm_all = 0.0
    norm_positive = 0.0
    for i_bin in range(1, histogram.GetNbinsX() + 1):
        this_bin = histogram.GetBinContent(i_bin)
        if this_bin < 0.0:
            histogram.SetBinContent(i_bin, 0.0)
        else:
            norm_positive += this_bin
        norm_all += this_bin

    if norm_all == 0.0 and norm_positive != 0.0:
        logger.fatal(
            "Aborted renormalization because initial normalization is zero, but positive normalization not. . Check histogram %s",
            histogram.GetName(),
        )
        raise Exception

    if norm_all < 0.0:
        logger.fatal(
            "Aborted renormalization because initial normalization is negative: %f. Check histogram %s ",
            norm_all,
            histogram.GetName(),
        )
        for i_bin in range(1, histogram.GetNbinsX() + 1):
            histogram.SetBinContent(i_bin, 0.0)
        norm_all = 0.0
        norm_positive = 0.0
        # raise Exception

    if abs(norm_all - norm_positive) > tolerance * norm_all:
        logger.warning(
            "Renormalization failed because the normalization changed by %f, which is above the tolerance %f. Check histogram %s",
            abs(norm_all - norm_positive),
            tolerance * norm_all,
            histogram.GetName(),
        )

    # Renormalize histogram if negative entries are found
    if norm_all != norm_positive:
        if norm_positive == 0.0:
            logger.fatal(
                "Renormalization failed because all bins have negative entries."
            )
            raise Exception
        for i_bin in range(1, histogram.GetNbinsX() + 1):
            this_bin = histogram.GetBinContent(i_bin)
            histogram.SetBinContent(i_bin, this_bin * norm_all / norm_positive)

    return histogram


def jet_fakes_estimation(rootfile, channel, selection, variable, variation="Nominal"):

    procs_to_add = ["Wjets", "DY", "rem_VV"]
    logger.debug(
        "Trying to get object {}".format(
            _name_string.format(
                dataset="TT",
                channel=channel,
                process="-" + _process_map["TT"],
                selection="-" + selection if selection != "" else "",
                variation=variation,
                variable=variable,
            )
        )
    )

    base_hist = rootfile.Get(
        _name_string.format(
            dataset="TT",
            channel=channel,
            process="-" + _process_map["TT"],
            selection="-" + selection if selection != "" else "",
            variation=variation,
            variable=variable,
        )
    ).Clone()
    for proc in procs_to_add:
        logger.debug(
            "Trying to get object {}".format(
                _name_string.format(
                    dataset=_dataset_map[proc],
                    channel=channel,
                    process="-" + _process_map[proc],
                    selection="-" + selection if selection != "" else "",
                    variation=variation,
                    variable=variable,
                )
            )
        )
        print(
            _name_string.format(
                dataset=_dataset_map[proc],
                channel=channel,
                process="-" + _process_map[proc],
                selection="-" + selection if selection != "" else "",
                variation=variation,
                variable=variable,
            )
        )
        base_hist.Add(
            rootfile.Get(
                _name_string.format(
                    dataset=_dataset_map[proc],
                    channel=channel,
                    process="-" + _process_map[proc],
                    selection="-" + selection if selection != "" else "",
                    variation=variation,
                    variable=variable,
                )
            ),
            1.0,
        )

    proc_name = "jetFakes"
    variation_name = (
        base_hist.GetName().replace("TT", proc_name).replace("-TT", proc_name)
    )
    base_hist.SetName(variation_name)
    base_hist.SetTitle(variation_name)
    return base_hist


def jet_fakes_nominal(rootfile, channel, category, variable):
    # function that adds all contributions from jetfakes together to a nominal histogram
    if channel == "emt":
        fake_contributions = [
            "mu2tau_anti_isoid",
            "ele1tau_anti_isoid",
            "mu2_anti_isoid",
            "ele1_anti_isoid",
        ]
    elif channel == "met":
        fake_contributions = [
            "mu1tau_anti_isoid",
            "ele2tau_anti_isoid",
            "mu1_anti_isoid",
            "ele2_anti_isoid",
        ]
    elif channel == "mmt":
        fake_contributions = [
            "mu2tau_anti_isoid",
            "mu2_anti_isoid",
        ]
    logger.debug(
        "Nominal jetfakes histogram -- Trying to get object {}".format(
            _name_string.format(
                dataset="jetFakes",
                channel=channel,
                process="-jetFakes",
                selection=category,
                variation="tau_anti_iso",
                variable=variable,
            )
        )
    )
    base_hist = rootfile.Get(
        _name_string.format(
            dataset="jetFakes",
            channel=channel,
            process="-jetFakes",
            selection=category,
            variation="tau_anti_iso",
            variable=variable,
        )
    ).Clone()
    if channel not in ["ett", "mtt"]:
        for var_ in fake_contributions:
            logger.debug(
                "Nominal jetfakes histogram -- Trying to fetch root histogram {}".format(
                    _name_string.format(
                        dataset="jetFakes",
                        channel=channel,
                        process="-jetFakes",
                        selection=category,
                        variation=var_,
                        variable=variable,
                    )
                )
            )
            base_hist.Add(
                rootfile.Get(
                    _name_string.format(
                        dataset="jetFakes",
                        channel=channel,
                        process="-jetFakes",
                        selection=category,
                        variation=var_,
                        variable=variable,
                    )
                ),
                1,
            )
    ff_variation = "Nominal"
    variation_name = base_hist.GetName().replace("tau_anti_iso", ff_variation)
    base_hist.SetName(variation_name)
    base_hist.SetTitle(variation_name)
    return base_hist


def main(args):
    input_file = ROOT.TFile(args.input, "update")
    # input_file.SetOverwrite(True)
    # Loop over histograms in root file to find available FF inputs.
    ff_inputs = {}
    logger.info("Reading inputs from file {}".format(args.input))
    for key in input_file.GetListOfKeys():
        logger.debug("Processing histogram %s", key.GetName())
        dataset, selection, variation, variable = key.GetName().split("#")
        if "anti_iso" in variation:
            sel_split = selection.split("-", maxsplit=1)
            # Set category to default since not present in control plots.
            category = ""
            # Treat data hists seperately because only channel selection is applied to data.
            if "data" in dataset:
                channel = sel_split[0]
                # Set category label for analysis categories.
                if len(sel_split) > 1:
                    category = sel_split[1]
                process = "data"
            else:
                channel = sel_split[0]
                #  Check if analysis category present in root file.
                if (
                    len(sel_split[1].split("-")) > 2
                    or ("Embedded" in sel_split[1] and len(sel_split[1].split("-")) > 1)
                    or ("W" in sel_split[1] and len(sel_split[1].split("-")) > 1)
                ):
                    process = "-".join(sel_split[1].split("-")[:-1])
                    category = sel_split[1].split("-")[-1]
                else:
                    # Set only process if no categorization applied.
                    process = sel_split[1]
            if channel in ff_inputs:
                if category in ff_inputs[channel]:
                    if variable in ff_inputs[channel][category]:
                        if variation in ff_inputs[channel][category][variable]:
                            ff_inputs[channel][category][variable][variation].append(
                                process
                            )
                        else:
                            ff_inputs[channel][category][variable][variation] = [
                                process
                            ]
                    else:
                        ff_inputs[channel][category][variable] = {variation: [process]}
                else:
                    ff_inputs[channel][category] = {variable: {variation: [process]}}
            else:
                ff_inputs[channel] = {category: {variable: {variation: [process]}}}

    # Loop over available ff inputs and do the estimations
    logger.info("Starting estimations for fake factors and their variations")
    logger.debug("%s", json.dumps(ff_inputs, sort_keys=True, indent=4))
    for ch in ff_inputs:
        for cat in ff_inputs[ch]:
            logger.info("Do estimation for category %s", cat)
            for var in ff_inputs[ch][cat]:
                for variation in ff_inputs[ch][cat][var]:
                    estimated_hist = jet_fakes_estimation(
                        input_file, ch, cat, var, variation=variation
                    )
                    estimated_hist.Write()

    for ch in ff_inputs:
        for cat in ff_inputs[ch]:
            for var in ff_inputs[ch][cat]:
                estimated_hist = jet_fakes_nominal(input_file, ch, cat, var)
                estimated_hist.Write()
                estimated_hist.Write()
    logger.info("Successfully finished estimations.")

    # Clean-up.
    input_file.Close()
    return


if __name__ == "__main__":
    args = parse_args()
    setup_logging("do_estimations.log", level=logging.DEBUG)
    main(args)
