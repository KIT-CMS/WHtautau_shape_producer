CHANNELS="emt mmt mtt ett"
ERAS="2016preVFP 2016postVFP"
NTUPLE_TAG="03_11_23_allch_alleras_shifts"
SHAPE_TAG_CAT="fit_shapes_ssTight_osTight"
SHAPE_TAG="${SHAPE_TAG_CAT}_emt_met_comb_2016combcats"
CHARGES="plus minus"
for ERA in $ERAS
do
    for CHANNEL in $CHANNELS
    do
        for CHARGE in $CHARGES
        do
            REGION="all_cats_${CHARGE}"
            mkdir -p output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
            SHAPES_RFILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}.root"
            echo "${SHAPES_RFILE} output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG_CAT}/sig_${CHARGE}.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG_CAT}/control_${CHARGE}.root"
            hadd -j 1 -n 600 -f ${SHAPES_RFILE} output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG_CAT}/sig_${CHARGE}.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG_CAT}/control_${CHARGE}.root
            bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${SHAPES_RFILE} ${REGION}
        done
        OUTFILE_SYNC=output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/${ERA}_${CHANNEL}_synced.root
        echo "[INFO] Adding written files to single output file $OUTFILE..."
        hadd -f $OUTFILE_SYNC output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*.root
    done
done 