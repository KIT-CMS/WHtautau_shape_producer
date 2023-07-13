#WH friendtree production
# TAG="11_07_shifts_all_ch"
# #NTUPLE_PATH="/ceph/rschmieder/WH_analysis/ntuple_sets/${TAG}/ntuples"
NTUPLE_TAG="11_07_shifts_all_ch"
NTUPLE_PATH="root://cmsxrootd-kit.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
NTHREADS=20

#numberofgeneratedeventsweight, crosssectionpereventweight
FRIEND="crosssection"
FRIEND_PATH="root://cmsxrootd-kit.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FRIEND}/"

#environment
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

#start xsec and eventweight friendtree production
#python friends/crosssection.py --basepath ${NTUPLE_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.yaml


#jetfakes rate
FRIEND="jetfakes_incl_bveto_ortho_det_reg_AN_binning_unc"
FRIEND_PATH="root://cmsxrootd-kit.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FRIEND}/"

#start jetfakes friendtree production
python friends/jet_fakerate.py --basepath ${NTUPLE_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.yaml --corr_file_tau friends/jetfakes_lib_tau_incl_bveto_ortho_det_reg_AN_binning_unc.json --corr_file_mu friends/jetfakes_lib_mu_incl_bveto_ortho_det_reg_unc.json --corr_file_ele friends/jetfakes_lib_ele_incl_bveto_ortho_det_reg_unc.json 