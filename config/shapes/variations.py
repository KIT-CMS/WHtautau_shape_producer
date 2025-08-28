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
print("llt anti iso:", "tau_fakerate_Era*tau_closure_correction_njets_Era")
print("ltt anti iso:", "tau_fakerate_Era*tau_closure_correction_njets_Era")
print("llt:", "lep_closure_correction_Era")
print("unc beachtet")
# anti_iso_ltt = ReplaceCutAndAddWeight(
#     "tau_anti_iso",
#     "tau_iso",
#     Cut(
#         "(((q_1*q_2>0) && id_tau_vsJet_VTight_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_VTight_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_Medium_2>0.5))",
#         "tau_anti_iso",
#     ),
#     Weight("tau_fakerate_Era", "fake_factor"),
# )
anti_iso_llt_tau = ReplaceCutAndAddWeight(
    "tau_anti_iso",
    "tau_iso",
    Cut("id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
    Weight(
        "tau_fakerate_Era",
        "fake_factor",
    ),
)
anti_isoid_mu_2 = ReplaceMultipleCutsAndAddWeight(
    "mu2_anti_isoid",
    ["id_iso_cut_2"],
    [
        Cut(
            "((iso_2<0.5 && iso_2>0.15) || muon_is_mediumid_2<0.5)",
            "mu_2_anti_isoid",
        )
    ],
    Weight(
        "lep_2_fakerate_Era",
        "fake_factor",
    ),
)
anti_isoid_ele_2 = ReplaceMultipleCutsAndAddWeight(
    "ele2_anti_isoid",
    ["id_iso_cut_2"],
    [
        Cut(
            "((iso_2<0.5 && iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
            "ele_2_anti_isoid",
        )
    ],
    Weight(
        "lep_2_fakerate_Era",
        "fake_factor",
    ),
)
anti_isoid_mu_2_tau = ReplaceMultipleCutsAndAddWeight(
    "mu2tau_anti_isoid",
    ["id_iso_cut_2", "tau_iso"],
    [
        Cut(
            "((iso_2<0.5 && iso_2>0.15) || muon_is_mediumid_2<0.5)",
            "mu_2_anti_iso",
        ),
        Cut("(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
    ],
    Weight(
        "-tau_fakerate_Era*lep_2_fakerate_Era",
        "fake_factor",
    ),
)
anti_isoid_ele_2_tau = ReplaceMultipleCutsAndAddWeight(
    "ele2tau_anti_isoid",
    ["id_iso_cut_2", "tau_iso"],
    [
        Cut(
            "(iso_2<0.5 && iso_2>0.15) || electron_is_nonisowp90_2<0.5",
            "ele_2_anti_iso",
        ),
        Cut("(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
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
        "(((q_1*q_2>0) && id_tau_vsJet_Medium_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_Medium_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_Medium_2>0.5))",
        "tau_anti_iso",
    ),
    Weight(
        "tau_fakerate_Era",
        "fake_factor",
    ),
)

# FF uncertainties
anti_iso_llt_tau_var = [
    ReplaceCutAndAddWeight(
        "tau_anti_iso_{unc}_Era{shift}".format(unc=unc, shift=shift),
        "tau_iso",
        Cut("id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
        Weight(
            "tau_fakerate_{unc}_Era{shift}".format(unc=unc, shift=shift),
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
            "(((q_1*q_2>0) && id_tau_vsJet_Medium_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_Medium_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_Medium_2>0.5))",
            "tau_anti_iso",
        ),
        Weight(
            "tau_fakerate_{unc}_Era{shift}".format(unc=unc, shift=shift),
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
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mu_2_anti_isoid",
            )
        ],
        Weight(
            "(((pt_2<60)*lep_2_fakerate_{unc}_Era{shift})+((pt_2<60)*lep_2_fakerate_{unc}_Era{shift}*1.5))".format(
                unc=unc, shift=shift
            ),
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
                "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
                "ele_2_anti_isoid",
            )
        ],
        Weight(
            "(((pt_2<60)*lep_2_fakerate_{unc}_Era{shift})+((pt_2<60)*lep_2_fakerate_{unc}_Era{shift}*1.5))".format(
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
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mu_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
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
anti_isoid_ele_2_tau_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele2tau_anti_isoid_{unc}_Era{shift}".format(unc=unc, shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
                "ele_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
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

# ff shape det->sig uncertainty
anti_iso_ltt_var_syst_det_up = ReplaceCutAndAddWeight(
    "tau_anti_iso_CMS_ff_systdet_EraUp",
    "tau_iso",
    Cut(
        "(((q_1*q_2>0) && id_tau_vsJet_Medium_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_Medium_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_Medium_2>0.5))",
        "tau_anti_iso",
    ),
    Weight(
        "tau_fakerate_Era*1.25",
        "fake_factor",
    ),
)
anti_iso_ltt_var_syst_det_down = ReplaceCutAndAddWeight(
    "tau_anti_iso_CMS_ff_systdet_EraDown",
    "tau_iso",
    Cut(
        "(((q_1*q_2>0) && id_tau_vsJet_Medium_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_Medium_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_Medium_2>0.5))",
        "tau_anti_iso",
    ),
    Weight(
        "tau_fakerate_Era*0.75",
        "fake_factor",
    ),
)
anti_iso_llt_var_syst_det_up = ReplaceCutAndAddWeight(
    "tau_anti_iso_CMS_ff_systdet_EraUp",
    "tau_iso",
    Cut("id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
    Weight(
        "tau_fakerate_Era*1.25",
        "fake_factor",
    ),
)
anti_iso_llt_var_syst_det_down = ReplaceCutAndAddWeight(
    "tau_anti_iso_CMS_ff_systdet_EraDown",
    "tau_iso",
    Cut("id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
    Weight(
        "tau_fakerate_Era*0.75",
        "fake_factor",
    ),
)
anti_isoid_mu_2_var_syst_det_up = ReplaceMultipleCutsAndAddWeight(
    "mu2_anti_isoid_CMS_ff_systdet_EraUp",
    ["id_iso_cut_2"],
    [
        Cut(
            "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
            "mu_2_anti_isoid",
        )
    ],
    Weight(
        "lep_2_fakerate_Era*1.25",
        "fake_factor",
    ),
)
anti_isoid_mu_2_var_syst_det_down = ReplaceMultipleCutsAndAddWeight(
    "mu2_anti_isoid_CMS_ff_systdet_EraDown",
    ["id_iso_cut_2"],
    [
        Cut(
            "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
            "mu_2_anti_isoid",
        )
    ],
    Weight(
        "lep_2_fakerate_Era*0.75",
        "fake_factor",
    ),
)

anti_isoid_ele_2_var_syst_det_up = ReplaceMultipleCutsAndAddWeight(
    "ele2_anti_isoid_CMS_ff_systdet_EraUp",
    ["id_iso_cut_2"],
    [
        Cut(
            "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
            "ele_2_anti_isoid",
        )
    ],
    Weight(
        "lep_2_fakerate_Era*1.25",
        "fake_factor",
    ),
)
anti_isoid_ele_2_var_syst_det_down = ReplaceMultipleCutsAndAddWeight(
    "ele2_anti_isoid_CMS_ff_systdet_EraDown",
    ["id_iso_cut_2"],
    [
        Cut(
            "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
            "ele_2_anti_isoid",
        )
    ],
    Weight(
        "lep_2_fakerate_Era*0.75",
        "fake_factor",
    ),
)
anti_isoid_mu_2_tau_var_syst_det_up = ReplaceMultipleCutsAndAddWeight(
    "mu2tau_anti_isoid_CMS_ff_systdet_EraUp",
    ["id_iso_cut_2", "tau_iso"],
    [
        Cut(
            "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
            "mu_2_anti_iso",
        ),
        Cut(
            "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
            "tau_anti_iso",
        ),
    ],
    Weight(
        "-tau_fakerate_Era*lep_2_fakerate_Era*1.25",
        "fake_factor",
    ),
)
anti_isoid_mu_2_tau_var_syst_det_down = ReplaceMultipleCutsAndAddWeight(
    "mu2tau_anti_isoid_CMS_ff_systdet_EraDown",
    ["id_iso_cut_2", "tau_iso"],
    [
        Cut(
            "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
            "mu_2_anti_iso",
        ),
        Cut(
            "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
            "tau_anti_iso",
        ),
    ],
    Weight(
        "-tau_fakerate_Era*lep_2_fakerate_Era*0.75",
        "fake_factor",
    ),
)
anti_isoid_ele_2_tau_var_syst_det_up = ReplaceMultipleCutsAndAddWeight(
    "ele2tau_anti_isoid_CMS_ff_systdet_EraUp",
    ["id_iso_cut_2", "tau_iso"],
    [
        Cut(
            "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
            "ele_2_anti_iso",
        ),
        Cut(
            "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
            "tau_anti_iso",
        ),
    ],
    Weight(
        "-tau_fakerate_Era*lep_2_fakerate_Era*1.25",
        "fake_factor",
    ),
)
anti_isoid_ele_2_tau_var_syst_det_down = ReplaceMultipleCutsAndAddWeight(
    "ele2tau_anti_isoid_CMS_ff_systdet_EraDown",
    ["id_iso_cut_2", "tau_iso"],
    [
        Cut(
            "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
            "ele_2_anti_iso",
        ),
        Cut(
            "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
            "tau_anti_iso",
        ),
    ],
    Weight(
        "-tau_fakerate_Era*lep_2_fakerate_Era*0.75",
        "fake_factor",
    ),
)
# FF met uncertainty, lep only variations are only placeholders for the workflow. They have no additional weight
anti_iso_llt_tau_met_var = [
    ReplaceCutAndAddWeight(
        "tau_anti_iso_CMS_ff_systmetllt_Era{shift}".format(shift=shift),
        "tau_iso",
        Cut("id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
        Weight(
            "tau_fakerate_Era*fakerate_CMS_ff_syst_met_Era{shift}".format(shift=shift),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_iso_ltt_tau_met_var = [
    ReplaceCutAndAddWeight(
        "tau_anti_iso_CMS_ff_systmetltt_Era{shift}".format(shift=shift),
        "tau_iso",
        Cut(
            "(((q_1*q_2>0) && id_tau_vsJet_Medium_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_Medium_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_Medium_2>0.5))",
            "tau_anti_iso",
        ),
        Weight(
            "tau_fakerate_Era*fakerate_CMS_ff_syst_met_Era{shift}".format(shift=shift),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_mu_2_met_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2_anti_isoid_CMS_ff_systmetllt_Era{shift}".format(shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mu_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_Era",
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_ele_2_met_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele2_anti_isoid_CMS_ff_systmetllt_Era{shift}".format(shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
                "ele_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_Era",
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_mu_2_tau_met_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2tau_anti_isoid_CMS_ff_systmetllt_Era{shift}".format(shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mu_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_Era*lep_2_fakerate_Era*fakerate_CMS_ff_syst_met_Era{shift}".format(
                shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_ele_2_tau_met_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele2tau_anti_isoid_CMS_ff_systmetllt_Era{shift}".format(shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
                "ele_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_Era*lep_2_fakerate_Era*fakerate_CMS_ff_syst_met_Era{shift}".format(
                shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
# FF pt_1 uncertainty, lep only variations are only placeholders for the workflow. They have no additional weight
# FF pt_1 uncertainty, lep only variations are only placeholders for the workflow. They have no additional weight
anti_iso_llt_tau_pt_1_var = [
    ReplaceCutAndAddWeight(
        "tau_anti_iso_CMS_ff_systpt1llt_Era{shift}".format(shift=shift),
        "tau_iso",
        Cut("id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
        Weight(
            "tau_fakerate_Era*fakerate_CMS_ff_syst_pt1_Era{shift}".format(shift=shift),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_iso_ltt_tau_pt_1_var = [
    ReplaceCutAndAddWeight(
        "tau_anti_iso_CMS_ff_systpt1ltt_Era{shift}".format(shift=shift),
        "tau_iso",
        Cut(
            "(((q_1*q_2>0) && id_tau_vsJet_Medium_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_Medium_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_Medium_2>0.5))",
            "tau_anti_iso",
        ),
        Weight(
            "tau_fakerate_Era*fakerate_CMS_ff_syst_pt1_Era{shift}".format(shift=shift),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_mu_2_pt_1_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2_anti_isoid_CMS_ff_systpt1llt_Era{shift}".format(shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mu_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_Era",
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_ele_2_pt_1_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele2_anti_isoid_CMS_ff_systpt1llt_Era{shift}".format(shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
                "ele_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_Era",
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_mu_2_tau_pt_1_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2tau_anti_isoid_CMS_ff_systpt1llt_Era{shift}".format(shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mu_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_Era*lep_2_fakerate_Era*fakerate_CMS_ff_syst_pt1_Era{shift}".format(
                shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_ele_2_tau_pt_1_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele2tau_anti_isoid_CMS_ff_systpt1llt_Era{shift}".format(shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
                "ele_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_Era*lep_2_fakerate_Era*fakerate_CMS_ff_syst_pt1_Era{shift}".format(
                shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
# FF NN uncertainty, lep only variations are only placeholders for the workflow. They have no additional weight
anti_iso_llt_tau_nn_var = [
    ReplaceCutAndAddWeight(
        "tau_anti_iso_CMS_ff_nnscore_Era{shift}".format(shift=shift),
        "tau_iso",
        Cut("id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
        Weight(
            "tau_fakerate_Era*fakerate_CMS_ff_syst_nnscore_Era{shift}".format(
                shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_iso_ltt_tau_nn_var = [
    ReplaceCutAndAddWeight(
        "tau_anti_iso_CMS_ff_nnscore_Era{shift}".format(shift=shift),
        "tau_iso",
        Cut(
            "(((q_1*q_2>0) && id_tau_vsJet_Medium_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_Medium_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_Medium_2>0.5))",
            "tau_anti_iso",
        ),
        Weight(
            "tau_fakerate_Era*fakerate_CMS_ff_syst_nnscore_Era{shift}".format(
                shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_mu_2_nn_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2_anti_isoid_CMS_ff_nnscore_Era{shift}".format(shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mu_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_Era",
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
mmt_anti_isoid_mu_2_nn_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2_anti_isoid_CMS_ff_nnscore_Era{shift}".format(shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mmt_mu_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_Era",
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_ele_2_nn_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele2_anti_isoid_CMS_ff_nnscore_Era{shift}".format(shift=shift),
        ["id_iso_cut_2"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
                "ele_2_anti_isoid",
            )
        ],
        Weight(
            "lep_2_fakerate_Era",
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_mu_2_tau_nn_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2tau_anti_isoid_CMS_ff_nnscore_Era{shift}".format(shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mu_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_Era*lep_2_fakerate_Era*fakerate_CMS_ff_syst_nnscore_Era{shift}".format(
                shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
mmt_anti_isoid_mu_2_tau_nn_var = [
    ReplaceMultipleCutsAndAddWeight(
        "mu2tau_anti_isoid_CMS_ff_nnscore_Era{shift}".format(shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || muon_is_mediumid_2<0.5)",
                "mu_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_Era*lep_2_fakerate_Era*fakerate_CMS_ff_syst_nnscore_Era{shift}".format(
                shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
anti_isoid_ele_2_tau_nn_var = [
    ReplaceMultipleCutsAndAddWeight(
        "ele2tau_anti_isoid_CMS_ff_nnscore_Era{shift}".format(shift=shift),
        ["id_iso_cut_2", "tau_iso"],
        [
            Cut(
                "((iso_2<0.5&&iso_2>0.15) || electron_is_nonisowp90_2<0.5)",
                "ele_2_anti_iso",
            ),
            Cut(
                "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
                "tau_anti_iso",
            ),
        ],
        Weight(
            "-tau_fakerate_Era*lep_2_fakerate_Era*fakerate_CMS_ff_syst_nnscore_Era{shift}".format(
                shift=shift
            ),
            "fake_factor",
        ),
    )
    for shift in ["Up", "Down"]
]
# to calculate closure corrections
anti_iso_mmt_closure = ReplaceCutAndAddWeight(
    "tau_anti_iso",
    "tau_iso",
    Cut(
        "(id_tau_vsJet_Medium_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)",
        "tau_anti_iso",
    ),
    Weight(
        "tau_fakerate_Era",
        "fake_factor",
    ),
)
anti_iso_eem_closure = ReplaceCutAndAddWeight(
    "anti_id_iso_3",
    "id_iso_3",
    Cut(
        "((iso_3<0.5 && iso_3>0.15) || muon_is_mediumid_3<0.5)",
        "lep_anti_iso",
    ),
    Weight(
        "lep_3_fakerate_Era",
        "fake_factor",
    ),
)
anti_iso_mme_closure = ReplaceCutAndAddWeight(
    "anti_id_iso_3",
    "id_iso_3",
    Cut(
        "((iso_3<0.5 && iso_3>0.15) || electron_is_nonisowp90_3<0.5)",
        "lep_anti_iso",
    ),
    Weight(
        "lep_3_fakerate_Era",
        "fake_factor",
    ),
)
# Pileup reweighting
pileup_reweighting = [
    ReplaceVariable("CMS_pileup_EraUp", "PileUpUp"),
    ReplaceVariable("CMS_pileup_EraDown", "PileUpDown"),
]
# electron reco uncertainty
ele_reco_unc = [
    ReplaceVariable("CMS_eff_e_recoUp", "eleRecoUp"),
    ReplaceVariable("CMS_eff_e_recoDown", "eleRecoDown"),
]

# electron ID uncertainty
emt_eleID_unc = [
    ReplaceWeight(
        "CMS_eff_eUp",
        "idweight",
        Weight(
            "(((pt_1<100. || abs(eta_1)<1.566)*1.02+(pt_1>100. && abs(eta_1)>1.566)*1.025)*id_wgt_ele_wp90nonIso_1*electron_is_nonisowp90_1>0.5+1.0*electron_is_nonisowp90_1<0.5)*(id_wgt_mu_2*muon_is_mediumid_2 > 0.5 + 1.0*muon_is_mediumid_2 < 0.5)",
            "idweight",
        ),
    ),
    ReplaceWeight(
        "CMS_eff_eDown",
        "idweight",
        Weight(
            "(((pt_1<100.|| abs(eta_1)<1.566)*0.98+(pt_1>100. && abs(eta_1)>1.566)*0.975)*id_wgt_ele_wp90nonIso_1*electron_is_nonisowp90_1>0.5+1.0*electron_is_nonisowp90_1<0.5)*(id_wgt_mu_2*muon_is_mediumid_2 > 0.5 + 1.0*muon_is_mediumid_2 < 0.5)",
            "idweight",
        ),
    ),
]
ett_eleID_unc = [
    ReplaceWeight(
        "CMS_eff_eUp",
        "idweight",
        Weight(
            "(((pt_1<100. || abs(eta_1)<1.566)*1.02+(pt_1>100. && abs(eta_1)>1.566)*1.025)*id_wgt_ele_wp90nonIso_1*electron_is_nonisowp90_1>0.5+1.0*electron_is_nonisowp90_1<0.5)",
            "idweight",
        ),
    ),
    ReplaceWeight(
        "CMS_eff_eDown",
        "idweight",
        Weight(
            "(((pt_1<100. || abs(eta_1)<1.566)*0.98+(pt_1>100. && abs(eta_1)>1.566)*0.975)*id_wgt_ele_wp90nonIso_1*electron_is_nonisowp90_1>0.5+1.0*electron_is_nonisowp90_1<0.5)",
            "idweight",
        ),
    ),
]
met_eleID_unc = [
    ReplaceWeight(
        "CMS_eff_eUp",
        "idweight",
        Weight(
            "(((pt_2<100. || abs(eta_2)<1.566)*1.02+(pt_2>100. && abs(eta_2)>1.566)*1.025)*id_wgt_ele_wp90nonIso_2*electron_is_nonisowp90_2>0.5+1.0*electron_is_nonisowp90_2<0.5)*(id_wgt_mu_1*muon_is_mediumid_1 > 0.5 + 1.0*muon_is_mediumid_1 < 0.5)",
            "idweight",
        ),
    ),
    ReplaceWeight(
        "CMS_eff_eDown",
        "idweight",
        Weight(
            "(((pt_2<100. || abs(eta_2)<1.566)*0.98+(pt_2>100. && abs(eta_2)>1.566)*0.975)*id_wgt_ele_wp90nonIso_2*electron_is_nonisowp90_2>0.5+1.0*electron_is_nonisowp90_2<0.5)*(id_wgt_mu_1*muon_is_mediumid_1 > 0.5 + 1.0*muon_is_mediumid_1 < 0.5)",
            "idweight",
        ),
    ),
]
# btag uncertainties
btag_sf_unc = [
    ReplaceVariable("CMS_btag_shape_hfUp", "btagUncHFUp"),
    ReplaceVariable("CMS_btag_shape_hfDown", "btagUncHFDown"),
    ReplaceVariable("CMS_btag_shape_hfstats1_EraUp", "btagUncHFstats1Up"),
    ReplaceVariable("CMS_btag_shape_hfstats1_EraDown", "btagUncHFstats1Down"),
    ReplaceVariable("CMS_btag_shape_hfstats2_EraUp", "btagUncHFstats2Up"),
    ReplaceVariable("CMS_btag_shape_hfstats2_EraDown", "btagUncHFstats2Down"),
    ReplaceVariable("CMS_btag_shape_lfUp", "btagUncLFUp"),
    ReplaceVariable("CMS_btag_shape_lfDown", "btagUncLFDown"),
    ReplaceVariable("CMS_btag_shape_lfstats1_EraUp", "btagUncLFstats1Up"),
    ReplaceVariable("CMS_btag_shape_lfstats1_EraDown", "btagUncLFstats1Down"),
    ReplaceVariable("CMS_btag_shape_lfstats2_EraUp", "btagUncLFstats2Up"),
    ReplaceVariable("CMS_btag_shape_lfstats2_EraDown", "btagUncLFstats2Down"),
    ReplaceVariable("CMS_btag_shape_cferr1Up", "btagUncCFerr1Up"),
    ReplaceVariable("CMS_btag_shape_cferr1Down", "btagUncCFerr1Down"),
    ReplaceVariable("CMS_btag_shape_cferr2Up", "btagUncCFerr2Up"),
    ReplaceVariable("CMS_btag_shape_cferr2Down", "btagUncCFerr2Down"),
]

# Energy scales.
# Previously defined with 2017 in name.
tau_es_3prong = [
    ReplaceVariable("CMS_scale_t_DM10_EraUp", "tauEs3prong0pizeroUp"),
    ReplaceVariable("CMS_scale_t_DM10_EraDown", "tauEs3prong0pizeroDown"),
]

tau_es_3prong1pizero = [
    ReplaceVariable("CMS_scale_t_DM11_EraUp", "tauEs3prong1pizeroUp"),
    ReplaceVariable("CMS_scale_t_DM11_EraDown", "tauEs3prong1pizeroDown"),
]

tau_es_1prong = [
    ReplaceVariable("CMS_scale_t_DM0_EraUp", "tauEs1prong0pizeroUp"),
    ReplaceVariable("CMS_scale_t_DM0_EraDown", "tauEs1prong0pizeroDown"),
]

tau_es_1prong1pizero = [
    ReplaceVariable("CMS_scale_t_DM1_EraUp", "tauEs1prong1pizeroUp"),
    ReplaceVariable("CMS_scale_t_DM1_EraDown", "tauEs1prong1pizeroDown"),
]
# Electron energy scale
ele_es = [
    ReplaceVariable("CMS_scale_eUp", "eleEsScaleUp"),
    ReplaceVariable("CMS_scale_eDown", "eleEsScaleDown"),
]

ele_res = [
    ReplaceVariable("CMS_res_eUp", "eleEsResoUp"),
    ReplaceVariable("CMS_res_eDown", "eleEsResoDown"),
]

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
    ReplaceVariable("CMS_scale_met_EraUp", "metUnclusteredEnUp"),
    ReplaceVariable("CMS_scale_met_EraDown", "metUnclusteredEnDown"),
]

# Recoil correction uncertainties
recoil_resolution = [
    ReplaceVariable("CMS_res_met_EraUp", "metRecoilResolutionUp"),
    ReplaceVariable("CMS_res_met_EraDown", "metRecoilResolutionDown"),
]

recoil_response = [
    ReplaceVariable("CMS_scale_met_EraUp", "metRecoilResponseUp"),
    ReplaceVariable("CMS_scale_met_EraDown", "metRecoilResponseDown"),
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
    ReplaceVariable("CMS_eff_t_DM0_EraUp", "vsJetTauDM0Up"),
    ReplaceVariable("CMS_eff_t_DM0_EraDown", "vsJetTauDM0Down"),
    ReplaceVariable("CMS_eff_t_DM1_EraUp", "vsJetTauDM1Up"),
    ReplaceVariable("CMS_eff_t_DM1_EraDown", "vsJetTauDM1Down"),
    ReplaceVariable("CMS_eff_t_DM10_EraUp", "vsJetTauDM10Up"),
    ReplaceVariable("CMS_eff_t_DM10_EraDown", "vsJetTauDM10Down"),
    ReplaceVariable("CMS_eff_t_DM11_EraUp", "vsJetTauDM11Up"),
    ReplaceVariable("CMS_eff_t_DM11_EraDown", "vsJetTauDM11Down"),
]

# # Trigger efficiency uncertainties.
trigger_eff_mu = [
    ReplaceVariable("CMS_eff_m_trigger_EraUp", "singleMuonTriggerSFUp"),
    ReplaceVariable("CMS_eff_m_trigger_EraDown", "singleMuonTriggerSFDown"),
]
trigger_eff_e = [
    ReplaceVariable("CMS_eff_e_trigger_EraUp", "singleElectronTriggerSFUp"),
    ReplaceVariable("CMS_eff_e_trigger_EraDown", "singleElectronTriggerSFDown"),
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
qcd_scale_vv = [
    ReplaceWeight(
        "QCD_ren_scale_VVDown",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRDown", "lhe_scale_weight_mur_down"),
    ),
    ReplaceWeight(
        "QCD_ren_scale_VVUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRUp", "lhe_scale_weight_mur_up"),
    ),
    ReplaceWeight(
        "QCD_fac_scale_VVDown",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuFDown", "lhe_scale_weight_muf_down"),
    ),
    ReplaceWeight(
        "QCD_fac_scale_VVUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuFUp", "lhe_scale_weight_muf_up"),
    ),
]
qcd_scale_vh = [
    ReplaceWeight(
        "QCD_ren_scale_VHDown",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRDown", "lhe_scale_weight_mur_down"),
    ),
    ReplaceWeight(
        "QCD_ren_scale_VHUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRUp", "lhe_scale_weight_mur_up"),
    ),
    ReplaceWeight(
        "QCD_fac_scale_VHDown",
        "lhe_scale_weight",
        Weight(
            "lhe_scale_weight__LHEScaleWeightMuFDown*(lhe_scale_weight__LHEScaleWeightMuFDown>0.0)+1.*(lhe_scale_weight__LHEScaleWeightMuFDown<0.0)",
            "lhe_scale_weight_muf_down",
        ),
    ),
    ReplaceWeight(
        "QCD_fac_scale_VHUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuFUp", "lhe_scale_weight_muf_up"),
    ),
]
qcd_scale_ggzh = [
    ReplaceWeight(
        "QCD_ren_scale_ggZHDown",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRDown", "lhe_scale_weight_mur_down"),
    ),
    ReplaceWeight(
        "QCD_ren_scale_ggZHUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRUp", "lhe_scale_weight_mur_up"),
    ),
    ReplaceWeight(
        "QCD_fac_scale_ggZHDown",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuFDown", "lhe_scale_weight_muf_down"),
    ),
    ReplaceWeight(
        "QCD_fac_scale_ggZHUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuFUp", "lhe_scale_weight_muf_up"),
    ),
]
qcd_scale_ttv = [
    ReplaceWeight(
        "QCD_ren_scale_TTVDown",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRDown", "lhe_scale_weight_mur_down"),
    ),
    ReplaceWeight(
        "QCD_ren_scale_TTVUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRUp", "lhe_scale_weight_mur_up"),
    ),
    ReplaceWeight(
        "QCD_fac_scale_TTVDown",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuFDown", "lhe_scale_weight_muf_down"),
    ),
    ReplaceWeight(
        "QCD_fac_scale_TTVUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuFUp", "lhe_scale_weight_muf_up"),
    ),
]
qcd_scale_vvv = [
    ReplaceWeight(
        "QCD_ren_scale_VVVDown",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRDown", "lhe_scale_weight_mur_down"),
    ),
    ReplaceWeight(
        "QCD_ren_scale_VVVUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuRUp", "lhe_scale_weight_mur_up"),
    ),
    ReplaceWeight(
        "QCD_fac_scale_VVVDown",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuFDown", "lhe_scale_weight_muf_down"),
    ),
    ReplaceWeight(
        "QCD_fac_scale_VVVUp",
        "lhe_scale_weight",
        Weight("lhe_scale_weight__LHEScaleWeightMuFUp", "lhe_scale_weight_muf_up"),
    ),
]
pdf_WH = [
    ReplaceWeight(
        "pdf_WHUp",
        "lhe_pdf_weight",
        Weight("lhe_pdf_weight_up", "lhe_pdf_weight_up"),
    ),
    ReplaceWeight(
        "pdf_WHDown",
        "lhe_pdf_weight",
        Weight("lhe_pdf_weight_down", "lhe_pdf_weight_down"),
    ),
]
pdf_qqbar = [
    ReplaceWeight(
        "pdf_qqbarUp",
        "lhe_pdf_weight",
        Weight("lhe_pdf_weight_up", "lhe_pdf_weight_up"),
    ),
    ReplaceWeight(
        "pdf_qqbarDown",
        "lhe_pdf_weight",
        Weight("lhe_pdf_weight_down", "lhe_pdf_weight_down"),
    ),
]
zpt = [
    SquareWeight("CMS_htt_dyShape_EraUp", "zPtReweightWeight"),
    RemoveWeight("CMS_htt_dyShape_EraDown", "zPtReweightWeight"),
]

top_pt = [
    RemoveWeight("top_pt_reweightingUp", "topPtReweightWeight"),
    RemoveWeight("top_pt_reweightingDown", "topPtReweightWeight"),
]


## v_3
# anti_iso_llt_tau = ReplaceCutAndAddWeight(
#     "tau_anti_iso",
#     "tau_iso",
#     Cut("id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
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
#         Cut("(id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
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
#         Cut("(id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
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
#         Cut("(id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
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
#         Cut("(id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
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
#         Cut("(id_tau_vsJet_Tight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5)", "tau_anti_iso"),
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
#         "((q_1*q_2>0) && id_tau_vsJet_Tight_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5 && id_tau_vsJet_Tight_3>0.5) || ((q_1*q_3>0) && id_tau_vsJet_Tight_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5 && id_tau_vsJet_Tight_2>0.5)",
#         "tau_anti_iso",
#     ),
#     Weight("tau_fakerate", "fake_factor"),
# )
