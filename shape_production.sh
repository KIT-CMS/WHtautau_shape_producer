#shape production to plots
source utils/setup_root.sh

NTUPLE_TAG="11_08_emb_sf_17_18"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FRIEND_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends"
#FRIEND_PATH="/store/user/rschmieder/CROWN/ntuples/2017__26_07_all_ch/CROWNFriends"
CHANNELS="met mmt"
SHAPE_TAG="ptW_AN_binning"
ERA="2018"
REGIONS="control"
#shape production
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
            python shapes/produce_shapes.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection ${FRIEND_PATH}/jetfakes_incl_bveto_ortho_det_reg_AN_binning_unc --control-plot-set pt_W,m_tt,m_vis,pt_1,pt_2,pt_3,met --region ${REGION} --xrootd --skip-systematic-variations 
            # # # #jetfakes estimation
            bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 
        else
            python shapes/produce_shapes.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection ${FRIEND_PATH}/jetfakes_incl_bveto_ortho_det_reg_AN_binning_unc --control-plot-set pt_W,m_tt --region ${REGION} --xrootd
            # # # #jetfakes estimation
            bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 
            #synced shapes for fit
            bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${OUTPUT_FILE}.root ${REGION}
        fi
    done
    if ! [ $REGION == "control" ]; then
        OUTFILE=output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/${ERA}_${CHANNEL}_synced.root
        echo "[INFO] Adding written files to single output file $OUTFILE..."
        hadd -f $OUTFILE output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*.root
    fi
done


