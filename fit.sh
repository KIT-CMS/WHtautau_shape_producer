# MODE options are: PRINT (print fit results), FIT, POSTFIT (produces postfit and prefit shapes), PLOT
MODE="$1"
CHANNELS="all"
ERA="2018"
#NTUPLE_TAG="11_07_shifts_all_ch"
NTUPLE_TAG="11_07_shifts_all_ch"
SHAPE_TAG="ptW_mtt_AN_ptW_binning"
SYNCED_DIR_EMT=output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/synced_shapes
SYNCED_DIR_MMT=output/shapes/${NTUPLE_TAG}/${ERA}/mmt/${SHAPE_TAG}/synced_shapes
SYNCED_DIR_MET=output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG}/synced_shapes
SYNCED_DIR_ETT=output/shapes/${NTUPLE_TAG}/${ERA}/ett/${SHAPE_TAG}/synced_shapes
SYNCED_DIR_MTT=output/shapes/${NTUPLE_TAG}/${ERA}/mtt/${SHAPE_TAG}/synced_shapes
BASE_PATH="output/datacard_output/${NTUPLE_TAG}/${SHAPE_TAG}_incl_mtt_control"
if [[ $MODE == "PRINT" ]]; then
    source utils/setup_cmssw.sh 
    for CHANNEL in $CHANNELS
    do
        DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}"
        echo $MODE
        for RESDIR in $DATACARD_OUTPUT/cmb; do
                echo "[INFO] Printing fit result for category $(basename $RESDIR)"
                FITFILE=${RESDIR}/higgsCombine${ERA}.MultiDimFit.mH125.root
                python print_fitresult.py ${FITFILE}
        done
done
fi
if [[ $MODE == "FIT" ]]; then
    for CHANNEL in $CHANNELS
    do
        DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}"
        echo $MODE    
        source utils/setup_cmssw.sh    
        ${CMSSW_BASE}/bin/slc7_amd64_gcc900/MorphingSMRun2Legacy \
            --base_path=$PWD \
            --input_folder_emt=$SYNCED_DIR_EMT \
            --input_folder_met=$SYNCED_DIR_MET \
            --input_folder_mmt=$SYNCED_DIR_MMT \
            --input_folder_ett=$SYNCED_DIR_ETT \
            --input_folder_mtt=$SYNCED_DIR_MTT \
            --real_data=false \
            --classic_bbb=false \
            --binomial_bbb=false \
            --jetfakes=1 \
            --embedding=0 \
            --channel=${CHANNEL} \
            --auto_rebin=false \
            --stxs_signals="stxs_stage0" \
            --categories="stxs_stage0" \
            --era=${ERA} \
            --output=${DATACARD_OUTPUT} \
            --use_automc=false \
            --train_ff=1 \
            --train_stage0=1\
            --train_emb=1
        THIS_PWD=${PWD}
        echo $THIS_PWD
        cd ${DATACARD_OUTPUT}
        for FILE in */*.txt; do
            sed -i '$s/$/\n * autoMCStats 0.0/' $FILE
        done
        cd $THIS_PWD

        echo "[INFO] Create Workspace for datacard"
        # combineTool.py -M T2W -i output/$datacard_output/htt_$channel_*/ -o workspace.root --parallel 4 -m 125
        python --version
        echo $DATACARD_OUTPUT/$CHANNEL
        combineTool.py -M T2W -o workspace.root -i $DATACARD_OUTPUT/cmb -m 125 \
            -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
            --PO verbose \
            --PO 'map=.*/WHplus.?$:r[1,-10,10]' \
            --PO 'map=.*/WHminus.?$:r'
            #  --PO '"map=^.*/WH.?$:r_WH[1,-10,10]"' \
            # --PO '"map=^.*/rem_VH.?$:r_rem_VH[1,0.99,1.01]"' \
            # --PO '"map=^.*/WHplus.?$:r_WHplus=expr;;r_WHplus(\"@0*(1+@1)/(2*0.8380)\",r_S[1.3693,0.01,5],r_A[0.224,-1,1])"' \
            # --PO '"map=^.*/WHminus.?$:r_WHminus=expr;;r_WHminus(\"@0*(1-@1)/(2*0.5313)\",r_S,r_A)"' \
            # --PO '"map=^.*/WHplus.?$:r_WHplus[0.831,-200,200]"' \
            # --PO '"map=^.*/WHminus.?$:r_WHminus[0.527,-200,200]"'

        source utils/setup_cmssw.sh
        combineTool.py \
        -M MultiDimFit \
        -m 125 \
        -d $DATACARD_OUTPUT/cmb/workspace.root \
        --algo singles \
        --robustFit 1 \
        --X-rtd MINIMIZER_analytic \
        --cminDefaultMinimizerStrategy 0 \
        --setParameters r=1.0 \
        --setParameterRanges r=-10,10 \
        --redefineSignalPOIs r \
        -n $ERA -v1 \
        -t -1 \
        --parallel 1 --there 
        # --setParameters r_S=1.3693,r_A=0.224 \
        # --setParameterRanges r_S=0.01,50:r_A=-1,1 \
        # --redefineSignalPOIs r_S,r_A \
    done
