source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh
ERA="2018"
CHANNELS="mmt emt met mtt ett"
NTUPLE_TAG="11_07_shifts_all_ch"
SHAPE_TAG="ptW_mtt"
FILENAME="signal_region"
for CHANNEL in $CHANNELS
do
    if [ "$CHANNEL" = "eem" ]
    then
        for WP in Loose Tight
        do 
            FILENAME="id_wp_mu_${WP}"
            INPUT="output/shapes/09_02_eem_mme_2/${CHANNEL}/fakerate_measurement_incl_bveto_ortho_det_reg/${FILENAME}.root"
            TAG="09_02_eem_mme_2/${CHANNEL}/${FILENAME}_incl_red_bkg_nbbwidth_incl_bveto_ortho_det_reg_AN_binning"
            for VAR in pt_3 mt_3 met #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
            do
                python plotting/plot_shapes_control_eem_mme.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation --normalize-by-bin-width
            done
        done 
    elif [ "$CHANNEL" = "mme" ]
    then 
        for WP in Loose Tight
        do     
            FILENAME="id_wp_ele_${WP}"
            INPUT="output/shapes/09_02_eem_mme_2/${CHANNEL}/fakerate_measurement_incl_bveto_ortho_det_reg/${FILENAME}.root"
            TAG="09_02_eem_mme_2/${CHANNEL}/${FILENAME}_incl_red_bkg_nbbwidth_incl_bveto_ortho_det_reg_AN_binning"
            for VAR in pt_3 mt_3 met #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
            do
                python plotting/plot_shapes_control_eem_mme.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation --normalize-by-bin-width
            done
        done 
    else 
        INPUT="output/shapes/${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}/${FILENAME}.root"
        TAG="${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}/${FILENAME}"
        for VAR in pt_W m_tt #m_vis pt_1 pt_2 pt_3 m_vis mjj njets pt_vis phi_2 eta_2 nbtag
        do
            python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} --blinded #--draw-jet-fake-variation tau_anti_iso #--normalize-by-bin-width
            python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation --blinded #--draw-jet-fake-variation tau_anti_iso # --normalize-by-bin-width
        done
    
    fi
done
# CHANNEL="mmt"
# VAR="pt_3"
# for WP in VTight VVVLoose
# do 
#     FILENAME="${WP}_vs_jets__Tight_vs_mu__Tight_vs_ele__DM0"
#     INPUT="output/shapes/${NTUPLE_TAG}/${CHANNEL}/fakerate_measurement_incl_bveto_ortho_det_reg_AN_binning/${FILENAME}.root"
#     TAG="${NTUPLE_TAG}/${CHANNEL}/${FILENAME}_incl_bveto_ortho_det_reg_AN_binning"
#     python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation --normalize-by-bin-width
# done