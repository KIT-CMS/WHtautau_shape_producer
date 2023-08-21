#jetfake calculation and json 
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

# #jet to tau fakerates
ERA="2018"
NTUPLE_TAG="27_01_all_ch"
#INPUT_FILE="output/shapes/${NTUPLE_TAG}/${ERA}/mmt/fakerate_measurement_incl_bveto_ortho_det_reg_AN_binning"
INPUT_FILE="output/shapes/${NTUPLE_TAG}/mmt/fakerate_measurement_incl_bveto_ortho_det_reg_AN_binning"
OUTPUT_FILE="friends/jetfakes_lib_tau_incl_bveto_ortho_det_reg_AN_binning_17_08.json"
PLOT_OUTPUT="plots/${NTUPLE_TAG}/${ERA}/jet_to_tau_fakerates_incl_bveto_ortho_det_reg_AN_binning_17_08"
SYST_UNC=10
mkdir -p ${PLOT_OUTPUT}
python friends/jet_to_tau_fakerate_calculation.py --base_path ${INPUT_FILE} --output_file ${OUTPUT_FILE} --plot_output ${PLOT_OUTPUT} --syst_unc ${SYST_UNC}


# #jet to mu fakerates
NTUPLE_TAG="09_02_eem_mme_2"
INPUT_FILE="output/shapes/${NTUPLE_TAG}/eem/fakerate_measurement_incl_bveto_ortho_det_reg"
OUTPUT_FILE="friends/jetfakes_lib_mu_incl_bveto_ortho_det_reg_2018_17_08.json"
PLOT_OUTPUT="plots/${NTUPLE_TAG}/${ERA}/jet_to_mu_incl_bveto_ortho_det_reg_2018_17_08"
mkdir -p ${PLOT_OUTPUT}
python friends/jet_to_mu_fakerate_calculation.py --base_path ${INPUT_FILE} --output_file ${OUTPUT_FILE} --plot_output ${PLOT_OUTPUT} --syst_unc ${SYST_UNC}

# #jet to ele fakerates
INPUT_FILE="output/shapes/${NTUPLE_TAG}/mme/fakerate_measurement_incl_bveto_ortho_det_reg"
OUTPUT_FILE="friends/jetfakes_lib_ele_incl_bveto_ortho_det_reg_2018_17_08.json"
PLOT_OUTPUT="plots/${NTUPLE_TAG}/${ERA}/jet_to_ele_fakerates_incl_bveto_ortho_det_reg_2018_17_08"
mkdir -p ${PLOT_OUTPUT}
python friends/jet_to_ele_fakerate_calculation.py --base_path ${INPUT_FILE} --output_file ${OUTPUT_FILE} --plot_output ${PLOT_OUTPUT} --syst_unc ${SYST_UNC}