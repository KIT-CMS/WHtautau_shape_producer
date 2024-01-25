source utils/setup_cmssw.sh

ulimit -s unlimited
#script to combine datacards
MODE=$1
if [[ $MODE == "COMBINE_DATACARDS" ]]; then
    GLOB_WW="/work/rschmieder/WH_analysis/datacards_WH_comb/wh_charge_asymmetry_combination/WW/2023_12_11"
    GLOB_TT="/work/rschmieder/WH_analysis/datacards_WH_comb/wh_charge_asymmetry_combination/TT/2023_12_20"
    ERAS="2018"
    for ERA in $ERAS
    do 
        python script_combine_datacards_TT_WW.py --era ${ERA} --global_path_ww ${GLOB_WW} --global_path_tt ${GLOB_TT}
    done
fi
if [[ $MODE == "COMBINED_FIT" ]]; then
    echo "-----------------------------------"
    echo "perform combined fit"
    echo "-----------------------------------"
    DATACARD_NAME="Combination/WH_chargeAsymmetry_WH_FullRun2_100_bins_original_signal_scale"
    OUTPUT="Combination/fullRun2_WW_TT_combined.txt"
    python script_workspace_and_fit.py --datacard_name ${DATACARD_NAME} --output_name ${OUTPUT}
fi