### Setup of CMSSW release
CMSSW=CMSSW_11_3_4

export SCRAM_ARCH=slc7_amd64_gcc900
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

scramv1 project $CMSSW; pushd $CMSSW/src
eval `scramv1 runtime -sh`

# combine on 102X slc7
git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v9.0.1
cd -

# CombineHarvester (current master for 102X)
git clone git@github.com:cms-analysis/CombineHarvester.git CombineHarvester

# SM analysis specific code
git clone git@github.com:KIT-CMS/SMRun2Legacy.git CombineHarvester/SMRun2Legacy

# compile everything
# Build
CORES=`grep -c ^processor /proc/cpuinfo`
scramv1 b clean; scramv1 b -j $CORES