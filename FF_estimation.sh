MODE=$1
NTUPLE_TAG="06_05_24_FF_ntuples"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FRIEND_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/"
ERAS="2016preVFP 2016postVFP 2017 2018"
#ERAS="2016postVFP"
ulimit -s unlimited
DATE="07_05_24"
#if you want to change the TauvsJets WP you have to change the scripts: 
#jet_to_tau_fakerate_shapes.sh
#jet_fakerate_caluclation.sh
#friendtree_production.sh
#config/shapes/channel_selection_fakerate.py (cause of the loose selection)
if [[ $MODE == "JET_SHAPES" ]]; then
    for ERA in $ERAS
    do
        bash jet_to_tau_fakerate_shapes.sh $NTUPLE_TAG $NTUPLE_PATH $FRIEND_PATH $ERA $DATE
    done
fi
if [[ $MODE == "LEPTON_SHAPES" ]]; then
    for ERA in $ERAS
    do
        bash jet_to_lepton_fakerate_shapes.sh $NTUPLE_TAG $NTUPLE_PATH $FRIEND_PATH $ERA $DATE
    done
fi
if [[ $MODE == "FF_CALC" ]]; then
    for ERA in $ERAS
    do
        bash jet_fakerate_calculation.sh $NTUPLE_TAG $ERA $DATE
    done
fi
