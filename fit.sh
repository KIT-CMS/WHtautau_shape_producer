# MODE options are: PRINT (print fit results), FIT, POSTFIT (produces postfit and prefit shapes), PLOT, IMPACTS
MODE="$1"
CHANNELS="all" #"ett mtt emt mmt all"
ERAS="all_eras" #"2016preVFP 2016postVFP 2017 2018"
#NTUPLE_TAG="11_07_shifts_all_ch"
NTUPLE_TAG="03_11_23_allch_alleras_shifts"
SHAPE_TAG="fit_shapes_ssTight_osTight_emt_met_comb_2016combcats"
BASE_PATH="output/datacard_output/${NTUPLE_TAG}/${SHAPE_TAG}"
ulimit -s unlimited
if [[ $MODE == "COMBINE_ERAS" ]]; then
    for CHANNEL in $CHANNELS
    do
        if [[ $CHANNEL == "all" ]]; then
            OUTDIR=${BASE_PATH}/all_eras_${CHANNEL}_autorebin/cmb
            for ERA in ${ERAS}
            do
                DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}_autorebin/cmb"
                mkdir -p $OUTDIR/common
                cp ${DATACARD_OUTPUT}/htt_*.txt $OUTDIR
                cp ${DATACARD_OUTPUT}/common/htt_input_${ERA}.root $OUTDIR/common
            done
        else
            OUTDIR=${BASE_PATH}/all_eras_${CHANNEL}_autorebin/cmb
            for ERA in ${ERAS}
            do
                DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}_autorebin/cmb"
                mkdir -p $OUTDIR/common
                cp ${DATACARD_OUTPUT}/htt_*.txt $OUTDIR
                cp ${DATACARD_OUTPUT}/common/htt_input_${ERA}.root $OUTDIR/common
            done
        fi
    done 
fi
if [[ $MODE == "PRINT" ]]; then
    source utils/setup_cmssw.sh 
    for ERA in $ERAS
    do
    for CHANNEL in $CHANNELS
    do
        DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}_autorebin"
        echo $MODE
        for RESDIR in $DATACARD_OUTPUT/cmb; do
                echo "[INFO] Printing fit result for category $(basename $RESDIR)"
                FITFILE=${RESDIR}/higgsCombine${ERA}.MultiDimFit.mH125.root
                python print_fitresult.py ${FITFILE}
        done
    done
done
fi
if [[ $MODE == "FIT" ]]; then
    for ERA in $ERAS
    do
        if [[ $ERA == "all_eras" ]]; then
            for CHANNEL in $CHANNELS
            do
                DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}_autorebin"
                echo $MODE    
                source utils/setup_cmssw.sh 
                echo $DATACARD_OUTPUT/$CHANNEL
                combineTool.py -M T2W -o workspace.root -i $DATACARD_OUTPUT/cmb -m 125 \
                    -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
                    --PO verbose \
                    --PO 'map=.*/WHplus.?$:r[1,-10,10]' \
                    --PO 'map=.*/WHminus.?$:r'
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
                --parallel 1 --there \
                -t -1 
                echo "${CHANNEL} done"
            done
        else
            SYNCED_DIR_EMT=output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_MMT=output/shapes/${NTUPLE_TAG}/${ERA}/mmt/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_MET=output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_ETT=output/shapes/${NTUPLE_TAG}/${ERA}/ett/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_MTT=output/shapes/${NTUPLE_TAG}/${ERA}/mtt/${SHAPE_TAG}/synced_shapes
            for CHANNEL in $CHANNELS
            do
                DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}"
                echo $MODE    
                source utils/setup_cmssw.sh    
                echo "hi $ERA"
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
                    --auto_rebin=true \
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
                echo "huhu"
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
                --parallel 1 --there \
                -t -1 
                echo "${CHANNEL} done"

                # --setParameters r_S=1.3693,r_A=0.224 \
                # --setParameterRanges r_S=0.01,50:r_A=-1,1 \
                # --redefineSignalPOIs r_S,r_A \
            done
        fi
    done
fi
if [[ $MODE == "POSTFIT" ]]; then
    source utils/setup_cmssw.sh
    for ERA in $ERAS
    do
    for CHANNEL in $CHANNELS
    do
        DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}_autorebin"
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
    done
