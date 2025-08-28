# top level script for everything around the fit
MODE="$1"
#ERAS="2017 2018"
ERAS="2016preVFP 2016postVFP 2017 2018"
ERAS="all_eras"
CHANNELS="all"
CHANNELS="all"
NTUPLE_TAG="14_04_25_alleras_allch3"
SHAPE_TAG="10_05_25_nn_fitshapes"
FIT_TAG="CA_AS2"
BASE_PATH="output/datacard_output/${NTUPLE_TAG}/${SHAPE_TAG}_${FIT_TAG}"
ulimit -s unlimited
if [[ $MODE == "PRINT" ]]; then
    source utils/setup_cmssw.sh 
    for ERA in $ERAS
    do
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
done
fi
if [[ $MODE == "FIT" ]]; then
    source utils/setup_cmssw.sh
    for ERA in $ERAS
    do
        echo $ERA
        if [[ $ERA == "all_eras" ]]; then
            for CHANNEL in $CHANNELS
            do
                mkdir -p ${BASE_PATH}/all_eras_${CHANNEL}
                DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}"
                echo $MODE    
                source utils/setup_cmssw.sh 
                echo $DATACARD_OUTPUT/$CHANNEL
                combineTool.py -M T2W -o workspace.root -i $DATACARD_OUTPUT/cmb -m 125 \
                    -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
                    --PO verbose \
                    --PO '"map=^.*/ggZH.?$:r_ZH[1,0.99,1.01]"' \
                    --PO '"map=^.*/WH_h.*_plus.?$:r_WHplus=expr;;r_WHplus(\"@0*(1+@1)/(2*0.8380)\",r_S[1.3693,-5,5],r_A[0.224,-5,5])"' \
                    --PO '"map=^.*/WH_h.*_minus.?$:r_WHminus=expr;;r_WHminus(\"@0*(1-@1)/(2*0.5313)\",r_S,r_A)"' 

                combineTool.py \
                -M MultiDimFit \
                -m 125 \
                -d $DATACARD_OUTPUT/cmb/workspace.root \
                --algo singles \
                --robustFit 1 \
                --X-rtd MINIMIZER_analytic \
                --cminDefaultMinimizerStrategy 0 \
                --setParameters r_S=1.3693,r_A=0.224 \
                --setParameterRanges r_S=-5,5:r_A=-5,5 \
                --redefineSignalPOIs r_S,r_A \
                -n $ERA -v1 \
                --parallel 1 --there \
                -t -1 
                echo "${CHANNEL} done"
            done
        else
            echo "Huhu"
            SYNCED_DIR_EMT=output/shapes/${NTUPLE_TAG}/${ERA}/emt/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_MMT=output/shapes/${NTUPLE_TAG}/${ERA}/mmt/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_MET=output/shapes/${NTUPLE_TAG}/${ERA}/met/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_ETT=output/shapes/${NTUPLE_TAG}/${ERA}/ett/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_MTT=output/shapes/${NTUPLE_TAG}/${ERA}/mtt/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_LLT=output/shapes/${NTUPLE_TAG}/${ERA}/llt/${SHAPE_TAG}/synced_shapes
            SYNCED_DIR_LTT=output/shapes/${NTUPLE_TAG}/${ERA}/ltt/${SHAPE_TAG}/synced_shapes
            for CHANNEL in $CHANNELS
            do
                DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}"
                echo $MODE    
                source utils/setup_cmssw.sh    
                echo "hi $ERA"
                if timeout 260s ${CMSSW_BASE}/bin/slc7_amd64_gcc900/MorphingSMRun2Legacy \
                    --base_path=$PWD \
                    --input_folder_emt=$SYNCED_DIR_EMT \
                    --input_folder_met=$SYNCED_DIR_MET \
                    --input_folder_mmt=$SYNCED_DIR_MMT \
                    --input_folder_ett=$SYNCED_DIR_ETT \
                    --input_folder_mtt=$SYNCED_DIR_MTT \
                    --input_folder_llt=$SYNCED_DIR_LLT \
                    --input_folder_ltt=$SYNCED_DIR_LTT \
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
                then 
                echo "Iteration ${VARIABLE} completed successfully."
                else 
                    echo "Iteration ${VARIABLE} timed out, moving "
                fi
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
                if timeout 60s combineTool.py -M T2W -o workspace.root -i $DATACARD_OUTPUT/cmb -m 125 \
                    -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
                    --PO verbose \
                    --PO '"map=^.*/ggZH.?$:r_ZH[1,0.99,1.01]"' \
                    --PO '"map=^.*/WH_h.*_plus.?$:r_WHplus=expr;;r_WHplus(\"@0*(1+@1)/(2*0.8380)\",r_S[1.3693,-5,5],r_A[0.224,-5,5])"' \
                    --PO '"map=^.*/WH_h.*_minus.?$:r_WHminus=expr;;r_WHminus(\"@0*(1-@1)/(2*0.5313)\",r_S,r_A)"' 
                then 
                echo "Iteration ${VARIABLE} completed successfully."
                else 
                    echo "Iteration ${VARIABLE} timed out, moving "
                fi

                if timeout 60s combineTool.py \
                -M MultiDimFit \
                -m 125 \
                -d $DATACARD_OUTPUT/cmb/workspace.root \
                --algo singles \
                --robustFit 1 \
                --X-rtd MINIMIZER_analytic \
                --cminDefaultMinimizerStrategy 0 \
                --setParameters r_S=1.3693,r_A=0.224 \
                --setParameterRanges r_S=-5,5:r_A=-5,5 \
                --redefineSignalPOIs r_S,r_A \
                -n $ERA -v1 \
                --parallel 1 --there \
                -t -1 
                then 
                echo "Iteration ${VARIABLE} completed successfully."
                else 
                    echo "Iteration ${VARIABLE} timed out, moving "
                fi
                echo "${CHANNEL} done"
                mv higgsCombine${ERA}.MultiDimFit.mH125.root $DATACARD_OUTPUT/cmb/.
                # --setParameters r_S=1.3693,r_A=0.224 \
                # --setParameterRanges r_S=0.01,50:r_A=-1,1 \
                # --redefineSignalPOIs r_S,r_A \
            done
        fi
    done
