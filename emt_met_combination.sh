ERAS="2016preVFP 2016postVFP"
NTUPLE_TAG="03_11_23_allch_alleras_shifts"
SHAPE_TAG_REF="fit_shapes_ssTight_osTight"
SHAPE_TAG="${SHAPE_TAG_REF}_emt_met_comb_2016combcats"
REGIONS="control_plus control_minus sig_plus sig_minus"
OTHER_CHANNELS="ett mtt mmt"
source utils/setup_root.sh
for ERA in $ERAS
do
    # if [[ $ERA == "2016preVFP" || $ERA == "2016postVFP" ]]; then
    #     REGION="all_cats"
    #     OUTPUT="output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}"
    #     mkdir -p $OUTPUT
    #     echo " ------------- "
    #     echo "$ERA emt met combination"
    #     echo " ------------- "
    #     python shapes/emt_met_combination.py --input_emt "output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/${REGION}.root" --input_met "output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG}/${REGION}.root" --output ${OUTPUT}/${REGION}.root
    #     echo " ------------- "
    #     echo "$ERA emt met sync"
    #     echo " ------------- "
    #     bash shapes/convert_to_synced_shapes.sh ${ERA} emt ${NTUPLE_TAG} ${SHAPE_TAG} ${OUTPUT}/${REGION}.root ${REGION}
    #     OUTFILE_SYNC=output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/synced_shapes/${ERA}_emt_synced.root
    #     mv output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/synced_shapes/${ERA}-emt-synced-m_tt-${REGION}.root ${OUTFILE_SYNC}
    # else
   # rm -r "output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/"
        # for REGION in $REGIONS
        # do
        #     echo $REGION
            
        #     OUTPUT="output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/"
        #     mkdir -p $OUTPUT
        #     python shapes/emt_met_combination.py --input_emt "output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG_REF}/${REGION}.root" --input_met "output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG_REF}/${REGION}.root" --output ${OUTPUT}/${REGION}.root
        #     bash shapes/convert_to_synced_shapes.sh ${ERA} emt ${NTUPLE_TAG} ${SHAPE_TAG} ${OUTPUT}/${REGION}.root ${REGION}
        #     OUTFILE_SYNC=output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/synced_shapes/${ERA}_emt_synced.root
        #     hadd -f $OUTFILE_SYNC output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/synced_shapes/*.root
        # done
        hadd -f output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/control.root output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/control*.root
   #fi
    # for CHANNEL in $OTHER_CHANNELS
    # do 
    #     #rm -r "output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/"
    #     mkdir -p "output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/"
    #     cp -r "output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG_REF}/synced_shapes" "output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/." 
    # done
done 