fi
if [[ $MODE == "PLOT" ]]; then
    source utils/setup_cvmfs_sft.sh
    source utils/setup_python.sh
    if [[ "all" == *"$CHANNELS" ]];then
        for ERA in $ERAS
        do
        INPUT="output/datacard_output/${NTUPLE_TAG}/${SHAPE_TAG}/${ERA}_all/cmb/postfitshape.root"
        for CHANNEL in $CHANNELS
        do
            if [[ $CHANNEL == "all" ]]; then
            exit 0
            fi
            for CAT in control_plus_high_ptw control_plus_low_ptw control_minus_high_ptw control_minus_low_ptw sig_plus sig_minus
            do
                OUTPUT=plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}
                python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} --prefit 
                python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} 
            done
        done
        done
    else 
    for ERA in $ERAS
    do
        if [[ "$ERA" == "2016preVFP" || "$ERA" == "2016postVFP" ]]; then
            for CHANNEL in $CHANNELS
            do
                INPUT="${BASE_PATH}/${ERA}_${CHANNEL}_autorebin/cmb/postfitshape.root"
                for CAT in all_cats_minus all_cats_plus
                do
                    OUTPUT=plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}_autorebin
                    python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} --prefit 
                    python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} 
                done
            done
        else
            for CHANNEL in $CHANNELS
            do
                INPUT="${BASE_PATH}/${ERA}_${CHANNEL}_autorebin/cmb/postfitshape.root"
                for CAT in control_minus control_plus sig_plus sig_minus
                do
                    OUTPUT=plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}_autorebin
                    python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} --prefit 
                    python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} 
                done
            done
        fi
    done
    fi
fi
if [[ $MODE == "IMPACTS" ]]; then
    source utils/setup_cmssw.sh
    CHANNELS="all"
    for ERA in $ERAS
    do
    for CHANNEL in $CHANNELS
    do
        DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}_autorebin/cmb"
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
    done
fi
if [[ $MODE == "UNC_SPLIT" ]]; then
    source utils/setup_cmssw.sh
    DATACARD_OUTPUT="${BASE_PATH}/${ERA}_all/cmb"
    DATACARD=${DATACARD_OUTPUT}/combined.txt.cmb
    # this can be check by checking if "theory group" can be found in the card. If not, add the groups
    if ! grep -q "theory group" $DATACARD; then
        echo "Adding MC unc groups to datacard"
        cat uncertainty_groups_2017.txt >> $DATACARD
    fi
    combineTool.py -M T2W -o workspace.root -i $DATACARD -m 125 \
                -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
                --PO verbose \
                --PO 'map=.*/WHplus.?$:r[1,-10,10]' \
                --PO 'map=.*/WHminus.?$:r'
    POIS=("r")
    RESULTFOLDER=$DATACARD_OUTPUT/unc_split/

    mkdir -p $RESULTFOLDER
    echo "Will run fit for POIs: ${POIS[@]}"
    # # loop though the POIs and run the fit
    for POI in ${POIS[@]}; do
        combine -M MultiDimFit $DATACARD_OUTPUT/workspace.root -n .snapshot -m 125 --saveWorkspace --redefineSignalPOIs $POI -t -1 --setParameters r=1.0 
        # combineTool.py \
        # -M MultiDimFit \
        # -m 125 \
        # -d $DATACARD_OUTPUT/cmb/workspace.root \
        # --algo singles \
        # --robustFit 1 \
        # --X-rtd MINIMIZER_analytic \
        # --cminDefaultMinimizerStrategy 0 \
        # --setParameters r=1.0 \
        # --setParameterRanges r=-10,10 \
        # --redefineSignalPOIs r \
        # -n $ERA -v1 \
        # -t -1 \
        # --parallel 1 --there 
        combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .nominal -m 125 --algo grid --snapshotName MultiDimFit --redefineSignalPOIs $POI --points 20 --setParameters r=1.0 -t -1

        combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .freezebbb -m 125 --algo grid --freezeNuisanceGroups autoMCStats --snapshotName MultiDimFit --redefineSignalPOIs $POI --points 20 --setParameters r=1.0 -t -1

        combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .freezesyst -m 125 --algo grid --freezeNuisanceGroups autoMCStats,syst --snapshotName MultiDimFit --redefineSignalPOIs $POI --points 20 --setParameters r=1.0 -t -1

        combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .freezetheory -m 125 --algo grid --freezeNuisanceGroups syst,theory,autoMCStats --snapshotName MultiDimFit --redefineSignalPOIs $POI  --points 20 --setParameters r=1.0 -t -1

        combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .freezeall -m 125 --algo grid --freezeParameters allConstrainedNuisances --snapshotName MultiDimFit --redefineSignalPOIs $POI --points 20 --setParameters r=1.0 -t -1

        outputname=freeze_${POI}_mc
        plot1DScan.py higgsCombine.nominal.MultiDimFit.mH125.root --POI $POI --others higgsCombine.freezebbb.MultiDimFit.mH125.root:"freeze bbb":4 higgsCombine.freezesyst.MultiDimFit.mH125.root:"freeze bbb + syst":6 higgsCombine.freezetheory.MultiDimFit.mH125.root:"freeze bbb + syst + theo":7 higgsCombine.freezeall.MultiDimFit.mH125.root:"Stat. only":2 -o ${outputname} --breakdown bbb,syst,theory,rest,stat --y-max 4  #--x-range 0,2
        #--json $outputname.json

        # move all output files to the result folder
        echo "Moving output files to $RESULTFOLDER"
        mv higgsCombine* $RESULTFOLDER
        mv ${outputname}.pdf $RESULTFOLDER
        mv ${outputname}.png $RESULTFOLDER
        mv ${outputname}.root $RESULTFOLDER
    done
fi