# 2016prevfp ggzz control_plus mtt 
# 2016prevfp remtt control_minus mtt
# 2016prevfp zzz sig_minus ett
MODE=$1
NTUPLE_TAG="11_07_24_alleras_allch"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
#this date and WP is only for FF friends. The date is the date of today, when FF Friends are produced
FF_FRIEND_WP_VS_JET="VTight"
FF_FRIEND_WP_VS_LEP="Tight"
FF_DATE="07_06_24"
FF_FRIEND_TAG_LLT="jetfakes_wpVSjet_Tight_07_06_24"
FF_FRIEND_TAG_LTT="jetfakes_wpVSjet_VTight_07_06_24"
FF_NTUPLE_TAG="31_05_24_ff_ntuples_2"
NN_FRIEND_TAG="None"
CHANNELS="met emt mmt mtt ett"
SHAPE_TAG="05_08_24_control_plots_kinvars"
ERAS="2016preVFP 2016postVFP 2017 2018"
CONTROL=0
PROCESSES="sig data bkg1 bkg2 bkg3"
PLOT_CATS="sig diboson misc"
#REGION can be either nn_control (pt_1, pt_2, m_tt, pt_3, ..), nn_control_max_value (predicted_max_value) or nn_signal_plus (predicted_max_value+systematics)
REGIONS="control"


if [[ $MODE == "XSEC" ]]; then
    bash friendtree_production.sh XSEC $NTUPLE_TAG $NTUPLE_PATH "" ""
fi
if [[ $MODE == "FF_FRIEND" ]]; then
    bash friendtree_production.sh FF $NTUPLE_TAG $NTUPLE_PATH $FF_NTUPLE_TAG $FF_DATE $FF_FRIEND_WP_VS_JET $FF_FRIEND_WP_VS_LEP
fi
if [[ $MODE == "LOCAL" ]]; then
    source utils/setup_root.sh
    echo "[INFO] Running LOCAL"
    for ERA in $ERAS
    do  
        for CHANNEL in $CHANNELS
        do
            if [ "$CHANNEL" = "ett" ] || [ "$CHANNEL" = "mtt" ] ; then
                FF_FRIEND_TAG=$FF_FRIEND_TAG_LTT
                NN_FRIEND_TAG=$NN_FRIEND_TAG_LTT
            else
                FF_FRIEND_TAG=$FF_FRIEND_TAG_LLT
                NN_FRIEND_TAG=$NN_FRIEND_TAG_LLT
            fi
            source utils/setup_samples.sh $NTUPLE_TAG $ERA
            echo $XSEC_FRIENDS $FF_FRIENDS $NN_FRIENDS
            echo "--------------------------------------"
            for REGION in $REGIONS
            do
                FILENAME="${REGION}"
                OUTPUT_FILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${FILENAME}"
                mkdir -p output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
                if [[ $REGION == "control" ]]; then
                    CONTROL_ARG="--control-plot-set m_tt,pt_1,pt_2,pt_3 --skip-systematic-variations --control-plots" # "
                    echo "[INFO] Control shapes for cutbased analysis will be produced. Argument: ${CONTROL_ARG}"
                else
                    CONTROL_ARG="--control-plot-set m_tt" # ,m_vis,mjj,njets,pt_vis,nbtag,pt_W,m_tt,m_vis,pt_1,pt_2,pt_3"
                    echo "[INFO] Analysis shapes for cutbased analysis will be produced. Argument: ${CONTROL_ARG}"
                fi
                python shapes/produce_shapes.py --channels $CHANNEL \
                --output-file ${OUTPUT_FILE} \
                --directory $NTUPLES \
                --ntuple_type crown \
                --$CHANNEL-friend-directory $XSEC_FRIENDS $FF_FRIENDS \
                --era $ERA \
                --num-processes 1 \
                --num-threads 1 \
                --optimization-level 1 \
                --region ${REGION} \
                --xrootd \
                $CONTROL_ARG
                bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 
            done
        done
    done    
    echo "[INFO] finished"
fi
if [[ $MODE == "CONDOR" ]]; then
    source utils/setup_root.sh
    echo "[INFO] Running on Condor"
    for ERA in $ERAS
    do
        for CHANNEL in $CHANNELS
        do
            if [ "$CHANNEL" = "ett" ] || [ "$CHANNEL" = "mtt" ] ; then
                FF_FRIEND_TAG=$FF_FRIEND_TAG_LTT
            else
                FF_FRIEND_TAG=$FF_FRIEND_TAG_LLT
            fi
            for REGION in $REGIONS
            do
                for PROC in $PROCESSES
                do
                    echo $PROC
                    CONDOR_OUTPUT="output/condor_shapes/${ERA}-${CHANNEL}-${NTUPLE_TAG}-${SHAPE_TAG}-${REGION}-${PROC}"
                    echo "[INFO] Condor output folder: ${CONDOR_OUTPUT}"
                    bash submit/submit_shape_production.sh $ERA $CHANNEL "singlegraph" $NTUPLE_TAG $SHAPE_TAG $REGION $CONTROL $CONDOR_OUTPUT $FF_FRIEND_TAG $NN_FRIEND_TAG ${PROC}
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

    #combine control and signal region in 2016eras
    CHANNELS="emt mmt mtt ett"
    ERAS="2016preVFP 2016postVFP"
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
                echo "${SHAPES_RFILE} output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG_CAT}/sig_${CHARGE}.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/control_${CHARGE}.root"
                hadd -j 1 -n 600 -f ${SHAPES_RFILE} output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/sig_${CHARGE}.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/control_${CHARGE}.root
            done
        done
    done 
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
                    bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${SHAPES_RFILE} ${REGION} --gof
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
    CHANNELS="emt mtt mmt ett"
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