fi
if [[ $MODE == "COMBINE_ERAS" ]]; then
    for CHANNEL in $CHANNELS
    do
        if [[ $CHANNEL == "all" ]]; then
            OUTDIR=${BASE_PATH}/all_eras_${CHANNEL}/cmb
            for ERA in ${ERAS}
            do
                DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}/cmb"
                mkdir -p $OUTDIR/common
                cp ${DATACARD_OUTPUT}/htt_*.txt $OUTDIR
                cp ${DATACARD_OUTPUT}/common/htt_input_${ERA}.root $OUTDIR/common
            done
        else
            OUTDIR=${BASE_PATH}/all_eras_${CHANNEL}/cmb
            for ERA in ${ERAS}
            do
                DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}/cmb"
                mkdir -p $OUTDIR/common
                cp ${DATACARD_OUTPUT}/htt_*.txt $OUTDIR
                cp ${DATACARD_OUTPUT}/common/htt_input_${ERA}.root $OUTDIR/common
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
            --setParameters r_S=1.3693,r_A=0.224 \
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
    source utils/setup_root.sh
    source utils/setup_python.sh
    if [[ "all" == *"$CHANNELS" ]];then
        for ERA in $ERAS
        do
        INPUT="output/datacard_output/${NTUPLE_TAG}/${SHAPE_TAG}_${FIT_TAG}/${ERA}_all/cmb/postfitshape.root"
        for CHANNEL in $CHANNELS
        do
            if [[ $CHANNEL == "all" ]]; then
                continue
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
        # if [[ "$ERA" == "2016preVFP" || "$ERA" == "2016postVFP" ]]; then
        #     for CHANNEL in $CHANNELS
        #     do
        #         INPUT="${BASE_PATH}/${ERA}_${CHANNEL}/cmb/postfitshape.root"
        #         for CAT in all_cats_minus all_cats_plus
        #         do
        #             OUTPUT=plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}
        #             python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} --prefit 
        #             python plotting/plot_prefit_postfit.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} 
        #         done
        #     done
        # else
            for CHANNEL in $CHANNELS
            do
                if [[ $CHANNEL == "all" ]]; then
                    continue
                fi
                for PREPOST in prefit postfit
                do
                    INPUT="${BASE_PATH}/${ERA}_${CHANNEL}/cmb/${PREPOST}shape.root"
                    for CAT in sig_nn_signal_minus misc_nn_signal_plus #misc_nn_signal_minus diboson_nn_signal_plus diboson_nn_signal_minus
                    do
                        OUTPUT=plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}_${FIT_TAG}
                        python plotting/plot_prefit_postfit_sigstacked.py --category ${CAT} --era ${ERA} --input ${INPUT} --channels ${CHANNEL} --output ${OUTPUT} --prepost ${PREPOST} 
                    done
                done
            done
        #fi
    done
    fi
