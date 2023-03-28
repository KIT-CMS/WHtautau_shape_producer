#WH friendtree production
TAG="27_01_all_ch"
NTUPLE_PATH="/work/rschmieder/WH_analysis/WHtautau_shape_producer/temp_ntuples_friends/${TAG}/ntuples"
NTHREADS=20

#numberofgeneratedeventsweight, crosssectionpereventweight
FRIEND="crosssection"
FRIEND_PATH="/ceph/rschmieder/WH_analysis/friend_sets/${TAG}/friends/${FRIEND}/"

#environment
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

#start xsec and eventweight friendtree production
#python friends/crosssection.py --basepath ${NTUPLE_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.yaml --remove_empty_ntuples


#jetfakes rate
FRIEND="jetfakes_incl_bveto_ortho_det_reg"
FRIEND_PATH="/ceph/rschmieder/WH_analysis/friend_sets/${TAG}/friends/${FRIEND}/"

#start jetfakes friendtree production
python friends/jet_fakerate.py --basepath ${NTUPLE_PATH} --outputpath ${FRIEND_PATH} --nthreads ${NTHREADS} --dataset-config /work/rschmieder/WH_analysis/KingMaker/sample_database/datasets.yaml --corr_file_tau friends/jetfakes_lib_tau_incl_bveto_ortho_det_reg.json --corr_file_mu friends/jetfakes_lib_mu_incl_bveto_ortho_det_reg.json --corr_file_ele friends/jetfakes_lib_ele_incl_bveto_ortho_det_reg.json --remove_empty_ntuples