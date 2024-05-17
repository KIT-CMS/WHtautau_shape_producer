#!/bin/bash
set -e
NTUPLE_TAG=$1
ERA=$2

KINGMAKER_BASEDIR="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
KINGMAKER_BASEDIR_XROOTD=" root://cmsdcache-kit-disk.gridka.de/${KINGMAKER_BASEDIR}"
XSEC_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/crosssection/"
FF_FRIENDS="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/${FF_FRIEND_TAG}/"
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