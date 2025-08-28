# 2016prevfp ggzz control_plus mtt 
# 2016prevfp remtt control_minus mtt
# 2016prevfp zzz sig_minus ett
MODE=$1
NTUPLE_TAG="14_04_25_alleras_allch3"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
#this date and WP is only for FF friends
FF_FRIEND_WP_VS_JET="Medium"
FF_FRIEND_WP_VS_LEP="Medium"
FF_DATE="27_02_25_MediumvsJetsvsL"
FF_NTUPLE_TAG="26_02_25_ff"
#From here it is analysis level
FF_FRIEND_TAG_LLT="jetfakes_wpVSjet_Medium_27_02_25_MediumvsJetsvsL"
FF_FRIEND_TAG_LTT="jetfakes_wpVSjet_Medium_27_02_25_MediumvsJetsvsL"
# FF_FRIEND_TAG_LLT="jetfakes_wpVSjet_Medium_08_05_25_MediumvsJetsvsL_nomtcut"
# FF_FRIEND_TAG_LTT="jetfakes_wpVSjet_Medium_08_05_25_MediumvsJetsvsL_nomtcut"
FF_MET_SHAPE_FRIEND_TAG="met_unc_04_03_25"
FF_PT1_SHAPE_FRIEND_TAG="pt_1_unc_04_03_25"
FF_NN_SHAPE_FRIEND_TAG="nn_score_2017_llt_uncfinal"
NN_FRIEND_TAG_LLT="nn_friends_15_04_25_MediumJL_10_4_standard2"
NN_FRIEND_TAG_LTT="nn_friends_15_04_25_MediumJL_10_4_standard2"
# NN_FRIEND_TAG_LLT="nn_friends_07_05_25__27_03_25_alldibosonindiboson"
# NN_FRIEND_TAG_LTT="nn_friends_07_05_25__27_03_25_alldibosonindiboson"
CHANNELS="met mmt emt mtt ett"
#CHANNELS="emt"
SHAPE_TAG="11_08_25_nncontrol_incl"
ERAS="2018 2017 2016postVFP 2016preVFP"
#ERAS="all_eras"
CONTROL=0
PROCESSES="bkg1 bkg2 data sig"
PLOT_CATS="sig diboson misc"
#REGION can be either nn_control (pt_1, pt_2, m_tt, pt_3, ..), nn_control_max_value (predicted_max_value) or nn_signal_plus (predicted_max_value+systematics)
REGIONS="nn_control"
if [[ $MODE == "XSEC" ]]; then
    bash friendtree_production.sh XSEC $NTUPLE_TAG $NTUPLE_PATH "" ""
fi
if [[ $MODE == "FF_FRIEND" ]]; then
    bash friendtree_production.sh FF $NTUPLE_TAG $NTUPLE_PATH $FF_NTUPLE_TAG $FF_DATE $FF_FRIEND_WP_VS_JET $FF_FRIEND_WP_VS_LEP
fi
if [[ $MODE == "CLOSURE_FRIEND" ]]; then
    bash friendtree_production.sh CLOSURE $NTUPLE_TAG $NTUPLE_PATH $FF_NTUPLE_TAG $FF_DATE $FF_FRIEND_WP_VS_JET $FF_FRIEND_WP_VS_LEP
fi
if [[ $MODE == "MET_UNC" ]]; then
    bash friendtree_production.sh MET $NTUPLE_TAG $NTUPLE_PATH $FF_NTUPLE_TAG $FF_DATE $FF_FRIEND_WP_VS_JET $FF_FRIEND_WP_VS_LEP
