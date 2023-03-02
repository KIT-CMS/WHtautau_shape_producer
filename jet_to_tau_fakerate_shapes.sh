#WH fake rate shapes
source utils/setup_root.sh

TAG="27_01_all_ch"
NTUPLE_PATH="/work/rschmieder/WH_analysis/WHtautau_shape_producer/temp_ntuples_friends/${TAG}/ntuples"
FRIEND_PATH="/work/rschmieder/WH_analysis/WHtautau_shape_producer/temp_ntuples_friends/${TAG}/friends"
CHANNEL="mmt"
ERA="2018"
OUTPUT_DIR="output/shapes/${TAG}/${CHANNEL}/fakerate_measurement2"
mkdir -p ${OUTPUT_DIR}

for DM in 0 1 10 11
do
    for WP_JET in VTight VVVLoose
    do
        echo "$DM, $WP_JET"
        WP_ELE="Tight"
        WP_MU="VLoose"
        FILENAME="${WP_JET}_vs_jets__${WP_MU}_vs_mu__${WP_ELE}_vs_ele__DM${DM}"
        OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}"
        python shapes/produce_shapes_fakerate.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 2 --num-threads 2 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection --skip-systematic-variations --control-plot-set pt_3 --wp_vs_jet ${WP_JET} --wp_vs_mu ${WP_MU} --wp_vs_ele ${WP_ELE} --decay_mode ${DM} --id_wp_ele Tight --id_wp_mu Tight

        WP_ELE="VLoose"
        WP_MU="Tight"
        FILENAME="${WP_JET}_vs_jets__${WP_MU}_vs_mu__${WP_ELE}_vs_ele__DM${DM}"
        OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}"
        python shapes/produce_shapes_fakerate.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 2 --num-threads 2 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection --skip-systematic-variations --control-plot-set pt_3 --wp_vs_jet ${WP_JET} --wp_vs_mu ${WP_MU} --wp_vs_ele ${WP_ELE} --decay_mode ${DM} --id_wp_ele Tight --id_wp_mu Tight

        WP_ELE="Tight"
        WP_MU="Tight"
        FILENAME="${WP_JET}_vs_jets__${WP_MU}_vs_mu__${WP_ELE}_vs_ele__DM${DM}"
        OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}"
        python shapes/produce_shapes_fakerate.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 2 --num-threads 2 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection --skip-systematic-variations --control-plot-set pt_3 --wp_vs_jet ${WP_JET} --wp_vs_mu ${WP_MU} --wp_vs_ele ${WP_ELE} --decay_mode ${DM} --id_wp_ele Tight --id_wp_mu Tight
    done
done