from asyncio import new_event_loop
from ntuple_processor.utils import Selection
import ROOT as R

##### wh analysis selction
def channel_selection(
    channel, era, wp_vs_jet, wp_vs_mu, wp_vs_ele, decay_mode, id_wp_ele, id_wp_mu
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
            (
                "(((trg_single_mu27 == 1) || (trg_single_mu24 == 1)) && pt_1 > 25)",
                "trg_selection",
            ),
            ("muon_is_mediumid_1 > 0.5 && muon_is_mediumid_2 > 0.5", "muon_id_cut"),
            # ("id_tau_vsJet_{wp_vs_jet}_3>0.5".format(wp_vs_jet=wp_vs_jet), "tau_iso"),
            ("nbtag<0.5", "b_veto"),
        ]
        if wp_vs_jet == "VTight":
            cuts.append(
                (
                    "id_tau_vsJet_{wp_vs_jet}_3>0.5".format(wp_vs_jet=wp_vs_jet),
                    "tau_iso",
                )
            )
        else:
            cuts.append(
                (
                    "id_tau_vsJet_{wp_vs_jet}_3>0.5 && id_tau_vsJet_VTight_3<0.5".format(
                        wp_vs_jet=wp_vs_jet
                    ),
                    "tau_iso",
                )
            )
    # jet to electron fakerate
    elif channel == "mme":
        # base
        cuts = [
            ("q_1*q_2<0.0", "os"),
            ("pt_2>10", "pt_2_cut"),
            ("iso_1<0.15", "iso_1"),
            ("iso_2<0.15", "iso_2"),
            (
                "(((trg_single_mu27 == 1) || (trg_single_mu24 == 1)) && pt_1 > 25)",
                "trg_selection",
            ),
            ("mt_3<40", "mt_cut"),
            ("muon_is_mediumid_1 > 0.5 && muon_is_mediumid_2 > 0.5", "muon_id_cut"),
            ("nbtag<0.5", "b_veto"),
            # ("electron_is_nonisowp90_3>0.5", "ele_id_cut"),
        ]
        # tight
        if id_wp_ele == "Tight":
            cuts.append(("iso_3<0.15", "iso_3"))
            cuts.append(("electron_is_nonisowp90_3>0.5", "ele_id_cut"))
        else:
            cuts.append(("iso_3>0.15 || electron_is_nonisowp90_3<0.5", "id_iso_3"))
    # jet to muon fakerate
    elif channel == "eem":
        # base
        cuts = [
            ("q_1*q_2<0.0", "os"),
            ("pt_2>10", "pt_2_cut"),
            ("iso_1<0.15", "iso_1"),
            ("iso_2<0.15", "iso_2"),
            (
                "((trg_single_ele32 == 1) || (trg_single_ele35 == 1)) && pt_1>33",
                "trg_selection",
            ),
            ("mt_3<40", "mt_cut"),
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
            cuts.append(("iso_3>0.15 || muon_is_mediumid_3<0.5", "id_iso_3"))
    return Selection(name="{ch}".format(ch=channel), cuts=cuts)
