from asyncio import new_event_loop
from ntuple_processor.utils import Selection
import ROOT as R

##### wh analysis selction
def channel_selection(channel, era, region):
    if channel in ["emt", "met", "mmt"]:
        if region == "sig_plus":
            cuts = [
                (
                    "Lt>100 && (abs(eta_1-eta_vis)<2.0) && (abs(deltaPhi_WH)>2.0)",
                    "signal_region",
                ),
                ("q_1>0.0", "signal_plus"),
            ]
        elif region == "sig_minus":
            cuts = [
                (
                    "Lt>100 && (abs(eta_1-eta_vis)<2.0) && (abs(deltaPhi_WH)>2.0)",
                    "signal_region",
                ),
                ("q_1<0.0", "signal_minus"),
            ]
        elif region == "control_plus":
            cuts = [
                (
                    "!(Lt>100 && (abs(eta_1-eta_vis)<2.0) && (abs(deltaPhi_WH)>2.0))",
                    "ctrl_region",
                ),
                ("q_1>0.0", "control_plus"),
            ]
        elif region == "control_minus":
            cuts = [
                (
                    "!(Lt>100 && (abs(eta_1-eta_vis)<2.0) && (abs(deltaPhi_WH)>2.0))",
                    "ctrl_region",
                ),
                ("q_1<0.0", "control_minus"),
            ]
        elif region == "control":
            cuts = [
                (
                    "!(Lt>100 && (abs(eta_1-eta_vis)<2.0) && (abs(deltaPhi_WH)>2.0))",
                    "ctrl_region",
                ),
            ]
    elif channel in ["ett", "mtt"]:
        if region == "sig_plus":
            cuts = [
                (
                    "Lt>130 && pt_123met<70",
                    "signal_region",
                ),
                ("q_1>0.0", "signal_plus"),
            ]
        elif region == "sig_minus":
            cuts = [
                (
                    "Lt>130 && pt_123met<70",
                    "signal_region",
                ),
                ("q_1<0.0", "signal_minus"),
            ]
        elif region == "control_plus":
            cuts = [
                (
                    "!(Lt>130 && pt_123met<70)",
                    "ctrl_region",
                ),
                ("q_1>0.0", "signal_plus"),
            ]
        elif region == "control_minus":
            cuts = [
                (
                    "!(Lt>130 && pt_123met<70)",
                    "ctrl_region",
                ),
                ("q_1<0.0", "signal_minus"),
            ]
        elif region == "control":
            cuts = [
                (
                    "!(Lt>130 && pt_123met<70)",
                    "ctrl",
                ),
            ]
    # Specify general channel and era independent cuts.
    if channel in ["emt", "met"]:
        cuts.extend(
            [
                ("q_1*q_2>0.0", "ss"),
                ("q_2*q_3<0.0", "os"),
                ("pt_1>15.", "pt_1_cut"),
                ("pt_2>15.", "pt_2_cut"),
                ("nbtag<0.5", "b_veto"),
                ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
                ("id_tau_vsEle_Tight_3>0.5", "againstElectronDiscriminator"),
                ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
            ]
        )
        if channel == "emt":
            # triggermatching for single ele and single mu trigger and corresponding pt requirements
            # id and iso cuts have to be in one cut, cause of the variations
            # cuts.append(("muon_is_mediumid_2 > 0.5 && iso_2<0.15", "id_iso_cut_2"))
            cuts.append(("muon_is_mediumid_2 > 0.5 && iso_2<0.15", "id_iso_cut_2"))
            cuts.append(("electron_is_nonisowp90_1>0.5 && iso_1<0.15", "id_iso_cut_1"))
            if era == "2018":
                cuts.append(
                    (
                        "(((pt_2>=28&&(trg_single_mu27 == 1)) || (pt_2>25&&pt_2<28&&(trg_single_mu24 == 1))) &&pt_1<33 && (abs(eta_2)<2.1)) || ((abs(eta_1)<2.1)&&((pt_1>=33 && pt_1 < 36 && (trg_single_ele32==1)) || (pt_1 >=36 && (trg_single_ele35==1))))",
                        "trg_selection",
                    )
                )
            elif era == "2017":
                cuts.append(
                    (
                        "(((pt_2>=28&&(trg_single_mu27 == 1)) || (pt_2>25&&pt_2<28&&(trg_single_mu24 == 1))) && pt_1<28 && (abs(eta_2)<2.1)) || ((abs(eta_1)<2.1)&&((pt_1>=33 && pt_1 < 36 && (trg_single_ele32==1)) || (pt_1 >=36 && (trg_single_ele35==1)) ||(pt_1>28&&pt_1<=33&&(trg_single_ele27==1))))",
                        "trg_selection",
                    )
                )
            elif "2016" in era:
                cuts.append(
                    (
                        "((trg_single_mu22 == 1) && pt_2 > 23 && pt_1<26 && (abs(eta_2)<2.1)) || (pt_1 > 26 && (abs(eta_1)<2.1) && (trg_single_ele25 == 1))",
                        "trg_selection",
                    )
                )
        elif channel == "met":
            cuts.append(("muon_is_mediumid_1>0.5 && iso_1<0.15", "id_iso_cut_1"))
            cuts.append(("electron_is_nonisowp90_2>0.5 && iso_2<0.15", "id_iso_cut_2"))
            # triggermatching for single ele and single mu trigger and corresponding pt requirements
            if era == "2018":
                cuts.append(
                    (
                        "((((trg_single_mu27 == 1)&&pt_1>27) || ((trg_single_mu24 == 1)&&pt_1<=27&&pt_1>25)) && (abs(eta_1)<2.4)) || (pt_1 < 25 && (abs(eta_2)<2.1) && (((trg_single_ele32 == 1)&&pt_2>33&&pt_2<=36) || ((trg_single_ele35 == 1)&&pt_2>36)))",
                        "trg_selection",
                    )
                )
            elif era == "2017":
                cuts.append(
                    (
                        "((((trg_single_mu27 == 1)&&pt_1>27) || ((trg_single_mu24 == 1)&&pt_1<=27&&pt_1>25)) && (abs(eta_1)<2.4)) || (pt_1 < 25 && (abs(eta_2)<2.1) && (((trg_single_ele32 == 1)&&pt_2>33&&pt_2<=36) || ((trg_single_ele35 == 1)&&pt_2>36)) || ((trg_single_ele27 == 1)&&pt_2>28&&pt_2<=33))",
                        "trg_selection",
                    )
                )
            elif "2016" in era:
                cuts.append(
                    (
                        "((trg_single_mu22 == 1) && pt_1 > 23 && (abs(eta_1)<2.1)) || (pt_1 < 23 && pt_2 > 26 && (abs(eta_2)<2.1) && (trg_single_ele25 == 1))",
                        "trg_selection",
                    )
                )
    elif channel == "mmt":
        cuts.extend(
            [
                ("q_1*q_2>0.0", "ss"),
                ("q_2*q_3<0.0", "os"),
                ("pt_1>15.", "pt_1_cut"),
                ("pt_2>15.", "pt_2_cut"),
                ("nbtag<0.5", "b_veto"),
                ("id_tau_vsMu_Tight_3>0.5", "againstMuonDiscriminator"),
                ("id_tau_vsEle_VLoose_3>0.5", "againstElectronDiscriminator"),
                ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
                ("iso_1<0.15", "iso_cut_1"),
                ("deltaR_13>0.5&&deltaR_23>0.5", "deltaR_cut"),
                ("muon_is_mediumid_1 > 0.5", "id_cut_1"),
                ("muon_is_mediumid_2 > 0.5 && iso_2<0.15", "id_iso_cut_2"),
            ]
        )
        if era in ["2018", "2017"]:
            cuts.append(
                (
                    "((((trg_single_mu27 == 1)&&pt_1>28) || ((trg_single_mu24 == 1)&&pt_1>25&&pt_1<=28)) && (abs(eta_1)<2.4))",
                    "trg_selection",
                )
            )
        else:
            cuts.append(
                (
                    "((trg_single_mu22 == 1) && pt_1 > 23 && (abs(eta_1)<2.1))",
                    "trg_selection",
                )
            )
    elif channel == "ett":
        cuts.extend(
            [
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
                # (
                #     "((q_1*q_2>0.5)*id_tau_vsJet_Tight_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0.5)*id_tau_vsJet_Medium_2>0.5 && id_tau_vsJet_Tight_3>0.5)",
                #     "tau_iso",
                # ),
                (
                    "(id_tau_vsJet_Tight_2>0.5 && id_tau_vsJet_Tight_3>0.5)",
                    "tau_iso",
                ),
                ("deltaR_13>0.5&&deltaR_23>0.5&&deltaR_12>0.5", "deltaR_cut"),
                ("extramuon_veto<0.5", "extramuon_veto"),
                (
                    "((q_1*q_2>0.5) && pt_2>30) || ((q_1*q_3>0.5) && pt_3>30)",
                    "ss_pt_cut",
                ),
            ]
        )
        if era == "2018":
            cuts.append(
                (
                    "(abs(eta_1)<2.1) && (((trg_single_ele32 == 1)&&pt_1>33&&pt_1<=36) || ((trg_single_ele35 == 1&&pt_1>36)))",
                    "trg_selection",
                )
            )
        elif era == "2017":
            cuts.append(
                (
                    "(abs(eta_1)<2.1) && (((trg_single_ele27 == 1)&&pt_1>27&&pt_1<=33) || ((trg_single_ele32 == 1)&&pt_1>33&&pt_1<=36) || ((trg_single_ele35 == 1)&&pt_1>36))",
                    "trg_selection",
                )
            )
        else:
            cuts.append(
                (
                    "pt_1 > 26 && (abs(eta_1)<2.1) && (trg_single_ele25 == 1)",
                    "trg_selection",
                )
            )

    elif channel == "mtt":
        cuts.extend(
            [
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
                # (
                #     "((q_1*q_2>0.5)*id_tau_vsJet_Tight_2>0.5 && id_tau_vsJet_Medium_3>0.5) || ((q_1*q_3>0.5)*id_tau_vsJet_Medium_2>0.5 && id_tau_vsJet_Tight_3>0.5)",
                #     "tau_iso",
                # ),
                (
                    "(id_tau_vsJet_Tight_2>0.5 && id_tau_vsJet_Tight_3>0.5)",
                    "tau_iso",
                ),
                ("deltaR_13>0.5&&deltaR_23>0.5&&deltaR_12>0.5", "deltaR_cut"),
                ("extraelec_veto<0.5", "extraelectron_veto"),
                (
                    "((q_1*q_2>0.5) && pt_2>30) || ((q_1*q_3>0.5) && pt_3>30)",
                    "ss_pt_cut",
                ),
            ]
        )
        if era in ["2018", "2017"]:
            cuts.append(
                (
                    "((((trg_single_mu27 == 1)&&pt_1>28) || ((trg_single_mu24 == 1)&&pt_1>25&&pt_1<=28))&& (abs(eta_1)<2.4))",
                    "trg_selection",
                ),
            )
        else:
            cuts.append(
                (
                    "((trg_single_mu22 == 1) && pt_1 > 23 && (abs(eta_1)<2.1))",
                    "trg_selection",
                ),
            )
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
#         ("id_tau_vsJet_Tight_3>0.5", "tau_iso"),
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
