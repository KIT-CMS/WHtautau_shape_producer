
ERA=2018
CHANNEL="mmt"
NTUPLE_TAG="11_07_shifts_all_ch"
SHAPE_TAG="ptW_mtt"
SYNCED_DIR_EMT=output/shapes/${NTUPLE_TAG}/emt/${SHAPE_TAG}/synced_shapes
SYNCED_DIR_MMT=output/shapes/${NTUPLE_TAG}/mmt/${SHAPE_TAG}/synced_shapes
SYNCED_DIR_MET=output/shapes/${NTUPLE_TAG}/met/${SHAPE_TAG}/synced_shapes
SYNCED_DIR_ETT=output/shapes/${NTUPLE_TAG}/ett/${SHAPE_TAG}/synced_shapes
SYNCED_DIR_MTT=output/shapes/${NTUPLE_TAG}/mtt/${SHAPE_TAG}/synced_shapes
DATACARD_OUTPUT="output/datacard_output/${NTUPLE_TAG}/${SHAPE_TAG}/${ERA}_${CHANNEL}"

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
    --auto_rebin=true \
    --stxs_signals="stxs_stage0" \
    --categories="stxs_stage0" \
    --era=${ERA} \
    --output=${DATACARD_OUTPUT} \
    --use_automc=true \
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
    --PO '"map=^.*/rem_VH.?$:r_rem_VH[1,0.99,1.01]"' \
    --PO '"map=^.*/WHplus.?$:r_WHplus=expr;;r_WHplus(\"@0*(1+@1)/(2*0.8380)\",r_S[1.3693,0.01,5],r_A[0.224,-1,1])"' \
    --PO '"map=^.*/WHminus.?$:r_WHminus=expr;;r_WHminus(\"@0*(1-@1)/(2*0.5313)\",r_S,r_A)"' \
    # --PO 'map=.*/WHplus:r_WHplus=expr;;r_WHplus(\"@0*(1+@1)/(2*0.8380)\",r_S[1.3693,0.01,5],r_A[0.224,-1,1])' \
    # --PO 'map=.*/WHminus:r_WHminus=expr;;r_WHminus(\"@0*(1-@1)/(2*0.5313)\",r_S,r_A)' \
    # --PO '"map=^.*/WHplus.?$:r_WHplus[0.831,-200,200]"' \
    # --PO '"map=^.*/WHminus.?$:r_WHminus[0.527,-200,200]"'
    # --PO '"map=^.*/WH_htt.?$:r_VH[1,-5,7]"' \
    # --PO '"map=^.*/ZH_htt.?$:r_VH[1,-5,7]"'
    # --PO '"map=^.*/ggZH_had_htt.?$:r_ggH[1,-5,5]"' \
    # --PO '"map=^.*/WH_had_htt.?$:r_qqH[1,-5,5]"' \
    # --PO '"map=^.*/ZH_had_htt.?$:r_qqH[1,-5,5]"' \
    # --PO '"map=^.*/ggZH_lep_htt.?$:r_VH[1,-5,7]"'

source utils/setup_cmssw.sh
combineTool.py \
-M MultiDimFit \
-m 125 \
-d $DATACARD_OUTPUT/cmb/workspace.root \
--algo singles \
--robustFit 1 \
--X-rtd MINIMIZER_analytic \
--cminDefaultMinimizerStrategy 0 \
--setParameters r_S=1.3693,r_A=0.224 \
--setParameterRanges r_S=0.01,50:r_A=-1,1 \
--redefineSignalPOIs r_S,r_A \
-n $ERA -v1 \
-t -1 \
--parallel 1 --there 

for RESDIR in $DATACARD_OUTPUT/cmb; do
    echo "[INFO] Printing fit result for category $(basename $RESDIR)"
    FITFILE=${RESDIR}/higgsCombine${ERA}.MultiDimFit.mH125.root
    python print_fitresult.py ${FITFILE}
done
