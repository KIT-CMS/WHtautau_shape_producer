from asyncio import new_event_loop
from ntuple_processor.utils import Selection
import ROOT as R


##### wh analysis selction
def channel_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, decay_mode, id_wp_ele, id_wp_mu, wp_vs_jet_tight
):
    # jet to tau fakerate
    if channel == "mmt":
        cuts = [
            ("q_1*q_2<0.0", "os"),
            (
                "id_tau_vsMu_{wp_vs_mu}_3>0.5".format(wp_vs_mu=wp_vs_mu),
                "againstMuonDiscriminator",
            ),
            (
                "id_tau_vsEle_{wp_vs_ele}_3>0.5".format(wp_vs_ele=wp_vs_ele),
                "againstElectronDiscriminator",
            ),
            ("iso_1<0.15", "iso_1"),
            ("iso_2<0.15", "iso_2"),
            ("decaymode_3=={decay_mode}".format(decay_mode=decay_mode), "DM_cut"),
            ("muon_is_mediumid_1 > 0.5 && muon_is_mediumid_2 > 0.5", "muon_id_cut"),
            # ("id_tau_vsJet_{wp_vs_jet}_3>0.5".format(wp_vs_jet=wp_vs_jet), "tau_iso"),
            ("nbtag<0.5", "b_veto"),
        ]
        if wp_vs_jet == "VVVLoose":
            cuts.append(
                (
                    "id_tau_vsJet_{wp_vs_jet}_3>0.5 && id_tau_vsJet_{wp_vs_jet_tight}_3<0.5".format(
                        wp_vs_jet=wp_vs_jet, wp_vs_jet_tight=wp_vs_jet_tight
                    ),
                    "tau_iso",
                )
            )
        else:
            cuts.append(
                (
                    "id_tau_vsJet_{wp_vs_jet}_3>0.5".format(wp_vs_jet=wp_vs_jet),
                    "tau_iso",
                )
            )
        if era in ["2018", "2017"]:
            cuts.append(
                (
                    "((((trg_single_mu27 == 1)&&pt_1>28) || ((trg_single_mu24 == 1)&&pt_1>25&&pt_1<=28)) && (abs(eta_1)<2.1))",
                    "trg_selection",
                ),
            )
        else:
            cuts.append(
                (
                    "(((trg_single_mu22 == 1) || (trg_single_mu22_tk == 1)  || (trg_single_mu22_eta2p1 == 1)  || (trg_single_mu22_tk_eta2p1 == 1)) && pt_1 > 23 && (abs(eta_1)<2.1))",
                    "trg_selection",
                ),
            )
    # jet to electron fakerate
    elif channel == "mme":
        # base
        cuts = [
            ("q_1*q_2<0.0", "os"),
            ("pt_2>10", "pt_2_cut"),
            ("iso_1<0.15", "iso_1"),
            ("iso_2<0.15", "iso_2"),
            # ("mt_3<40", "mt_cut"),
            ("muon_is_mediumid_1 > 0.5 && muon_is_mediumid_2 > 0.5", "muon_id_cut"),
            ("nbtag<0.5", "b_veto"),
        ]
        # tight
        if id_wp_ele == "Tight":
            cuts.append(("iso_3<0.15", "iso_3"))
            cuts.append(("electron_is_nonisowp90_3>0.5", "ele_id_cut"))
        else:
            cuts.append(
                (
                    "((iso_3>0.15 && iso_3<0.5) || electron_is_nonisowp90_3<0.5)",
                    "id_iso_3",
                )
            )

        # trigger requirements
        if era in ["2018", "2017"]:
            cuts.append(
                (
                    "((((trg_single_mu27 == 1)&&pt_1>28) || ((trg_single_mu24 == 1)&&pt_1>25&&pt_1<=28)) && (abs(eta_1)<2.1))",
                    "trg_selection",
                ),
            )
        else:
            cuts.append(
                (
                    "(((trg_single_mu22 == 1) || (trg_single_mu22_tk == 1)  || (trg_single_mu22_eta2p1 == 1)  || (trg_single_mu22_tk_eta2p1 == 1)) && pt_1 > 23 && (abs(eta_1)<2.1))",
                    "trg_selection",
                ),
            )
    # jet to muon fakerate
    elif channel == "eem":
        # base
        cuts = [
            ("q_1*q_2<0.0", "os"),
            ("pt_2>10", "pt_2_cut"),
            ("iso_1<0.15", "iso_1"),
            ("iso_2<0.15", "iso_2"),
            # ("mt_3<40", "mt_cut"),
            (
                "electron_is_nonisowp90_1>0.5 && electron_is_nonisowp90_2>0.5",
                "ele_id_cut",
            ),
            ("nbtag<0.5", "b_veto"),
            # ("muon_is_mediumid_3>0.5", "mu_id_cut"),
        ]
        # tight
        if id_wp_mu == "Tight":
            cuts.append(("iso_3<0.15", "iso_3"))
            cuts.append(("muon_is_mediumid_3>0.5", "mu_id_cut"))
        else:
            cuts.append(
                ("(iso_3<0.5 && iso_3>0.15) || muon_is_mediumid_3<0.5", "id_iso_3")
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
                    "(abs(eta_1)<2.1) && (((trg_single_ele27 == 1)&&pt_1>28&&pt_1<=33) || ((trg_single_ele32 == 1)&&pt_1>33&&pt_1<=36) || ((trg_single_ele35 == 1)&&pt_1>36))",
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
    return Selection(name="{ch}".format(ch=channel), cuts=cuts)
