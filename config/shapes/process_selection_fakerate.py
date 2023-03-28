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
        tauidweight = (
            "((gen_match_3==5)*id_wgt_tau_vsJet_{wp_vs_jet}_3 + (gen_match_3!=5))".format(
                wp_vs_jet=wp_vs_jet
            ),
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
    elif channel == "mme":
        isoweight = ("iso_wgt_mu_1 * iso_wgt_mu_2", "isoweight")
        # idweight = ("id_wgt_mu_1 * id_wgt_mu_2", "idweight")
        idweight = ("id_wgt_mu_1 * id_wgt_mu_2* id_wgt_ele_wp90nonIso_3", "idweight")
        trgweight = (
            "(pt_1>=25 * trg_wgt_single_mu24)",
            "trgweight",
        )
        # if id_wp_ele == "Tight":
        #     idweight = (
        #         "id_wgt_mu_1 * id_wgt_mu_2 * id_wgt_ele_wp90nonIso_3",
        #         "idweight",
        #     )
        # else:
        #     idweight = (
        #         "id_wgt_mu_1 * id_wgt_mu_2*((electron_is_nonisowp90_3>0.5)*id_wgt_ele_wp90nonIso_3+1.0*(electron_is_nonisowp90_3<0.5))",
        #         "idweight",
        #     )
        MC_base_process_weights = [
            ("puweight", "puweight"),
            lumi_weight(era),
            isoweight,
            idweight,
            trgweight,
        ]
    elif channel == "eem":
        idweight = (
            "id_wgt_ele_wp90nonIso_1 * id_wgt_ele_wp90nonIso_2 * id_wgt_mu_3",
            "idweight",
        )
        # idweight = ("id_wgt_ele_wp90nonIso_1 * id_wgt_ele_wp90nonIso_2", "idweight")
        trgweight = (
            "pt_1>33* trg_wgt_single_ele32",
            "trgweight",
        )
        isoweight = ("1", "isoweight")
        if id_wp_mu == "Tight":
            # idweight = (
            #     "id_wgt_ele_wp90nonIso_1 * id_wgt_ele_wp90nonIso_2 * id_wgt_mu_3",
            #     "idweight",
            # )
            isoweight = ("iso_wgt_mu_3", "isoweight")
        # else:
        #     idweight = (
        #         "id_wgt_ele_wp90nonIso_1 * id_wgt_ele_wp90nonIso_2 * (id_wgt_mu_3*(muon_is_mediumid_3 > 0.5)+1.0*(muon_is_mediumid_3 < 0.5))",
        #         "idweight",
        #     )
        #     isoweight = ("iso_wgt_mu_3*(iso_3<0.15)+1.0*(iso_3>0.15)", "isoweight")
        MC_base_process_weights = [
            ("puweight", "puweight"),
            lumi_weight(era),
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


def VV_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    VV_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
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


def WWW_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    WWW_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
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


def WWZ_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    WWZ_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
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


def WZZ_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    WZZ_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
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


def ZZZ_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    ZZZ_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
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


def VVV_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    VVV_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
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


def VH_process_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
):
    VH_process_weights = MC_base_process_selection(
        channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, id_wp_ele, id_wp_mu
    ).weights
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
