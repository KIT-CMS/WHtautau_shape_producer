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

###incl. bveto
anti_iso_llt_tau = ReplaceCutAndAddWeight(
    "tau_anti_iso",
    "tau_iso",
    Cut("id_tau_vsJet_VTight_3<0.5&&id_tau_vsJet_VVVLoose_3>0.5", "tau_anti_iso"),
    Weight("tau_fakerate", "fake_factor"),
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
    Weight("lep_1_fakerate", "fake_factor"),
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
    Weight("lep_2_fakerate", "fake_factor"),
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
    Weight("lep_2_fakerate", "fake_factor"),
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
    Weight("lep_1_fakerate", "fake_factor"),
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
    Weight("lep_2_fakerate", "fake_factor"),
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
        "-tau_fakerate*lep_1_fakerate",
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
        "-tau_fakerate*lep_2_fakerate",
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
        "-tau_fakerate*lep_2_fakerate",
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
        "-tau_fakerate*lep_1_fakerate",
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
        "-tau_fakerate*lep_2_fakerate",
        "fake_factor",
    ),
)
anti_iso_ltt = ReplaceCutAndAddWeight(
    "tau_anti_iso",
    "tau_iso",
    Cut(
        "((q_1*q_2>0) && id_tau_vsJet_VTight_2<0.5 && id_tau_vsJet_VVVLoose_2>0.5) || ((q_1*q_3>0) && id_tau_vsJet_VTight_3<0.5 && id_tau_vsJet_VVVLoose_3>0.5)",
        "tau_anti_iso",
    ),
    Weight("tau_fakerate/(1-tau_fakerate)", "fake_factor"),
)
