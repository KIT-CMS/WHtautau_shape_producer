#WH jet to lepton fake rate shapes
#the arguments --wp_vs_jet --wp_vs_mu --wp_vs_ele --decay_mode and --id_wp_ele/mu are not relevant for the shapes for jet to mu/ele 
source utils/setup_root.sh

TAG="09_02_eem_mme_2"
NTUPLE_PATH="/work/rschmieder/WH_analysis/WHtautau_shape_producer/temp_ntuples_friends/${TAG}/ntuples"
FRIEND_PATH="/work/rschmieder/WH_analysis/WHtautau_shape_producer/temp_ntuples_friends/${TAG}/friends"
ERA="2018"

#jet to electron fakerate shapes
CHANNEL="mme"
OUTPUT_DIR="output/shapes/${TAG}/${CHANNEL}/fakerate_measurement2"
mkdir -p ${OUTPUT_DIR}

for IDWP_ELE in Loose Tight
do
    echo "id_wp_ele: $IDWP_ELE"
    FILENAME="id_wp_ele_${IDWP_ELE}"
    OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}"
    python shapes/produce_shapes_fakerate.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 2 --num-threads 2 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection --skip-systematic-variations --control-plot-set pt_3,mt_3,met --wp_vs_jet VTight --wp_vs_mu Tight --wp_vs_ele Tight --decay_mode 0 --id_wp_ele $IDWP_ELE --id_wp_mu 1
    #pt_3,mt_3,met,m_vis,pt_1,pt_2,m_vis,mjj,njets,pt_vis,phi_2,eta_2,phi_1,nbtag,met_uncorrected,pfmet,pfmet_uncorrected,metphi,metphi_uncorrected,pfmetphi,pfmetphi_uncorrected --wp_vs_jet VTight --wp_vs_mu Tight --wp_vs_ele Tight --decay_mode 0 --id_wp_ele $IDWP_ELE --id_wp_mu 1
done

#jet to muon fakerate shapes
CHANNEL="eem"
ERA="2018"
OUTPUT_DIR="output/shapes/${TAG}/${CHANNEL}/fakerate_measurement2"
mkdir -p ${OUTPUT_DIR}

for IDWP_MU in Loose Tight
do
    echo "id_wp_mu: $IDWP_MU"
    FILENAME="id_wp_mu_${IDWP_MU}"
    OUTPUT_FILE="${OUTPUT_DIR}/${FILENAME}"
    python shapes/produce_shapes_fakerate.py --channels ${CHANNEL} --output-file ${OUTPUT_FILE} --directory ${NTUPLE_PATH}  --era ${ERA} --num-processes 2 --num-threads 2 --optimization-level 1 --control-plots --ntuple_type crown --${CHANNEL}-friend-directory ${FRIEND_PATH}/crosssection --skip-systematic-variations --control-plot-set pt_3,mt_3,met --wp_vs_jet VTight --wp_vs_mu Tight --wp_vs_ele Tight --decay_mode 0 --id_wp_ele 1 --id_wp_mu $IDWP_MU
    #pt_3,mt_3,met,m_vis,pt_1,pt_2,m_vis,mjj,njets,pt_vis,phi_2,eta_2,phi_1,nbtag,met_uncorrected,pfmet,pfmet_uncorrected,metphi,metphi_uncorrected,pfmetphi,pfmetphi_uncorrected --wp_vs_jet VTight --wp_vs_mu Tight --wp_vs_ele Tight --decay_mode 0 --id_wp_ele 1 --id_wp_mu $IDWP_MU
done