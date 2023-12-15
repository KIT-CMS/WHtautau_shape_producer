#WH friendtree production
MODE=$1
NTUPLE_TAG=$2
NTUPLE_PATH=$3
ERA=$4
DATE=$5

NTHREADS=25
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh
if [[ $MODE == "XSEC" ]]; then
    #numberofgeneratedeventsweight, crosssectionpereventweight
    FRIEND="crosssection"
    FRIEND_PATH="root://cmsxrootd-kit-disk.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FRIEND}/"
    #start xsec and eventweight friendtree production
    python friends/crosssection.py --basepath ${NTUPLE_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.yaml
fi
if [[ $MODE == "FF" ]]; then
#jetfakes rate, pass the wp_vs_jet argument for the tau_h (llt) or ss tau_h (ltt)
WP_VS_JET="Tight"
FRIEND="jetfakes_wpVSjet_${WP_VS_JET}_${DATE}"
FRIEND_PATH="root://cmsxrootd-kit-disk.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FRIEND}/"
ERAS="2016preVFP,2016postVFP,2017,2018"
#start jetfakes friendtree production
python friends/jet_fakerate.py --basepath ${NTUPLE_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.yaml --eras ${ERAS} --wp_vs_jets ${WP_VS_JET} --corr_file_tau_18 friends/2018/jetfakes_lib_tau_${NTUPLE_TAG}_TightvsJets_${DATE}.json --corr_file_mu_18 friends/2018/jetfakes_lib_mu_${NTUPLE_TAG}_${DATE}.json --corr_file_ele_18 friends/2018/jetfakes_lib_ele_${NTUPLE_TAG}_${DATE}.json --corr_file_tau_17 friends/2017/jetfakes_lib_tau_${NTUPLE_TAG}_TightvsJets_${DATE}.json --corr_file_mu_17 friends/2017/jetfakes_lib_mu_${NTUPLE_TAG}_${DATE}.json --corr_file_ele_17 friends/2017/jetfakes_lib_ele_${NTUPLE_TAG}_${DATE}.json --corr_file_tau_16postVFP friends/2016postVFP/jetfakes_lib_tau_${NTUPLE_TAG}_TightvsJets_${DATE}.json --corr_file_mu_16postVFP friends/2016postVFP/jetfakes_lib_mu_${NTUPLE_TAG}_${DATE}.json --corr_file_ele_16postVFP friends/2016postVFP/jetfakes_lib_ele_${NTUPLE_TAG}_${DATE}.json --corr_file_tau_16preVFP friends/2016preVFP/jetfakes_lib_tau_${NTUPLE_TAG}_TightvsJets_${DATE}.json --corr_file_mu_16preVFP friends/2016preVFP/jetfakes_lib_mu_${NTUPLE_TAG}_${DATE}.json --corr_file_ele_16preVFP friends/2016preVFP/jetfakes_lib_ele_${NTUPLE_TAG}_${DATE}.json
fi