# 2016prevfp ggzz control_plus mtt 
# 2016prevfp remtt control_minus mtt
# 2016prevfp zzz sig_minus ett
MODE=$1
NTUPLE_TAG="03_11_23_allch_alleras_shifts"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FF_FRIEND_TAG="jetfakes_wpVSjet_Tight_22_11"
#FF_FRIENDS="/store/user/rschmieder/CROWN/ntuples/21_08_23_all_ch_17_18_shifts/CROWNFriends"
CHANNELS="ett mtt emt met mmt"
SHAPE_TAG="fit_shapes_ssTight_osMedium"
ERAS="2016preVFP 2016postVFP 2017 2018"
REGIONS="control_plus control_minus sig_plus sig_minus"
CONTROL=0
#PROCESSES="ggzz rem_vh rem_ttbar www wwz wzz zzz whminus whplus zh wz zz dy tt wjets data"
PROCESSES="all"
if [[ $MODE == "CONDOR" ]]; then
    source utils/setup_root.sh
    echo "[INFO] Running on Condor"
    for ERA in $ERAS
    do
        for CHANNEL in $CHANNELS
        do
            for REGION in $REGIONS
            do
                for PROC in $PROCESSES
                do
                    
                    CONDOR_OUTPUT="output/condor_shapes/${ERA}-${CHANNEL}-${NTUPLE_TAG}-${SHAPE_TAG}-${REGION}-${PROC}"
                    echo "[INFO] Condor output folder: ${CONDOR_OUTPUT}"
                    bash submit/submit_shape_production.sh $ERA $CHANNEL "singlegraph" $NTUPLE_TAG $SHAPE_TAG $REGION $CONTROL $CONDOR_OUTPUT $FF_FRIEND_TAG ${PROC}
                done
            done
        done
    done    
    echo "[INFO] Jobs submitted"
fi
if [[ $MODE == "MERGE_FF" ]]; then
    source utils/setup_root.sh
    for ERA in $ERAS
    do
        for CHANNEL in $CHANNELS
        do
            #rm -r output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
            mkdir -p output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
            for REGION in $REGIONS
            do
                CONDOR_OUTPUT="output/condor_shapes/${ERA}-${CHANNEL}-${NTUPLE_TAG}-${SHAPE_TAG}-${REGION}"
                SHAPES_RFILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}.root"
                echo "[INFO] Merging outputs located in ${CONDOR_OUTPUT}"
                hadd -j 1 -n 600 -f ${SHAPES_RFILE} output/shapes/control_unit_graphs-${ERA}-${CHANNEL}-${NTUPLE_TAG}-${SHAPE_TAG}-${REGION}-*/*.root
                bash shapes/do_estimations.sh ${ERA} ${SHAPES_RFILE} 0 
            done 
        done 
    done
fi
if [[ $MODE == "SYNC" ]]; then
    source utils/setup_root.sh
    for ERA in $ERAS
    do
        for CHANNEL in $CHANNELS
        do
            for REGION in $REGIONS
            do
                SHAPES_RFILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}.root"
                echo "[INFO] Producing synced shapes for ${SHAPES_RFILE}"
                bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${SHAPES_RFILE} ${REGION}
            done 
            OUTFILE=output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/${ERA}_${CHANNEL}_synced.root
            echo "[INFO] Adding written files to single output file $OUTFILE..."
            hadd -f $OUTFILE output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*.root
        done 
    done
fi