fi
if [[ $MODE == "PT_UNC" ]]; then
    bash friendtree_production.sh PT $NTUPLE_TAG $NTUPLE_PATH $FF_NTUPLE_TAG $FF_DATE $FF_FRIEND_WP_VS_JET $FF_FRIEND_WP_VS_LEP
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
               # rm -r output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
                mkdir -p output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
                if [[ $REGION == "control" ]]; then
                    CONTROL_ARG="--control-plot-set m_tt,pt_1,pt_2,pt_3 --skip-systematic-variations --control-plots" # "
                    echo "[INFO] Control shapes for cutbased analysis will be produced. Argument: ${CONTROL_ARG}"
                elif [[ $REGION == "nn_control" ]]; then
                    CONTROL_ARG="--control-plot-set pt_1 --skip-systematic-variations --control-plots"
                    echo "[INFO] Control shapes with kinematic variables for nn analysis will be produced. Argument: ${CONTROL_ARG}"
                elif [[ $REGION == "nn_control_max_value" ]]; then
                    CONTROL_ARG="--control-plot-set predicted_max_value --skip-systematic-variations" # "
                    echo "[INFO] Control shapes with max value for nn analysis will be produced. Argument: ${CONTROL_ARG}"
                elif [[ $REGION == "nn_signal_plus" ]] || [[ $REGION == "nn_signal_minus" ]]; then
                    CONTROL_ARG="--control-plot-set predicted_max_value" #,zh,wh_htt_minus,wh_htt_plus,wh_hww_minus,wh_hww_plus" # "
                    echo "[INFO] Analysis shapes for nn analysis will be produced. Argument: ${CONTROL_ARG}"
                else
                    CONTROL_ARG="--control-plot-set m_tt" # ,m_vis,mjj,njets,pt_vis,nbtag,pt_W,m_tt,m_vis,pt_1,pt_2,pt_3"
                    echo "[INFO] Analysis shapes for cutbased analysis will be produced. Argument: ${CONTROL_ARG}"
                fi
                #$PT_SHAPE_FRIENDS $MET_SHAPE_FRIENDS $NN_SHAPE_FRIENDS \
                python shapes/produce_shapes.py --channels $CHANNEL \
                --output-file ${OUTPUT_FILE} \
                --directory $NTUPLES \
                --ntuple_type crown \
                --$CHANNEL-friend-directory $XSEC_FRIENDS $NN_FRIENDS $FF_FRIENDS $PT_SHAPE_FRIENDS $MET_SHAPE_FRIENDS \
                --era $ERA \
                --num-processes 2 \
                --num-threads 4 \
                --optimization-level 1 \
                --region ${REGION} \
                --xrootd \
                --process-selection tth \
                $CONTROL_ARG
               bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 
            done
        done
    done    
    echo "[INFO] finished"
                    
