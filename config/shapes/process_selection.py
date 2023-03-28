from ntuple_processor.utils import Selection


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


def lumi_weight(era):
    if era == "2016":
        lumi = "35.87"
    elif era == "2017":
        lumi = "41.529"
    elif era == "2018":
        lumi = "59.7"
    else:
        raise ValueError("Given era {} not defined.".format(era))
    return ("{} * 1000.0".format(lumi), "lumi")


# for the tauid weights its necessary to define the weight also in the anti iso region for the fake rate application
def MC_base_process_selection(channel, era):
    if channel in ["emt", "met"]:
        tauidweight = (
            "((gen_match_3==5)*((id_tau_vsJet_VTight_3>0.5)*id_wgt_tau_vsJet_VTight_3 + (id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5))",
            "taubyIsoIdWeight",
        )
        vsmu_weight = ("id_wgt_tau_vsMu_Tight_3", "vsmuweight")
        vsele_weight = ("id_wgt_tau_vsEle_Tight_3", "vseleweight")
        if channel == "emt":
            isoweight = ("iso_wgt_mu_2*(iso_2<0.15)+1.*(iso_2>0.15)", "isoweight")
            idweight = (
                "(id_wgt_ele_wp90nonIso_1*electron_is_nonisowp90_1>0.5+1.0*electron_is_nonisowp90_1<0.5)*(id_wgt_mu_2*muon_is_mediumid_2 > 0.5 + 1.0*muon_is_mediumid_2 < 0.5)",
                "idweight",
            )
            trgweight = (
                "(pt_2>=25 * trg_wgt_single_mu24) + ((pt_1>33 && pt_2<25)* trg_wgt_single_ele32)",
                "trgweight",
            )
        elif channel == "met":
            isoweight = ("iso_wgt_mu_1*(iso_1<0.15)+1.*(iso_1>0.15)", "isoweight")
            idweight = (
                "(id_wgt_mu_1*muon_is_mediumid_1>0.5+1.0*muon_is_mediumid_1<0.5) * (id_wgt_ele_wp90nonIso_2*electron_is_nonisowp90_2>0.5+1.0*electron_is_nonisowp90_2<0.5)",
                "idweight",
            )
            trgweight = (
                "(pt_1>=25 * trg_wgt_single_mu24) + ((pt_2>33 && pt_1<25)* trg_wgt_single_ele32)",
                "trgweight",
            )
    elif channel == "mmt":
        tauidweight = (
            "((gen_match_3==5)*((id_tau_vsJet_VTight_3>0.5)*id_wgt_tau_vsJet_VTight_3 + (id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5))",
            "taubyIsoIdWeight",
        )
        vsmu_weight = ("id_wgt_tau_vsMu_Tight_3", "vsmuweight")
        vsele_weight = ("id_wgt_tau_vsEle_VLoose_3", "vseleweight")

        isoweight = (
            "(iso_wgt_mu_1*(iso_1<0.15)+1.*(iso_1>0.15))*(iso_wgt_mu_2*(iso_2<0.15)+1.*(iso_2>0.15))",
            "isoweight",
        )
        idweight = (
            "id_wgt_mu_1 * (id_wgt_mu_2*muon_is_mediumid_2 > 0.5 + 1.0*muon_is_mediumid_2 < 0.5)",
            "idweight",
        )
        trgweight = (
            "(pt_1>=25 * trg_wgt_single_mu24)",
            "trgweight",
        )
    elif channel == "ett":
        tauidweight = (
            "((gen_match_3==5)*((id_tau_vsJet_VTight_3>0.5)*id_wgt_tau_vsJet_VTight_3+(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5)) * ((gen_match_2==5)*((id_tau_vsJet_VTight_2>0.5)*id_wgt_tau_vsJet_VTight_2+(id_tau_vsJet_VTight_2<0.5&&id_tau_vsJet_VVVLoose_2>0.5)*id_wgt_tau_vsJet_VVVLoose_2) + (gen_match_2!=5))",
            "taubyIsoIdWeight",
        )
        vsmu_weight = (
            "id_wgt_tau_vsMu_VLoose_3*id_wgt_tau_vsMu_VLoose_2",
            "vsmuweight",
        )
        vsele_weight = (
            "id_wgt_tau_vsEle_Tight_3*id_wgt_tau_vsEle_Tight_2",
            "vseleweight",
        )

        isoweight = ("1", "isoweight")
        idweight = ("id_wgt_ele_wp90nonIso_1", "idweight")
        trgweight = ("pt_1>33 * trg_wgt_single_ele32", "trgweight")
    elif channel == "mtt":
        tauidweight = (
            "((gen_match_3==5)*((id_tau_vsJet_VTight_3>0.5)*id_wgt_tau_vsJet_VTight_3+(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5)) * ((gen_match_2==5)*((id_tau_vsJet_VTight_2>0.5)*id_wgt_tau_vsJet_VTight_2+(id_tau_vsJet_VTight_2<0.5&&id_tau_vsJet_VVVLoose_2>0.5)*id_wgt_tau_vsJet_VVVLoose_2) + (gen_match_2!=5))",
            "taubyIsoIdWeight",
        )
        vsmu_weight = (
            "id_wgt_tau_vsMu_Tight_3*id_wgt_tau_vsMu_Tight_2",
            "vsmuweight",
        )
        vsele_weight = (
            "id_wgt_tau_vsEle_VLoose_3*id_wgt_tau_vsEle_VLoose_2",
            "vseleweight",
        )

        isoweight = ("iso_wgt_mu_1", "isoweight")
        idweight = ("id_wgt_mu_1", "idweight")
        trgweight = (
            "(pt_1>=25 * trg_wgt_single_mu24)",
            "trgweight",
        )
    MC_base_process_weights = [
        ("puweight", "puweight"),
        lumi_weight(era),
        isoweight,
        idweight,
        tauidweight,
        vsmu_weight,
        vsele_weight,
        trgweight,
    ]
    return Selection(name="MC_base", weights=MC_base_process_weights)


