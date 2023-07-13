source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh
CHANNELS="emt met mmt"
NAME="control_region_jetfakes_incl_bveto_ortho_det_reg_AN_binning"
for CHANNEL in ${CHANNELS}
do
    INPUT="output/shapes/27_01_all_ch/${CHANNEL}/${NAME}.root"
    OUTPUT="plots/27_01_all_ch/${CHANNEL}/${NAME}/Run2018_plots_fully_classic/${CHANNEL}/"
    python jetfake_contributions.py --input ${INPUT} --plot_output ${OUTPUT} --channel ${CHANNEL}
done