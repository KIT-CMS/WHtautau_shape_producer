#jetfake calculation and json 
#source utils/setup_root.sh
#source /cvmfs/sft.cern.ch/lcg/views/LCG_102/x86_64-centos7-gcc11-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_98python3/x86_64-centos7-gcc9-opt/setup.sh
NTUPLE_TAG=$1
ERA=$2
DATE=$3
# #jet to tau fakerates
INPUT_FILE="output/shapes/${NTUPLE_TAG}/${ERA}/mmt/fakerate_measurement_${DATE}/VTightvsJets"
OUTPUT_FILE="friends/${ERA}/jetfakes_lib_tau_${NTUPLE_TAG}_VTightvsJets_${DATE}.json"
PLOT_OUTPUT="plots/${NTUPLE_TAG}/${ERA}/jet_to_tau_fakerates_VTightvsJets_${DATE}"
# unc in %
SYST_UNC=10
WP_VS_JET="VTight"
WP_VS_MU="Tight,VLoose"
WP_VS_ELE="Tight,VLoose"
mkdir -p ${PLOT_OUTPUT}
mkdir -p friends/${ERA}/

python friends/jet_to_tau_fakerate_calculation.py --base_path ${INPUT_FILE} --output_file ${OUTPUT_FILE} --plot_output ${PLOT_OUTPUT} --syst_unc ${SYST_UNC} --wp_vs_jets ${WP_VS_JET} --wp_vs_mu ${WP_VS_MU} --wp_vs_ele ${WP_VS_ELE} 

# jet to mu fakerates
INPUT_FILE="output/shapes/${NTUPLE_TAG}/${ERA}/eem/fakerate_measurement_${DATE}"
OUTPUT_FILE="friends/${ERA}/jetfakes_lib_mu_${NTUPLE_TAG}_${DATE}.json"
PLOT_OUTPUT="plots/${NTUPLE_TAG}/${ERA}/jet_to_mu_fakerates_${DATE}"
mkdir -p ${PLOT_OUTPUT}
python friends/jet_to_mu_fakerate_calculation.py --base_path ${INPUT_FILE} --output_file ${OUTPUT_FILE} --plot_output ${PLOT_OUTPUT} --syst_unc ${SYST_UNC}

# #jet to ele fakerates
INPUT_FILE="output/shapes/${NTUPLE_TAG}/${ERA}/mme/fakerate_measurement_${DATE}"
OUTPUT_FILE="friends/${ERA}/jetfakes_lib_ele_${NTUPLE_TAG}_${DATE}.json"
PLOT_OUTPUT="plots/${NTUPLE_TAG}/${ERA}/jet_to_ele_fakerates_${DATE}"
mkdir -p ${PLOT_OUTPUT}
python friends/jet_to_ele_fakerate_calculation.py --base_path ${INPUT_FILE} --output_file ${OUTPUT_FILE} --plot_output ${PLOT_OUTPUT} --syst_unc ${SYST_UNC}
