#!/bin/bash

ERA=$1
CHANNEL=$2
SUBMIT_MODE=$3
NTUPLE_TAG=$4
SHAPE_TAG=$5
REGION=$6
CONTROL=$7
OUTPUT=$8
FF_FRIEND_TAG=$9
NN_FRIEND_TAG=${10}
PROC=${11}
if [[ "$PROC" == "all" ]]; then
    PROC="data,dy,ggzh,ggzz,rem_ttbar,tt,vvv,wh_htt_minus,wh_htt_plus,wh_hww_minus,wh_hww_plus,wjets,wz,zh,zz"
elif [[ "$PROC" == "data" ]]; then
    PROC="data"
elif [[ "$PROC" == "bkg1" ]]; then
    PROC="dy,ggzz,rem_ttbar,zz"
elif [[ "$PROC" == "bkg2" ]]; then
    PROC="ggzh,tt,zh"
elif [[ "$PROC" == "sig" ]]; then
    PROC="wh_htt_minus,wh_htt_plus,wh_hww_minus,wh_hww_plus"
elif [[ "$PROC" == "bkg3" ]]; then
    PROC="vvv,wjets,wz"
fi
echo "producing shapes for processes era=$ERA, ch=$CHANNEL sub_mod=$SUBMIT_MODE ntupletag=$NTUPLE_TAG shapetag=$SHAPE_TAG region=$REGION crtl_arg=$CONTROL output=$OUTPUT ff=$FF_FRIEND_TAG nn=$NN_FRIEND_TAG proc=$PROC"
[[ ! -z $1 && ! -z $2 && ! -z $3 && ! -z $4 && ! -z $5 ]] || (
    echo "[ERROR] Number of given parameters is too small."
    exit 1
)
[[ ! -z $6 ]] || CONTROL=0
CONTROL_ARG=""
if [[ $REGION == "control" ]]; then
    CONTROL_ARG="--control-plot-set m_tt,pt_1,pt_2,pt_3 --skip-systematic-variations --control-plots" # "
    echo "[INFO] Control plots will be produced. Argument: ${CONTROL_ARG}"
elif [[ $REGION == "nn_control" ]]; then
    CONTROL_ARG="--control-plot-set m_vis,met,pt_1,pt_2,pt_3 --skip-systematic-variations --control-plots" # "
    echo "[INFO] Control plots will be produced. Argument: ${CONTROL_ARG}"
elif [[ $REGION == "nn_control_max_value" ]]; then
    CONTROL_ARG="--control-plot-set predicted_max_value,m_vis,met,pt_1,pt_2,pt_3,eta_1,eta_2,eta_3,deltaR_12,deltaR_13,deltaR_23,njets,phi_1,phi_2,phi_3,jpt_1,jpt_2 --skip-systematic-variations" # "
    echo "[INFO] Control plots will be produced. Argument: ${CONTROL_ARG}"
elif [[ $REGION == "nn_signal_plus" ]] || [[ $REGION == "nn_signal_minus" ]]; then
    CONTROL_ARG="--control-plot-set predicted_max_value" # "
    echo "[INFO] Control plots will be produced. Argument: ${CONTROL_ARG}"
else
    CONTROL_ARG="--control-plot-set m_tt" # ,m_vis,mjj,njets,pt_vis,nbtag,pt_W,m_tt,m_vis,pt_1,pt_2,pt_3"
    echo "[INFO] Analysis plots will be produced. Argument: ${CONTROL_ARG}"
fi
source utils/setup_samples.sh $NTUPLE_TAG $ERA
source utils/setup_root.sh
source utils/bashFunctionCollection.sh

if [[ "$SUBMIT_MODE" == "multigraph" ]]; then
    echo "[ERROR] Not implemented yet."
    exit 1
