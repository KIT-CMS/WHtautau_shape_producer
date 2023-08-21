source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh
ERA="2017"
CHANNELS="ett mtt emt met mmt"
NTUPLE_TAG="2017__07_08_all_ch_shifts"
SHAPE_TAG="ptW_AN_binning"
INPUT="output/datacard_output/${NTUPLE_TAG}/${SHAPE_TAG}/2017_all/cmb/postfitshape.root"
for CHANNEL in $CHANNELS
do
    for CAT in pt_W_plus m_tt_plus pt_W_minus m_tt_minus
    do
        OUTPUT=plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}
        python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} --prefit 
        python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} 
    done
done
