#shape production to plots
source utils/setup_root.sh

NTUPLE_TAG="21_08_23_all_ch_17_18_shifts"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FRIEND_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends"
CHANNELS="ett emt met mmt mtt"
SHAPE_TAG="six_ortho_regions"
ERAS="2017 2018"
REGIONS="control_plus_high_ptw control_plus_low_ptw control_minus_high_ptw control_minus_low_ptw sig_plus sig_minus"
#shape production
for ERA in $ERAS 
do 
for CHANNEL in $CHANNELS
do
    #remove all files in the synced shapes directory to have it clean, as the last step combines all root files in the directory
    rm -r output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes
    for REGION in $REGIONS
    do
        FILENAME="${REGION}"
        OUTPUT_FILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${FILENAME}"
        mkdir -p output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
        if [ $REGION == "control" ]; then
            python shapes/produce_shapes.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection ${FRIEND_PATH}/jetfakes_incl_bveto_ortho_det_reg_AN_binning_unc_emb_sfs_test --control-plot-set m_tt --region ${REGION} --xrootd #--skip-systematic-variations 
            # # # #jetfakes estimation
            bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 
            bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${OUTPUT_FILE}.root ${REGION}
        else
            #python shapes/produce_shapes.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection ${FRIEND_PATH}/jetfakes_incl_bveto_ortho_det_reg_AN_binning_unc_emb_sfs_test --control-plot-set m_tt --region ${REGION} --xrootd
            # # # #jetfakes estimation
            bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 
            #synced shapes for fit
            bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${OUTPUT_FILE}.root ${REGION}
        fi
    done
    OUTFILE=output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/${ERA}_${CHANNEL}_synced.root
    echo "[INFO] Adding written files to single output file $OUTFILE..."
    hadd -f $OUTFILE output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*.root
done
done


