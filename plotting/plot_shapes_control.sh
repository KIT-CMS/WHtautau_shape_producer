# source utils/setup_cvmfs_sft.sh
source utils/setup_root.sh
export PYTHONPATH=$PYTHONPATH:$PWD/Dumbledraw

NTUPLE_TAG="31_05_24_ff_ntuples_2"
NTUPLE_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNRun/"
FRIEND_PATH="/store/user/rschmieder/CROWN/ntuples/${NTUPLE_TAG}/CROWNFriends/"
ERAS="2016preVFP 2016postVFP 2017"
CHANNELS="mme"
SHAPE_TAG="fakerate_measurement_12_07_24_mt_control"
REGIONS="Loose Tight"
PLOT_CATS="diboson misc"
for ERA in $ERAS
do
for CHANNEL in $CHANNELS
do
    for REGION in $REGIONS
    do
        INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/id_wp_ele_${REGION}.root"
        TAG="${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${REGION}"
        #if [ "$REGION" = "control" ]; then
            for VAR in mt_3 #m_vis pt_W pt_1 pt_2 pt_3
            do
                #python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG} #--draw-jet-fake-variation tau_anti_iso #--normalize-by-bin-width
                python plotting/plot_shapes_control_eem_mme.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation #--draw-jet-fake-variation tau_anti_iso # --normalize-by-bin-width
            done
        # else
        #     echo "hi"
        #     for VAR in predicted_max_value #m_vis mjj njets pt_vis phi_2 eta_2 nbtag #pt_W m_tt m_vis pt_1 pt_2 pt_3
        #     do
        #         for PLOT_CAT in $PLOT_CATS
        #         do 
        #             python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}  --category-postfix $PLOT_CAT #--blinded #--draw-jet-fake-variation tau_anti_iso #--normalize-by-bin-width
        #             python plotting/plot_shapes_control.py -l --era Run${ERA} --input ${INPUT} --variables ${VAR} --channels ${CHANNEL} --tag ${TAG}_simulation --simulation --category-postfix $PLOT_CAT #--blinded #--draw-jet-fake-variation tau_anti_iso # --normalize-by-bin-width
        #         done
        #     done
        #fi
    done
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