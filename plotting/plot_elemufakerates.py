import json
import matplotlib

matplotlib.use("Agg")  # Avoid GUI issues
import matplotlib.pyplot as plt


def extract_data(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    content = data["corrections"][0]["data"]["content"]
    tight_entry = next(item for item in content if item["key"] == "Tight")["value"]

    pt_edges = tight_entry["edges"]
    pt_centers = [(pt_edges[i] + pt_edges[i + 1]) / 2 for i in range(len(pt_edges) - 1)]

    nom_vals = []
    stat_errs = []

    for bin_data in tight_entry["content"]:
        syst_data = {entry["key"]: entry["value"] for entry in bin_data["content"]}
        nom = syst_data.get("nom")
        stat_up = syst_data.get("stat_up")
        stat_down = syst_data.get("stat_down")

        if nom is not None and stat_up is not None and stat_down is not None:
            nom_vals.append(nom)
            stat_errs.append(abs(stat_up - stat_down) / 2)
        else:
            nom_vals.append(None)
            stat_errs.append(0)

    return pt_centers, nom_vals, stat_errs


def compare_two_jsons(json1_path, json2_path):
    pt1, nom1, err1 = extract_data(json1_path)
    pt2, nom2, err2 = extract_data(json2_path)

    plt.figure(figsize=(6, 6))

    plt.errorbar(
        pt1,
        nom1,
        yerr=err1,
        fmt="o",
        capsize=0,
        elinewidth=1.5,
        linestyle="None",
        color="#2f5061",
        marker="o",
        label=r"jet$\to\mu$",
    )

    plt.errorbar(
        pt2,
        nom2,
        yerr=err2,
        fmt="s",
        capsize=0,
        elinewidth=1.5,
        linestyle="None",
        color="#db1f48",
        marker="o",
        label=r"jet$\to$e",
    )

    plt.xlabel(r"$\ell-p_{\mathrm{T}}$ (GeV)")
    plt.ylabel(r"$F_{\mathrm{F}}^{\ell}$")
    # plt.title("Muon Fake Rate Comparison")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("muon_fakerate_comparison_2016postVFP.pdf")
    print("Plot saved as muon_fakerate_comparison.png")


# Example usage:
compare_two_jsons(
    "friends/2016postVFP/jetfakes_lib_mu_26_02_25_ff_27_02_25_MediumvsJetsvsL.json",
    "friends/2016postVFP/jetfakes_lib_ele_26_02_25_ff_27_02_25_MediumvsJetsvsL.json",
)
