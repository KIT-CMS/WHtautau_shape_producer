import ROOT
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
        "--remove_empty_ntuples",
        action="store_true",
        help="if set, empty ntuples will be removed",
    )
    return parser.parse_args()


ROOT.gInterpreter.Declare(
    """
    float deltaphi(const float &pt1,const float &eta1, const float &phi1, const float &mass1, const float &pt2, const float &eta2, const float &phi2, const float &mass2) {
        ROOT::Math::PtEtaPhiMVector p1 = ROOT::Math::PtEtaPhiMVector(pt1, eta1, phi1, mass1);
        ROOT::Math::PtEtaPhiMVector p2 = ROOT::Math::PtEtaPhiMVector(pt2, eta2, phi2, mass2);
        const float dphi = ROOT::Math::VectorUtil::DeltaPhi(p1, p2);
        return dphi;
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
    inputfile, output_path, dataset_proc, era, channel, use_xrootd, debug=False
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
    # for data and embedded, we don't need to do anything
    if (
        dataset_proc["sample_type"] == "data"
        or dataset_proc["sample_type"] == "embedding"
    ):
        return
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
        print(f"{inputfile} is empty, generating empty friend tree")
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
    # else:
    # print(f"{inputfile} is not empty, generating friend tree")
    rdf = ROOT.RDataFrame("ntuple", rootfile)
    numberGeneratedEventsWeight = 1 / float(dataset_proc["nevents"])
    crossSectionPerEventWeight = float(dataset_proc["xsec"])
    generator_weight = float(dataset_proc["generator_weight"])
    rdf = rdf.Define(
        "numberGeneratedEventsWeight",
        "(float){ngw}".format(ngw=numberGeneratedEventsWeight),
    )
    rdf = rdf.Define(
        "crossSectionPerEventWeight",
        "(float){xsec}".format(xsec=crossSectionPerEventWeight),
    )
    rdf = rdf.Define(
        "generator_weight",
        "(float){gen_weight}".format(gen_weight=generator_weight),
    )
    # rdf = rdf.Define(
    #     "deltaPhi_12",
    #     "(float) deltaphi(pt_1,eta_1,phi_1,mass_1,pt_2,eta_2,phi_2,mass_2)",
    # )
    # rdf = rdf.Define(
    #     "deltaPhi_13",
    #     "(float) deltaphi(pt_1,eta_1,phi_1,mass_1,pt_3,eta_3,phi_3,mass_3)",
    # )
    # rdf.Snapshot(
    #     "ntuple",
    #     output_file,
    #     [
    #         "deltaPhi_12",
    #         "deltaPhi_13",
    #     ],
    # )
    rdf.Snapshot(
        "ntuple",
        output_file,
        [
            "numberGeneratedEventsWeight",
            "crossSectionPerEventWeight",
            "generator_weight"
        ],
    )
    rootfile.Close()
    return


def generate_friend_trees(dataset, ntuples, nthreads, output_path, use_xrootd, debug):
    print("Using {} threads".format(nthreads))
    arguments = [
        (
            ntuple,
            output_path,
            dataset[parse_filepath(ntuple)["nick"]],
            parse_filepath(ntuple)["era"],
            parse_filepath(ntuple)["channel"],
            use_xrootd,
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
        dataset, ntuples_wo_data, nthreads, output_path, args.xrootd, args.debug
    )
    print("Done")
