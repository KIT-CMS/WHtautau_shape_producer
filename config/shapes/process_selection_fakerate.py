from ntuple_processor.utils import Selection
import json

"""Base processes

List of base processes, mostly containing only weights:
    - triggerweight
    - triggerweight_emb
    - tau_by_iso_id_weight
    - ele_hlt_Z_vtx_weight
    - ele_reco_weight
    - aiso_muon_correction
    - lumi_weight
    - MC_base_process_selection
    - DY_base_process_selection
    - TT_process_selection
    - VV_process_selection
    - W_process_selection
    - HTT_base_process_selection
    - HTT_process_selection
    - HWW_process_selection
"""


def btag_correction(era, channel, proc):
    file_path = "/work/rschmieder/WH_analysis/btagweight_study/shape_producer/WHtautau_shape_producer/btagweight_corrfactors_FF.json"
    with open(file_path, "r") as json_file:
        corr_factors = json.load(json_file)
    corr_factor = corr_factors[era][channel][proc]
    return corr_factor


def lumi_weight(era):
    if era == "2016preVFP":
        lumi = "19.5"  # "36.326450080"
    elif era == "2016postVFP":
        lumi = "16.8"
    elif era == "2017":
        lumi = "41.529"
    elif era == "2018":
        lumi = "59.83"
    else:
        raise ValueError("Given era {} not defined.".format(era))
    return ("{} * 1000.0".format(lumi), "lumi")


def prefiring_weight(era):
    if era in ["2016preVFP", "2016postVFP", "2017"]:
        weight = ("prefiring_wgt", "prefiring_wgt")
    else:
        weight = ("1.0", "prefiring_wgt")
    return weight


def MC_base_process_selection(
    channel,
    era,
    wp_vs_jet,
    wp_vs_mu,
    wp_vs_ele,
    id_wp_ele,
    id_wp_mu,
):
    if channel == "mmt":
        if wp_vs_jet in ["VTight", "Tight", "Medium", "Loose"]:
            tauidweight = (
                "((gen_match_3==5)*id_wgt_tau_vsJet_{wp_vs_jet}_3 + (gen_match_3!=5))".format(
                    wp_vs_jet=wp_vs_jet
                ),
                "taubyIsoIdWeight",
            )
        else:
            tauidweight = (
                "1",
                "taubyIsoIdWeight",
            )
        vsmu_weight = (
            "id_wgt_tau_vsMu_{wp_vs_mu}_3".format(wp_vs_mu=wp_vs_mu),
            "vsmuweight",
        )
        vsele_weight = (
            "id_wgt_tau_vsEle_{wp_vs_ele}_3".format(wp_vs_ele=wp_vs_ele),
            "vseleweight",
        )

        isoweight = ("iso_wgt_mu_1 * iso_wgt_mu_2", "isoweight")
        idweight = ("id_wgt_mu_1 * id_wgt_mu_2", "idweight")
        if "2016" in era:
            trgweight = (
                "(pt_1>=23 * trg_wgt_single_mu22)",
                "trgweight",
            )
        else:
            trgweight = (
                "trg_wgt_single_mu24ormu27",
                "trgweight",
            )
        MC_base_process_weights = [
            ("btag_weight", "btagWeight"),
            ("puweight", "puweight"),
            lumi_weight(era),
            prefiring_weight(era),
            isoweight,
            idweight,
            tauidweight,
            vsmu_weight,
            vsele_weight,
            trgweight,
        ]
    elif channel == "mme":
        isoweight = (
            "iso_wgt_mu_1 * iso_wgt_mu_2*(iso_wgt_ele_3*(iso_3<0.15)+1.*(iso_3>0.15))",
            "isoweight",
        )
        idweight = (
            "id_wgt_mu_1 * id_wgt_mu_2* (id_wgt_ele_wp90nonIso_3*electron_is_nonisowp90_3>0.5+1.0*electron_is_nonisowp90_3<0.5)",
            "idweight",
        )
        recoweight = (
            "((pt_3<20.)*reco_ptst20_wgt_ele_3)+((pt_3>20.)*reco_ptgt20_wgt_ele_3)",
            "recoweight",
        )
        if "2016" in era:
            trgweight = (
                "(pt_1>=23 * trg_wgt_single_mu22)",
                "trgweight",
            )
        else:
            trgweight = (
                "trg_wgt_single_mu24ormu27",
                "trgweight",
            )
        MC_base_process_weights = [
            ("puweight", "puweight"),
            lumi_weight(era),
            recoweight,
            isoweight,
            idweight,
            trgweight,
        ]
    elif channel == "eem":
        idweight = (
            "id_wgt_ele_wp90nonIso_1 * id_wgt_ele_wp90nonIso_2 * (id_wgt_mu_3*(muon_is_mediumid_3>0.5)+1.0*(muon_is_mediumid_3<0.5))",
            "idweight",
        )
        isoweight = (
            "iso_wgt_ele_1*iso_wgt_ele_2*(iso_wgt_mu_3*(iso_3<0.15)+1.*(iso_3>0.15))",
            "isoweight",
        )
        recoweight = (
            "(((pt_1<20.)*reco_ptst20_wgt_ele_1)+((pt_1>20.)*reco_ptgt20_wgt_ele_1))*(((pt_2<20.)*reco_ptst20_wgt_ele_2)+((pt_2>20.)*reco_ptgt20_wgt_ele_2))",
            "recoweight",
        )
        if "2016" in era:
            trgweight = ("trg_wgt_single_ele25", "trgweight")
        elif "2017" in era:
            trgweight = ("trg_wgt_single_ele27orele32orele35", "trgweight")
        elif "2018" in era:
            trgweight = ("trg_wgt_single_ele32orele35", "trgweight")
        MC_base_process_weights = [
            ("btag_weight", "btagWeight"),
            ("puweight", "puweight"),
            lumi_weight(era),
            recoweight,
            isoweight,
            idweight,
            trgweight,
        ]
    return Selection(name="MC_base", weights=MC_base_process_weights)


