import ROOT

for ch in ["ett", "mtt"]:
    for reg in ["lowpt", "midpt", "highpt"]:
        # for ch in ["mmt"]:
        print("----------")
        print(ch, reg)
        rfile = ROOT.TFile(
            "output/shapes/23_10_23_ett_mtt_shifts/2018/{ch}/yield_test_ssTight_ostight_correctptmetcut/sig_{reg}.root".format(
                ch=ch, reg=reg
            ),
            "READ",
        )
        data = rfile.Get("data#{ch}#Nominal#m_tt".format(ch=ch))
        # red = rfile.Get("jetFakes#{ch}-jetFakes#Nominal#m_tt".format(ch=ch))
        # zz = rfile.Get("ZZ#{ch}-VV#Nominal#m_tt".format(ch=ch))
        # ggzz = rfile.Get("ggZZ#{ch}-VV#Nominal#m_tt".format(ch=ch))
        # wz = rfile.Get("WZ#{ch}-VV#Nominal#m_tt".format(ch=ch))
        print("data", data.Integral())
        # print("reducibel", red.Integral())
        # print("zz", zz.Integral() + ggzz.Integral())
        # print("wz", wz.Integral())