fi
if [[ $MODE == "POSTFIT" ]]; then
    source utils/setup_cmssw.sh
    for CHANNEL in $CHANNELS
    do
        DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}"
        RESDIR=$DATACARD_OUTPUT/cmb
        WORKSPACE=${RESDIR}/workspace.root
        echo "[INFO] Printing fit result for category $(basename $RESDIR)"
        FILE=${RESDIR}/postfitshape.root
        echo ${RESDIR}/postfitshape.root
        FITFILE=${RESDIR}/fitDiagnostics.${ERA}.root
        combine \
            -n .$ERA \
            -M FitDiagnostics \
            -m 125 -d $WORKSPACE \
            --robustFit 1 -v1 \
            --robustHesse 1 \
            --X-rtd MINIMIZER_analytic \
            --cminDefaultMinimizerStrategy 0
        mv fitDiagnostics.${ERA}.root $FITFILE
        echo "[INFO] Building Prefit/Postfit shapes"
        PostFitShapesFromWorkspace -w ${WORKSPACE} \
            -m 125 -d ${RESDIR}/combined.txt.cmb \
            --output ${FILE} \
            -f ${FITFILE}:fit_s --postfit
        FILE=${RESDIR}/prefitshape.root
        PostFitShapesFromWorkspace -w ${WORKSPACE} \
            -m 125 -d ${RESDIR}/combined.txt.cmb \
            --output ${FILE}
    done
fi
if [[ $MODE == "PLOT" ]]; then
    source utils/setup_cvmfs_sft.sh
    source utils/setup_python.sh
    if [[ "all" == *"$CHANNELS" ]];then
        INPUT="output/datacard_output/${NTUPLE_TAG}/${SHAPE_TAG}/${ERA}_all/cmb/postfitshape.root"
        for CHANNEL in $CHANNELS
        do
            for CAT in pt_W_plus m_tt_plus pt_W_minus m_tt_minus
            do
                OUTPUT=plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}
                python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} --prefit 
                python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} 
            done
        done
    else 
        for CHANNEL in $CHANNELS
        do
            INPUT="${BASE_PATH}/${ERA}_${CHANNEL}/cmb/postfitshape.root"
            for CAT in pt_W_plus m_tt_plus pt_W_minus m_tt_minus
            do
                OUTPUT=plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}
                python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} --prefit 
                python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} 
            done
        done
    fi
fi
if [[ $MODE == "IMPACTS" ]]; then
    source utils/setup_cmssw.sh
    for CHANNEL in $CHANNELS
    do
        DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}/cmb"
        WORKSPACE=${DATACARD_OUTPUT}/workspace.root
        combineTool.py -M Impacts -d $WORKSPACE -m 125 \
            --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 \
            --doInitialFit --robustFit 1 \
            --parallel 16
        combineTool.py -M Impacts -d $WORKSPACE -m 125 \
            --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 \
            --robustFit 1 --doFits \
            --parallel 16
        combineTool.py -M Impacts -d $WORKSPACE -m 125 -o sm_mc_${ERA}_${CHANNEL}_impacts.json
        plotImpacts.py -i sm_mc_${ERA}_${CHANNEL}_impacts.json -o sm_mc_${ERA}_${CHANNEL}_impacts
        # cleanup the fit files
        rm higgsCombine*.root
        echo "sm_mc_${ERA}_${CHANNEL}_impacts.pdf $DATACARD_OUTPUT/."
        mv sm_mc_${ERA}_${CHANNEL}_impacts.pdf $DATACARD_OUTPUT/.
        mv sm_mc_${ERA}_${CHANNEL}_impacts.json $DATACARD_OUTPUT/.
        ls $DATACARD_OUTPUT/sm_mc_${ERA}_${CHANNEL}_impacts.pdf 
    done
fi