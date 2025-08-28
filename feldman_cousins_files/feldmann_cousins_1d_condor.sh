#!/bin/bash
cd /work/rschmieder/WH_analysis/WHtautau_shape_producer
source utils/setup_cmssw.sh
ulimit -s unlimited
POINT=$1
echo $pwd
NTUPLE_TAG="14_04_25_alleras_allch3"
SHAPE_TAG="10_05_25_nn_fitshapes"
FIT_TAG="WpmH_RD"
BASE_PATH="output/datacard_output/${NTUPLE_TAG}/${SHAPE_TAG}_${FIT_TAG}"
DATACARD_OUTPUT="${BASE_PATH}/all_eras_all"
combine -M HybridNew --saveToys --saveHybridResult --LHCmode LHC-feldman-cousins --clsAcc 0 -n .r_WH_minus.${POINT} --singlePoint r_WH_minus=${POINT}  -T 1000 -s 1 -d $DATACARD_OUTPUT/cmb/workspace.root --redefineSignalPOIs r_WH_minus --setParameterRanges r_WH_plus=0.,5.:r_WH_minus=-1,1.
