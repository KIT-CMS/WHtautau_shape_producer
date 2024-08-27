# source utils/setup_cvmfs_sft.sh
source utils/setup_root.sh
export PYTHONPATH=$PYTHONPATH:$PWD/Dumbledraw

ERAS="2018" #2016preVFP 2016postVFP 2017 2018"
CHANNELS="eem" #"eem mme" # mmt"
NTUPLE_TAG="11_03_24_triggermatchDR05_FF"
SHAPE_TAG="fakerate_measurement_09_04_24_no_mt_cut"
for ERA in $ERAS
do
for CHANNEL in $CHANNELS
do
    if [ "$CHANNEL" = "eem" ]
    then
        for WP in Loose Tight
        do 
            INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/id_wp_mu_${WP}.root"
            TAG="${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/id_wp_mu_${WP}"
            for VAR in pt_3 met mt_3 pt_1 #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
            do
                python plotting/plot_shapes_control_eem_mme.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation #--normalize-by-bin-width
            done
        done 
    elif [ "$CHANNEL" = "mme" ]
    then 
        for WP in Loose Tight
        do     
            INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/id_wp_ele_${WP}.root"
            TAG="${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/id_wp_ele_${WP}"
            for VAR in pt_3 met mt_3 pt_1 #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
            do
                python plotting/plot_shapes_control_eem_mme.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation #--normalize-by-bin-width
            done
        done 
    else 
        for WP in VVVLoose Tight
        do     
            INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/TightvsJets/${WP}_vs_jets__Tight_vs_mu__Tight_vs_ele__DM0.root"
            TAG="${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/TightvsJets/${WP}_vs_jets__Tight_vs_mu__Tight_vs_ele_DM0"
            for VAR in pt_3 #m_vis pt_1 pt_2 m_vis mjj njets pt_vis phi_2 eta_2 phi_1 nbtag met_uncorrected pfmet pfmet_uncorrected metphi metphi_uncorrected pfmetphi pfmetphi_uncorrected
            do
                python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation --normalize-by-bin-width
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