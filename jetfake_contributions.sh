source utils/setup_root.sh
source utils/setup_python.sh
NTUPLE_TAG="15_03_24_triggermatchDR05_alleras_allch"
SHAPE_TAG="control_shapes_16_04_24"
ERAS="2018" #"2016preVFP 2016postVFP 2017 2018"
CHANNELS="met emt"
for ERA in $ERAS
do
for CHANNEL in $CHANNELS
do
    echo $CHANNEL
    INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/control.root"
    OUTPUT="plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/"
    mkdir -p plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/
    python jetfake_contributions.py --input ${INPUT} --plot_output ${OUTPUT} --channel ${CHANNEL}
done
done