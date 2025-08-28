#!/bin/bash
set -e
NTUPLE_TAG=$1
ERA=$2

KINGMAKER_BASEDIR="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
KINGMAKER_BASEDIR_XROOTD=" root://cmsdcache-kit-disk.gridka.de/${KINGMAKER_BASEDIR}"
XSEC_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/crosssection/"
FF_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FF_FRIEND_TAG}/"
NJETS_CLOSURE_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${NJETS_CLOSURE_FRIEND_TAG}/"
MET_CLOSURE_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${MET_CLOSURE_FRIEND_TAG}/"
MET_SHAPE_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FF_MET_SHAPE_FRIEND_TAG}"
PT_SHAPE_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FF_PT1_SHAPE_FRIEND_TAG}"
NN_SHAPE_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FF_NN_SHAPE_FRIEND_TAG}"

if [[ $NN_FRIEND_TAG == "None" ]]; then
    NN_FRIENDS=""
else
    NN_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${NN_FRIEND_TAG}/"
fi
echo $ERA 
if [[ $ERA == *"2016preVFP"* ]]; then
    NTUPLES=$KINGMAKER_BASEDIR
elif [[ $ERA == *"2016postVFP"* ]]; then
    NTUPLES=$KINGMAKER_BASEDIR
elif [[ $ERA == *"2017"* ]]; then
    NTUPLES=$KINGMAKER_BASEDIR
elif [[ $ERA == *"2018"* ]]; then
    NTUPLES=$KINGMAKER_BASEDIR
fi