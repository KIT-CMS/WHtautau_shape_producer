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
    "rem_H": "rem_H",
    "ggH": "ggH",
    "qqH": "qqH",
    "ggZH": "ggZH",
    "ZH": "ZH",
    "ttH": "ttH",
    "triboson": "triboson",
    "Wjets": "Wjets",
    "DY": "DY",
    "rem_VV": "rem_VV",
    "VVV": "VVV",
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
    "VVV": "VVV",
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
    "rem_H": "H",
    "ggH": "H",
    "qqH": "H",
    "ggZH": "H",
    "ZH": "H",
    "ttH": "H",
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
    procs_to_subtract = [
        "VVV",
        # "ggZZ",
        "ZZ",
        "rem_ttbar",
        "WZ",
        # "ggH",
        "ZH",
        # "qqH",
        "ttH",
        "ggZH",
    ]
    logger.debug(
        "Trying to get object {}".format(
            _name_string.format(
                dataset="data",
                channel=channel,
                process="",
                selection="-" + selection if selection != "" else "",
                variation=variation,
                variable=variable,
            )
        )
    )
    print(variable)
    print(
        _name_string.format(
            dataset="data",
            channel=channel,
            process="",
            selection="-" + selection if selection != "" else "",
            variation=variation,
            variable=variable,
        )
    )
    base_hist = rootfile.Get(
        _name_string.format(
            dataset="data",
            channel=channel,
            process="",
            selection="-" + selection if selection != "" else "",
            variation=variation,
            variable=variable,
        )
    ).Clone()
    for proc in procs_to_subtract:
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
        print(variation)
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
            -1.0,
        )
    proc_name = "jetFakes"
    variation_name = (
        base_hist.GetName()
        .replace("data", proc_name)
        .replace("#" + channel, "#" + "-".join([channel, proc_name]), 1)
    )
    base_hist.SetName(variation_name)
    base_hist.SetTitle(variation_name)
    return base_hist


def jet_fakes_nominal(rootfile, channel, selection, variable, variation):
    # function that adds all contributions from jetfakes together to a nominal histogram
    if "Up" in variation or "Down" in variation:
        print(variation)
        print(variation.split("_")[-2], variation.split("_")[-1])
        unc = "_CMS_ff_{syst}_{shift}".format(
            syst=variation.split("_")[-2], shift=variation.split("_")[-1]
        )
        ff_variation = "CMS_ff_{syst}_{shift}".format(
            syst=variation.split("_")[-2], shift=variation.split("_")[-1]
        )
    else:
        unc = ""
        ff_variation = "Nominal"
    if channel == "emt":
        fake_contributions = [
            "mu2tau_anti_isoid",
            # "ele1tau_anti_isoid",
            "mu2_anti_isoid",
            # "ele1_anti_isoid",
        ]
    elif channel == "met":
        fake_contributions = [
            # "mu1tau_anti_isoid",
            "ele2tau_anti_isoid",
            # "mu1_anti_isoid",
            "ele2_anti_isoid",
        ]
    elif channel == "mmt":
        fake_contributions = [
            "mu2tau_anti_isoid",
            "mu2_anti_isoid",
        ]
    # print(
    #     "Nominal jetfakes histogram -- Trying to get object {}".format(
    #         _name_string.format(
    #             dataset="jetFakes",
    #             channel=channel,
    #             process="-jetFakes",
    #             selection="-" + selection if selection != "" else "",
    #             variation="tau_anti_iso{unc}".format(unc=unc),
    #             variable=variable,
    #         )
    #     )
    # )
    logger.debug(
        "Nominal jetfakes histogram -- Trying to get object {}".format(
            _name_string.format(
                dataset="jetFakes",
                channel=channel,
                process="-jetFakes",
                selection="-" + selection if selection != "" else "",
                variation="tau_anti_iso{unc}".format(unc=unc),
                variable=variable,
            )
        )
    )
    if channel in ["eem", "mme"]:
        base_hist = rootfile.Get(
            _name_string.format(
                dataset="jetFakes",
                channel=channel,
                process="-jetFakes",
                selection="-" + selection if selection != "" else "",
                variation="anti_id_iso_3{unc}".format(unc=unc),
                variable=variable,
            )
        ).Clone()
    else:
        base_hist = rootfile.Get(
            _name_string.format(
                dataset="jetFakes",
                channel=channel,
                process="-jetFakes",
                selection="-" + selection if selection != "" else "",
                variation="tau_anti_iso{unc}".format(unc=unc),
                variable=variable,
            )
        ).Clone()
    if channel not in ["ett", "mtt", "eem", "mme"]:
        for var_ in fake_contributions:
            logger.debug(
                "Nominal jetfakes histogram -- Trying to fetch root histogram {}".format(
                    _name_string.format(
                        dataset="jetFakes",
                        channel=channel,
                        process="-jetFakes",
                        selection="-" + selection if selection != "" else "",
                        variation="{var_}{unc}".format(var_=var_, unc=unc),
                        variable=variable,
                    )
                )
            )
            print(
                _name_string.format(
                    dataset="jetFakes",
                    channel=channel,
                    process="-jetFakes",
                    selection="-" + selection if selection != "" else "",
                    variation="{var_}{unc}".format(var_=var_, unc=unc),
                    variable=variable,
                )
            )
            base_hist.Add(
                rootfile.Get(
                    _name_string.format(
                        dataset="jetFakes",
                        channel=channel,
                        process="-jetFakes",
                        selection="-" + selection if selection != "" else "",
                        variation="{var_}{unc}".format(var_=var_, unc=unc),
                        variable=variable,
                    )
                ),
                1,
            )
    if channel in ["eem", "mme"]:
        variation_name = base_hist.GetName().replace(
            "anti_id_iso_3{unc}".format(unc=unc), ff_variation
        )
        print(variation_name)
    else:
        variation_name = base_hist.GetName().replace(
            "tau_anti_iso{unc}".format(unc=unc), ff_variation
        )

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
        if "njets" in key:
            print(
                "-------------------------------------------------------------------------------------------"
            )
            print(key)
        if "anti_iso" in variation or "anti_id_iso" in variation:
            sel_split = selection.split("-")
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
                if len(sel_split) > 2:
                    process = sel_split[1]
                    category = sel_split[2]
                else:
                    # Set only process if no categorization applied.
                    process = sel_split[1]
            if channel in ff_inputs:
                if category in ff_inputs[channel]:
                    # print(key.GetName())
                    # print(category)
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
    print(ff_inputs)
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
                for variation in ff_inputs[ch][cat][var]:
                    if (
                        variation == "tau_anti_iso"
                        or "tau_anti_iso_CMS" in variation
                        or "anti_id_iso" in variation
                    ):
                        estimated_hist = jet_fakes_nominal(
                            input_file, ch, cat, var, variation
                        )
                        estimated_hist.Write()
                        estimated_hist.Write()
    logger.info("Successfully finished estimations.")

    # Clean-up.
    input_file.Close()
    return


if __name__ == "__main__":
    args = parse_args()
    setup_logging("do_estimations.log", level=logging.INFO)
    main(args)
