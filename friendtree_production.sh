#WH friendtree production
MODE=$1
NTUPLE_TAG=$2
NTUPLE_PATH=$3
FF_NTUPLE_TAG=$4
DATE=$5
WP_VS_JET=$6
WP_VS_LEP=$7
NTUPLE_TOT_PATH="root://cmsdcache-kit-disk.gridka.de/${NTUPLE_PATH}"
NTHREADS=30
source utils/setup_root.sh
if [[ $MODE == "XSEC" ]]; then
    #numberofgeneratedeventsweight, crosssectionpereventweight
    FRIEND="crosssection"
    FRIEND_PATH="root://cmsdcache-kit-disk.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FRIEND}/"
    #start xsec and eventweight friendtree production
    python friends/crosssection.py --basepath ${NTUPLE_TOT_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.json
fi
if [[ $MODE == "FF" ]]; then
#jetfakes rate, pass the wp_vs_jet argument for the tau_h (llt) or ss tau_h (ltt)
FRIEND="jetfakes_wpVSjet_${WP_VS_JET}_${DATE}"
FRIEND_PATH="root://cmsdcache-kit-disk.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FRIEND}/"
ERAS="2016preVFP,2016postVFP,2017,2018"
python friends/jet_fakerate.py --basepath ${NTUPLE_TOT_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.json --eras ${ERAS} --wp_vs_jets ${WP_VS_JET} --wp_vs_lep ${WP_VS_LEP} --corr_file_tau_18 friends/2018/jetfakes_lib_tau_${FF_NTUPLE_TAG}_${WP_VS_JET}vsJets_${DATE}.json --corr_file_mu_18 friends/2018/jetfakes_lib_mu_${FF_NTUPLE_TAG}_${DATE}.json --corr_file_ele_18 friends/2018/jetfakes_lib_ele_${FF_NTUPLE_TAG}_${DATE}.json --corr_file_tau_17 friends/2017/jetfakes_lib_tau_${FF_NTUPLE_TAG}_${WP_VS_JET}vsJets_${DATE}.json --corr_file_mu_17 friends/2017/jetfakes_lib_mu_${FF_NTUPLE_TAG}_${DATE}.json --corr_file_ele_17 friends/2017/jetfakes_lib_ele_${FF_NTUPLE_TAG}_${DATE}.json --corr_file_tau_16postVFP friends/2016postVFP/jetfakes_lib_tau_${FF_NTUPLE_TAG}_${WP_VS_JET}vsJets_${DATE}.json --corr_file_mu_16postVFP friends/2016postVFP/jetfakes_lib_mu_${FF_NTUPLE_TAG}_${DATE}.json --corr_file_ele_16postVFP friends/2016postVFP/jetfakes_lib_ele_${FF_NTUPLE_TAG}_${DATE}.json --corr_file_tau_16preVFP friends/2016preVFP/jetfakes_lib_tau_${FF_NTUPLE_TAG}_${WP_VS_JET}vsJets_${DATE}.json --corr_file_mu_16preVFP friends/2016preVFP/jetfakes_lib_mu_${FF_NTUPLE_TAG}_${DATE}.json --corr_file_ele_16preVFP friends/2016preVFP/jetfakes_lib_ele_${FF_NTUPLE_TAG}_${DATE}.json
fi