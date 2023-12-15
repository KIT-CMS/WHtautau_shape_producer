# source utils/setup_cvmfs_sft.sh
source utils/setup_root.sh
export PYTHONPATH=$PYTHONPATH:$PWD/Dumbledraw


ERAS="2016preVFP 2016postVFP 2017 2018"
CHANNELS="emt"
NTUPLE_TAG="03_11_23_allch_alleras_shifts"
SHAPE_TAG="fit_shapes_ssTight_osTight_emt_met_comb_2016combcats"
REGIONS="control"
for ERA in $ERAS
do
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
        for REGION in $REGIONS
        do
            INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}.root"
            TAG="${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}"
            if [ "$REGION" = "control" ]; then
                for VAR in m_tt #m_vis pt_W pt_1 pt_2 pt_3
                do
                    python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} #--draw-jet-fake-variation tau_anti_iso #--normalize-by-bin-width
                    python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation #--draw-jet-fake-variation tau_anti_iso # --normalize-by-bin-width
                done
            else
                for VAR in m_tt #m_vis mjj njets pt_vis phi_2 eta_2 nbtag #pt_W m_tt m_vis pt_1 pt_2 pt_3
                do
                    python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} #--blinded #--draw-jet-fake-variation tau_anti_iso #--normalize-by-bin-width
                    python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation #--blinded #--draw-jet-fake-variation tau_anti_iso # --normalize-by-bin-width
                done
            fi
        done
    fi
done
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