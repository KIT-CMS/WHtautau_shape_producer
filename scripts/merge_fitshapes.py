import ROOT
import os
from collections import defaultdict

# Configuration
years = ["2016preVFP", "2016postVFP", "2017", "2018"]
final_states = ["llt", "ltt"]
base_categories = [1, 2, 3, 4, 5, 6]
fit_stage = "prefit"
merge_mode = "all_years"  # Options: "all_years", "all_final_states", "all"
# Add combined categories
category_map = {7: [3, 4], 8: [5, 6]}

all_categories = base_categories + list(category_map.keys())
# Template to locate input files

input_path_template = "output/datacard_output/14_04_25_alleras_allch3/19_05_25_nn_fitshapes_coarsebinning_CA_AS/{year}_{final_state}/cmb/{fit_stage}shape.root"

# Output file
if merge_mode == "all":
    output_file = ROOT.TFile(
        f"output/datacard_output/14_04_25_alleras_allch3/19_05_25_nn_fitshapes_coarsebinning_CA_AS/all_eras_all/cmb/{fit_stage}shape.root",
        "RECREATE",
    )


def accumulate_histograms(hist_dict, hist_name, hist_obj):
    """Add or clone histogram into dict"""
    if hist_name not in hist_dict:
        hist_dict[hist_name] = hist_obj.Clone()
        hist_dict[hist_name].SetDirectory(0)
    else:
        hist_dict[hist_name].Add(hist_obj)


# Main logic
if merge_mode == "all_years":
    for final_state in final_states:
        output_file = ROOT.TFile(
            f"output/datacard_output/14_04_25_alleras_allch3/19_05_25_nn_fitshapes_coarsebinning_CA_AS/all_eras_{final_state}/cmb/{fit_stage}shape.root",
            "RECREATE",
        )

        # First: process normal categories
        for category in base_categories:
            combined_name = f"htt_{final_state}_{category}_all_eras_{fit_stage}"
            output_file.mkdir(combined_name)
            output_dir = output_file.Get(combined_name)

            histograms = {}

            for year in years:
                file_path = input_path_template.format(
                    final_state=final_state, year=year, fit_stage=fit_stage
                )
                if not os.path.exists(file_path):
                    print(f"Missing file: {file_path}")
                    continue

                f = ROOT.TFile.Open(file_path)
                folder_name = f"htt_{final_state}_{category}_{year}_{fit_stage}"
                folder = f.Get(folder_name)
                if not folder:
                    print(f"Missing folder: {folder_name}")
                    continue

                for key in folder.GetListOfKeys():
                    obj = key.ReadObj()
                    if isinstance(obj, ROOT.TH1):
                        accumulate_histograms(histograms, obj.GetName(), obj)

                f.Close()

            output_dir.cd()
            for hist in histograms.values():
                hist.Write()

        # Then: process merged virtual categories 7 and 8
        for virtual_cat, input_cats in category_map.items():
            combined_name = f"htt_{final_state}_{virtual_cat}_all_eras_{fit_stage}"
            output_file.mkdir(combined_name)
            output_dir = output_file.Get(combined_name)

            histograms = {}

            for year in years:
                file_path = input_path_template.format(
                    final_state=final_state, year=year, fit_stage=fit_stage
                )
                if not os.path.exists(file_path):
                    print(f"Missing file: {file_path}")
                    continue

                f = ROOT.TFile.Open(file_path)

                for cat_in in input_cats:
                    folder_name = f"htt_{final_state}_{cat_in}_{year}_{fit_stage}"
                    folder = f.Get(folder_name)
                    if not folder:
                        print(f"Missing folder: {folder_name}")
                        continue

                    for key in folder.GetListOfKeys():
                        obj = key.ReadObj()
                        if isinstance(obj, ROOT.TH1):
                            accumulate_histograms(histograms, obj.GetName(), obj)

                f.Close()

            output_dir.cd()
            for hist in histograms.values():
                hist.Write()

        output_file.Close()


elif merge_mode == "all":
    for category in base_categories:
        input_categories = category_map.get(category, [category])
        combined_name = f"htt_all_{category}_all_eras_{fit_stage}"
        output_file.mkdir(combined_name)
        output_dir = output_file.Get(combined_name)

        histograms = {}

        for final_state in final_states:
            for year in years:
                file_path = input_path_template.format(
                    final_state=final_state, year=year, fit_stage=fit_stage
                )
                if not os.path.exists(file_path):
                    print(f"Missing file: {file_path}")
                    continue

                f = ROOT.TFile.Open(file_path)
                for cat_in in input_categories:
                    folder_name = f"htt_{final_state}_{cat_in}_{year}_{fit_stage}"
                    folder = f.Get(folder_name)
                    if not folder:
                        print(f"Missing folder: {folder_name}")
                        continue

                    for key in folder.GetListOfKeys():
                        obj = key.ReadObj()
                        if isinstance(obj, ROOT.TH1):
                            accumulate_histograms(histograms, obj.GetName(), obj)

                f.Close()

        output_dir.cd()
        for hist in histograms.values():
            hist.Write()
    for virtual_cat, input_cats in category_map.items():
        combined_name = f"htt_all_{virtual_cat}_all_eras_{fit_stage}"
        output_file.mkdir(combined_name)
        output_dir = output_file.Get(combined_name)

        histograms = {}

        for final_state in final_states:
            for year in years:
                file_path = input_path_template.format(
                    final_state=final_state, year=year, fit_stage=fit_stage
                )
                if not os.path.exists(file_path):
                    print(f"Missing file: {file_path}")
                    continue

                f = ROOT.TFile.Open(file_path)

                for cat_in in input_cats:
                    folder_name = f"htt_{final_state}_{cat_in}_{year}_{fit_stage}"
                    folder = f.Get(folder_name)
                    if not folder:
                        print(f"Missing folder: {folder_name}")
                        continue

                    for key in folder.GetListOfKeys():
                        obj = key.ReadObj()
                        if isinstance(obj, ROOT.TH1):
                            accumulate_histograms(histograms, obj.GetName(), obj)

                f.Close()

        output_dir.cd()
        for hist in histograms.values():
            hist.Write()

else:
    print(
        f"Invalid merge_mode: {merge_mode}. Choose from 'all_years', 'all_final_states', or 'all'."
    )

print("✅ Finished writing combined histograms.")
