#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc900
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

pushd CMSSW_11_3_4/src
eval `scramv1 runtime -sh`
popd
