#shape production to plots
source utils/setup_root.sh

NTUPLE_TAG="shifts_mmt_10_05"
NTUPLE_PATH="/ceph/rschmieder/WH_analysis/ntuple_sets/${NTUPLE_TAG}/ntuples"
CHANNELS="mmt"
SHAPE_TAG="ptW_mtt_ff_unc2"
FILENAME="signal_region3"
ERA="2018"

#shape production
for CHANNEL in $CHANNELS
do
OUTPUT_FILE="output/shapes/${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}/${FILENAME}"
mkdir -p output/shapes/${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}
python shapes/produce_shapes.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory /ceph/rschmieder/WH_analysis/friend_sets/${NTUPLE_TAG}/friends/crosssection /ceph/rschmieder/WH_analysis/friend_sets/${NTUPLE_TAG}/friends/jetfakes_incl_bveto_ortho_det_reg_AN_binning_unc2 --control-plot-set pt_W,m_tt,pt_1,pt_2,pt_3 #--skip-systematic-variations#,m_vis,pt_1,pt_2,mjj,njets,pt_vis,phi_2,eta_2,nbtag #--process-selection wz,ggzz,zz,data,rem_vh,www,wzz,wwz,zzz,rem_ttbar

# # #jetfakes estimation
bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 

#synced shapes for fit
#bash shapes/convert_to_synced_shapes.sh ${ERA} ${CHANNEL} ${NTUPLE_TAG} ${SHAPE_TAG} ${OUTPUT_FILE}.root
done


