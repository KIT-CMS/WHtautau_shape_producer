import ROOT
from correctionlib import _core
import argparse
import yaml
import os
import glob
import time
from tqdm import tqdm
from multiprocessing import Pool, current_process, RLock
from ROOT import Math
from ROOT import TLorentzVector

# source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh
# noge weight does not consider extension files


def args_parser():
    parser = argparse.ArgumentParser(
        description="Generate xsec friend trees for SM-HTT analysis"
    )
    parser.add_argument(
        "--basepath",
        type=str,
        required=True,
        help="Basepath",
    )
    parser.add_argument(
        "--outputpath",
        type=str,
        required=True,
        help="Path to output directory",
    )
    parser.add_argument(
        "--nthreads",
        type=int,
        default=1,
        help="Number of threads to use",
    )
    parser.add_argument(
        "--dataset-config",
        type=str,
        default="datasets/datasets.yaml",
        help="path to the datasets.yaml",
    )
    parser.add_argument(
        "--xrootd",
        action="store_true",
        help="if set, the files will be read via xrootd",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="if set, debug mode will be enabled",
    )
    parser.add_argument(
        "--corr_file",
        type=str,
        required=True,
        help="Path to jetfake rates",
    )
    parser.add_argument(
        "--remove_empty_ntuples",
        action="store_true",
        help="if set, empty ntuples will be removed",
    )
    return parser.parse_args()


ROOT.gInterpreter.Declare(
    """
    #include "correction.h"
    float fake_rate(const float &pt3, const int &dm, const std::string &wp_vs_jets, const std::string &wp_vs_mu, const std::string &wp_vs_ele, const std::string &corr_file) {
        auto cset = correction::CorrectionSet::from_file(corr_file);
        auto ev = cset->at("jet_to_tau_fakerate");
        float sf = ev->evaluate({wp_vs_jets, wp_vs_mu, wp_vs_ele, dm, pt3});
        return sf;
    };
    """
)


def parse_filepath(path):
    """
    filepaths always look like this:
    /$basepath/2018/samplenick/mt/samplenick_3.root
    so the channel is the [-2] element
    """
    splitted = path.split("/")
    data = {
        "era": splitted[-4],
        "channel": splitted[-2],
        "nick": splitted[-3],
    }

    return data


def convert_to_xrootd(path):
    if path.startswith("/storage/gridka-nrg/"):
        return path.replace(
            "/storage/gridka-nrg/",
            "root://xrootd-cms.infn.it///store/user/",
        )
    elif path.startswith("/ceph"):
        return path


def job_wrapper(args):
    return friend_producer(*args)


def friend_producer(
    inputfile,
    output_path,
    dataset_proc,
    era,
    channel,
    use_xrootd,
    corr_file_ele,
    corr_file_mu,
    debug=False,
):
    # filepath = os.path.dirname(inputfile).split("/")
    output_file = os.path.join(
        output_path, era, dataset_proc["nick"], channel, os.path.basename(inputfile)
    )
    if debug:
        print(f"Processing {inputfile}")
        print(f"Outputting to {output_file}")
    # remove outputfile if it exists
    # if os.path.exists(output_path):
    #     os.remove(output_path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    if use_xrootd:
        inputfile = convert_to_xrootd(inputfile)
    # check if the output file is empty
    # print(f"Checking if {inputfile} is empty")
    try:
        rootfile = ROOT.TFile.Open(inputfile, "READ")
    except OSError:
        print(f"{inputfile} is broken")
        return
    # if the ntuple tree does not exist, the file is empty, so we can skip it
    if "ntuple" not in [x.GetTitle() for x in rootfile.GetListOfKeys()]:
        # print(f"{inputfile} is empty, generating empty friend tree")
        if debug:
            print("Available keys: ", [x.GetTitle() for x in rootfile.GetListOfKeys()])
        if args.remove_empty_ntuples:
            print(f"removing empty ntuple {inputfile}")
            os.remove(inputfile)
        # generate empty friend tree
        # friend_tree = ROOT.TFile(output_file, "CREATE")
        # tree = ROOT.TTree("ntuple", "")
        # tree.Write()
        # friend_tree.Close()
        rootfile.Close()
        print("done")
        return
    if channel in ["eem", "mme"]:
        rootfile.Close()
        return
    # else:
    # print(f"{inputfile} is not empty, generating friend tree")
    rdf = ROOT.RDataFrame("ntuple", rootfile)
    if channel == "emt":
        print(channel)
        rdf = rdf.Define(
            "ele_fakerate",
            '(float) lepfake_rate(pt_1,"{corr_file}")'.format(
                corr_file=corr_file_ele,
            ),
        )
        rdf = rdf.Define(
            "mu_fakerate",
            '(float) lep_fake_rate(pt_2,"{corr_file}")'.format(
                corr_file=corr_file_mu,
            ),
        )
    elif channel == "met":
        rdf = rdf.Define(
            "mu_fakerate",
            '(float) lep_fake_rate(pt_1,"{corr_file}")'.format(
                corr_file=corr_file_mu,
            ),
        )
        rdf = rdf.Define(
            "ele_fakerate",
            '(float) lep_fake_rate(pt_2,"{corr_file}")'.format(
                corr_file=corr_file_ele,
            ),
        )
    elif channel == "mmt":
        rdf = rdf.Define(
            "mu_fakerate",
            '(float) lep_fake_rate(pt_1,"{corr_file}")'.format(
                corr_file=corr_file_mu,
            ),
        )
        rdf = rdf.Define(
            "mu_fakerate",
            '(float) lep_fake_rate(pt_2,"{corr_file}")'.format(
                corr_file=corr_file_mu,
            ),
        )
    rdf.Snapshot(
        "ntuple",
        output_file,
        [
            "fakerate",
        ],
    )
    rootfile.Close()
    return


def generate_friend_trees(
    dataset, ntuples, nthreads, output_path, use_xrootd, corr_file, debug
):
    print("Using {} threads".format(nthreads))
    arguments = [
        (
            ntuple,
            output_path,
            dataset[parse_filepath(ntuple)["nick"]],
            parse_filepath(ntuple)["era"],
            parse_filepath(ntuple)["channel"],
            use_xrootd,
            corr_file,
            debug,
        )
        for ntuple in ntuples
    ]
    pbar = tqdm(
        total=len(arguments),
        desc="Total progess",
        position=nthreads + 1,
        dynamic_ncols=True,
        leave=True,
    )
    with Pool(nthreads, initargs=(RLock(),), initializer=tqdm.set_lock) as pool:
        for result in pool.imap_unordered(job_wrapper, arguments):
            pbar.update(1)
    pool.close()
    pbar.close()


if __name__ == "__main__":
    args = args_parser()
    base_path = os.path.join(args.basepath, "*/*/*/*.root")
    output_path = os.path.join(args.outputpath)
    dataset = yaml.safe_load(open(args.dataset_config))
    ntuples = glob.glob(base_path)
    ntuples_wo_data = ntuples.copy()
    for ntuple in ntuples:
        filename = os.path.basename(ntuple)
    nthreads = args.nthreads
    if nthreads > len(ntuples_wo_data):
        nthreads = len(ntuples_wo_data)
    generate_friend_trees(
        dataset,
        ntuples_wo_data,
        nthreads,
        output_path,
        args.xrootd,
        args.corr_file,
        args.debug,
    )
    print("Done")
