#shape production to plots
source utils/setup_root.sh

NTUPLE_TAG="11_07_shifts_all_ch"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FRIEND_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FRIEND}/"
CHANNELS="mmt emt met mtt ett"
SHAPE_TAG="ptW_mtt"
FILENAME="signal_region"
ERA="2018"

#shape production
for CHANNEL in $CHANNELS
do
    OUTPUT_FILE="output/shapes/${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}/${FILENAME}"
    mkdir -p output/shapes/${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}
    python shapes/produce_shapes.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/xsec ${FRIEND_PATH}/jetfakes_incl_bveto_ortho_det_reg_AN_binning_unc --control-plot-set pt_W,m_tt --xrootd #--skip-systematic-variations#,m_vis,pt_1,pt_2,mjj,njets,pt_vis,phi_2,eta_2,nbtag #--process-selection wz,ggzz,zz,data,rem_vh,www,wzz,wwz,zzz,rem_ttbar

    # # #jetfakes estimation
    bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 

    #synced shapes for fit, remove all files in the synced shapes directory to have it clean, as the last step combines all root files in the directory
    rm -r output/shapes/${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}/synced_shapes
    bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${OUTPUT_FILE}.root
done


