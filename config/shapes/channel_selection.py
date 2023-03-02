from asyncio import new_event_loop
from ntuple_processor.utils import Selection
import ROOT as R

##### wh analysis selction
def channel_selection(channel, era):
    # Specify general channel and era independent cuts.
    if channel in ["emt", "met"]:
        cuts = [
            ("q_1*q_2<0.0", "ss"),
            #("q_2*q_3<0.0", "os"),
            ("pt_1>15.", "pt_1_cut"),
            ("pt_2>15.", "pt_2_cut"),
            ("nbtag<0.5", "b_veto"),
            ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
            ("id_tau_vsEle_Tight_3>0.5", "againstElectronDiscriminator"),
            ("id_tau_vsJet_VTight_3>0.5", "tau_iso"),
            ("iso_1<0.15", "iso_cut_1"),
            ("iso_2<0.15", "iso_cut_2"),
            # (
            #     "Lt<100 || (abs(eta_1-eta_2)>2.0) || (abs(eta_1-eta_3)>2.0) || (abs(deltaPhi_elemu)<2.0) || (abs(deltaPhi_eletau)<2.0)",
            #     "ctrl1",
            # ),
            (
                "Lt<100 || (abs(eta_1-eta_vis)>2.0) || (abs(deltaPhi_WH)<2.0)",
                "ctrl_region",
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
        if channel == "emt":
            # triggermatching for single ele and single mu trigger and corresponding pt requirements
            cuts.append(("muon_is_mediumid_2 > 0.5", "id_cut_2"))
            cuts.append(("electron_is_nonisowp90_1>0.5", "id_cut_1"))
            cuts.append(
                (
                    "(((trg_single_mu27 == 1) || (trg_single_mu24 == 1)) && pt_2 > 25) || (pt_2 < 25 && pt_1 > 33 && ((trg_single_ele32 == 1) || (trg_single_ele35 == 1)))",
                    "trg_selection",
                )
            )
        elif channel == "met":
            cuts.append(("muon_is_mediumid_1 > 0.5", "id_cut_1"))
            cuts.append(("electron_is_nonisowp90_2>0.5", "id_cut_2"))
            # triggermatching for single ele and single mu trigger and corresponding pt requirements
            cuts.append(
                (
                    "(((trg_single_mu27 == 1) || (trg_single_mu24 == 1)) && pt_1 > 25) || (pt_1 < 25 && pt_2 > 33 && ((trg_single_ele32 == 1) || (trg_single_ele35 == 1)))",
                    "trg_selection",
                )
            )
    elif channel == "mmt":
        cuts = [
            ("q_1*q_2<0.0", "ss"),
            #("q_2*q_3<0.0", "os"),
            ("pt_1>15.", "pt_1_cut"),
            ("pt_2>15.", "pt_2_cut"),
            ("nbtag<0.5", "b_veto"),
            ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
            ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
            ("id_tau_vsJet_VTight_3>0.5", "tau_iso"),
            ("iso_1<0.15", "iso_cut_1"),
            ("iso_2<0.15", "iso_cut_2"),
            ("deltaR_13>0.5&&deltaR_23>0.5", "deltaR_cut"),
            (
                "Lt<100 || (abs(eta_1-eta_vis)>2.0) || (abs(deltaPhi_WH)<2.0)",
                "ctrl_region",
            ),
            ("muon_is_mediumid_1 > 0.5", "id_cut_1"),
            ("muon_is_mediumid_2 > 0.5", "id_cut_2"),
        ]
        cuts.append(
            (
                "(((trg_single_mu27 == 1) || (trg_single_mu24 == 1)) && pt_1 > 25)",
                "trg_selection",
            )
        )
    elif channel == "ett":
        cuts = [
            ("electron_is_nonisowp90_1>0.5", "id_cut"),
            ("pt_1>33.", "pt_1_cut"),
            ("iso_1<0.15", "iso_cut_1"),
            ("nbtag<0.5", "b_veto"),
            ("q_2*q_3<0.0", "os"),
            (
                "id_tau_vsEle_Tight_3>0.5&&id_tau_vsEle_Tight_2>0.5",
                "againstElectronDiscriminator",
            ),
            (
                "id_tau_vsMu_VLoose_3>0.5&&id_tau_vsMu_VLoose_2>0.5",
                "againstMuonDiscriminator",
            ),
            ("id_tau_vsJet_VTight_3>0.5&&id_tau_vsJet_VTight_2>0.5", "tau_iso"),
            ("deltaR_13>0.5&&deltaR_23>0.5&&deltaR_12>0.5", "deltaR_cut"),
            ("extramuon_veto<0.5", "extramuon_veto"),
            ("((q_1*q_2>0.5) && pt_2>30) || ((q_1*q_3>0.5) && pt_3>30)", "ss_pt_cut"),
            # trigger selection
            (
                "pt_1 > 33 && ((trg_single_ele32 == 1) || (trg_single_ele35 == 1))",
                "trg_selection",
            ),
            # control region cut
            # (
            #     "Lt<130 || pt_123>70 || met>70",
            #     "ctrl_region",
            # ),
        ]
    elif channel == "mtt":
        cuts = [
            ("muon_is_mediumid_1 > 0.5", "muon_id_cut"),
            ("pt_1>10.", "pt_1_cut"),
            ("iso_1<0.15", "iso_cut_1"),
            ("nbtag<0.5", "b_veto"),
            ("q_2*q_3<0.0", "os"),
            (
                "id_tau_vsEle_VLoose_3>0.5&&id_tau_vsEle_VLoose_2>0.5",
                "againstElectronDiscriminator",
            ),
            (
                "id_tau_vsMu_Tight_3>0.5&&id_tau_vsMu_Tight_2>0.5",
                "againstMuonDiscriminator",
            ),
            ("id_tau_vsJet_VTight_3>0.5&&id_tau_vsJet_VTight_2>0.5", "tau_iso"),
            ("deltaR_13>0.5&&deltaR_23>0.5&&deltaR_12>0.5", "deltaR_cut"),
            ("extraelec_veto<0.5", "extraelectron_veto"),
            ("((q_1*q_2>0.5) && pt_2>30) || ((q_1*q_3>0.5) && pt_3>30)", "ss_pt_cut"),
            # trigger selection
            (
                "(((trg_single_mu27 == 1) || (trg_single_mu24 == 1)) && pt_1 > 25)",
                "trg_selection",
            ),
            # control region cut
            (
                "Lt<130 || pt_123>70 || met>70",
                "ctrl_region",
            ),
        ]
    return Selection(name="{ch}".format(ch=channel), cuts=cuts)


##### end


##### analysis_selection_cut without considering the electron in crown
# def channel_selection(channel, era):
#     cuts = [
#         ("q_1*q_2>0.0", "ss"),
#         ("q_2*q_3<0.0", "os"),
#         ("pt_1>15.", "ele_pt"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_Tight_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_VTight_3>0.5", "tau_iso"),
#         ("nbtag<1.", "b_veto"),
#         ("iso_1<0.15", "electron_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("nelectrons==1", "ele_veto"),
#         ("pt_1>pt_2", "elemu_pt"),
#         ("abs(eta_1)<2.4", "ele_eta"),
#         ("abs(eta_1-eta_2)", "deta_12"),
#         ("abs(eta_3-eta_2)", "deta_23"),
#         (
#             "Lt<100 || (abs(eta_1-eta_vis)>2.0) || (abs(deltaPhi_WH)<2.0)",
#             "ctrl2",
#         ),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "(((trg_single_mu27 == 1) || (trg_single_mu24 == 1)) && pt_2 > 25) || (pt_2 < 25 && pt_1 > 33 && ((trg_single_ele32 == 1) || (trg_single_ele35 == 1)))",
#                 "trg_selection",
#             )
#         )
#     return Selection(name="emt", cuts=cuts)


##### end

##### mt baseline
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)


##### end mt baseline

##### mjj_cut
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("mjj>70 && mjj < 150", "mjj_cut"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)


##### end mt baseline

##### njets_cut
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("njets>=1", "njets_cut"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)


##### end mt baseline

##### nbtag_cut
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("nbtag>=1", "nbtag_cut"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)


##### end mt baseline

##### mjj_njets_nbtag_cut
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("nbtag>0", "nbtag_cut"),
#         ("njets>0", "njets_cut"),
#         ("mjj>70 && mjj < 150", "mjj_cut"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)


##### end mt baseline

##### nbtagst1_cut
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("nbtag<1.", "nbtag_cut"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)


##### end mt baseline

##### pt1_cut
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("nbtag<1.", "nbtag_cut"),
#         ("pt_1>15.", "ele_pt"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)


##### end mt baseline

##### pt1_cut
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("nbtag<1.", "nbtag_cut"),
#         ("pt_1>15.", "ele_pt"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)

##### end mt baseline

##### pt1_os_cut
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("nbtag<1.", "nbtag_cut"),
#         ("pt_1>15.", "ele_pt"),
#         ("q_1*q_2>0.0", "ss"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)


##### end mt baseline

##### mjj_nbtagst1_cut
# def channel_selection(channel, era):
#     cuts = [
#         ("q_2*q_3<0.0", "os"),
#         ("pt_2>15.", "mu_pt"),
#         ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
#         ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
#         ("iso_2<0.15", "muon_iso"),
#         ("nbtag<1", "nbtag_cut"),
#         ("mjj>60 && mjj < 100", "mjj_cut"),
#     ]
#     if "emt" in channel:
#         # triggermatching for single ele and single mu trigger and corresponding pt requirements
#         cuts.append(
#             (
#                 "pt_3>30 && ( (pt_2>=28 && (trg_single_mu27 == 1)) || (pt_2>=25 && pt_2 < 28 && (trg_single_mu24 == 1)))",
#                 "trg_selection",
#             ),
#         )
#     return Selection(name="emt", cuts=cuts)


##### end mt baseline
