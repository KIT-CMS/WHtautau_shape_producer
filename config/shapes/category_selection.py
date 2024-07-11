from ntuple_processor import Histogram
from ntuple_processor.utils import Selection
import logging
import yaml

m_sv_hist = Histogram("m_sv_puppi", "m_sv_puppi", [i for i in range(0, 255, 5)])
mt_tot_hist = Histogram("mt_tot_puppi", "mt_tot_puppi", [i for i in range(0, 3900, 10)])

fine_binning = [
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.0,
]
hist = Histogram("predicted_max_value", "predicted_max_value", fine_binning)
pt_1 = Histogram("pt_1", "pt_1", [20, 25, 30, 35, 40, 50, 60, 120])
pt_2 = Histogram("pt_2", "pt_2", [20, 21, 22, 23, 24, 25, 30, 35, 40, 50, 60, 120])
pt_3 = Histogram("pt_3", "pt_3", [20, 25, 30, 35, 40, 50, 60, 120])
met = Histogram("met", "met", [0, 10, 20, 30, 40, 50, 60, 120])
m_vis = Histogram(
    "m_vis",
    "m_vis",
    [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 140, 160, 180, 200],
)
iso_2 = Histogram(
    "iso_2",
    "iso_2",
    [
        0.0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
    ],
)
iso_1 = Histogram(
    "iso_1",
    "iso_1",
    [
        0.0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
    ],
)
njets = Histogram("njets", "njets", [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
eta_1 = Histogram("eta_1", "eta_1", [-2.5, -1.25, 0.0, 1.25, 2.5])
eta_2 = Histogram("eta_2", "eta_2", [-2.5, -1.25, 0.0, 1.25, 2.5])
eta_3 = Histogram("eta_3", "eta_3", [-2.5, -1.25, 0.0, 1.25, 2.5])
phi_2 = Histogram(
    "phi_2", "phi_2", [-3.14, -2.44, -1.74, -1.05, -0.35, 0.35, 1.05, 1.74, 2.44, 3.14]
)
phi_3 = Histogram(
    "phi_3", "phi_3", [-3.14, -2.44, -1.74, -1.05, -0.35, 0.35, 1.05, 1.74, 2.44, 3.14]
)
phi_1 = Histogram(
    "phi_1", "phi_1", [-3.14, -2.44, -1.74, -1.05, -0.35, 0.35, 1.05, 1.74, 2.44, 3.14]
)
deltaR_12 = Histogram(
    "deltaR_12",
    "deltaR_12",
    [
        0.0,
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
        1.2,
        1.4,
        1.6,
        1.8,
        2.0,
        2.2,
        2.4,
        2.6,
        2.8,
        3.0,
        3.2,
        3.4,
        3.6,
        3.8,
        4.0,
        4.2,
        4.4,
        4.6,
        4.8,
    ],
)
deltaR_13 = Histogram(
    "deltaR_13",
    "deltaR_13",
    [
        0.0,
        0.2,
        0.4,
        0.61,
        0.8,
        1.0,
        1.22,
        1.41,
        1.6,
        1.8,
        2.0,
        2.2,
        2.44,
        2.6,
        2.83,
        3.0,
        3.2,
        3.44,
        3.6,
        3.83,
        4.0,
        4.2,
        4.4,
        4.65,
        4.81,
    ],
)
deltaR_23 = Histogram(
    "deltaR_23",
    "deltaR_23",
    [
        0.0,
        0.01,
        0.02,
        0.03,
        0.04,
        0.05,
        0.1,
        0.15,
        0.2,
        0.4,
        0.61,
        0.8,
        1.0,
        1.22,
        1.41,
        1.6,
        1.8,
        2.0,
        2.2,
        2.44,
        2.6,
        2.83,
        3.0,
        3.2,
        3.44,
        3.6,
        3.83,
        4.0,
        4.2,
        4.4,
        4.65,
        4.81,
    ],
)
jpt_1 = Histogram("jpt_1", "jpt_1", [20, 25, 30, 35, 40, 50, 60, 120])
jpt_2 = Histogram("jpt_2", "jpt_2", [20, 25, 30, 35, 40, 50, 60, 120])


# classdict for NMSSM Index
def nn_cat(channel):
    classdict = {
        "sig": {"index": "0", "binning": fine_binning},
        "misc": {"index": "1", "binning": fine_binning},
        "diboson": {"index": "2", "binning": fine_binning},
    }
    nn_categorization = {"{ch}".format(ch=channel): []}
    catsL_ = nn_categorization["{ch}".format(ch=channel)]
    for category in classdict.keys():
        catsL_.append(
            (
                Selection(
                    name="{lab}".format(lab=category),
                    cuts=[
                        (
                            "predicted_class=={index}".format(
                                index=classdict[category]["index"]
                            ),
                            "category_selection",
                        )
                    ],
                ),
                [hist, deltaR_23, pt_2],
            )
        )
    nn_categorization = {"{ch}".format(ch=channel): catsL_}
    print(nn_categorization)
    return nn_categorization
    #   [
    #         hist,
    #         m_vis,
    #         met,
    #         pt_1,
    #         pt_2,
    #         pt_3,
    #         eta_1,
    #         eta_2,
    #         eta_3,
    #         deltaR_12,
    #         deltaR_13,
    #         deltaR_23,
    #         njets,
    #         phi_1,
    #         phi_2,
    #         phi_3,
    #         jpt_1,
    #         jpt_2,
    #     ],
