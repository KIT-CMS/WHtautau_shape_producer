from ntuple_processor import Histogram
import numpy as np


minimal_control_plot_set = [
    "pt_1",
    "pt_2",
    "pt_3",
    "eta_1",
    "eta_2",
    "eta_3",
    "m_vis",
    "pt_vis",
    "jpt_1",
    "jpt_2",
    "jeta_1",
    "jeta_2",
    "pfmet",
    "DeltaR_elemu_wh",
    "DeltaR_eletau_wh",
    "DeltaR_mutau_wh",
    "njets",
    "nbtag",
    # "jdeta",
    "met",
    "mjj",
    "gen_pt_1",
    "gen_pt_2",
    "gen_pt_3",
    "genbosonmass",
    "Lt",
    "decaymode_3",
    "m_tt",
    "pt_W",
]

binning_llt = {
    "pt_W": Histogram("pt_W", "pt_W", [0, 225]),
    # "pt_W": Histogram("pt_W", "pt_W", np.arange(0, 220, 20)),
    "m_tt": Histogram("m_tt", "m_tt", np.arange(0, 220, 20)),
    "phi_2": Histogram("phi_2", "phi_2", np.linspace(-3.14, 3.14, 10)),
    "genbosonpt": Histogram("genbosonpt", "genbosonpt", np.arange(0, 150, 10)),
    "deltaR_ditaupair": Histogram("DiTauDeltaR", "DiTauDeltaR", np.arange(0, 5, 0.2)),
    "mTdileptonMET_puppi": Histogram(
        "mTdileptonMET_puppi", "mTdileptonMET_puppi", np.arange(0, 200, 4)
    ),
    "pzetamissvis": Histogram("pzetamissvis", "pzetamissvis", np.arange(-200, 200, 5)),
    "pzetamissvis_pf": Histogram(
        "pzetamissvis_pf", "pzetamissvis_pf", np.arange(-200, 200, 5)
    ),
    "m_sv_puppi": Histogram("m_sv_puppi", "m_sv_puppi", np.arange(0, 225, 5)),
    "pt_sv_puppi": Histogram("pt_sv_puppi", "pt_sv_puppi", np.arange(0, 160, 5)),
    "eta_sv_puppi": Histogram(
        "eta_sv_puppi", "eta_sv_puppi", np.linspace(-2.5, 2.5, 50)
    ),
    "m_vis": Histogram("m_vis", "m_vis", np.arange(15, 200, 20)),
    "pt_vis": Histogram("pt_vis", "pt_vis", np.arange(15, 200, 20)),
    "ME_q2v1": Histogram("ME_q2v1", "ME_q2v1", np.arange(0, 300000, 6000)),
    "ME_q2v2": Histogram("ME_q2v1", "ME_q2v1", np.arange(0, 300000, 6000)),
    "ME_costheta1": Histogram("ME_costheta1", "ME_costheta1", np.linspace(-1, 1, 50)),
    "ME_costheta2": Histogram("ME_costheta2", "ME_costheta2", np.linspace(-1, 1, 50)),
    "ME_costhetastar": Histogram(
        "ME_costhetastar", "ME_costhetastar", np.linspace(-1, 1, 50)
    ),
    "ME_phi": Histogram("ME_phi", "ME_phi", np.linspace(-3.14, 3.14, 50)),
    "ME_phi1": Histogram("ME_phi1", "ME_phi1", np.linspace(-3.14, 3.14, 50)),
    "pfmetphi": Histogram("pfmetphi", "pfmetphi", np.linspace(-3.14, 3.14, 50)),
    "metphi": Histogram("metphi", "metphi", np.linspace(-3.14, 3.14, 50)),
    "pfmetphi_uncorrected": Histogram(
        "pfmetphi_uncorrected", "pfmetphi_uncorrected", np.linspace(-3.14, 3.14, 50)
    ),
    "metphi_uncorrected": Histogram(
        "metphi_uncorrected", "metphi_uncorrected", np.linspace(-3.14, 3.14, 50)
    ),
    "mt_tot": Histogram("mt_tot", "mt_tot", np.arange(0, 400, 8)),
    "mt_tot_puppi": Histogram("mt_tot_puppi", "mt_tot_puppi", np.arange(0, 400, 8)),
    "pt_1": Histogram("pt_1", "pt_1", np.arange(15, 200, 20)),
    "pt_2": Histogram("pt_2", "pt_2", np.arange(15, 200, 20)),
    "pt_3": Histogram("pt_3", "pt_3", np.arange(20, 200, 20)),
    # "pt_3": Histogram("pt_3", "pt_3", [20, 25, 30, 35, 40, 50, 60, 120]),
    "Lt": Histogram("Lt", "Lt", np.arange(0, 100, 5)),
    "eta_1": Histogram("eta_1", "eta_1", np.linspace(-2.5, 2.5, 5)),
    "eta_2": Histogram("eta_2", "eta_2", np.linspace(-2.5, 2.5, 5)),
    "eta_3": Histogram("eta_3", "eta_3", np.linspace(-2.5, 2.5, 5)),
    "jpt_1": Histogram(
        "jpt_1", "jpt_1", np.append(np.array([0]), np.arange(20, 160, 5))
    ),
    "jpt_2": Histogram(
        "jpt_2", "jpt_2", np.append(np.array([0]), np.arange(20, 160, 5))
    ),
    "jeta_1": Histogram("jeta_1", "jeta_1", np.linspace(-5, 5, 50)),
    "jeta_2": Histogram("jeta_2", "jeta_2", np.linspace(-5, 5, 50)),
    "jphi_1": Histogram("jphi_1", "jphi_1", np.linspace(-3.14, 3.14, 50)),
    "jphi_2": Histogram("jphi_2", "jphi_2", np.linspace(-3.14, 3.14, 50)),
    "jdeta": Histogram("jdeta", "jdeta", np.arange(0, 6, 0.2)),
    "njets": Histogram("njets", "njets", [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]),
    "nbtag": Histogram("nbtag", "nbtag", [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]),
    "decayMode_1": Histogram(
        "decayMode_1",
        "decayMode_1",
        [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5],
    ),
    "decayMode_2": Histogram(
        "decayMode_2",
        "decayMode_2",
        [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5],
    ),
    "rho": Histogram("rho", "rho", np.arange(0, 100, 2)),
    "m_1": Histogram("m_1", "m_1", np.linspace(0, 3, 50)),
    "m_2": Histogram("m_2", "m_2", np.linspace(0, 3, 50)),
    "mt_1": Histogram("mt_1", "mt_1", np.arange(0, 160, 5)),
    "mt_2": Histogram("mt_2", "mt_2", np.arange(0, 160, 5)),
    "mt_3": Histogram("mt_3", "mt_3", np.arange(0, 160, 10)),
    "mt_1_pf": Histogram("mt_1_pf", "mt_1_pf", np.arange(0, 160, 5)),
    "mt_2_pf": Histogram("mt_2_pf", "mt_2_pf", np.arange(0, 160, 5)),
    "ptvis": Histogram("ptvis", "ptvis", np.arange(0, 160, 5)),
    "pt_tt": Histogram("pt_tt", "pt_tt", np.arange(0, 160, 5)),
    "pt_tt_pf": Histogram("pt_tt_pf", "pt_tt_pf", np.arange(0, 160, 5)),
    "pt_ttjj": Histogram("pt_ttjj", "pt_ttjj", np.arange(0, 160, 5)),
    "mjj": Histogram("mjj", "mjj", np.arange(0, 300, 10)),
    "met": Histogram("met", "met", np.arange(0, 200, 10)),
    "pfmet": Histogram("pfmet", "pfmet", np.arange(0, 160, 10)),
    "met_uncorrected": Histogram(
        "met_uncorrected", "met_uncorrected", np.arange(0, 160, 10)
    ),
    "pfmet_uncorrected": Histogram(
        "pfmet_uncorrected", "pfmet_uncorrected", np.arange(0, 160, 10)
    ),
    "iso_1": Histogram("iso_1", "iso_1", np.linspace(0, 0.3, 50)),
    "iso_2": Histogram("iso_2", "iso_2", np.linspace(0, 1.0, 20)),
    "bpt_1": Histogram("bpt_1", "bpt_1", np.arange(0, 160, 5)),
    "bpt_2": Histogram("bpt_2", "bpt_2", np.arange(0, 160, 5)),
    "beta_1": Histogram("beta_1", "beta_1", np.linspace(-5, 5, 20)),
    "beta_2": Histogram("beta_2", "beta_2", np.linspace(-5, 5, 20)),
    # fastmtt variables
    "m_fastmtt": Histogram("m_fastmtt", "m_fastmtt", np.arange(0, 225, 5)),
    "pt_fastmtt": Histogram("pt_fastmtt", "pt_fastmtt", np.arange(0, 160, 5)),
    "eta_fastmtt": Histogram("eta_fastmtt", "eta_fastmtt", np.linspace(-2.5, 2.5, 50)),
    "phi_fastmtt": Histogram(
        "phi_fastmtt", "phi_fastmtt", np.linspace(-3.14, 3.14, 50)
    ),
}
binning_ltt = {
    "pt_W": Histogram("pt_W", "pt_W", [0, 225]),
    "m_tt": Histogram("m_tt", "m_tt", np.arange(0, 220, 20)),
    "phi_2": Histogram("phi_2", "phi_2", np.linspace(-3.14, 3.14, 10)),
    "genbosonpt": Histogram("genbosonpt", "genbosonpt", np.arange(0, 150, 10)),
    "deltaR_ditaupair": Histogram("DiTauDeltaR", "DiTauDeltaR", np.arange(0, 5, 0.2)),
    "mTdileptonMET_puppi": Histogram(
        "mTdileptonMET_puppi", "mTdileptonMET_puppi", np.arange(0, 200, 4)
    ),
    "pzetamissvis": Histogram("pzetamissvis", "pzetamissvis", np.arange(-200, 200, 5)),
    "pzetamissvis_pf": Histogram(
        "pzetamissvis_pf", "pzetamissvis_pf", np.arange(-200, 200, 5)
    ),
    "m_sv_puppi": Histogram("m_sv_puppi", "m_sv_puppi", np.arange(0, 225, 5)),
    "pt_sv_puppi": Histogram("pt_sv_puppi", "pt_sv_puppi", np.arange(0, 160, 5)),
    "eta_sv_puppi": Histogram(
        "eta_sv_puppi", "eta_sv_puppi", np.linspace(-2.5, 2.5, 50)
    ),
    "m_vis": Histogram("m_vis", "m_vis", np.arange(15, 200, 20)),
    "pt_vis": Histogram("pt_vis", "pt_vis", np.arange(15, 200, 20)),
    "ME_q2v1": Histogram("ME_q2v1", "ME_q2v1", np.arange(0, 300000, 6000)),
    "ME_q2v2": Histogram("ME_q2v1", "ME_q2v1", np.arange(0, 300000, 6000)),
    "ME_costheta1": Histogram("ME_costheta1", "ME_costheta1", np.linspace(-1, 1, 50)),
    "ME_costheta2": Histogram("ME_costheta2", "ME_costheta2", np.linspace(-1, 1, 50)),
    "ME_costhetastar": Histogram(
        "ME_costhetastar", "ME_costhetastar", np.linspace(-1, 1, 50)
    ),
    "ME_phi": Histogram("ME_phi", "ME_phi", np.linspace(-3.14, 3.14, 50)),
    "ME_phi1": Histogram("ME_phi1", "ME_phi1", np.linspace(-3.14, 3.14, 50)),
    "pfmetphi": Histogram("pfmetphi", "pfmetphi", np.linspace(-3.14, 3.14, 50)),
    "metphi": Histogram("metphi", "metphi", np.linspace(-3.14, 3.14, 50)),
    "pfmetphi_uncorrected": Histogram(
        "pfmetphi_uncorrected", "pfmetphi_uncorrected", np.linspace(-3.14, 3.14, 50)
    ),
    "metphi_uncorrected": Histogram(
        "metphi_uncorrected", "metphi_uncorrected", np.linspace(-3.14, 3.14, 50)
    ),
    "mt_tot": Histogram("mt_tot", "mt_tot", np.arange(0, 400, 8)),
    "mt_tot_puppi": Histogram("mt_tot_puppi", "mt_tot_puppi", np.arange(0, 400, 8)),
    "pt_1": Histogram("pt_1", "pt_1", np.arange(15, 200, 20)),
    "pt_2": Histogram("pt_2", "pt_2", np.arange(15, 200, 20)),
    "pt_3": Histogram("pt_3", "pt_3", np.arange(20, 200, 20)),
    # "pt_3": Histogram("pt_3", "pt_3", [20, 25, 30, 35, 40, 50, 60, 120]),
    # "pt_3": Histogram("pt_3", "pt_3", np.arange(20, 200, 20)),
    "Lt": Histogram("Lt", "Lt", np.arange(0, 100, 5)),
    "eta_1": Histogram("eta_1", "eta_1", np.linspace(-2.5, 2.5, 50)),
    "eta_2": Histogram("eta_2", "eta_2", np.linspace(-2.5, 2.5, 50)),
    "eta_3": Histogram("eta_3", "eta_3", np.linspace(-2.5, 2.5, 50)),
    "jpt_1": Histogram(
        "jpt_1", "jpt_1", np.append(np.array([0]), np.arange(20, 160, 5))
    ),
    "jpt_2": Histogram(
        "jpt_2", "jpt_2", np.append(np.array([0]), np.arange(20, 160, 5))
    ),
    "jeta_1": Histogram("jeta_1", "jeta_1", np.linspace(-5, 5, 50)),
    "jeta_2": Histogram("jeta_2", "jeta_2", np.linspace(-5, 5, 50)),
    "jphi_1": Histogram("jphi_1", "jphi_1", np.linspace(-3.14, 3.14, 50)),
    "jphi_2": Histogram("jphi_2", "jphi_2", np.linspace(-3.14, 3.14, 50)),
    "jdeta": Histogram("jdeta", "jdeta", np.arange(0, 6, 0.2)),
    "njets": Histogram("njets", "njets", [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]),
    "nbtag": Histogram("nbtag", "nbtag", [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]),
    "decayMode_1": Histogram(
        "decayMode_1",
        "decayMode_1",
        [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5],
    ),
    "decayMode_2": Histogram(
        "decayMode_2",
        "decayMode_2",
        [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5],
    ),
    "rho": Histogram("rho", "rho", np.arange(0, 100, 2)),
    "m_1": Histogram("m_1", "m_1", np.linspace(0, 3, 50)),
    "m_2": Histogram("m_2", "m_2", np.linspace(0, 3, 50)),
    "mt_1": Histogram("mt_1", "mt_1", np.arange(0, 160, 5)),
    "mt_2": Histogram("mt_2", "mt_2", np.arange(0, 160, 5)),
    "mt_3": Histogram("mt_3", "mt_3", np.arange(0, 160, 10)),
    "mt_1_pf": Histogram("mt_1_pf", "mt_1_pf", np.arange(0, 160, 5)),
    "mt_2_pf": Histogram("mt_2_pf", "mt_2_pf", np.arange(0, 160, 5)),
    "ptvis": Histogram("ptvis", "ptvis", np.arange(0, 160, 5)),
    "pt_tt": Histogram("pt_tt", "pt_tt", np.arange(0, 160, 5)),
    "pt_tt_pf": Histogram("pt_tt_pf", "pt_tt_pf", np.arange(0, 160, 5)),
    "pt_ttjj": Histogram("pt_ttjj", "pt_ttjj", np.arange(0, 160, 5)),
    "mjj": Histogram("mjj", "mjj", np.arange(0, 300, 10)),
    "met": Histogram("met", "met", np.arange(0, 200, 20)),
    "pfmet": Histogram("pfmet", "pfmet", np.arange(0, 160, 10)),
    "met_uncorrected": Histogram(
        "met_uncorrected", "met_uncorrected", np.arange(0, 160, 10)
    ),
    "pfmet_uncorrected": Histogram(
        "pfmet_uncorrected", "pfmet_uncorrected", np.arange(0, 160, 10)
    ),
    "iso_1": Histogram("iso_1", "iso_1", np.linspace(0, 0.3, 50)),
    "iso_2": Histogram("iso_2", "iso_2", np.linspace(0, 1.0, 50)),
    "bpt_1": Histogram("bpt_1", "bpt_1", np.arange(0, 160, 5)),
    "bpt_2": Histogram("bpt_2", "bpt_2", np.arange(0, 160, 5)),
    "beta_1": Histogram("beta_1", "beta_1", np.linspace(-5, 5, 20)),
    "beta_2": Histogram("beta_2", "beta_2", np.linspace(-5, 5, 20)),
    # fastmtt variables
    "m_fastmtt": Histogram("m_fastmtt", "m_fastmtt", np.arange(0, 225, 5)),
    "pt_fastmtt": Histogram("pt_fastmtt", "pt_fastmtt", np.arange(0, 160, 5)),
    "eta_fastmtt": Histogram("eta_fastmtt", "eta_fastmtt", np.linspace(-2.5, 2.5, 50)),
    "phi_fastmtt": Histogram(
        "phi_fastmtt", "phi_fastmtt", np.linspace(-3.14, 3.14, 50)
    ),
}
eem_mme_binning = {
    "pt_W": Histogram("pt_W", "pt_W", np.arange(0, 200, 10)),
    "m_tt": Histogram("m_tt", "m_tt", np.arange(0, 200, 10)),
    "pt_W_tt": Histogram("pt_W_tt", "pt_W_tt", np.arange(0, 200, 10)),
    "m_tt_tt": Histogram("m_tt_tt", "m_tt_tt", np.arange(0, 200, 10)),
    "phi_2": Histogram("phi_2", "phi_2", np.linspace(-3.14, 3.14, 10)),
    "genbosonpt": Histogram("genbosonpt", "genbosonpt", np.arange(0, 150, 10)),
    "deltaR_ditaupair": Histogram("DiTauDeltaR", "DiTauDeltaR", np.arange(0, 5, 0.2)),
    "mTdileptonMET_puppi": Histogram(
        "mTdileptonMET_puppi", "mTdileptonMET_puppi", np.arange(0, 200, 4)
    ),
    "pzetamissvis": Histogram("pzetamissvis", "pzetamissvis", np.arange(-200, 200, 5)),
    "pzetamissvis_pf": Histogram(
        "pzetamissvis_pf", "pzetamissvis_pf", np.arange(-200, 200, 5)
    ),
    "m_sv_puppi": Histogram("m_sv_puppi", "m_sv_puppi", np.arange(0, 225, 5)),
    "pt_sv_puppi": Histogram("pt_sv_puppi", "pt_sv_puppi", np.arange(0, 160, 5)),
    "eta_sv_puppi": Histogram(
        "eta_sv_puppi", "eta_sv_puppi", np.linspace(-2.5, 2.5, 50)
    ),
    "m_vis": Histogram("m_vis", "m_vis", np.arange(0, 260, 5)),
    "pt_vis": Histogram("pt_vis", "pt_vis", np.arange(0, 260, 10)),
    "ME_q2v1": Histogram("ME_q2v1", "ME_q2v1", np.arange(0, 300000, 6000)),
    "ME_q2v2": Histogram("ME_q2v1", "ME_q2v1", np.arange(0, 300000, 6000)),
    "ME_costheta1": Histogram("ME_costheta1", "ME_costheta1", np.linspace(-1, 1, 50)),
    "ME_costheta2": Histogram("ME_costheta2", "ME_costheta2", np.linspace(-1, 1, 50)),
    "ME_costhetastar": Histogram(
        "ME_costhetastar", "ME_costhetastar", np.linspace(-1, 1, 50)
    ),
    "ME_phi": Histogram("ME_phi", "ME_phi", np.linspace(-3.14, 3.14, 50)),
    "ME_phi1": Histogram("ME_phi1", "ME_phi1", np.linspace(-3.14, 3.14, 50)),
    "pfmetphi": Histogram("pfmetphi", "pfmetphi", np.linspace(-3.14, 3.14, 50)),
    "metphi": Histogram("metphi", "metphi", np.linspace(-3.14, 3.14, 50)),
    "pfmetphi_uncorrected": Histogram(
        "pfmetphi_uncorrected", "pfmetphi_uncorrected", np.linspace(-3.14, 3.14, 50)
    ),
    "metphi_uncorrected": Histogram(
        "metphi_uncorrected", "metphi_uncorrected", np.linspace(-3.14, 3.14, 50)
    ),
    "mt_tot": Histogram("mt_tot", "mt_tot", np.arange(0, 400, 8)),
    "mt_tot_puppi": Histogram("mt_tot_puppi", "mt_tot_puppi", np.arange(0, 400, 8)),
    "pt_1": Histogram("pt_1", "pt_1", [20, 25, 30, 35, 40, 50, 60, 120]),
    "pt_2": Histogram("pt_2", "pt_2", [20, 25, 30, 35, 40, 50, 60, 120]),
    "pt_3": Histogram("pt_3", "pt_3", [15, 20, 30, 40, 60]),
    "Lt": Histogram("Lt", "Lt", np.arange(0, 100, 5)),
    "eta_1": Histogram("eta_1", "eta_1", np.linspace(-2.5, 2.5, 50)),
    "eta_2": Histogram("eta_2", "eta_2", np.linspace(-2.5, 2.5, 50)),
    "eta_3": Histogram("eta_3", "eta_3", np.linspace(-2.5, 2.5, 50)),
    "jpt_1": Histogram(
        "jpt_1", "jpt_1", np.append(np.array([0]), np.arange(20, 160, 5))
    ),
    "jpt_2": Histogram(
        "jpt_2", "jpt_2", np.append(np.array([0]), np.arange(20, 160, 5))
    ),
    "jeta_1": Histogram("jeta_1", "jeta_1", np.linspace(-5, 5, 50)),
    "jeta_2": Histogram("jeta_2", "jeta_2", np.linspace(-5, 5, 50)),
    "jphi_1": Histogram("jphi_1", "jphi_1", np.linspace(-3.14, 3.14, 50)),
    "jphi_2": Histogram("jphi_2", "jphi_2", np.linspace(-3.14, 3.14, 50)),
    "jdeta": Histogram("jdeta", "jdeta", np.arange(0, 6, 0.2)),
    "njets": Histogram("njets", "njets", [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]),
    "nbtag": Histogram("nbtag", "nbtag", [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]),
    "decayMode_1": Histogram(
        "decayMode_1",
        "decayMode_1",
        [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5],
    ),
    "decayMode_2": Histogram(
        "decayMode_2",
        "decayMode_2",
        [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5],
    ),
    "rho": Histogram("rho", "rho", np.arange(0, 100, 2)),
    "m_1": Histogram("m_1", "m_1", np.linspace(0, 3, 50)),
    "m_2": Histogram("m_2", "m_2", np.linspace(0, 3, 50)),
    "mt_1": Histogram("mt_1", "mt_1", np.arange(0, 160, 5)),
    "mt_2": Histogram("mt_2", "mt_2", np.arange(0, 160, 5)),
    "mt_3": Histogram("mt_3", "mt_3", np.arange(0, 160, 10)),
    "mt_1_pf": Histogram("mt_1_pf", "mt_1_pf", np.arange(0, 160, 5)),
    "mt_2_pf": Histogram("mt_2_pf", "mt_2_pf", np.arange(0, 160, 5)),
    "ptvis": Histogram("ptvis", "ptvis", np.arange(0, 160, 5)),
    "pt_tt": Histogram("pt_tt", "pt_tt", np.arange(0, 160, 5)),
    "pt_tt_pf": Histogram("pt_tt_pf", "pt_tt_pf", np.arange(0, 160, 5)),
    "pt_ttjj": Histogram("pt_ttjj", "pt_ttjj", np.arange(0, 160, 5)),
    "mjj": Histogram("mjj", "mjj", np.arange(0, 300, 10)),
    "met": Histogram("met", "met", np.arange(0, 160, 10)),
    "pfmet": Histogram("pfmet", "pfmet", np.arange(0, 160, 10)),
    "met_uncorrected": Histogram(
        "met_uncorrected", "met_uncorrected", np.arange(0, 160, 10)
    ),
    "pfmet_uncorrected": Histogram(
        "pfmet_uncorrected", "pfmet_uncorrected", np.arange(0, 160, 10)
    ),
    "iso_1": Histogram("iso_1", "iso_1", np.linspace(0, 0.3, 50)),
    "iso_2": Histogram("iso_2", "iso_2", np.linspace(0, 1.0, 50)),
    "bpt_1": Histogram("bpt_1", "bpt_1", np.arange(0, 160, 5)),
    "bpt_2": Histogram("bpt_2", "bpt_2", np.arange(0, 160, 5)),
    "beta_1": Histogram("beta_1", "beta_1", np.linspace(-5, 5, 20)),
    "beta_2": Histogram("beta_2", "beta_2", np.linspace(-5, 5, 20)),
    # fastmtt variables
    "m_fastmtt": Histogram("m_fastmtt", "m_fastmtt", np.arange(0, 225, 5)),
    "pt_fastmtt": Histogram("pt_fastmtt", "pt_fastmtt", np.arange(0, 160, 5)),
    "eta_fastmtt": Histogram("eta_fastmtt", "eta_fastmtt", np.linspace(-2.5, 2.5, 50)),
    "phi_fastmtt": Histogram(
        "phi_fastmtt", "phi_fastmtt", np.linspace(-3.14, 3.14, 50)
    ),
}
control_binning = {}
for channel in ["emt", "met", "mmt", "ett", "mtt", "eem", "mme"]:
    if channel in ["emt", "met", "mmt"]:
        control_binning[channel] = binning_llt
    elif channel in ["eem", "mme"]:
        control_binning[channel] = eem_mme_binning
    else:
        control_binning[channel] = binning_ltt
