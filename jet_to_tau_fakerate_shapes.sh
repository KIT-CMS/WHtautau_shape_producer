#WH fake rate shapes
source utils/setup_root.sh
NTUPLE_TAG=$1
NTUPLE_PATH=$2
FRIEND_PATH=$3
ERA=$4
DATE=$5
WP_VS_JET=$6
WP_ELE=$7
WP_MU=$8
MODE=$9
FF_FRIEND=${10}
CLOSURE_FRIEND=${11}
MET_CLOSURE_FRIEND=${12}
CHANNEL="mmt"
DMS="0"
OUTPUT_DIR="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/fakerate_measurement_${DATE}/${WP_VS_JET}vsJets"
mkdir -p ${OUTPUT_DIR}

if [[ $MODE == "FF" ]]; then
    for DM in $DMS
    do
        for WP_JET in ${WP_VS_JET} VVVLoose   
        do
            echo "Decay Mode: $DM, WP_Jet: $WP_JET, WP_Ele: ${WP_ELE}, WP_Mu: ${WP_MU}"
            FILENAME="${WP_JET}_vs_jets__${WP_MU}_vs_mu__${WP_ELE}_vs_ele__DM${DM}"
            OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}"
            python shapes/produce_shapes_fakerate.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 2 --num-threads 2 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection --skip-systematic-variations --control-plot-set pt_3 --wp_vs_jet ${WP_JET} --wp_vs_jet_tight ${WP_VS_JET} --wp_vs_mu ${WP_MU} --wp_vs_ele ${WP_ELE} --decay_mode ${DM} --id_wp_ele Tight --id_wp_mu Tight --xrootd
        done
    done
elif [[ $MODE == "CLOSURE" ]]; then
    for DM in $DMS
    do
        WP_JET=$WP_VS_JET
        FILENAME="${WP_JET}_vs_jets__${WP_MU}_vs_mu__${WP_ELE}_vs_ele__DM${DM}"
        OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}"
        echo "huuuuuuuuuu"
        echo "${FRIEND_PATH}/${CLOSURE_FRIEND}"
        echo "${FRIEND_PATH}/${MET_CLOSURE_FRIEND}"
        python shapes/produce_shapes_fakerate.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 2 --num-threads 2 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection ${FF_FRIEND} ${CLOSURE_FRIEND} ${MET_CLOSURE_FRIEND} --skip-systematic-variations --control-plot-set pt_3,njets,met,eta_3 --wp_vs_jet ${WP_JET} --wp_vs_jet_tight ${WP_VS_JET} --wp_vs_mu ${WP_MU} --wp_vs_ele ${WP_ELE} --decay_mode ${DM} --id_wp_ele Tight --id_wp_mu Tight --xrootd --closure_corr
        bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0
    done
fi
