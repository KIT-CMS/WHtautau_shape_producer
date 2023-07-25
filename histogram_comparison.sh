source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh
CHANNELS="emt met mmt"
for CHANNEL in ${CHANNELS}
do
    INPUT_DATA="output/shapes/27_01_all_ch/${CHANNEL}/control_region_newfakes_xsec.root"
    INPUT_MC="output/shapes/27_01_all_ch/${CHANNEL}/control_region_jetfakes_closure_test.root"
    OUTPUT="plots/27_01_all_ch/${CHANNEL}/control_region_jetfakes_closure_test/Run2018_plots_fully_classic/${CHANNEL}/"
    python histogram_comparison.py --data ${INPUT_DATA} --mc ${INPUT_MC} --plot_output ${OUTPUT} --channel ${CHANNEL}
done