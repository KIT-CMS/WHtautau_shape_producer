from ntuple_processor.utils import Selection
import ROOT as R


def channel_selection(channel, era):
    # Specify general channel and era independent cuts.

    cuts = [
        ("q_1*q_2>0.0", "ss"),
        ("q_2*q_3<0.0", "os"),
        ("pt_1>15.", "ele_pt"),
        ("pt_2>15.", "mu_pt"),
        ("nbtag<1.", "b_veto"),
        ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
        ("id_tau_vsEle_Tight_3>0.5", "againstElectronDiscriminator"),
        ("id_tau_vsJet_VTight_3>0.5", "tau_iso"),
        # (
        #     "Lt<100 || (abs(eta_1-eta_2)>2.0) || (abs(eta_1-eta_3)>2.0) || (abs(deltaPhi_elemu)<2.0) || (abs(deltaPhi_eletau)<2.0)",
        #     "ctrl1",
        # ),
        (
            "Lt<100 || (abs(eta_1-eta_vis)>2.0) || (abs(deltaPhi_WH)<2.0)",
            "ctrl2",
        ),
        # (
        #     "Lt>100. && (abs(eta_1-eta_2)<2.0) && (abs(eta_1-eta_3)<2.0) && (abs(deltaPhi_elemu)>2.0) && (abs(deltaPhi_eletau)>2.0)",
        #     "sig",
        # ),
        # (
        #     "Lt>100. && (abs(eta_1-eta_vis)<2.0) && (abs(deltaPhi_WH)>2.0)",
        #     "sig2",
        # ),
    ]
    if "emt" in channel:
        # triggermatching for single ele and single mu trigger and corresponding pt requirements
        cuts.append(
            (
                "(((trg_single_mu27 == 1) || (trg_single_mu24 == 1)) && pt_2 > 25) || (pt_2 < 25 && pt_1 > 33 && ((trg_single_ele32 == 1) || (trg_single_ele35 == 1)))",
                "trg_selection",
            )
        )
    return Selection(name="emt", cuts=cuts)