fi
#
if [[ $MODE == "CONDOR" ]]; then
    source utils/setup_root.sh
    echo "[INFO] Running on Condor"
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
            for REGION in $REGIONS
            do
                for PROC in $PROCESSES
                do
                    echo $PROC
                    CONDOR_OUTPUT="output/condor_shapes/${ERA}-${CHANNEL}-${NTUPLE_TAG}-${SHAPE_TAG}-${REGION}-${PROC}"
                    echo "[INFO] Condor output folder: ${CONDOR_OUTPUT}"
                    bash submit/submit_shape_production.sh $ERA $CHANNEL "singlegraph" $NTUPLE_TAG $SHAPE_TAG $REGION $CONTROL $CONDOR_OUTPUT $FF_FRIEND_TAG $NN_FRIEND_TAG ${PROC} $FF_MET_SHAPE_FRIEND_TAG $FF_PT1_SHAPE_FRIEND_TAG $FF_NN_SHAPE_FRIEND_TAG
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
                hadd -j 1 -n 600 -f ${SHAPES_RFILE} output/shapes/nn_unit_graphs-${ERA}-${CHANNEL}-${NTUPLE_TAG}-${SHAPE_TAG}-${REGION}-*/*.root
                bash shapes/do_estimations.sh ${ERA} ${SHAPES_RFILE} 0 
            done 
        done 
    done
fi
if [[ $MODE == "COMB_LLT" ]]; then
    source utils/setup_root.sh
    for ERA in $ERAS # 2016preVFP 2016postVFP
    do
        OUTPUT="output/shapes/${NTUPLE_TAG}/${ERA}/llt/${SHAPE_TAG}"
        mkdir -p $OUTPUT
        for REGION in $REGIONS
        do 
            echo " ------------- "
            echo "$ERA emt met mmt to llt combination in 2016 eras"
            echo " ------------- "
            echo "emt file: "output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/${REGION}.root""
            echo "met file: "output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG}/${REGION}.root""
            echo "mmt file: "output/shapes/${NTUPLE_TAG}/${ERA}/mmt/${SHAPE_TAG}/${REGION}.root""

            python shapes/llt_ltt_combination.py --input_emt "output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/${REGION}.root" --input_met "output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG}/${REGION}.root" --input_mmt "output/shapes/${NTUPLE_TAG}/${ERA}/mmt/${SHAPE_TAG}/${REGION}.root" --output ${OUTPUT}/${REGION}.root --channel llt
        done
    done
fi
if [[ $MODE == "COMB_LTT" ]]; then
    source utils/setup_root.sh
    for ERA in $ERAS # 2016preVFP 2016postVFP
    do
        OUTPUT="output/shapes/${NTUPLE_TAG}/${ERA}/ltt/${SHAPE_TAG}"
        mkdir -p $OUTPUT
        for REGION in $REGIONS
        do 
            echo " ------------- "
            echo "$ERA ett mtt to ltt combination in 2016 eras"
            echo " ------------- "
            echo "ett file: "output/shapes/${NTUPLE_TAG}/${ERA}/ett/${SHAPE_TAG}/${REGION}.root""
            echo "mtt file: "output/shapes/${NTUPLE_TAG}/${ERA}/mtt/${SHAPE_TAG}/${REGION}.root""

            python shapes/llt_ltt_combination.py --input_ett "output/shapes/${NTUPLE_TAG}/${ERA}/ett/${SHAPE_TAG}/${REGION}.root" --input_mtt "output/shapes/${NTUPLE_TAG}/${ERA}/mtt/${SHAPE_TAG}/${REGION}.root" --output ${OUTPUT}/${REGION}.root --channel ltt
        done
    done
fi
if [[ $MODE == "COMB_EMT" ]]; then
    echo " ------------- "
    echo "combination of emt and met to emt in 2017,2018 eras"
    echo " ------------- "
    CHANNELS="emt met"

    source utils/setup_root.sh
    
    for ERA in $ERAS
    do
        OUTPUT="output/shapes/${NTUPLE_TAG}/${ERA}/emmet/${SHAPE_TAG}"
    mkdir -p $OUTPUT
        for REGION in $REGIONS
        do 
            ls "output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/${REGION}.root"
            ls "output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG}/${REGION}.root"
            echo " ------------- "
            echo "$ERA emt met combination"
            echo " ------------- "
            python shapes/llt_ltt_combination.py --input_emt "output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/${REGION}.root" --input_met "output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG}/${REGION}.root" --output ${OUTPUT}/${REGION}.root --channel emt
        done
    done
fi
if [[ $MODE == "COMB_CHARGE" ]]; then
    CHARGES="plus minus"
    CHANNELS="llt ltt"
    for ERA in $ERAS
    do
        for CHANNEL in $CHANNELS
        do
                REGIONS="both_charges"
                rm -r "output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGIONS}.root"
                SHAPES_RFILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGIONS}.root"
                echo "${SHAPES_RFILE} output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/nn_signal_plus.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/nn_signal_minus.root"
                hadd -j 1 -n 600 -f ${SHAPES_RFILE} output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/nn_signal_plus.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/nn_signal_minus.root
        done
    done
fi
if [[ $MODE == "COMB_ERA" ]]; then
    source utils/setup_root.sh
    for CHANNEL in $CHANNELS
    do
        OUTPUT="output/shapes/${NTUPLE_TAG}/all_eras/${CHANNEL}/${SHAPE_TAG}"
        mkdir -p ${OUTPUT}
        for REGION in $REGIONS
        do 
            hadd -j 1 -n 600 -f ${OUTPUT}/${REGION}.root "output/shapes/${NTUPLE_TAG}/2016preVFP/${CHANNEL}/${SHAPE_TAG}/${REGION}.root" "output/shapes/${NTUPLE_TAG}/2016postVFP/${CHANNEL}/${SHAPE_TAG}/${REGION}.root" "output/shapes/${NTUPLE_TAG}/2017/${CHANNEL}/${SHAPE_TAG}/${REGION}.root" "output/shapes/${NTUPLE_TAG}/2018/${CHANNEL}/${SHAPE_TAG}/${REGION}.root"
        done
    done
fi
if [[ $MODE == "COMB_CH" ]]; then
    source utils/setup_root.sh
    for ERA in $ERAS # 2016preVFP 2016postVFP
    do
        OUTPUT="output/shapes/${NTUPLE_TAG}/${ERA}/allch/${SHAPE_TAG}"
        mkdir -p $OUTPUT
        for REGION in $REGIONS
        do 
            python shapes/llt_ltt_combination.py --input_ett "output/shapes/${NTUPLE_TAG}/${ERA}/ett/${SHAPE_TAG}/${REGION}.root" --input_mtt "output/shapes/${NTUPLE_TAG}/${ERA}/mtt/${SHAPE_TAG}/${REGION}.root" --output ${OUTPUT}/${REGION}.root --input_emt "output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/${REGION}.root" --input_met "output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG}/${REGION}.root" --input_mmt "output/shapes/${NTUPLE_TAG}/${ERA}/mmt/${SHAPE_TAG}/${REGION}.root" --output ${OUTPUT}/${REGION}.root --channel all
        done
    done
fi
if [[ $MODE == "SYNC" ]]; then
    source utils/setup_root.sh
    for ERA in $ERAS
    do
        # if [[ $ERA == "2016preVFP" ]] || [[ $ERA == "2016postVFP" ]]; then
        #     CHANNELS="llt ltt"
        # else
        #     CHANNELS="llt mmt mtt ett"
        # fi
        CHANNELS="llt ltt"
        #REGIONS="both_charges"
        for CHANNEL in $CHANNELS
        do
            rm -r output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/
            for REGION in $REGIONS
            do
                if [[ $REGION == "nn_control" ]] || [[ $REGION == "nn_control_max_value" ]]; then
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
    done
fi
if [[ $MODE == "COMB_CATS" ]]; then
    #combine control and signal region in 2016eras
    CHANNELS="emt mmt mtt ett"
    ERAS="2016preVFP 2016postVFP"
    CHARGES="plus minus"
    for ERA in $ERAS
    do
        for CHANNEL in $CHANNELS
        do
                FILE="${ERA}_${CHANNEL}_synced.root"
                mkdir -p output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
                SHAPES_RFILE="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/${FILE}"
                
                for CHARGE in ${CHARGES}
                do
                    hadd -j 1 -n 600 -f output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/${CHANNEL}_allcats_${CHARGE}.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*_${CHARGE}.root
                done
                echo "${SHAPES_RFILE} output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*allcats_* "
                hadd -j 1 -n 600 -f ${CHANNEL}_allcats_${CHARGE}.root output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*allcats*
        done
    done 
fi
if [[ $MODE == "PLOT" ]]; then
    #CHANNELS="met emt mtt mmt ett"
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
                if [ "$REGION" = "nn_control" ]; then
                    for VAR in pt_1,pt_2,pt_3,m_vis,met,njets
                    do
                        # for PLOT_CAT in $PLOT_CATS
                        # do
                            python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} #--draw-jet-fake-variation tau_anti_iso #--normalize-by-bin-width
                            #python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation #--draw-jet-fake-variation tau_anti_iso # --normalize-by-bin-width
                        #done
                    done
                else
                    for PLOT_CAT in $PLOT_CATS
                    do
                        for VAR in predicted_max_value #,m_vis,pt_1,pt_2,pt_3,njets,met
                        do
                            # if [ "$PLOT_CAT" = "sig" ]; then
                            #     python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} --category-postfix $PLOT_CAT --blinded
                            # else
                                python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} --category-postfix $PLOT_CAT #--blinded
                            #fi
                        done
                    done
                fi
            done
        done 
    done 
fi