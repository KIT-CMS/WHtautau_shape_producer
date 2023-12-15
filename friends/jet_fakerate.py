import ROOT
from correctionlib import _core
import argparse
import yaml
import os
import glob
import shutil
from tqdm import tqdm
from multiprocessing import Pool, current_process, RLock
import XRootD.client.glob_funcs as xrdglob
import XRootD.client as client
from XRootD.client.flags import DirListFlags

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
        "--eras",
        default=[],
        type=lambda eralist: [era for era in eralist.split(",")],
        help="eras to be considered, seperated by a comma without space",
    )
    parser.add_argument(
        "--corr_file_tau_16preVFP",
        default=None,
        type=str,
        help="Path to jet to tau fakerates",
    )
    parser.add_argument(
        "--corr_file_mu_16preVFP",
        default=None,
        type=str,
        help="Path to jet to mu fakerates",
    )
    parser.add_argument(
        "--corr_file_ele_16preVFP",
        default=None,
        type=str,
        help="Path to jet to ele fakerates",
    )
    parser.add_argument(
        "--corr_file_tau_16postVFP",
        default=None,
        type=str,
        help="Path to jet to tau fakerates",
    )
    parser.add_argument(
        "--corr_file_mu_16postVFP",
        default=None,
        type=str,
        help="Path to jet to mu fakerates",
    )
    parser.add_argument(
        "--corr_file_ele_16postVFP",
        default=None,
        type=str,
        help="Path to jet to ele fakerates",
    )
    parser.add_argument(
        "--corr_file_tau_17",
        default=None,
        type=str,
        help="Path to jet to tau fakerates",
    )
    parser.add_argument(
        "--corr_file_mu_17",
        default=None,
        type=str,
        help="Path to jet to mu fakerates",
    )
    parser.add_argument(
        "--corr_file_ele_17",
        default=None,
        type=str,
        help="Path to jet to ele fakerates",
    )
    parser.add_argument(
        "--corr_file_tau_18",
        default=None,
        type=str,
        help="Path to jet to tau fakerates",
    )
    parser.add_argument(
        "--corr_file_mu_18",
        default=None,
        type=str,
        help="Path to jet to mu fakerates",
    )
    parser.add_argument(
        "--corr_file_ele_18",
        default=None,
        type=str,
        help="Path to jet to ele fakerates",
    )
    parser.add_argument(
        "--tempdir",
        type=str,
        default="tmp_dir",
        help="Temporary directory to store intermediate files",
    )
    parser.add_argument(
        "--wp_vs_jets",
        type=str,
        default="VTight",
        help="working point vs. jets",
    )
    return parser.parse_args()


