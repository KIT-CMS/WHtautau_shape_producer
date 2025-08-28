import json
import matplotlib

matplotlib.use("Agg")  # Use non-GUI backend to avoid Qt issues
import matplotlib.pyplot as plt


def extract_nom_and_errors(dm_content, dm_value):
    # Find the entry for the specified decay mode
    dm_entry = next((item for item in dm_content if item["key"] == dm_value), None)
    if not dm_entry:
        return None, None, None

    dm_data = dm_entry["value"]
    pt_edges = dm_data["edges"]
    pt_centers = [(pt_edges[i] + pt_edges[i + 1]) / 2 for i in range(len(pt_edges) - 1)]

    nom_values = []
    errors = []

    for bin_content in dm_data["content"]:
        syst_entries = {s["key"]: s["value"] for s in bin_content["content"]}
        nom = syst_entries.get("nom")
        stat_up = syst_entries.get("stat_up")
        stat_down = syst_entries.get("stat_down")

        if nom is not None and stat_up is not None and stat_down is not None:
            nom_values.append(nom)
            error = abs(stat_up - stat_down) / 2
            errors.append(error)
        else:
            nom_values.append(None)
            errors.append(0)

    return pt_centers, nom_values, errors


def plot_multiple_dms_with_errors(json_path, dm_list):
    with open(json_path, "r") as f:
        data = json.load(f)

    # Navigate to the dm category content
    dm_content = next(
        item
        for item in data["corrections"][0]["data"]["content"]
        if item["key"] == "Medium"
    )["value"]["content"]
    dm_content = next(item for item in dm_content if item["key"] == "Medium")["value"][
        "content"
    ]
    dm_content = next(item for item in dm_content if item["key"] == "Medium")["value"][
        "content"
    ]

    plt.figure(figsize=(6, 6))
    dm_colors = {0: "#4297a0", 1: "#db1f48", 10: "#e57f84", 11: "#2f5061"}
    for dm in dm_list:
        color = dm_colors[dm]
        pt, nom, err = extract_nom_and_errors(dm_content, dm)
        if pt and nom:
            plt.errorbar(
                pt,
                nom,
                yerr=err,
                fmt="o",
                capsize=0,
                elinewidth=1.5,
                label=f"DM={dm}",
                linestyle="None",
                color=color,
            )
        else:
            print(f"DM={dm} not found in JSON.")

    plt.xlabel(r"$\tau_{\mathrm{h}}-p_{\mathrm{T}}$ (GeV)")
    plt.ylabel(r"$F_{\mathrm{F}}^{\tau_{\mathrm{h}}}$")
    # plt.title("Jet→τ Fake Rate vs pT with Statistical Errors")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tau_fakerate_2018.pdf")
    print("Plot saved as fakerate_plot_with_errors.png")


# Example usage:
plot_multiple_dms_with_errors(
    "friends/2018/jetfakes_lib_tau_26_02_25_ff_MediumvsJets_27_02_25_MediumvsJetsvsL.json",
    [0, 1, 10, 11],
)