def DY_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    DY_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    DY_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
            ("ZPtMassReweightWeight", "zPtReweightWeight"),
        ]
    )
    return Selection(name="DY", weights=DY_process_weights)


def TT_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    TT_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    btag_corr = btag_correction(era, channel, "tt_procs")
    TT_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
            ("topPtReweightWeight", "topPtReweightWeight"),
            ("{btag_corr}".format(btag_corr=btag_corr), "btag_correction"),
        ]
    )
    return Selection(name="TT", weights=TT_process_weights)


def VV_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    VV_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    btag_corr = btag_correction(era, channel, "vv_procs")
    VV_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
            ("{btag_corr}".format(btag_corr=btag_corr), "btag_correction"),
        ]
    )
    return Selection(name="VV", weights=VV_process_weights)


def WWW_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    WWW_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    if era == "2018":
        WWW_process_weights.extend(
            [
                ("1./(240000+9894000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2017":
        WWW_process_weights.extend(
            [
                ("1./(171000+9854000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016postVFP":
        WWW_process_weights.extend(
            [
                ("1./(69000+4159000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016preVFP":
        WWW_process_weights.extend(
            [
                ("1./(71000+5190000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    return Selection(name="WWW", weights=WWW_process_weights)


def WWZ_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    WWZ_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    if era == "2018":
        WWZ_process_weights.extend(
            [
                ("1./(248000+9961999)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2017":
        WWZ_process_weights.extend(
            [
                ("1./(178000+9938400)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016postVFP":
        WWZ_process_weights.extend(
            [
                ("1./(67000+4595000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016preVFP":
        WWZ_process_weights.extend(
            [
                ("1./(81000+5072000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    return Selection(name="WWZ", weights=WWZ_process_weights)


def WZZ_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    WZZ_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    if era == "2018":
        WZZ_process_weights.extend(
            [
                ("1./(300000+9994000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2017":
        WZZ_process_weights.extend(
            [
                ("1./(298000+9898000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016postVFP":
        WZZ_process_weights.extend(
            [
                ("1./(137000+4191000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016preVFP":
        WZZ_process_weights.extend(
            [
                ("1./(160000+5394000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    return Selection(name="WZZ", weights=WZZ_process_weights)


def ZZZ_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    ZZZ_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    if era == "2018":
        ZZZ_process_weights.extend(
            [
                ("1./(250000+9889000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2017":
        ZZZ_process_weights.extend(
            [
                ("1./(178000+9524000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016postVFP":
        ZZZ_process_weights.extend(
            [
                ("1./(72000+4534000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016postVFP":
        ZZZ_process_weights.extend(
            [
                ("1./(72000+4534000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016preVFP":
        ZZZ_process_weights.extend(
            [
                ("1./(81000+5302000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    return Selection(name="ZZZ", weights=ZZZ_process_weights)


# collection of ZZZ,WZZ,WWZ,WWW processes. To ensure every event has the same weight as if the process selection for the four processes were seperated, the numberofgeneratedeventsweight has to be the same. This is ensured by hard coding the crosssection (from datasets.yaml in the sample database repo). The condition has the queue ZZZ,WZZ,WWZ,WWW
def VVV_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    VVV_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    btag_corr = btag_correction(era, channel, "vvv_procs")
    if era == "2016preVFP":
        VVV_process_weights.extend(
            [
                (
                    "(crossSectionPerEventWeight<0.01477&&crossSectionPerEventWeight>0.01475)*1./(81000+5302000)+(crossSectionPerEventWeight<0.05710&&crossSectionPerEventWeight>0.05708)*1./(160000+5394000)+(crossSectionPerEventWeight<0.1708&&crossSectionPerEventWeight>0.1706)*1./(81000+5072000)+(crossSectionPerEventWeight<0.2159&&crossSectionPerEventWeight>0.2157)*1./(71000+5190000)",
                    "numberGeneratedEventsWeight",
                ),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
                ("{btag_corr}".format(btag_corr=btag_corr), "btag_correction"),
            ]
        )
    elif era == "2016postVFP":
        VVV_process_weights.extend(
            [
                (
                    "(crossSectionPerEventWeight<0.01477&&crossSectionPerEventWeight>0.01475)*1./(72000+4534000)+(crossSectionPerEventWeight<0.05710&&crossSectionPerEventWeight>0.05708)*1./(137000+4554000)+(crossSectionPerEventWeight<0.1708&&crossSectionPerEventWeight>0.1706)*1./(67000+4595000)+(crossSectionPerEventWeight<0.2159&&crossSectionPerEventWeight>0.2157)*1./(69000+4159000)",
                    "numberGeneratedEventsWeight",
                ),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
                ("{btag_corr}".format(btag_corr=btag_corr), "btag_correction"),
            ]
        )
    elif era == "2017":
        VVV_process_weights.extend(
            [
                (
                    "(crossSectionPerEventWeight<0.01477&&crossSectionPerEventWeight>0.01475)*1./(178000+9524000)+(crossSectionPerEventWeight<0.05710&&crossSectionPerEventWeight>0.05708)*1./(298000+9898000)+(crossSectionPerEventWeight<0.1708&&crossSectionPerEventWeight>0.1706)*1./(178000+9938400)+(crossSectionPerEventWeight<0.2159&&crossSectionPerEventWeight>0.2157)*1./(171000+9854000)",
                    "numberGeneratedEventsWeight",
                ),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
                ("{btag_corr}".format(btag_corr=btag_corr), "btag_correction"),
            ]
        )
    elif era == "2018":
        VVV_process_weights.extend(
            [
                (
                    "(crossSectionPerEventWeight<0.01477&&crossSectionPerEventWeight>0.01475)*1./(250000+9889000)+(crossSectionPerEventWeight<0.05710&&crossSectionPerEventWeight>0.05708)*1./(300000+9994000)+(crossSectionPerEventWeight<0.1708&&crossSectionPerEventWeight>0.1706)*1./(248000+9961999)+(crossSectionPerEventWeight<0.2159&&crossSectionPerEventWeight>0.2157)*1./(240000+9894000)",
                    "numberGeneratedEventsWeight",
                ),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
                ("{btag_corr}".format(btag_corr=btag_corr), "btag_correction"),
            ]
        )
    return Selection(name="VVV", weights=VVV_process_weights)


def W_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    W_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    W_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
        ]
    )
    # W_process_weights.append(W_stitching_weight(era)) # TODO add W stitching weight in when npartons is available
    return Selection(name="W", weights=W_process_weights)


def HTT_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    HTT_weights = HTT_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights + [
        ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
        ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
        (
            "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
            "generator_weight",
        ),
    ]
    return Selection(name="HTT", weights=HTT_weights)


def HWW_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    HWW_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    btag_corr = btag_correction(era, channel, "vh_procs")
    HWW_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
            ("{btag_corr}".format(btag_corr=btag_corr), "btag_correction"),
        ]
    )
    return Selection(name="HWW", weights=HWW_process_weights)


def VH_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    VH_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    btag_corr = btag_correction(era, channel, "vh_procs")
    VH_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
            ("{btag_corr}".format(btag_corr=btag_corr), "btag_correction"),
        ]
    )
    return Selection(name="VH", weights=VH_process_weights)


def H_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    H_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
    btag_corr = btag_correction(era, channel, "vh_procs")
    H_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
            ("{btag_corr}".format(btag_corr=btag_corr), "btag_correction"),
        ]
    )
    return Selection(name="H", weights=H_process_weights)
