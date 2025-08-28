import ROOT


def plot_2DFC():
    # Open ROOT file
    file0 = ROOT.TFile.Open(
        "CA_FC_10_05_25_nn_fitshapes_CA_RD2_CAwithZH_1000toys/FeldmanCousins.root"
    )

    # Create canvas
    can = ROOT.TCanvas("c", "c", 600, 540)

    # Get the 2D graph
    gpX = file0.Get("obs")
    gpX.Draw("colz")

    # Clone the histogram from the graph
    h68 = gpX.GetHistogram().Clone("h95")
    h68.SetContour(2)
    h68.SetContourLevel(1, 0.05)
    h68.SetLineWidth(3)
    h68.SetLineColor(1)
    h68.Draw("CONT3same")

    # Set axis titles
    gpX.SetTitle("")
    gpX.GetXaxis().SetTitle("r_A")
    gpX.GetYaxis().SetTitle("r_ZH")

    # Turn off stats box
    ROOT.gStyle.SetOptStat(0)

    # Save canvas
    can.SaveAs("CA_FC_10_05_25_nn_fitshapes_CA_RD2_CAwithZH_1000toys/2D_FC.png")


# Call the function
plot_2DFC()
