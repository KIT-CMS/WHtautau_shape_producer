#shape production to plots
source utils/setup_root.sh

NTUPLE_TAG="03_11_23_allch_alleras_shifts"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FRIEND_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/"
FF="jetfakes_wpVSjet_Tight_22_11"
#FF_FRIENDS="/store/user/rschmieder/CROWN/ntuples/21_08_23_all_ch_17_18_shifts/CROWNFriends"
CHANNELS="mtt"
SHAPE_TAG="fit_shapes_ssTight_osTight_datayield"
ERAS="2016preVFP 2016postVFP"
REGIONS="control"
#shape production
for ERA in $ERAS 
do 
for CHANNEL in $CHANNELS
do
    #remove all files in the synced shapes directory to have it clean, as the last step combines all root files in the directory
    #rm -r output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes
    for REGION in $REGIONS
    do
        FILENAME="${REGION}"
        OUTPUT_FILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${FILENAME}"
        mkdir -p output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
        if [ $REGION == "control" ]; then
            python shapes/produce_shapes.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 1 --num-threads 1 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection ${FRIEND_PATH}/${FF} --control-plot-set m_tt  --region ${REGION} --xrootd --skip-systematic-variations --process-selection data #,m_vis,mjj,njets,pt_vis,nbtag,pt_W,pt_1,pt_2,pt_3
            # # # #jetfakes estimation
            #bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 
            # bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${OUTPUT_FILE}.root ${REGION}
        else
            python shapes/produce_shapes.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 4 --num-threads 12 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection ${FRIEND_PATH}/${FF} --control-plot-set m_tt --region ${REGION} --xrootd
            # # # #jetfakes estimation
            bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 
            #synced shapes for fit
            bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${OUTPUT_FILE}.root ${REGION}
        fi
    done
    #OUTFILE=output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/${ERA}_${CHANNEL}_synced.root
    #echo "[INFO] Adding written files to single output file $OUTFILE..."
    #hadd -f $OUTFILE output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*.root
done
done


