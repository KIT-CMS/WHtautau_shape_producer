source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh
CHANNELS="emt met mmt"
NAME="fakerates_incl_bveto_ortho_det_reg"
for CHANNEL in ${CHANNELS}
do
    INPUT="output/shapes/27_01_all_ch/${CHANNEL}/control_region_${NAME}.root"
    OUTPUT="plots/27_01_all_ch/${CHANNEL}/control_region_${NAME}/Run2018_plots_fully_classic/${CHANNEL}/"
    python jetfake_contributions.py --input ${INPUT} --plot_output ${OUTPUT} --channel ${CHANNEL}
done