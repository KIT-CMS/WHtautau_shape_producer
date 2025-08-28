# source utils/setup_cvmfs_sft.sh
source utils/setup_root.sh
export PYTHONPATH=$PYTHONPATH:$PWD/Dumbledraw

ERAS="2018"
CHANNELS="mmt" # mmt"
NTUPLE_TAG="26_02_25_ff"
WP_VS_JET="Medium"
SHAPE_TAG="fakerate_measurement_24_03_25_MediumvsJetsvsL"

for ERA in $ERAS
do
for CHANNEL in $CHANNELS
do
    if [ "$CHANNEL" = "eem" ]
    then
        for WP in Tight
        do 
            INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/id_wp_mu_${WP}.root"
            TAG="${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/id_wp_mu_${WP}"
            for VAR in pt_3 #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
            do
                python plotting/plot_shapes_control_eem_mme.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} #--simulation #--normalize-by-bin-width
            done
        done 
    elif [ "$CHANNEL" = "mme" ]
    then 
        for WP in Tight
        do     
            INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/id_wp_ele_${WP}.root"
            TAG="${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/id_wp_ele_${WP}"
            for VAR in pt_3 #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
            do
                python plotting/plot_shapes_control_eem_mme.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} #--simulation #--normalize-by-bin-width
            done
        done 
    else 
        for WP in ${WP_VS_JET}
        do     
            for DM in 0
            do
                INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${WP_VS_JET}vsJets/VVVLoose_vs_jets__${WP}_vs_mu__${WP}_vs_ele__DM${DM}.root"
                TAG="${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${WP_VS_JET}vsJets/VVVLoose_vs_jets__${WP}_vs_mu__${WP}_vs_ele__DM${DM}"
                for VAR in pt_3  #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
                do
                    # python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation --normalize-by-bin-width
                    python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} --simulation #--normalize-by-bin-width
                done
            done
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