fi
if [[ $MODE == "IMPACTS" ]]; then
    source utils/setup_cmssw.sh
    #CHANNELS="llt"
    #ERAS="2016postVFP"
    for ERA in $ERAS
    do
    for CHANNEL in $CHANNELS
    do
        DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}/cmb"
        WORKSPACE=${DATACARD_OUTPUT}/workspace.root
        echo "huuu"
        # echo $WORKSPACE
        combineTool.py -M Impacts -d $WORKSPACE -m 125 --doInitialFit -t -1 --setParameters r_S=1.3693,r_A=0.224,r_ZH=1 --setParameterRanges r_S=0,10:r_A=-1,1 --redefineSignalPOIs r_A --freezeParameters r_ZH --parallel 16 

        combineTool.py -M Impacts -d $WORKSPACE -m 125 --doFits -t -1 --setParameters r_S=1.3693,r_A=0.224,r_ZH=1 --setParameterRanges r_S=0,10:r_A=-1,1 --redefineSignalPOIs r_A  --freezeParameters r_ZH --parallel 16  #--job-mode=condor

        combineTool.py -M Impacts -d $WORKSPACE -m 125 -t -1 -o sm_mc_${ERA}_${CHANNEL}_impacts.json --setParameters r_S=1.3693,r_A=0.224,r_ZH=1 --setParameterRanges r_S=0,10:r_A=-1,1 --redefineSignalPOIs r_A --freezeParameters r_ZH
        # combineTool.py -M Impacts -d $WORKSPACE -m 125 \
        #     --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 \
        #     --doInitialFit --robustFit 1 \
        #     --parallel 16 \
        #     --setParameters r_S=1.3693,r_A=0.224 \
        #     --setParameterRanges r_S=0.01,50:r_A=-1,1 \
        #     --redefineSignalPOIs r_S,r_A 

        # combineTool.py -M Impacts -d $WORKSPACE -m 125 \
        #     --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 \
        #     --robustFit 1 --doFits \
        #     --parallel 16 \
        #     --setParameters r_S=1.3693,r_A=0.224 \
        #     --setParameterRanges r_S=0.01,50:r_A=-1,1 \
        #     --redefineSignalPOIs r_S,r_A

        combineTool.py -M Impacts -d $WORKSPACE -m 125 -o $DATACARD_OUTPUT/sm_mc_${ERA}_${CHANNEL}_impacts.json --setParameters r_S=1.3693,r_A=0.224 \
            --setParameterRanges r_S=0.01,50:r_A=-1,1 \
            --redefineSignalPOIs r_S,r_A 
        plotImpacts.py -i $DATACARD_OUTPUT/sm_mc_${ERA}_${CHANNEL}_impacts.json -o $DATACARD_OUTPUT/sm_mc_${ERA}_${CHANNEL}_impacts
        # cleanup the fit files
        #rm higgsCombine*.root
        echo "sm_mc_${ERA}_${CHANNEL}_impacts.pdf $DATACARD_OUTPUT/."
        mv sm_mc_${ERA}_${CHANNEL}_impacts.pdf $DATACARD_OUTPUT/.
        mv sm_mc_${ERA}_${CHANNEL}_impacts.json $DATACARD_OUTPUT/.
        ls $DATACARD_OUTPUT/sm_mc_${ERA}_${CHANNEL}_impacts.pdf 
    done
    done
