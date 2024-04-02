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


# for the tauid weights its necessary to define the weight also in the anti iso region for the fake rate application
def MC_base_process_selection(channel, era):
    if channel in ["emt", "met"]:
        tauidweight = (
            "((gen_match_3==5)*((id_tau_vsJet_Tight_3>0.5)*id_wgt_tau_vsJet_Tight_3 + (id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5))",
            "taubyIsoIdWeight",
        )
        vsmu_weight = ("id_wgt_tau_vsMu_Tight_3", "vsmuweight")
        vsele_weight = ("id_wgt_tau_vsEle_Tight_3", "vseleweight")
        if channel == "emt":
            isoweight = (
                "(iso_wgt_mu_2*(iso_2<0.15)+1.*(iso_2>0.15))*(iso_wgt_ele_1*(iso_1<0.15)+1.*(iso_1>0.15))",
                "isoweight",
            )
            idweight = (
                "(id_wgt_ele_wp90nonIso_1*electron_is_nonisowp90_1>0.5+1.0*electron_is_nonisowp90_1<0.5)*(id_wgt_mu_2*muon_is_mediumid_2 > 0.5 + 1.0*muon_is_mediumid_2 < 0.5)",
                "idweight",
            )
            if "2016" in era:
                trgweight = (
                    "((pt_2>=23&&pt_1<=26) * trg_wgt_single_mu22) + ((pt_1>26) * trg_wgt_single_ele25)",
                    "trgweight",
                )
            elif era == "2017":
                trgweight = (
                    "(((pt_2>=28*trg_wgt_single_mu27)+((pt_2>25&&pt_2<28)*trg_wgt_single_mu24))*(pt_1<28) && (abs(eta_2)<2.1))+((pt_1>=28)*trg_wgt_single_ele27orele32orele35)",
                    "trgweight",
                )
            elif era == "2018":
                trgweight = (
                    "(((pt_2>=28*trg_wgt_single_mu27)+((pt_2>25&&pt_2<28)*trg_wgt_single_mu24))*(pt_1<33) && (abs(eta_2)<2.1))+(pt_1>=33*trg_wgt_single_ele32orele35)",
                    "trgweight",
                )
        elif channel == "met":
            isoweight = (
                "(iso_wgt_mu_1*(iso_1<0.15)+1.*(iso_1>0.15))*(iso_wgt_ele_2*(iso_2<0.15)+1.*(iso_2>0.15))",
                "isoweight",
            )
            idweight = (
                "(id_wgt_mu_1*muon_is_mediumid_1>0.5+1.0*muon_is_mediumid_1<0.5) * (id_wgt_ele_wp90nonIso_2*electron_is_nonisowp90_2>0.5+1.0*electron_is_nonisowp90_2<0.5)",
                "idweight",
            )
            if "2016" in era:
                trgweight = (
                    "(pt_1>=23 * trg_wgt_single_mu22) + ((pt_2>26 && pt_1<23)* trg_wgt_single_ele25)",
                    "trgweight",
                )
            elif era == "2017":
                trgweight = (
                    "(((trg_wgt_single_mu27*(pt_1>27))+(trg_wgt_single_mu24*(pt_1<=27&&pt_1>25))*(abs(eta_1)<2.4)) +((pt_1 < 25 &&pt_1>=28)*trg_wgt_single_ele27orele32orele35))",
                    "trgweight",
                )
            elif era == "2018":
                trgweight = (
                    "(((trg_wgt_single_mu27*pt_1>27)+(trg_wgt_single_mu24*(pt_1<=27&&pt_1>25))*(abs(eta_1)<2.4))+ (pt_1 < 25 && (abs(eta_2)<2.1)*((pt_1>=33*trg_wgt_single_ele32orele35))))",
                    "trgweight",
                )
    elif channel == "mmt":
        tauidweight = (
            "((gen_match_3==5)*((id_tau_vsJet_Tight_3>0.5)*id_wgt_tau_vsJet_Tight_3 + (id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5))",
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
        if "2016" in era:
            trgweight = (
                "(pt_1>=23 * trg_wgt_single_mu22)",
                "trgweight",
            )
        else:
            trgweight = (
                "((pt_1>=25&&pt_1<=28) * trg_wgt_single_mu24)+(pt_1>28*trg_wgt_single_mu27)",
                "trgweight",
            )
    elif channel == "ett":
        # tauidweight = (
        #     "((q_1*q_2>0.5)*((gen_match_3==5)*((id_tau_vsJet_Medium_3>0.5)*id_wgt_tau_vsJet_Medium_3) + (gen_match_3!=5))*((gen_match_2==5)*((id_tau_vsJet_Tight_2>0.5)*id_wgt_tau_vsJet_Tight_2+(id_tau_vsJet_Tight_2<0.5&&id_tau_vsJet_VVVLoose_2>0.5)*id_wgt_tau_vsJet_VVVLoose_2) + (gen_match_2!=5))+((q_1*q_2<0.5)*((gen_match_3==5)*((id_tau_vsJet_Tight_3>0.5)*id_wgt_tau_vsJet_Tight_3+(id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5)) * ((gen_match_2==5)*((id_tau_vsJet_Medium_2>0.5)*id_wgt_tau_vsJet_Medium_2) + (gen_match_2!=5))))",
        #     "taubyIsoIdWeight",
        # )
        tauidweight = (
            "((q_1*q_2>0.5)*((gen_match_3==5)*((id_tau_vsJet_Tight_3>0.5)*id_wgt_tau_vsJet_Tight_3) + (gen_match_3!=5))*((gen_match_2==5)*((id_tau_vsJet_Tight_2>0.5)*id_wgt_tau_vsJet_Tight_2+(id_tau_vsJet_Tight_2<0.5&&id_tau_vsJet_VVVLoose_2>0.5)*id_wgt_tau_vsJet_VVVLoose_2) + (gen_match_2!=5))+((q_1*q_2<0.5)*((gen_match_3==5)*((id_tau_vsJet_Tight_3>0.5)*id_wgt_tau_vsJet_Tight_3+(id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5)) * ((gen_match_2==5)*((id_tau_vsJet_Tight_2>0.5)*id_wgt_tau_vsJet_Tight_2) + (gen_match_2!=5))))",
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

        isoweight = ("(iso_wgt_ele_1*(iso_1<0.15)+1.*(iso_1>0.15))", "isoweight")
        idweight = ("id_wgt_ele_wp90nonIso_1", "idweight")
        if "2016" in era:
            trgweight = ("pt_1>26 * trg_wgt_single_ele25", "trgweight")
        elif "2017" in era:
            trgweight = ("trg_wgt_single_ele27orele32orele35", "trgweight")
        elif "2018" in era: 
            trgweight = ("trg_wgt_single_ele32orele35", "trgweight")
    elif channel == "mtt":
        # tauidweight = (
        #     "((q_1*q_2>0.5)*((gen_match_3==5)*((id_tau_vsJet_Medium_3>0.5)*id_wgt_tau_vsJet_Medium_3) + (gen_match_3!=5))*((gen_match_2==5)*((id_tau_vsJet_Tight_2>0.5)*id_wgt_tau_vsJet_Tight_2+(id_tau_vsJet_Tight_2<0.5&&id_tau_vsJet_VVVLoose_2>0.5)*id_wgt_tau_vsJet_VVVLoose_2) + (gen_match_2!=5))+((q_1*q_2<0.5)*((gen_match_3==5)*((id_tau_vsJet_Tight_3>0.5)*id_wgt_tau_vsJet_Tight_3+(id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5)) * ((gen_match_2==5)*((id_tau_vsJet_Medium_2>0.5)*id_wgt_tau_vsJet_Medium_2) + (gen_match_2!=5))))",
        #     "taubyIsoIdWeight",
        # )
        tauidweight = (
            "((q_1*q_2>0.5)*((gen_match_3==5)*((id_tau_vsJet_Tight_3>0.5)*id_wgt_tau_vsJet_Tight_3) + (gen_match_3!=5))*((gen_match_2==5)*((id_tau_vsJet_Tight_2>0.5)*id_wgt_tau_vsJet_Tight_2+(id_tau_vsJet_Tight_2<0.5&&id_tau_vsJet_VVVLoose_2>0.5)*id_wgt_tau_vsJet_VVVLoose_2) + (gen_match_2!=5))+((q_1*q_2<0.5)*((gen_match_3==5)*((id_tau_vsJet_Tight_3>0.5)*id_wgt_tau_vsJet_Tight_3+(id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)*id_wgt_tau_vsJet_VVVLoose_3) + (gen_match_3!=5)) * ((gen_match_2==5)*((id_tau_vsJet_Tight_2>0.5)*id_wgt_tau_vsJet_Tight_2) + (gen_match_2!=5))))",
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

        isoweight = ("(iso_wgt_mu_1*(iso_1<0.15)+1.*(iso_1>0.15))", "isoweight")
        idweight = ("id_wgt_mu_1", "idweight")
        if "2016" in era:
            trgweight = ("trg_wgt_single_mu22", "trgweight")
        elif era in ["2017", "2018"]:
            trgweight = ("(trg_wgt_single_mu27*(pt_1>28))+(trg_wgt_single_mu24*(pt_1>25&&pt_1<=28))", "trgweight")
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


def WWZ_process_selection(channel, era):
    WWZ_process_weights = MC_base_process_selection(channel, era).weights
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


def WZZ_process_selection(channel, era):
    WZZ_process_weights = MC_base_process_selection(channel, era).weights
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
                ("1./(137000+4554000)", "numberGeneratedEventsWeight"),
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


def ZZZ_process_selection(channel, era):
    ZZZ_process_weights = MC_base_process_selection(channel, era).weights
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

#collection of ZZZ,WZZ,WWZ,WWW processes. To ensure every event has the same weight as if the process selection for the four processes were seperated, the numberofgeneratedeventsweight has to be the same. This is ensured by hard coding the crosssection (from datasets.yaml in the sample database repo). The condition has the queue ZZZ,WZZ,WWZ,WWW
def VVV_process_selection(channel, era):
    VVV_process_weights = MC_base_process_selection(channel, era).weights
    if era == "2016preVFP":
        VVV_process_weights.extend(
            [
                ("(crossSectionPerEventWeight<0.01477&&crossSectionPerEventWeight>0.01475)*1./(81000+5302000)+(crossSectionPerEventWeight<0.05710&&crossSectionPerEventWeight>0.05708)*1./(160000+5394000)+(crossSectionPerEventWeight<0.1708&&crossSectionPerEventWeight>0.1706)*1./(81000+5072000)+(crossSectionPerEventWeight<0.2159&&crossSectionPerEventWeight>0.2157)*1./(71000+5190000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2016postVFP":
        VVV_process_weights.extend(
            [
                ("(crossSectionPerEventWeight<0.01477&&crossSectionPerEventWeight>0.01475)*1./(72000+4534000)+(crossSectionPerEventWeight<0.05710&&crossSectionPerEventWeight>0.05708)*1./(137000+4554000)+(crossSectionPerEventWeight<0.1708&&crossSectionPerEventWeight>0.1706)*1./(67000+4595000)+(crossSectionPerEventWeight<0.2159&&crossSectionPerEventWeight>0.2157)*1./(69000+4159000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2017":
        VVV_process_weights.extend(
            [
                ("(crossSectionPerEventWeight<0.01477&&crossSectionPerEventWeight>0.01475)*1./(178000+9524000)+(crossSectionPerEventWeight<0.05710&&crossSectionPerEventWeight>0.05708)*1./(298000+9898000)+(crossSectionPerEventWeight<0.1708&&crossSectionPerEventWeight>0.1706)*1./(178000+9938400)+(crossSectionPerEventWeight<0.2159&&crossSectionPerEventWeight>0.2157)*1./(171000+9854000)", "numberGeneratedEventsWeight"),
                ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
                (
                    "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                    "generator_weight",
                ),
            ]
        )
    elif era == "2018":
        VVV_process_weights.extend(
            [
                ("(crossSectionPerEventWeight<0.01477&&crossSectionPerEventWeight>0.01475)*1./(250000+9889000)+(crossSectionPerEventWeight<0.05710&&crossSectionPerEventWeight>0.05708)*1./(300000+9994000)+(crossSectionPerEventWeight<0.1708&&crossSectionPerEventWeight>0.1706)*1./(248000+9961999)+(crossSectionPerEventWeight<0.2159&&crossSectionPerEventWeight>0.2157)*1./(240000+9894000)", "numberGeneratedEventsWeight"),
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
def H_process_selection(channel, era):
    H_process_weights = MC_base_process_selection(channel, era).weights
    H_process_weights.extend(
        [
            ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
            ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            (
                "1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)",
                "generator_weight",
            ),
        ]
    )
    return Selection(name="H", weights=H_process_weights)