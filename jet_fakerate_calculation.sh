#jetfake calculation and json 
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

# #jet to tau fakerates
INPUT_FILE="output/shapes/27_01_all_ch/mmt/fakerate_measurement2"
OUTPUT_FILE="friends/jetfakes_lib_tau.json"
PLOT_OUTPUT="plots/27_01_all_ch/jet_to_tau_fakerates"
mkdir -p ${PLOT_OUTPUT}
#python friends/jet_to_tau_fakerate.py --base_path ${INPUT_FILE} --output_file ${OUTPUT_FILE} --plot_output ${PLOT_OUTPUT}


#jet to mu fakerates
INPUT_FILE="output/shapes/09_02_eem_mme_2/eem/fakerate_measurement2"
OUTPUT_FILE="friends/jetfakes_lib_mu.json"
PLOT_OUTPUT="plots/09_02_eem_mme_2/jet_to_mu_fakerates"
mkdir -p ${PLOT_OUTPUT}
python friends/jet_to_mu_fakerate_calculation.py --base_path ${INPUT_FILE} --output_file ${OUTPUT_FILE} --plot_output ${PLOT_OUTPUT}

#jet to ele fakerates
INPUT_FILE="output/shapes/09_02_eem_mme_2/mme/fakerate_measurement2"
OUTPUT_FILE="friends/jetfakes_lib_ele.json"
PLOT_OUTPUT="plots/09_02_eem_mme_2/jet_to_ele_fakerates"
mkdir -p ${PLOT_OUTPUT}
python friends/jet_to_ele_fakerate_calculation.py --base_path ${INPUT_FILE} --output_file ${OUTPUT_FILE} --plot_output ${PLOT_OUTPUT}