from ntuple_processor.utils import Cut
from ntuple_processor.utils import Weight

from ntuple_processor.variations import ReplaceVariable
from ntuple_processor.variations import ReplaceCut
from ntuple_processor.variations import ReplaceWeight
from ntuple_processor.variations import RemoveCut
from ntuple_processor.variations import RemoveWeight
from ntuple_processor.variations import AddCut
from ntuple_processor.variations import AddWeight
from ntuple_processor.variations import SquareWeight
from ntuple_processor.variations import ReplaceCutAndAddWeight
from ntuple_processor.variations import ReplaceMultipleCuts
from ntuple_processor.variations import ReplaceMultipleCutsAndAddWeight
from ntuple_processor.variations import ReplaceVariableReplaceCutAndAddWeight
from ntuple_processor.variations import ChangeDatasetReplaceMultipleCutsAndAddWeight

##we have two fake rate versions here: incl. bveto and incl. ID in the fake rate measurement. you need to change only variations.py.

###incl. bveto
anti_iso_llt_tau = ReplaceCutAndAddWeight(
    "tau_anti_iso",
    "tau_iso",
    Cut("id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
    Weight("tau_fakerate_Era", "fake_factor"),
)
anti_isoid_mu_1 = ReplaceMultipleCutsAndAddWeight(
    "mu1_anti_isoid",
    ["id_iso_cut_1"],
    [
        Cut(
            "(iso_1>0.15 || muon_is_mediumid_1<0.5) && pt_1<25",
            "mu_1_anti_isoid",
        )
    ],
    Weight("lep_1_fakerate_Era", "fake_factor"),
)
anti_isoid_mu_2 = ReplaceMultipleCutsAndAddWeight(
    "mu2_anti_isoid",
    ["id_iso_cut_2"],
    [
        Cut(
            "(iso_2>0.15 || muon_is_mediumid_2<0.5) && pt_2<25",
            "mu_2_anti_isoid",
        )
    ],
    Weight("lep_2_fakerate_Era", "fake_factor"),
)
mmt_anti_isoid_mu_2 = ReplaceMultipleCutsAndAddWeight(
    "mu2_anti_isoid",
    ["id_iso_cut_2"],
    [
        Cut(
            "(iso_2>0.15 || muon_is_mediumid_2<0.5)",
            "mmt_mu_2_anti_isoid",
        )
    ],
    Weight("lep_2_fakerate_Era", "fake_factor"),
)
anti_isoid_ele_1 = ReplaceMultipleCutsAndAddWeight(
    "ele1_anti_isoid",
    ["id_iso_cut_1"],
    [
        Cut(
            "(iso_1>0.15 || electron_is_nonisowp90_1<0.5) && pt_2>25",
            "ele_1_anti_isoid",
        )
    ],
    Weight("lep_1_fakerate_Era", "fake_factor"),
)
anti_isoid_ele_2 = ReplaceMultipleCutsAndAddWeight(
    "ele2_anti_isoid",
    ["id_iso_cut_2"],
    [
        Cut(
            "(iso_2>0.15 || electron_is_nonisowp90_2<0.5) && pt_1>25",
            "ele_2_anti_isoid",
        )
    ],
    Weight("lep_2_fakerate_Era", "fake_factor"),
)
anti_isoid_mu_1_tau = ReplaceMultipleCutsAndAddWeight(
    "mu1tau_anti_isoid",
    ["id_iso_cut_1", "tau_iso"],
    [
        Cut(
            "(iso_1>0.15 || muon_is_mediumid_1<0.5) && pt_1<25",
            "mu_1_anti_iso",
        ),
        Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
    ],
    Weight(
        "-tau_fakerate_Era*lep_1_fakerate_Era",
        "fake_factor",
    ),
)
anti_isoid_mu_2_tau = ReplaceMultipleCutsAndAddWeight(
    "mu2tau_anti_isoid",
    ["id_iso_cut_2", "tau_iso"],
    [
        Cut(
            "(iso_2>0.15 || muon_is_mediumid_2<0.5) && pt_2<25",
            "mu_2_anti_iso",
        ),
        Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
    ],
    Weight(
        "-tau_fakerate_Era*lep_2_fakerate_Era",
        "fake_factor",
    ),
)
mmt_anti_isoid_mu_2_tau = ReplaceMultipleCutsAndAddWeight(
    "mu2tau_anti_isoid",
    ["id_iso_cut_2", "tau_iso"],
    [
        Cut(
            "(iso_2>0.15|| muon_is_mediumid_2<0.5)",
            "mu_2_anti_iso",
        ),
        Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
    ],
    Weight(
        "-tau_fakerate_Era*lep_2_fakerate_Era",
        "fake_factor",
    ),
)
anti_isoid_ele_1_tau = ReplaceMultipleCutsAndAddWeight(
    "ele1tau_anti_isoid",
    ["id_iso_cut_1", "tau_iso"],
    [
        Cut(
            "(iso_1>0.15 || electron_is_nonisowp90_1<0.5) && pt_2>25",
            "ele_1_tau_anti_isoid",
        ),
        Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
    ],
    Weight(
        "-tau_fakerate_Era*lep_1_fakerate_Era",
        "fake_factor",
    ),
)
anti_isoid_ele_2_tau = ReplaceMultipleCutsAndAddWeight(
    "ele2tau_anti_isoid",
    ["id_iso_cut_2", "tau_iso"],
    [
        Cut(
            "(iso_2>0.15 || electron_is_nonisowp90_2<0.5) && pt_1>25",
            "ele_2_anti_iso",
        ),
        Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
    ],
    Weight(
        "-tau_fakerate_Era*lep_2_fakerate_Era",
        "fake_factor",
    ),
)
anti_iso_ltt = ReplaceCutAndAddWeight(
    "tau_anti_iso",
    "tau_iso",
    Cut(
        "((q_1*q_2>0) && id_tau_vsJet_VTight_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_VTight_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_VTight_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_VTight_2>0.5)",
        "tau_anti_iso",
    ),
    Weight("tau_fakerate_Era", "fake_factor"),
)
# Pileup reweighting
pileup_reweighting = [
    ReplaceVariable("CMS_PileUpUp", "PileUpUp"),
    ReplaceVariable("CMS_PileUpDown", "PileUpDown"),
]


# Energy scales.
# Previously defined with 2017 in name.
tau_es_3prong = [
    ReplaceVariable("CMS_scale_t_3prong_EraUp", "tauEs3prong0pizeroUp"),
    ReplaceVariable("CMS_scale_t_3prong_EraDown", "tauEs3prong0pizeroDown"),
]

tau_es_3prong1pizero = [
    ReplaceVariable("CMS_scale_t_3prong1pizero_EraUp", "tauEs3prong1pizeroUp"),
    ReplaceVariable("CMS_scale_t_3prong1pizero_EraDown", "tauEs3prong1pizeroDown"),
]

tau_es_1prong = [
    ReplaceVariable("CMS_scale_t_1prong_EraUp", "tauEs1prong0pizeroUp"),
    ReplaceVariable("CMS_scale_t_1prong_EraDown", "tauEs1prong0pizeroDown"),
]

tau_es_1prong1pizero = [
    ReplaceVariable("CMS_scale_t_1prong1pizero_EraUp", "tauEs1prong1pizeroUp"),
    ReplaceVariable("CMS_scale_t_1prong1pizero_EraDown", "tauEs1prong1pizeroDown"),
]
# Electron energy scale
# TODO add in ntuples ?
# ele_es = [
#     ReplaceVariable("CMS_scale_eUp", "eleScaleUp"),
#     ReplaceVariable("CMS_scale_eDown", "eleScaleDown"),
# ]

# ele_res = [
#     ReplaceVariable("CMS_res_eUp", "eleSmearUp"),
#     ReplaceVariable("CMS_res_eDown", "eleSmearDown"),
# ]

# Jet energy scale split by sources.
jet_es = [
    ReplaceVariable("CMS_scale_j_AbsoluteUp", "jesUncAbsoluteUp"),
    ReplaceVariable("CMS_scale_j_AbsoluteDown", "jesUncAbsoluteDown"),
    ReplaceVariable("CMS_scale_j_Absolute_EraUp", "jesUncAbsoluteYearUp"),
    ReplaceVariable("CMS_scale_j_Absolute_EraDown", "jesUncAbsoluteYearDown"),
    ReplaceVariable("CMS_scale_j_BBEC1Up", "jesUncBBEC1Up"),
    ReplaceVariable("CMS_scale_j_BBEC1Down", "jesUncBBEC1Down"),
    ReplaceVariable("CMS_scale_j_BBEC1_EraUp", "jesUncBBEC1YearUp"),
    ReplaceVariable("CMS_scale_j_BBEC1_EraDown", "jesUncBBEC1YearDown"),
    ReplaceVariable("CMS_scale_j_EC2Up", "jesUncEC2Up"),
    ReplaceVariable("CMS_scale_j_EC2Down", "jesUncEC2Down"),
    ReplaceVariable("CMS_scale_j_EC2_EraUp", "jesUncEC2YearUp"),
    ReplaceVariable("CMS_scale_j_EC2_EraDown", "jesUncEC2YearDown"),
    ReplaceVariable("CMS_scale_j_HFUp", "jesUncHFUp"),
    ReplaceVariable("CMS_scale_j_HFDown", "jesUncHFDown"),
    ReplaceVariable("CMS_scale_j_HF_EraUp", "jesUncHFYearUp"),
    ReplaceVariable("CMS_scale_j_HF_EraDown", "jesUncHFYearDown"),
    ReplaceVariable("CMS_scale_j_FlavorQCDUp", "jesUncFlavorQCDUp"),
    ReplaceVariable("CMS_scale_j_FlavorQCDDown", "jesUncFlavorQCDDown"),
    ReplaceVariable("CMS_scale_j_RelativeBalUp", "jesUncRelativeBalUp"),
    ReplaceVariable("CMS_scale_j_RelativeBalDown", "jesUncRelativeBalDown"),
    ReplaceVariable("CMS_scale_j_RelativeSample_EraUp", "jesUncRelativeSampleYearUp"),
    ReplaceVariable(
        "CMS_scale_j_RelativeSample_EraDown", "jesUncRelativeSampleYearDown"
    ),
    ReplaceVariable("CMS_res_j_EraUp", "jerUncUp"),
    ReplaceVariable("CMS_res_j_EraDown", "jerUncDown"),
]


# MET variations.
met_unclustered = [
    ReplaceVariable("CMS_scale_met_unclustered_EraUp", "metUnclusteredEnUp"),
    ReplaceVariable("CMS_scale_met_unclustered_EraDown", "metUnclusteredEnDown"),
]

# Recoil correction uncertainties
recoil_resolution = [
    ReplaceVariable("CMS_htt_boson_res_met_EraUp", "metRecoilResolutionUp"),
    ReplaceVariable("CMS_htt_boson_res_met_EraDown", "metRecoilResolutionDown"),
]

recoil_response = [
    ReplaceVariable("CMS_htt_boson_scale_met_EraUp", "metRecoilResponseUp"),
    ReplaceVariable("CMS_htt_boson_scale_met_EraDown", "metRecoilResponseDown"),
]
# Eta binned uncertainty
ele_fake_es_1prong = [
    ReplaceVariable("CMS_ZLShape_et_1prong_barrel_EraUp", "tauEleFakeEs1prongBarrelUp"),
    ReplaceVariable(
        "CMS_ZLShape_et_1prong_barrel_EraDown", "tauEleFakeEs1prongBarrelDown"
    ),
    ReplaceVariable("CMS_ZLShape_et_1prong_endcap_EraUp", "tauEleFakeEs1prongEndcapUp"),
    ReplaceVariable(
        "CMS_ZLShape_et_1prong_endcap_EraDown", "tauEleFakeEs1prongEndcapDown"
    ),
]

ele_fake_es_1prong1pizero = [
    ReplaceVariable(
        "CMS_ZLShape_et_1prong1pizero_barrel_EraUp", "tauEleFakeEs1prong1pizeroBarrelUp"
    ),
    ReplaceVariable(
        "CMS_ZLShape_et_1prong1pizero_barrel_EraDown",
        "tauEleFakeEs1prong1pizeroBarrelDown",
    ),
    ReplaceVariable(
        "CMS_ZLShape_et_1prong1pizero_endcap_EraUp", "tauEleFakeEs1prong1pizeroEndcapUp"
    ),
    ReplaceVariable(
        "CMS_ZLShape_et_1prong1pizero_endcap_EraDown",
        "tauEleFakeEs1prong1pizeroEndcapDown",
    ),
]

ele_fake_es = ele_fake_es_1prong + ele_fake_es_1prong1pizero

mu_fake_es_inc = [
    ReplaceVariable("CMS_ZLShape_mt_EraUp", "tauMuFakeEsUp"),
    ReplaceVariable("CMS_ZLShape_mt_EraDown", "tauMuFakeEsDown"),
]

# Efficiency corrections.
# Tau ID efficiency.

# TODO add high pt tau ID efficiency
tau_id_eff_lt = [
    ReplaceVariable("CMS_eff_t_30-35_EraUp", "vsJetTau30to35Up"),
    ReplaceVariable("CMS_eff_t_30-35_EraDown", "vsJetTau30to35Down"),
    ReplaceVariable("CMS_eff_t_35-40_EraUp", "vsJetTau35to40Up"),
    ReplaceVariable("CMS_eff_t_35-40_EraDown", "vsJetTau35to40Down"),
    ReplaceVariable("CMS_eff_t_40-500_EraUp", "vsJetTau40to500Up"),
    ReplaceVariable("CMS_eff_t_40-500_EraDown", "vsJetTau40to500Down"),
    ReplaceVariable("CMS_eff_t_500-1000_EraUp", "vsJetTau500to1000Up"),
    ReplaceVariable("CMS_eff_t_500-1000_EraDown", "vsJetTau500to1000Down"),
]
tau_id_eff_tt = [
    ReplaceVariable("CMS_eff_t_dm0_EraUp", "vsJetTauDM0Up"),
    ReplaceVariable("CMS_eff_t_dm0_EraDown", "vsJetTauDM0Down"),
    ReplaceVariable("CMS_eff_t_dm1_EraUp", "vsJetTauDM1Up"),
    ReplaceVariable("CMS_eff_t_dm1_EraDown", "vsJetTauDM1Down"),
    ReplaceVariable("CMS_eff_t_dm10_EraUp", "vsJetTauDM10Up"),
    ReplaceVariable("CMS_eff_t_dm10_EraDown", "vsJetTauDM10Down"),
    ReplaceVariable("CMS_eff_t_dm11_EraUp", "vsJetTauDM11Up"),
    ReplaceVariable("CMS_eff_t_dm11_EraDown", "vsJetTauDM11Down"),
]
# Jet to tau fake rate.
jet_to_tau_fake = [
    AddWeight(
        "CMS_htt_fake_j_EraUp",
        Weight("max(1.0-pt_2*0.002, 0.6)", "jetToTauFake_weight"),
    ),
    AddWeight(
        "CMS_htt_fake_j_EraDown",
        Weight("min(1.0+pt_2*0.002, 1.4)", "jetToTauFake_weight"),
    ),
]

vsE_fake_rate = [
    ReplaceVariable("CMS_fake_e_BA_EraUp", "vsEleBarrelUp"),
    ReplaceVariable("CMS_fake_e_BA_EraDown", "vsEleBarrelDown"),
    ReplaceVariable("CMS_fake_e_EC_EraUp", "vsEleEndcapUp"),
    ReplaceVariable("CMS_fake_e_EC_EraDown", "vsEleEndcapDown"),
]

vsMu_fake_rate_up = [
    ReplaceVariable(f"CMS_fake_m_WH{region}_EraUp", f"vsMuWheel{region}Up")
    for region in ["1", "2", "3", "4", "5"]
]
vsMu_fake_rate_down = [
    ReplaceVariable(f"CMS_fake_m_WH{region}_EraDown", f"vsMuWheel{region}Down")
    for region in ["1", "2", "3", "4", "5"]
]

vsMu_fake_rate = vsMu_fake_rate_up + vsMu_fake_rate_down

# # Trigger efficiency uncertainties.
trigger_eff_mu = [
    ReplaceVariable("CMS_eff_trigger_mt_EraUp", "singleMuonTriggerSFUp"),
    ReplaceVariable("CMS_eff_trigger_mt_EraDown", "singleMuonTriggerSFDown"),
]
trigger_eff_e = [
    ReplaceVariable("CMS_eff_trigger_et_EraUp", "singleElectronTriggerSFUp"),
    ReplaceVariable("CMS_eff_trigger_et_EraDown", "singleElectronTriggerSFDown"),
]
prefiring = [
    ReplaceWeight(
        "CMS_prefiringUp",
        "prefiring_wgt",
        Weight("prefiring_wgt__prefiringUp", "prefiring_wgt"),
    ),
    ReplaceWeight(
        "CMS_prefiringDown",
        "prefiring_wgt",
        Weight("prefiring_wgt__prefiringDown", "prefiring_wgt"),
    ),
]

zpt = [
    SquareWeight("CMS_htt_dyShape_EraUp", "zPtReweightWeight"),
    RemoveWeight("CMS_htt_dyShape_EraDown", "zPtReweightWeight"),
]

top_pt = [
    SquareWeight("CMS_htt_ttbarShapeUp", "topPtReweightWeight"),
    RemoveWeight("CMS_htt_ttbarShapeDown", "topPtReweightWeight"),
]

# fake factor variations

anti_iso_llt_tau_var = [
    ReplaceCutAndAddWeight(
        "tau_anti_iso_{unc}_Era{shift}".format(unc=unc, shift=shift),
        "tau_iso",
        Cut("id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
        Weight(
            "tau_fakerate_{unc}_Era{shift}".format(unc=unc, shift=shift), "fake_factor"
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]

anti_isoid_mu_1_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu1_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_1"],
        [
            Cut(
                "(iso_1>0.15 || muon_is_mediumid_1<0.5) && pt_1<25",
                "mu_1_anti_isoid",
            )
        ],
        Weight(
            "lep_1_fakerate_{unc}_Era{shift}".format(unc=unc, shift=shift),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
anti_isoid_mu_2_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "(iso_2>0.15 || muon_is_mediumid_2<0.5) && pt_2<25",
                "mu_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_{unc}_Era{shift}".format(unc=unc, shift=shift),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
mmt_anti_isoid_mu_2_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "(iso_2>0.15 || muon_is_mediumid_2<0.5)",
                "mmt_mu_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_{unc}_Era{shift}".format(unc=unc, shift=shift),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
anti_isoid_ele_1_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele1_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_1"],
        [
            Cut(
                "(iso_1>0.15 || electron_is_nonisowp90_1<0.5) && pt_2>25",
                "ele_1_anti_isoid",
            )
        ],
        Weight(
            "lep_1_fakerate_{unc}_Era{shift}".format(unc=unc, shift=shift),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
anti_isoid_ele_2_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele2_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "(iso_2>0.15 || electron_is_nonisowp90_2<0.5) && pt_1>25",
                "ele_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_{unc}_Era{shift}".format(unc=unc, shift=shift),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
anti_isoid_mu_1_tau_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu1tau_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_1", "tau_iso"],
        [
            Cut(
                "(iso_1>0.15 || muon_is_mediumid_1<0.5) && pt_1<25",
                "mu_1_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_{unc}_Era{shift}*lep_1_fakerate_{unc}_Era{shift}".format(
                unc=unc, shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
anti_isoid_mu_2_tau_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2tau_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "(iso_2>0.15 || muon_is_mediumid_2<0.5) && pt_2<25",
                "mu_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_{unc}_Era{shift}*lep_2_fakerate_{unc}_Era{shift}".format(
                unc=unc, shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
mmt_anti_isoid_mu_2_tau_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2tau_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "(iso_2>0.15|| muon_is_mediumid_2<0.5)",
                "mu_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_{unc}_Era{shift}*lep_2_fakerate_{unc}_Era{shift}".format(
                unc=unc, shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
anti_isoid_ele_1_tau_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele1tau_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_1", "tau_iso"],
        [
            Cut(
                "(iso_1>0.15 || electron_is_nonisowp90_1<0.5) && pt_2>25",
                "ele_1_tau_anti_isoid",
            ),
            Cut(
                "(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_{unc}_Era{shift}*lep_1_fakerate_{unc}_Era{shift}".format(
                unc=unc, shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
anti_isoid_ele_2_tau_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele2tau_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "(iso_2>0.15 || electron_is_nonisowp90_2<0.5) && pt_1>25",
                "ele_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_{unc}_Era{shift}*lep_2_fakerate_{unc}_Era{shift}".format(
                unc=unc, shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
anti_iso_ltt_var = [
    ReplaceCutAndAddWeight(
        "tau_anti_iso_{unc}_Era{shift}".format(unc=unc, shift=shift),
        "tau_iso",
        Cut(
            "((q_1*q_2>0) && id_tau_vsJet_VTight_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_VTight_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_VTight_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_VTight_2>0.5)",
            "tau_anti_iso",
        ),
        Weight(
            "tau_fakerate_{unc}_Era{shift}".format(unc=unc, shift=shift), "fake_factor"
        ),
    )
    for shift in ["Up", "Down"]
    for unc in ["CMS_ff_syst", "CMS_ff_stat"]
]
## v_3
# anti_iso_llt_tau = ReplaceCutAndAddWeight(
#     "tau_anti_iso",
#     "tau_iso",
#     Cut("id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
#     Weight("tau_fakerate", "fake_factor"),
# )
# anti_isoid_mu_1 = ReplaceMultipleCutsAndAddWeight(
#     "mu1_anti_isoid",
#     ["id_iso_cut_1"],
#     [
#         Cut(
#             "(iso_1>0.15 && muon_is_mediumid_1>0.5) && pt_1<25",
#             "mu_1_anti_isoid",
#         )
#     ],
#     Weight("lep_1_fakerate", "fake_factor"),
# )
# anti_isoid_mu_2 = ReplaceMultipleCutsAndAddWeight(
#     "mu2_anti_isoid",
#     ["id_iso_cut_2"],
#     [
#         Cut(
#             "(iso_2>0.15 && muon_is_mediumid_2>0.5) && pt_2<25",
#             "mu_2_anti_isoid",
#         )
#     ],
#     Weight("lep_2_fakerate", "fake_factor"),
# )
# mmt_anti_isoid_mu_2 = ReplaceMultipleCutsAndAddWeight(
#     "mu2_anti_isoid",
#     ["id_iso_cut_2"],
#     [
#         Cut(
#             "(iso_2>0.15 && muon_is_mediumid_2>0.5)",
#             "mmt_mu_2_anti_isoid",
#         )
#     ],
#     Weight("lep_2_fakerate", "fake_factor"),
# )
# anti_isoid_ele_1 = ReplaceMultipleCutsAndAddWeight(
#     "ele1_anti_isoid",
#     ["id_iso_cut_1"],
#     [
#         Cut(
#             "(iso_1>0.15 && electron_is_nonisowp90_1>0.5) && pt_2>25",
#             "ele_1_anti_isoid",
#         )
#     ],
#     Weight("lep_1_fakerate", "fake_factor"),
# )
# anti_isoid_ele_2 = ReplaceMultipleCutsAndAddWeight(
#     "ele2_anti_isoid",
#     ["id_iso_cut_2"],
#     [
#         Cut(
#             "(iso_2>0.15 && electron_is_nonisowp90_2>0.5) && pt_1>25",
#             "ele_2_anti_isoid",
#         )
#     ],
#     Weight("lep_2_fakerate", "fake_factor"),
# )
# anti_isoid_mu_1_tau = ReplaceMultipleCutsAndAddWeight(
#     "mu1tau_anti_isoid",
#     ["id_iso_cut_1", "tau_iso"],
#     [
#         Cut(
#             "(iso_1>0.15 && muon_is_mediumid_1>0.5) && pt_1<25",
#             "mu_1_anti_iso",
#         ),
#         Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
#     ],
#     Weight(
#         "-tau_fakerate*lep_1_fakerate",
#         "fake_factor",
#     ),
# )
# anti_isoid_mu_2_tau = ReplaceMultipleCutsAndAddWeight(
#     "mu2tau_anti_isoid",
#     ["id_iso_cut_2", "tau_iso"],
#     [
#         Cut(
#             "(iso_2>0.15 && muon_is_mediumid_2>0.5) && pt_2<25",
#             "mu_2_anti_iso",
#         ),
#         Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
#     ],
#     Weight(
#         "-tau_fakerate*lep_2_fakerate",
#         "fake_factor",
#     ),
# )
# mmt_anti_isoid_mu_2_tau = ReplaceMultipleCutsAndAddWeight(
#     "mu2tau_anti_isoid",
#     ["id_iso_cut_2", "tau_iso"],
#     [
#         Cut(
#             "(iso_2>0.15 && muon_is_mediumid_2>0.5)",
#             "mu_2_anti_iso",
#         ),
#         Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
#     ],
#     Weight(
#         "-tau_fakerate*lep_2_fakerate",
#         "fake_factor",
#     ),
# )
# anti_isoid_ele_1_tau = ReplaceMultipleCutsAndAddWeight(
#     "ele1tau_anti_isoid",
#     ["id_iso_cut_1", "tau_iso"],
#     [
#         Cut(
#             "(iso_1>0.15 && electron_is_nonisowp90_1>0.5) && pt_2>25",
#             "ele_1_tau_anti_isoid",
#         ),
#         Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
#     ],
#     Weight(
#         "-tau_fakerate*lep_1_fakerate",
#         "fake_factor",
#     ),
# )
# anti_isoid_ele_2_tau = ReplaceMultipleCutsAndAddWeight(
#     "ele2tau_anti_isoid",
#     ["id_iso_cut_2", "tau_iso"],
#     [
#         Cut(
#             "(iso_2>0.15 && electron_is_nonisowp90_2>0.5) && pt_1>25",
#             "ele_2_anti_iso",
#         ),
#         Cut("(id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
#     ],
#     Weight(
#         "-tau_fakerate*lep_2_fakerate",
#         "fake_factor",
#     ),
# )
# anti_iso_ltt = ReplaceCutAndAddWeight(
#     "tau_anti_iso",
#     "tau_iso",
#     Cut(
#         "((q_1*q_2>0) && id_tau_vsJet_VTight_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_VTight_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_VTight_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_VTight_2>0.5)",
#         "tau_anti_iso",
#     ),
#     Weight("tau_fakerate", "fake_factor"),
# )
