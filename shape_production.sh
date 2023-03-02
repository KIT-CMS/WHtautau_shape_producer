#shape production to plots
source utils/setup_root.sh

TAG="27_01_all_ch"
NTUPLE_PATH="/work/rschmieder/WH_analysis/WHtautau_shape_producer/temp_ntuples_friends/${TAG}/ntuples"
CHANNELS="emt met mmt"
FILENAME="control_region_q1q2os_noq3"
ERA="2018"
#shape production
for CHANNEL in $CHANNELS
do
OUTPUT_FILE="output/shapes/${TAG}/${CHANNEL}/${FILENAME}"
mkdir -p output/shapes/${TAG}/${CHANNEL}
python shapes/produce_shapes.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory /work/rschmieder/WH_analysis/WHtautau_shape_producer/temp_ntuples_friends/${TAG}/friends/crosssection /work/rschmieder/WH_analysis/WHtautau_shape_producer/temp_ntuples_friends/${TAG}/friends/jetfakes --skip-systematic-variations --control-plot-set pt_W_lt,m_tt_lt,pt_3,pt_1,pt_2 #,m_vis,pt_1,pt_2,mjj,njets,pt_vis,phi_2,eta_2,nbtag #--process-selection wz,ggzz,zz,data,rem_vh,www,wzz,wwz,zzz,rem_ttbar
#jetfakes estimation
bash shapes/do_estimations.sh ${ERA} ${OUTPUT_FILE}.root 0 
done