elif [[ "$SUBMIT_MODE" == "singlegraph" ]]; then
    echo "[INFO] Preparing graph for processes $PROC for submission..."
    echo "[INFO] Using tag $TAG"
    echo "[INFO] Using friends $XSEC_FRIENDS $FF_FRIENDS $NN_FRIENDS"
    [[ ! -d $OUTPUT ]] && mkdir -p $OUTPUT
    echo "[INFO] Using ntuples in $NTUPLES"

    python shapes/produce_shapes.py --channels $CHANNEL \
    --output-file dummy.root \
    --directory $NTUPLES \
    --ntuple_type crown \
    --$CHANNEL-friend-directory $XSEC_FRIENDS $FF_FRIENDS $NN_FRIENDS\
    --era $ERA \
    --optimization-level 1 \
    --process-selection $PROC \
    --region ${REGION} \
    --only-create-graphs \
    --graph-dir $OUTPUT \
    --xrootd \
    $CONTROL_ARG
    fi
    # Set output graph file name produced during graph creation.
    echo $PROC
    if [[ "${REGION}" == *"nn_"* ]];
    then
        GRAPH_FILE_FULL_NAME=${OUTPUT}/nn_unit_graphs-${ERA}-${CHANNEL}-${REGION}-${PROC}.pkl
        GRAPH_FILE=${OUTPUT}/nn_unit_graphs-${ERA}-${CHANNEL}-${NTUPLE_TAG}-${SHAPE_TAG}-${REGION}-${PROC}.pkl
        echo "nn_analysis"
    else
        GRAPH_FILE_FULL_NAME=${OUTPUT}/control_unit_graphs-${ERA}-${CHANNEL}-${REGION}-${PROC}.pkl
        GRAPH_FILE=${OUTPUT}/control_unit_graphs-${ERA}-${CHANNEL}-${NTUPLE_TAG}-${SHAPE_TAG}-${REGION}-${PROC}.pkl
    fi

    # rename the graph file to a shorter name
    mv $GRAPH_FILE_FULL_NAME $GRAPH_FILE

    # Prepare the jdl file for single core jobs.
    echo "[INFO] Creating the logging direcory for the jobs..."
    GF_NAME=$(basename $GRAPH_FILE)
    if [[ ! -d log/condorShapes/${GF_NAME%.pkl}/ ]]; then
        mkdir -p log/condorShapes/${GF_NAME%.pkl}/
    fi
    if [[ ! -d log/${GF_NAME%.pkl}/ ]]; then
        mkdir -p log/${GF_NAME%.pkl}/
    fi

    echo "[INFO] Preparing submission file for single core jobs for variation pipelines..."
    cp submit/produce_shapes_cc7.jdl $OUTPUT
    echo "output = log/condorShapes/${GF_NAME%.pkl}/\$(cluster).\$(Process).out" >>$OUTPUT/produce_shapes_cc7.jdl
    echo "error = log/condorShapes/${GF_NAME%.pkl}/\$(cluster).\$(Process).err" >>$OUTPUT/produce_shapes_cc7.jdl
    echo "log = log/condorShapes/${GF_NAME%.pkl}/\$(cluster).\$(Process).log" >>$OUTPUT/produce_shapes_cc7.jdl
    echo "queue a3,a2,a1 from $OUTPUT/arguments.txt" >>$OUTPUT/produce_shapes_cc7.jdl
    echo "JobBatchName = Shapes_${CHANNEL}_${ERA}" >>$OUTPUT/produce_shapes_cc7.jdl

    # Prepare the multicore jdl.
    echo "[INFO] Preparing submission file for multi core jobs for nominal pipeline..."
    cp submit/produce_shapes_cc7.jdl $OUTPUT/produce_shapes_cc7_multicore.jdl
    # Replace the values in the config which differ for multicore jobs.
    if [[ $CONTROL == 1 ]]; then
        sed -i '/^RequestMemory/c\RequestMemory = 16000' $OUTPUT/produce_shapes_cc7_multicore.jdl
    else
        sed -i '/^RequestMemory/c\RequestMemory = 10000' $OUTPUT/produce_shapes_cc7_multicore.jdl
    fi
    sed -i '/^RequestCpus/c\RequestCpus = 8' $OUTPUT/produce_shapes_cc7_multicore.jdl
    sed -i '/^arguments/c\arguments = $(a1) $(a2) $(a3) $(a4)' ${OUTPUT}/produce_shapes_cc7_multicore.jdl
    # Add log file locations to output file.
    echo "output = log/condorShapes/${GF_NAME%.pkl}/multicore.\$(cluster).\$(Process).out" >>$OUTPUT/produce_shapes_cc7_multicore.jdl
    echo "error = log/condorShapes/${GF_NAME%.pkl}/multicore.\$(cluster).\$(Process).err" >>$OUTPUT/produce_shapes_cc7_multicore.jdl
    echo "log = log/condorShapes/${GF_NAME%.pkl}/multicore.\$(cluster).\$(Process).log" >>$OUTPUT/produce_shapes_cc7_multicore.jdl
    echo "JobBatchName = Shapes_${CHANNEL}_${ERA}" >>$OUTPUT/produce_shapes_cc7_multicore.jdl
    echo "x509userproxy = /home/rschmieder/.globus/x509up" >>$OUTPUT/produce_shapes_cc7_multicore.jdl
    echo "queue a3,a2,a4,a1 from $OUTPUT/arguments_multicore.txt" >>$OUTPUT/produce_shapes_cc7_multicore.jdl

    # Assemble the arguments.txt file used in the submission
    python submit/prepare_args_file.py --graph-file $GRAPH_FILE --output-dir $OUTPUT --pack-multiple-pipelines 10
    echo "[INFO] Submit shape production with 'condor_submit $OUTPUT/produce_shapes_cc7.jdl' and 'condor_submit $OUTPUT/produce_shapes_cc7_multicore.jdl'"
    condor_submit $OUTPUT/produce_shapes_cc7.jdl
    condor_submit $OUTPUT/produce_shapes_cc7_multicore.jdl
else
    echo "[ERROR] Given mode $SUBMIT_MODE is not supported. Aborting..."
    exit 1
fi