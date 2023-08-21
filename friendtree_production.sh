#WH friendtree production
# TAG="11_07_shifts_all_ch"
# #NTUPLE_PATH="/ceph/rschmieder/WH_analysis/ntuple_sets/${TAG}/ntuples"
NTUPLE_TAG="11_08_emb_sf_17_18"
NTUPLE_PATH="root://cmsxrootd-kit.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
NTHREADS=25

#numberofgeneratedeventsweight, crosssectionpereventweight
FRIEND="crosssection"
FRIEND_PATH="root://cmsxrootd-kit.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FRIEND}/"

#environment
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

#start xsec and eventweight friendtree production
#python friends/crosssection.py --basepath ${NTUPLE_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.yaml


#jetfakes rate
FRIEND="jetfakes_incl_bveto_ortho_det_reg_AN_binning_unc_emb_sfs_test"
FRIEND_PATH="root://cmsxrootd-kit.gridka.de//store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FRIEND}/"

#start jetfakes friendtree production
python friends/jet_fakerate.py --basepath ${NTUPLE_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.yaml --eras 2017,2018 --corr_file_tau_18 friends/jetfakes_lib_tau_incl_bveto_ortho_det_reg_AN_binning_prefirewgt_emb_sfs_2018.json --corr_file_mu_18 friends/jetfakes_lib_mu_incl_bveto_ortho_det_reg_prefirewgt_emb_sfs_2018.json --corr_file_ele_18 friends/jetfakes_lib_ele_incl_bveto_ortho_det_reg_prefirewgt_emb_sfs_2018.json --corr_file_tau_17 friends/jetfakes_lib_tau_incl_bveto_ortho_det_reg_AN_binning_prefirewgt_2017.json --corr_file_mu_17 friends/jetfakes_lib_mu_incl_bveto_ortho_det_reg_prefirewgt_2017.json --corr_file_ele_17 friends/jetfakes_lib_ele_incl_bveto_ortho_det_reg_prefirewgt_2017.json --debug