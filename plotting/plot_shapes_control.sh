source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh
NAME="control_region_q1q2os_noq3"
ERA="2018"
CHANNELS="emt met mmt"
for CHANNEL in $CHANNELS
do
    if [ "$CHANNEL" = "ett" ] || [ "$CHANNEL" = "mtt" ]
    then
        INPUT="output/shapes/27_01_all_ch/${CHANNEL}/${NAME}.root"
        TAG="27_01_all_ch/${CHANNEL}/${NAME}"
        for VAR in m_tt_tt pt_W_tt pt_3 #m_vis pt_1 pt_2 pt_3 m_vis mjj njets pt_vis phi_2 eta_2 nbtag
        do
            python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}
            python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation
        done
    elif [ "$CHANNEL" = "eem" ]
    then
        for WP in Loose Tight
        do 
            NAME="id_wp_mu_${WP}_wo_mtcut_only_single_ele_data"
            INPUT="output/shapes/09_02_eem_mme_2/${CHANNEL}/control_shapes/${NAME}.root"
            TAG="09_02_eem_mme_2/${CHANNEL}/${NAME}_incl_red_bkg_nbbwidth"
            for VAR in pt_3 mt_3 met #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
            do
                python plotting/plot_shapes_control_eem_mme.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation --normalize-by-bin-width
            done
        done 
    elif [ "$CHANNEL" = "mme" ]
    then 
        for WP in Loose Tight
        do     
            NAME="id_wp_ele_${WP}_wo_mtcut_only_single_mu_data"
            INPUT="output/shapes/09_02_eem_mme_2/${CHANNEL}/control_shapes/${NAME}.root"
            TAG="09_02_eem_mme_2/${CHANNEL}/${NAME}_incl_red_bkg_nbbwidth"
            for VAR in pt_3 mt_3 met #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
            do
                python plotting/plot_shapes_control_eem_mme.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation --normalize-by-bin-width
            done
        done 
    else 
        INPUT="output/shapes/27_01_all_ch/${CHANNEL}/${NAME}.root"
        TAG="27_01_all_ch/${CHANNEL}/${NAME}"
        for VAR in pt_W_lt m_tt_lt pt_3 pt_1 pt_2 #m_vis pt_1 pt_2 pt_3 m_vis mjj njets pt_vis phi_2 eta_2 nbtag
        do
            python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} #--draw-jet-fake-variation tau_anti_iso #--normalize-by-bin-width
            python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation #--draw-jet-fake-variation tau_anti_iso # --normalize-by-bin-width
        done
    
    fi
done
