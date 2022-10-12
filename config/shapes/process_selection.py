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


def MC_base_process_selection(channel, era):
    if channel == "emt":
        isoweight = ("iso_wgt_mu_2", "isoweight")
        idweight = ("id_wgt_ele_wp90nonIso_1 * id_wgt_mu_2", "idweight")
        tauidweight = (
            "((gen_match_3==5)*id_wgt_tau_vsJet_VTight_3 + (gen_match_3!=5))",
            "taubyIsoIdWeight",
        )
        vsmu_weight = ("id_wgt_tau_vsMu_Tight_3", "vsmuweight")
        vsele_weight = ("id_wgt_tau_vsEle_Tight_3", "vseleweight")
    MC_base_process_weights = [
        ("numberGeneratedEventsWeight", "numberGeneratedEventsWeight"),
        ("puweight", "puweight"),
        ("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
        lumi_weight(era),
        isoweight,
        idweight,
        tauidweight,
        vsmu_weight,
        vsele_weight,
        ("1./generator_weight*(genWeight>0)-1./generator_weight*(genWeight<0)", "generator_weight"),
    ]

    return Selection(name="MC_base", weights=MC_base_process_weights)