def DY_process_selection(channel, era):
    DY_process_weights = MC_base_process_selection(channel, era).weights
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


def TT_process_selection(channel, era):
    TT_process_weights = MC_base_process_selection(channel, era).weights
    TT_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
            ("topPtReweightWeight", "topPtReweightWeight"),
        ]
    )
    return Selection(name="TT", weights=TT_process_weights)


def VV_process_selection(channel, era):
    VV_process_weights = MC_base_process_selection(channel, era).weights
    VV_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
        ]
    )
    return Selection(name="VV", weights=VV_process_weights)


def WWW_process_selection(channel, era):
    WWW_process_weights = MC_base_process_selection(channel, era).weights
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
    return Selection(name="WWW", weights=WWW_process_weights)


def WWZ_process_selection(channel, era):
    WWZ_process_weights = MC_base_process_selection(channel, era).weights
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
    return Selection(name="WWZ", weights=WWZ_process_weights)


def WZZ_process_selection(channel, era):
    WZZ_process_weights = MC_base_process_selection(channel, era).weights
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
    return Selection(name="WZZ", weights=WZZ_process_weights)


def ZZZ_process_selection(channel, era):
    ZZZ_process_weights = MC_base_process_selection(channel, era).weights
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
    return Selection(name="ZZZ", weights=ZZZ_process_weights)


def VVV_process_selection(channel, era):
    VVV_process_weights = MC_base_process_selection(channel, era).weights
    VVV_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
        ]
    )
    return Selection(name="VVV", weights=VVV_process_weights)


def W_process_selection(channel, era):
    W_process_weights = MC_base_process_selection(channel, era).weights
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


def HTT_process_selection(channel, era):
    HTT_weights = HTT_base_process_selection(channel, era).weights + [
        ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
        ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
        (
            "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
            "generator_weight",
        ),
    ]
    return Selection(name="HTT", weights=HTT_weights)


def HWW_process_selection(channel, era):
    HWW_process_weights = MC_base_process_selection(channel, era).weights
    HWW_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
        ]
    )
    return Selection(name="HWW", weights=HWW_process_weights)


def VH_process_selection(channel, era):
    VH_process_weights = MC_base_process_selection(channel, era).weights
    VH_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
        ]
    )
    return Selection(name="VH", weights=VH_process_weights)
