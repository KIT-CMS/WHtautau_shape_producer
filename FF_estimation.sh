MODE=$1
NTUPLE_TAG="31_05_24_ff_ntuples_2"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FRIEND_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/"
ERAS="2016preVFP 2016postVFP 2017 2018"
#ERAS="2016postVFP"
ulimit -s unlimited
DATE="19_08_24_mediumvsj_tightvsl"
#for jet to tau fake shapes
WP_VS_JET="Medium"
WP_VS_ELE="Tight,VLoose"
WP_VS_MU="Tight,VLoose"
#if you want to change the TauvsJets WP you have to change the scripts: 
#jet_to_tau_fakerate_shapes.sh
#jet_fakerate_caluclation.sh
#friendtree_production.sh
#config/shapes/channel_selection_fakerate.py (cause of the loose selection)
if [[ $MODE == "JET_SHAPES" ]]; then
    for ERA in $ERAS
    do
        for WP_MU in $WP_VS_MU
        do
            for WP_ELE in $WP_VS_ELE
            do 
                bash jet_to_tau_fakerate_shapes.sh $NTUPLE_TAG $NTUPLE_PATH $FRIEND_PATH $ERA $DATE $WP_VS_JET $WP_ELE $WP_MU 
            done
        done
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
        bash jet_fakerate_calculation.sh $NTUPLE_TAG $ERA $DATE $WP_VS_JET $WP_VS_ELE $WP_VS_MU 
    done
fi