ROOT.gInterpreter.Declare(
    """
    #include "correction.h"
    float deltaphi(const float &pt1,const float &eta1, const float &phi1, const float &mass1, const float &pt2, const float &eta2, const float &phi2, const float &mass2) {
        ROOT::Math::PtEtaPhiMVector p1 = ROOT::Math::PtEtaPhiMVector(pt1, eta1, phi1, mass1);
        ROOT::Math::PtEtaPhiMVector p2 = ROOT::Math::PtEtaPhiMVector(pt2, eta2, phi2, mass2);
        const float dphi = ROOT::Math::VectorUtil::DeltaPhi(p1, p2);
        return dphi;
    };

    float tau_fakerate_llt(const float &pt3, const int &dm, const std::string &wp_vs_jets, const std::string &wp_vs_mu, const std::string &wp_vs_ele, const std::string &corr_file, const std::string &shift) {
        auto cset = correction::CorrectionSet::from_file(corr_file);
        float sf;
        if (pt3>0.0) {
        auto ev = cset->at("jet_to_tau_fakerate");
        sf = ev->evaluate({wp_vs_jets, wp_vs_mu, wp_vs_ele, dm, pt3, shift});
        }
        else {
        sf = -10.;
        }
        return sf;
    };
    float tau_fakerate_ltt(const int &q1, const int &q2, const int &q3, const float &pt2, const float &pt3, const int &dm2, const int &dm3, const std::string &wp_vs_jets, const std::string &wp_vs_mu, const std::string &wp_vs_ele, const std::string &corr_file, const std::string &shift) {
        auto cset = correction::CorrectionSet::from_file(corr_file);
        auto ev = cset->at("jet_to_tau_fakerate");
        float sf;
        if (q1*q2>0.0 && q1*q3<0.0) {
            sf = ev->evaluate({wp_vs_jets, wp_vs_mu, wp_vs_ele, dm2, pt2, shift});
        }
        else if (q1*q3>0.0 && q1*q2<0.0) {
            sf = ev->evaluate({wp_vs_jets, wp_vs_mu, wp_vs_ele, dm3, pt3, shift});
        }
        else {
            sf = -10.; 
        }
        return sf;
    };
    float lep_fakerate(const float &pt, const std::string &corr_file, const std::string &shift) {
        float sf;
        if (pt>0.0) {
        auto cset = correction::CorrectionSet::from_file(corr_file);
        auto ev = cset->at("jet_to_lep_fakerate");
        sf = ev->evaluate({"Tight",pt, shift});
        }
        else {
        sf = -10.;
        }
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


def working_points(channel, wp_vs_jets):
    if channel == "emt" or channel == "met":
        wp_vs_jets = wp_vs_jets
        wp_vs_mu = "Tight"
        wp_vs_ele = "Tight"
    elif channel == "mmt":
        wp_vs_jets = wp_vs_jets
        wp_vs_mu = "Tight"
        wp_vs_ele = "VLoose"
    elif channel == "mtt":
        wp_vs_jets = wp_vs_jets
        wp_vs_mu = "Tight"
        wp_vs_ele = "VLoose"
    elif channel == "ett":
        wp_vs_jets = wp_vs_jets
        wp_vs_mu = "VLoose"
        wp_vs_ele = "Tight"
    return [wp_vs_jets, wp_vs_mu, wp_vs_ele]


def job_wrapper(args):
    return friend_producer(*args)


def check_file_exists_remote(serverpath, file_path):
    server_url = serverpath.split("store")[0][:-1]
    file_path = (
        "/store" + serverpath.split("store")[1] + file_path.replace(serverpath, "")
    )
    # print(f"Checking if {file_path} exists in {server_url}")
    myclient = client.FileSystem(server_url)
    status, listing = myclient.stat(file_path, DirListFlags.STAT)
    if status.ok:
        # print(f"{file_path} exists")
        return True
    else:
        # print(f"{file_path} does not exist")
        return False


def is_file_empty(inputfile, debug=False):
    try:
        rootfile = ROOT.TFile.Open(inputfile, "READ")
    except OSError:
        print(f"{inputfile} is broken")
        return True
    ntuple = rootfile.Get("ntuple")
    if len(ntuple.GetListOfLeaves()) < 1:
        print(f"{inputfile} is empty")
        if debug:
            print("Available keys: ", [x.GetTitle() for x in rootfile.GetListOfKeys()])
        rootfile.Close()
        return True
    rootfile.Close()
    return False


def friend_producer(
    inputfile,
    workdir,
    output_path,
    dataset_proc,
    era,
    channel,
    corr_file_dict_tau,
    corr_file_dict_ele,
    corr_file_dict_mu,
    wp_vs_jets,
    debug=True,
):
    temp_output_file = os.path.join(
        workdir, era, dataset_proc["nick"], channel, os.path.basename(inputfile)
    )
    final_output_file = os.path.join(
        output_path, era, dataset_proc["nick"], channel, os.path.basename(inputfile)
    )
    if era == "2016preVFP":
        corr_file_tau = corr_file_dict_tau["2016preVFP"]
        corr_file_ele = corr_file_dict_ele["2016preVFP"]
        corr_file_mu = corr_file_dict_mu["2016preVFP"]
    elif era == "2016postVFP":
        corr_file_tau = corr_file_dict_tau["2016postVFP"]
        corr_file_ele = corr_file_dict_ele["2016postVFP"]
        corr_file_mu = corr_file_dict_mu["2016postVFP"]    
    elif era == "2017":
        corr_file_tau = corr_file_dict_tau["2017"]
        corr_file_ele = corr_file_dict_ele["2017"]
        corr_file_mu = corr_file_dict_mu["2017"]
    elif era == "2018":
        corr_file_tau = corr_file_dict_tau["2018"]
        corr_file_ele = corr_file_dict_ele["2018"]
        corr_file_mu = corr_file_dict_mu["2018"]
    if debug:
        print(f"Processing {inputfile}")
        print(f"Outputting to {temp_output_file}")
    os.makedirs(os.path.dirname(temp_output_file), exist_ok=True)
    if channel in ["eem", "mme", "et", "mt"]:
        return
    if not is_file_empty(inputfile, debug):
        if not check_file_exists_remote(output_path, final_output_file):
            rdf = build_rdf(
                inputfile,
                channel,
                temp_output_file,
                corr_file_tau,
                corr_file_ele,
                corr_file_mu,
                wp_vs_jets,
            )
            upload_file(output_path, temp_output_file, final_output_file)
    else:
        if not check_file_exists_remote(output_path, final_output_file):
            print(f"{inputfile} is empty, generating empty friend tree")
            generate_empty_friend_tree(temp_output_file)
            upload_file(output_path, temp_output_file, final_output_file)


def build_rdf(
    inputfile,
    channel,
    output_file,
    corr_file_tau,
    corr_file_ele,
    corr_file_mu,
    wp_vs_jets,
):
    rootfile = ROOT.TFile.Open(inputfile, "READ")
    rdf = ROOT.RDataFrame("ntuple", rootfile)
    wp_vs_jets = working_points(channel, wp_vs_jets)[0]
    wp_vs_mu = working_points(channel, wp_vs_jets)[1]
    wp_vs_ele = working_points(channel, wp_vs_jets)[2]
    if channel in ["emt", "met", "mmt"]:
        rdf = rdf.Define(
            "tau_fakerate_Era",
            '(float) tau_fakerate_llt(pt_3, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "nom")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        rdf = rdf.Define(
            "tau_fakerate_CMS_ff_syst_EraUp",
            '(float) tau_fakerate_llt(pt_3, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "syst_up")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        rdf = rdf.Define(
            "tau_fakerate_CMS_ff_syst_EraDown",
            '(float) tau_fakerate_llt(pt_3, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "syst_down")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        rdf = rdf.Define(
            "tau_fakerate_CMS_ff_stat_EraUp",
            '(float) tau_fakerate_llt(pt_3, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "stat_up")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        rdf = rdf.Define(
            "tau_fakerate_CMS_ff_stat_EraDown",
            '(float) tau_fakerate_llt(pt_3, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "stat_down")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        if channel == "emt":
            rdf = rdf.Define(
                "lep_1_fakerate_Era",
                '(float) lep_fakerate(pt_1,"{corr_file}", "nom")'.format(
                    corr_file=corr_file_ele,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_syst_EraUp",
                '(float) lep_fakerate(pt_1,"{corr_file}", "syst_up")'.format(
                    corr_file=corr_file_ele,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_syst_EraDown",
                '(float) lep_fakerate(pt_1,"{corr_file}", "syst_down")'.format(
                    corr_file=corr_file_ele,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_stat_EraUp",
                '(float) lep_fakerate(pt_1,"{corr_file}", "stat_up")'.format(
                    corr_file=corr_file_ele,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_stat_EraDown",
                '(float) lep_fakerate(pt_1,"{corr_file}", "stat_down")'.format(
                    corr_file=corr_file_ele,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_Era",
                '(float) lep_fakerate(pt_2,"{corr_file}", "nom")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_syst_EraUp",
                '(float) lep_fakerate(pt_2,"{corr_file}", "syst_up")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_syst_EraDown",
                '(float) lep_fakerate(pt_2,"{corr_file}", "syst_down")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_stat_EraUp",
                '(float) lep_fakerate(pt_2,"{corr_file}", "stat_up")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_stat_EraDown",
                '(float) lep_fakerate(pt_2,"{corr_file}", "stat_down")'.format(
                    corr_file=corr_file_mu,
                ),
            )
        elif channel == "met":
            rdf = rdf.Define(
                "lep_1_fakerate_Era",
                '(float) lep_fakerate(pt_1,"{corr_file}", "nom")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_syst_EraUp",
                '(float) lep_fakerate(pt_1,"{corr_file}", "syst_up")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_syst_EraDown",
                '(float) lep_fakerate(pt_1,"{corr_file}", "syst_down")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_stat_EraUp",
                '(float) lep_fakerate(pt_1,"{corr_file}", "stat_up")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_stat_EraDown",
                '(float) lep_fakerate(pt_1,"{corr_file}", "stat_down")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_Era",
                '(float) lep_fakerate(pt_2,"{corr_file}", "nom")'.format(
                    corr_file=corr_file_ele,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_syst_EraUp",
                '(float) lep_fakerate(pt_2,"{corr_file}", "syst_up")'.format(
                    corr_file=corr_file_ele,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_syst_EraDown",
                '(float) lep_fakerate(pt_2,"{corr_file}", "syst_down")'.format(
                    corr_file=corr_file_ele,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_stat_EraUp",
                '(float) lep_fakerate(pt_2,"{corr_file}", "stat_up")'.format(
                    corr_file=corr_file_ele,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_stat_EraDown",
                '(float) lep_fakerate(pt_2,"{corr_file}", "stat_down")'.format(
                    corr_file=corr_file_ele,
                ),
            )
        elif channel == "mmt":
            rdf = rdf.Define(
                "lep_1_fakerate_Era",
                '(float) lep_fakerate(pt_1,"{corr_file}", "nom")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_syst_EraUp",
                '(float) lep_fakerate(pt_1,"{corr_file}", "syst_up")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_syst_EraDown",
                '(float) lep_fakerate(pt_1,"{corr_file}", "syst_down")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_stat_EraUp",
                '(float) lep_fakerate(pt_1,"{corr_file}", "stat_up")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_1_fakerate_CMS_ff_stat_EraDown",
                '(float) lep_fakerate(pt_1,"{corr_file}", "stat_down")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_Era",
                '(float) lep_fakerate(pt_2,"{corr_file}", "nom")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_syst_EraUp",
                '(float) lep_fakerate(pt_2,"{corr_file}", "syst_up")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_syst_EraDown",
                '(float) lep_fakerate(pt_2,"{corr_file}", "syst_down")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_stat_EraUp",
                '(float) lep_fakerate(pt_2,"{corr_file}", "stat_up")'.format(
                    corr_file=corr_file_mu,
                ),
            )
            rdf = rdf.Define(
                "lep_2_fakerate_CMS_ff_stat_EraDown",
                '(float) lep_fakerate(pt_2,"{corr_file}", "stat_up")'.format(
                    corr_file=corr_file_mu,
                ),
            )
        rdf.Snapshot(
            "ntuple",
            output_file,
            [
                "tau_fakerate_Era",
                "tau_fakerate_CMS_ff_syst_EraUp",
                "tau_fakerate_CMS_ff_syst_EraDown",
                "tau_fakerate_CMS_ff_stat_EraUp",
                "tau_fakerate_CMS_ff_stat_EraDown",
                "lep_1_fakerate_Era",
                "lep_1_fakerate_CMS_ff_syst_EraUp",
                "lep_1_fakerate_CMS_ff_syst_EraDown",
                "lep_1_fakerate_CMS_ff_stat_EraUp",
                "lep_1_fakerate_CMS_ff_stat_EraDown",
                "lep_2_fakerate_Era",
                "lep_2_fakerate_CMS_ff_syst_EraUp",
                "lep_2_fakerate_CMS_ff_syst_EraDown",
                "lep_2_fakerate_CMS_ff_stat_EraUp",
                "lep_2_fakerate_CMS_ff_stat_EraDown",
            ],
        )
    elif channel in ["ett", "mtt"]:
        rdf = rdf.Define(
            "tau_fakerate_Era",
            '(float) tau_fakerate_ltt(q_1, q_2, q_3, pt_2, pt_3, decaymode_2, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "nom")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        rdf = rdf.Define(
            "tau_fakerate_CMS_ff_syst_EraUp",
            '(float) tau_fakerate_ltt(q_1, q_2, q_3, pt_2, pt_3, decaymode_2, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "syst_up")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        rdf = rdf.Define(
            "tau_fakerate_CMS_ff_syst_EraDown",
            '(float) tau_fakerate_ltt(q_1, q_2, q_3, pt_2, pt_3, decaymode_2, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "syst_down")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        rdf = rdf.Define(
            "tau_fakerate_CMS_ff_stat_EraUp",
            '(float) tau_fakerate_ltt(q_1, q_2, q_3, pt_2, pt_3, decaymode_2, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "stat_up")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        rdf = rdf.Define(
            "tau_fakerate_CMS_ff_stat_EraDown",
            '(float) tau_fakerate_ltt(q_1, q_2, q_3, pt_2, pt_3, decaymode_2, decaymode_3, "{wp_vs_jets}", "{wp_vs_mu}", "{wp_vs_ele}", "{corr_file}", "stat_down")'.format(
                wp_vs_jets=wp_vs_jets,
                wp_vs_mu=wp_vs_mu,
                wp_vs_ele=wp_vs_ele,
                corr_file=corr_file_tau,
            ),
        )
        rdf.Snapshot(
            "ntuple",
            output_file,
            [
                "tau_fakerate_Era",
                "tau_fakerate_CMS_ff_syst_EraUp",
                "tau_fakerate_CMS_ff_syst_EraDown",
                "tau_fakerate_CMS_ff_stat_EraUp",
                "tau_fakerate_CMS_ff_stat_EraDown",
            ],
        )
    rootfile.Close()
    return


def upload_file(redirector, input_file, output_file, max_retries=10):
    success = False
    n = 0
    while not success and n < max_retries:
        if output_file.startswith("root://"):
            os.system(f"xrdcp {input_file} {output_file}")
            if check_file_exists_remote(redirector, output_file):
                success = True
            else:
                print(f"Failed to upload {output_file}")
                print(f"Retrying {n+1}/{max_retries}")
                n += 1
        else:
            if not os.path.exists(os.path.dirname(output_file)):
                os.makedirs(os.path.dirname(output_file))
            os.system(f"mv {input_file} {output_file}")
            success = True


def generate_empty_friend_tree(output_file):
    friend_tree = ROOT.TFile(output_file, "CREATE")
    tree = ROOT.TTree("ntuple", "")
    tree.Write()
    friend_tree.Close()


def generate_friend_trees(
    dataset,
    ntuples,
    nthreads,
    workdir,
    output_path,
    corr_file_dict_tau,
    corr_file_dict_ele,
    corr_file_dict_mu,
    wp_vs_jets,
    debug,
):
    print("Using {} threads".format(nthreads))
    arguments = [
        (
            ntuple,
            workdir,
            output_path,
            dataset[parse_filepath(ntuple)["nick"]],
            parse_filepath(ntuple)["era"],
            parse_filepath(ntuple)["channel"],
            corr_file_dict_tau,
            corr_file_dict_ele,
            corr_file_dict_mu,
            wp_vs_jets,
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
    workdir = os.path.join(args.tempdir)
    dataset = yaml.safe_load(open(args.dataset_config))
    wp_vs_jets = args.wp_vs_jets
    ntuples = glob.glob(base_path)
    print(args.eras)
    corr_file_dict_tau = {}
    corr_file_dict_ele = {}
    corr_file_dict_mu = {}
    if "2016preVFP" in args.eras:
        corr_file_dict_tau["2016preVFP"] = args.corr_file_tau_16preVFP
        corr_file_dict_ele["2016preVFP"] = args.corr_file_ele_16preVFP
        corr_file_dict_mu["2016preVFP"] = args.corr_file_mu_16preVFP
    if "2016postVFP" in args.eras:
        corr_file_dict_tau["2016postVFP"] = args.corr_file_tau_16postVFP
        corr_file_dict_ele["2016postVFP"] = args.corr_file_ele_16postVFP
        corr_file_dict_mu["2016postVFP"] = args.corr_file_mu_16postVFP
    if "2017" in args.eras:
        corr_file_dict_tau["2017"] = args.corr_file_tau_17
        corr_file_dict_ele["2017"] = args.corr_file_ele_17
        corr_file_dict_mu["2017"] = args.corr_file_mu_17
    if "2018" in args.eras:
        corr_file_dict_tau["2018"] = args.corr_file_tau_18
        corr_file_dict_ele["2018"] = args.corr_file_ele_18
        corr_file_dict_mu["2018"] = args.corr_file_mu_18
    if base_path.startswith("root://"):
        ntuples = xrdglob.glob(base_path)
    else:
        ntuples = glob.glob(base_path)
    print("Found {} ntuples".format(len(ntuples)))
    nthreads = args.nthreads
    generate_friend_trees(
        dataset,
        ntuples,
        nthreads,
        workdir,
        output_path,
        corr_file_dict_tau,
        corr_file_dict_ele,
        corr_file_dict_mu,
        wp_vs_jets,
        args.debug,
    )
    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    print("Done")
