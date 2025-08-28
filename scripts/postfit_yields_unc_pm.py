import ROOT
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Produce shapes for the legacy NMSSM analysis."
    )
    parser.add_argument("--input", required=True, type=str, help="Input ROOT file.")
    parser.add_argument("--era", required=True, type=str, help="Experiment era.")
    parser.add_argument("--channel", required=True, type=str, help="Analysis channel.")
    parser.add_argument("--tag", required=True, type=str, help="Experiment era.")
    return parser.parse_args()


def get_total_yield_and_error(file_name, dir_name, hist_names):
    """
    Compute total yield and error for a list of histograms.

    Args:
        file_name (str): Path to the ROOT file.
        dir_name (str): Name of the TDirectory.
        hist_names (list): List of histogram names to sum.

    Returns:
        tuple: (total yield, total error) if successful, otherwise (None, None).
    """
    root_file = ROOT.TFile.Open(file_name, "READ")
    if not root_file or root_file.IsZombie():
        print(f"Error: Could not open file {file_name}")
        return None, None

    directory = root_file.Get(dir_name)
    if not directory or not isinstance(directory, ROOT.TDirectory):
        print(f"Error: TDirectory {dir_name} not found in file {file_name}")
        root_file.Close()
        return None, None

    total_yield = 0.0
    total_error2 = 0.0  # Sum of squared errors

    for hist_name in hist_names:
        hist = directory.Get(hist_name)
        if not hist:
            print(
                f"Warning: Histogram {hist_name} not found in {dir_name}. Skipping..."
            )
            continue

        total_yield += hist.Integral()
        total_error2 += sum(
            hist.GetBinError(i) ** 2 for i in range(1, hist.GetNbinsX() + 1)
        )

    root_file.Close()
    return round(total_yield, 2), round(ROOT.TMath.Sqrt(total_error2), 2)


def generate_latex_table(results, channel, era):
    """
    Generate a LaTeX table from the extracted results.

    Args:
        results (dict): Dictionary containing the yield and error for each process.
        channel (str): The analysis channel.
        era (str): The experiment era.

    Returns:
        str: LaTeX table as a string.
    """
    process_dict = {
        "TotalBkg": "Bkg.",
        "Signal(+)": "Signal(+)",
        "Signal(-)": "Signal(-)",
        "data_obs": "Data",
    }

    table = """\
\\begin{table}[htbp]
    \\centering
    \\caption{Prefit yields in %s in the $%s$ channel.}
    \\label{tab:yields}
    \\begin{tabular}{lcccccc}
        \\hline
        \\hline
        Process & signal(+) & signal(-) & misc(+) & misc(-) & VV(+) & VV(-) \\\\
        \\hline
""" % (
        era,
        channel,
    )

    for key in results.keys():
        table += f"{process_dict[key]} "
        for i in range(1, 7):
            dir_key = f"htt_{channel}_{i}_{era}_prefit"
            yield_val = results[key][dir_key]["yield"]
            error_val = results[key][dir_key]["error"]
            table += f"& {yield_val} \\pm {error_val} "
        table += "\\\\ \n"

    table += """\
        \\hline
    \\end{tabular}
\\end{table}
"""
    return table


if __name__ == "__main__":
    args = parse_arguments()
    root_file_name = args.input
    era = args.era
    channel = args.channel
    tag = args.tag

    # Define directories and histogram names
    directories = [f"htt_{channel}_{i}_{era}_prefit" for i in range(1, 7)]
    histograms = {
        "TotalBkg": ["TotalBkg"],
        "data_obs": ["data_obs"],
        "Signal(+)": ["WH_htt_plus", "WH_hww_plus"],
        "Signal(-)": ["WH_htt_minus", "WH_hww_minus"],
    }

    results = {key: {dir_name: {} for dir_name in directories} for key in histograms}

    for dir_name in directories:
        for key, hist_list in histograms.items():
            yield_value, error_value = get_total_yield_and_error(
                root_file_name, dir_name, hist_list
            )
            results[key][dir_name] = {"yield": yield_value, "error": error_value}

            if yield_value is not None and error_value is not None:
                print(
                    f"Directory: {dir_name}, Process: {key}, Total Yield: {yield_value}, Total Error: {error_value}"
                )

    # Generate LaTeX table
    latex_table = generate_latex_table(results, channel, era)

    # Save LaTeX table to a file
    tex_filename = f"yield_unc_{era}_{channel}_{tag}.tex"
    with open(tex_filename, "w") as tex_file:
        tex_file.write(latex_table)

    print(f"LaTeX table saved to {tex_filename}")
