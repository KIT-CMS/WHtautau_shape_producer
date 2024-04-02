# 2016prevfp ggzz control_plus mtt 
# 2016prevfp remtt control_minus mtt
# 2016prevfp zzz sig_minus ett
MODE=$1
NTUPLE_TAG="16_02_24_charge_req_in_ntuple_alleras_allch"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FF_FRIEND_TAG="jetfakes_wpVSjet_Tight_19_02_24"
#FF_FRIENDS="/store/user/rschmieder/CROWN/ntuples/21_08_23_all_ch_17_18_shifts/CROWNFriends"
CHANNELS="mmt"
SHAPE_TAG="fit_shapes_ssTight_osTight_19_02_24"
ERAS="2016preVFP 2016postVFP 2017 2018"
REGIONS="control" #"control_plus control_minus sig_plus sig_minus"
CONTROL=1
PROCESSES="sig data bkg1 bkg2 bkg3"
if [[ $MODE == "XSEC" ]]; then
    bash friendtree_production.sh XSEC $NTUPLE_TAG $NTUPLE_PATH "" ""
fi
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
                    echo $PROC
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
            #rm -r output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/
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
if [[ $MODE == "COMB" ]]; then
    echo " ------------- "
    echo "combination of emt and met to emt and combination of control and signal category in 2016eras"
    echo " ------------- "
    CHANNELS="emt met"
    source utils/setup_root.sh
    #combine emt and met channels in all eras
    for ERA in $ERAS
    do
        for CHANNEL in $CHANNELS
        do  
            mkdir -p output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}_only/${SHAPE_TAG}/
            for REGION in $REGIONS
            do                    
                mv output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}_only/${SHAPE_TAG}/.
            done
        done 
    done
    for ERA in $ERAS
    do
        OUTPUT="output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}"
        mkdir -p $OUTPUT
        for REGION in $REGIONS
        do 
            echo " ------------- "
            echo "$ERA emt met combination"
            echo " ------------- "
            python shapes/emt_met_combination.py --input_emt "output/shapes/${NTUPLE_TAG}/${ERA}/emt_only/${SHAPE_TAG}/${REGION}.root" --input_met "output/shapes/${NTUPLE_TAG}/${ERA}/met_only/${SHAPE_TAG}/${REGION}.root" --output ${OUTPUT}/${REGION}.root
        done
    done

    # #combine control and signal region in 2016eras
    # CHANNELS="emt mmt mtt ett"
    # ERAS="2016preVFP 2016postVFP"
    # CHARGES="plus minus"
    # for ERA in $ERAS
    # do
    #     for CHANNEL in $CHANNELS
    #     do
    #         for CHARGE in $CHARGES
    #         do
    #             REGION="all_cats_${CHARGE}"
    #             mkdir -p output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
    #             SHAPES_RFILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}.root"
    #             echo "${SHAPES_RFILE} output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG_CAT}/sig_${CHARGE}.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/control_${CHARGE}.root"
    #             hadd -j 1 -n 600 -f ${SHAPES_RFILE} output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/sig_${CHARGE}.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/control_${CHARGE}.root
    #         done
    #     done
    # done 
fi
if [[ $MODE == "SYNC" ]]; then
    CHANNELS="emt mtt mmt ett"
    source utils/setup_root.sh
    for ERA in $ERAS
    do
        if [[ $ERA == "2016preVFP" || $ERA == "2016postVFP" ]]; then
            for CHANNEL in $CHANNELS
            do
                REGIONS2016="all_cats_plus all_cats_minus"
                for REGION in ${REGIONS2016}
                do
                    SHAPES_RFILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}.root"
                    echo " -----------"
                    echo "[INFO] Producing synced shapes for ${SHAPES_RFILE}"
                    echo " -----------"
                    bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${SHAPES_RFILE} ${REGION}
                done 
                OUTFILE=output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/${ERA}_${CHANNEL}_synced.root
                echo " -----------"
                echo "[INFO] Adding written files to single output file $OUTFILE..."
                echo " -----------"
                hadd -f $OUTFILE output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*.root
            done
        else
            for CHANNEL in $CHANNELS
            do
                for REGION in $REGIONS
                do
                    if [[ $REGION == "control" ]]; then
                        echo " -----------"
                        echo "control region, no sync necessary"
                        echo " -----------"
                    else
                        SHAPES_RFILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}.root"
                        echo " -----------"
                        echo "[INFO] Producing synced shapes for ${SHAPES_RFILE}"
                        echo " -----------"
                        bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${SHAPES_RFILE} ${REGION}
                    fi
                done 
                OUTFILE=output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/${ERA}_${CHANNEL}_synced.root
                echo " -----------"
                echo "[INFO] Adding written files to single output file $OUTFILE..."
                echo " -----------"
                hadd -f $OUTFILE output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*.root
            done 
        fi
    done
fi
if [[ $MODE == "PLOT" ]]; then
    CHANNELS="mmt" #"emt mtt mmt ett"
    source utils/setup_root.sh
    export PYTHONPATH=$PYTHONPATH:$PWD/Dumbledraw
    for ERA in $ERAS
    do
        for CHANNEL in $CHANNELS
        do
            for REGION in $REGIONS
            do
                INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}.root"
                TAG="${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}"
                if [ "$REGION" = "control" ]; then
                    for VAR in m_tt pt_1 pt_2 pt_3
                    do
                        python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} #--draw-jet-fake-variation tau_anti_iso #--normalize-by-bin-width
                        python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation #--draw-jet-fake-variation tau_anti_iso # --normalize-by-bin-width
                    done
                else
                    for VAR in m_tt #m_vis mjj njets pt_vis phi_2 eta_2 nbtag #pt_W m_tt m_vis pt_1 pt_2 pt_3
                    do
                        python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} #--blinded #--draw-jet-fake-variation tau_anti_iso #--normalize-by-bin-width
                        python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation #--blinded #--draw-jet-fake-variation tau_anti_iso # --normalize-by-bin-width
                    done
                fi
            done
        done 
    done 
fi