MODE=$1
NTUPLE_TAG="26_02_25_ff"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FRIEND_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/"
ERAS="2018"
#ERAS="2016postVFP"
ulimit -s unlimited
#for jet to tau fake shapes
WP_VS_JET="Medium"
WP_VS_ELE="Medium"
WP_VS_MU="Medium"
DATE="24_03_25_${WP_VS_JET}vsJetsvsL"
#only needed for closure correction: if you calculate first order closure, than only pass the FF friend. If you calculate nth order, you have to pass all closure friends"
FF_FRIEND_TAG="${FRIEND_PATH}jetfakes_wpVSjet_${WP_VS_JET}_30_08_24_${WP_VS_JET}vsJetsvsL" 
NJETS_CLOSURE_FRIEND_TAG="${FRIEND_PATH}jetfakes_wpVSjet_${WP_VS_JET}_11_10_24_${WP_VS_JET}vsJetsvsL_measure_njetclosure" 
MET_CLOSURE_FRIEND_TAG="${FRIEND_PATH}jetfakes_wpVSjet_${WP_VS_JET}_11_10_24_${WP_VS_JET}vsJetsvsL_measure_metclosure" 
#check variations.py if you do closure shapes because of the vsjet wp
#check do_estiamtions.py if you do closure shapes: change if channel not in ["ett", "mtt", "eem", "mme"]: to if channel not in ["ett", "mtt", "mmt", "eem", "mme"]:
if [[ $MODE == "JET_SHAPES" ]]; then
    for ERA in $ERAS
    do
        for WP_MU in $WP_VS_MU
        do
            for WP_ELE in $WP_VS_ELE
            do 
                bash jet_to_tau_fakerate_shapes.sh $NTUPLE_TAG $NTUPLE_PATH $FRIEND_PATH $ERA $DATE $WP_VS_JET $WP_ELE $WP_MU "FF"
            done
        done
    done
fi
if [[ $MODE == "LEPTON_SHAPES" ]]; then
    for ERA in $ERAS
    do
        bash jet_to_lepton_fakerate_shapes.sh $NTUPLE_TAG $NTUPLE_PATH $FRIEND_PATH $ERA $DATE "FF"
    done
fi
if [[ $MODE == "FF_CALC" ]]; then
    for ERA in $ERAS
    do
        bash jet_fakerate_calculation.sh $NTUPLE_TAG $ERA $DATE $WP_VS_JET $WP_VS_ELE $WP_VS_MU "FF"
    done
fi
if [[ $MODE == "CLOSURE_SHAPES" ]]; then
    for ERA in $ERAS
    do
        for WP_MU in $WP_VS_MU
        do
            for WP_ELE in $WP_VS_ELE
            do 
                echo $WP_MU $WP_ELE
                bash jet_to_tau_fakerate_shapes.sh $NTUPLE_TAG $NTUPLE_PATH $FRIEND_PATH $ERA $DATE $WP_VS_JET $WP_ELE $WP_MU "CLOSURE" ${FF_FRIEND_TAG} ${NJETS_CLOSURE_FRIEND_TAG} ${MET_CLOSURE_FRIEND_TAG}
            done
        done
        bash jet_to_lepton_fakerate_shapes.sh $NTUPLE_TAG $NTUPLE_PATH $FRIEND_PATH $ERA $DATE "CLOSURE" ${FF_FRIEND_TAG} ${NJETS_CLOSURE_FRIEND_TAG} ${MET_CLOSURE_FRIEND_TAG}
    done
fi
if [[ $MODE == "CLOSURE_CALC" ]]; then
    for ERA in $ERAS
    do
        bash jet_fakerate_calculation.sh $NTUPLE_TAG $ERA $DATE $WP_VS_JET $WP_VS_ELE $WP_VS_MU "CLOSURE"
    done
fi