fi
if [[ $MODE == "UNC_SPLIT" ]]; then
    source utils/setup_cmssw.sh
    ERA="all_eras"
    DATACARD_OUTPUT="${BASE_PATH}/${ERA}_all/cmb"
    DATACARD=${DATACARD_OUTPUT}/combined.txt.cmb
    # this can be check by checking if "theory group" can be found in the card. If not, add the groups
    # if ! grep -q "theory group" $DATACARD; then
    #     echo "Adding MC unc groups to datacard"
    #     cat uncertainty_groups_alleras.txt >> $DATACARD
    # fi
    #cat $DATACARD 
    echo $DATACARD 
    combineTool.py -M T2W -o workspace.root -i $DATACARD -m 125 \
                    -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
                    --PO '"map=^.*/ZH.?$:r_ZH[1,0.99,1.01]"' \
                    --PO '"map=^.*/WH_h.*_plus.?$:r_WHplus=expr;;r_WHplus(\"@0*(1+@1)/(2*0.8380)\",r_S[1.3693,0.01,5],r_A[0.224,-1,1])"' \
                    --PO '"map=^.*/WH_h.*_minus.?$:r_WHminus=expr;;r_WHminus(\"@0*(1-@1)/(2*0.5313)\",r_S,r_A)"' 
    #cat $DATACARD
    POIS=("r_A")
    RESULTFOLDER=$DATACARD_OUTPUT/unc_split/

    mkdir -p $RESULTFOLDER
    echo "Will run fit for POIs: ${POIS[@]}"
    # # loop though the POIs and run the fit
    for POI in ${POIS[@]}; do
        combine -M MultiDimFit $DATACARD_OUTPUT/workspace.root -n .snapshot -m 125 --saveWorkspace --redefineSignalPOIs $POI -t -1 --setParameters r_A=0.224 --robustFit 1 \
                --X-rtd MINIMIZER_analytic \
                --cminDefaultMinimizerStrategy 0 \

        combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .nominal -m 125 --algo grid --snapshotName MultiDimFit --redefineSignalPOIs $POI --points 20 --setParameters r_A=0.224 -t -1 --robustFit 1 \
                --X-rtd MINIMIZER_analytic \
                --cminDefaultMinimizerStrategy 0 \

        # combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .freezebbb -m 125 --algo grid --freezeNuisanceGroups autoMCStats --snapshotName MultiDimFit --redefineSignalPOIs $POI --points 20 --setParameters r_A=0.224 -t -1

        # echo " -----------------"
        # echo "syst"
        # echo " -----------------"

        # combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .freezesyst -m 125 --algo grid --freezeNuisanceGroups autoMCStats,syst --snapshotName MultiDimFit --redefineSignalPOIs $POI --points 20 --setParameters r_A=0.224 -t -1

        # echo " -----------------"
        # echo "theory"
        # echo " -----------------"

        # combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .freezetheory -m 125 --algo grid --freezeNuisanceGroups syst,theory,autoMCStats --snapshotName MultiDimFit --redefineSignalPOIs $POI  --points 20 --setParameters r_A=0.224 -t -1

        combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH125.root -n .freezeall -m 125 --algo grid --freezeParameters allConstrainedNuisances --snapshotName MultiDimFit --redefineSignalPOIs $POI --points 20 --setParameters r_A=0.224 -t -1 --robustFit 1 \
                --X-rtd MINIMIZER_analytic \
                --cminDefaultMinimizerStrategy 0 \

        outputname=freeze_${POI}_mc

        echo " -----------------"
        echo "plot"
        echo " -----------------"
        plot1DScan.py higgsCombine.nominal.MultiDimFit.mH125.root --POI $POI --others higgsCombine.freezeall.MultiDimFit.mH125.root:"Stat. only":2 -o ${outputname} --breakdown syst,stat --y-max 4  #--x-range 0,2
        # plot1DScan.py higgsCombine.nominal.MultiDimFit.mH125.root --POI $POI --others higgsCombine.freezebbb.MultiDimFit.mH125.root:"freeze bbb":4 higgsCombine.freezesyst.MultiDimFit.mH125.root:"freeze bbb + syst":6 higgsCombine.freezetheory.MultiDimFit.mH125.root:"freeze bbb + syst + theo":7 higgsCombine.freezeall.MultiDimFit.mH125.root:"Stat. only":2 -o ${outputname} --breakdown bbb,syst,theory,rest,stat --y-max 4  #--x-range 0,2
        #--json $outputname.json

        # move all output files to the result folder
        echo "Moving output files to $RESULTFOLDER"
        mv higgsCombine* $RESULTFOLDER
        mv ${outputname}.pdf $RESULTFOLDER
        mv ${outputname}.png $RESULTFOLDER
        mv ${outputname}.root $RESULTFOLDER
    done
fi
if [[ $MODE == "SCAN" ]]; then
source utils/setup_cmssw.sh
for ERA in $ERAS
do
for CHANNEL in $CHANNELS
do
DATACARD_OUTPUT="${BASE_PATH}/${ERA}_${CHANNEL}"
combineTool.py -M MultiDimFit \
    -m 125 \
    -d $DATACARD_OUTPUT/cmb/workspace.root \
    --algo grid \
    --points 50 \
    --setParameters cross_section_VV=0.75 \
    --setParameterRanges cross_section_VV=-2.5,2.5 \
    --redefineSignalPOIs cross_section_VV \
    --cminDefaultMinimizerStrategy 0 \
    --cminFallbackAlgo Minuit2,0:0.2 \
    -n cross_section_VV -v2
outputname="scan"
plot1DScan.py higgsCombinecross_section_VV.MultiDimFit.mH125.root --POI cross_section_VV -o $DATACARD_OUTPUT/$outputname --y-max 4 
done 
done 
fi